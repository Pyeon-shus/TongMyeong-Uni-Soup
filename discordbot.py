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

local_time = now
kr_tz = pytz.timezone('Asia/Seoul')
kr_time = local_time.astimezone(kr_tz)
now_string = now.strftime("%Y-%m-%d")
tomorrow = now +  datetime.timedelta(days=1)
tomo_string = tomorrow.strftime("%Y-%m-%d")
    
#------------------------------------------------------------------------------------------------------------------------------------------------    
            
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
    
#------------------------------------------------------------------------------------------------------------------------------------------------

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
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
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
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
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
            embed = discord.Embed(title=":fork_and_knife:오늘의 학식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
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
 
        embed = discord.Embed(title=":fork_and_knife:학식이 소개:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4474/4474873.png")
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="😲많은 이용부탁 드립니다!😲".format(url), value=f"", inline=False)
        embed.add_field(name="\n", value=f"\n", inline=False)
        embed.add_field(name="#현제 실행중인 명령어".format(url), value=f"!소개, !식단 출처, !학식, !내일 학식 \n!기숙사 식단 출처, !숙식", inline=False)
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

        embed = discord.Embed(title=":fork_and_knife:식단 출처:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
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

        embed = discord.Embed(title=":fork_and_knife:식단 출처:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
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
        #channel = client.get_channel(1092242713279201280)# 출력할 채널 ID를 넣어주세요
        channel = client.get_channel(620986130153603092)# 출력할 채널 ID를 넣어주세요
        print(f'!숙식 입력됨')
        import requests
        from bs4 import BeautifulSoup
        import datetime

        # 크롤링할 URL
        url = "https://www.tu.ac.kr/dormitory/sub06_06.do?mode=wList"

        # 크롤링할 페이지 요청
        res = requests.get(url)

        # 페이지 파싱
        soup = BeautifulSoup(res.text, "html.parser")

        # 학식 메뉴가 있는 박스 찾기
        box_list = soup.find_all("div", {"class": "b-cal-content-box no-list"})

        # 현재 날짜 구하기
        today = kr_time.strftime("%Y.%m.%d")
        
        # 조식 메뉴와 석식 메뉴를 저장할 문자열
        breakfast_menu_str = ""
        dinner_menu_str = ""

        # 박스마다 학식 메뉴 출력
        for box in box_list:
            # 날짜 추출
            date_box = box.find("p", {"class": "b-cal-date"})
            date_value = ""
            if date_box:
                date_text = date_box.find("span").text.strip()
                date_value = date_text.split("(")[0]

            # 날짜 정보와 현재 날짜 비교
            if date_value == today:
                # 학식 메뉴 추출
                menu_list = box.find_all("ul", {"class": "b-cal-undergrad"})
                # 박스마다 학식 메뉴 출력
                for box in box_list:
                    # 날짜 추출
                    date_box = box.find("p", {"class": "b-cal-date"})
                    date_value = ""
                    if date_box:
                        date_text = date_box.find("span").text.strip()
                        date_value = date_text.split("(")[0]

                    # 날짜 정보와 현재 날짜 비교
                    if date_value == today:
                        # 학식 메뉴 추출
                        menu_list = box.find_all("ul", {"class": "b-cal-undergrad"})
                        
                        embed = discord.Embed(title=":fork_and_knife:오늘의 숙식:fork_and_knife:", description="",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00b992)
                        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4916/4916579.png")
                        embed.add_field(name="\n", value=f"\n", inline=False)

                        # 메뉴 출력
                        for menu in menu_list:
                            # 메뉴 항목 추출
                            menu_items = menu.find_all("li")
                            # 메뉴 출력
                            for item in menu_items:
                                menu_text = item.text.strip()

                                # ":" 기준으로 분리
                                menu_split = menu_text.split(":")

                                # 분리된 항목이 조식/석식인 경우
                                if menu_split[0] == "조식 ":
                                    if len(breakfast_menu_str) > 0:
                                        breakfast_menu_str += "\n"
                                    breakfast_menu_str += menu_split[1]
                                elif menu_split[0] == "A코스 " or menu_split[0] == "B코스 ":
                                    if len(breakfast_menu_str) > 0:
                                        breakfast_menu_str += "\n"
                                    breakfast_menu_str += (" " + menu_text)
                                elif menu_split[0] == "석식 ":
                                    if len(dinner_menu_str) > 0:
                                        dinner_menu_str += "\n"
                                    dinner_menu_str += menu_split[1]
                                    
                        if len(breakfast_menu) > 0:
                            for menu in breakfast_menu:
                                menu += '\n'.join(breakfast_menu) + '\n'
                            embed.add_field(name="#조식", value=f"{menu}\n\n", inline=False)
                        else:
                            embed.add_field(name="#조식", value=f"오늘 조식 메뉴가 없습니다.\n\n", inline=False)
                        embed.add_field(name="\n", value=f"\n", inline=False)
                        
                        if len(dinner_menu) > 0:
                            embed.add_field(name="#석식", value=f"{dinner_menu}\n\n", inline=False)
                        else:
                            embed.add_field(name="#석식", value=f"오늘 석식 메뉴가 없습니다.\n\n", inline=False)
                        embed.add_field(name="\n", value=f"\n", inline=False)
                        
                        #embed.add_field(name=" ", value=f"⚠️!숙식은 현재 불안정 합니다 차후 수정할 계획입니다.⚠️\n", inline=False)
                        embed.add_field(name="\n", value=f"\n", inline=False)
                        embed.add_field(name=" ", value=f"식단 출처: {url}\n\n", inline=False)
                        embed.set_footer(text="Bot Made by. Shus#7777, 자유롭게 이용해 주시면 됩니다.")
                        await channel.send (embed=embed) #채팅방에 출력되도록 하려면 messae.channel.send 로 바꾸면 된다.
                        #await message.author.send (embed=embed) #유저 개인 DM으로 전송한다.
                        #await channel.send(result)
                        print(f'정상 출력됨\n')

#------------------------------------------------------------------------------------------------------------------------------------------------

#async def my_background_task():
#    await client.wait_until_ready()
#    channel = client.get_channel(969983391183282258) # 출력할 채널 ID 입력
#    while True:
#        now = datetime.datetime.now()
#        if now.hour == 9 and now.minute == 0: # 매일 오전 9시
#            await channel.send(Today_Uni_Soup()) # 함수 실행
#        await asyncio.sleep(60) # 1분마다 반복
#
#client.loop.create_task(my_background_task())

#------------------------------------------------------------------------------------------------------------------------------------------------
        
        
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
