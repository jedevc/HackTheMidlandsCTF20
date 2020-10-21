#!/bin/sh

BASE=$(dirname $(realpath $0))

HT=$(htpasswd -Bbn "$IMAGE_REPO_USERNAME" "$IMAGE_REPO_PASSWORD")

helm install docker-registry stable/docker-registry \
    --namespace docker-registry \
    --version 1.9.4 \
    --set secrets.htpasswd="$HT" \
    --set ingress.enabled

cat $BASE/registry.yaml | envsubst | kubectl apply -f -
kubectl create secret -n default docker-registry docker-registry-creds \
    --docker-server="$IMAGE_REPO" \
    --docker-username="$IMAGE_REPO_USERNAME" \
    --docker-password="$IMAGE_REPO_PASSWORD"

kubectl patch serviceaccount -n default default \
    --patch '{"imagePullSecrets": [{"name": "docker-registry-creds"}]}'
