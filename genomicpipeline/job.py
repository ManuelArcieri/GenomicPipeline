import os.path
import subprocess
from enum import Enum, auto
from typing import Optional
from utility import ensure, get_or_raise


class Job:
    def __init__(self, *, uuid: str, script_file: str, memory: str, account: str, partition: str, max_run_time: str,
                 qos = None, n_nodes: int, n_threads: int, name, skip_file_check = False, previous_step = None, next_step = None):
        self.uuid = uuid
        self.script_file = script_file
        self.memory = memory
        self.account = account
        self.partition = partition
        self.max_run_time = max_run_time
        self.qos: Optional[str] = qos if qos != '' and qos is not None else None
        self.n_nodes = n_nodes
        self.n_threads = n_threads
        self.name: Optional[str] = name if name != '' and name is not None else None
        self.id: Optional[int] = None
        self.status = JobStatus.PENDING
        self.pipeline_step: Optional[int] = None
        self.skip_file_check = skip_file_check
        self.previous_step: Optional[Job] = previous_step
        self.previous_step_uuid: Optional[str] = None
        self.next_step: Optional[Job] = next_step
        self.next_step_uuid: Optional[str] = None

        if self.previous_step is not None:
            self.previous_step_uuid = self.previous_step.uuid
            self.previous_step.next_step = self

        if self.next_step is not None:
            self.next_step_uuid = self.next_step.uuid
            self.next_step.previous_step = self

        self._check_parameters()


    def _check_parameters(self):
        if not self.skip_file_check:
            ensure(os.path.exists(self.script_file), f'the script file does not exist: "{self.script_file}"')
            ensure(os.path.isfile(self.script_file), f'the provided script is not a file: "{self.script_file}"')

        ensure(self.memory[:-1].isnumeric(), f'the memory value "{self.memory}" does not start with a number')
        ensure(self.memory[-1] in ('K', 'M', 'G', 'T', 'KB', 'MB', 'GB', 'TB') or self.memory[-1].isnumeric(),
               f'the memory value "{self.memory}" does not end with a valid suffix (K|M|G|T)')
        ensure(len(self.account) > 0, 'the account is undefined')
        ensure(len(self.partition) > 0, 'the partition is undefined')
        ensure(len(self.max_run_time) > 0, 'the maximum run time is undefined')
        ensure(self.n_nodes > 0, f'the number of nodes must be greater than zero (found: {self.n_nodes})')
        ensure(self.n_threads > 0, f'the number of threads must be greater than zero (found: {self.n_nodes})')


    def run(self):
        dependency = '' if self.previous_step is None else f'--dependency afterok:{self.previous_step.id}'
        job_name = '' if self.name is None else f'--job-name "{self.name}"'
        qos = '' if self.qos is None else f'--qos {self.qos}'

        cmd = f'sbatch --account {self.account} --comment "Automatically queued by Genomic Pipeline: https://github.com/ManuelArcieri/GenomicPipeline" \
                {dependency} --error "./%j-err.txt" {job_name} --mem {self.memory} --nodes {self.n_nodes} --ntasks {self.n_threads} \
                --output "./%j-out.txt" --partition {self.partition} {qos} --time "{self.max_run_time}" {self.script_file}' \
            .replace('                 ', ' ').replace('  ', ' ')

        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        out, err = process.communicate()
        ensure(process.returncode == 0, f'sbatch exited with error code {process.returncode}.\n\n'
                                        f'cmd = {cmd}\n\n'
                                        f'stderr = {err}\n\n'
                                        f'stdout = {out}\n\n')

        self.id = int(out.strip().split(' ')[-1])  # E.g. "Submitted batch job 1234"
        self.status = JobStatus.RUNNING


    def __dict__(self) -> dict:
        job = {}
        if self.name is not None and self.name != '':
            job['name'] = self.name
        if self.id is not None:
            job['id'] = self.id
        job['uuid'] = self.uuid
        job['status'] = self.status.name
        job['script_file'] = self.script_file
        job['n_nodes'] = self.n_nodes
        job['n_threads'] = self.n_threads
        job['memory'] = self.memory
        job['account'] = self.account
        job['partition'] = self.partition
        if self.qos is not None and self.qos != '':
            job['qos'] = self.qos
        job['max_run_time'] = self.max_run_time
        if self.pipeline_step is not None:
            job['pipeline_step'] = self.pipeline_step
        if self.skip_file_check:
            job['skip_file_check'] = self.skip_file_check
        if self.previous_step_uuid is not None and self.previous_step_uuid != '':
            job['previous_step_uuid'] = self.previous_step_uuid
        if self.next_step_uuid is not None and self.next_step_uuid != '':
            job['next_step_uuid'] = self.next_step_uuid
        return job


    @staticmethod
    def from_dict(values: dict):
        job = Job(uuid = get_or_raise(values, 'uuid'),
                  script_file = get_or_raise(values, 'script_file'),
                  memory = get_or_raise(values, 'memory'),
                  account = get_or_raise(values, 'account'),
                  partition = get_or_raise(values, 'partition'),
                  max_run_time = get_or_raise(values, 'max_run_time'),
                  qos = values.get('qos', None),
                  n_nodes = get_or_raise(values, 'n_nodes'),
                  n_threads = get_or_raise(values, 'n_threads'),
                  name = values.get('name', None),
                  skip_file_check = values.get('skip_file_check', False))

        job.id = values.get('id', None)
        job.status = JobStatus(get_or_raise(values, 'status'))
        job.pipeline_step = values.get('pipeline_step', None)
        job.previous_step_uuid = values.get('previous_step_uuid', None)
        job.next_step_uuid = values.get('next_step_uuid', None)
        return job


class JobStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    COMPLETED = 'COMPLETED'
