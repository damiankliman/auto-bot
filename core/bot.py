import os
import discord
from discord.ext import commands
from core.commands import handle_commands
from core.database import get_db
from core import services

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX') or '/'
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'{bot.user} is connected and running')

    @bot.before_invoke
    async def before_invoke(ctx):
        ctx.local_user = services.get_or_create_local_user(ctx.author)

    handle_commands(bot)

    bot.run(TOKEN)
