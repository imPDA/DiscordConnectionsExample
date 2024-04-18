import asyncio
import json
from typing import Literal

import discord
import ezcord

import environ
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
from discord import app_commands, Interaction
from discord.app_commands import AppCommand
from punq import Container

from init import init_container
from settings.settings import Settings

# env = environ.Env()


class Bot(ezcord.Bot):
    def __init__(self, settings: Settings):
        super().__init__(
            intents=discord.Intents.default(),
            status=discord.Status.idle,
            activity=discord.Game(name="Testing..."),
        )
        self.settings = settings

    async def setup_hook(self):
        await super().setup_hook()

        cmds: list[AppCommand] = await self.tree.sync(
            guild=self.get_guild(1164631376956489858)
        )

        if cmds:
            self.add_ready_info(
                f"Commands synced ({len(cmds)})",
                "\n".join([cmd.name for cmd in cmds])
            )


@app_commands.guilds(1164631376956489858, )
class CommandsCog(ezcord.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot=bot)

        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bot.settings.kafka.bootstrap_servers  # env("KAFKA_BOOTSTRAP_SERVERS")
        )

    async def cog_load(self) -> None:
        try:
            await self.producer.start()
        except KafkaConnectionError:
            await asyncio.sleep(10)
            await self.producer.start()

    async def cog_unload(self) -> None:
        await self.producer.stop()

    @app_commands.command()
    async def set_info(
        self,
        interaction: Interaction,
        age: int = None,
        sex: Literal['male', 'female'] = None,
        favourite_number: int = None,
        favourite_animal: str = None
    ) -> None:
        # Send message to the broker
        message = {
            "age": age,
            "sex": sex,
            "favourite_number": favourite_number,
            "favourite_animal": favourite_animal
        }
        await self.producer.send_and_wait(
            topic=self.bot.settings.kafka.new_metadata_topic,  # env("KAFKA_NEW_METADATA_TOPIC"),
            value=json.dumps(message).encode(),
            key=str(interaction.user.id).encode(),
        )
        # Send message to indicate success
        await interaction.response.send_message("Done :)", ephemeral=True)

    @set_info.error
    async def set_info_error(self, interaction: Interaction, error) -> None:
        # TODO log the exception
        await interaction.response.send_message(f"Something went wrong :(", ephemeral=True)


async def main() -> None:
    container: Container = init_container()
    settings: Settings = container.resolve(Settings)

    bot = Bot(settings=settings)

    await bot.add_cog(CommandsCog(bot))
    await bot.start(settings.discord_token)  # env("TOKEN")


if __name__ == "__main__":
    asyncio.run(main())
    # TODO graceful shutdown
