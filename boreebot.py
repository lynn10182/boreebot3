import discord
from discord.ext import commands
import os
from random import randint
import random
import datetime
import calendar
import asyncio
import openpyxl

client = commands.Bot(command_prefix="보리야 ") 
d = datetime.datetime.now()

@client.event
async def on_ready(): 

    print('start')
    await client.change_presence(
                                         status=discord.Status.online,
                                         activity=discord.Game(name="보리~ 보리~ 쌀!"))  

@client.event
async def on_message(message):  
    author = message.author  
    channel = message.channel  
    content = message.content
    now = datetime.datetime.now()
    
    if author.bot:
        return None 
   
    if content == "보리야":
        await channel.send("나 불렀어요?")

    if content.startswith("보리야뽑기"):
        msg1 = content.split(' ')
        if len(msg1) > 1:
            srp = random.choice(msg1[1:])
        else:
            srp = random.choice()
        embed = discord.Embed(title="뽑기 결과", description=srp)
        await channel.send(embed=embed)

    if message.content.startswith("보리야삭제"):
        msg = content.split(' ')
        try:
            if int(msg[1]) < 100:
                await message.delete()
                await channel.purge(limit=int(msg[1]))
                await channel.send("다량의 메시지를 삭제하였습니다.")
            else:
                await message.delete()
                await channel.send("100개 이상의 메시지는 삭제할 수 없습니다.")
        except discord.DiscordException:
            return
      
    if content.startswith("보리야배워"):
        file = openpyxl.load_workbook("기억.xlsx")
        sheet = file.active
        learn = content.split(" ")
        for i in range(1, 101):
            if sheet["A" + str(i)].value == "-":
                sheet["A" + str(i)].value = learn[1]
                sheet["B" + str(i)].value = learn[2]
                await channel.send("단어를 배웠습니다. 보리야기억으로 물어봐주세요!")
                break
        file.save("기억.xlsx")

    if content.startswith("보리야기억"):
        file = openpyxl.load_workbook("기억.xlsx")
        sheet = file.active
        memory = content.split(" ")
        for i in range(1, 101):
            if sheet["A" + str(i)].value == memory[1]:
                await channel.send(sheet["B" + str(i)].value)
                break
        
    await client.process_commands(message)
    
@client.command() 
async def 말해(ctx, *args):

    content = ' '.join(args) 
    
    if args == (): 
        await ctx.send("뭘 말해요? 님 바보라고요?")  
        return None

    await ctx.send(content)  

@client.command() 
async def 주사위(ctx, *args):
    await ctx.send(f"데굴데굴... :game_die: 몇이 나올까? **{randint(1, 6)}**")

@client.command() 
async def 안녕(ctx, *args):
    await ctx.send(f"{ctx.author.name}님 안녕하세요? 보리랑 같이 놀아요! ``보리야 도움말``")

@client.command() 
async def 오늘(ctx, *args):
    await ctx.send(f"오늘은 {datetime.date.today()}!")

@client.command() 
async def 뭐해(ctx, *args):
    responses = [f"어떻게 하면 {ctx.author.name}님을 재밌게 해드릴 수 있을지 생각중이에요!",
                 "제 상태메시지를 보세요!",
                 "그렇게 전남친 같은 어조로 말씀하지 말아주세요...!",
                 f"{ctx.author.name}님 생각? ^^7",
                 "빨리 간식을 먹고 싶다는 생각중이었어요! 이래봬도 보디콜리 강아지니깐요~",
                 "제 친구 쌀은 도대체 어디 있는 걸까요? 고민중이에요.",
                 "주사위 놀이중이에요! 같이 하실래요? ``보리야 주사위``",
                 "달력을 보고 있었어요! 오늘이 며칠인지 까먹어서요... 헤헤... ``보리야 오늘``",
                 "개발자님이 써주신 공지를 읽고 있어요! 전 언제쯤 알파고보다 똑똑한 천재봇으로 이름을 알릴 수 있을까요? ``보리야 공지``"]
    await ctx.send(f"{random.choice(responses)}")

@client.command() 
async def 자니(ctx, *args):
    responses2 = ["*밖이야...*?",
                 "*자는구나...*",
                 "*많이 보고싶다...*",
                 "*보면 연락줘...*",
                 "*곧 생일이지...? 축하해...*",
                 "*우리.. 좋았잖아...*",
                 "*그래... 잘자...*",
                 "*난 너가 많이 그리워...*",
                 "*우리... 그때로 다시 돌아갈 수 있을까...?*"]
    await ctx.send(f"{random.choice(responses2)}")

@client.command()
async def 자는구나(ctx):
    await ctx.send("다음 말이 예상이 가는 건 기분탓?")

@client.command()
async def 잘자(ctx):
    message = await ctx.send("**그만해 역겨워**")
    await asyncio.sleep(2)
    await message.edit(content="제가 별 말 했나요? ㅎㅎ")
    
@client.command()
async def 바보(ctx):
    message = await ctx.send("**님이 더 바보임**")
    await asyncio.sleep(2)
    await message.edit(content="제가 별 말 했나요? ㅎㅎ")

@client.command()
async def 시간(ctx):
    message = await ctx.send("그 기능은 개발자님이 없애신지 오랜데... **바보 ㅋㅋ**")
    await asyncio.sleep(3)
    await message.edit(content="제가 별 말 했나요? ㅎㅎ")
    
@client.command()
async def 공지(ctx):
    message = await ctx.send("나 김볼희에게 개발자님이 커맨드 예외처리를 넣어주셨다! 이제 아무말이나 해도 알아먹는다! ~~모르는 말은 똑같은 반응만 반복할거임~~")

@client.command()
async def 도움말(ctx, *args):
    await ctx.send(f"{ctx.author.name}님 안녕하세요? 봇 도움말을 안내해 드리겠습니다.")
    await ctx.send(embed=discord.Embed(title="명령어", description="```보리야 말해 <할 말>``` ```보리야 주사위``` ```보리야 오늘``` ```보리야 공지``` ```보리야뽑기 <항목1> <항목2> ...``` ```보리야삭제 <지울 메시지 수>```"))   
    
@client.event
async def on_command_error(ctx, error):
    await ctx.send("무슨 말인지 모르겠어요!")
    
access_token = os.environ['BOT_TOKEN']
client.run(access_token) 
