""" This module handles all the different menu fetches, formatting and so on """
from datetime import datetime
from modules.variables import JUVENES_RESTAURANTS
from modules.emoji import random_emoji
from modules.juvenes_parser import fetch_juvenes_data, extract_juvenes_menu_items
from modules.uniresta_parser import fetch_uniresta_data, extract_uniresta_menu_items


def get_menus():
    """ Function to get all menus for today """
    today = datetime.now()
    today_uniresta = today.strftime("%Y-%m-%d")
    today_juvenes = today.strftime("%Y%m%d")

    uniresta_data = ["julinia", "lipasto"]
    response_messages = [
        f"{random_emoji()} Here are the menus for {today_uniresta} {random_emoji()}\n"
    ]

    for uniresta_restaurant in uniresta_data:
        uniresta_data_response = fetch_uniresta_data(
            uniresta_restaurant, today_uniresta
        )
        if uniresta_data_response:
            response_messages.append(
                extract_uniresta_menu_items(uniresta_data_response, uniresta_restaurant)
            )

    juvenes_data = JUVENES_RESTAURANTS
    for restaurant in juvenes_data["restaurants"]:
        customer_id = restaurant["customerID"]
        kitchen_id = restaurant["kitchenID"]
        juvenes_data_response = fetch_juvenes_data(customer_id, kitchen_id)
        if juvenes_data_response:
            response_messages.append(
                extract_juvenes_menu_items(juvenes_data_response, today_juvenes)
            )

    if response_messages:
        return "".join(response_messages)
    return "Rankaise tämän spagetin luojaa!"
