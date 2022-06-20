#!/bin/bash
#
# Sort alignments by leftmost coordinates.

set -e

module load autoload profile/bioinf
module load samtools

BAM_FILE="$GEP_WD/BAM/$GEP_SAMPLE.bam"

mkdir --parents "$(dirname "$BAM_FILE")"

samtools sort -@ "$GEP_N_THREADS" -o "$BAM_FILE" "$GEP_WD/SAM/$GEP_SAMPLE.sam"
