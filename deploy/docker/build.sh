#!/bin/bash

shopt -s globstar

ROOT=$PWD

for source in challenges/**/challenge.yaml; do
    cd $(dirname $source)

    if [ -z "$IMAGE_TAG" ]; then
        IMAGE_TAG="latest"
    fi
    IMAGE_NAME="${IMAGE_PREFIX}challenge-$(basename $(dirname $source))"

    if [ -n "$IMAGE_PREFIX" ]; then
        docker pull "$IMAGE_NAME:$IMAGE_TAG" || true
    fi
    docker build --cache-from "$IMAGE_NAME:$IMAGE_TAG" -t "$IMAGE_NAME" .

    cd $ROOT
done
