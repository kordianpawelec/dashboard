#!/bin/sh
set -e

git pull

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt


nohup python3 -m scripts.scheduler > scheduler.log 2>&1 & echo $!

nohup python3 app.py > app.log 2>&1 & echo $!