#!/bin/bash
#
# Download the specified Sequence Read Archive (SRA) datafile and store it locally.
#
# IMPORTANT: the temp folder $HOME/ncbi must be manually removed after the execution
#            of the jobs.
#
# INPUT:
# - $SAMPLE: SRA accession (e.g. "SRR390728")
# - $OUT_FILE: file name (e.g. "/some/dir/SRR390728.sra")

set -e

module load profile/bioinf
module load autoload sra

echo "Downloading $SAMPLE..."

vdb-config -s /repository/remote/disabled=false
vdb-config -s /repository/user/cache-disabled=false
vdb-config -s /repository/user/main/public/root=$SCRATCH/ncbi/public

prefetch "$SAMPLE" --output-file "$OUT_FILE"
echo "$SAMPLE downloaded successfully"
