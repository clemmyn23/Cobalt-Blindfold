# Cobalt-Blindfold
Soul-shields data and utilities for Blade and Soul game.  

Add it as a module for your discord bot of choice, and it'll list  
whichever ss stats you query for.


## Credits:
* [chibi_prae](https://twitter.com/chibi_prae) for [bopae cheatsheet](https://docs.google.com/spreadsheets/d/1JOQK34BUTR_55XwnbJOk388gjokrtLZFdhi3vIwXjZc)
([webview](https://docs.google.com/spreadsheets/d/1JOQK34BUTR_55XwnbJOk388gjokrtLZFdhi3vIwXjZc/htmlview?sle=true#))
* [new sheet](https://docs.google.com/spreadsheets/d/1v0tY9qwTmQalLrD0FW2LkX2AJWqEKKSrBz5Ij4WvRXo/htmlview?sle=true#gid=0)


## Dependencies:  
* [Red-DiscordBot](https://github.com/Twentysix26/Red-DiscordBot)
* ~~BeautifulSoup4 for web parsing components~~ (disabled)

## Commands:
* `!bopae` or `!bopae search`
* `!bopae list`
* ~~`!bopae compare`~~ (disabled)
* ~~`!bopae reload`~~ (disabled)
* and maybe more.


## Install:  
#### Red-DiscordBot:  
* Make sure the `downloader` cog that comes with Red-DiscordBot is enabled.  

1. ssh `[p]cog repo add Cobalt-Blindfold git@github.com:clemmyn23/Cobalt-Blindfold.git@develop`  
https `[p]cog repo add Cobalt-Blindfold https://github.com/clemmyn23/Cobalt-Blindfold.git@develop`
2. Read the warning and type `I agree` when prompted.
3. `[p]cog install bopae`
4. Type `yes` to load the cog when prompted.

* `[p]reload bopae` to reload the cog  

## TODO:  
- redesign search to account for class specific soul shields
- profile parser
- statistics and analysis?
