#!/usr/bin/env bash

SRC="$(dirname "$0")/src"

chroma run &
PYTHONPATH="$PYTHONPATH:$SRC" python3 -m t4search "$@"
