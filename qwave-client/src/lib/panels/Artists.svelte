<script>
    import { activeTab, tabMeta } from "../stores/ui";
    import { onMount } from "svelte"
    import { api } from "../stores/api"
    import { play, playNext, queueItem, currentTrack } from "../stores/player";

    let artists = []
    let artists_raw = []
    let loading = true
    let error = ""

    onMount(async () => {
      try {
        const res = await api.artists({ limit: 512 })
        artists_raw = res.artists.sort((a, b) => a.name.localeCompare(b.title))
        artists = artists_raw.filter(artist => artist.track_count !== 0)
      } catch (e) {
        error = e.message
      } finally {
        loading = false
      }
    })

    async function getDuration(artist) {
      let duration = 0
      const a = await api.artist(artist.id)
      console.log(a)
      for (const track of a.tracks) {
        duration = duration + track.duration
      }
      const m = Math.floor(duration / 60).toString()
      const s = Math.floor(duration % 60).toString().padStart(2, "0")
      return `${m}m${s}s`
    }

    function s(num) {
      if (num == 1) {
        return ""
      } else {
        return "S"
      }
    }
</script>


<div class="songs">
    {#if loading}
        <div class="status">loading...</div>
    {:else if error}
        <div class="error">{error}</div>
    {:else if artists.length === 0}
        <div class="status">no tracks found! open the upload tab!</div>
    {:else}
        {#each artists as artist}
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <!-- svelte-ignore a11y_no_static_element_interactions -->
            <div class="artist" on:click={() => {activeTab.set("artist"); tabMeta.set(artist.id)}}>
                <div class="artist-main">
                    <div class="artist-name">{artist.name}</div>
                    {#await getDuration(artist)}
                        <div class="artist-duration">ARTIST</div>
                    {:then data}
                        <div class="artist-duration">ARTIST | {data}</div>
                    {/await}
                </div>
                <div class="artist-right">
                    <span class="tracknum">{artist.track_count} TRACK{s(artist.track_count)}</span>
                    <div class="actions">
                        <button title="play all" on:click|stopPropagation={() => play}>󱏦</button>
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

    .artist {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0.3rem;
        border-bottom: var(--border-small) solid var(--dim);
        cursor: pointer;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }

    .artist:hover { background: var(--dimmer); }

    .artist-main {
        display: flex;
        flex-direction: column;
        min-width: 0;
        flex: 1;
    }

    .artist-name {
        color: var(--secondary);
        font-size: var(--font-titles);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .artist-duration {
        color: var(--dim);
        font-size: var(--font-info);
    }

    .artist-right {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-shrink: 0;
    }

    .tracknum {
        color: var(--dim);
        font-size: var(--font-artist);
    }

    .actions {
        display: flex;
        gap: 0.2rem;
    }

    button {
        text-shadow: 0.03ex 0 0 currentcolor;
        font-family: "ProFont";
        font-size: var(--font-titles);
        background: none;
        color: var(--primary);
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
