import  discord
from discord.ext import commands
from core.classes import Cog_extension
import pandas as pd
import requests
import random
import time
import json

with open('setting.json','r', encoding='utf8' ) as jfile:
    jdata = json.load(jfile)

class main(Cog_extension):

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')
        #ctx = context 包含有頻道參數 latency延遲 round小數點四捨五入 await 頻道位置.send傳送訊息到頻道上
    

def setup(bot):
    bot.add_cog(main(bot))