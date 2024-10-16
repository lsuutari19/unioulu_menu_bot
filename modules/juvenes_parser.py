import requests, json
from variables import JUVENES_URL
from emoji import random_emoji

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
    """Function to load Uniresta restaurant data from the JSON file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_juvenes_menu_items(juvenes_data, today_date):
    """Function to extract kitchenName, specific meal option names, and menu items"""

    messages = []
    for kitchen in juvenes_data:
        kitchen_name = kitchen.get("kitchenName", "Unknown Kitchen")
        messages.append(f"\n### {kitchen_name} {random_emoji()}\n```\n")

        for menu_type in kitchen.get("menuTypes", []):
            for menu in menu_type.get("menus", []):
                for day in menu.get("days", []):
                    if str(day.get("date")) == today_date:
                        for meal_option in day.get("mealoptions", []):
                            meal_option_name = meal_option.get(
                                "name", "Unknown Meal Option"
                            )

                            messages.append(f"    {meal_option_name}\n")
                            for menu_item in meal_option.get("menuItems", []):
                                item_name = menu_item.get("name", "Unknown Item")
                                messages.append(f"        {item_name}\n")
    messages.append("```")
    return "".join(messages)
