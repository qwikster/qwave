<script>
    import { onDestroy } from "svelte"
    import { currentTrack, playing, progress, duration, volume, next, prev, togglePlaying, addRecent } from "./stores/player";
    import { api } from "./stores/api";
    import { audio, audioctx } from "./stores/audio";

    function resume() { if (audioctx.state === "suspended") audioctx.resume() }

    let prevTrack = null
    let currentTime = 0

    $: if ($currentTrack && $currentTrack.id !== prevTrack) {
      prevTrack = $currentTrack.id
      const token = localStorage.getItem("token")

      audio.src = `${api.stream($currentTrack.id)}?token=${token}`
      audio.load()
      resume()
      if ($playing) audio.play()

      addRecent($currentTrack)
    }

    $: if ($playing) { audio.play().catch(() => playing.set(false)) } else { audio.pause() }

    $: audio.volume = $volume

    let seeking = false

    audio.addEventListener("timeupdate", () => {
      if (!seeking) {
        duration.set(audio.duration || 0)
        currentTime = audio.currentTime
        progress.set(audio.duration ? (audio.currentTime / audio.duration) * 100 : 0)
      }
    })

    audio.addEventListener("ended", () => next())
    audio.addEventListener("error", () => playing.set(false))

    function onSeek(e) {
      if (audio.duration) {
        audio.currentTime = (e.target.value / 100) * audio.duration
      }
    }

    function formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return "00:00"
      const m = Math.floor(seconds / 60).toString().padStart(2, "0")
      const s = Math.floor(seconds % 60).toString().padStart(2, "0")
      return `${m}:${s}`
    }

    function primaryArtist(track) {
      return track?.artists.find(a => a.is_primary)?.name
      ?? track?.artists[0]?.name
      ?? "Unknown Artist"
    }

    onDestroy(() => {
      audio.pause()
      audio.src = ""
    })

</script>

<div class="now-playing">
    <div class="playing-info">
        <div class="playing-artist">{$currentTrack ? `NOW PLAYING: ${primaryArtist($currentTrack)}` : "NOT PLAYING"}</div>
        <div class="playing-title">{$currentTrack?.title ?? "pick a song!"}</div>
        <input class="playing-seek" type="range" min="0" max="100"
            value={$progress} style="--progress: {$progress}%"
            on:mousedown={() => {seeking = true}} on:mouseup={() => {seeking = false}}
            on:input={e => {
              seeking = true
              audio.currentTime = (e.target.value / 100) * (audio.duration || 0)
              currentTime = audio.currentTime
        }}>
    </div>
    <div class="playing-controls">
        <div class="track">{$currentTrack ? `TRACK ${$currentTrack.track_number ?? ""}` : "SINGLE"}</div>
        <div class="time">{formatTime(currentTime)}/{formatTime($duration)}</div>
        <div class="controls">
            <button class="control" id="controls-prev" on:click={prev}>󰒮</button>
            <button class="control" id="controls-pause" on:click={() => {resume(); playing.update(p => !p);}}>
                {$playing ? "󰏤" : "󰐊"}
            </button>
            <button class="control" id="controls-next" on:click={next}>󰒭</button>
        </div>
    </div>
</div>

<style>
    .now-playing {
        grid-area: nowplaying;
        background: var(--bg);
        grid-column: 2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
        border: var(--border-tile) solid var(--primary);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;
        min-width: 40vw;
    }

    .playing-info {
        display: flex;
        flex-direction: column;
        min-width: 0;
        width: 100%;
    }

    .playing-artist {
        font-size: var(--font-artist);
        color: var(--dim);
    }

    .playing-seek {
        display: block;
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 3vmin;
        background: transparent;
        outline: none;
        cursor: pointer;
        margin-top: 0.5vh;
        box-sizing: border-box;
    }

    .playing-seek::-webkit-slider-runnable-track {
        background: linear-gradient(
            to right,
            var(--primary) 0%,
            var(--primary) calc(var(--progress, 0%) - 0.8%),
            var(--dim) calc(var(--progress, 0%) + 0.4%),
            var(--dim) 100%
        );
        height: 1.2vmin;
        border-radius: 1vmin;
    }

    .playing-seek::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 3vmin;
        height: 3vmin;
        border: 0.6vmin solid var(--dim);
        border-radius: 50%;
        background: var(--secondary);
        cursor: pointer;
        margin-top: calc(-1.5vmin + 0.6vmin)
    }

    .playing-seek::-moz-range-thumb {
        width: 2vmin;
        height: 2vmin;
        border-color: #4C6460;
        border-radius: 50%;
        border-width: 4px;
        background: var(--secondary);
    }

    .playing-seek::-moz-range-track {
        background: var(--dim);
        height: 1.2vmin;
    }

    .playing-seek::-moz-range-progress {
        background: var(--primary);
        height: 1.2vmin;
    }

    .playing-controls {
        flex: 0 0 auto;
        border-left: var(--border-hr) solid var(--dim);
        padding-left: 0.5rem;
        text-align: center;
    }

    .track, .time {
        font-size: var(--font-info);
        color: var(--dim);
    }

    .playing-artist, .playing-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .controls {
        display: flex;
        gap: 0.2rem;
        justify-content: center;
    }

    .control {
        font-family: 'ProFont';
        color: var(--secondary);
        background-color: var(--bg);
        border-color: var(--secondary);
        border-radius: 5px;
        margin-top: 0.5rem;
        padding-inline: 0.7vw;
        padding-block: 0;
        cursor: pointer;
    }

    .control:hover { color: var(--accent); border-style: solid }

    @media (max-width: 540px) { .now-playing { grid-column: span 2; } }
</style>
