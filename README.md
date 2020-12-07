# Hinata Quiz

## 概要

LINE Bot 日向クイズのコード。

本番環境でほぼ同じ物が動いているので、

↓こちらから友だち登録お待ちしています！↓

<a href="https://lin.ee/9EoVmJf"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="36" border="0"></a>

<img src="https://qr-official.line.me/sid/M/023palzz.png">

## 技術的特徴

- Djangoアプリケーション
- LINE Messaging API
- pipenv

## 使い方

1. このリポジトリをクローン

1. 依存関係のインストール

    ```
    pipenv install
    ```

1. マイグレーションファイル作成

    ```
    python manage.py makemigrations
    ```

1. マイグレーション実行

    ```
    python manage.py migrate
    ```

1. 管理者作成

    ```
    python manage.py createsuperuser
    ```

1. SECRET_KEY生成

    ```
    vi ./hinata_quiz/local_settings.py 
    ```

    以下を記述

    ```
    SECRET_KEY = 'your_secret_key'

    ```
1. LINE Messaging API関係

    1. LINE Developersに登録

    1. LINE Developers Consoleより新規チャネル(Messaging API)を作成

    1. チャネル詳細の「チャネル基本設定」からチャネルシークレットを、「Messaging API設定」からチャネルアクセストークン（長期）をコピー。

    1. Messaging API関係のenvファイルを作成

        ```
        vi ./api/.env
        ```

        以下を記述

        ```
        LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
        LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
        ```

1. アプリケーション実行(ローカル)

    ```
    python manage.py runserver
    ```

1. ngrokをインストール

    [公式サイト](https://dashboard.ngrok.com/get-started/setup)よりインストール

1. 別ターミナルでngrokでフォワーディング

    以下のコマンドを実行

    ```
    ngrok http 8000
    ```

    実行結果

    ```
    ngrok by @inconshreveable                                            (Ctrl+C to quit)
    Session Status                online
    Session Expires               7 hours, 59 minutes
    Version                       2.3.35
    Region                        United States (us)
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    http://XXXXXXXXXXXX.ngrok.io -> http://localhost:8000  
    Forwarding                    https://XXXXXXXXXXXX.ngrok.io -> http://localhost:8000 
           
    ```

    httpsでフォワーディングされたURLをコピー

1. LINE Developers Consoleのチャネル詳細の「Messaging API設定」のWebhook URLに以下のURLを設定する。

    ```
    https://XXXXXXXXXXXX.ngrok.io(コピーしたURL)/api/
    ```

以上で設定は完了。AdminからQuizを作成すれば配信される。

## 最後に

このプロジェクトに何か問題を見つけた方はぜひissueをお待ちしております。