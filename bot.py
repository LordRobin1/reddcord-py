import time
import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from redditapi import get_post, sub_info

load_dotenv()

def setup():
    TOKEN = os.getenv('DISCORD_TOKEN')
    ID = os.getenv('GUILD_ID')
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    return client, tree, TOKEN, ID

client, tree, TOKEN, ID = setup()
color = discord.Colour.from_rgb(26, 188, 156)
lastPost = {}

def setLastPost(post: dict):
    global lastPost
    lastPost = post
    print("set ",lastPost)

def getLastPost():
    global lastPost
    return lastPost

@client.event
async def on_ready():
    print("="*30 + "\nbot is online\n" + "="*30)
    await client.wait_until_ready()
    await tree.sync(guild=discord.Object(id=ID))

#commands
@tree.command(name="hellothere", guild=discord.Object(id=ID))
async def hellothere(interaction: discord.Interaction):
    print("="*30 + "\ncommand: hellothere\n" + "="*30)
    embed = discord.Embed()
    embed.color = color
    embed.title = "General Kenobi"
    embed.set_image(url="https://media.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif")
    await interaction.response.send_message(embed=embed)


@tree.command(name="reddit", guild=discord.Object(id=ID))
async def reddit(interaction: discord.Interaction, sub: str='memes', info: bool=False):
    start_time = time.time()
    embed = discord.Embed()
    if not info:
        print("="*30 + f"\ncommand: reddit ({sub})\n" + "="*30)
        try:
            post = await get_post(sub)
            link = post['imgurl']
            desc = ''
            setLastPost(post)
        except Exception as e:
            print(e)
            await error(interaction)
            return
        if post['type'] == "video" or post['type'] == "badgif":
            await interaction.response.send_message(post['imgurl'])
            return
        if post['type'] == "gallery": 
            desc = f"*Reddit posts with gallery not supported yet*"
            link = ""
        if post['type'] == "text":
            try:
                desc = sendText(post)
                link = ""
            except Exception as e:
                print(f"bot error: {e}")
                desc = "Sorry, an error occured :(" 
        embed.title = post['title']
        embed.description = desc
        if link != "": embed.set_image(url=link)
        embed.url = f"https://reddit.com{post['url']}"
        embed.color = color
        await interaction.response.send_message(embed=embed)
        print(f"{time.time() - start_time}")
        return

    if info:
        await sendInfo(sub, interaction)
        print(f"{time.time() - start_time}")
        return


def sendText(post):
    desc = ""
    if post['text'] != '': desc += post['text']
    if post['comment'] != '': desc += f"\n\n**Top Comment:**\n{post['comment']}"
    return desc

async def sendInfo(sub: str, interaction: discord.Interaction):
    print("="*30 + f"\ncommand: reddit ({sub} info)\n" + "="*30)
    try:
        title, desc = await sub_info(sub)        
    except Exception as e:
        await error(interaction, e)
        return
    if len(desc) > 2000:
        desc = "description too long"
    embed = discord.Embed(title=title, description=desc, colour=color)
    embed.url = f"https://reddit.com/{title}/"
    await interaction.response.send_message(embed=embed)

@tree.command(name="last_post_media", guild=discord.Object(id=ID))
async def last_post_media(interaction: discord.Interaction):
    print("="*30 + "\ncommand: last_post_media\n" + "="*30)
    if lastPost == {}:
        await interaction.response.send_message("No last post")
        return
    await interaction.response.send_message(lastPost['imgurl'])

async def error(interaction: discord.Interaction, e: Exception):
    if str(e) == "Redirect to /subreddits/search":
        err= "Subreddit not found"
    else: 
        err= "Error"
    print(err)
    embed = discord.Embed(title=f"{err} :/", color=color )
    embed.url = "https://github.com/LordRobin1/reddcord-py/issues"
    embed.set_image(url="https://tenor.com/view/error-windows-glitch-gif-5012719.gif")
    await interaction.response.send_message(embed=embed)

@tree.command(name="help", guild=discord.Object(id=ID))
async def help(interaction: discord.Interaction):
    print("="*30 + "\ncommand: help\n" + "="*30)
    lfield = "`help`:\n\n"
    lfield += "`hellothere`:\n\n"
    lfield += "`reddit`:\n\n"
    lfield += "\n\n`last_post_media`:\n\n"
    rfield = "Shows this message\n\n"
    rfield += "General Kenobi\n\n"
    rfield += "Gets a hot post from the provided subreddit\n`/reddit subreddit info`\n`/reddit` defaults to `/reddit memes`\n\n"
    rfield += "Posts the media from last post directly as message\n(usefull if gifs don't load in the embed)\n\n"
    embed = discord.Embed(title="Help", colour=color)
    embed.add_field(name="Command", value=lfield, inline=True)
    embed.add_field(name="ELI5", value=rfield, inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# events 
@client.event 
async def on_member_join(member):
    print(f"event: {member} joined")
    channel = client.get_channel(962284660992393246)
    await channel.send(f"Welcum @{member}")

client.run(TOKEN)