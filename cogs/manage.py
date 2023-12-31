import datetime

import discord
from discord import app_commands, Interaction
from discord.ext import commands

from config.config import Config


class Manage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    async def cog_check(self, ctx):
        owner_id = ctx.guild.owner_id

        return (ctx.author.guild_permissions.administrator or
                ctx.author.guild_permissions.manage_guild or
                owner_id == ctx.author.id
                )

    def _get_embed(self, title: str, description: str) -> discord.Embed:
        avatar = self.__bot.user.avatar
        embed = discord.Embed(
            title=f'{avatar} {title} {avatar}',
            description=description,
            colour=discord.Colour.dark_blue()
        )
        return embed

    @app_commands.command(
        name='create_role',
        description='Create new role'
    )
    async def create_role(
        self,
        interaction: Interaction,
        name: str = '',
        copy_roles_from_roles: str = ''
    ):
        embed = self._get_embed("TEST", "TESTTESTTESTTEST description")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name='ban_user',
        description='Ban user',
    )
    @app_commands.default_permissions(ban_members=True)
    async def _ban_user(
            self,
            interaction: Interaction,
            member: discord.Member,
            reason: str = ''
    ):
        description = (f"The user {member.mention} has been banned "
                       f"for **{reason}**.")
        embed = self._get_embed("Ban", description)
        await interaction.response.send_message(embed=embed)
        await member.ban(reason=reason)

    @app_commands.command(
        name='unban_user',
        description='Unban user',
    )
    @app_commands.default_permissions(ban_members=True)
    async def _unban_user(
            self,
            interaction: Interaction,
            member: discord.Member,
            reason: str = ''
    ):
        description = (f"The user {member.mention} has been unbanned "
                       f"for **{reason}**.")
        embed = self._get_embed("Unban", description)
        await interaction.response.send_message(embed=embed)
        await member.unban(reason=reason)

    @app_commands.command(
        name='kick_user',
        description='Kick user',
    )
    @app_commands.default_permissions(kick_members=True)
    async def _kick_user(
            self,
            interaction: Interaction,
            member: discord.Member,
            reason: str = ''
    ):
        description = (f"The user {member.mention} has been kicked "
                       f"for **{reason}**.")
        embed = self._get_embed("Kick", description)
        await interaction.response.send_message(embed=embed)
        await member.kick(reason=reason)

    @app_commands.command(
        name='timeout_user',
        description='Timeout user',
    )
    @app_commands.default_permissions(kick_members=True)
    @app_commands.choices(unit_of_measure=[
        app_commands.Choice(name="Days", value='days'),
        app_commands.Choice(name="Hours", value='hours'),
        app_commands.Choice(name="Minutes", value='minutes'),
        app_commands.Choice(name="Seconds", value='seconds')
    ])
    async def _timeout_user(
            self,
            interaction: Interaction,
            member: discord.Member,
            unit_of_measure: app_commands.Choice[str],
            time: int,
            reason: str = ''
    ):
        delta_kwargs = {unit_of_measure: time}
        until = datetime.timedelta(**delta_kwargs)
        description = (f"The user {member.mention} received a "
                       f"{time}-{unit_of_measure[:-1]} timeout "
                       f"for **{reason}**.")
        embed = self._get_embed("Timeout", description)
        await interaction.response.send_message(embed=embed)
        await member.timeout(until, reason=reason)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Manage(bot), guilds=bot.guilds)
