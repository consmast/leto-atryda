import discord
import os
import requests
import json
import random
import asyncio

from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # don't forget to set the environment
OWM_API_KEY = os.getenv('OPENWM_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
#client = discord.Client()

def weather(city):
    url = "http://api.openweathermap.org/geo/1.0/direct?q={},,PL&appid={}".format(city, OWM_API_KEY)
    response = requests.get(url).json()[0]
    print(response)
    location = {'lat':response["lat"],'lon':response["lon"]}

    url = "https://api.openweathermap.org/data/2.5/weather?units=metric&lat={}&lon={}&appid={}".format(location['lat'], location['lon'], OWM_API_KEY)
    response = requests.get(url).json()
    print(response)
    temperature=response['main']['temp']
    clouds = response['weather'][0]['main']
    icon = response['weather'][0]['icon']
    return ("Temperatura: {}C\nZachmurzenie: {}\n".format(temperature, clouds), "https://openweathermap.org/img/wn/{}.png".format(icon))

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
    elif message.content.startswith('$pogoda'):
        print(f'Pogoda triggered by {message.author}')
        city = message.content.split()[1]
        forecast,icon = weather(city)
        embed = discord.Embed()
        embed.set_image(url=icon)
        await message.channel.send('Pogoda dla ' + city + "\n" + forecast,embed=embed)
    elif message.content.startswith('$guess'):
        await message.channel.send('Zgadnij liczbe miedzy 1 a 10.')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Sorry, za dlugo myslisz, odpowiedz to {answer}.')

        if int(guess.content) == answer:
            await message.channel.send('Brawo! Tak jest!')
        else:
            await message.channel.send(f'Ups. Niestety, odpowiedz to {answer}.')

client.run(TOKEN)
