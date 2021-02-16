import discord
from discord.ext import commands, tasks

import features as features
from random import choice,randint

import youtube_dl
import ffmpeg
import asyncio

from glob import glob


youtube_dl.utils.bug_reports_message=lambda:''

client = commands.Bot(command_prefix="|")

status=['Anong ginagawgaw mo', 'Mark bulok ka', 'Beep Boop Pap Pap','Ginagawgaw ni mark', 'Kibong nanay mo']

cogs=[path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]

for cog in cogs:
    client.load_extension(f"cogs.{cog}")
    print(f"{cog} cog has loaded")


queueSong=[]

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@client.command(name='play', help='This command plays some music from youtube')
async def play(ctx,url):

    if not ctx.message.author.voice:
        await ctx.send('Kailangan nasa voice channel ka gawgaw')
        return 
    else:
        channel= ctx.message.author.voice.channel

    await channel.connect()

    
    global queueSong
    queueSong.append(url)

    server=ctx.message.guild
    voiceChannel=server.voice_client

    async with ctx.typing():
        player=await YTDLSource.from_url(queueSong[0], loop=client.loop,stream=True)
        voiceChannel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)
        del(queueSong[0])


    await ctx.send(f'**Soundtrip mo:** `{player.title}` :stars:')

@client.command(name='queue')
async def queue(ctx, url):
    global queueSong

    queueSong.append(url)
    await ctx.send(f"Nadagdag na to boss: `{url}` ")

@client.command(name='remove')
async def remove(ctx, number):
    global queueSong

    try:
        del(queueSong[int(number)])
        await ctx.send(f'Ito na nakapila boss `{queueSong}`')
    
    except :
        await ctx.send('Wala naman na tugtog eh!!!')

@client.command(name='view', help='show the queue')
async def view(ctx):
    await ctx.send(f"Ito yung line up boss: `{queueSong}`")


@client.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send('Kailangan nasa voice channel ka gawgaw')
        return 
    else:
        channel= ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='leave', help='This command stops the music currently playing and leaves the voice channel')
async def leave(ctx):
    voiceClient= ctx.message.guild.voice_client
    await voiceClient.disconnect()



@client.command(name='stop', help='This command stops the music currently playing and leaves the voice channel')
async def stop(ctx):
    voiceClient= ctx.message.guild.voice_client
    await voiceClient.disconnect()


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



player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

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

@client.command()
async def ttt(ctx, p1: discord.Member, p2: discord.Member = None):
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

@client.command()
async def place(ctx, pos: int):
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

@client.command()
async def end(ctx):
  global gameOver
  if not gameOver:
    gameOver = True
    await ctx.send("Stopping current game...")
  else:
    await ctx.send("There is currently no game running!")

def tie():
  global gameOver
  gameOver = True

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@ttt.error
async def ttt_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a player for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping player (ie. <@797023993591889920>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")




client.run("ODA3ODY4NTgzOTcxMjU4Mzc4.YB-QPw.6MRruxiMZknORQKwOcm1ULUtiRI")