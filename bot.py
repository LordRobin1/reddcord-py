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
    bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)
    reddit = create_reddit()
    return bot, TOKEN, reddit

bot, TOKEN, r = setup()


#commands
@bot.command(name="hellothere", help="")
async def hellothere(ctx):
    print("="*30 + "\ncommand: hellothere\n" + "="*30)
    response = "General Kenobi"
    await ctx.send(response)


@bot.command(name="reddit", help="gets a hot image from provided subreddit `?reddit subreddit info` (`info` optional)")
async def reddit(ctx, arg=None, arg2=None):
    sub = arg
    if sub == None:
        await ctx.send("Must enter a Subreddit as first argument:\n `?reddit memes`")
        return
    if arg2 is None:
        print("="*30 + f"\ncommand: reddit ({arg})\n" + "="*30)
        post = await get_images(r, sub)
        if post['type'] == "gallery": 
            await ctx.send(f"{post['title']}\n"+
                           f"{post['url']}"+
                            "\n*Reddit posts with gallery not supported yet*")
            return
        if post['type'] == "text":            
            try:
                await sendText(post, ctx)
            except Exception as e:
                print(f"error: {e}")
                await ctx.send("Sorry, an error occured :(")
            return
        await ctx.send(f"{post['title']}\n{post['url']}")
        return

    if arg2 == "info":
        await sendInfo(sub, ctx)

async def sendText(post, ctx):
    desc = ""
    if post['text'] != '': desc += post['text']
    if post['comment'] != '': desc += f"\n\n**Top Comment:**\n{post['comment']}"
    embed = discord.Embed(title=post['title'], description=desc, colour=0x87ce)
    await ctx.send(embed=embed)

async def sendInfo(sub, ctx):
    print("="*30 + f"\ncommand: reddit ({sub} info)\n" + "="*30)
    title, desc = await sub_info(r, sub)        
    if len(desc) > 4000:
        desc = "description too long"
    embed = discord.Embed(title=title, description=desc, colour=0x87CEEB)
    await ctx.send(embed=embed)

@bot.command(name="help")
async def help(ctx):
    title = "Help"
    desc = "`hellothere`\n\n" + "`help`: Shows this message\n\n" 
    desc += "`reddit`: gets a hot post from provided subreddit\n`?reddit subreddit info` (`info` optional)"
    embed = discord.Embed(title=title, description=desc, colour=discord.Colour.from_rgb(26, 188, 156))
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