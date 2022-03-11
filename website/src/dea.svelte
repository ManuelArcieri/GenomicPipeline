<script>
    import {writable} from "svelte/store";

    export const vars = writable({
        pipelineName: ""
    });
</script>


<div class="container-fluid">
    <div class="row">
        <div class="col-6">
            <div class="form-floating">
                <input type="text" id="pipelineNameInput" bind:value={$vars.pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                <label for="pipelineNameInput">Pipeline name</label>
            </div>
        </div>
    </div>


    <div class="row">
        <div class="col">
            <div class="form-floating">
                <input type="text" id="workingDirectoryInput" bind:value={$vars.pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                <label for="pipelineName">Pipeline name</label>
            </div>
        </div>

        <div class="col">
            <div class="form-floating">
                <input type="text" id="pipelineName" bind:value={$vars.pipelineName} class="form-control" placeholder="Pipeline name" minlength="1" spellcheck="true" required>
                <label for="pipelineName">Pipeline name</label>
            </div>
        </div>
    </div>
</div>
