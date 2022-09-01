import  discord
from discord.ext import commands
from core.classes import Cog_extension
import pandas as pd
import requests
import random
import time
import json
import numpy as np
import matplotlib.pyplot as plt

with open('setting.json','r', encoding='utf8' ) as jfile:
    jdata = json.load(jfile)


class react(Cog_extension):



    @commands.command()#傳送貓貓圖片
    async def cutecat(self,ctx):
        randomcat = random.choice(jdata["cutecatpic"])
        cat = discord.File(randomcat)
        await ctx.send(file = cat)
    
    @commands.command()
    async def profile(self,ctx):
        embed=discord.Embed(title="組員", description="王帷橙、封錦童、高大剛、董囿村", color=0x880af0)
        embed.set_author(name="discord機器人股票爬蟲")
        embed.set_thumbnail(url="https://doqvf81n9htmm.cloudfront.net/data/crop_article/108199/shutterstock_563106079.jpg_1140x855.jpg")
        embed.add_field(name="股票爬蟲", value="封錦童、高大剛", inline=True)
        embed.add_field(name="discord機器人", value="王帷橙、董囿村", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def draw(self,ctx):
        a = 0
        x = pd.period_range(pd.datetime.now(), periods=200, freq='d')
        x = x.to_timestamp().to_pydatetime()
        # 產生三組，每組 200 個隨機常態分布元素
        y = np.random.randn(200, 3).cumsum(0)
        plt.plot(x, y)
        plt.savefig("draw.png")
        draw = discord.File("draw.png")
        await ctx.send(file = draw)
        plt.clf()
        await ctx.send(a)        




def setup(bot):
    bot.add_cog(react(bot))