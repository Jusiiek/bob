import asyncio

import discord
from discord import app_commands, Interaction
from discord.ext import commands

from config.config import Config
from config.config_keys import RolesKeys
from config.environment import SERVER_ID


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    async def cog_check(self, ctx):
        guild_id = ctx.guild.id
        owner_id = ctx.guild.owner_id

        if owner_id == ctx.author.id:
            return True
        else:
            return (self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value) \
            and any(role.id for role in ctx.author.roles) in \
            self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value))

    @app_commands.command(name='set_admins', description='Set list of admin roles')
    @app_commands.choices(choices=[
        app_commands.Choice(name="Set admins", value="set_admins"),
        app_commands.Choice(name="Add admins", value="add_admins")
    ])
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def set_admins(
        self,
        interaction: Interaction,
        roles: commands.Greedy[discord.Role],
        command: app_commands.Choice[str]
    ):
        guild_id = interaction.guild_id
        roles = [role.id for role in roles]

        match command:
            case "set_admins":
                self.__config.set_config(
                    guild_id,
                    RolesKeys.ADMINISTRATORS_ROLES.value,
                    roles
                )
                await interaction.response.send_message(
                    "Successfully set new rules admins",
                    ephemeral=True
                )
            case "add_admins":
                for role in roles:
                    self.__config.add_value_to_array_config_value(
                        guild_id,
                        RolesKeys.ADMINISTRATORS_ROLES.value,
                        role
                    )
                await interaction.response.send_message(
                    "Successfully added new admins",
                    ephemeral=True
                )

    @app_commands.command(name='set_moderators', description='Set rules channel')
    @app_commands.choices(choices=[
        app_commands.Choice(name="Set moderators", value="set_moderators"),
        app_commands.Choice(name="Add moderators", value="add_moderators")
    ])
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def set_welcomes_channel(
            self,
            interaction: Interaction,
            roles: commands.Greedy[discord.Role],
            command: app_commands.Choice[str]
    ):
        guild_id = interaction.guild_id
        roles = [role.id for role in roles]

        match command:
            case "set_moderators":
                self.__config.set_config(
                    guild_id,
                    RolesKeys.MODERATORS_ROLES.value,
                    roles
                )
                await interaction.response.send_message(
                    "Successfully set new rules moderators",
                    ephemeral=True
                )
            case "add_moderators":
                for role in roles:
                    self.__config.add_value_to_array_config_value(
                        guild_id,
                        RolesKeys.MODERATORS_ROLES.value,
                        role
                    )
                await interaction.response.send_message(
                    "Successfully added new moderators",
                    ephemeral=True
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
