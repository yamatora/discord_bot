# setup
## Require
- [config.iniを同階層に配置](#configini)

## Optional
- [登録条件の追加](#項目追加)

# config.ini
```dummy.ini
[ID]
TOKEN = 0MzYzNjhogehogehogeTE5.YkgiYG0eWFrcjhf_-8
ID_EVERYONE = 8250123456780851
ID_NOTIFY_CHANNEL = 959771234567849104
ALLOWED_CHANNELS = [959771234567849104, 12345678567849104]
```

## TOKEN
下記手順にて取得したTOKEN文字列を設定
1. [Discord DEVELOPER PORTAL](https://discord.com/developers/applications)にてアプリを作成
2. Botを作成し、TOKENを取得

## ID_EVERYONE
下記手順にて取得したロールIDを設定

1. Discord: `ユーザ設定`>`詳細設定`>`開発者モード`を有効化
2. `サーバー設定`>`ロール`>`デフォルトの権限`等にて対象ロールを右クリックしIDを取得

## ID_NOTIFY_CHANNEL
下記手順にて取得したチャンネルIDを設定

1. Discord: `ユーザ設定`>`詳細設定`>`開発者モード`を有効化
2. 対象チャンネルを右クリックしIDを取得

## ALLOWED_CHANNELS
[ID_EVERYONE](#id_everyone)と同様の手順にてIDを取得し、配列として設定

# 項目追加
## 自動登録項目
`bot.py`>`loop_subscribe`関数内にて`set_regular_event`関数を使用して取得した配列を`self.queue`に追加

## ロールおよびチャンネルのリンク
```example
roll:       <@&{ID_ROLL}>
channel:    <#{ID_CHANNEL}}>
```
参考: [DiscordのID直打ちでのリンクの書き方と文字装飾 - Qiita](https://qiita.com/Mijinko/items/df3d2e1f90dbed5a4019)