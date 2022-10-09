# reddcord-py
Fetches hot posts or subreddit information from reddit. <br/>
Does support `/commands`!<br/>
Using [asyncpraw](https://asyncpraw.readthedocs.io/en/stable/index.html) version 7.5.0
## Usage
**Please don't.** 
This bot is being developed for learning purposes. It is neither finished nor does every "feature" work. <br/>
I advise to *just look at it* if you really want to.
### Still want to try?
Put your reddit api token(s) as well as your discord api token into the `.env` file (below)inside the same directory. <br/>
`.env` must be in same directory as `.py` files. <br/>
  ```
    #.env
    
    DISCORD_TOKEN = <your-DISCORD_TOKEN>  #discord

    CLIENT_SECRET = <your-CLIENT_SECRET>  #reddit
    CLIENT_ID     = <your-CLIENT_ID>      #reddit
    
  ```
Add bot to your server, start `bot.py` &#8594; done
## Commands
- `reddit` `sub` `info` <br/>
  Fetches one of the hot posts (image, gif, video, text) from the specified subreddit (one for each command). <br/>
  Both `sub` and `info` are optional arguments. <br/>
  - If you don't put `sub` it will default to the r/memes subreddit
  -  If you put the `info` argument it fetches some subreddit information and displays it.
- `hellothere`: bot responds with `General Kenobi`
- Greets new members (this feature does not work as of now)
