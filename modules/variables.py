
UNIRESTA_URL = (
    "https://api.fi.poweresta.com/publicmenu/dates"
    "/uniresta/{name}/?menu=ravintola{name}&dates={date}"
)

JUVENES_URL = (
    "http://fi.jamix.cloud/apps/menuservice/"
    "rest/haku/menu/{customerID}/{kitchenID}?lang=fi"
)

JUVENES_RESTAURANTS = [
    {
        "customerID": "93077",
        "kitchenID": "69",
        "comment": "Foobar"
    },
    {
        "customerID": "93077",
        "kitchenID": "70",
        "comment": "Kerttu"
    },
    {
        "customerID": "93077",
        "kitchenID": "49",
        "comment": "Mara"
    }
]
