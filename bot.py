import discord
from discord.ext import commands, tasks
from random import choice
from glob import glob


client = commands.Bot(command_prefix="|")

status=['Anong ginagawgaw mo', 'Mark bulok ka', 'Beep Boop Pap Pap','Ginagawgaw ni mark', 'Kibong nanay mo']


cogs=[path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
for cog in cogs:
    client.load_extension(f"cogs.{cog}")
    print(f"{cog} cog has loaded")


@client.event
async def on_ready():
    changeStatus.start()
    print('Ready!')

@tasks.loop(minutes=20)
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


client.run(token)