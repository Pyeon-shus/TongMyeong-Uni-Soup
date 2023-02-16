from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import urllib.request
from bs4 import BeautifulSoup
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')
    if message.content.startswith(f'{PREFIX}학식'): { ## "?"이라고 말했을때
       import urllib.request
        #웹 페이지를 요청합니다.
        html = urllib.request.urlopen('https://www.tu.ac.kr/tuhome/diet.do?sch')

        #HTML을 분석합니다.
        soup = BeautifulSoup(html, 'html.parser')

        #필요한 데이터를 가져옵니다.
        table = soup.find('table', class_='table-st1')

        #데이터를 리스트에 저장합니다.
        data = []
        for tr in table.find_all('tr'):
           row = []
           for td in tr.find_all('td'):
              row.append(td.text)
           data.append(row)

        #봇에 출력하기 위해 리스트를 문자열로 변환합니다.
        result = ''
        for row in data:
            result += '\n'.join(row) + '\n'

        #결과를 봇으로 출력합니다.
        msg.reply(result)



try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
