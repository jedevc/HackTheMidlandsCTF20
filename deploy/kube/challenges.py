#!/usr/bin/env python3

import os
import site
import sys
import yaml

site.addsitedir(".")
import ctftool


def main():
    for challenge in ctftool.Challenge.load_all():
        service = generate_service(challenge)
        if service:
            yaml.dump(service, sys.stdout)
            print("---")

        deploy = generate_deployment(challenge)
        if deploy:
            yaml.dump(deploy, sys.stdout)
            print("---")


def generate_deployment(challenge):
    if not challenge.deploy.docker:
        return None

    ports = []
    if (port := challenge.deploy.internalPort) :
        ports.append({"containerPort": port})

    IMAGE_PREFIX = os.environ.get("IMAGE_PREFIX", "")
    IMAGE_TAG = os.environ.get("IMAGE_TAG", "latest")

    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"challenge-{challenge.name}-deployment",
            "labels": {"app": "challenge", "challenge": challenge.name},
        },
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"challenge": challenge.name}},
            "template": {
                "metadata": {
                    "name": f"challenge-{challenge.name}",
                    "labels": {"app": "challenge", "challenge": challenge.name},
                },
                "spec": {
                    "automountServiceAccountToken": False,
                    "containers": [
                        {
                            "name": f"challenge-{challenge.name}",
                            "image": f"{IMAGE_PREFIX}challenge-{challenge.name}:{IMAGE_TAG}",
                            "imagePullPolicy": "Always",
                            "ports": ports,
                        },
                    ],
                },
            },
        },
    }


def generate_service(challenge):
    if not challenge.deploy.docker:
        return None

    ports = []
    if (internal := challenge.deploy.internalPort) :
        port = {"port": internal, "targetPort": internal, "protocol": "TCP"}
        if (external := challenge.deploy.externalPort) :
            port["nodePort"] = external
        ports.append(port)

    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"challenge-{challenge.name}-service",
            "labels": {"challenge": challenge.name},
        },
        "spec": {
            "type": "NodePort",
            "selector": {"challenge": challenge.name},
            "ports": ports,
        },
    }


if __name__ == "__main__":
    main()
