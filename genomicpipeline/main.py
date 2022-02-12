import os.path
from sys import argv, stderr
from pipeline import Pipeline
from job import Job
from uuid import uuid4


def main():
    if len(argv) <= 1 or argv[1].lower() in ('help', '-h', '--help'):
        print_help()

    elif len(argv) == 3 and argv[1] == 'run':  # ./gp.sh run pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            pipeline.run_entire_pipeline()
            pipeline.save_to_toml_file(argv[2])
            print('All jobs have been queued.\nRun "./gp.sh status pipeline.toml" to display the current status of the jobs.')
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    elif len(argv) == 3 and argv[1] == 'step':  # ./gp.sh step pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            pipeline.run_next_step()
            pipeline.save_to_toml_file(argv[2])
            print('All jobs of the next step have been queued.\nRun "./gp.sh status pipeline.toml" to display the current status of the jobs.')
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    elif len(argv) == 3 and argv[1] == 'status':  # ./gp.sh status pipeline.toml
        if os.path.isfile(argv[2]):
            pipeline = Pipeline.load_from_toml_file(argv[2])
            # ...
            pipeline.save_to_toml_file(argv[2])
        else:
            print(f'The provided file does not exist: {argv[2]}', file = stderr)
            exit(2)

    else:
        print_help()


def print_help():
    print('Genomic Pipeline')
    print('https://github.com/ManuelArcieri/GenomicPipeline')
    print('\nUsage: ./gp.sh <COMMAND>')  # TODO Define commands


if __name__ == '__main__':
    printer = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/print.sh', memory = '4G', account = 'ELIX4_castrign2',
                  partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer', skip_file_check = True)

    reader = Job(uuid = str(uuid4()), script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/read.sh', memory = '4G', account = 'ELIX4_castrign2',
                 partition = 'g100_usr_prod', max_run_time = '0:30:00', n_nodes = 1, n_threads = 1, name = 'Reader', previous_step = printer, skip_file_check = True)

    jobs = [reader, printer]

    p = Pipeline('Test pipeline', jobs)
    p.save_to_toml_file('test.toml')
    p2 = Pipeline.load_from_toml_file('test.toml')
    main()
