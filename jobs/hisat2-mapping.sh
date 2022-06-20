#!/bin/bash
#
# Maps a pair-ended sample into a SAM file.

set -e

module load autoload profile/bioinf
module load hisat2

TRIM_DIR="$GEP_WD/trimmed"

mkdir --parents "$(dirname "$OUT_FILE")"

hisat2 --threads "$GEP_N_THREADS" --downstream-transcriptome-assembly --quiet \
    -x "$HISAT2_HOME"/genomic_indexes/hg38_UCSC/genome \
    -1 "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.paired.fastq \
    -2 "$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.paired.fastq \
    -U "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.unpaired.fastq,"$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.unpaired.fastq \
    -S "$GEP_WD/SAM/$GEP_SAMPLE.sam"
