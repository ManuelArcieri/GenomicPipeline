#!/bin/bash
#
# Download the specified Sequence Read Archive (SRA) datafile and store it locally.

set -e

SRA_FILE="$GEP_WD/SRA/$GEP_SAMPLE.sra"

if [ -f "$GEP_SAMPLE" ]; then
    echo "$GEP_SAMPLE is a file. Copying..."
    cp --update "$GEP_SAMPLE" "$SRA_FILE"
    echo "File copied. Exiting..."
    exit
fi

module load profile/bioinf
module load autoload sra

echo "Downloading $GEP_SAMPLE..."

mkdir --parents "$SCRATCH/ncbi"
vdb-config -s /repository/remote/disabled=false
vdb-config -s /repository/user/cache-disabled=false
vdb-config -s /repository/user/main/public/cache-enabled=true
vdb-config -s /repository/user/main/public/root="$SCRATCH/ncbi"

prefetch --max-size 200G --output-file "$SRA_FILE" "$GEP_SAMPLE"
echo "$GEP_SAMPLE downloaded successfully"
