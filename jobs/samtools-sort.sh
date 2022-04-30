#!/bin/bash
#
# Sort alignments by leftmost coordinates.
#
# INPUT:
# - $SAM_FILE: input SAM file (e.g. "/some/dir/SRR8615270.sam")
# - $OUT_FILE: output BAM file (e.g. "/some/dir/SRR8615270.bam")

set -e

module load autoload profile/bioinf
module load samtools

python3 $"GEP_HOME"/jobs/makedirs.py "$(dirname "$OUT_FILE")"

samtools sort -@ 36 -o "$OUT_FILE" "$SAM_FILE"
