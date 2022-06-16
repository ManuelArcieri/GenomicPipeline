<script>
    import * as pipeline from "./pipeline";
    import {jobByUUID, jobsByStep} from "./stores";
</script>


<div class="container-fluid section-container">
    <div class="top-caption">
        <img class="top-logo" src="img/icon.png" alt="Genomic Pipeline icon">
        <span class="margin-left-small">Genomic Pipeline</span>
    </div>

    <div class="container-fluid">
        <div class="section-caption">
            <span>Runtime environment</span>
        </div>

        <div class="row">
            <div class="col-6">
                <div class="form-floating">
                    <input type="text" id="pipelineNameInput" bind:value={pipeline.pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                    <label for="pipelineNameInput">Pipeline name</label>
                </div>
            </div>

            <div class="col-6">
                <div class="form-floating">
                    <input type="text" id="accountInput" bind:value={pipeline.accountName} class="form-control" placeholder="Account (Slurm)" minlength="1" spellcheck="true" required>
                    <label for="accountInput">Account (Slurm)</label>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-6">
                <div class="form-floating">
                    <input type="text" id="workingDirectoryInput" bind:value={pipeline.workingDirectory} class="form-control" placeholder="Working directory ($GEP_WD)" minlength="1" spellcheck="true" required>
                    <label for="workingDirectoryInput">Working directory ($GEP_WD)</label>
                </div>
            </div>

            <div class="col-6">
                <div class="form-floating">
                    <input type="text" id="logsDirectoryInput" bind:value={pipeline.logsDirectory} class="form-control" placeholder="Logs directory" minlength="1" spellcheck="true" required>
                    <label for="logsDirectoryInput">Logs directory</label>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="form-floating">
                    <textarea id="samplesInput" bind:value={pipeline.samples} class="form-control" placeholder="Samples (one per line)" minlength="1" autocomplete="off" spellcheck="false" wrap="soft" required></textarea>
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
                {#if i_jobs[0] === -1}
                    <span class="error-color">Invalid dependencies</span>
                {:else}
                    <span>Step {i_jobs[0] + 1}</span>
                {/if}
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
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["jobName"]} class="form-control" placeholder="Job name ($GEP_JOB_NAME)" minlength="1" spellcheck="true" required>
                                                <label>Job name ($GEP_JOB_NAME)</label>
                                            </div>
                                        </div>

                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["scriptFile"]} class="form-control" placeholder="Script file ($GEP_SCRIPT_FILE)" minlength="1" spellcheck="true" required>
                                                <label>Script file ($GEP_SCRIPT_FILE)</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["nodes"]} class="form-control" placeholder="Number of nodes ($GEP_N_NODES)" minlength="1" spellcheck="true" required>
                                                <label>Number of nodes ($GEP_N_NODES)</label>
                                            </div>
                                        </div>

                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["threads"]} class="form-control" placeholder="Number of threads ($GEP_N_THREADS)" minlength="1" spellcheck="true" required>
                                                <label>Number of threads ($GEP_N_THREADS)</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["memory"]} class="form-control" placeholder="Memory ($GEP_MEMORY)" minlength="1" spellcheck="true" required>
                                                <label>Memory ($GEP_MEMORY)</label>
                                            </div>
                                        </div>

                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["runTime"]} class="form-control" placeholder="Maximum run time ($GEP_MAX_RUNTIME)" minlength="1" spellcheck="true" required>
                                                <label>Maximum run time ($GEP_MAX_RUNTIME)</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-6">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["partition"]} class="form-control" placeholder="Slurm partition ($GEP_SLURM_PARTITION)" minlength="1" spellcheck="true" required>
                                                <label>Slurm partition ($GEP_SLURM_PARTITION)</label>
                                            </div>
                                        </div>

                                        <div class="col-6">
                                            <div class="form-floating">
                                                <select bind:value={$jobByUUID[job.UUID]["runMode"]} class="form-select">
                                                    <option value="once" selected>Run only once</option>
                                                    <option value="forEachSample">Run once for each sample ($GEP_SAMPLE)</option>
                                                </select>
                                                <label>Execution policy ($GEP_EXEC_POLICY)</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-12">
                                            <div class="form-floating">
                                                <input type="text" bind:value={$jobByUUID[job.UUID]["variables"]} class="form-control" placeholder="Environment variables (comma separated)" spellcheck="true" required>
                                                <label>Environment variables (comma separated)</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="section-caption">
                                        <span>Dependencies</span>
                                    </div>

                                    <div class="row">
                                        <div class="col-12">
                                            <div class="form-floating">
                                                <ul id="dependencyList{job.UUID}" class="list-group">
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
</div>


<div class="container-fluid section-container">
    <div class="row">
        <div class="col text-center">
            <button type="button" on:click={pipeline.generatePipeline} class="btn btn-primary"><span class="material-symbols-rounded">download</span> Generate pipeline file</button>
        </div>
    </div>

    <div class="section-caption">
        <span>How to use</span>
    </div>

    <div class="text-center">
        <p>First, <strong>download and install</strong> GEP on your machine by typing:</p>
        <code>curl -sL https://raw.githubusercontent.com/ManuelArcieri/GenomicPipeline/main/install.sh | bash</code>
        <br>
        <code>alias gep=$HOME/GenomicPipeline/gep.sh</code>

        <p class="text-spacer">After that, you can <strong>run</strong> your pipeline with:</p>
        <code>gep run pipeline.toml</code>

        <p class="text-spacer">You can check the <strong>status</strong> of your pipeline with:</p>
        <code>gep status pipeline.toml</code>

        <p class="text-spacer">For more information, type:</p>
        <code>gep help</code>
    </div>

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
                            <input type="text" id="JobNameInput" bind:value={pipeline.jobName} class="form-control" placeholder="Job name ($GEP_JOB_NAME)" minlength="1" spellcheck="true" required>
                            <label for="JobNameInput">Job name ($GEP_JOB_NAME)</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="scriptFileInput" bind:value={pipeline.scriptFile} class="form-control" placeholder="Script file ($GEP_SCRIPT_FILE)" minlength="1" spellcheck="true" required>
                            <label for="scriptFileInput">Script file ($GEP_SCRIPT_FILE)</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="nodesInput" bind:value={pipeline.nodes} class="form-control" placeholder="Number of nodes ($GEP_N_NODES)" minlength="1" spellcheck="true" required>
                            <label for="nodesInput">Number of nodes ($GEP_N_NODES)</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="threadsInput" bind:value={pipeline.threads} class="form-control" placeholder="Number of threads ($GEP_N_THREADS)" minlength="1" spellcheck="true" required>
                            <label for="threadsInput">Number of threads ($GEP_N_THREADS)</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="memoryInput" bind:value={pipeline.memory} class="form-control" placeholder="Memory ($GEP_MEMORY)" minlength="1" spellcheck="true" required>
                            <label for="memoryInput">Memory ($GEP_MEMORY)</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="runTimeInput" bind:value={pipeline.runTime} class="form-control" placeholder="Maximum run time ($GEP_MAX_RUNTIME)" minlength="1" spellcheck="true" required>
                            <label for="runTimeInput">Maximum run time ($GEP_MAX_RUNTIME)</label>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-6">
                        <div class="form-floating">
                            <input type="text" id="partitionInput" bind:value={pipeline.partition} class="form-control" placeholder="Slurm partition ($GEP_SLURM_PARTITION)" minlength="1" spellcheck="true" required>
                            <label for="partitionInput">Slurm partition ($GEP_SLURM_PARTITION)</label>
                        </div>
                    </div>

                    <div class="col-6">
                        <div class="form-floating">
                            <select id="runModeSelect" bind:value={pipeline.runMode} class="form-select">
                                <option value="once" selected>Run only once</option>
                                <option value="forEachSample">Run once for each sample ($GEP_SAMPLE)</option>
                            </select>
                            <label for="runModeSelect">Execution policy ($GEP_EXEC_POLICY)</label>
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
