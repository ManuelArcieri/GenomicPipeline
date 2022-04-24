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

for sample in carcinoma:
    sra_file = f'$SCRATCH/carcinoma-melanoma/carcinoma/SRA/{sample}.sra'
    fastq_dir = '$SCRATCH/carcinoma-melanoma/carcinoma/FASTQ'

    prefetch = Job(uuid = uuid4().hex, script_file = 'sra-prefetch.sh', memory = '8GB', account = 'ELIX4_palomba', partition = 'g100_all_serial', max_run_time = '4:00:00',
                   n_nodes = 1, n_threads = 1, name = f'Prefetch {sample}',
                   environment_variables = f'SAMPLE={sample},OUT_FILE={sra_file}')

    dump = Job(uuid = uuid4().hex, script_file = 'fastq-dump.sh', memory = '30GB', account = 'ELIX4_palomba', partition = 'g100_all_serial', max_run_time = '4:00:00',
               n_nodes = 1, n_threads = 4, name = f'fastq-dump {sample}',
               environment_variables = f'SRA_FILE={sra_file},OUT_DIR={fastq_dir}', previous_steps = {prefetch.uuid: prefetch})

    jobs.extend((prefetch, dump))

for sample in melanoma:
    sra_file = f'$SCRATCH/carcinoma-melanoma/melanoma/SRA/{sample}.sra'
    fastq_dir = '$SCRATCH/carcinoma-melanoma/melanoma/FASTQ'

    prefetch = Job(uuid = uuid4().hex, script_file = 'sra-prefetch.sh', memory = '8GB', account = 'ELIX4_palomba', partition = 'g100_all_serial', max_run_time = '4:00:00',
                   n_nodes = 1, n_threads = 1, name = f'Prefetch {sample}',
                   environment_variables = f'SAMPLE={sample},OUT_FILE={sra_file}')

    dump = Job(uuid = uuid4().hex, script_file = 'fastq-dump.sh', memory = '30GB', account = 'ELIX4_palomba', partition = 'g100_all_serial', max_run_time = '4:00:00',
               n_nodes = 1, n_threads = 4, name = f'fastq-dump {sample}',
               environment_variables = f'SRA_FILE={sra_file},OUT_DIR={fastq_dir}', previous_steps = {prefetch.uuid: prefetch})

    jobs.extend((prefetch, dump))

pipeline = Pipeline('Carcinoma/melanoma pipeline', jobs, '$SCRATCH/carcinoma-melanoma')
pipeline_path = f'{desktop}/pipeline.toml'
pipeline.save_to_toml_file(pipeline_path)
print(f'Pipeline exported in {pipeline_path}')
