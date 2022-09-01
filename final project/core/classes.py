import  discord
from discord.ext import commands
import pandas as pd
import requests
import random
import time
import json

with open('setting.json','r', encoding='utf8' ) as jfile:
    jdata = json.load(jfile)

class Cog_extension(commands.Cog):
    def __init__(self,bot) :
        self.bot = bot 