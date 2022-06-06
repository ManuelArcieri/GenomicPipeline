import {writable} from "svelte/store";

export const jobs = writable([]);
export const jobByUUID = writable(new Map());
export const jobsByStep = writable([]);
