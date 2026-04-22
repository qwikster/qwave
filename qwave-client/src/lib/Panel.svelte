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
        background: var(--bg);
        overflow-y: auto;
        flex: 1;
        border: var(--border-tile) solid var(--dim);
        padding: 0.5rem;
    }

    .panel {
        margin: 0.2rem;
        min-width: 50vw;
        grid-column: 2;
        display: flex;
        flex-direction: column;
    }

    p { margin: 0rem; }
</style>
