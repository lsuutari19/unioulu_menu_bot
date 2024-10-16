""" This module handles all the different menu fetches, formatting and so on """

import json
import random
from datetime import datetime
import requests

# Templated endpoints for API calls
UNIRESTA_URL = (
    "https://api.fi.poweresta.com/publicmenu/dates"
    "/uniresta/{name}/?menu=ravintola{name}&dates={date}"
)

JUVENES_URL = (
    "http://fi.jamix.cloud/apps/menuservice/"
    "rest/haku/menu/{customerID}/{kitchenID}?lang=fi"
)


def random_emoji():
    """
    Function for getting a random emoji, used for the markdown message
    """
    emojis = [
        "😀",
        "😳",
        "😵",
        "😡",
        "😷",
        "🤒",
        "🤕",
        "🤠",
        "🤖",
        "💻",
        "🎉",
        "🎈",
        "✨",
        "❤️",
        "🌟",
        "🌈",
        "🐶",
        "🐱",
        "🦁",
        "🐯",
        "🐻",
        "🐼",
        "🦄",
        "🐔",
        "🐢",
        "🦊",
        "🌻",
        "🌺",
        "🌸",
        "🌼",
        "🍀",
        "🍉",
        "🍕",
        "🍔",
        "🌭",
        "🍟",
        "🍦",
        "🍰",
        "🎂",
        "🍩",
        "🥨",
        "🍿",
        "🌮",
        "🥗",
        "🌽",
        "🍇",
        "🍊",
        "🍏",
        "🍌",
        "🥥",
        "🎈",
        "🎉",
        "🎊",
        "🎵",
        "🎶",
        "🔔",
        "📚",
        "🎮",
        "💼",
        "📸",
        "✈️",
        "⛷️",
        "🏖️",
    ]
    return random.choice(emojis)


def fetch_juvenes_data(customer_id, kitchen_id):
    """
    Function to fetch Juvenes data
    """
    url = JUVENES_URL.format(customerID=customer_id, kitchenID=kitchen_id)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"Error fetching Juvenes data: {error}")
        return None


def load_juvenes_restaurants(file_path):
    """
    Function to load Uniresta restaurant data from the JSON file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_juvenes_menu_items(juvenes_data, today_date, kitchen_id):
    """
    Function to extract kitchenName, specific meal option names, and menu items.
    Handles the case for kitchenID 70 separately for Kerttu and Voltti based on menuTypeName.
    """
    menu_structure = {}

    # Check for specific kitchenID case
    if kitchen_id == 70:
        for kitchen in juvenes_data:
            if kitchen["kitchenId"] == kitchen_id:
                for menu_type in kitchen.get("menuTypes", []):
                    menu_type_name = menu_type.get("menuTypeName", "")
                    print(menu_type_name)
                    for menu in menu_type.get("menus", []):
                        for day in menu.get("days", []):
                            if str(day.get("date")) == today_date:
                                for meal_option in day.get("mealoptions", []):
                                    meal_option_name = meal_option.get(
                                        "name", "Unknown Meal Option"
                                    )

                                    # Separate structures for Kerttu and Voltti based on menuTypeName
                                    if "Kerttu lounas" in menu_type_name:
                                        menu_structure.setdefault("Kerttu", {})[
                                            meal_option_name
                                        ] = []
                                    elif "Voltti lounas" in menu_type_name:
                                        menu_structure.setdefault("Voltti", {})[
                                            meal_option_name
                                        ] = []

                                    for menu_item in meal_option.get("menuItems", []):
                                        item_name = menu_item.get(
                                            "name", "Unknown Item"
                                        )
                                        if "Kerttu lounas" in menu_type_name:
                                            menu_structure["Kerttu"][
                                                meal_option_name
                                            ].append(item_name)
                                        elif "Voltti lounas" in menu_type_name:
                                            menu_structure["Voltti"][
                                                meal_option_name
                                            ].append(item_name)

    else:
        # For other kitchenIDs
        for kitchen in juvenes_data:
            for menu_type in kitchen.get("menuTypes", []):
                for menu in menu_type.get("menus", []):
                    for day in menu.get("days", []):
                        if str(day.get("date")) == today_date:
                            for meal_option in day.get("mealoptions", []):
                                meal_option_name = meal_option.get(
                                    "name", "Unknown Meal Option"
                                )
                                menu_structure[meal_option_name] = []

                                for menu_item in meal_option.get("menuItems", []):
                                    item_name = menu_item.get("name", "Unknown Item")
                                    menu_structure[meal_option_name].append(item_name)

    return menu_structure


def fetch_uniresta_data(restaurant_name, today_date):
    """
    Function to fetch Uniresta data
    """
    url = UNIRESTA_URL.format(name=restaurant_name, date=today_date)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"Error fetching Uniresta data: {error}")
        return None


def extract_uniresta_menu_items(uniresta_data):
    """
    Function to extract Uniresta menu items in Finnish along with the restaurant name
    """
    menu_structure = {}

    for item in uniresta_data:
        data = item.get("data", {})
        meal_options = data.get("mealOptions", [])
        if meal_options:
            for meal_option in meal_options:
                option_names = meal_option.get("names", [])
                for name in option_names:
                    if name.get("language") == "fi":
                        meal_option_name = name["name"]
                        menu_structure[meal_option_name] = []

                        rows = meal_option.get("rows", [])
                        for row in rows:
                            names = row.get("names", [])
                            for name in names:
                                if name.get("language") == "fi":
                                    food_item_name = name.get("name", "Unknown Item")
                                    menu_structure[meal_option_name].append(
                                        food_item_name
                                    )

    return menu_structure


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
    response_messages = [
        f"{random_emoji()} Here are the menus for {today_uniresta} {random_emoji()}\n"
    ]

    restaurant_menus = {}

    for uniresta_restaurant in uniresta_data:
        uniresta_data_response = fetch_uniresta_data(
            uniresta_restaurant, today_uniresta
        )

        if uniresta_data_response:
            menu_items = extract_uniresta_menu_items(uniresta_data_response)
            restaurant_menus[uniresta_restaurant] = menu_items

    juvenes_data = load_juvenes_restaurants("juvenes_restaurants.json")

    for restaurant in juvenes_data["restaurants"]:
        customer_id = restaurant["customerID"]
        kitchen_id = restaurant["kitchenID"]
        restaurant_name = restaurant.get("comment", "Unknown Restaurant")

        juvenes_data_response = fetch_juvenes_data(customer_id, kitchen_id)
        if juvenes_data_response:
            menu_items = extract_juvenes_menu_items(
                juvenes_data_response, today_juvenes, kitchen_id
            )
            restaurant_menus[restaurant_name] = menu_items

    for restaurant_name, menu in restaurant_menus.items():
        response_messages.append(f"### {restaurant_name}\n{menu}")

    for message in response_messages:
        print(message + "\n")

    save_menus_to_file(restaurant_menus, today_juvenes + ".json")

    if response_messages:
        return "".join(response_messages)

    return "Rankaise tämän spagetin luojaa!"


get_menus()
