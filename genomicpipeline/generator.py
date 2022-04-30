import os.path
from job import Job
from uuid import uuid4
from pipeline import Pipeline


desktop = os.path.expandvars('$HOME/Desktop')

with open(f'{desktop}/carcinoma.txt') as c_file:
    carcinoma = [a.strip() for a in c_file.read().splitlines() if a.strip() != '']

with open(f'{desktop}/melanoma.txt') as m_file:
    melanoma = [a.strip() for a in m_file.read().splitlines() if a.strip() != '']

assert all(map(lambda s: len(s) == 10, carcinoma))
assert all(map(lambda s: len(s) == 10, melanoma))

jobs = []

for folder, samples in (('carcinoma', carcinoma), ('melanoma', melanoma)):
    for sample in samples:
        fastq_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/FASTQ'
        c_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/FASTQC'
        trim_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/trimmed'
        sam_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/SAM'
        bam_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/BAM'
        gtf_dir = f'$SCRATCH/carcinoma-melanoma/{folder}/GTF'

        trimming = Job(uuid = uuid4().hex, script_file = 'trimmomatic.sh', memory = '128GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                       n_nodes = 1, n_threads = 36, name = f'Trim {sample}',
                       environment_variables = f'MATE_1={fastq_dir}/{sample}_1.fastq,MATE_2={fastq_dir}/{sample}_2.fastq,OUT_MATE_PAIRED_1={trim_dir}/{sample}_1.trimmed.paired.fastq,OUT_MATE_PAIRED_2={trim_dir}/{sample}_2.trimmed.paired.fastq,OUT_MATE_UNPAIRED_1={trim_dir}/{sample}_1.trimmed.unpaired.fastq,OUT_MATE_UNPAIRED_2={trim_dir}/{sample}_2.trimmed.unpaired.fastq')

        fastqc_t1 = Job(uuid = uuid4().hex, script_file = 'fastqc.sh', memory = '32GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                        n_nodes = 1, n_threads = 6, name = f'fastqc trimmed {sample}',
                        environment_variables = f'SAMPLE={trim_dir}/{sample}_1.trimmed.paired.fastq,OUT_DIR={c_dir}/{sample}_1.trimmed.paired.fastq',
                        previous_steps = {trimming.uuid: trimming})

        fastqc_t2 = Job(uuid = uuid4().hex, script_file = 'fastqc.sh', memory = '32GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                        n_nodes = 1, n_threads = 6, name = f'fastqc trimmed {sample}',
                        environment_variables = f'SAMPLE={trim_dir}/{sample}_2.trimmed.paired.fastq,OUT_DIR={c_dir}/{sample}_2.trimmed.paired.fastq',
                        previous_steps = {trimming.uuid: trimming})

        fastqc_t3 = Job(uuid = uuid4().hex, script_file = 'fastqc.sh', memory = '32GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                        n_nodes = 1, n_threads = 6, name = f'fastqc trimmed {sample}',
                        environment_variables = f'SAMPLE={trim_dir}/{sample}_1.trimmed.unpaired.fastq,OUT_DIR={c_dir}/{sample}_1.trimmed.unpaired.fastq',
                        previous_steps = {trimming.uuid: trimming})

        fastqc_t4 = Job(uuid = uuid4().hex, script_file = 'fastqc.sh', memory = '32GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                        n_nodes = 1, n_threads = 6, name = f'fastqc trimmed {sample}',
                        environment_variables = f'SAMPLE={trim_dir}/{sample}_2.trimmed.unpaired.fastq,OUT_DIR={c_dir}/{sample}_2.trimmed.unpaired.fastq',
                        previous_steps = {trimming.uuid: trimming})

        mapping = Job(uuid = uuid4().hex, script_file = 'hisat2-mapping.sh', memory = '256GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                      n_nodes = 1, n_threads = 36, name = f'Map {sample}',
                      environment_variables = f'MATE_PAIRED_1={trim_dir}/{sample}_1.trimmed.paired.fastq,MATE_PAIRED_2={trim_dir}/{sample}_2.trimmed.paired.fastq,MATE_UNPAIRED_1={trim_dir}/{sample}_1.trimmed.unpaired.fastq,MATE_UNPAIRED_2={trim_dir}/{sample}_2.trimmed.unpaired.fastq,OUT_FILE={sam_dir}/{sample}.sam',
                      previous_steps = {trimming.uuid: trimming})

        sorting = Job(uuid = uuid4().hex, script_file = 'samtools-sort.sh', memory = '128GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                      n_nodes = 1, n_threads = 36, name = f'Sort {sample}',
                      environment_variables = f'SAM_FILE={sam_dir}/{sample}.sam,OUT_FILE={bam_dir}/{sample}.bam',
                      previous_steps = {mapping.uuid: mapping})

        stringtie = Job(uuid = uuid4().hex, script_file = 'stringtie.sh', memory = '256GB', account = 'ELIX4_palomba', partition = 'g100_usr_prod', max_run_time = '24:00:00',
                        n_nodes = 1, n_threads = 36, name = f'StringTie {sample}',
                        environment_variables = f'BAM_FILE={bam_dir}/{sample}.bam,LABEL={sample},OUT_FILE={gtf_dir}/{sample}.gtf',
                        previous_steps = {sorting.uuid: sorting})

        jobs.extend((trimming, fastqc_t1, fastqc_t2, fastqc_t3, fastqc_t4, mapping, sorting, stringtie))

pipeline = Pipeline('Carcinoma/melanoma pipeline tris', jobs, '$SCRATCH/carcinoma-melanoma')
pipeline_path = f'{desktop}/pipeline-5.toml'
pipeline.save_to_toml_file(pipeline_path)
print(f'Pipeline exported in {pipeline_path}')
