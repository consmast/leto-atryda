import discord

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

client.run('token-put-here')
