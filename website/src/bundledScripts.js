"use strict";

export const scripts = [
    {
        file: "barrier.sh",
        name: "Barrier (NO-OP)",
        envVariables: ""
    },
    {
        file: "fastq-dump-PE.sh",
        name: "fastq-dump (paired-end)",
        envVariables: ""
    },
    {
        file: "fastq-dump-SE.sh",
        name: "fastq-dump (single-end)",
        envVariables: ""
    },
    {
        file: "fastqc.sh",
        name: "FastQC",
        envVariables: "FASTQ_FILE=/some/dir/file.fastq"
    },
    {
        file: "hisat2-mapping-PE.sh",
        name: "HISAT2 (paired-end, Human)",
        envVariables: ""
    },
    {
        file: "hisat2-mapping-PE-custom.sh",
        name: "HISAT2 (paired-end, custom genome)",
        envVariables: "GENOME_INDEX=some/directory"
    },
    {
        file: "hisat2-mapping-PE-mm10.sh",
        name: "HISAT2 (paired-end, Mus musculus)",
        envVariables: ""
    },
    {
        file: "hisat2-mapping-SE.sh",
        name: "HISAT2 (single-end, Human)",
        envVariables: ""
    },
    {
        file: "samtools-sort.sh",
        name: "Sort (Samtools)",
        envVariables: ""
    },
    {
        file: "sra-prefetch.sh",
        name: "Prefetch (SRA tools)",
        envVariables: ""
    },
    {
        file: "stringtie.sh",
        name: "StringTie (Human)",
        envVariables: ""
    },
    {
        file: "stringtie-mm10.sh",
        name: "StringTie (Mus musculus)",
        envVariables: ""
    },
    {
        file: "trimmomatic-PE.sh",
        name: "Trimmomatic (paired-end)",
        envVariables: ""
    },
    {
        file: "trimmomatic-PE-g.sh",
        name: "Trimmomatic (paired-end, generic file extension)",
        envVariables: "FASTQ_EXT_1=_R1_001.fastq.gz,FASTQ_EXT_2=_R2_001.fastq.gz"
    },
    {
        file: "trimmomatic-SE.sh",
        name: "Trimmomatic (single-end)",
        envVariables: ""
    }
];
