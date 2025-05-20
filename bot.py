import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Cogs 로드
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename not in ['__init__.py', 'command_info.py', 'help.py', 'tier.py']:
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded: {filename}')

bot.run(TOKEN)
