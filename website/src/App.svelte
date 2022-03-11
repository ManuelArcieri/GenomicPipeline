<script>
    import Dea from "./dea.svelte";

    let selectedPipeline;
</script>

<label for="pipeline-selector">Pipeline:</label>
<select id="pipeline-selector" bind:value={selectedPipeline} class="form-select w-20rem">
    <option value="none" selected>Choose a pipeline...</option>
    <option value="dea">Differential expression analysis</option>
</select>

{#if selectedPipeline === "dea"}
    <Dea />
{/if}
