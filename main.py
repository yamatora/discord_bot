# import
import sys
import os
from datetime import datetime
import discord
from discord.ext import commands
import calendar
# sys.path.append("../bot")
sys.path.append('./class')
sys.path.append('./common')
import define as df
from data_manager import DataManager
from event_manager import EventManager
from ini_loader import IniLoader
import json
from typing import Union

class main:
    def __init__(self, ini_path) -> None:
        self.data = DataManager(ini_path)
        self.event = EventManager(ini_path)
        ini = IniLoader(ini_path)
        self.NotifyChannel = ini.get(df.SEC_ID, df.KEY_ID_CH_NOTIFY)
        self.AllowedChannels = ini.getArray(df.SEC_ID, df.KEY_ID_CH_ALLOWED)
        self.IdEveryone = ini.get(df.SEC_ID, df.KEY_ID_EVERYONE)
        
    def run(self):
        self.event.onLoopNotify = self.onLoopNotify
        self.event.onLoopSubscribe = self.onLoopSubscribe
        self.event.onNotify = self.onNotify
        self.event.onClear = self.onClear
        self.event.onCheck = self.onCheck
        print("run")
        self.event.start()
    
    # event
    async def onLoopNotify(self):     # 通知
        queue = self.data.get()
        # print(len(queue))
        now = datetime.now().strftime('%y%m%d%H%M')
        for item in queue:
            if len(item) < 2:
                continue
            time = item[1]
            if int(time) > int(now):
                continue
            channel = self.event.get_channel(item[0])
            if channel == None:
                continue    # 起動直後
            await channel.send(f"@everyone {item[2]}")
            self.data.remove(item=item)
            return
    async def onLoopSubscribe(self):  # 定期イベント登録
        channel = self.event.get_channel(self.NotifyChannel)
        if channel is None:
            return
        now = datetime.now()
        last = datetime.fromtimestamp(0)
        str_last = self.data.get_update_date()
        if str_last is not None:
            last = self.get_datetime(str_last)
        if now.year==last.year and now.month==last.month:
            return  # 登録済
        # イベント登録
        event_pre = self.event_date(2, calendar.SATURDAY, 20, 00,
                f'今月の報告会は今週の土曜日です',
                offset=-3
            )
        event_day = self.event_date(2, calendar.SATURDAY, 19, 00,
                f'20時より報告会を開始します'
            )
        self.data.append(event_pre)
        self.data.append(event_day)
        # 登録内容通知
        event_date = self.get_datetime(event_day[1])
        await channel.send(f'今月の報告会: {event_date.strftime("%Y/%m/%d %H:%M~")}')
        # 最終更新日
        self.data.set_update_date()
        
    async def onNotify(self, ctx: commands.Context, *args: Union[discord.TextChannel, discord.Member, str]):  # 通知登録
        if ctx.channel.id not in self.AllowedChannels:
            return
        try:
            datetime = self.get_datetime(args[0])
            self.data.append([
                str(ctx.channel.id),
                self.get_datestr(datetime),
                args[1]
            ])
        except:
            await ctx.send('invalid value')
    async def onClear(self, ctx: commands.Context, *args):  # 登録内容削除
        if ctx.channel.id not in self.AllowedChannels:
            return
        self.data.clear()
    async def onCheck(self, ctx: commands.Context, *args):  # 登録内容確認
        if ctx.channel.id not in self.AllowedChannels:
            return
        result = ""
        for item in self.data.get():
            if len(item) < 3:
                continue
            date = self.get_datetime(item[1])
            i_msg = item[2]
            result += f'{date.strftime("%Y/%m/%d %H:%M")}:\t{i_msg}\r\n'
        if len(result) == 0:
            await ctx.send("no item")
            return
        await ctx.send(result)

    # 日程
    def get_datestr(self, date: datetime) -> str:
        return date.strftime('%y%m%d%H%M')
    def get_datetime(self, str_date: str) -> datetime:
        year = int(str_date[0:2])+2000
        month = int(str_date[2:4])
        day = int(str_date[4:6])
        hour = int(str_date[6:8])
        min = int(str_date[8:10])
        return datetime(year, month, day, hour, min)
    def get_nday(self, year, month, week_n, day_week):    # n週w曜の日付を取得 w:0~6
        first, month_days = calendar.monthrange(year, month)
        result = 7 * (week_n - 1) + (day_week - first) % 7 + 1
        if result > month_days:
            return None
        return result
    def event_date(self, week_n, day_week, hour, minute, msg: str, offset=0):
        now = datetime.now()
        day = self.get_nday(now.year, now.month, week_n, day_week)
        date = datetime(now.year, now.month, day+offset, hour, minute)
        return [self.NotifyChannel, self.get_datestr(date), msg]

if __name__ == '__main__':
    app = main(os.path.abspath('./config.ini'))
    app.run()