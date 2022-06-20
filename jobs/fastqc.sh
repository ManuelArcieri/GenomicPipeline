#!/bin/bash
#
# Do some quality control checks on raw sequence data coming from high throughput sequencing pipelines.

set -e

module load autoload profile/bioinf
module load fastqc

FASTQC_DIR="$GEP_WD/fastqc/$GEP_SAMPLE"

mkdir --parents "$FASTQC_DIR"

fastqc --outdir "$FASTQC_DIR" --threads "$GEP_N_THREADS" "$GEP_WD/FASTQ/$GEP_SAMPLE"_1.fastq
fastqc --outdir "$FASTQC_DIR" --threads "$GEP_N_THREADS" "$GEP_WD/FASTQ/$GEP_SAMPLE"_2.fastq
