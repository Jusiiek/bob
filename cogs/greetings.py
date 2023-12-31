import discord
from discord.ext import commands
from discord import app_commands, Interaction

from cogs.base import Base
from config.environment import SERVER_ID
from config.config import Config


class Greetings(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    @app_commands.command(name='set_welcomes_channel', description='Set welcomes channel')
    async def set_welcomes_channel(self, interaction: Interaction, channel: discord.TextChannel):
        await interaction.response.send_message(content="Not implemented yet!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot), guilds=bot.guilds)
