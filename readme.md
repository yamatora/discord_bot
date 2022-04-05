# setup
- Require
  - [config.iniを同階層に配置](#configini)
  - [デプロイ](#デプロイ)
- Optional
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

# デプロイ
下記記事の`Heroku`へのデプロイ部を参考  
参考: [Pythonで実用Discord Bot(discordpy解説)](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f#bot%E3%82%9224%E6%99%82%E9%96%93365%E6%97%A5%E7%A8%BC%E5%83%8D%E3%81%95%E3%81%9B%E3%82%8B)

## ループ処理が動作しない問題
[30分スリープ問題](https://note.com/hidekiikeda/n/nf9c9db122572)  
[Heroku無料枠の限界に挑む](https://qiita.com/Oyuki123/items/855aa97e5ce27e44079f)  
下記にて解決  

- アカウント認証(クレジットカード登録)
- `Heroku Scheduler`アドオン追加
- 10分間隔にて`curl https://[app_name].herokuapp.com/`等サーバに対してアクセスを行うコマンドを実行

# 項目追加
## 自動登録項目
`bot.py`>`loop_subscribe`関数内にて`set_regular_event`関数を使用して取得した配列を`self.queue`に追加