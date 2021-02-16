import discord
from discord.ext import commands
from random import choice

class Quirks(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.command(name="coinflip", help="flips a coin")
    async def coinflip(self,ctx):
        await ctx.send(coinfliper())

    @commands.command(name="calcu", help="basic calculator")
    async def calcu(self,ctx, num1:int, operator, num2:int):
        embed=discord.Embed(
        title="Calcu ni Mark",
        description="Ito na master teka lang di ako marunong magbilang :teacher:                  " ,
        color=discord.Color.dark_green()
        )
        embed.add_field(name="Eto hula ko oh: " + str(calculate(num1, operator, num2)), value=str(num1)+" "+str(operator)+" "+str(num2))
        embed.set_thumbnail(url="https://i.imgur.com/vcYOMu8.jpg")

        await ctx.send(embed=embed)





def coinfliper():
    coin=['heads', 'tails']
    result=choice(coin)
    if result =='heads':
         result= '***Heads!!!*** :coin: :coin: :coin:'
         return result
    else:
        result= '***Tails!!!*** :coin: :coin: :coin:'
        return result


def calculate(num1:int , operator , num2:int):
    if operator=="+":
        return num1 + num2
    if operator=="-":
        return num1 - num2
    if operator=="x" or operator=="*":
        return num1*num2
    if operator=="/":
        return num1/num2
    else:
        return False



def setup(client):
    client.add_cog(Quirks(client))