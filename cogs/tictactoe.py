from discord.ext import commands
from random import choice,randint
import discord

player1=""
player2=""
turn=""
gameOver=True

board=[]

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def tie():
        global gameOver
        gameOver = True

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


class TicTacToe(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name="tictactoe", help="play tictactoe :O")
    async def tictactoe(self,ctx, p1: discord.Member, p2: discord.Member = None):
        if p2 == None:
            p2 = ctx.author
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            await ctx.send(embed = discord.Embed(title="Tic Tac Boom Boom"))
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            num = randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("Ikaw na<@" + str(player1.id) + ">.")
            elif num == 2:
                turn = player2
                await ctx.send("Ikaw na <@" + str(player2.id) + ">.")
            else:
                await ctx.send("May naglalaro na pre teka lang")


    @commands.command(name="place", help="place your mark")
    async def place(self,ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if gameOver:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        await ctx.send("It's a tie!")
                        tie()

                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Integer 1 - 9 lang pre tsaka yung walang laman lang ah")
            else:
                await ctx.send("Hoy hindi pa ikaw")
        else:
            await ctx.send("Please start a new game using the !ttt command.")

    @commands.command(name="end", help="ends the current game")
    async def end(self,ctx):
        global gameOver
        if not gameOver:
            gameOver = True
            await ctx.send("Stopping current game...")
        else:
            await ctx.send("There is currently no game running!")

    @tictactoe.error
    async def ttt_error(self,ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a player for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping player (ie. <@797023993591889920>).")

    @place.error
    async def place_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")





def setup(client):
    client.add_cog(TicTacToe(client))