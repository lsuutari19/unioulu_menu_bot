import requests
import json
import random
from datetime import datetime

"""
For my minds sake I have to define here for remembering:
Uniresta: LIPASTO AND JULINIA (Old Napa and Foodoo)
Juvenes: All the rest

TO-DO: Where does one get Voltti information?
"""

# Templated endpoints for API calls
uniresta_url_template = "https://api.fi.poweresta.com/publicmenu/dates/uniresta/{name}/?menu=ravintola{name}&dates={date}"
juvenes_url_template = "http://fi.jamix.cloud/apps/menuservice/rest/haku/menu/{customerID}/{kitchenID}?lang=fi"

def random_emoji():
    emojis = [
        "😀", "😂", "😅", "😇", "😉", "😊", "😍", "😎", "😜", "🤔",
        "😐", "😑", "😩", "😢", "😤", "😮", "😱", "😳", "😵", "😡",
        "😷", "🤒", "🤕", "🤠", "🤖", "💻", "🎉", "🎈", "✨", "❤️",
        "🌟", "🌈", "🐶", "🐱", "🦁", "🐯", "🐻", "🐼", "🦄", "🐔",
        "🐢", "🦊", "🌻", "🌺", "🌸", "🌼", "🍀", "🍉", "🍕", "🍔",
        "🌭", "🍟", "🍦", "🍰", "🎂", "🍩", "🥨", "🍿", "🌮", "🥗",
        "🌽", "🍇", "🍊", "🍏", "🍌", "🥥", "🎈", "🎉", "🎊", "🎵",
        "🎶", "🔔", "📚", "🎮", "💼", "📸", "✈️", "⛷️", "🏖️"
    ]
    return random.choice(emojis)

# Function to fetch Juvenes data
def fetch_juvenes_data(customer_id, kitchen_id):
    url = juvenes_url_template.format(customerID=customer_id, kitchenID=kitchen_id)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Juvenes data: {e}")
        return None

# Function to load Uniresta restaurant data from the JSON file
def load_juvenes_restaurants(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to extract kitchenName, specific meal option names, and menu items
def extract_juvenes_menu_items(juvenes_data, today_date):
    ignored_items = {"CLASSIC", "JÄLKIRUOKA", "KASVISLOUNAS", "SALAD AND SOUP", "MY POPUP GRILL KASVIS", "MY POPUP GRILL"}
    
    messages = []
    for kitchen in juvenes_data:
        kitchen_name = kitchen.get('kitchenName', 'Unknown Kitchen')
        messages.append(f"\n### {kitchen_name} {random_emoji()}\n```\n")
        
        for menu_type in kitchen.get('menuTypes', []):
            for menu in menu_type.get('menus', []):
                for day in menu.get('days', []):
                    if str(day.get('date')) == today_date:
                        for meal_option in day.get('mealoptions', []):
                            meal_option_name = meal_option.get('name', 'Unknown Meal Option')
                            
                            # Check if the meal option is not in the ignored items
                            if meal_option_name not in ignored_items:
                                messages.append(f"    {meal_option_name}\n")
                                for menu_item in meal_option.get('menuItems', []):
                                    item_name = menu_item.get('name', 'Unknown Item')
                                    messages.append(f"        {item_name}\n")
    messages.append("```")
    return ''.join(messages)

# Function to fetch Uniresta data
def fetch_uniresta_data(restaurant_name, today_date):
    url = uniresta_url_template.format(name=restaurant_name, date=today_date)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Uniresta data: {e}")
        return None

# Function to extract Uniresta menu items in Finnish along with the restaurant name
def extract_uniresta_menu_items(uniresta_data_list, restaurant_name):
    ignored_items = {"Tumma riisi", "Peruna", "Kasvissekoitus", "Päivän jälkiruoka", "Lämmin lisäke", "Päivän jälkiruoka 1,40€", "Kahvila Lipaston salaattitori", "Kasvislounas", "Lipaston Grilli"}
    
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
                        meal_name = name.get('name', 'Unknown Meal Option')
                        break
                        
                if meal_name not in ignored_items:
                    messages.append(f"    {meal_name}\n")
                    rows = meal_option.get("rows", [])
                    for row in rows:
                        names = row.get("names", [])
                        for name in names:
                            if name.get("language") == "fi":
                                food_item_name = name.get('name', 'Unknown Item')
                                messages.append(f"        {food_item_name}\n")
    messages.append("```")
    return ''.join(messages)

# Function to get all menus for today
def get_menus():
    today = datetime.now()
    today_uniresta = today.strftime("%Y-%m-%d")
    today_juvenes = today.strftime("%Y%m%d")

    uniresta_data = ["julinia", "lipasto"]
    response_messages = [f"{random_emoji()} Here are the menus for {today_uniresta} {random_emoji()}\n"]

    for uniresta_restaurant in uniresta_data:
        uniresta_data_response = fetch_uniresta_data(uniresta_restaurant, today_uniresta)
        if uniresta_data_response:
            response_messages.append(extract_uniresta_menu_items(uniresta_data_response, uniresta_restaurant))
    
    juvenes_data = load_juvenes_restaurants('juvenes_restaurants.json')
    for restaurant in juvenes_data['restaurants']:
        customer_id = restaurant['customerID']
        kitchen_id = restaurant['kitchenID']
        juvenes_data_response = fetch_juvenes_data(customer_id, kitchen_id)
        if juvenes_data_response:
            response_messages.append(extract_juvenes_menu_items(juvenes_data_response, today_juvenes))

    if response_messages:
        return ''.join(response_messages)
    else:
        return "Rankaise tämän spagetin luojaa!"
