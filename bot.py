import os
import re
import asyncpraw
import discord
from discord import app_commands
from dotenv import load_dotenv
from redditapi import get_images, sub_info, create_reddit

load_dotenv()

def setup():
    TOKEN = os.getenv('DISCORD_TOKEN')
    ID = os.getenv('GUILD_ID')
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    # reddit = create_reddit()
    return client, tree, TOKEN, ID #, reddit

client, tree, TOKEN, ID = setup()

@client.event
async def on_ready():
    print("="*30 + "\nbot is online\n" + "="*30)
    await client.wait_until_ready()
    await tree.sync(guild=discord.Object(id=ID))

#commands
@tree.command(name="test", guild=discord.Object(id=ID))
async def slash(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f'Hello {name}', ephemeral=True)

@tree.command(name="hellothere", guild=discord.Object(id=ID))
async def hellothere(interaction: discord.Interaction):
    print("="*30 + "\ncommand: hellothere\n" + "="*30)
    response = "General Kenobi"
    await interaction.response.send_message(response)


@tree.command(name="reddit", guild=discord.Object(id=ID))
async def reddit(interaction: discord.Interaction, arg: str, arg2: str=""):
    sub = arg
    if arg2 == "":
        print("="*30 + f"\ncommand: reddit ({arg})\n" + "="*30)
        try:
            post = await get_images(sub)
        except Exception as e:
            print(e)
            if e == "Redirect to /subreddits/search":
                await interaction.response.send_message("Subreddit not found :/")
                return
            await interaction.response.send_message(f"An error occured: {e}")
            return
        msg = f"{post['title']}\n{post['url']}"
        if post['type'] == "error":
            msg = f"An error occured :/ \n {post['title']}"
        if post['type'] == "gallery": 
            msg = f"{post['title']}\n{post['url']}\n*Reddit posts with gallery not supported yet*"
            await interaction.response.send_message(msg)
            return
        if post['type'] == "text":            
            try:
                msg = sendText(post)
            except Exception as e:
                print(f"error: {e}")
                msg = "Sorry, an error occured :("
        await interaction.response.send_message(msg)
        return

    if arg2 == "info":
        msg = await sendInfo(sub)
        await interaction.response.send_message(msg)
        return

def sendText(post):
    desc = ""
    if post['text'] != '': desc += post['text']
    if post['comment'] != '': desc += f"\n\n**Top Comment:**\n{post['comment']}"
    embed = discord.Embed(title=post['title'], description=desc, colour=0x87ce)
    return embed

async def sendInfo(sub):
    print("="*30 + f"\ncommand: reddit ({sub} info)\n" + "="*30)
    title, desc = await sub_info(sub)        
    if len(desc) > 4000:
        desc = "description too long"
    embed = discord.Embed(title=title, description=desc, colour=0x87CEEB)
    return embed

@tree.command(name="help", guild=discord.Object(id=ID))
async def help(interaction: discord.Interaction):
    title = "Help"
    desc = "`hellothere`\n\n" + "`help`: Shows this message\n\n" 
    desc += "`reddit`: gets a hot post from provided subreddit\n`?reddit subreddit info` (`info` optional)"
    embed = discord.Embed(title=title, description=desc, colour=discord.Colour.from_rgb(26, 188, 156))
    await interaction.response.send_message(embed=embed, ephemeral=True)

# events 
@client.event 
async def on_member_join(member):
    print(f"event: {member} joined")
    channel = client.get_channel(962284660992393246)
    await channel.send(f"welcum @{member}")

client.run(TOKEN)