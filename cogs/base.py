import asyncio

from discord.ext import commands
from discord.ext.commands import Context

from config.environment import SERVER_ID
from config.config import Config
from config.config_keys import ConfigKeys


class Base(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Loaded {self.__class__.__name__} commands.")


class Basics(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    @commands.command(name="set_admins")
    async def set_admins(self, context: Context):
        if (self.__config.get_config_value(ConfigKeys.ADMINISTRATORS_ROLES.value) \
                and any(role.id for role in context.author.roles) in \
                self.__config.get_config_value(ConfigKeys.ADMINISTRATORS_ROLES.value)):
            return await context.channel.send(
                "I'm sorry, but looks like you don't have permission"
            )

        await context.channel.send(
            "Hello. To set a list of admins use belows examples.\n"
            "```\n"
            "set_admins | @role1 @role2"
            "```\n"
            "or if you already created a list of admins use\n"
            "```\n"
            "add_admins | @role1 @role2"
            "```\n"
        )

        try:
            command = await self.__bot.wait_for(
                "message",
                check=lambda m: m.author == context.author and m.channel == context.channel,
                timeout=60.0
            )
        except asyncio.TimeoutError:
            await context.channel.send("Ouch, never mind then. :sweat_smile: ")

        else:
            print(command.content)
            command, role_mentions_text = command.content.split("|")
            command = command.replace(" ", "")
            role_mentions = [
                int(role.strip('<@&>').strip('>')) for role in role_mentions_text.split(" ")
                if role != ""
            ]

            match command:
                case "set_admins":
                    self.__config.set_config(
                        ConfigKeys.ADMINISTRATORS_ROLES.value,
                        role_mentions
                    )
                case "add_admins":
                    for role in role_mentions:
                        self.__config.add_value_to_array_config_value(
                            ConfigKeys.ADMINISTRATORS_ROLES.value,
                            role
                        )
                case _:
                    await context.channel.send("Invalid command")

    @commands.command(name="sync")
    async def sync(self, context: Context):
        if not self.__config.get_config_value(ConfigKeys.ADMINISTRATORS_ROLES.value):
            return await context.channel.send(
                "It looks like you haven't configured the admin key.\n" +
                "Use 'set_admins' command to create admins list or add new admin to the list"
            )
        print("Running sync command")
        user_roles = [role.id for role in context.author.roles]
        allowed_roles = self.__config.get_config_value(ConfigKeys.ADMINISTRATORS_ROLES.value)

        if any(role_id in allowed_roles for role_id in user_roles):
            fmt = await self.__bot.tree.sync(guild=context.guild)
            await context.channel.send(
                f"Synced {len(fmt)} commands to the current guild."
            )
        else:
            await context.channel.send("You have not permission to execute this command")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))
