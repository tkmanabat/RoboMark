import discord
from discord.ext import commands
import datetime
import asyncio
import random
from random import choice

from PIL import Image
from io import  BytesIO
class memes(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.command(name="meme", help="Alamin ang iyong worth")
    async def meme(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        meme=['meme1','meme2','meme3']
        result=choice(meme)
        if result == 'meme1':
            meme = Image.open("meme.jpg")

            asset = user.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)

            pfp = pfp.resize((121,121))
            meme.paste(pfp, (156,81))
            meme.save("profile.jpg")
            await ctx.send(file = discord.File("profile.jpg"))
        elif result == 'meme2':
            meme = Image.open("panelo.jpg")

            asset = user.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)

            pfp = pfp.resize((364,364))
            meme.paste(pfp, (821,183))
            meme.save("profile.jpg")
            await ctx.send(file = discord.File("profile.jpg"))
        elif result == 'meme3':
            meme = Image.open("rip.jpg")

            asset = user.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)

            pfp = pfp.resize((119,119))
            meme.paste(pfp, (237,167))
            meme.save("profile.jpg")
            await ctx.send(file = discord.File("profile.jpg"))




        

def setup(client):
    client.add_cog(memes(client))
    