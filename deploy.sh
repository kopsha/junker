#!/usr/bin/env bash
set -e

PROJECT_ROOT=$(git rev-parse --show-toplevel)
PROJECT_NAME=$(basename $PROJECT_ROOT)


printf " --\n"
printf " -- deploying $PROJECT_NAME (from $PROJECT_ROOT)\n"
printf " --\n"

find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

printf "copying files"
scp ./* fibonet:~/$PROJECT_NAME/

## service recomposition
printf " --\n"
printf " -- rebuilding services\n"
printf " --\n"

ssh fibonet /bin/bash <<'EOT'
set -e
cd ~/junker
./go
EOT

printf " -- done\n"
