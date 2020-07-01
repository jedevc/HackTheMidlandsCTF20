#!/usr/bin/env python3

import os
import site
import sys
import yaml

site.addsitedir(".")
import ctftool


def main():
    services = {}
    for challenge in ctftool.Challenge.load_all():
        service = generate_service(challenge)
        if service:
            services = {**service, **services}

    compose = {
        "version": "3",
        "services": services,
    }
    yaml.dump(compose, sys.stdout)


def generate_service(challenge):
    if not challenge.deploy.docker:
        return None

    ports = []
    if (internalPort := challenge.deploy.internalPort) :
        if (externalPort := challenge.deploy.externalPort) :
            ports.append(f"{externalPort}:{internalPort}")
        else:
            ports.append(f"{internalPort}")

    return {
        f"challenge-{challenge.name}": {
            "image": f"challenge-{challenge.name}",
            "build": os.path.dirname(challenge.path),
            "restart": "always",
            "ports": ports,
        }
    }


if __name__ == "__main__":
    main()
