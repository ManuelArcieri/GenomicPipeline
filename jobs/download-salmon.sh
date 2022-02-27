#!/bin/bash
#
# Download and install Salmon.
#
# INPUT:
# - $OUT_DIR: output directory (e.g. "/some/dir")

set -e

echo "Downloading Salmon 1.7.0..."
mkdir --parents "$OUT_DIR"
rm --force --recursive --dir "$OUT_DIR"
mkdir --parents "$OUT_DIR"
wget --no-verbose --tries 5 --timeout 10 --output-document "$OUT_DIR"/salmon.tar.gz https://github.com/COMBINE-lab/salmon/releases/download/v1.7.0/salmon-1.7.0_linux_x86_64.tar.gz
echo "Salmon downloaded successfully"

echo "Extracting archive..."
tar --extract --gzip --verbose --file "$OUT_DIR"/salmon.tar.gz --directory "$OUT_DIR"
rm --force "$OUT_DIR"/salmon.tar.gz
echo "Archive extracted successfully"
echo "Salmon location: $(realpath "$OUT_DIR"/salmon-1.7.0_linux_x86_64/bin/salmon)"
