# コマンド一覧
- [`/notify`](#notify)
- [`/check`](#check)
- [`/clear`](#clear)

---

# /notify
指定日時にメッセージを通知させるコマンド  
コマンドを使用したチャンネルに通知を行う  
```
/notify [yymmddHHMM] [message]
```
## yymmddHHMM
通知日時を設定  

## message
通知するメッセージを設定

## example
ex. 2022年04月08日23時40分「通知メッセージ」
```
/notify 2204082340 通知メッセージ
```

### ロールおよびチャンネルのリンク
```example
roll:       <@&{ID_ROLL}>
channel:    <#{ID_CHANNEL}}>
```
参考: [DiscordのID直打ちでのリンクの書き方と文字装飾 - Qiita](https://qiita.com/Mijinko/items/df3d2e1f90dbed5a4019)

# /check
引数なしで現在キューに入っているリストを表示する  
`yyyy/mm/dd HH:MM:  [message]`  
ex.  
```
2022/05/11 20:00:   message00
2022/05/22 22:33:   message01
```

# /clear
引数なしで現在キューに入っているリストをクリアする