#!/bin/bash
#
# Convert a SRA archive into a FASTQ file

set -e

module load profile/bioinf
module load autoload sra

SRA_FILE="$GEP_WD/SRA/$GEP_SAMPLE.sra"

echo "Splitting $SRA_FILE"

vdb-config -s /repository/user/main/public/cache-enabled=true
vdb-config -s /repository/user/main/public/root="$SCRATCH/ncbi"

fastq-dump --outdir "$GEP_WD/FASTQ" "$SRA_FILE"

echo "Sample split successfully"
