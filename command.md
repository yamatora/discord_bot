- [`/notify`](#notify)
- [`/check`](#check)

# /notify
指定日時にメッセージを通知させるコマンド  
コマンドを使用したチャンネルに通知を行う  
```
/notify [yymmddHHMM] [message]
```
## yymmddHHMM
通知日時を設定  
ex. 2022年04月08日23時40分
```
/notify 2204082340 [message]
```

## message
通知するメッセージを設定  
ex. ID_EVERYONE: `@everyone`ロールのID  
```
/notify 2204091000 <@&{ID_EVERYONE}>ミーティングを開始します
```

### ロールおよびチャンネルのリンク
```example
roll:       <@&{ID_ROLL}>
channel:    <#{ID_CHANNEL}}>
```
参考: [DiscordのID直打ちでのリンクの書き方と文字装飾 - Qiita](https://qiita.com/Mijinko/items/df3d2e1f90dbed5a4019)

# /check
引数なしで現在キューに入っているリストを表示する  
`[通知先チャンネル] [yy/mm/dd HH:MM]`  
ex.  
```
#discord_bot 22/04/06 20:00
#discord_bot 22/04/09 19:00
```