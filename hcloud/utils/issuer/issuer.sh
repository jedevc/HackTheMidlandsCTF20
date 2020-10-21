#!/bin/sh

BASE=$(dirname $(realpath $0))
cat $BASE/issuer.yaml | envsubst | kubectl apply -f -
