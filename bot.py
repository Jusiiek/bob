import discord
from discord.ext import commands
from discord.ext.commands import Context, CommandError


class Bot(commands.Bot):
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True

    def __init__(self):
        super().__init__(command_prefix='$', intents=self.intents)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.user.display_name} is connected to the server")

    @commands.Cog.listener()
    async def on_command_error(self, context: Context, errors: CommandError) -> None:
        if errors:
            await context.send("Command not found")
            print(f"[ERROR]: {errors}")
