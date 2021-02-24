import discord

from discord.ext import commands

class memes(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.command()
def setup(client):
    client.add_cog(memes(client))