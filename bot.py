import discord
from discord.ext import commands, tasks

import features as features
from random import choice,randint

import youtube_dl
import ffmpeg
import asyncio


youtube_dl.utils.bug_reports_message=lambda:''

client = commands.Bot(command_prefix="|")

status=['Anong ginagawgaw mo', 'Mark bulok ka', 'Beep Boop Pap Pap','Ginagawgaw ni mark', 'Kibong nanay mo']

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
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
        await ctx.send('Kailangan nasa voice channel kagawgaw')
        return 
    else:
        channel= ctx.message.author.voice.channel

    await channel.connect()

    server=ctx.message.guild
    voiceChannel=server.voice_client

    async with ctx.typing():
        player=await YTDLSource.from_url(url, loop=client.loop,stream=True)
        voiceChannel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)

    await ctx.send(f'**Soundtrip mo:** `{player.title}` :stars:')

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

@client.command(name='ping', help='Checks the latency of RoboMark')
async def ping(ctx):
    await ctx.send("**PongPorungPong** Lag: "+str(round(client.latency*1000))+" ms")

@client.command(name='coinflip', help='Your boi flips a coin')
async def coinflip(ctx):
    await ctx.send(features.coinfliper())

@client.command(name='calcu', help='Your basic calculator ex: calcu 1 + 1')
async def calcu(ctx, num1:int, operator, num2:int):
    embed=discord.Embed(
        title="Calcu ni Mark",
        description="Ito na master teka lang di ako marunong magbilang :teacher:                  " ,
        color=discord.Color.dark_green()
    )
    embed.add_field(name="Eto hula ko oh: " + str(features.calculate(num1, operator, num2)), value=str(num1)+" "+str(operator)+" "+str(num2))
    embed.set_thumbnail(url="https://i.imgur.com/vcYOMu8.jpg")

    await ctx.send(embed=embed)

@client.command(name="hi", help=";)")
async def hi(ctx):
    if str(ctx.author)=="timmm#3989":
        await ctx.send("hi pogi :wink:")
    else:
        await ctx.send("gingawgaw mu, `{0.display_name}` HAHAHAHA".format(ctx.author))

@client.command(name="server", help="Shows the server information and etc.")
async def server(ctx):
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






player1=""
player2=""
turn=""
gameOver=True

board=[]

winningConditions= [
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
async  def tictac(ctx, p1: discord.Member, p2: discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board=[":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",]
        turn=""
        gameOver=False
        count=0

        player1=p1
        player2=p2

        #print the board
        line=""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " +board[x]
                await ctx.send(line)
                line=""
            else:
                line += " "+board[x]

        #detemine who goes first
        num=randint(1,2)
        if num ==1:
            turn = player1
            await ctx.send("Ikaw na <@" +str(player1.id)+">")
        elif num ==2:
            turn = player2
            await ctx.send("Ikaw na <@" +str(player1.id)+">")
    else:
        await ctx.send("Wait lang boss may nalaro na")

@client.command()
async def place(ctx, pos:int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark=""
        if turn == ctx.author:
            if turn == player1:
                mark=":regional_indicator_x:"
            elif turn == player2:
                mark==":o2:"
            if 0 < pos < 10 and board[pos-1]==":white_large_square:":
                board[pos-1]=mark
                count+=1

                #print board
                line=""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " +board[x]
                        await ctx.send(line)
                        line=""
                    else:
                        line += " "+board[x]

                checkWinner(winningConditions,mark)
                if gameOver:
                    await ctx.send(mark + "wins!!!!")
                elif count >=9:
                    await ctx.send("Wala tie lang kayo!")

                #switch turn
                if turn== player1:
                    turn=player2
                elif turn==player2:
                    turn=player1

            else:
                await ctx.send("Integer 1-9 lang input boy baka may lamana na yan")
        else:
            await ctx.send("Hindi pa ikaw baliw")

    else:
        await ctx.send("Hindi pa nakastart yung game")




def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]]==mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver=True

@tictac.error
async def tictac_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("2 players to lods.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Mention mo dapat yung user")

@place.error
async def place_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Lagay mo yung posisyon kung saan mo gusto")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Number lang ang input!!")

client.run(token)