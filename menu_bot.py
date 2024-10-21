""" Module that handles the commands between the DiscordBot and the end user"""

import logging
import datetime
import json
import os
from dotenv import load_dotenv, find_dotenv
import discord
from menus import get_menus, parse_menu_from_file


dotenv_file = find_dotenv(usecwd=True)

load_dotenv(dotenv_file)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None or TOKEN == "":
    print("No token found in .env file")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def check_todays_menu_exists():
    """Checks if today's menu is already fetched into menus folder and returns the parsed JSON"""
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    file_path = f"menus/{today_date}.json"
    print(file_path)

    if os.path.isfile(file_path):
        print("Menu exists!")
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                menu_data = json.load(file)
                return menu_data
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None
    else:
        print("Menu file does not exist.")
        return None


@client.event
async def on_ready():
    """Logs which client user the bot starts as"""
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """Handles the messages between end user and the bot"""
    if message.author == client.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("!menu"):
        # Check if today's menu file exists and get the parsed data
        menu_data = await check_todays_menu_exists()

        if not menu_data:
            await get_menus()

            menu_data = await check_todays_menu_exists()

            # Last check to make sure there wasn't issues in creating the json file
            if not menu_data:
                await message.channel.send("Menu could not be fetched or created.")
                return

        markdown_message = await parse_menu_from_file(menu_data)
        await message.channel.send(markdown_message)


client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
