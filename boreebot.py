import discord
from discord.ext import commands
import os
from random import randint
import random
import datetime
import calendar

client = commands.Bot(command_prefix="보리야 ") 

@client.event
async def on_ready(): 

    print('start')
    await client.change_presence(
                                         status=discord.Status.online,
                                         activity=discord.Game(name="보리가 발전하는 중"))  

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

    if content == "보리야 달력":
        title = f"2020년 11월의 달력입니다." 
        em = discord.Embed(title="2020년 11월 달력", description=f"``{calendar.month(2020, 11)}``")
        await channel.send(embed=em)

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
async def 뭐해(ctx, *args):
    responses = [f"어떻게 하면 {ctx.author.name}님을 재밌게 해드릴 수 있을지 생각중이에요!",
                 "제 상태메시지를 보세요!",
                 "그렇게 전남친 같은 어조로 말씀하지 말아주세요...!",
                 f"{ctx.author.name}님 생각? ^^7",
                 "빨리 간식을 먹고 싶다는 생각중이었어요! 이래봬도 보디콜리 강아지니깐요~",
                 "제 친구 쌀은 도대체 어디 있는 걸까요? 고민중이에요.",
                 "주사위 놀이중이에요! 같이 하실래요? ``보리야 주사위`",
                 "달력을 보고 있었어요! 오늘이 며칠인지 까먹어서요... 헤헤... ``보리야 달력``",
                 "개발자님이 써주신 공지를 읽고 있어요! 전 언제쯤 알파고보다 똑똑한 천재봇으로 이름을 알릴 수 있을까요?"]
    await ctx.send(f"{random.choice(responses)}")

@client.command()
async def 공지(ctx, *args):
    await ctx.send("시간, 오늘 기능을 없애고 보리야 달력, 보리야뽑기, 보리야삭제 기능을 추가했습니다. ```띄어쓰기가 헷갈리신다면 뒤에 무언가가 붙는 건 붙여쓰고, 붙지 않는 건 띄어쓰시면 됩니다. 보리야 말해는 뺴고 ㅋㅋㄹ``` **보리가 정상작동하려면 관리자 권한이 필요한데... 그래서 보리에게 관리자 권한을 부여하였습니다. 혹여나 문제가 생길 시 제보 부탁드립니다.**")

@client.command()
async def 도움말(ctx, *args):
    await ctx.send(f"{ctx.author.name}님 안녕하세요? 봇 도움말을 안내해 드리겠습니다.")
    await ctx.send(embed=discord.Embed(title="명령어", description="```보리야 말해 <할 말>``` ```보리야 주사위``` ```보리야 달력``` ```보리야 공지``` ```보리야뽑기 <항목1> <항목2> ...``` ```보리야삭제 <지울 메시지 수>```"))   
    
client.run('NzY2Mjk1OTI3NTYwMzM5NDg4.X4hSsg.OAr3LAm2LU72VrWHBJmrlP-CX9c') 