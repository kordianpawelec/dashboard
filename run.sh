#!/bin/sh
git pull

# docker-compose down --remove-orphans

docker-compose build dashboard-app

docker-compose up -d --no-deps --scale dashboard-app=2

sleep 5

docker-compose up -d --scale dashboard-app=2

docker image prune -f