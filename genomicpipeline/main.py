import os.path
from sys import argv, stderr
from pipeline import Pipeline
from job import Job
from uuid import uuid4


def main():
    if len(argv) <= 1 or argv[1].lower() in ('help', '-h', '--help'):
        print_help_and_quit()
    elif len(argv) >= 3 and argv[1] == 'run':
        if os.path.exists(argv[2]) and os.path.isfile(argv[2]):
            pass
        else:
            print('The provided file does not exist', file = stderr)
            exit(2)


def print_help_and_quit():
    print('Genomic Pipeline')
    print('https://github.com/ManuelArcieri/GenomicPipeline')
    print('\nUsage: ./gp.sh <COMMAND>')  # TODO Define commands
    exit()


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
