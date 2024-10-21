"""
This module ingests the data returned from uniresta_parser and juvenes_parser
and saves it into a .json format for use by the Discord bot. 
"""

import json
import os
from datetime import datetime
from api_parsers.variables import (
    JUVENES_RESTAURANTS,
    JUVENES_URL,
    UNIRESTA_URL,
    fetch_api_data,
)
from api_parsers.emoji import random_emoji
from api_parsers.juvenes_parser import extract_juvenes_menu_items
from api_parsers.uniresta_parser import extract_uniresta_menu_items


def save_menus_to_file(menus_dict, filename):
    """
    Save the collected menus to a JSON file.
    """
    file_path = os.path.join("menus", filename)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(menus_dict, file, ensure_ascii=False, indent=4)


async def parse_menu_from_file(menu_data):
    """
    This function parses the data that the discord bot will then send as a message.
    """
    markdown_message = ""

    for restaurant, meals in menu_data.items():
        markdown_message += f"# {random_emoji()}    {restaurant}\n\n"
        if meals:
            for meal_type, items in meals.items():
                markdown_message += f"### {meal_type}\n"
                for i, item in enumerate(items):
                    if i == len(items) - 1:
                        markdown_message += f"- {item}"
                    else:
                        markdown_message += f"- {item}\n"
                markdown_message += "\n"
        else:
            markdown_message += "No menu available.\n\n"
    markdown_message += "\n"
    return markdown_message


async def get_menus():
    """
    Function to get all menus for today
    """
    today = datetime.now()
    today_uniresta = today.strftime("%Y-%m-%d")
    today_juvenes = today.strftime("%Y%m%d")

    uniresta_data = ["julinia", "lipasto"]
    menus = {}

    for uniresta_restaurant in uniresta_data:
        uniresta_data_response = fetch_api_data(
            UNIRESTA_URL, name=uniresta_restaurant, date=today_uniresta
        )

        if uniresta_data_response:
            menu_items = extract_uniresta_menu_items(uniresta_data_response)
            # Check that there are no empty values in the menu
            filtered_menu_items = {
                meal: items for meal, items in menu_items.items() if items
            }

            if filtered_menu_items:
                print(filtered_menu_items)
                menus[uniresta_restaurant.capitalize()] = filtered_menu_items
            else:
                print(f"{uniresta_restaurant.capitalize()} has no valid menu items.")

    for restaurant in JUVENES_RESTAURANTS:
        customer_id = restaurant["customerID"]
        kitchen_id = restaurant["kitchenID"]

        juvenes_data_response = fetch_api_data(
            JUVENES_URL, customerID=customer_id, kitchenID=kitchen_id
        )

        if juvenes_data_response:
            menu_items = extract_juvenes_menu_items(
                juvenes_data_response, today_juvenes
            )

            if menu_items:
                # Only add to 'menus' if at least one of the meal types has items
                for meal_type_name, meal_options in menu_items.items():
                    if meal_options:
                        print({meal_type_name: meal_options})
                        menus[meal_type_name] = meal_options

    save_menus_to_file(menus, today_juvenes + ".json")


get_menus()
