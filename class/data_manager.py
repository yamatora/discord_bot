from datetime import datetime
import queue
import sys
import redis
import time
sys.path.append("../common")
from ini_loader import IniLoader
import define as df

# 区切り文字列
SP_QUEUE = '{\r\n}'
SP_ITEM = ','

# DataManager
#   Redisと同期するデータ管理クラス
class DataManager:
    def __init__(self, ini_path):
        # redis読込
        ini = IniLoader(ini_path)
        redis_url = ini.get(df.SEC_REDIS, df.KEY_REDIS_URL)
        self.__redis = redis.from_url(url=redis_url, decode_responses=True)

        time.sleep(1)

        self.__queue = []
        if not self.__redis.exists(df.RKEY_QUEUE):
            return  # DBデータ空
        vals = self.__redis.get(df.RKEY_QUEUE).split(SP_QUEUE)
        for val in vals:
            if len(val) > 8:
                self.__queue.append(val)

    def get(self) -> list:
        list_queue = []
        for item in self.__queue:
            vals = item.split(SP_ITEM)
            list_queue.append(vals)
        return list_queue
    def append(self, item: list):  # 要素追加  item: [time, message]
        str_item = SP_ITEM.join(item)  # str_item: "time,message"
        self.__queue.append(str_item)
        self.sync()
    # def remove(self, index: int):   # index指定にて要素削除
    #     if index >= len(self.__queue):
    #         return
    #     del self.__queue[index]
    #     self.sync()
    def remove(self, item: list):
        str_item = SP_ITEM.join(item)
        if not str_item in self.__queue:
            return
        self.__queue.remove(str_item)
        self.sync()
    def clear(self):
        self.__queue.clear()
        self.sync()
    def sync(self):   # 同期
        str_queue = SP_QUEUE.join(self.__queue)   # 改行区切り
        self.__redis.set(df.RKEY_QUEUE, str_queue)
    def set_update_date(self):
        now = datetime.now().strftime('%y%m%d%H%M')
        self.__redis.set(df.RKEY_LAST_UPDATE, now)
    def get_update_date(self):
        if not self.__redis.exists(df.RKEY_LAST_UPDATE):
            return None
        return self.__redis.get(df.RKEY_LAST_UPDATE)
    def reset_update_date(self):
        self.__redis.set(df.RKEY_LAST_UPDATE, datetime.fromtimestamp(0).strftime('%y%m%d%H%M'))
        print("reset")
        exit(0) # アプリ終了