#!/usr/bin/env bash
set -e

find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

PROJECT_NAME=junker

user_id=$(id -u)
group_id=$(id -g)

docker build --build-arg UID=$user_id --build-arg GID=$group_id -t ${PROJECT_NAME} .

cmd=$*
docker run -ti --rm -v $(pwd):/app/src ${PROJECT_NAME} ${cmd}
