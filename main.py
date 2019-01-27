import discord
import os
import json
import random
import time
import requests
from discord.ext.commands import Bot
from discord.ext import commands

access_token= os.environ["BOT_TOKEN"]
Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

TOKEN = access_token

@client.event
async def on_ready():
    print("Link builder online")
    print("name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    if message.content.startswith('!build'):
        vars = []
        titles = []
        messageSplit = message.content.split(' ')
        link = messageSplit[1]
        site = link.split('/')
        site = site[2]
        print(site)
        print(link + ".json")
        r = requests.get(link + ".json")
        r = r.json()
        prodname = r["product"] ["title"]
        for i in r["product"] ["variants"]:
            id = i['id']
            vars.append(id)
            title = i['title']
            titles.append(title)
        embed = discord.Embed(title="ATC Builder", description=prodname, color=16711680)
        embed.set_footer(text=message.server.name)
        x = 0
        for i in titles:
            embed.add_field(name=str(i), value="https://" + site + "/cart/" + str(vars[x]) + ":1", inline=False)
            x = x+1
        embed.set_footer(text=message.server.name)
        await client.send_message(message.channel, embed=embed)

client.run(TOKEN)
