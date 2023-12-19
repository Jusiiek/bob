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
        guild_id = ctx.guild.id
        owner_id = ctx.guild.owner_id

        if owner_id == ctx.author.id:
            return True
        else:
            return (self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value) \
                    and any(role.id for role in ctx.author.roles) in \
                    zip(self.__config.get_config_value(guild_id, RolesKeys.ADMINISTRATORS_ROLES.value),
                        self.__config.get_config_value(guild_id, RolesKeys.MODERATORS_ROLES.value)
                        )
                    )

    @app_commands.command(name='set_rules_channel', description='Set rules channel')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def set_welcomes_channel(self, interaction: Interaction, channel: discord.TextChannel):
        self.__config.set_config(
            ChannelsKeys.RULES_CHANNEL.value,
            channel.id
        )

        await interaction.response.send_message(
            "Successfully set new rules channel",
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logs(bot))
