from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
channel_id = '1031928945114894397'

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    channel = client.get_channel(969983391183282258) # 출력할 채널 ID를 넣어주세요

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'call':
        await channel.send("callback!")

    if message.content.startswith('$hello'):
        await channel.send('Hello!')
        
    if message.content.startswith('$학식'):
        print(f'입력됨')
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
        await channel.send(result)
        

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
