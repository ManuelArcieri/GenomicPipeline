import os.path
import subprocess
from enum import Enum
from typing import Optional
from utility import ensure, get_or_raise


class Job:
    def __init__(self, *, uuid: str, script_file: str, memory: str, account: str, partition: str, max_run_time: str,
                 qos = None, n_nodes: int, n_threads: int, name, environment_variables = None, skip_file_check = False, previous_step = None, next_step = None):
        self.uuid = uuid
        self.script_file = script_file
        self.memory = memory
        self.account = account
        self.partition = partition
        self.max_run_time = max_run_time
        self.current_run_time: Optional[str] = None
        self.qos: Optional[str] = qos if qos != '' and qos is not None else None
        self.n_nodes = n_nodes
        self.n_threads = n_threads
        self.name: Optional[str] = name if name != '' and name is not None else None
        self.environment_variables: Optional[str] = environment_variables if environment_variables != '' and environment_variables is not None else None
        self.id: Optional[int] = None
        self.reason: Optional[str] = None
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
            self.previous_step.next_step_uuid = self.uuid

        if self.next_step is not None:
            self.next_step_uuid = self.next_step.uuid
            self.next_step.previous_step = self
            self.next_step.previous_step_uuid = self.uuid

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
        export = '--export ALL' if self.environment_variables is None else f'--export ALL,{self.environment_variables}'
        qos = '' if self.qos is None else f'--qos {self.qos}'

        cmd = f'sbatch --account {self.account} --comment "Automatically queued by Genomic Pipeline: https://github.com/ManuelArcieri/GenomicPipeline" \
                {dependency} --error "./%j-err.txt" {export} {job_name} --mem {self.memory} --nodes {self.n_nodes} --ntasks {self.n_threads} \
                --output "./%j-out.txt" --partition {self.partition} {qos} --time "{self.max_run_time}" {self.script_file}' \
            .replace('                 ', ' ').replace('  ', ' ')

        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        out, err = process.communicate()
        ensure(process.returncode == 0, f'sbatch exited with error code {process.returncode}.\n\n'
                                        f'cmd = {cmd}\n\n'
                                        f'stderr = {err}\n\n'
                                        f'stdout = {out}\n\n')

        self.id = int(out.strip().split(' ')[-1])  # E.g. "Submitted batch job 1234"
        self.status = JobStatus.PENDING


    def get_pretty_name(self) -> str:
        if self.name is not None:
            return self.name
        return os.path.basename(self.script_file)


    def __dict__(self) -> dict:
        job = {}
        if self.name is not None and self.name != '':
            job['name'] = self.name
        job['uuid'] = self.uuid
        if self.id is not None:
            job['id'] = self.id
        job['status'] = self.status.name
        if self.reason is not None and self.reason != '':
            job['reason'] = self.reason
        job['script_file'] = self.script_file
        job['n_nodes'] = self.n_nodes
        job['n_threads'] = self.n_threads
        job['memory'] = self.memory
        job['account'] = self.account
        job['partition'] = self.partition
        if self.qos is not None and self.qos != '':
            job['qos'] = self.qos
        job['max_run_time'] = self.max_run_time
        if self.environment_variables is not None and self.environment_variables != '':
            job['environment_variables'] = self.environment_variables
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
                  environment_variables = values.get('environment_variables', None),
                  skip_file_check = values.get('skip_file_check', False))

        job.id = values.get('id', None)
        job.status = JobStatus(get_or_raise(values, 'status'))
        job.reason = values.get('reason', None)
        job.pipeline_step = values.get('pipeline_step', None)
        job.previous_step_uuid = values.get('previous_step_uuid', None)
        job.next_step_uuid = values.get('next_step_uuid', None)
        return job


# From: https://slurm.schedmd.com/sacct.html#SECTION_JOB-STATE-CODES
class JobStatus(Enum):
    BOOT_FAIL = 'BOOT_FAIL'  # Job terminated due to launch failure, typically due to a hardware failure (e.g. unable to boot the node or block and the job can not be requeued).
    CANCELLED = 'CANCELLED'  # Job was explicitly cancelled by the user or system administrator. The job may or may not have been initiated.
    COMPLETED = 'COMPLETED'  # Job has terminated all processes on all nodes with an exit code of zero.
    DEADLINE = 'DEADLINE'  # Job terminated on deadline.
    FAILED = 'FAILED'  # Job terminated with non-zero exit code or other failure condition.
    NODE_FAIL = 'NODE_FAIL'  # Job terminated due to failure of one or more allocated nodes.
    OUT_OF_MEMORY = 'OUT_OF_MEMORY'  # Job experienced out of memory error.
    PENDING = 'PENDING'  # Job is awaiting resource allocation.
    PREEMPTED = 'PREEMPTED'  # Job terminated due to preemption.
    RUNNING = 'RUNNING'  # Job currently has an allocation.
    REQUEUED = 'REQUEUED'  # Job was requeued.
    RESIZING = 'RESIZING'  # Job is about to change size.
    REVOKED = 'REVOKED'  # Sibling was removed from cluster due to other cluster starting the job.
    SUSPENDED = 'SUSPENDED'  # Job has an allocation, but execution has been suspended and CPUs have been released for other jobs.
    TIMEOUT = 'TIMEOUT'  # Job terminated upon reaching its time limit.
