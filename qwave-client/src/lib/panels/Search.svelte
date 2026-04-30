<script>
    import { onMount } from "svelte"
    import { api } from "../stores/api"
    import { play, playNext, queueItem, currentTrack } from "../stores/player";
    import { get } from "svelte/store";
    import { activePanel, activeTab, tabMeta } from "../stores/ui";

    let results = { tracks: [], artists: [], albums: [] }
    let loading = false
    let error = ""
    let lastQuery = ""

    $: if ($tabMeta && $tabMeta !== lastQuery) {
      lastQuery = $tabMeta
      search($tabMeta)
    }

    async function search(query) {
      loading = true
      error = ""
      results = { tracks: [], artists: [], albums: [] }
      try {
        results = await api.search(query)
      } catch (e) {
        error = e.message
      } finally {
        loading = false
      }
    }

    function getDuration(seconds) {
      const m = Math.floor(seconds / 60).toString().padStart(2, "0")
      const s = Math.floor(seconds % 60).toString().padStart(2, "0")
      return `${m}:${s}`
    }

    function primaryArtist(track) {
      return track.artists.find(a => a.is_primary)?.name
        ?? track.artists[0]?.name
        ?? "Unknown"
    }
</script>

<div class="songs">
    {#if loading}
        <div class="status">loading...</div>
    {:else if error}
        <div class="error">{error}</div>
    {:else if !results.artists.length && !results.tracks.length && !results.albums.length}
        <div class="status">no results... :(</div>
    {:else}
        {#if results.artists.length}
            {#each results.artists as artist}

            {/each}
        {/if}
        {#if results.tracks.length}
            {#each results.tracks as track}

            {/each}
        {/if}
    {/if}
</div>


<style>
    .songs {
        display: flex;
        flex-direction: column;
    }

    .track {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0.3rem;
        border-bottom: var(--border-small) solid var(--dim);
        cursor: pointer;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }

    .track.active { background: #14f5aa11; }
    .track:hover { background: var(--dimmer); }
    .track.active .track-title { color: var(--accent); }

    .track-main {
        display: flex;
        flex-direction: column;
        min-width: 0;
        flex: 1;
    }

    .track-title {
        color: var(--secondary);
        font-size: var(--font-titles);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .track-artist {
        color: var(--dim);
        font-size: var(--font-info);
    }

    .track-right {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-shrink: 0;
    }

    .duration {
        color: var(--dim);
        font-size: var(--font-artist);
    }

    .track-actions {
        display: flex;
        gap: 0.2rem;
    }

    button {
        font-family: "ProFont";
        font-size: var(--font-info);
        background: none;
        color: var(--dim);
        border: none;
        cursor: pointer;
        padding: 0.2rem;
        line-height: 1;
        display: flex;
        align-items: center;
        border-radius: 20%;
        transition: all 0.2s ease;
    }

    button:hover {
        color: var(--accent);
        background-color: var(--dim);
    }

</style>
