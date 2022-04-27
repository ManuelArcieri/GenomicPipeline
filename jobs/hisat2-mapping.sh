#!/bin/bash
#
# Maps a pair-ended sample into a SAM file.
#
# INPUT:
# - $MATE_PAIRED_1: paired mate 1 (e.g. "SRR8615270_1.paired.fastq")
# - $MATE_PAIRED_2: paired mate 2 (e.g. "SRR8615270_2.paired.fastq")
# - $MATE_UNPAIRED_1: unpaired mate 1 (e.g. "SRR8615270_1.unpaired.fastq")
# - $MATE_UNPAIRED_2: unpaired mate 2 (e.g. "SRR8615270_2.unpaired.fastq")
# - $OUT_FILE: output file (e.g. "/some/dir/SRR8615270.sam")

set -e

module load autoload profile/bioinf
module load hisat2

bash -c "mkdir --parents $(dirname "$OUT_FILE")"

hisat2 --threads 36 --downstream-transcriptome-assembly --quiet \
    -x "$HISAT2_HOME"/genomic_indexes/hg38_UCSC/genome \
    -1 "$MATE_PAIRED_1" \
    -2 "$MATE_PAIRED_2" \
    -U "$MATE_UNPAIRED_1","$MATE_UNPAIRED_2" \
    -S "$OUT_FILE"
