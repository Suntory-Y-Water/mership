# 前準備

Microsoft Edgeでアプリにログインしてください。

# 使用方法

アプリケーションを起動する前に**CheckUserdirPath.bat**を実行します。
実行後 **./app/gui.exe** を起動します。

# 業務解説

## 商品情報取得

やることリストから発送する必要がある商品のみを取得して、購入者情報をCSVに書き出します。
実行中はコマンドプロンプトから、どの商品を取得しているか確認できます。

実行する前に必ずMicrosoft Edgeのタスクを全て落としてから実行してください。
**CloseEdgs.bat**を実行することで、バックグラウンドで動いているものも落とせます。

## 発送通知

発送が終わったあと、自動で発送通知を押してくれます。
このとき、CSVファイルにある全ての商品を発送するため、**発送しない商品はCSVファイルから削除する必要があります。**

通常の発送方法とは異なるもの(例:匿名配送)はCSVファイルがあっても、スルーする設定なので問題ないです。
# tree

```cmd
│   .gitignore
│   CheckUserdirPath.bat
│   CloseEdgs.bat
│   README.md
│   宛名作成.lbx
│
├───driver
│       msedgedriver.exe
│
└───source
        gui.py
        logmaster.py
        move_file.py
        scraper.py
```