from datetime import datetime, timezone
from job import Job
from tomlkit import load, document, item, aot, comment, nl, table, dump
from typing import Optional, Iterable
from utility import ensure, get_or_raise


class Pipeline:
    def __init__(self, name: str, jobs: Iterable[Job]):
        self.name = name
        self.jobs_per_step: dict[int, list[Job]] = {}
        self.step_per_job: dict[Job, int] = {}
        self.step: Optional[int] = None
        self.size = 0

        self._build_pipeline(jobs)


    def _build_pipeline(self, jobs: Iterable[Job]):
        is_running = True
        while is_running:
            is_running = False
            for job in jobs:
                if job.pipeline_step is None:
                    if job.previous_step is None:
                        step = 0
                    elif job.previous_step.pipeline_step is None:
                        continue
                    else:
                        step = job.previous_step.pipeline_step + 1

                    job.pipeline_step = step
                    self.step_per_job[job] = step
                    temp = self.jobs_per_step.get(step, [])
                    temp.append(job)
                    self.jobs_per_step[step] = temp
                    self.size = max(self.size, step + 1)
                    is_running = True

        ensure(all(map(lambda j: True if j.pipeline_step is not None else False, jobs)),
               'some jobs of the pipeline were not queued for execution', AssertionError)


    def run_entire_pipeline(self):
        if self.step is not None:
            raise RuntimeError("you cannot run an already executed pipeline")

        for _ in range(self.size):
            self.run_next_step()


    def run_next_step(self):
        if self.step is not None and self.step == self.size - 1:
            raise RuntimeError("all steps of the pipeline were already executed")

        self.step = 0 if self.step is None else self.step + 1
        for job in self.jobs_per_step[self.step]:
            job.run()


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

        raw_jobs = get_or_raise(pipeline, 'jobs')
        jobs_obj = [Job.from_dict(j) for j in raw_jobs]
        uuid_per_job = {j.uuid: j for j in jobs_obj}

        for job in jobs_obj:
            if job.previous_step_uuid is not None and job.previous_step_uuid != '':
                job.previous_step = get_or_raise(uuid_per_job, job.previous_step_uuid)
            if job.next_step_uuid is not None and job.next_step_uuid != '':
                job.next_step_uuid = get_or_raise(uuid_per_job, job.next_step_uuid)

        pipeline_obj = Pipeline(name, jobs_obj)
        step = pipeline.get('step', None)
        if step is not None:
            pipeline_obj.step = step
        pipeline_obj.size = get_or_raise(pipeline, 'size')
        return pipeline_obj
