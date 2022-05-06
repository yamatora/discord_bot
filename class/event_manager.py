import sys
from types import NoneType
sys.path.append("../")
sys.path.append("../common/")
import discord
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext import tasks
from typing import Union

from ini_loader import IniLoader
import define as df

class EventManager:
    def __init__(self, ini_path):
        super().__init__()

        # config
        ini = IniLoader(ini_path)
        self.TOKEN = ini.get(df.SEC_ID, df.KEY_TOKEN)

        # event     (self, ctx, *args)
        self.onNotify = None
        self.onClear = None
        self.onCheck = None
        self.onLoopNotify = None
        self.onLoopSubscribe = None

        # var
        self.bot = commands.Bot(command_prefix=commands.when_mentioned_or('/'))

        # loop
        self.__loop_notify.start()
        self.__loop_subscribe.start()

        # bot
        cmd = CommandList(self)
        self.bot.add_cog(cmd)
    def start(self):
        self.bot.run(self.TOKEN)
    
    def get_channel(self, id) -> TextChannel:
        return self.bot.get_channel(int(id))
    
    # ループ
    @tasks.loop(seconds=5)
    async def __loop_notify(self):
        # 通知処理
        if self.onLoopNotify is None:
            return
        await self.onLoopNotify()
    @tasks.loop(seconds=3600)   # 1h
    async def __loop_subscribe(self):
        # 定期イベント登録処理
        if self.onLoopSubscribe is None:
            return
        await self.onLoopSubscribe()

class CommandList(commands.Cog):
    def __init__(self, manager: EventManager):
        self.manager = manager
        self.bot = manager.bot
    
    # コマンド
    @commands.command() # 通知登録
    async def notify(self, ctx, *args: Union[discord.TextChannel, discord.Member, str]):
        if self.manager.onNotify is None:
            return
        # channel = self.bot.get_channel(df.KEY_ID_CH_NOTIFY)
        await self.manager.onNotify(ctx, args[0], ''.join(args[1:]))
    @commands.command() # 登録内容削除
    async def clear(self, ctx, *args: Union[discord.TextChannel, discord.Member, str]):
        if self.manager.onClear is None:
            return
        await self.manager.onClear(ctx, args)
    @commands.command() # 登録内容確認
    async def check(self, ctx, *args: Union[discord.TextChannel, discord.Member, str]):
        if self.manager.onCheck is None:
            return
        # channel = self.bot.get_channel(df.KEY_ID_CH_NOTIFY)
        await self.manager.onCheck(ctx, args)