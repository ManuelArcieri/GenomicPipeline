#!/bin/bash
#
# Download the specified Sequence Read Archive (SRA) datafile and store it locally.
#
# INPUT:
# - $SAMPLE: SRA accession (e.g. "SRR390728")
# - $OUT_FILE: file name (e.g. "/some/dir/SRR390728.sra")

set -e

module load profile/bioinf
module load autoload sra

echo "Downloading $SAMPLE..."

mkdir --parents "$SCRATCH/ncbi"
vdb-config -s /repository/remote/disabled=false
vdb-config -s /repository/user/cache-disabled=false
vdb-config -s /repository/user/main/public/cache-enabled=true
vdb-config -s /repository/user/main/public/root="$SCRATCH/ncbi"

prefetch "$SAMPLE" --output-file "$OUT_FILE"
echo "$SAMPLE downloaded successfully"
