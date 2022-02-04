import os.path
import subprocess
from enum import Enum, auto
from typing import Optional
from utility import ensure


class Job:
    def __init__(self, *, script_file: str, memory: str, account: str, partition: str, max_run_time: str,
                 qos = None, n_nodes: int, n_threads: int, name, previous_step = None, next_step = None):
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
        self.previous_step: Optional[Job] = previous_step
        self.next_step: Optional[Job] = next_step
        self._check_parameters()


    def _check_parameters(self):
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

        cmd = f'sbatch --account {self.account} --comment "Autorun by Genetic Pipeline" {dependency} --error "./%j-err.txt" {job_name} \
                --mem {self.memory} --nodes {self.n_nodes} --ntasks {self.n_threads} --output "./%j-out.txt" \
                --partition {self.partition} {qos} --time "{self.max_run_time}" {self.script_file}'.replace('                 ', ' ').replace('  ', ' ')

        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        out, err = process.communicate()
        ensure(process.returncode == 0, f'sbatch exited with error code {process.returncode}.\n\n'
                                        f'cmd = {cmd}\n\n'
                                        f'stderr = {err}\n\n'
                                        f'stdout = {out}\n\n')

        self.id = int(out.strip().split(' ')[-1])  # E.g. "Submitted batch job 1234"
        self.status = JobStatus.RUNNING


class JobStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    ERRORED = auto()
    COMPLETED = auto()
