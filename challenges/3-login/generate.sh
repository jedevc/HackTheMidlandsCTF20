#!/bin/bash

###
# Generate a git repo that you can push to GitHub for the challenge.
#

set -e

BASE=${PWD}

TEMP=`mktemp -d`
cd $TEMP
git init
git config --local user.name "Strong Security Inc."
git config --local user.email "strongsecurity@example.com"

cp -r $BASE/{app.py,templates,password.txt} .
git add .
git commit -m "Initial commit"

git rm password.txt
git commit -m "Woops!"

cp $BASE/README.md .
git add .
git commit -m "Create a README.md"

echo "Git repo is at $TEMP"
