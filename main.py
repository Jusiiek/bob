import asyncio
import os

from bot import Bot
from config.environment import TOKEN
from config.environment import COGS_FOLDER


async def setup(bot):
    for filename in os.listdir(COGS_FOLDER):
        if filename.endswith('.py') and filename != 'voice_assistant.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    bot = Bot()
    await setup(bot)
    await bot.start(TOKEN)


asyncio.run(main())
