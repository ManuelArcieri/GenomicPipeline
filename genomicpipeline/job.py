import os.path
import subprocess
from enum import Enum
from sys import stderr
from typing import Optional
from utility import ensure, get_or_raise, GEP_FOLDER


class Job:
    def __init__(self, *, uuid: str, script_file: str, memory: str, account: str, partition: str, max_run_time: str,
                 qos = None, n_nodes: int, n_threads: int, name, environment_variables = None, skip_file_check = False, previous_steps = None):
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
        self.previous_steps: dict[str, Job] = previous_steps if previous_steps is not None else {}
        self.logs_directory = '.'

        self._check_parameters()


    def _check_parameters(self):
        if not self.skip_file_check:
            ensure(self._script_file_exists(), f'the script file does not exist: "{self.script_file}"')

        ensure(self.memory[0].isnumeric(), f'the memory value "{self.memory}" does not start with a number')
        ensure(self.memory[-1] in ('K', 'M', 'G', 'T') or self.memory[-2:] in ('KB', 'MB', 'GB', 'TB') or self.memory[-1].isnumeric(),
               f'the memory value "{self.memory}" does not end with a valid suffix (K|M|G|T)')
        ensure(len(self.account) > 0, 'the account is undefined')
        ensure(len(self.partition) > 0, 'the partition is undefined')
        ensure(len(self.max_run_time) > 0, 'the maximum run time is undefined')
        ensure(self.n_nodes > 0, f'the number of nodes must be greater than zero (found: {self.n_nodes})')
        ensure(self.n_threads > 0, f'the number of threads must be greater than zero (found: {self.n_nodes})')


    def _script_file_exists(self) -> bool:
        if self._get_real_script_file() is not None:
            return True
        return False


    def _get_real_script_file(self) -> Optional[str]:
        if os.path.isfile(self.script_file):
            return self.script_file

        alternative_file = os.path.join(GEP_FOLDER, 'jobs', self.script_file)
        if os.path.isfile(alternative_file):
            return alternative_file

        return None


    def run(self):
        ensure(self._script_file_exists(), f'the script file does not exist: "{self.script_file}"')
        script_file = self._get_real_script_file()
        previous_ids = [str(i.id) for i in self.previous_steps.values()]
        dependency = '' if len(previous_ids) == 0 else f'--dependency afterok:{":".join(previous_ids)}'
        job_name = '' if self.name is None else f'--job-name "{self.name}"'
        logs = os.path.expandvars(os.path.join(self.logs_directory, self.uuid))
        print(logs)
        export = '--export ALL' if self.environment_variables is None else f'--export ALL,{self.environment_variables}'
        qos = '' if self.qos is None else f'--qos {self.qos}'

        cmd = f'sbatch --account {self.account} --comment "Automatically queued by Genomic Pipeline: https://github.com/ManuelArcieri/GenomicPipeline | UUID: {self.uuid}" \
                {dependency} --error "{logs}-err.txt" {export} {job_name} --mem {self.memory} --nodes {self.n_nodes} --ntasks {self.n_threads} \
                --output "{logs}-out.txt" --partition {self.partition} {qos} --requeue --time "{self.max_run_time}" {script_file}' \
            .replace('                 ', ' ').replace('  ', ' ')
        print(cmd)

        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        out, err = process.communicate()
        ensure(process.returncode == 0, f'sbatch exited with error code {process.returncode}.\n\n'
                                        f'cmd = {cmd}\n\n'
                                        f'stderr = {err}\n\n'
                                        f'stdout = {out}\n\n')

        self.id = int(out.strip().split(' ')[-1])  # E.g. "Submitted batch job 1234"
        self.status = JobStatus.PENDING


    def requeue(self):
        ensure(self.id is not None, 'tried to restart a job with an invalid ID')

        cmd = f'scontrol requeue {self.id}'
        process = subprocess.Popen(cmd, shell = True)

        if process.wait() == 0:
            self.status = JobStatus.PENDING
        else:
            print(f'Failed to requeue job {self.id} ({self.uuid})', file = stderr)


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
        job['logs_directory'] = self.logs_directory
        if self.qos is not None and self.qos != '':
            job['qos'] = self.qos
        job['max_run_time'] = self.max_run_time
        if self.environment_variables is not None and self.environment_variables != '':
            job['environment_variables'] = self.environment_variables
        if self.pipeline_step is not None:
            job['pipeline_step'] = self.pipeline_step
        if self.skip_file_check:
            job['skip_file_check'] = self.skip_file_check
        if len(self.previous_steps) > 0:
            job['previous_steps_uuid'] = ','.join(self.previous_steps.keys())
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
        job.logs_directory = values.get('logs_directory', '.')
        previous_steps_uuid = values.get('previous_steps_uuid', '').split(',')
        job.previous_steps = {u: None for u in previous_steps_uuid if u != ''}
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
