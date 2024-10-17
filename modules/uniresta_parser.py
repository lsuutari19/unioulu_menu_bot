"""
The functions in this module handle the fetching of data from Uniresta API,
extracting them and parsing the results for usage by the menus.py module
"""


def extract_uniresta_menu_items(uniresta_data):
    """Function to extract Uniresta menu items in Finnish along with the restaurant name"""
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
