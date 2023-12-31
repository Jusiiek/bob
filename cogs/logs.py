import discord
from discord import app_commands, Interaction
from discord.ext import commands

from config.config import Config
from config.config_keys import ChannelsKeys, RolesKeys
from config.environment import SERVER_ID


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    async def cog_check(self, ctx):
        owner_id = ctx.guild.owner_id

        return (ctx.author.guild_permissions.administrator or
                ctx.author.guild_permissions.manage_guild or
                owner_id == ctx.author.id
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(Logs(bot), guilds=bot.guilds)
