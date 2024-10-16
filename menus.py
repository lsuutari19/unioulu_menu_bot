""" This module handles all the different menu fetches, formatting and so on """
import json
from datetime import datetime
from modules.variables import JUVENES_RESTAURANTS
from modules.juvenes_parser import fetch_juvenes_data, extract_juvenes_menu_items
from modules.uniresta_parser import fetch_uniresta_data, extract_uniresta_menu_items

def save_menus_to_file(menus_dict, filename):
    """
    Save the collected menus to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(menus_dict, f, ensure_ascii=False, indent=4)

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
        uniresta_data_response = fetch_uniresta_data(
            uniresta_restaurant, today_uniresta
        )

        if uniresta_data_response:
            menu_items = extract_uniresta_menu_items(uniresta_data_response)
            menus[uniresta_restaurant.capitalize()] = menu_items

    for restaurant in JUVENES_RESTAURANTS:
        customer_id = restaurant["customerID"]
        kitchen_id = restaurant["kitchenID"]

        juvenes_data_response = fetch_juvenes_data(customer_id, kitchen_id)
        if juvenes_data_response:
            menu_items = extract_juvenes_menu_items(
                juvenes_data_response, today_juvenes, kitchen_id
            )
            for meal_type_name, meal_options in menu_items.items():
                menus[meal_type_name] = meal_options


    save_menus_to_file(menus, today_juvenes + ".json")

    return

get_menus()
