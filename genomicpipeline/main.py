import os.path
import subprocess
from job import Job
from pipeline import Pipeline
from sys import argv, stderr
from uuid import uuid4


VERSION = '0.1.1'


def main():
    if len(argv) <= 1 or argv[1].lower() in ('help', '-h', '--help'):
        print_help()

    elif len(argv) == 3 and argv[1] == 'run':  # gep run pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            pipeline.run_entire_pipeline()
            pipeline.save_to_toml_file(argv[2])
            print(f'All jobs have been queued.\nType "gep status {argv[2]}" to display the current status of the jobs.')
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    elif len(argv) == 3 and argv[1] == 'step':  # gep step pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            pipeline.run_next_step()
            pipeline.save_to_toml_file(argv[2])
            print(f'All jobs of the next step have been queued.\nType "gep status {argv[2]}" to display the current status of the jobs.')
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    elif len(argv) == 3 and argv[1] == 'status':  # gep status pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            pipeline.update_jobs_status()
            pipeline.save_to_toml_file(argv[2])
            pipeline.print_jobs_table()
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    elif len(argv) == 2 and argv[1] == 'upgrade':  # gep upgrade
        cmd = 'sh "$HOME"/GenomicPipeline/install.sh'
        process = subprocess.Popen(cmd, shell = True)
        process.wait()

    else:
        print_help()


def print_help():
    print(f'Genomic Pipeline {VERSION}')
    print('https://github.com/ManuelArcieri/GenomicPipeline')
    print('\nUsage: gep <COMMAND>')  # TODO Define commands


if __name__ == '__main__':
    printer1 = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/print.sh', memory = '4G', account = 'ELIX4_castrign2',
                   partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer', environment_variables = 'FILEN=1',
                   skip_file_check = True)

    printer2 = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/print.sh', memory = '4G', account = 'ELIX4_castrign2',
                   partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer', environment_variables = 'FILEN=2',
                   skip_file_check = True)

    printer3 = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/print.sh', memory = '4G', account = 'ELIX4_castrign2',
                   partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer', environment_variables = 'FILEN=3',
                   skip_file_check = True)

    reader = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/read.sh', memory = '4G', account = 'ELIX4_castrign2',
                 partition = 'g100_usr_prod', max_run_time = '0:30:00', n_nodes = 1, n_threads = 1, name = 'Reader', previous_steps = {printer1.uuid: printer1,
                                                                                                                                       printer2.uuid: printer2,
                                                                                                                                       printer3.uuid: printer3},
                 skip_file_check = True)

    jobs = [printer2, reader, printer3, printer1]

    # p = Pipeline('Test pipeline', jobs, '.')
    # p.save_to_toml_file('test.toml')
    main()
