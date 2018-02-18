#!/bin/bash
set -eu

SECRET=ewb-secret
TEMPLATE=templates/secret.yaml
require_params=1
if [ $# -lt $require_params ]; then
    echo "This script needs at least $require_params argument(s)"
    echo "Usage: $0 deployment_name"
    echo "e.g. $0 ewb-deploy"
    exit 1
fi
deployment_name="$1"

# make a secret
echo "Please input the following credentials"
echo -n "CONSUMER_KEY: "
read CONSUMER_KEY
echo -n "CONSUMER_SECRET: "
read CONSUMER_SECRET
echo -n "ACCESS_KEY: "
read ACCESS_KEY
echo -n "ACCESS_SECRET: "
read ACCESS_SECRET
echo -n "BITLY_ACCESS_TOKEN: "
read BITLY_ACCESS_TOKEN

cat $TEMPLATE > temp.yaml
echo "  CONSUMER_KEY: $(echo -n "$CONSUMER_KEY" | base64)" >> temp.yaml
echo "  CONSUMER_SECRET: $(echo -n "$CONSUMER_SECRET" | base64)" >> temp.yaml
echo "  ACCESS_KEY: $(echo -n "$ACCESS_KEY" | base64)" >> temp.yaml
echo "  ACCESS_SECRET: $(echo -n "$ACCESS_SECRET" | base64)" >> temp.yaml
echo "  BITLY_ACCESS_TOKEN: $(echo -n "$BITLY_ACCESS_TOKEN" | base64)" >> temp.yaml

echo "Created temp.yaml"


# push the secret
num=$(kubectl describe secrets/$SECRET | wc -l)
if [ $num -gt 1 ]; then
    echo "Deleting the previous $SECRET..."
    kubectl delete -f ./temp.yaml
fi

echo "Uploading secrets..."
kubectl create -f ./temp.yaml

# set up environment variables by modifying the manifest of ewb-deploy deployment
kubectl patch deployment $deployment_name --patch "$(cat ./templates/setup_env.yaml)"
