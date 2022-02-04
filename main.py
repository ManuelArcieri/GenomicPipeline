from pipeline import Pipeline
from job import Job


if __name__ == '__main__':
    jobs = [Job(script_file = '/g100/home/userexternal/marcieri/SCRATCH/pipeline/test.sh', memory = '4G', account = 'ELIX4_castrign2',
                partition = 'g100_usr_prod', max_run_time = '4:00:00', n_nodes = 1, n_threads = 1, name = 'Printer')]

    p = Pipeline(jobs)
    p.run_entire_pipeline()
