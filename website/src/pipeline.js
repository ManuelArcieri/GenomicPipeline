"use strict";

import {get} from "svelte/store";
import * as stores from "./stores";

export function clearForm()
{
    jobName = "";
    scriptFile = "";
    nodes = "";
    threads = "";
    memory = "";
    runTime = "";
    partition = "";
    variables = "";

    const modal = document.getElementById("addJobModal");
    for (const element of modal.getElementsByClassName("form-control"))
        element.value = "";
    for (const element of modal.querySelectorAll("#dependenciesList input[type=checkbox]:checked"))
        element.checked = false;
}

export let jobName = "";
export let scriptFile = "";
export let nodes = "";
export let threads = "";
export let memory = "";
export let runTime = "";
export let partition = "";
export let variables = "";

export function addJob()
{
    if (isEmpty(jobName)) {
        alert("Please enter a job name");
        return;
    }

    if (isEmpty(scriptFile)) {
        alert("Please enter a script file");
        return;
    }

    if (isEmpty(nodes)) {
        alert("Please enter the number of nodes");
        return;
    }

    if (isEmpty(threads)) {
        alert("Please enter the number of threads");
        return;
    }

    if (isEmpty(memory)) {
        alert("Please enter the amount of memory");
        return;
    }

    if (isEmpty(runTime)) {
        alert("Please enter the maximum run time");
        return;
    }

    if (isEmpty(partition)) {
        alert("Please enter the Slurm partition");
        return;
    }

    createJob();
    bootstrap.Modal.getInstance(document.getElementById("addJobModal")).hide();
    clearForm();
}

function createJob() {
    if (self?.crypto?.randomUUID === undefined) {
        alert("Crypto module unavailable, cannot proceed");
        console.error("Crypto module unavailable, cannot proceed");
        return;
    }

    const UUID = self.crypto.randomUUID();
    const dependencies = [];
    for (const element of document.querySelectorAll("#dependenciesList input[type=checkbox]:checked"))
        dependencies.push(element.value);

    const newJob = {
        UUID,
        step: -1,
        jobName,
        scriptFile,
        nodes,
        threads,
        memory,
        runTime,
        partition,
        variables,
        dependencies
    };

    stores.jobs.update(contents => [...contents, newJob]);
    stores.jobByUUID.update(contents => {
        contents[UUID] = newJob;
        return contents;
    });
}

function isEmpty(string)
{
    return string.length <= 0;
}

function getJobsByStep()
{
    const jobs = get(stores.jobs);
    const jobByUUID = get(stores.jobByUUID);

    for (const job of jobs)
        if (job.dependencies.length === 0)
            job.step = 0;

    let somethingChanged = true;
    while (somethingChanged)
    {
        somethingChanged = false;
        for (const job of jobs)
            if (job.step !== -1)
                for (const previousJob of job.dependencies)
                    if (job.dependencies.length === 0)
                        job.step = 0;
    }
}
