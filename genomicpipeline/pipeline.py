import json
import os
import os.path
import subprocess
from datetime import datetime, timezone
from job import Job, JobStatus
from tomlkit import load, document, item, aot, comment, nl, table, dump
from typing import Optional, Collection
from utility import *


class Pipeline:
    def __init__(self, name: str, jobs: Collection[Job], working_directory: str):
        self.name = name
        self.jobs_per_step: dict[int, list[Job]] = {}
        self.step_per_job: dict[Job, int] = {}
        self.step: Optional[int] = None
        self.working_directory = working_directory
        self.logs_directory = os.path.join(working_directory, 'logs')
        self.size = 0

        self._build_pipeline(jobs)


    def _build_pipeline(self, jobs: Collection[Job]):
        while len(self.step_per_job) < len(jobs):
            for job in jobs:
                job.logs_directory = self.logs_directory

                if job.pipeline_step is None:
                    if len(job.previous_steps) == 0:
                        step = 0
                        job.pipeline_step = step
                    elif any(map(lambda j: True if j.pipeline_step is None else False, job.previous_steps.values())):
                        continue
                    else:
                        step = -1
                        for j in job.previous_steps.values():
                            step = max(step, j.pipeline_step)
                        step += 1
                        job.pipeline_step = step
                else:
                    step = job.pipeline_step

                self.step_per_job[job] = step
                temp = self.jobs_per_step.get(step, [])
                if job not in temp:
                    temp.append(job)
                    self.jobs_per_step[step] = temp
                self.size = max(self.size, step + 1)

        ensure(all(map(lambda j: True if j.pipeline_step is not None else False, jobs)),
               'some jobs of the pipeline were not queued for execution', AssertionError)


    def run_entire_pipeline(self):
        start = 0 if self.step is None else self.step + 1
        for _ in range(start, self.size):
            self.run_next_step()


    def run_next_step(self):
        if self.step is not None and self.step == self.size - 1:
            print("All steps of the pipeline were already executed")
            exit()

        self.step = 0 if self.step is None else self.step + 1
        for job in self.jobs_per_step[self.step]:
            job.run()


    def update_jobs_status(self):
        queued_jobs = {j.id: j for j in self.step_per_job.keys() if j.id is not None}
        if len(queued_jobs) <= 0:
            return

        ids = ','.join([str(i.id) for i in queued_jobs.values()])
        cmd = f'sacct -j {ids} --json'
        process = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)

        out, err = process.communicate()
        ensure(process.returncode == 0, f'sacct exited with error code {process.returncode}.\n\n'
                                        f'cmd = {cmd}\n\n'
                                        f'stderr = {err}\n\n'
                                        f'stdout = {out}\n\n')

        data = json.loads(out)
        for job_data in data['jobs']:
            job_id = job_data['job_id']
            status = JobStatus(job_data['state']['current'])
            reason = job_data['state']['reason']
            reason = reason if reason != 'None' else None

            job = queued_jobs[job_id]
            job.status = status
            job.reason = reason
            job.current_run_time = get_user_friendly_time(job_data['time']['start'], job_data['time']['end'])


    def print_jobs_table(self):
        print(f'\n[{self.name}] Step {(self.step if self.step is not None else 0) + 1}/{self.size}')

        for step in range(self.size):
            print('|\n|')
            print(f'(Step {step + 1})')

            for job in self.jobs_per_step[step]:
                env = job.environment_variables
                if env is not None:
                    env = [e for e in env.split(',') if not e.startswith('GEP_')]
                    env = ','.join(env)

                print('|\n|')
                print(f'+---+--- Job: {job.get_pretty_name()} ({job.id if job.id is not None else "-"})')
                print(f'|   +--- Status: {job.status.value}{(" (" + job.reason + ")") if job.reason is not None else ""}')
                print(f'|   +--- Run time: {job.current_run_time if job.current_run_time is not None else "-"}')
                print(f'|   +--- Env: {env if env is not None else "-"}')
                print(f'|   +--- UUID: {job.uuid}')
        print()


    def requeue_failed_jobs(self):
        failed_jobs = 0
        js = JobStatus
        for job in self.step_per_job.keys():
            if job.status in (js.BOOT_FAIL, js.CANCELLED, js.DEADLINE, js.FAILED, js.NODE_FAIL, js.OUT_OF_MEMORY, js.PREEMPTED, js.TIMEOUT):
                job.requeue()
                failed_jobs += 1
        print(f'Requeued {failed_jobs} jobs')


    def save_to_toml_file(self, path: str):
        doc = document()
        doc.add(comment('Auto-generated by Genomic Pipeline'))
        doc.add(comment('https://github.com/ManuelArcieri/GenomicPipeline'))
        doc.add(nl())
        doc.add('timestamp', datetime.now(timezone.utc))
        doc.add(nl())

        pipeline = table()
        pipeline.add('name', self.name)
        if self.step is not None:
            pipeline.add('step', self.step)
        pipeline.add('size', self.size)
        pipeline.add('working_directory', self.working_directory)
        pipeline.add('logs_directory', self.logs_directory)

        jobs = aot()


        def job_key(j: Job):
            return j.pipeline_step if j.pipeline_step is not None else 0


        for job in sorted(self.step_per_job.keys(), key = job_key):
            jobs.append(item(job.__dict__()))

        pipeline.add('jobs', jobs)
        doc.add('pipeline', pipeline)

        with open(path, 'w') as file:
            dump(doc, file)


    @staticmethod
    def load_from_toml_file(path: str):
        with open(path) as file:
            root = load(file)

        pipeline = get_or_raise(root, 'pipeline')
        name = get_or_raise(pipeline, 'name')
        working_directory = get_or_raise(pipeline, 'working_directory')

        raw_jobs = get_or_raise(pipeline, 'jobs')
        jobs_obj = [Job.from_dict(j) for j in raw_jobs]
        uuid_per_job = {j.uuid: j for j in jobs_obj}

        for job in jobs_obj:
            for previous_job_uuid in job.previous_steps.keys():
                job.previous_steps[previous_job_uuid] = get_or_raise(uuid_per_job, previous_job_uuid)

        pipeline_obj = Pipeline(name, jobs_obj, working_directory)
        step = pipeline.get('step', None)
        if step is not None:
            pipeline_obj.step = step
        pipeline_obj.size = get_or_raise(pipeline, 'size')
        pipeline.logs_directory = get_or_raise(pipeline, 'logs_directory')
        return pipeline_obj
