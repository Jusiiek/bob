import discord
from discord.ext import commands
from discord import app_commands, Interaction

from cogs.base import Base
from config.config import Config


class Rules(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    @app_commands.command(name='set_rules_channel', description='Set rules channel')
    async def set_welcomes_channel(self, interaction: Interaction, channel: discord.TextChannel):
        await interaction.response.send_message(content="Not implemented yet!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Rules(bot), guilds=bot.guilds)
