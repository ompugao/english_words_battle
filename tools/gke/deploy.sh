#!/bin/sh
set -eu

APP_NAME=english_words_battle
CONTAINER_REGISTRY=asia.gcr.io

require_params=2
if [ $# -lt $require_params ]; then
    echo "This script needs at least $require_params argument(s)"
    echo "Usage: $0 docker_image_tag deployment_name"
    echo "e.g. $0 1.0 ewb-deploy"
    exit 1
fi
tag="$1"
deployment_name="$2"

# check gcloud installation
type gcloud 1>/dev/null 2>&1
ret=$?
if [ $ret == 0 ]; then
    GCLOUD=$(which gcloud)
else
    # for circleci version 1.0
    type /opt/google-cloud-sdk/bin/gcloud 1>/dev/null 2>&1
    ret=$?
    if [ $ret == 0 ]; then
        GCLOUD=/opt/google-cloud-sdk/bin/gcloud
    else
        echo "gcloud is not installed!"
        exit 1
    fi
fi

# get project name
GCP_PROJECT=$($GCLOUD config get-value project)
echo "This project is $GCP_PROJECT"

image=$CONTAINER_REGISTRY/$GCP_PROJECT/$APP_NAME:$tag


# move to the root folder
cd $(git rev-parse --show-toplevel)

# build and push a container to Container Repository (visit https://console.cloud.google.com/gcr/images)
echo "Building and pushing a container to Container Repository..."
docker build -t $image .
$GCLOUD docker -- push $image
echo "Pushed a container to Container Repository. See https://console.cloud.google.com/gcr/images"

# deploy
num=$(kubectl get pod | grep $deployment_name | wc -l)
if [ $num -lt 1 ]; then
    echo "Start Running the container..."
    kubectl run $deployment_name --image=$image --command -- python /ewb/src/main.py
else
    echo "$deployment_name already exists. Updating the image with the new tag ($tag)..."
    kubectl set image deployment/$deployment_name $deployment_name=$image
fi

# check if the deploy worked
echo ""
echo "Please make sure you can see 'Running' for $deployment_name by running 'kubectl get pod'"
