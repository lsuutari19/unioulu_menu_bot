"""
The functions in this module handle the fetching of data from Juvenes API,
extracting them and parsing the results for usage by the menus.py module
"""


def extract_juvenes_menu_items(juvenes_data, today_date):
    """Function to extract kitchenName, specific meal option names, and menu items"""
    menu_structure = {}

    for kitchen in juvenes_data:
        for menu_type in kitchen.get("menuTypes", []):
            menu_type_name = menu_type.get("menuTypeName", "")

            if menu_type_name not in menu_structure:
                menu_structure[menu_type_name] = {}

            # Dictionary to track the count of each meal option name for this menu_type
            meal_name_count = {}

            for menu in menu_type.get("menus", []):
                for day in menu.get("days", []):
                    if str(day.get("date")) == today_date:
                        if today_date not in menu_structure[menu_type_name]:
                            menu_structure[menu_type_name] = {}

                        for meal_option in day.get("mealoptions", []):
                            meal_name = meal_option.get("name", "Unknown Meal Option")

                            # Check if meal option name already exists and append count if needed
                            if meal_name in meal_name_count:
                                meal_name_count[meal_name] += 1
                                new_meal_name = f"{meal_name} {meal_name_count[meal_name]}"
                            else:
                                meal_name_count[meal_name] = 1
                                new_meal_name = meal_name

                            # Initialize the meal option list if not already present
                            if new_meal_name not in menu_structure[menu_type_name]:
                                menu_structure[menu_type_name][new_meal_name] = []

                            # Add menu items to the corresponding meal option
                            for menu_item in meal_option.get("menuItems", []):
                                item_name = menu_item.get("name", "Unknown Item")
                                menu_structure[menu_type_name][new_meal_name].append(item_name)

    return menu_structure
