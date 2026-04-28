<script>
    import { queue, queueIndex, currentTrack, play, skip } from "../stores/player";
    import { get } from "svelte/store";

    let dragFrom = null

    function primaryArtist(track) {
      return track.artists?.find(a => a.is_primary)?.name
      ?? track.artists?.[0]?.name
      ?? "Unknown Artist"
    }

    function getDuration(seconds) {
      const m = Math.floor(seconds / 60).toString()
      const s = Math.floor(seconds % 60).toString()
      return `${m}m ${s}s`
    }

    function dragStart(i) {
      dragFrom = i
    }

    function dragOver(e) {
      e.preventDefault()
    }

    function drop(i) {
      if (dragFrom === null || dragFrom === i) return
      queue.update(q => {
        const next = [...q]
        const [moved] = next.splice(dragFrom, 1)
        next.splice(i, 0, moved)
        return next
      })
      queueIndex.update(idx => {
        if (dragFrom === idx) return i
        if (dragFrom < idx && i >= idx) return idx - 1
        if (dragFrom > idx && i <= idx) return idx + 1
        return idx
      })
      dragFrom = null
    }

</script>

<div class="queue">
    {#if $queue.length === 0}
        <div class="status">queue is empty :(</div>
    {:else}
        <div class="status">drag to rearrange!</div>
        {#each $queue as track, i}
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <!-- svelte-ignore a11y_no_static_element_interactions -->
            <div
                class = "track"
                class:active = {$currentTrack.id === track.id && i === $queueIndex}
                draggable="true"
                on:dragstart={() => dragStart(i)}
                on:dragover={dragOver}
                on:drop={() => drop(i)}
                on:click={skip(i)}>
                <span class="index">{i + 1}</span>
                <div class="track-main">
                    <div class="track-title">{track.title}</div>
                    <div class="track-artist">{primaryArtist(track)}</div>
                </div>
                <span class="duration">{getDuration(track.duration)}</span>
                <button title="remove" on:click|stopPropagation={() => {queue.update(q => q.filter((_, j) => j !== i)); queueIndex.update(idx => i < idx ? idx - 1 : idx);}}></button>
            </div>
        {/each}
    {/if}
</div>

<style>
    .queue {
        display: flex;
        flex-direction: column;
    }

    .status {
        color: var(--dim);
        font-size: var(--font-artist);
        text-align: center;
    }

    .track {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.2rem 0.3rem;
        border-bottom: var(--border-small) solid var(--dim);
        cursor: grab;
        transition: background 0.15s ease;
    }

    .track:active { cursor: grabbing }
    .track:hover { background: var(--dimmer); }
    .track.active { background: #14f5aa11; }
    .track.active .track-title { color: var(--accent); }

    .index {
        color: var(--primary);
        font-size: var(--font-info);
        min-width: 2ch;
        text-align: right;
        flex-shrink: 0;
        margin-right: 1rem;
    }

    .track-main {
        display: flex;
        flex-direction: column;
        min-width: 0;
        flex: 1;
    }

    .track-title {
        color: var(--secondary);
        font-size: var(--font-artist);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .track-artist {
        color: var(--dim);
        font-size: var(--font-info);
    }

    .duration {
        color: var(--dim);
        font-size: var(--font-info);
    }

    button {
        font-family: "ProFont";
        font-size: var(--font-info);
        background: none;
        color: var(--primary);
        border: none;
        cursor: pointer;
        padding: 0.2rem 0.4rem;
        border-radius: 20%;
        flex-shrink: 0;
        transition: all 0.2s ease;
    }

    button:hover { color: var(--accent); background: var(--dimmer); }
</style>
