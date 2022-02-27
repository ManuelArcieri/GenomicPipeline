#!/bin/bash
#
# Delete the temporary folder created by prefetch.

set -e

echo "Deleting $HOME/ncbi..."
mkdir --parents "$HOME"/ncbi
rm --force --recursive --dir "$HOME"/ncbi
echo "$HOME/ncbi deleted successfully"
