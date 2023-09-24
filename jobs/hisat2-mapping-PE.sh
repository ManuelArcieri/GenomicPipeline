#!/bin/bash
#
# Maps a pair-ended sample into a SAM file.

set -e

module load autoload profile/bioinf
module load hisat2
module load illumina_genome_Homo_sapiens

TRIM_DIR="$GEP_WD/trimmed"
SAM_DIR="$GEP_WD/SAM"

mkdir --parents "$(dirname "$OUT_FILE")"
mkdir --parents "$SAM_DIR"

hisat2 --threads "$GEP_N_THREADS" --downstream-transcriptome-assembly --quiet \
    -x "$HISAT2_INDEX" \
    -1 "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.paired.fastq \
    -2 "$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.paired.fastq \
    -U "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.unpaired.fastq,"$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.unpaired.fastq \
    -S "$SAM_DIR/$GEP_SAMPLE.sam"
