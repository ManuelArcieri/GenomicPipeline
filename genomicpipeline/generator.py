import os.path
from job import Job
from uuid import uuid4
from pipeline import Pipeline


desktop = os.path.expandvars('$HOME/Desktop')

with open(f'{desktop}/BREAST.txt') as b_file:
    breast = [a.strip() for a in b_file.read().splitlines() if a.strip() != '']

with open(f'{desktop}/MELANOMA.txt') as m_file:
    melanoma = [a.strip() for a in m_file.read().splitlines() if a.strip() != '']

assert all(map(lambda s: len(s) == 10, breast))
assert all(map(lambda s: len(s) == 10, melanoma))

salmon_dir = '$SCRATCH/breast-melanoma/salmon'
salmon_exe = f'{salmon_dir}/salmon-1.7.0_linux_x86_64/bin/salmon'
salmon_index = '$SCRATCH/breast-melanoma/salmon-index-hg38'
quant_dir = '$SCRATCH/breast-melanoma/quant'

download_salmon = Job(uuid = uuid4().hex, script_file = 'download-salmon.sh', memory = '4GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial',
                      max_run_time = '04:00:00',
                      n_nodes = 1, n_threads = 1, name = 'Download Salmon binary',
                      environment_variables = f'OUT_DIR={salmon_dir}')

download_index = Job(uuid = uuid4().hex, script_file = 'download-hg38-salmon-index.sh', memory = '4GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial',
                     max_run_time = '04:00:00',
                     n_nodes = 1, n_threads = 1, name = 'Download pre-built hg38 Salmon index',
                     environment_variables = f'OUT_DIR={salmon_index}')

jobs = [download_salmon, download_index]

for sample in breast:
    sra_file = f'$SCRATCH/breast-melanoma/breast/SRA/{sample}.sra'
    fastq_dir = '$SCRATCH/breast-melanoma/breast/FASTQ'

    prefetch = Job(uuid = uuid4().hex, script_file = 'sra-prefetch.sh', memory = '8GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial', max_run_time = '4:00:00',
                   n_nodes = 1, n_threads = 1, name = f'Prefetch {sample}',
                   environment_variables = f'SAMPLE={sample},OUT_FILE={sra_file}')

    dump = Job(uuid = uuid4().hex, script_file = 'fastq-dump.sh', memory = '30GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial', max_run_time = '4:00:00',
               n_nodes = 1, n_threads = 4, name = f'fastq-dump {sample}',
               environment_variables = f'SRA_FILE={sra_file},OUT_DIR={fastq_dir}', previous_steps = {prefetch.uuid: prefetch})

    quant = Job(uuid = uuid4().hex, script_file = 'salmon-quant.sh', memory = '256GB', account = 'ELIX4_castrign2', partition = 'g100_usr_prod', max_run_time = '20:00:00',
                n_nodes = 1, n_threads = 8, name = f'Salmon quant {sample}',
                environment_variables = f'SALMON_EXE={salmon_exe},INDEX_DIR={salmon_index},MATES_1={fastq_dir}/{sample}_1.fastq,MATES_2={fastq_dir}/{sample}_2.fastq,OUT_DIR={quant_dir}/{sample}',
                previous_steps = {download_index.uuid: download_index, download_salmon.uuid: download_salmon, dump.uuid: dump})

    jobs.extend((prefetch, dump, quant))

for sample in melanoma:
    sra_file = f'$SCRATCH/breast-melanoma/melanoma/SRA/{sample}.sra'
    fastq_dir = '$SCRATCH/breast-melanoma/melanoma/FASTQ'

    prefetch = Job(uuid = uuid4().hex, script_file = 'sra-prefetch.sh', memory = '8GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial', max_run_time = '4:00:00',
                   n_nodes = 1, n_threads = 1, name = f'Prefetch {sample}',
                   environment_variables = f'SAMPLE={sample},OUT_FILE={sra_file}')

    dump = Job(uuid = uuid4().hex, script_file = 'fastq-dump.sh', memory = '30GB', account = 'ELIX4_castrign2', partition = 'g100_all_serial', max_run_time = '4:00:00',
               n_nodes = 1, n_threads = 4, name = f'fastq-dump {sample}',
               environment_variables = f'SRA_FILE={sra_file},OUT_DIR={fastq_dir}', previous_steps = {prefetch.uuid: prefetch})

    quant = Job(uuid = uuid4().hex, script_file = 'salmon-quant.sh', memory = '256GB', account = 'ELIX4_castrign2', partition = 'g100_usr_prod', max_run_time = '20:00:00',
                n_nodes = 1, n_threads = 8, name = f'Salmon quant {sample}',
                environment_variables = f'SALMON_EXE={salmon_exe},INDEX_DIR={salmon_index},MATES_1={fastq_dir}/{sample}_1.fastq,MATES_2={fastq_dir}/{sample}_2.fastq,OUT_DIR={quant_dir}/{sample}',
                previous_steps = {download_index.uuid: download_index, download_salmon.uuid: download_salmon, dump.uuid: dump})

    jobs.extend((prefetch, dump, quant))

pipeline = Pipeline('Breast/melanoma pipeline', jobs, '$SCRATCH/breast-melanoma')
pipeline_path = f'{desktop}/pipeline.toml'
pipeline.save_to_toml_file(pipeline_path)
print(f'Pipeline exported in {pipeline_path}')
