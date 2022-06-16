#!/bin/bash
#
# Perform dual-phase, selective-alignment-based estimation of
# transcript abundance from RNA-seq reads.
#
# INPUT:
# - $SALMON_EXE: Salmon executable file (e.g. "/bin/salmon")
# - $INDEX_DIR: Salmon index (e.g. "/some/dir")
# - $MATES_1: File containing the #1 mates (e.g. "SRR8618301_1.fastq")
# - $MATES_2: File containing the #2 mates (e.g. "SRR8618301_2.fastq")
# - $OUT_DIR: output directory (e.g. "/some/dir")

set -e

echo "Quantifying RNA-seq reads..."
$SALMON_EXE --no-version-check quant --index "$INDEX_DIR" --threads "$GEP_N_THREADS" --libType A --gcBias --numGibbsSamples 20 --output "$OUT_DIR" --mates1 "$MATES_1" --mates2 "$MATES_2"
echo "RNA-seq reads quantified successfully"
