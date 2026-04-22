<script>
    import { activePanel } from "./stores/ui"
    import Login from "./panels/Login.svelte"
    import Songs from "./panels/Songs.svelte"
    import Artists from "./panels/Artists.svelte";
    import Albums from "./panels/Albums.svelte";
    import Playlists from "./panels/Playlists.svelte";
    import Recent from "./panels/Recent.svelte";
    import Settings from "./panels/Settings.svelte";
    import Upload from "./panels/Upload.svelte";
</script>

<div class="panel">
    {#if $activePanel === "login"}
        <Login />
    {:else if $activePanel === "songs"}
        <Songs />
    {:else if $activePanel === "artists"}
        <Artists />
    {:else if $activePanel === "albums"}
        <Albums />
    {:else if $activePanel === "playlists"}
        <Playlists />
    {:else if $activePanel === "recent"}
        <Recent />
    {:else if $activePanel === "settings"}
        <Settings />
    {:else if $activePanel === "upload"}
        <Upload />
    {:else}
        <p>Invalid panel?</p>
    {/if}
</div>

<style>
    .panel {
        background: var(--bg);
        grid-column: 2;
        overflow-y: auto;
        flex: 1;
        border: var(--border-tile) solid var(--dim);
        margin: 0.2rem;
        padding: 0.5rem;
        min-width: 50vw;
    }

    p { margin: 0rem; }
</style>
