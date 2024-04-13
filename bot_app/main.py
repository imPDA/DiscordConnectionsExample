import discord
import ezcord

import environ

env = environ.Env()


bot = ezcord.Bot(
    intents=discord.Intents.default(),
    status=discord.Status.idle,
    activity=discord.Game(name="Testing..."),
)


if __name__ == "__main__":
    bot.run(env('TOKEN'))
    # TODO graceful shutdown
