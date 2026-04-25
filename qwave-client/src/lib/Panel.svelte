<script>
    import { activeTab } from "./stores/ui"
    import Tabs from "./Tabs.svelte"
    import Nav from "./panels/Nav.svelte"
    import Queue from "./panels/Queue.svelte"
    import Lyrics from "./panels/Lyrics.svelte"
    import Login from "./panels/Login.svelte"
    import Settings from "./panels/Settings.svelte";
    import Upload from "./panels/Upload.svelte";
</script>

<div class="panel">
    <Tabs />
    <div class="content">
        {#if $activeTab === "nav"}
            <Nav />
        {:else if $activeTab === "queue"}
            <Queue />
        {:else if $activeTab === "lyrics"}
            <Lyrics />
        {:else if $activeTab === "login"}
            <Login />
        {:else if $activeTab === "settings"}
            <Settings />
        {:else if $activeTab === "upload"}
            <Upload />
        {/if}
    </div>
</div>

<style>
    .content {
        display: flex;
        flex-direction: column;
        flex: 1;
        background: var(--bg);
        overflow-y: auto;
        border: var(--border-tile) solid var(--dim);
        padding: 0.5rem;
        min-height: 0;
        scrollbar-width: thin;
        scrollbar-color: var(--dim) var(--bg);
    }

    .panel {
        grid-area: panel;
        margin: 0.2rem;
        min-height: 0;
        min-width: 50vw;
        grid-column: 2;
        display: flex;
        flex-direction: column;
    }
</style>
