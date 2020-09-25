#!/bin/bash

set -e

docker build -t shipit .
docker save shipit > shipit.tar
