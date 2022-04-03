import configparser
import json
from time import sleep
from types import NoneType
from unittest import result
import discord
from discord.ext import commands
from discord.ext import tasks
from typing import Union
from datetime import datetime
import calendar

# load config
config = configparser.ConfigParser()
config.read('./config.ini', encoding='utf-8')
TOKEN = str(config['ID']['TOKEN'])
ID_EVERYONE = int(config['ID']['ID_EVERYONE'])
ID_NOTIFY_CHANNEL = int(config['ID']['ID_NOTIFY_CHANNEL'])
ALLOWED_CHANNELS = json.loads(config['ID']['ALLOWED_CHANNELS'])

# define
class Command(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.queue = []
        self.writer = configparser.RawConfigParser()
        
    @commands.command()
    async def notify(self, ctx, *args: Union[discord.TextChannel, discord.Member, str]):
        if ctx.channel.id not in ALLOWED_CHANNELS:
            return
        try:
            str_datetime = args[0]
            str_msg = ' '.join(args[1:])
            year = int(str_datetime[0:2])+2000
            month = int(str_datetime[2:4])
            day = int(str_datetime[4:6])
            hour = int(str_datetime[6:8])
            min = int(str_datetime[8:10])
            n_time = datetime(year, month, day, hour, min)
            self.queue.append([ctx.channel.id, n_time, str_msg.replace('`','')])
        except:
            await ctx.send('invalid value')
    def get_str_info(self, item):
        time: datetime = item[1]
        msg = f'<#{item[0]}> {time.strftime("%y/%m/%d %H:%M")}'
        return msg
    @commands.command()
    async def check(self, ctx, *args: Union[discord.TextChannel, discord.Member, str]):
        if ctx.channel.id not in ALLOWED_CHANNELS:
            return
        str = ""
        for item in self.queue:
            str_item = self.get_str_info(item)
            str += f'{str_item}\r\n'
        if len(str) == 0:
            await ctx.send("no item")
            return
        await ctx.send(str)

def get_nday(year, month, week_n, day_week):
    first, month_days = calendar.monthrange(year, month)
    result = 7 * (week_n - 1) + (day_week - first) % 7 + 1
    if result > month_days:
        return None
    return result
def set_regular_event(week_n, day_week, hour, minute, msg, offset=0):
    now = datetime.now()
    day = get_nday(now.year, now.month, week_n, day_week)
    date = datetime(now.year, now.month, day+offset, hour, minute)
    return [ID_NOTIFY_CHANNEL, date, msg]

@tasks.loop(seconds=86400)  # 86400 sec = 1 day
async def loop_subscribe(command: Command):
    channel = bot.get_channel(ID_NOTIFY_CHANNEL)
    if channel is None:
        return
    now = datetime.now()
    if (now.day == 1) or (now.day < 7 and len(command.queue)==0):   # 毎月1日 or 6日まででキューが空になっているとき
        # 第2日曜20:00 - 3日
        event_pre = set_regular_event(2, calendar.SATURDAY, 20, 00, f'<@&{ID_EVERYONE}>今月の報告会は今週の土曜日です', offset=-3)
        # 第2日曜19:00
        event_day = set_regular_event(2, calendar.SATURDAY, 19, 00, f'<@&{ID_EVERYONE}>20時より報告会を開始します')
        command.queue.append(event_pre)
        command.queue.append(event_day)
        # notify
        msg = "今月の報告会を登録しました\r\n"
        msg += f'{command.get_str_info(event_pre)}\r\n'
        msg += f'{command.get_str_info(event_day)}\r\n'
        await channel.send(msg)

@tasks.loop(seconds=5)
async def loop_notify(command: Command):
    now = datetime.now().strftime('%y%m%d%H%M')
    print(f"{now}: {str(len(command.queue))}")
    if(len(command.queue) == 0):
        return
    for item in command.queue:
        time = item[1].strftime('%y%m%d%H%M')
        if int(now) >= int(time):
            print(item[2])
            channel = bot.get_channel(item[0])
            if channel == None:
                return
            await channel.send(f"@everyone {item[2]}")
            command.queue.remove(item)
            return

# create instance
bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'))  
command = Command(bot=bot)

# start loop
loop_subscribe.start(command)
loop_notify.start(command)

# start bot
bot.add_cog(command)
bot.run(TOKEN)