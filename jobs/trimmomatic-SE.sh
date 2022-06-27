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
    "$FASTQ_DIR/$GEP_SAMPLE".fastq "$FASTQ_DIR/$GEP_SAMPLE".trimmed.fastq \
    ILLUMINACLIP:"$TRIMM_ADAPTERS"/TruSeq3-SE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:20 HEADCROP:13
