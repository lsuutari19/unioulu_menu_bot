Very simple Discord bot that just shows the unioulu menus for the day by calling it using command !menu in discord.
It will provide then respond with a markdown message for example: 

```
🍩 Here are the menus for 2024-10-15 😢

Restaurant julinia 🎈
    Lounas 1
        Tonnikalalasagnettea
    Lounas 2
        Koskenlaskijan jauhelihakeittoa
    Herkkulounas
        Kanan filettä tomaatti-vuohenjuustokastikkeessa
        Juures-perunasärää

Restaurant lipasto 😳
    Lounas 1
        Tonnikalalasagnettea
    Lounas 2
        Paneroitu broilerin sisäfilee
        Tomaatti-kookoskastiketta
    Iltaruoka 15.00-18.00
        Carbonara pastavuokaa
        ...
```

To use it you need to create a dotenv file (.env) that contains your own github API key in the following format:
DISCORD_BOT_TOKEN=<API_KEY>

