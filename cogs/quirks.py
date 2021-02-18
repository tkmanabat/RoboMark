import discord
from discord.ext import commands
from random import choice,randint

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

    @commands.command(name="guess", help="guessing game")
    async def guess(self,ctx):
        lives=3
        number=randint(1,10)
        await ctx.send("Guess the number from `1 to 10` :zany_face:")
        await ctx.send("Enter the guess only ex: `1`")

        while lives !=-1:

            if lives==0:
                lives=lives-1
                await ctx.send(f"Game Over!!! The number was {number}")
                break

            guess=await self.client.wait_for("message",timeout=30)

            if int(guess.content)>number:
                lives=lives-1
                await ctx.send(f"Your guess is **TOO BIG** , you have `{lives}` attempts left")
            elif int(guess.content)<number:
                lives=lives-1
                await ctx.send(f"Your guess is **TOO SMALL** ,  you have `{lives}` attempts left")
            elif int(guess.content)==number:
                await ctx.send("Your guess is ***Correct*** :exploding_head: :exploding_head: :exploding_head: ")
                break
            







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