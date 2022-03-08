import App from "./App.svelte";

const app = new App({
    target: document.getElementById("app"),
    props: {
        test: "Manuel"
    }
});

export default app;
