from typing import Literal

import discord
import ezcord

import environ
from discord import app_commands, Interaction

env = environ.Env()


bot = ezcord.Bot(
    intents=discord.Intents.default(),
    status=discord.Status.idle,
    activity=discord.Game(name="Testing..."),
)


class CommandsCog(ezcord.Cog):
    @app_commands.command()
    async def set_info(
        self,
        interaction: Interaction,
        nickname: str = None,
        date_of_birth: str = None,
        sex: Literal['male', 'female'] = None,
        favourite_number: int = None,
        favourite_animal: str = None
    ) -> None:
        await interaction.response.send_message("Done", ephemeral=True)

        


if __name__ == "__main__":
    bot.run(env('TOKEN'))
    # TODO graceful shutdown
