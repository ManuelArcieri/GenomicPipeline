#!/bin/bash
#
# Assemble RNA-Seq alignments into potential transcripts.

set -e

module load autoload profile/bioinf
module load stringtie
module load illumina_genome_Homo_sapiens

BAM_FILE="$GEP_WD/BAM/$GEP_SAMPLE.bam"
GTF_FILE="$GEP_WD/GTF/$GEP_SAMPLE.gtf"

mkdir --parents "$(dirname "$GTF_FILE")"

stringtie -o "$GTF_FILE" \
    -eB -p "$GEP_N_THREADS" -G "$ANNOTATION"/Genes/genes.gtf \
    -l "$GEP_SAMPLE" "$BAM_FILE"
