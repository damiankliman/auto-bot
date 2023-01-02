import os
import discord
from core import responses

async def send_message(message, user_message, is_private):
  try:
    response = responses.handle_response(user_message)

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
    user_message = str(message.content)[1:]
    channel = str(message.channel)

    print(f"{username} with id:{user_id} in {channel}: {user_message}")

    if user_message.startswith('!'):
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else: await send_message(message, user_message, is_private=False)

  client.run(TOKEN)
