#!/bin/sh
set -eu

# initialize gcloud for your local machine
gcloud init

# install kubectl
gcloud components update
gcloud components install kubectl

# make a k8s cluster as ewb
gcloud container clusters create --num-nodes=1 ewb --zone asia-northeast1-a \
