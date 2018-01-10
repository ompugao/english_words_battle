#!/bin/sh
set -eu

# delete all
kubectl delete deployment,service,pod --all
gcloud container clusters delete ewb
