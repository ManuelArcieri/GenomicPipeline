#!/bin/bash
#
# Assemble RNA-Seq alignments into potential transcripts.
#
# INPUT:
# - $BAM_FILE: input BAM file (e.g. "/some/dir/SRR8615270.bam")
# - $LABEL: prefix for the name of the output transcripts (e.g. "SRR8615270")
# - $OUT_FILE: output GTF file (e.g. "/some/dir/SRR8615270.gtf")

set -e

module load autoload profile/bioinf
module load stringtie
module load illumina_genome_Homo_sapiens

bash -c "mkdir --parents $(dirname "$OUT_FILE")"

stringtie -o "$OUT_FILE" \
    -eB -p 36 -G "$ANNOTATION"/Genes/genes.gtf \
    -l "$LABEL" "$BAM_FILE"
