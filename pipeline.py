from job import Job
from typing import Optional, Iterable
from utility import ensure


class Pipeline:
    def __init__(self, jobs: Iterable[Job]):
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
            raise AssertionError("you cannot run an already executed pipeline")

        for _ in range(self.size):
            self.run_next_step()


    def run_next_step(self):
        if self.step is not None and self.step == self.size - 1:
            raise AssertionError("all steps of the pipeline were already executed")

        self.step = 0 if self.step is None else self.step + 1
        for job in self.jobs_per_step[self.step]:
            job.run()
