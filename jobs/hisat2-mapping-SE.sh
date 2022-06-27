#!/bin/bash
#
# Maps a single-ended sample into a SAM file.

set -e

module load autoload profile/bioinf
module load hisat2

TRIM_DIR="$GEP_WD/trimmed"
SAM_DIR="$GEP_WD/SAM"

mkdir --parents "$(dirname "$OUT_FILE")"
mkdir --parents "$SAM_DIR"

hisat2 --threads "$GEP_N_THREADS" --downstream-transcriptome-assembly --quiet \
    -x "$HISAT2_INDEXES"/hg38_UCSC/genome \
    -U "$TRIM_DIR/$GEP_SAMPLE".trimmed.fastq \
    -S "$SAM_DIR/$GEP_SAMPLE.sam"
