import {writable} from "svelte/store";

export const pipelineData = writable({
    pipelineName: "",
    account: "",
    workingDirectory: "",
    logsDirectory: "",
    samples: "",

    salmonDownloadName: "Download Salmon binary",
    salmonDownloadScript: "download-salmon.sh",
    salmonDownloadNodes: "1",
    salmonDownloadThreads: "1",
    salmonDownloadMemory: "4GB",
    salmonDownloadRunTime: "04:00:00",
    salmonDownloadPartition: "g100_all_serial"
});
