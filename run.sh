#!/bin/sh
set -e


docker-compose down --remove-orphans
docker-compose compose up -d
