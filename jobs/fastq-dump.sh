#!/bin/bash
#
# Split the FASTQ reads into two files: one file for mate 1s and another for mate 2s.
#
# INPUT:
# - $SRA_FILE: SRA file (e.g. "SRR390728.sra")
# - $OUT_DIR: output directory (e.g. "/some/dir")

set -e

module load profile/bioinf
module load autoload sra

echo "Splitting $SRA_FILE"
fastq-dump --outdir "$OUT_DIR" --split-files "$SRA_FILE"
echo "Sample split successfully"
