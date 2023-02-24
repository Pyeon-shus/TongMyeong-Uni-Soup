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
        print(f'!학식 입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        #user = message.mentions[1] # '!학식' 에서 유저정보를 user에 담는다.
        #await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(user.author, user.mention)) # 작성된 채널에 메세지를 출력한다.
        #await channel.send ("{} | {}님이 '!학식'을 입력하셨습니다.".format(channel.author, channel.author.mention)) # 작성된 채널에 메세지 출력
        
        #웹페이지를 요청합니다.
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
        req = requests.get(url)

        #HTML을 분석합니다.
        soup = BeautifulSoup(req.text, 'html.parser')

        #필요한 데이터를 가져옵니다.
        table = soup.find('table', class_='table-st1')

        #각 음식 종류에 해당하는 메뉴를 따로 저장합니다.
        yangsik = []
        myeonryu = []
        bunsik = []
        teukjeongsik = []
        ddukbaegi = []
        ilpum = []

        for tr in table.find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            row = []
            if th and td:
                if th.text == '양식':
                    row.append(td.text)
                    yangsik.append(row)
                elif th.text == '면류':
                    row.append(td.text)
                    myeonryu.append(row)
                elif th.text == '분식':
                    row.append(td.text)
                    bunsik.append(row)
                elif th.text == '특정식':
                    row.append(td.text)
                    teukjeongsik.append(row)
                elif th.text == '뚝배기':
                    row.append(td.text)
                    ddukbaegi.append(row)
                elif th.text == '일품':
                    row.append(td.text)
                    ilpum.append(row)
                    
                    

        #봇에 출력하기 위해 리스트를 문자열로 변환합니다.
        result = ''
        #for row in data:
        #    result += '\n'.join(row) + '\n'
        embed = discord.Embed(title=":fork_and_knife:오늘의 식단:fork_and_knife:", description="{} 의 정보를 가져옵니다.".format(url),timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        for row in yangsik:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="양식", value=f"{yangsik}", inline=False)
        for row in myeonryu:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="면류", value=f"{myeonryu}", inline=False)
        for row in bunsik:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="분식", value=f"{bunsik}", inline=False)
        for row in teukjeongsik:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="특정식", value=f"{teukjeongsik}", inline=False)
        for row in ddukbaegi:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="뚝배기", value=f"{ddukbaegi}", inline=False)
        for row in ilpum:
            result += '\n'.join(row) + '\n'
        embed.add_field(name="일품", value=f"{ilpum}", inline=False)
        embed.set_footer(text="Bot Made by. Shus#7777_________________________________")
        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
        #await channel.send(result)

        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
