# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from redditapi import get_images, create_reddit, sub_info

load_dotenv()

def setup():
    TOKEN = os.getenv('DISCORD_TOKEN')    
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix="?", intents=intents)
    reddit = create_reddit()
    return bot, TOKEN, reddit

bot, TOKEN, r = setup()


#commands
@bot.command(name="hellothere", help="fuck off")
async def hellothere(ctx):
    print("="*30 + "\ncommand: hellothere\n" + "="*30)
    response = "General Kenobi"
    await ctx.send(response)


@bot.command(name="reddit", help="gets a hot image from whatever subreddit you type in")
async def reddit(ctx, arg, arg2=None):    

    sub = arg    
    if arg2 is None:
        print("="*30 + f"\ncommand: reddit ({arg})\n" + "="*30)
        imgLink = get_images(r, sub)
        await ctx.send(imgLink)

    elif arg2 == "info":
        print("="*30 + f"\ncommand: reddit ({arg} {arg2})\n" + "="*30)
        title, desc = sub_info(r, sub)
        
        if len(desc) > 1000:
            desc = "description too long"

        embed = discord.Embed(title=title, description=desc, colour=0x87CEEB)
        await ctx.send(embed=embed)


@bot.command(name="test", help="test command")
async def test(ctx):
    print("="*30 + "\ncommand: test\n" + "="*30)    
    embed = discord.Embed(title="Test", description="This is a test for discord.Embed")
    await ctx.send(embed=embed)


# events
@bot.event 
async def on_member_join(member):
    print(f"event: {member} joined")
    channel = bot.get_channel(962284660992393246)
    await channel.send(f"welcum @{member}")

@bot.event
async def on_ready():
    print("="*30 + "\nbot is online\n" + "="*30)
    # channel = bot.get_channel(962063883026182186)
    # await channel.send("bot is online")


bot.run(TOKEN)