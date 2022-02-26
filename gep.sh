#!/bin/bash
set -e

gep_folder="$HOME"/GenomicPipeline

source "$gep_folder"/env/bin/activate
python3 "$gep_folder"/genomicpipeline/main.py "$@"
deactivate
