"use strict";

export function clearForm()
{
    jobName = "";
    scriptFile = "";
    nodes = "";
    threads = "";
    memory = "";
    runTime = "";
    partition = "";

    const modal = document.getElementById("addJobModal");
    for (const element of modal.getElementsByClassName("form-control"))
        element.value = "";
}


export let jobs = [];

export let jobName = "";
export let scriptFile = "";
export let nodes = "";
export let threads = "";
export let memory = "";
export let runTime = "";
export let partition = "";

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
        alert("Crypto module unavailable");
        return;
    }

    const uuid = self.crypto.randomUUID();
    jobs.push({UUID: uuid, step: -1, jobName, scriptFile, nodes, threads, memory, runTime, partition});
}

function isEmpty(string)
{
    return string.length <= 0;
}
