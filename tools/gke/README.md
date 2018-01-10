Google Kubernetes Engine tools
===
このフォルダは，Google Cloud Platform (GCP) の Kubernetes (K8s) Engine にデプロイするためのツールをまとめています．


# 準備
## Setup
1. [GCP](https://cloud.google.com/) の無料トライアルに登録する．
1. GCP SDK をインストールする．
    * [クイックスタート  |  Cloud SDK  |  Google Cloud Platform](https://goo.gl/iprpCv)
    * これで gcloud コマンドが使えるようになるはず (うまく行かなかったら bin にパスを通す)．
1. GCP 上でプロジェクトを作成しておく．
1. setup スクリプトを走らせる `./setup.sh`．やっているのは以下のこと．
    * GCP で作成したプロジェクトとローカルの gcloud コマンドを紐付ける (上記で作成したプロジェクトを指定する)．
    * K8s の操作に使う kubectl をインストールする．
    * `ewb` という K8s クラスタを作っておく．

## Kubernetes Secrets のアップロード

```sh
./upload_secret.sh

# 指示に従って Twitter API のキーなどを入れる
```

アップロードした Secret を環境変数として参照するためには[こちら](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-environment-variables)を参照のこと．具体的には以下をマニフェストに記述する (TODO: これも script で行いたい)．

```
env:
  - name: CONSUMER_KEY
    valueFrom:
      secretKeyRef:
        name: ewb-secret
        key: CONSUMER_KEY
  - name: CONSUMER_SECRET
    valueFrom:
      secretKeyRef:
        name: ewb-secret
        key: CONSUMER_SECRET
  - name: ACCESS_KEY
    valueFrom:
      secretKeyRef:
        name: ewb-secret
        key: ACCESS_KEY
  - name: ACCESS_SECRET
    valueFrom:
      secretKeyRef:
        name: ewb-secret
        key: ACCESS_SECRET
  - name: BITLY_ACCESS_TOKEN
    valueFrom:
      secretKeyRef:
        name: ewb-secret
        key: BITLY_ACCESS_TOKEN
```

# デプロイ

```sh
./deploy.sh docker_image_tag # tag は docker 用
```


# クリーンアップ

```sh
./cleanup.sh
```

# Debug

以下を走らせると， [http://localhost:8001/ui](http://localhost:8001/ui) が参照可能になる．
```sh
GCP_PROJECT=$(gcloud config get-value project)                                                  # 初回のみ
gcloud container clusters get-credentials ewb --zone asia-northeast1-b --project $GCP_PROJECT   #
kubectl proxy
```
