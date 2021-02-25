import discord
import os
from discord.ext import commands, tasks
from random import choice
import json


def config(filename: str = "config"):
    try:
        with open(f"{filename}.json", encoding='utf8') as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

configfile = config("config")

client = commands.Bot(command_prefix="|")

status=['Anong ginagawgaw mo', 'Mark bulok ka', 'LF: GawJowa','Ginagawgaw ni mark', 'Kibong nanay mo','Gawgaw nyo pagod na','Tama na trashtalk tim','Gawgaw walang tutok', 'Tim ano ba yan','Asan kana kuya gaw','tim bat moko ginawang robot']


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
    
  else:
    print(f'Unable to load {filename[:-3]}')
    


@client.event
async def on_ready():
    changeStatus.start()
    print('Ready!')

@tasks.loop(minutes=5)
async def changeStatus():
    await client.change_presence(activity=discord.Game(choice(status)))

@client.listen()
async def on_message(message):
    if message.author==client.user:
        return
    if 'bobo' in message.content:
         await message.channel.send("Mas bobo si **gawgaw** :zany_face:")
    if '@here' in message.content:
         await message.channel.send("Nyay Loner :woozy_face: ")
    if 'Timoti' in message.content:
         await message.channel.send("Do not disturb the `master` ples")
    if 'tanga' in message.content:
         await message.channel.send("HAHAHAHA **mark** tanga :zany_face:")
    if 'gago' in message.content:
         await message.channel.send("HAHAHAHA gago ka mark")
    if 'Razz' in message.content:
         await message.channel.send("Bakit mo hinahanap yung gwapo")    
    if str(message.author)=="Gaw#0068":
        await message.add_reaction('🖕')
        await message.add_reaction('🤬')
    if str(message.author)=="timmm#3989":
        await message.add_reaction("😍")
        await message.add_reaction("❤")
        await message.add_reaction("🧡")
        await message.add_reaction("💛")
    if str(message.author)=="Boj#6437":
        await message.add_reaction("💥")
    if str(message.author)=="𝚁𝚊𝚣𝚣#1558":
        await message.add_reaction("🍆")
        await message.add_reaction("🔥")
        



        





client.run(configfile["token"])