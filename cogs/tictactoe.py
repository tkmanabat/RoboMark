from discord.ext import commands

class TicTacToe(commands.Cog):
    def __init__(self,client):
        self.client = client
    

    @commands.command()
    async def toe(self,ctx):
        await ctx.send("tac")

def setup(client):
    client.add_cog(TicTacToe(client))