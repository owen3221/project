from calendar import c
from ctypes import c_void_p
from tkinter.filedialog import askdirectory
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

class event(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(">> 程式已啟動 <<")

    @commands.Cog.listener()
    async def  on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata["welcom_cha"]))
        await channel.send(f"{member} 加入了")
        print(f'{member} 加入了!')

    @commands.Cog.listener()
    async def  on_member_leave(self,member):
        channel = self.bot.get_channel(int(jdata["welcom_cha"]))
        await channel.send(f"{member} 離開了")
        print(f'{member} 離開了!')

    @commands.Cog.listener()
    async def on_message(self, msg):

        if msg.content == 'hi' and msg.author != self.bot.user:
            await msg.channel.send('hi')




def setup(bot):
    bot.add_cog(event(bot))