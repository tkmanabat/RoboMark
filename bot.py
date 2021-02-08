import discord

client = discord.Client()

@client.event
async def on_message(message):
    message.content=message.content.lower()
    if message.author==client.user:
        return 
    if message.content.startswith("hello"):
       
        if str(message.author)=="timmm#3989":
            await message.channel.send("Hello my maker")
        else:
             await message.channel.send("Hello! Gawgaw bulok")

client.run("ODA3ODY4NTgzOTcxMjU4Mzc4.YB-QPw.3VgP4zLhWH2p9xfJpzun3psJoZk")