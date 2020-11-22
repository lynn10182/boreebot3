import discord
from discord.ext import commands
import os
from random import randint
import youtube_dl
import datetime
from Modules.search import Search

d = datetime.datetime.now()
client = commands.Bot(command_prefix="보리야 ") 

@client.event
async def on_ready(): 

    print('start')
    await client.change_presence(
                                         status=discord.Status.online,
                                         activity=discord.Game(name="볼희"))  

@client.event
async def on_message(message):  
    author = message.author  
    channel = message.channel  
    content = message.content
    search = Search()
    
    if author.bot:
        return None 
   
    if content == "보리야":
        await channel.send("나 불렀어요?")
    await client.process_commands(message)
    
    if content.startswith("보리야 검색"):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_youtube(msg1[1:]))
        
    if content.startswith("보리야 사진"):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_image(msg1[1:]))
        
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
    await ctx.send(f"어떻게 하면 {ctx.author.name}님을 재밌게 해드릴 수 있을지 생각중이에요!")

@client.command()
async def 공지(ctx, *args):
    await ctx.send("시간, 오늘 기능을 없앴습니다.")

@client.command()
async def 도움말(ctx, *args):
    await ctx.send(f"{ctx.author.name}님 안녕하세요? 봇 도움말을 안내해 드리겠습니다.")
    await ctx.send(embed=discord.Embed(title="명령어", description="보리야 말해 <할 말>, 보리야 주사위, 보리야 시간, 보리야 오늘, 보리야 공지"))   

access_token = os.environ['BOT_TOKEN']    
client.run(access_token) 