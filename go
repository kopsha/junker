#!/usr/bin/env bash
set -e

find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

PROJECT_ROOT=$(git rev-parse --show-toplevel)
PROJECT_NAME=$(basename $PROJECT_ROOT)

user_id=$(id -u)
group_id=$(id -g)

docker build --build-arg UID=$user_id --build-arg GID=$group_id -t ${PROJECT_NAME} .

cmd=$*
docker run -ti -v $(pwd)/src:/app/src ${PROJECT_NAME} ${cmd}
