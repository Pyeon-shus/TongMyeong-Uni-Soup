from cmath import log
from distutils.sysconfig import PREFIX
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

import discord, asyncio, datetime, pytz
from discord.ext import commands
from discord.utils import get
from discord import Member

load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
channel_id = '969983391183282258'
intents =discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    game = discord.Game('!학식 입력')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    global channel
    channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
    if message.author == client.user:
        return

    if message.content.startswith('!학식'):
        print(f'입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        async def hi(self, ctx): 
            await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(ctx.author, ctx.author.mention)) # 작성된 채널에 메세지를 출력한다.

        #웹페이지를 요청합니다.
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
        req = requests.get(url)

        #HTML을 분석합니다.
        soup = BeautifulSoup(req.text, 'html.parser')

        #필요한 데이터를 가져옵니다.
        table = soup.find('table', class_='table-st1')

        #데이터를 리스트에 저장합니다.
        data = []
        for tr in table.find_all('tr'):
           row = []
           for th in tr.find_all('th'):
                 row.append(tr.text)
           data.append(row)

        #봇에 출력하기 위해 리스트를 문자열로 변환합니다.
        result = ''
        for row in data:
            result += '\n'.join(row) + '\n'
        embed = discord.Embed(title=":fork_and_knife:오늘의 식단:fork_and_knife:", description=result,timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x4c2896)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.set_footer(text="Bot Made by. Shus#7777, , 문의는 DM으로 부탁드립니다 💬")
        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
        #await channel.send(result)

        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
