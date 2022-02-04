from pipeline import Pipeline
from job import Job


if __name__ == '__main__':
    printer = Job(script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/print.sh', memory = '4G', account = 'ELIX4_castrign2',
                  partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer', skip_file_check = True)

    reader = Job(script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/read.sh', memory = '4G', account = 'ELIX4_castrign2',
                 partition = 'g100_usr_prod', max_run_time = '0:30:00', n_nodes = 1, n_threads = 1, name = 'Reader', previous_step = printer, skip_file_check = True)

    jobs = [reader, printer]

    p = Pipeline(jobs)
    p.run_entire_pipeline()
