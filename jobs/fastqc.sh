#!/bin/bash
#
# Do some quality control checks on raw sequence data coming from high throughput sequencing pipelines.
#
# INPUT:
# - $SAMPLE: FASTQ file (e.g. "/some/dir/SRR8615270.fastq")
# - $OUT_DIR: output directory (e.g. "/some/dir/SRR8615270")

set -e

module load autoload profile/bioinf
module load fastqc

mkdir --parents "$OUT_DIR"
cd "$OUT_DIR"

fastqc "$SAMPLE"
