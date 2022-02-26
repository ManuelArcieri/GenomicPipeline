#!/bin/bash
set -e

GEP_HOME=$(realpath "$0")

source "$GEP_HOME"/env/bin/activate
python3 "$GEP_HOME"/genomicpipeline/main.py "$@"
deactivate
