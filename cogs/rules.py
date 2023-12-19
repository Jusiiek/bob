import discord
from discord.ext import commands
from discord import app_commands, Interaction

from cogs.base import Base
from config.config import Config
from config.config_keys import ChannelsKeys
from config.environment import SERVER_ID


class Modal(discord.ui.Modal, title="Create rules"):
    config = Config()
    rules = []

    add_button = discord.ui.Button(
        label="Add new rule",
        style=discord.ButtonStyle.success
    )

    for rule in rules:
        rule["title"] = discord.ui.TextInput(
            label="Title",
            placeholder="Type title",
            style=discord.TextStyle.short,
        )
        rule["text"] = discord.ui.TextInput(
            label="Text of the rule",
            placeholder="Type something",
            style=discord.TextStyle.short,
        )


class Rules(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

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

    @app_commands.command(name='create_rules', description='Create rules')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def create_rules(self, interaction: Interaction):
        try:
            rules_channel_id = self.__config.get_config_value(ChannelsKeys.RULES_CHANNEL.value)
            if not rules_channel_id:
                return await interaction.channel.send(
                    "It looks like you didn't select a channel with rules.\n" +
                    "Before creating rules, you must set up a rules channel.\n" +
                    "Use 'set_rules_channel' command to select a rules channel"
                )
            await interaction.response.send_modal(Modal())
        except Exception as e:
            print(str(e))


async def setup(bot: commands.Bot):
    await bot.add_cog(Rules(bot))
