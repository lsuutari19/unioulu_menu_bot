"""
These are global variables and functions to be used by any of the functions.
"""

import requests

UNIRESTA_URL = (
    "https://api.fi.poweresta.com/publicmenu/dates"
    "/uniresta/{name}/?menu=ravintola{name}&dates={date}"
)

JUVENES_URL = (
    "http://fi.jamix.cloud/apps/menuservice/"
    "rest/haku/menu/{customerID}/{kitchenID}?lang=fi"
)

JUVENES_RESTAURANTS = [
    {"customerID": "93077", "kitchenID": "69", "comment": "Foobar"},
    {"customerID": "93077", "kitchenID": "70", "comment": "Kerttu"},
    {"customerID": "93077", "kitchenID": "49", "comment": "Mara"},
]

def fetch_api_data(url_format, **kwargs):
    """
    Function to fetch data from a given URL format.
    
    :param url_format: The URL format string with placeholders.
    :param kwargs: The keyword arguments to format the URL.
    :return: The JSON response data or None if an error occurs.
    """
    url = url_format.format(**kwargs)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data: {error}")
        return None
