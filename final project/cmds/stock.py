from re import search
import  discord
import pandas as pd
import requests
import random
import time
from discord.ext import commands
import json
import random
import os
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np
import talib
from core.classes import Cog_extension

with open('setting.json','r', encoding='utf8' ) as jfile:
    jdata = json.load(jfile)

class stock(Cog_extension):

    @commands.command()
    async def startstock(self,ctx):
        res = requests.get('https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y')
        stock_list = pd.read_html(res.text)[0]

        name = set()
        length = len(stock_list)
        number = set()

        for i in range(1,length):
            number.add(stock_list[2][i])
        for j in range(1,length):
            name.add(stock_list[3][j])

            
        def get_stock_data(date,stock_no):
            url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % (date,stock_no)
            r = requests.get(url)
            data = r.json()
            if data['stat'] == "OK" :
                df = pd.DataFrame(data['data'], columns = data['fields'])
                return df
            else :
                return 'ERROR'


        d = ''

        d+=str(time.localtime()[0])
        if time.localtime()[1] < 10 :
            d+='0'
            d+=str(time.localtime()[1])
        else:
            d+=str(time.localtime()[1])

        d = int(d)

        await ctx.send('你想要哪一年到今年的資料')
        a = 0
        b = 0
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel 
        msg = await self.bot.wait_for("message", check=check)

        a = int(msg.content)

        await ctx.send('你想要哪一個月到今天的資料')
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel 
        msg = await self.bot.wait_for("message", check=check)

        b = int(msg.content)

        await ctx.send(f'將分析從{a}年{b}月到今天的資料')
        
        bb = b - 3
        if len(str(b)) == 1:
            b0 = '0' + str(b)
        else :
            b0 = str(b)
        if bb < 1 :
            aa = str(a - 1)
            bb = str(b + 12)
        else : 
            aa = str(a)
            bb = '0' + str(bb)
        day = int(aa+bb)

        if d < day :
            await ctx.send('請輸入正確的日期')
            raise Exception('請輸入正確的日期')
        
        await ctx.send('你想用1.有價證券代號查還是用2.有價證券名稱，輸入 1 or 2 ')
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel 
        msg = await self.bot.wait_for("message", check=check)

        search = msg.content

        if search == '1':
            await ctx.send('請輸入有價證券代號')
        
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel 
            msg = await self.bot.wait_for("message", check=check)

            search_number = msg.content
            if search_number in number:
                result = pd.DataFrame()
                while  day <= d:
                    date = str(day)+ '01'
                    result = pd.concat([result,get_stock_data(date,search_number)],axis=0)

                    time.sleep(3)
                    if day % 100 != 12:
                        day = day +1
                    else:
                        day = day +100 - 11

            else :
                await ctx.send('找不到此有價證券代號')
                raise Exception('找不到此有價證券代號')
        elif search == '2':
            await ctx.send('請輸入有價證券名稱')
        
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel 
            msg = await self.bot.wait_for("message", check=check)

            a = msg.content
            search_number = '0'
            for i in range(1,length):
                if a == stock_list.iloc[i][3]:
                    search_number = stock_list.iloc[i][2]
                    break
                else:
                    continue
                
            if search_number == '0' :
                await ctx.send('找不到此有價證券名稱')
                raise Exception('找不到此有價證券名稱')
            else :

                if search_number in number:
                    result = pd.DataFrame()
                    while  day <= d:
                        date = str(day)+ '01'
                        result = pd.concat([result,get_stock_data(date,search_number)],axis=0)
                        time.sleep(3)
                        if day % 100 != 12:
                            day = day +1
                        else:
                            day = day +100 - 11      
                
        else:
            await ctx.send("請輸入1或2")
            raise Exception("輸入1或2")

        result = result.reset_index(drop=True)

        startday = str(a-1911) + '/' + str(b0)
        sd = result.index[result['日期'].str.contains(startday)].tolist()[0]

        Open = np.array(result['開盤價'], dtype=float)
        Close = np.array(result['收盤價'], dtype=float)
        High = np.array(result['最高價'], dtype=float)
        Low = np.array(result['最低價'], dtype=float)
        VolumeStr = np.array(result['成交股數'],dtype=str)

        #把成交股數轉成int格式
        def transfer(a):
            c = ''
            for i in range(len(a)) :
                if a[i].isdigit():
                    c+=a[i]
            for j in range(len(c)):
                ans = c[:len(c)-3]
            return ans
        Volume = np.array([], dtype=int)
        for i in VolumeStr:
            j = int(transfer(i))
            Volume = np.append(Volume,j)

        #K線
        fig = plt.figure(figsize=(24, 20))
        ax = fig.add_axes([0.04,0.46,0.92,0.5])
        ax.set_xticks(range(0,len(result.index)-sd, 10))
        ax.set_xticklabels(result['日期'][sd:][::10])
        mpf.candlestick2_ochl(ax,Open[sd:],Close[sd:],High[sd:],Low[sd:],width=0.6,colorup='r',colordown='g')

        #均線
        def ma(x):
            sma = talib.SMA(Close,x)
            ax.plot(sma[sd:], label=str(x)+'MA')
            
        #成交量
        def volume(Num):
            ax2 = fig.add_axes([0.04,0.44-0.1*Num,0.92,0.1])
            mpf.volume_overlay(ax2,Open[sd:],Close[sd:],Volume[sd:],colorup='r',colordown='g',width=0.6)
            ax2.set_xticks(range(0,len(result.index)-sd, 10))
            ax2.set_xticklabels(result['日期'][sd:][::10])
            
        #布林通道
        def bband(x,y):
            bbands = talib.BBANDS(Close,x,y,y)
            upper = bbands[0][sd:]
            middle = bbands[1][sd:]
            lower = bbands[2][sd:]
            ax.plot(upper,label='UB'+str(y),color='green')
            ax.plot(middle,label='BBandMA'+str(x))
            ax.plot(lower,label='LB'+str(y),color='green')

        #KD值
        def kd(Num):
            ax3 = fig.add_axes([0.04,0.44-0.1*Num,0.92,0.1])
            k = talib.STOCH(High,Low,Close)[0][sd:]
            d = talib.STOCH(High,Low,Close)[1][sd:]
            ax3.plot(k,label='K')
            ax3.plot(d,label='D')
            ax3.set_xticks(range(0,len(result.index)-sd, 10))
            ax3.set_xticklabels(result['日期'][sd:][::10])
            ax3.legend()
            
        #RSI指標
        def rsi(x,Num):
            ax4 = fig.add_axes([0.04,0.44-0.1*Num,0.92,0.1])
            RSIIndex = talib.RSI(Close,x)[sd:]
            ax4.plot(RSIIndex,label='RSI='+str(x)+'T')
            ax4.set_xticks(range(0,len(result.index)-sd, 10))
            ax4.set_xticklabels(result['日期'][sd:][::10])
            ax4.legend()
            
        await ctx.send('是否變更指標及參數(y/n)')
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel 
        msg = await self.bot.wait_for("message", check=check)
            
        analysis = msg.content
        #使用預設指標及參數
        if analysis == 'n':
            ma(5)
            ma(10)
            ma(20)
            volume(1)
            
        #自訂指標及參數
        elif analysis == 'y':
            await ctx.send('輸入要使用的指標 1:均線 2:成交量 3:布林通道 4:KD指標 5:RSI指標')
        
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel 
            msg = await self.bot.wait_for("message", check=check)
            
            indicator = str(msg.content)
            NumSubP = 1
            for i in indicator:
                if i == '1':
                    await ctx.send('輸入均線時間 例:5,10,20')

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel 
                    msg = await self.bot.wait_for("message", check=check)
                    
                    xMA = msg.content
                    xMAlist = xMA.split(",")
                    for j in xMAlist:
                        ma(int(j))
                if i == '2':
                    volume(NumSubP)
                    NumSubP += 1
                if i == '3':
                    await ctx.send('輸入布林平均線 例:20')
                
                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel 
                    msg = await self.bot.wait_for("message", check=check)
                    
                    average = int(msg.content)

                    await ctx.send('輸入標準差倍數 例:1.6')
                
                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel 
                    msg = await self.bot.wait_for("message", check=check)
                    
                    xSD = float(msg.content)
                    bband(average,xSD)
                if i == '4':
                    kd(NumSubP)
                    NumSubP += 1
                if i == '5':
                    await ctx.send('輸入RSI週期 例:10')
                
                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel 
                    msg = await self.bot.wait_for("message", check=check)
                    
                    rsiT = int(msg.content)
                    rsi(rsiT,NumSubP)
                    NumSubP += 1
        else:
            await ctx.send('請輸入y或n')
            raise Exception('輸入y或n')
            
        ax.set_title("TW-"+search_number,fontsize=30)
        ax.legend()
        plt.savefig("draw.png",bbox_inches='tight')
        draw = discord.File("draw.png")
        await ctx.send(file = draw)
        plt.clf()

                


    

def setup(bot):
    bot.add_cog(stock(bot))

