"use strict";

import {get} from "svelte/store";
import * as stores from "./stores";
import {scripts} from "./bundledScripts";
import {Section, stringify} from "@ltd/j-toml";


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
    runMode = "once";

    const modal = document.getElementById("addJobModal");
    for (const element of modal.getElementsByClassName("form-control"))
        element.value = "";
    for (const element of modal.querySelectorAll("#dependenciesList input[type=checkbox]:checked"))
        element.checked = false;
}

export let pipelineName = "";
export let accountName = "";
export let workingDirectory = "";
export let logsDirectory = "";
export let samples = "";

export let jobName = "";
export let scriptType = "bundled";
export let bundledScriptFile = "barrier.sh";
export let scriptFile = "";
export let nodes = "";
export let threads = "";
export let memory = "";
export let runTime = "";
export let partition = "";
export let variables = "";
export let runMode = "once";


export function addJob()
{
    if (isEmpty(jobName)) {
        alert("Please enter a job name");
        return;
    }

    if (isEmpty(scriptFile) && scriptType === "custom") {
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
        scriptFile: scriptType === "bundled" ? bundledScriptFile : scriptFile,
        nodes,
        threads,
        memory,
        runTime,
        partition,
        variables,
        dependencies,
        runMode
    };

    stores.jobByUUID.update(contents => {
        contents[UUID] = newJob;
        return contents;
    });

    updateJobsByStep();
    collapseAllAccordions();
}

function isEmpty(string)
{
    return string.length <= 0;
}

function updateJobsByStep()
{
    const jobByUUID = get(stores.jobByUUID);
    const jobs = Array.from(Object.values(jobByUUID));
    if (Object.keys(jobByUUID).length === 0) {
        stores.jobsByStep.set([]);
        return;
    }

    for (const job of jobs)
        if (job.dependencies.length === 0)
            job.step = 0;
        else
            job.step = -1;

    let somethingChanged = true;
    let finalStep = -1;
    while (somethingChanged)
    {
        somethingChanged = false;
        for (const job of jobs)
            if (job.step === -1)
            {
                let maxStep = -1;
                for (const parentJob of getParentJobs(job, jobByUUID)) {
                    if (parentJob.step === -1) {
                        maxStep = -1;
                        break;
                    }
                    maxStep = Math.max(maxStep, parentJob.step);
                }

                if (maxStep !== -1) {
                    job.step = maxStep + 1;
                    finalStep = Math.max(finalStep, job.step);
                    somethingChanged = true;
                }
            } else {
                finalStep = Math.max(finalStep, job.step);
            }
    }

    let firstStep = 0;
    const jobByStep = new Map();
    for (const job of jobs) {
        let tempJobs = jobByStep.get(job.step);
        if (tempJobs === undefined)
            tempJobs = [];
        tempJobs.push(job);
        jobByStep.set(job.step, tempJobs);
        firstStep = Math.min(firstStep, job.step);
    }

    const jobsByStep = [];
    for (let i = firstStep; i <= finalStep; i++)
        jobsByStep.push([i, jobByStep.get(i)]);
    stores.jobsByStep.set(jobsByStep);

    updateDependencyCheckboxes();
    collapseAllAccordions();
}

function getParentJobs(job, jobByUUID)
{
    const parents = [];
    for (const uuid of job.dependencies)
        parents.push(jobByUUID[uuid]);
    return parents;
}

function collapseAllAccordions()
{
    for (let accordion of document.querySelectorAll(".accordion .collapse")) {
        const accordionInstance = bootstrap.Collapse.getInstance(accordion);
        if (accordionInstance !== null && accordionInstance !== undefined)
            accordionInstance.hide();
    }
}

function updateDependencyCheckboxes()
{
    const checkboxes = document.querySelectorAll(".accordion-item input[type=\"checkbox\"]");
    for (let checkbox of checkboxes) {
        const job = get(stores.jobByUUID)[checkbox.dataset.parent];
        const possibleDependency = get(stores.jobByUUID)[checkbox.value];
        checkbox.checked = !!job.dependencies.includes(possibleDependency.UUID);
    }
}

setInterval(updateDependencyCheckboxes, 700);

export function updateJobDependencies(event, parentJobUUID, relatedJobUUID)
{
    if (!event.isTrusted)
        return;

    const parentJob = get(stores.jobByUUID)[parentJobUUID];

    if (parentJob.dependencies.includes(relatedJobUUID))
        event.target.setAttribute("checked", "true");
    else
        event.target.removeAttribute("checked");

    if (event.target.checked) {
        if (!parentJob.dependencies.includes(relatedJobUUID)) {
            stores.jobByUUID.update((contents) => {
                const temp = contents[parentJobUUID]["dependencies"];
                temp.push(relatedJobUUID);
                contents[parentJobUUID]["dependencies"] = temp;
                return contents;
            });
            updateJobsByStep();
        }
    } else {
        if (parentJob.dependencies.includes(relatedJobUUID)) {
            stores.jobByUUID.update((contents) => {
                let temp = contents[parentJobUUID]["dependencies"];
                temp = temp.filter(uuid => uuid !== relatedJobUUID);
                contents[parentJobUUID]["dependencies"] = temp;
                return contents;
            });
            updateJobsByStep();
        }
    }
}

export function generatePipeline()
{
    const jobsByStep = get(stores.jobsByStep);
    if (jobsByStep.length === 0) {
        alert("You need to create at least one job");
        return;
    }

    if (isEmpty(pipelineName) || isEmpty(accountName) || isEmpty(workingDirectory) || isEmpty(logsDirectory)) {
        alert("Please specify the runtime environment for the pipeline");
        return;
    }

    const splitSamples = samples.trim().split("\n");

    let jobSections = [];
    let parallelJobsUUIDs = {};
    for (let stepList of jobsByStep)
        for (let job of stepList[1]) {
            let table = {
                "name": job.jobName,
                "uuid": job.UUID,
                "status": "PENDING",
                "script_file": job.scriptFile,
                "n_nodes": Number(job.nodes),
                "n_threads": Number(job.threads),
                "memory": job.memory,
                "account": accountName,
                "partition": job.partition,
                "logs_directory": logsDirectory,
                "max_run_time": job.runTime,
                "environment_variables": [`GEP_WD="${workingDirectory}"`, `GEP_JOB_NAME="${job.jobName}"`, `GEP_SCRIPT_FILE="${job.scriptFile}"`,
                                          `GEP_N_NODES="${job.nodes}"`, `GEP_N_THREADS="${job.threads}"`, `GEP_MEMORY="${job.memory}"`,
                                          `GEP_MAX_RUNTIME="${job.runTime}"`, `GEP_SLURM_PARTITION="${job.partition}"`, `GEP_EXEC_POLICY="${job.runMode}"`].join(","),
                "pipeline_step": stepList[0]
            };

            if (!isEmpty(job.variables))
                table["environment_variables"] = `${table["environment_variables"]},${job.variables}`;

            if (job.dependencies.length > 0)
                table["previous_steps_uuid"] = job.dependencies.join(",");

            if (job.runMode === "forEachSample") {
                for (let sample of splitSamples) {
                    let newTable = {...table};
                    const newUUID = self.crypto.randomUUID();
                    newTable["uuid"] = newUUID;
                    newTable["name"] = newTable["name"].replace("$GEP_SAMPLE", sample);
                    newTable["script_file"] = newTable["script_file"].replace("$GEP_SAMPLE", sample);
                    newTable["environment_variables"] = `GEP_SAMPLE="${sample}",${newTable["environment_variables"]}`;

                    let realDependencies = [];
                    if (job.dependencies.length > 0) {
                        for (let parentUUID of job.dependencies) {
                            const parentMap = parallelJobsUUIDs[parentUUID];
                            if (parentMap !== undefined)
                                realDependencies.push(parentMap[sample]);
                            else
                                realDependencies.push(parentUUID);
                        }
                    }

                    if (realDependencies.length > 0)
                        newTable["previous_steps_uuid"] = realDependencies.join(",");

                    const previousJobs = parallelJobsUUIDs[job.UUID];
                    if (previousJobs !== undefined)
                        parallelJobsUUIDs[job.UUID][sample] = newUUID;
                    else {
                        const newObj = {};
                        newObj[sample] = newUUID;
                        parallelJobsUUIDs[job.UUID] = newObj;
                    }

                    jobSections.push(Section(newTable));
                }
            } else {
                let realDependencies = [];
                if (job.dependencies.length > 0) {
                    for (let parentUUID of job.dependencies) {
                        const parentMap = parallelJobsUUIDs[parentUUID];
                        if (parentMap !== undefined)
                            for (let value of Object.values(parentMap))
                                realDependencies.push(value);
                        else
                            realDependencies.push(parentUUID);
                    }
                }

                if (realDependencies.length > 0)
                    table["previous_steps_uuid"] = realDependencies.join(",");

                jobSections.push(Section(table));
            }
        }

    let toml = stringify({
        "epoch": Date.now(),
        "pipeline": Section({
            "name": pipelineName,
            "size": jobsByStep[jobsByStep.length - 1][0] + 1,
            "working_directory": workingDirectory,
            "logs_directory": logsDirectory,
            "jobs": jobSections
        })
    }, {newline: "\n", newlineAround: "section", integer: Number.MAX_SAFE_INTEGER});

    toml = `# Auto-generated by Genomic Pipeline\n# https://github.com/ManuelArcieri/GenomicPipeline\n\n${toml}`;

    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(toml));
    element.setAttribute("download", "pipeline.toml");
    element.style.display = "none";

    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

export function checkJobEnvVariables()
{
    if (scriptType === "custom")
        return;

    for (let item of scripts) {
        if (item.file === bundledScriptFile) {
            const envVars = item.envVariables;
            variables = isEmpty(envVars) ? "" : envVars;
            return;
        }
    }
}

export function loadExample()
{
    if (self?.crypto?.randomUUID === undefined) {
        alert("Crypto module unavailable, cannot proceed");
        console.error("Crypto module unavailable, cannot proceed");
        return;
    }

    stores.jobByUUID.set({});
    stores.jobsByStep.set([]);

    pipelineName = "Sample pipeline";
    document.getElementById("pipelineNameInput").value = "Sample pipeline";
    accountName = "your-account";
    document.getElementById("accountInput").value = "your-account";
    workingDirectory = "$SCRATCH/sample";
    document.getElementById("workingDirectoryInput").value = "$SCRATCH/sample";
    logsDirectory = "$SCRATCH/sample/logs";
    document.getElementById("logsDirectoryInput").value = "$SCRATCH/sample/logs";
    samples = "SRR8615264\nSRR8615268\nSRR8615270\nSRR8615232\nSRR8615233\nSRR8615238";
    document.getElementById("samplesInput").value = "SRR8615264\nSRR8615268\nSRR8615270\nSRR8615232\nSRR8615233\nSRR8615238";

    const jobByUUID = {};

    const prefetchUUID = self.crypto.randomUUID();
    jobByUUID[prefetchUUID] = {
        UUID: prefetchUUID,
        step: -1,
        jobName: "Prefetch $GEP_SAMPLE",
        scriptFile: "sra-prefetch.sh",
        nodes: 1,
        threads: 1,
        memory: "8GB",
        runTime: "4:00:00",
        partition: "g100_all_serial",
        variables: "",
        dependencies: [],
        runMode: "forEachSample"
    };

    const fastqDumpUUID = self.crypto.randomUUID();
    jobByUUID[fastqDumpUUID] = {
        UUID: fastqDumpUUID,
        step: -1,
        jobName: "fastq-dump $GEP_SAMPLE",
        scriptFile: "fastq-dump-PE.sh",
        nodes: 1,
        threads: 4,
        memory: "8GB",
        runTime: "4:00:00",
        partition: "g100_all_serial",
        variables: "",
        dependencies: [prefetchUUID],
        runMode: "forEachSample"
    };

    const fastqc1UUID = self.crypto.randomUUID();
    jobByUUID[fastqc1UUID] = {
        UUID: fastqc1UUID,
        step: -1,
        jobName: "FastQC $GEP_SAMPLE (1)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/FASTQ/$GEP_SAMPLE\"_1.fastq",
        dependencies: [fastqDumpUUID],
        runMode: "forEachSample"
    };

    const fastqc2UUID = self.crypto.randomUUID();
    jobByUUID[fastqc2UUID] = {
        UUID: fastqc2UUID,
        step: -1,
        jobName: "FastQC $GEP_SAMPLE (2)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/FASTQ/$GEP_SAMPLE\"_2.fastq",
        dependencies: [fastqDumpUUID],
        runMode: "forEachSample"
    };

    const trimUUID = self.crypto.randomUUID();
    jobByUUID[trimUUID] = {
        UUID: trimUUID,
        step: -1,
        jobName: "Trim $GEP_SAMPLE",
        scriptFile: "trimmomatic-PE.sh",
        nodes: 1,
        threads: 36,
        memory: "128GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "",
        dependencies: [fastqDumpUUID],
        runMode: "forEachSample"
    };

    const fastqc3UUID = self.crypto.randomUUID();
    jobByUUID[fastqc3UUID] = {
        UUID: fastqc3UUID,
        step: -1,
        jobName: "FastQC trimmed $GEP_SAMPLE (paired, 1)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/trimmed/$GEP_SAMPLE\"_1.trimmed.paired.fastq",
        dependencies: [trimUUID],
        runMode: "forEachSample"
    };

    const fastqc4UUID = self.crypto.randomUUID();
    jobByUUID[fastqc4UUID] = {
        UUID: fastqc4UUID,
        step: -1,
        jobName: "FastQC trimmed $GEP_SAMPLE (paired, 2)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/trimmed/$GEP_SAMPLE\"_2.trimmed.paired.fastq",
        dependencies: [trimUUID],
        runMode: "forEachSample"
    };

    const fastqc5UUID = self.crypto.randomUUID();
    jobByUUID[fastqc5UUID] = {
        UUID: fastqc5UUID,
        step: -1,
        jobName: "FastQC trimmed $GEP_SAMPLE (unpaired, 1)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/trimmed/$GEP_SAMPLE\"_1.trimmed.unpaired.fastq",
        dependencies: [trimUUID],
        runMode: "forEachSample"
    };

    const fastqc6UUID = self.crypto.randomUUID();
    jobByUUID[fastqc6UUID] = {
        UUID: fastqc6UUID,
        step: -1,
        jobName: "FastQC trimmed $GEP_SAMPLE (unpaired, 2)",
        scriptFile: "fastqc.sh",
        nodes: 1,
        threads: 6,
        memory: "32GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "FASTQ_FILE=\"$GEP_WD/trimmed/$GEP_SAMPLE\"_2.trimmed.unpaired.fastq",
        dependencies: [trimUUID],
        runMode: "forEachSample"
    };

    const mapUUID = self.crypto.randomUUID();
    jobByUUID[mapUUID] = {
        UUID: mapUUID,
        step: -1,
        jobName: "Mapping $GEP_SAMPLE",
        scriptFile: "hisat2-mapping-PE.sh",
        nodes: 1,
        threads: 36,
        memory: "256GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "",
        dependencies: [trimUUID],
        runMode: "forEachSample"
    };

    const sortUUID = self.crypto.randomUUID();
    jobByUUID[sortUUID] = {
        UUID: sortUUID,
        step: -1,
        jobName: "Sorting $GEP_SAMPLE",
        scriptFile: "samtools-sort.sh",
        nodes: 1,
        threads: 36,
        memory: "128GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "",
        dependencies: [mapUUID],
        runMode: "forEachSample"
    };

    const stringTieUUID = self.crypto.randomUUID();
    jobByUUID[stringTieUUID] = {
        UUID: stringTieUUID,
        step: -1,
        jobName: "StringTie $GEP_SAMPLE",
        scriptFile: "stringtie.sh",
        nodes: 1,
        threads: 36,
        memory: "256GB",
        runTime: "24:00:00",
        partition: "g100_usr_prod",
        variables: "",
        dependencies: [sortUUID],
        runMode: "forEachSample"
    };

    stores.jobByUUID.set(jobByUUID);
    updateJobsByStep();
    collapseAllAccordions();
}
