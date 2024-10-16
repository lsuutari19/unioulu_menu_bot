""" Module that handles the commands between the DiscordBot and the end user"""
import logging
import datetime
import os
from dotenv import load_dotenv, find_dotenv
import discord
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

async def check_todays_menu_exists():
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    file_path = f"menus/{today_date}.json"

    # Check if the file exists
    if os.path.isfile(file_path):
        return True
    else:
        return False

@client.event
async def on_ready():
    """
        Logs which client user the bot starts as
    """
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """
        Handles the messages between end user and the bot
    """
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!menu'):
        if not check_todays_menu_exists:
            get_menus()
        await message.channel.send()


client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
