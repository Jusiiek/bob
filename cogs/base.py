from discord.ext import commands
from discord.ext.commands import Context

from config.config import Config
from config.config_keys import RolesKeys


class Base(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Loaded {self.__class__.__name__} commands.")


class Basics(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    @commands.command(name="sync")
    async def sync(self, context: Context):
        guild_id = context.guild.id
        if not self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value):
            return await context.channel.send(
                "It looks like you haven't configured the admin key.\n" +
                "Use 'set_admins' command to create admins list or add new admin to the list"
            )
        print("Running sync command")
        user_roles = [role.id for role in context.author.roles]
        allowed_roles = self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value)

        if any(role_id in allowed_roles for role_id in user_roles):
            fmt = await self.__bot.tree.sync(guild=context.guild)
            await context.channel.send(
                f"Synced {len(fmt)} commands to the current guild."
            )
        else:
            await context.channel.send("You have not permission to execute this command")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))
