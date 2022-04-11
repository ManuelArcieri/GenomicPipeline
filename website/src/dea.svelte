<script>
    import {pipelineData} from "./stores";
</script>


<div class="container-fluid">
    <!-------------------------- RUNTIME ENVIRONMENT -------------------------->

    <div class="section-caption">
        <span>Runtime environment</span>
    </div>

    <div class="row">
        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="pipelineNameInput" bind:value={$pipelineData.pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                <label for="pipelineNameInput">Pipeline name</label>
            </div>
        </div>

        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="accountInput" bind:value={$pipelineData.account} class="form-control" placeholder="Account (Slurm)" minlength="1" spellcheck="true" required>
                <label for="accountInput">Account (Slurm)</label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="workingDirectoryInput" bind:value={$pipelineData.workingDirectory} class="form-control" placeholder="Working directory" minlength="1" spellcheck="true" required>
                <label for="workingDirectoryInput">Working directory</label>
            </div>
        </div>

        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="logsDirectoryInput" bind:value={$pipelineData.logsDirectory} class="form-control" placeholder="Logs directory" minlength="1" spellcheck="true" required>
                <label for="logsDirectoryInput">Logs directory</label>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="form-floating">
                <textarea id="samplesInput" bind:value={$pipelineData.samples} class="form-control" placeholder="Samples (one per line)" minlength="1" autocomplete="off" spellcheck="false" wrap="soft" required></textarea>
                <label for="samplesInput">Samples (one per line)</label>
            </div>
        </div>
    </div>


    <!-------------------------- STEP 1: resources download -------------------------->

    <div class="section-caption">
        <span>Step 1: resources download</span>
    </div>

    <div class="row">
        <div class="accordion" id="accordionDownloadSalmon">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingDownloadSalmon">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDownloadSalmon" aria-expanded="false" aria-controls="collapseDownloadSalmon">
                        Download Salmon binary
                    </button>
                </h2>
                <div id="collapseDownloadSalmon" class="accordion-collapse collapse" aria-labelledby="headingDownloadSalmon" data-bs-parent="#accordionDownloadSalmon">
                    <div class="accordion-body">
                        <div class="row">
                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadNameInput" bind:value={$pipelineData.salmonDownloadName} class="form-control" placeholder="Name" minlength="1" spellcheck="true" required>
                                    <label for="workingDirectoryInput">Name</label>
                                </div>
                            </div>

                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadScriptInput" bind:value={$pipelineData.salmonDownloadScript} class="form-control" placeholder="Script file" minlength="1" spellcheck="true" required>
                                    <label for="logsDirectoryInput">Script file</label>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadNodesInput" bind:value={$pipelineData.salmonDownloadNodes} class="form-control" placeholder="Number of nodes" minlength="1" spellcheck="true" required>
                                    <label for="workingDirectoryInput">Number of nodes</label>
                                </div>
                            </div>

                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadThreadsInput" bind:value={$pipelineData.salmonDownloadThreads} class="form-control" placeholder="Number of threads" minlength="1" spellcheck="true" required>
                                    <label for="logsDirectoryInput">Number of threads</label>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadMemoryInput" bind:value={$pipelineData.salmonDownloadMemory} class="form-control" placeholder="Memory" minlength="1" spellcheck="true" required>
                                    <label for="workingDirectoryInput">Memory</label>
                                </div>
                            </div>

                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadRunTime" bind:value={$pipelineData.salmonDownloadRunTime} class="form-control" placeholder="Maximum run time" minlength="1" spellcheck="true" required>
                                    <label for="logsDirectoryInput">Maximum run time</label>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-6">
                                <div class="form-floating">
                                    <input type="text" id="salmonDownloadPartitionInput" bind:value={$pipelineData.salmonDownloadPartition} class="form-control" placeholder="Partition" minlength="1" spellcheck="true" required>
                                    <label for="workingDirectoryInput">Partition</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="accordion" id="accordionDownloadSalmonIndex">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingDownloadSalmonIndex">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseDownloadSalmonIndex" aria-expanded="false" aria-controls="collapseDownloadSalmonIndex">
                        Download pre-built hg38 Salmon index
                    </button>
                </h2>
                <div id="collapseDownloadSalmonIndex" class="accordion-collapse collapse" aria-labelledby="headingDownloadSalmonIndex" data-bs-parent="#accordionDownloadSalmonIndex">
                    <div class="accordion-body">

                    </div>
                </div>
            </div>
        </div>

        <div class="accordion" id="accordionPrefetch">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingPrefetch">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapsePrefetch" aria-expanded="false" aria-controls="collapsePrefetch">
                        Prefetch samples
                    </button>
                </h2>
                <div id="collapsePrefetch" class="accordion-collapse collapse" aria-labelledby="headingPrefetch" data-bs-parent="#accordionPrefetch">
                    <div class="accordion-body">

                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-------------------------- STEP 2: split SRA files -------------------------->

    <div class="section-caption">
        <span>Step 2: split SRA files</span>
    </div>

    <div class="row">
        <div class="accordion" id="accordionFastqDump">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingFastqDump">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFastqDump" aria-expanded="false" aria-controls="collapseFastqDump">
                        fastq-dump sample
                    </button>
                </h2>
                <div id="collapseFastqDump" class="accordion-collapse collapse" aria-labelledby="headingFastqDump" data-bs-parent="#accordionFastqDump">
                    <div class="accordion-body">

                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-------------------------- STEP 3: quantifying with Salmon -------------------------->

    <div class="section-caption">
        <span>Step 3: quantifying with Salmon</span>
    </div>

    <div class="row">
        <div class="accordion" id="accordionQuant">
            <div class="accordion-item">
                <h2 class="accordion-header" id="headingQuant">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseQuant" aria-expanded="false" aria-controls="collapseQuant">
                        salmon quant sample
                    </button>
                </h2>
                <div id="collapseQuant" class="accordion-collapse collapse" aria-labelledby="headingQuant" data-bs-parent="#accordionQuant">
                    <div class="accordion-body">

                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-------------------------- Generate TOML file -------------------------->

    <div class="section-caption">
        <span>Generate pipeline</span>
    </div>

    <div class="row">
        <div class="col-4"></div>

        <div class="col text-center">
            <button type="button" class="btn btn-primary">Download TOML file</button>
        </div>

        <div class="col-4"></div>
    </div>


    <!-------------------------- How to run -------------------------->

    <div class="section-caption">
        <span>How to run the pipeline</span>
    </div>

    <div class="row">
        <div class="col text-col">
            <p>First, install or update GEP by typing:</p>
            <code>curl -sL https://raw.githubusercontent.com/ManuelArcieri/GenomicPipeline/main/install.sh | bash<br>
                  alias gep=$HOME/GenomicPipeline/gep.sh</code>

            <p>Then, you can run the entire pipeline by typing:</p>
            <code>gep run pipeline.toml</code>

            <p>You can check the status of all running jobs with:</p>
            <code>gep status pipeline.toml</code>
        </div>
    </div>
</div>
