import discord
from discord.ext import commands
from discord import app_commands, Interaction

from cogs.base import Base
from config.environment import SERVER_ID
from config.config import Config
from config.config_keys import ChannelsKeys


class Modal(discord.ui.Modal, title="Add additional text"):
    config = Config()
    text = discord.ui.TextInput(
        label="Text",
        placeholder="Add additional text (can be empty)",
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: Interaction):
        guild_id = interaction.guild_id
        try:
            self.config.set_config(
                guild_id,
                ChannelsKeys.WELCOME_CHANNEL_TEXT.value,
                self.text.value
            )
            await interaction.response.send_message(
                "Successfully set new text for welcome message",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"{str(e)}"
            )


class Greetings(Base):
    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__config = Config()

    @app_commands.command(name='set_welcomes_channel', description='Set welcomes channel')
    @app_commands.guilds(discord.Object(id=SERVER_ID))
    async def set_welcomes_channel(self, interaction: Interaction, channel: discord.TextChannel):
        guild_id = interaction.guild_id
        await interaction.response.send_modal(Modal())
        self.__config.set_config(
            guild_id,
            ChannelsKeys.WELCOME_CHANNEL.value,
            channel.id
        )

    # TODO try to solve by passing the guild id to the config methods
    # @commands.Cog.listener(name='on_member_join')
    # async def on_member_join(self, member: discord.Member):
    #     channel_id = Config.get_config_value(ChannelsKeys.WELCOME_CHANNEL.value)
    #     if channel_id:
    #         guild = self.__bot.get_guild(SERVER_ID)
    #         channel = self.__bot.get_channel(Config.get_config_value(ChannelsKeys.WELCOME_CHANNEL.value))
    #         if channel is not None:
    #             await channel.send(
    #                 f'Hey {member.mention}, welcome to {guild.name}! :partying_face:\n' +
    #                 f"{self.__bot.get_channel(Config.get_config_value(ChannelsKeys.WELCOME_CHANNEL_TEXT.value))}"
    #             )


async def setup(bot: commands.Bot):
    await bot.add_cog(Greetings(bot))
