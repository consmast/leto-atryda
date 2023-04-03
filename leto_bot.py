import discord
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # don't forget to set the environment

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
#client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print(f'Hello triggered by {message.author}, let\'s write to channel')
        await message.channel.send('Hello!')
    elif message.content.startswith('$godzina'):
        now = datetime.now()
        print(f'Godzina triggered by {message.author}')
        await message.channel.send('Jest godzina ' + now.strftime('%H:%M:%S'))



client.run(TOKEN)
