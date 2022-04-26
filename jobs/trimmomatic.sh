#!/bin/bash
#
# Trim Illumina sequence data.
#
# INPUT:
# - $MATE_1: mate 1 (e.g. "/some/dir/SRR8615270_1.fastq")
# - $MATE_2: mate 2 (e.g. "/some/dir/SRR8615270_2.fastq")
# - $OUT_MATE_PAIRED_1: paired mate 1 (e.g. "/some/dir/SRR8615270_1.trimmed.paired.fastq")
# - $OUT_MATE_PAIRED_2: paired mate 2 (e.g. "/some/dir/SRR8615270_2.trimmed.paired.fastq")
# - $OUT_MATE_UNPAIRED_1: unpaired mate 1 (e.g. "/some/dir/SRR8615270_1.trimmed.unpaired.fastq")
# - $OUT_MATE_UNPAIRED_2: unpaired mate 2 (e.g. "/some/dir/SRR8615270_2.trimmed.unpaired.fastq")

set -e

module load autoload profile/bioinf
module load trimmomatic

mkdir --parents "$(dirname "$OUT_MATE_PAIRED_1")"
mkdir --parents "$(dirname "$OUT_MATE_PAIRED_2")"
mkdir --parents "$(dirname "$OUT_MATE_UNPAIRED_1")"
mkdir --parents "$(dirname "$OUT_MATE_UNPAIRED_2")"

java -jar "$TRIMMOMATIC_HOME"/bin/trimmomatic-0.39.jar PE -threads 36 -phred33 \
    "$MATE_1" "$MATE_2" \
    "$OUT_MATE_PAIRED_1" "$OUT_MATE_UNPAIRED_1" \
    "$OUT_MATE_PAIRED_2" "$OUT_MATE_UNPAIRED_2" \
    ILLUMINACLIP:"$TRIMM_ADAPTERS"/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:15 MINLEN:36 HEADCROP:13
