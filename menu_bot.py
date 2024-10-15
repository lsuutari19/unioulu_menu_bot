import discord
import logging
import os
from dotenv import load_dotenv, find_dotenv
from menus import get_menus

dotenv_file = find_dotenv(usecwd=True)

load_dotenv(dotenv_file)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None or TOKEN == "":
    print("No token found in .env file")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

"""
Example API call to Uniresta (Julinia)
https://api.fi.poweresta.com/publicmenu/dates/uniresta/julinia/?menu=ravintolajulinia&dates=2024-10-15

Example API call to Juvenes
http://fi.jamix.cloud/apps/menuservice/rest/haku/menu/<customerID>/<kitchenID>?lang=fi

"""

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$menu'):
        menu_data = get_menus()
        await message.channel.send(menu_data)
        




client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)