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
now = datetime.datetime.now()
now_string = now.strftime("%Y-%m-%d")
tomorrow = now +  datetime.timedelta(days=1)
tomo_string = tomorrow.strftime("%Y-%m-%d")


@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    game = discord.Game('!학식, !숙식 대기')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    global channel
    if message.author == client.user:
        return

    if message.content.startswith('!학식'):
        channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
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
        
        if table:
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
            #result = ''
            #for row in data:
            #    result += '\n'.join(row) + '\n'
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
            result = ''
            for row in yangsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="#양식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in myeonryu:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#면류", value=f"{result}\n\n", inline=False)
            result = ''
            for row in bunsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#분식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in teukjeongsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#특정식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in ddukbaegi:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#뚝배기", value=f"{result}\n\n", inline=False)
            result = ''
            for row in ilpum:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#일품", value=f"{result}\n", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
            embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
            await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
            #await channel.send(result)
            print(f'정상 출력됨\n')
        else:
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="⚠️{}에 등록된 식단메뉴가 없습니다⚠️".format(now_string), value=f"", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
            embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
            await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
            #await channel.send(result)
            print(f'정상 출력됨\n')

#------------------------------------------------------------------------------------------------------------------------------------------------            
            
    elif message.content.startswith('!내일 학식'):
        channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
        print(f'!내일 학식 입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        #user = message.mentions[1] # '!학식' 에서 유저정보를 user에 담는다.
        #await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(user.author, user.mention)) # 작성된 채널에 메세지를 출력한다.
        #await channel.send ("{} | {}님이 '!학식'을 입력하셨습니다.".format(channel.author, channel.author.mention)) # 작성된 채널에 메세지 출력
        
        #웹페이지를 요청합니다.
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
        Or_url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
        Ad_date = 'Date=' + tomo_string
        url = Or_url+Ad_date
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
        
        if table:
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
            #result = ''
            #for row in data:
            #    result += '\n'.join(row) + '\n'
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
            result = ''
            for row in yangsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="#양식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in myeonryu:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#면류", value=f"{result}\n\n", inline=False)
            result = ''
            for row in bunsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#분식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in teukjeongsik:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#특정식", value=f"{result}\n\n", inline=False)
            result = ''
            for row in ddukbaegi:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#뚝배기", value=f"{result}\n\n", inline=False)
            result = ''
            for row in ilpum:
                result += '\n'.join(row) + '\n'
            embed.add_field(name="#일품", value=f"{result}\n", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
            embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
            await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
            #await channel.send(result)
            print(f'정상 출력됨\n')
        else:
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="⚠️{}에 등록된 식단메뉴가 없습니다⚠️".format(tomo_string), value=f"", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
            embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
            await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
            #await channel.send(result)
            print(f'정상 출력됨\n')
            
#------------------------------------------------------------------------------------------------------------------------------------------------
           
    elif message.content.startswith('!소개'):
        channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
        print(f'!소개 입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        #user = message.mentions[1] # '!학식' 에서 유저정보를 user에 담는다.
        #await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(user.author, user.mention)) # 작성된 채널에 메세지를 출력한다.
        #await channel.send ("{} | {}님이 '!학식'을 입력하셨습니다.".format(channel.author, channel.author.mention)) # 작성된 채널에 메세지 출력
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'
 
        embed = discord.Embed(title=":fork_and_knife:학식이 소개:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="😲많은 이용부탁 드립니다!😲".format(url), value=f"", inline=False)
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="#현제 실행중인 명령어".format(url), value=f"!소개, !식단 출처, !학식, !내일 학식,", inline=False)
        embed.add_field(name="".format(url), value=f"!기숙사 식단 출처, !숙식,", inline=False)
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
        #await channel.send(result)
        print(f'정상 출력됨\n')

#------------------------------------------------------------------------------------------------------------------------------------------------            
           
    elif message.content.startswith('!식단 출처'):
        channel = client.get_channel(969983391183282258)# 출력할 채널 ID를 넣어주세요
        print(f'!식단 출처 입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        #user = message.mentions[1] # '!학식' 에서 유저정보를 user에 담는다.
        #await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(user.author, user.mention)) # 작성된 채널에 메세지를 출력한다.
        #await channel.send ("{} | {}님이 '!학식'을 입력하셨습니다.".format(channel.author, channel.author.mention)) # 작성된 채널에 메세지 출력
        url = 'https://www.tu.ac.kr/tuhome/diet.do?sch'

        embed = discord.Embed(title=":fork_and_knife:식단 출처:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="😲식단 출처: {}😲".format(url), value=f"", inline=False)
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
        #await channel.send(result)
        print(f'정상 출력됨\n')
 
#------------------------------------------------------------------------------------------------------------------------------------------------            
           
                   
    elif message.content.startswith('!기숙사 식단 출처'):
        channel = client.get_channel(620986130153603092)# 출력할 채널 ID를 넣어주세요
        print(f'!숙식 출처 입력됨')
        #입력한 채팅을 삭제한다.
        #await message.delete()
        #user = message.mentions[1] # '!학식' 에서 유저정보를 user에 담는다.
        #await channel.send("{} | {} 님이 '!학식'을 입력하셨습니다.".format(user.author, user.mention)) # 작성된 채널에 메세지를 출력한다.
        #await channel.send ("{} | {}님이 '!학식'을 입력하셨습니다.".format(channel.author, channel.author.mention)) # 작성된 채널에 메세지 출력
        url = 'https://www.tu.ac.kr/dormitory/index.do#nohref'

        embed = discord.Embed(title=":fork_and_knife:식단 출처:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="😲식단 출처: {}😲".format(url), value=f"", inline=False)
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
        #await channel.send(result)
        print(f'정상 출력됨\n')
 
#------------------------------------------------------------------------------------------------------------------------------------------------            

            
    elif message.content.startswith('!숙식'):
        channel = client.get_channel(620986130153603092)# 출력할 채널 ID를 넣어주세요
        print(f'!숙식 입력됨')
        # 웹페이지를 요청합니다.
        url = 'https://www.tu.ac.kr/dormitory/index.do#nohref'
        req = requests.get(url)

        # HTML을 분석합니다.
        soup = BeautifulSoup(req.text, 'html.parser')

        # 필요한 데이터를 가져옵니다.
        tabs_con_wrap = soup.find('div', class_='tabs-con-wrap')

        # 각 식사 종류에 해당하는 메뉴를 따로 저장합니다.
        dinner = []
        breakfast = []

        for tabs_con in tabs_con_wrap.find_all('div', class_='tabs-con'):
            for li in tabs_con.find_all('li', class_='item'):
                
                course = li.find('div', class_='course')
                detail = li.find('div', class_='detail')
                row = detail.text.replace('\n', '').strip()
                if course.text == '석식' and row not in dinner:
                    dinner.append(row)
                elif course.text == '조식' and row not in breakfast:
                    breakfast.append(row)

        # 각각의 식사 종류에 해당하는 메뉴들을 출력합니다.
        
        embed = discord.Embed(title=":fork_and_knife:오늘의 숙식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x96C81E)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4916/4916579.png")
        result = ''
        if breakfast:
            for row in breakfast:
                result += ''.join(row)
                embed.add_field(name="\n", value=f"\n", inline=False)
                embed.add_field(name="#조식", value=f"{result}\n\n", inline=False)
                result = ''
        else:
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="#조식", value=f"오늘은 조식이 제공되지 않습니다\n\n", inline=False)
            result = ''
            
        if  dinner :  
            for row in dinner:
                result += ''.join(row)
                embed.add_field(name="#석식", value=f"{result}\n\n", inline=False)
                embed.add_field(name=" ", value=f"⚠️!숙식은 현재 불안정 합니다 차후 수정할 계획입니다.⚠️\n", inline=False)
                embed.add_field(name="\n", value=f"\n", inline=False)
                embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
                embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
                await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
                #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
                #await channel.send(result)
                print(f'정상 출력됨\n')
        else:
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name="#조식", value=f"오늘은 석식이 제공되지 않습니다\n\n", inline=False)
            result = ''
            embed.add_field(name=" ", value=f"⚠️!숙식은 현재 불안정 합니다 차후 수정할 계획입니다.⚠️\n", inline=False)
            embed.add_field(name="\n", value=f"\n", inline=False)
            embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
            embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
            await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
            #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
            #await channel.send(result)
            print(f'정상 출력됨\n')
        
        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
