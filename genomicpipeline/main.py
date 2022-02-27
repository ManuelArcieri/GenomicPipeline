import os.path
import subprocess
from pipeline import Pipeline
from sys import argv, stderr


VERSION = '0.1.4'


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

    elif len(argv) == 4 and argv[1] == 'requeue' and argv[2] == 'failed':  # gep requeue failed pipeline.toml
        if os.path.isfile(argv[3]):
            pipeline = Pipeline.load_from_toml_file(argv[3])
            pipeline.update_jobs_status()
            pipeline.requeue_failed_jobs()
            pipeline.update_jobs_status()
            pipeline.save_to_toml_file(argv[3])
        else:
            print(f'The provided file does not exist: {argv[3]}', file = stderr)
            exit(2)

    elif len(argv) == 2 and argv[1] == 'upgrade':  # gep upgrade
        cmd = 'bash "$HOME"/GenomicPipeline/install.sh'
        process = subprocess.Popen(cmd, shell = True)
        process.wait()

    else:
        print_help()


def print_help():
    print(f'Genomic Pipeline {VERSION}')
    print('https://github.com/ManuelArcieri/GenomicPipeline')
    print('\nUsage:\n')
    print('• gep run [PIPELINE FILE]')
    print('      Runs all the steps of the specified pipeline (.toml) file\n')
    print('• gep step [PIPELINE FILE]')
    print('      Runs a single step of the specified pipeline (.toml) file\n')
    print('• gep status [PIPELINE FILE]')
    print('      Prints the status of all jobs of the specified pipeline (.toml) file\n')
    print('• gep upgrade')
    print('      Upgrades Genomic Pipeline to its latest version\n')


if __name__ == '__main__':
    main()
