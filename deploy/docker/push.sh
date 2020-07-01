#!/bin/bash

shopt -s globstar

for source in challenges/**/challenge.yaml; do
    IMAGE_NAME="${IMAGE_PREFIX}challenge-$(basename $(dirname $source))"

    if [ -n "$IMAGE_TAG" ]; then
        docker push "${IMAGE_NAME}:${IMAGE_TAG}"
    else
        docker push "${IMAGE_NAME}:latest"
    fi
done
