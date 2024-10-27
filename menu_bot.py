""" Module that handles the commands between the DiscordBot and the end user"""

import logging
import datetime
import json
import os
from dotenv import load_dotenv, find_dotenv
import discord
import pytz
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


async def check_todays_menu_exists(today):
    """Checks if today's menu is already fetched into menus folder and returns the parsed JSON"""

    file_path = f"menus/{today}.json"

    if os.path.isfile(file_path):
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
        current_time = datetime.datetime.now(pytz.timezone("Europe/Helsinki"))
        today = datetime.datetime.now().strftime("%Y%m%d")

        # Check if the time is past 5pm or Sunday, if it is look for the next day's menu
        if current_time.hour >= 17 or current_time.weekday() == 6:
            today = (current_time + datetime.timedelta(days=1)).strftime("%Y%m%d")

        # Check if today's menu file exists and get the parsed data
        menu_data = await check_todays_menu_exists(today)

        if not menu_data:
            await get_menus(today)
            menu_data = await check_todays_menu_exists(today)

            # Last check to make sure there wasn't issues in creating the json file
            if not menu_data:
                await message.channel.send("Menu could not be fetched or created.")
                return

        if isinstance(menu_data, str):
            menu_data = json.loads(menu_data)

        await message.channel.send(
            f"## Here are the restaurant menus for {today[:4]}-{today[4:6]}-{today[6:]}"
        )

        reactions = ["👍", "👎", "❤️"]

        # Loop through each restaurant and its menu, and send each one separately
        for restaurant, meals in menu_data.items():
            markdown_message = await parse_menu_from_file(restaurant, meals)
            sent_message = await message.channel.send(markdown_message)
            for reaction in reactions:
                await sent_message.add_reaction(reaction)


client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
