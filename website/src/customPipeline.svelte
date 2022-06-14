<script>
    "use strict";

    import * as pipeline from "./pipeline";
    import {jobByUUID, jobsByStep} from "./stores";
    import {afterUpdate} from "svelte";

    let pipelineName = "";
    let accountName = "";
    let workingDirectory = "";
    let logsDirectory = "";
    let samples = "";

    afterUpdate(() => {
        pipeline.updateDependencyCheckboxes();
    });
</script>

<div class="container-fluid">
    <div class="section-caption">
        <span>Runtime environment</span>
    </div>

    <div class="row">
        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="pipelineNameInput" bind:value={pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                <label for="pipelineNameInput">Pipeline name</label>
            </div>
        </div>

        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="accountInput" bind:value={accountName} class="form-control" placeholder="Account (Slurm)" minlength="1" spellcheck="true" required>
                <label for="accountInput">Account (Slurm)</label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="workingDirectoryInput" bind:value={workingDirectory} class="form-control" placeholder="Working directory" minlength="1" spellcheck="true" required>
                <label for="workingDirectoryInput">Working directory</label>
            </div>
        </div>

        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="logsDirectoryInput" bind:value={logsDirectory} class="form-control" placeholder="Logs directory" minlength="1" spellcheck="true" required>
                <label for="logsDirectoryInput">Logs directory</label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="form-floating">
                <textarea id="samplesInput" bind:value={samples} class="form-control" placeholder="Samples (one per line)" minlength="1" autocomplete="off" spellcheck="false" wrap="soft" required></textarea>
                <label for="samplesInput">Samples (one per line)</label>
            </div>
        </div>
    </div>

    <div class="section-caption">
        <span>Jobs</span>
    </div>

    <div class="row">
        <div class="col text-center">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addJobModal"><span class="material-symbols-rounded">add</span> Add new job</button>
        </div>
    </div>

    {#each $jobsByStep as i_jobs}
        <div class="section-caption">
            <span>Step {i_jobs[0] + 1}</span>
        </div>

        <div class="row">
            <div class="accordion" id="step{i_jobs[0]}Accordion">

                {#each i_jobs[1] as job}
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading{job.UUID}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{job.UUID}">
                                {$jobByUUID[job.UUID]["jobName"]}
                            </button>
                        </h2>

                        <div id="collapse{job.UUID}" class="accordion-collapse collapse" data-bs-parent="#step{i_jobs[0]}Accordion">
                            <div class="accordion-body">
                                <div class="row">
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["jobName"]} class="form-control" placeholder="Job Name" minlength="1" spellcheck="true" required>
                                            <label for="JobNameInput">Job name</label>
                                        </div>
                                    </div>

                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["scriptFile"]} class="form-control" placeholder="Script file" minlength="1" spellcheck="true" required>
                                            <label for="scriptFileInput">Script file</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["nodes"]} class="form-control" placeholder="Number of nodes" minlength="1" spellcheck="true" required>
                                            <label for="nodesInput">Number of nodes</label>
                                        </div>
                                    </div>

                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["threads"]} class="form-control" placeholder="Number of threads" minlength="1" spellcheck="true" required>
                                            <label for="threadsInput">Number of threads</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["memory"]} class="form-control" placeholder="Memory" minlength="1" spellcheck="true" required>
                                            <label for="memoryInput">Memory</label>
                                        </div>
                                    </div>

                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["runTime"]} class="form-control" placeholder="Maximum run time" minlength="1" spellcheck="true" required>
                                            <label for="runTimeInput">Maximum run time</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["partition"]} class="form-control" placeholder="Slurm partition" minlength="1" spellcheck="true" required>
                                            <label for="partitionInput">Slurm partition</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-12">
                                        <div class="form-floating">
                                            <input type="text" bind:value={$jobByUUID[job.UUID]["variables"]} class="form-control" placeholder="Environment variables (comma separated)" spellcheck="true" required>
                                            <label for="partitionInput">Environment variables (comma separated)</label>
                                        </div>
                                    </div>
                                </div>

                                <div class="section-caption">
                                    <span>Dependencies</span>
                                </div>

                                <div class="row">
                                    <div class="col-12">
                                        <div class="form-floating">
                                            <ul class="list-group">
                                                {#each Array.from(Object.values($jobByUUID)) as jobBis}
                                                    {#if job.UUID !== jobBis.UUID}
                                                        <li class="list-group-item">
                                                            <input on:change={(event) => {pipeline.updateJobDependencies(event, job.UUID, jobBis.UUID)}} class="form-check-input me-1" type="checkbox" value="{jobBis.UUID}" data-parent="{job.UUID}">
                                                            {jobBis.jobName}
                                                        </li>
                                                    {/if}
                                                {/each}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>

<div class="modal fade" id="addJobModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Add new job</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>

            <div class="modal-body">
                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="JobNameInput" bind:value={pipeline.jobName} class="form-control" placeholder="Job Name" minlength="1" spellcheck="true" required>
                            <label for="JobNameInput">Job name</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="scriptFileInput" bind:value={pipeline.scriptFile} class="form-control" placeholder="Script file" minlength="1" spellcheck="true" required>
                            <label for="scriptFileInput">Script file</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="nodesInput" bind:value={pipeline.nodes} class="form-control" placeholder="Number of nodes" minlength="1" spellcheck="true" required>
                            <label for="nodesInput">Number of nodes</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="threadsInput" bind:value={pipeline.threads} class="form-control" placeholder="Number of threads" minlength="1" spellcheck="true" required>
                            <label for="threadsInput">Number of threads</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="memoryInput" bind:value={pipeline.memory} class="form-control" placeholder="Memory" minlength="1" spellcheck="true" required>
                            <label for="memoryInput">Memory</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="runTimeInput" bind:value={pipeline.runTime} class="form-control" placeholder="Maximum run time" minlength="1" spellcheck="true" required>
                            <label for="runTimeInput">Maximum run time</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="partitionInput" bind:value={pipeline.partition} class="form-control" placeholder="Slurm partition" minlength="1" spellcheck="true" required>
                            <label for="partitionInput">Slurm partition</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12">
                        <div class="form-floating">
                            <input type="text" id="variablesInput" bind:value={pipeline.variables} class="form-control" placeholder="Environment variables (comma separated)" spellcheck="true" required>
                            <label for="partitionInput">Environment variables (comma separated)</label>
                        </div>
                    </div>
                </div>

                <div class="section-caption">
                    <span>Dependencies</span>
                </div>

                <div class="row">
                    <div class="col-12">
                        <div class="form-floating">
                            <ul id="dependenciesList" class="list-group">
                                {#each Array.from(Object.values($jobByUUID)) as job}
                                    <li class="list-group-item">
                                        <input class="form-check-input me-1" type="checkbox" value="{job.UUID}">
                                        {job.jobName}
                                    </li>
                                {/each}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" on:click={pipeline.clearForm} class="btn btn-secondary">Clear form</button>
                <button type="button" on:click={pipeline.addJob} class="btn btn-primary">Add</button>
            </div>
        </div>
    </div>
</div>

