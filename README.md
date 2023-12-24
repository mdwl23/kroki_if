# kroki_if

krokiサーバへテキストデータを送信して、画像データを取得するためのインターフェースツール

# Quick Start
```bash
cd docker
docker build --tag kroki_if_web .
sudo docker-compose up -d
```


# アーキテクチャ
- コア機能
    - テキストデータをバイナリ変換してサーバへ送信する機能
    - サーバから画像データを受信する機能
- 関連機能
    - 受信した画像データを表示する機能
    - テキストデータを入力する機能

# webアプリ版の使い方
## 環境の構成
- webサーバとしてgunicornを使用
- フレームワークはflask
## サーバを起動する
事前にコンテンツのデプロイ先となるディレクトリを用意しておく。docker/ へ移動して、docker buildすることでdocker imageを作成。
>docker build --tag kroki_if_web .

docker runにてポートとボリュームの設定を実施する

>docker run -d -p 8080:8000 -v /mnt/e/dev/web/:/app -t kroki_if_web

以下注意。
- 用意しておいたディレクトリをボリュームとしてマウントすること
- 用意しておいたディレクトリにあらかじめコンテンツを入れてないとエラーになるので注意
    - 今回の場合はflaskのsrc/app.py

[参考サイト](https://zenn.dev/4kzknt/articles/1baf245b3caca8)

## コンテンツを更新する
- ボリューム設定でマウントしてあるホスト側のディレクトリにコンテンツのファイルをデプロイ
- dockerコンテナを再起動する

## コンテンツの動作確認をする
動作確認だけならサーバへデプロイしなくてもflaskを直接起動して実行できる。
app.pyと同じディレクトリで下記コマンドを実行する。

>flask run --host=0.0.0.0

上記コマンドを実行後、 http://localhost:5000/ で動作確認用の簡易webサーバへアクセス可能。

## docker上のkrokiサーバと通信する
krokiサーバも同一マシン上のdockerコンテナで動いてる場合は、docker-compose.ymlを使ってコンテナ同士で通信できるようにする。
docker/ へ移動し以下コマンドを実行。
> sudo docker-compose up -d

[kroki](https://kroki.io/)
