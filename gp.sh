#!/bin/sh

source genomicpipeline/env/bin/activate
python3 ./genomicpipeline/main.py "$@"
deactivate
