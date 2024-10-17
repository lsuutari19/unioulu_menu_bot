"""
This module ingests the data returned from uniresta_parser and juvenes_parser
and saves it into a .json format for use by the Discord bot. 
"""

import json
import os
from datetime import datetime
from modules.variables import (
    JUVENES_RESTAURANTS,
    JUVENES_URL,
    UNIRESTA_URL,
    fetch_api_data,
)
from modules.juvenes_parser import extract_juvenes_menu_items
from modules.uniresta_parser import extract_uniresta_menu_items


def save_menus_to_file(menus_dict, filename):
    """
    Save the collected menus to a JSON file.
    """
    file_path = os.path.join("menus", filename)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(menus_dict, file, ensure_ascii=False, indent=4)


def get_menus():
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
            menus[uniresta_restaurant.capitalize()] = menu_items

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
            for meal_type_name, meal_options in menu_items.items():
                menus[meal_type_name] = meal_options

    save_menus_to_file(menus, today_juvenes + ".json")


get_menus()
