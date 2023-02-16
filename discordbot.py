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

    if message.content == f'{PREFIX}call':
        await channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await channel.send('Hello!')
        
    if message.content.startswith(f'{PREFIX}학식'):
        print('입력됨')
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meal_list = soup.find_all(class_='table-wrap')
        result = "오늘의 식단은 \n \n"
        for meals in meal_list:
            meal_name = meals.find('th').get_text()
            meal_detail = meals.find('td').get_text()
            result += f"{meal_name}: {meal_detail}\n"
        await channel.send(result)
        

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
