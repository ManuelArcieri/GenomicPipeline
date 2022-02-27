#!/bin/bash

gep_folder="$HOME"/GenomicPipeline

set -e
source "$gep_folder"/env/bin/activate
set +e
python3 "$gep_folder"/genomicpipeline/main.py "$@"
deactivate
