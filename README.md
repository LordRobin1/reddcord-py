# reddcord-py

Fetches hot posts or subreddit information from reddit.  
Does support `/commands`!  
Using [asyncpraw](https://asyncpraw.readthedocs.io/en/stable/index.html) version 7.5.0

## Usage

This bot is being developed for learning purposes. It is neither finished nor does every feature work.  

### Still want to try?

Put your reddit api token(s) as well as your discord api token into the `.env` file (below) inside the same directory.  
`.env` must be in same directory as `.py` files.  
  
  ```py
    #.env
    
    DISCORD_TOKEN = <your-DISCORD_TOKEN>  #discord

    CLIENT_SECRET = <your-CLIENT_SECRET>  #reddit
    CLIENT_ID     = <your-CLIENT_ID>      #reddit
    
  ```

Install `discord.py`, `asyncpraw` and `python-dotenv` via pip.  
Add the bot to your server, start `bot.py` &#8594; done.

## Commands

- `reddit` `sub` `info`  
  Fetches one of the hot posts (image, gif, video, text) from the specified subreddit (one for each command).  
  Both `sub` and `info` are optional arguments.  
  - If you don't put `sub` it will default to the r/memes subreddit.
  - If you put the `info` argument it fetches some subreddit information and displays it.
- `hellothere`: bot responds with `General Kenobi`
- Greets new members (this feature does not work as of now)
