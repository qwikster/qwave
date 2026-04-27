<script>
    import { activePanel } from "../stores/ui";
    import Songs from "./Songs.svelte";
    import Artists from "./Artists.svelte";
    import Albums from "./Albums.svelte";
    import Playlists from "./Playlists.svelte";
    import Recent from "./Recent.svelte";
</script>

<div class="cont">
    {#if $activePanel === "songs"}
        <Songs />
    {:else if $activePanel === "artists"}
        <Artists />
    {:else if $activePanel === "albums"}
        <Albums />
    {:else if $activePanel === "playlists"}
        <Playlists />
    {:else if $activePanel === "recent"}
        <Recent />
    {/if}
</div>
