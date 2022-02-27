#!/bin/bash
#
# Download a pre-built hg38 Salmon index and store it locally.
# Source: http://refgenomes.databio.org/v3/assets/splash/2230c535660fb4774114bfa966a62f823fdb6d21acf138d4/salmon_sa_index?tag=default
#
# INPUT:
# - $OUT_DIR: output directory (e.g. "/some/dir")

set -e

echo "Downloading hg38/salmon_sa_index:default..."
mkdir --parents "$OUT_DIR"
wget --no-verbose --tries 5 --timeout 10 --output-document "$OUT_DIR"/index.tar.gz http://refgenomes.databio.org/v3/assets/archive/2230c535660fb4774114bfa966a62f823fdb6d21acf138d4/salmon_sa_index?tag=default
echo "Salmon index downloaded successfully"

echo "Extracting archive..."
tar --extract --gzip --verbose --file "$OUT_DIR"/index.tar.gz --directory "$OUT_DIR"
rm --force "$OUT_DIR"/index.tar.gz
mv --force "$OUT_DIR"/default/* "$OUT_DIR"/
rm --force --recursive --dir "$OUT_DIR"/default
echo "Archive extracted successfully"
