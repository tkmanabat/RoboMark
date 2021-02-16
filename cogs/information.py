import discord
from discord.ext import commands

class Information(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.command(name="ping", help="Checks the latency")
    async def ping(self,ctx):
        await ctx.send("**PongPorungPong** Lag: "+str(round(self.client.latency*1000))+" ms")

    @commands.command(name="server", help="Check server info")
    async def server(self,ctx):
        name=str(ctx.guild.name)
        description=str(ctx.guild.description)
        owner=str(ctx.guild.owner)
        id=str(ctx.guild.id)
        region=str(ctx.guild.region)
        memberCount=str(ctx.guild.member_count)
        icon=str(ctx.guild.icon_url)

        embed=discord.Embed(
            title="Server information ng " + name,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Amo", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Rehiyon", value=region, inline=True)
        embed.add_field(name="Ilan Nandirito", value=memberCount, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="hi", help=";)")
    async def hi(self,ctx):
        if str(ctx.author)=="timmm#3989":
            await ctx.send("Hi `pogi` :wink:")
        else:
            await ctx.send("Ginagawgaw mo, `{0.display_name}` HAHAHAAHAHAH".format(ctx.author))


def setup(client):
    client.add_cog(Information(client))