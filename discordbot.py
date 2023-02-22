from cmath import log
from distutils.sysconfig import PREFIX
import discord
import datetime
import pytz
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
channel_id = '969983391183282258'
client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    channel = client.get_channel(969983391183282258) # 출력할 채널 ID를 넣어주세요
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    game = discord.Game('!학식 입력')
    await client.change_presence(status=discord.Status.online, activity=game)

class simple(commands.Cog): 

    def __init__(self, app):
        self.app = app 
    
    @commands.command(name="인사") # '!인사' 를 입력한다면
    async def hi(self, ctx): 
        await ctx.send("{} | {} 님 안녕하세요!".format(ctx.author, ctx.author.mention)) # 작성된 채널에 메세지를 출력한다.
        await ctx.author.send("{} | {} 님 안녕하세요!".format(ctx.author, ctx.author.mention)) # 작성한 유저에게 DM으로 메세지를 출력한다.

    @commands.command(name="식단") # '!식단'를 입력한다면
    async def information(self,ctx):
        embed = discord.Embed(title=":fork_and_knife:오늘의 식단:fork_and_knife:", description=result,timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x4c2896)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.set_footer(text="Bot Made by. Shus#7777, , 문의는 DM으로 부탁드립니다 💬")
        await ctx.send(embed=embed)

        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
