#!/bin/bash
#
# Do some quality control checks on raw sequence data coming from high throughput sequencing pipelines.
#
# INPUT:
# - $FASTQ_FILE: file to be sequenced (e.g. "SRR8615716.fastq")

set -e

module load autoload profile/bioinf
module load fastqc

FASTQC_DIR="$GEP_WD/fastqc/$(basename "$FASTQ_FILE" .fastq)"

mkdir --parents "$FASTQC_DIR"

fastqc --outdir "$FASTQC_DIR" --threads "$GEP_N_THREADS" "$FASTQ_FILE"
