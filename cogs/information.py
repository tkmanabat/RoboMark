import discord
from discord.ext import commands
from aiohttp import request

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

    @commands.command(name="covid",help="get philippine covid stats")
    async def covid(self,ctx):
        URL="https://disease.sh/v3/covid-19/countries/Philippines?yesterday=true&twoDaysAgo=false&strict=true&allowNull=true"

        async with request("GET",URL,headers=[]) as response:
            if response.status==200:
                data=await response.json()

                
                embed=discord.Embed(
                title="COVID-19 Information Philippines",
                description="Latest Information as of today",
                color=discord.Color.green()
                )
                embed.set_thumbnail(url="https://banner2.cleanpng.com/20180829/wvu/kisspng-flag-of-the-philippines-philippine-declaration-of-philiooines-flag-png-5b875882c25497.893421191535596674796.jpg")
                embed.add_field(name="Total Cases", value=data["cases"], inline=True)
                embed.add_field(name="Dumagdag Ngayon", value=data["todayCases"], inline=True)
                embed.add_field(name="Namatay Ngayon", value=data["todayDeaths"], inline=False)
                embed.add_field(name="Active Cases", value=data["active"], inline=True)

                await ctx.send(embed=embed)
            else: 
                await ctx.send(f"API returned a {response.status} status")



    @commands.command(name="hi", help=";)")
    async def hi(self,ctx):
        if str(ctx.author)=="timmm#3989":
            await ctx.send("Hi `pogi` :wink:")
        else:
            await ctx.send("Ginagawgaw mo, `{0.display_name}` HAHAHAAHAHAH".format(ctx.author))


def setup(client):
    client.add_cog(Information(client))