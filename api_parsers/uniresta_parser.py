"""
The functions in this module handle the fetching of data from Uniresta API,
extracting them and parsing the results for usage by the menus.py module
"""


def extract_uniresta_menu_items(uniresta_data):
    """Function to extract Uniresta menu items in Finnish along with the restaurant name"""
    menu_structure = {}
    meal_name_count = {}

    for item in uniresta_data:
        data = item.get("data", {})
        meal_options = data.get("mealOptions", [])
        if meal_options:
            for meal_option in meal_options:
                option_names = meal_option.get("names", [])
                for name in option_names:
                    if name.get("language") == "fi":
                        meal_name = name["name"].upper()
                        print("This is meal_name", meal_name)
                        if "SULJETTU" in meal_name:
                            continue
                        # Check if meal option name already exists and append count if needed
                        # so "lounas", "lounas 2" ...
                        if meal_name in meal_name_count:
                            meal_name_count[meal_name] += 1
                            new_meal_name = f"{meal_name} {meal_name_count[meal_name]}"
                        else:
                            meal_name_count[meal_name] = 1
                            new_meal_name = meal_name

                        # Initialize the menu structure for the meal option
                        menu_structure[new_meal_name] = []

                        rows = meal_option.get("rows", [])
                        for row in rows:
                            names = row.get("names", [])
                            for name in names:
                                if name.get("language") == "fi":
                                    food_item_name = name.get("name", "Unknown Item")
                                    menu_structure[new_meal_name].append(food_item_name)

    return menu_structure
