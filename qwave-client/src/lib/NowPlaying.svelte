<script>
    import { next, prev, play, togglePlaying } from "./stores/player";
</script>

<div class="now-playing">
    <div class="playing-info">
        <div class="playing-artist">NOW PLAYING: RICK ASTLEY</div>
        <div class="playing-title">Never Gonna Give You Up</div>
        <input class="playing-seek" type="range" style="--progress: 50%">
    </div>
    <div class="playing-controls">
        <div class="track">TRACK 2</div>
        <div class="time">01:02/03:32</div>
        <div class="controls">
            <button class="control" id="controls-prev" on:click={() => prev()}>󰒮</button>
            <button class="control" id="controls-pause" on:click={() => togglePlaying()}>󰏤</button>
            <button class="control" id="controls-next" on:click={() => next()}>󰒭</button>
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
    }

    .playing-seek::-webkit-slider-runnable-track {
        background: linear-gradient(
            to right,
            var(--primary) 0%,
            var(--primary) var(--progress, 0%),
            var(--dim) var(--progress, 0%),
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
        margin-top: -0.9vmin;
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
    }

    @media (max-width: 540px) { .now-playing { grid-column: span 2; } }
</style>
