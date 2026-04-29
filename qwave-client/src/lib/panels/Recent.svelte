<script>
    import { onMount } from "svelte"
    import { api } from "../stores/api"
    import { play, playNext, queueItem, currentTrack } from "../stores/player";
    let tracks = []
    let loading = false
    let error = ""

    onMount(() => {
      tracks = JSON.parse(localStorage.getItem("recent")) || []
    })

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
    {:else if tracks.length === 0}
        <div class="status">no tracks found! open the upload tab!</div>
    {:else}
        {#each tracks as track}
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <!-- svelte-ignore a11y_no_static_element_interactions -->
            <div class="track" class:active={$currentTrack?.id === track.id} on:click={() => play(tracks, tracks.indexOf(track))}>
                <div class="track-main">
                    <div class="track-title">{track.title}</div>
                    <div class="track-artist">{primaryArtist(track)}</div>
                </div>
                <div class="track-right">
                    <span class="duration">{getDuration(track.duration)}</span>
                    <div class="track-actions">
                        <button title="play next" on:click|stopPropagation={() => playNext(track)}>
                            <svg class="svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="2vmax" height="2vmax" display="bllock" fill="currentColor">
                                <path fill="var(--primary)" d="M6 2.86V5H3a1 1 0 00-1 1v12a1 1 0 102 0V7h2v2.137a.5.5 0 00.748.434L13 5.998 6.748 2.426A.5.5 0 006 2.86ZM21 5h-5a1 1 0 100 2h5a1 1 0 100-2Zm0 6H9a1 1 0 000 2h12a1 1 0 000-2Zm0 6H9a1 1 0 000 2h12a1 1 0 000-2Z"></path>
                            </svg>
                        </button>
                        <button title="add to queue" on:click|stopPropagation={() => queueItem(track)}>
                            <svg class="svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="2vmax" height="2vmax" display="bllock" fill="currentColor">
                                <path fill="var(--primary)" d="M21 6.998a1 1 0 100-2H9a1 1 0 000 2h12ZM6 21.138a.5.5 0 00.748.434L13 18l-6.252-3.573A.5.5 0 006 14.86V17H4V6a1 1 0 00-2 0v12a1 1 0 001 1h3v2.138Zm15-8.14a1 1 0 000-2H9a1 1 0 000 2h12Zm0 6a1 1 0 000-2h-5a1 1 0 000 2h5Z"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        {/each}
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
