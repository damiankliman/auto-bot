import os
import discord
from core import responses
from core.database import get_db
from core import services

async def send_message(message, response: str, is_private: bool):
    try:
        if not response:
            raise Exception("Command not found")

        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is connected and running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if not message.content.startswith('/'):
            return

        username = str(message.author)
        user_id = str(message.author.id)
        message_content = str(message.content)[1:]
        channel = str(message.channel)
        local_user = services.get_or_create_local_user(message.author)
        is_private = False

        print(f"{username} with id:{user_id} in {channel}: {message_content}")
        print(f"Local user: {local_user.username} with id: {local_user.id} with discord_id: {local_user.discord_id}")

        if message_content.startswith('!'):
            is_private = True
            message_content = message_content[1:]

        response = responses.handle_response(message_content, local_user)

        await send_message(message, response, is_private)


    client.run(TOKEN)
