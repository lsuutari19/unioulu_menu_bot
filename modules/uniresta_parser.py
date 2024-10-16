import requests
from emoji import random_emoji
from variables import UNIRESTA_URL

def fetch_uniresta_data(restaurant_name, today_date):
    """ Function to fetch Uniresta data """
    url = UNIRESTA_URL.format(name=restaurant_name, date=today_date)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"Error fetching Uniresta data: {error}")
        return None


def extract_uniresta_menu_items(uniresta_data_list, restaurant_name):
    """ Function to extract Uniresta menu items in Finnish along with the restaurant name """

    messages = [f"\n### Restaurant {restaurant_name} {random_emoji()}\n```\n"]

    for uniresta_data in uniresta_data_list:
        if uniresta_data.get("allSuccessful"):
            meal_options = uniresta_data.get("data", {}).get("mealOptions", [])
            for meal_option in meal_options:
                # Extract the meal option name
                option_names = meal_option.get("names", [])
                meal_name = "Unknown Meal Option"
                for name in option_names:
                    if name.get("language") == "fi":
                        meal_name = name.get("name", "Unknown Meal Option")
                        break

                messages.append(f"    {meal_name}\n")
                rows = meal_option.get("rows", [])
                for row in rows:
                    names = row.get("names", [])
                    for name in names:
                        if name.get("language") == "fi":
                            food_item_name = name.get("name", "Unknown Item")
                            messages.append(f"        {food_item_name}\n")
    messages.append("```")
    return "".join(messages)
