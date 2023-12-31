from discord.ext import commands
from discord.ext.commands import Context, CommandError

from config.config import Config

from logger import logger


class Base(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Loaded {self.__class__.__name__} commands.")


class Basics(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    # @commands.has_permissions(manage_guild=True)
    @commands.command(name="sync")
    async def sync(self, context: Context):
        guild = context.guild
        logger.info("Running sync command")

        if (not context.author.guild_permissions.administrator or
            not context.author.guild_permissions.manage_guild):
            raise Exception("You do not have permission to run this command")

        fmt = await self.__bot.tree.sync(guild=context.guild)
        await context.channel.send(
            f"Synced {len(fmt)} commands to the current guild."
        )
        logger.info(f"The guild {guild.name} with id {guild.id} synced successfully")

    @sync.error
    async def sync_error(self, context: Context, errors: CommandError) -> None:
        guild = context.guild
        if errors or isinstance(errors, commands.MissingPermissions):
            await context.send(
                f"The guild {guild.name} with id {guild.id} couldn't sync {str(errors)}",
                ephemeral=True
            )
            logger.error(f"[ERROR]: {errors}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot), guilds=bot.guilds)
