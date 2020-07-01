#!/bin/bash

BASE=$(dirname $0)

$BASE/docker-compose.py > $BASE/docker-compose.yaml
