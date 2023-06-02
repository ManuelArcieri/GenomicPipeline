#!/bin/bash
#
# Assemble RNA-Seq alignments into potential transcripts.

set -e

module load autoload profile/bioinf
module load stringtie
module load autoload illumina_genome_Mus_musculus/mm10

BAM_FILE="$GEP_WD/BAM/$GEP_SAMPLE.bam"
GTF_FILE="$GEP_WD/GTF/$GEP_SAMPLE.gtf"

mkdir --parents "$(dirname "$GTF_FILE")"

stringtie -o "$GTF_FILE" \
    -eB -p "$GEP_N_THREADS" -G "$ILLUMINA_GENOME_MUS_MUSCULUS_ANNOTATION"/Genes/genes.gtf \
    -l "$GEP_SAMPLE" "$BAM_FILE"
