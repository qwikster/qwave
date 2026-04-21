<script></script>

<div class="now-playing">
    <div class="playing-info">
        <div class="playing-artist">NOW PLAYING: RICK ASTLEY</div>
        <div class="playing-title">Never Gonna Give You Up</div>
        <div class="playing-bar" style="color: var(--accent);">-------seekbar-------</div>
    </div>
    <div class="playing-controls">
        <div class="track">TRACK 2</div>
        <div class="time">1:02/3:32</div>
        <div class="controls">
            <button class="control" id="controls-prev">󰒮</button>
            <button class="control" id="controls-pause">󰏤</button>
            <button class="control" id="controls-next">󰒭</button>
        </div>
    </div>
</div>

<style>
    .now-playing {
        grid-column: 2;
        display: flex;
        flex: 1;
        border: 3px solid var(--primary);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;
    }

    .playing-info {
        display: flex;
        flex-direction: column;
    }

    .playing-artist {
        font-size: 16px;
        color: var(--dim);
    }

    .playing-controls {
        border-left: 2px solid var(--dim);
        padding-left: 0.5rem;
        text-align: center;
    }

    .track, .time {
        font-size: 16px;
        color: var(--dim);
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
        border: 2px solid var(--secondary);
        border-radius: 5px;
        margin-top: 0.5rem;
    }
</style>
