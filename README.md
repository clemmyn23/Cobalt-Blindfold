# Cobalt-Blindfold
Soul-shields data and utilities for Blade and Soul game.  

Add it as a module for your discord bot of choice, and it'll list  
whichever ss stats you query for.


## Credits:
* [chibi_prae](https://twitter.com/chibi_prae) for [bopae cheatsheet](https://docs.google.com/spreadsheets/d/1JOQK34BUTR_55XwnbJOk388gjokrtLZFdhi3vIwXjZc)
([webview](https://docs.google.com/spreadsheets/d/1JOQK34BUTR_55XwnbJOk388gjokrtLZFdhi3vIwXjZc/htmlview?sle=true#))
* [new sheet](https://docs.google.com/spreadsheets/d/1v0tY9qwTmQalLrD0FW2LkX2AJWqEKKSrBz5Ij4WvRXo/htmlview?sle=true#gid=0)


## Dependencies:  
* [Red-DiscordBot](https://github.com/Twentysix26/Red-DiscordBot) or whichever bot
* BeautifulSoup4 for web parsing components (currently disabled)


## Install:  
#### Red-DiscordBot:  
1. Copy `/BOTS/RED-DISCORDBOT/bopae.py` into `~RED-DISCORDBOT/cogs/bopae.py`  
2. Copy `/data/*` into `~RED-DISCORDBOT/data/bopae/`  
3. Run `!load bopae` or `!reload bopae` (may have to restart Red if you updated `libbopae/`)
4. Run `!bopae` for help

#### BASEDBOT:  
1. - TODO -


## TODO:  
- redesign search to account for class specific soul shields
- profile parser
- statistics and analysis?
