"""
The functions in this module handle the fetching of data from Juvenes API,
extracting them and parsing the results for usage by the menus.py module
"""

import requests
from modules.variables import JUVENES_URL


def fetch_juvenes_data(customer_id, kitchen_id):
    """Function to fetch Juvenes data"""
    url = JUVENES_URL.format(customerID=customer_id, kitchenID=kitchen_id)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"Error fetching Juvenes data: {error}")
        return None


def extract_juvenes_menu_items(juvenes_data, today_date):
    """Function to extract kitchenName, specific meal option names, and menu items"""
    menu_structure = {}

    for kitchen in juvenes_data:
        for menu_type in kitchen.get("menuTypes", []):
            menu_type_name = menu_type.get("menuTypeName", "")

            if menu_type_name not in menu_structure:
                menu_structure[menu_type_name] = {}

            for menu in menu_type.get("menus", []):
                for day in menu.get("days", []):
                    if str(day.get("date")) == today_date:
                        if today_date not in menu_structure[menu_type_name]:
                            menu_structure[menu_type_name] = {}

                        for meal_option in day.get("mealoptions", []):
                            meal_option_name = meal_option.get(
                                "name", "Unknown Meal Option"
                            )

                            if meal_option_name not in menu_structure[menu_type_name]:
                                menu_structure[menu_type_name][meal_option_name] = []

                            for menu_item in meal_option.get("menuItems", []):
                                item_name = menu_item.get("name", "Unknown Item")
                                menu_structure[menu_type_name][meal_option_name].append(
                                    item_name
                                )

    return menu_structure
