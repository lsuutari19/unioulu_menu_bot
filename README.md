### Simple Discord bot that fetches the University of Oulu menus from different APIs, depending if the restaurant belongs to Uniresta or Juvenes (Sodexo aswell soon).

The two API's it calls are JAMIX and Poweresta, the data is fetched via the following API calls:

https://api.fi.poweresta.com/publicmenu/dates/uniresta/{name}/?menu=ravintola{name}&dates={date}

http://fi.jamix.cloud/apps/menuservice/rest/haku/menu/{customerID}/{kitchenID}?lang=fi

After fetching the data from the APIs it will then create a .json file in format {date}.json in the ./menus directory under repository root.
If !menu is executed on any discord channel where the bot exists it will first check if today's menus have already been fetched, if not
it will fetch them and display each restaurants menu in different message, this is to avoid the discord message limit. Furthermore, the bot
adds reactions under the menu's so that users can indicate which meals they would prefer!

Furthermore if the current time is past 5pm (or 17:00 in Finnish time), it will get the next day's menu.

#### Example output from running !menu

![image](https://github.com/user-attachments/assets/87f5655b-182c-493f-be3a-9668f9cd4f37)



#### To set it up on your own:
1. Have Python installed
2. Clone this repository & open the repository directory in terminal
3. Execute following command: pip install -r requirements.txt
4. Follow this to create your own bot: https://discordpy.readthedocs.io/en/stable/discord.html
5. Create an .env file that contains your own discord bot's token in the following format: DISCORD_BOT_TOKEN=<API_KEY>
6. Run the menu_bot.py

