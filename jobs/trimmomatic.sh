#!/bin/bash
#
# Trim Illumina sequence data.

set -e

module load autoload profile/bioinf
module load trimmomatic

FASTQ_DIR="$GEP_WD/FASTQ"
TRIM_DIR="$GEP_WD/trimmed"

mkdir --parents "$(dirname "$TRIM_DIR")"

java -jar "$TRIMMOMATIC_HOME"/bin/trimmomatic-0.39.jar PE -threads "$GEP_N_THREADS" -phred33 \
    "$FASTQ_DIR/$GEP_SAMPLE"_1.fastq "$FASTQ_DIR/$GEP_SAMPLE"_2.fastq \
    "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.paired.fastq "$TRIM_DIR/$GEP_SAMPLE"_1.trimmed.unpaired.fastq \
    "$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.paired.fastq "$TRIM_DIR/$GEP_SAMPLE"_2.trimmed.unpaired.fastq \
    ILLUMINACLIP:"$TRIMM_ADAPTERS"/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:36 HEADCROP:13
