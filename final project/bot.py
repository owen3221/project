import  discord
import pandas as pd
import requests
import random
import time
from discord.ext import commands
import json
import random
import os



with open('setting.json','r', encoding='utf8' ) as jfile:
    jdata = json.load(jfile)


bot = commands.Bot(command_prefix=";")
#prefix 呼叫機器人的起始命令


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'已加載{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'已卸載{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'已重載{extension}')


for Filename in os.listdir('./cmds'): #用for導入所有類別
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')#做的事情跟form ... import ... 一樣

if __name__ == "__main__":
    bot.run(jdata["TOKEN"])
    #啟動機器人