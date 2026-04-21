<script></script>

<div class="app">
    <header>
        <img src="./src/assets/logo_lg.png" alt="n" width="140px" class="logo">
        <input id="search" type="search" class="search" placeholder="SEARCH..." />
        <span class="clock">10:10PM</span>
    </header>
    <div class="main">
        <div class="top">
            <div style="color: var(--accent);" class="visualizer tile">
                <span>cool visualizer</span>
            </div>
            <div class="now-playing tile">
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
        </div>
        <div class="bottom">
            <aside class="sidebar tile">
                <nav>
                    <div class="navitem">
                        <span class="navicon">󰎇</span><span class="navlink">SONGS</span>
                    </div>
                    <hr>
                    <div class="navitem">
                        <span class="navicon"></span><span class="navlink">ARTISTS</span>
                    </div>
                    <hr>
                    <div class="navitem">
                        <span class="navicon"></span><span class="navlink">ALBUMS</span>
                    </div>
                    <hr>
                    <div class="navitem">
                        <span class="navicon">󰐑</span><span class="navlink">PLAYLISTS</span>
                    </div>
                    <hr>
                    <div class="navitem">
                        <span class="navicon"></span><span class="navlink">RECENT</span>
                    </div>
                    <hr>
                    <div class="navitem">
                        <span class="navicon"></span><span class="navlink">RANDOM</span>
                    </div>
                    <hr>
                </nav>
                <div class="sidebar-bottom">
                    <button>Upload</button>
                    <button>Settings</button>
                </div>
            </aside>
            <div class="panel tile">
                panel here
            </div>
        </div>
    </div>
</div>

<style>
    .app {
        text-shadow: 0.03ex 0 0 currentcolor;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        background: var(--bg);
        color: var(--secondary);
        font-family: 'ProFont', monospace;
        font-size: 24px;
    }

    header {
        display: flex;
        align-items: stretch;
        padding: 0rem 0.2rem;
        margin: 0.2rem 0rem;
        flex: 1;
    }

    img {
        image-rendering: pixelated;
    }

    .search {
        flex-grow: 1;
        border: 3px solid var(--dim);
        background-color: var(--bg);
        color: var(--primary);
        font-family: 'ProFont';
        font-size: 16px;
        padding: 0.2rem;
        margin: 0rem 0.4rem;
    }

    .search::placeholder {
        color: var(--dim);
    }

    .clock {
        border: 3px solid var(--dim);
        color: var(--dim);
        padding: 0.2rem;
        font-size: 20px;
    }

    hr {
        border: 1px solid var(--dim);
        margin: 0.2rem;
    }

    .main {
        display: grid;
        grid-template-columns: 200px 1fr;
        flex-direction: column;
        flex: 1;
        overflow: hidden;
    }

    .tile {
        border: 3px solid var(--primary);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;
    }

    .top {
        display: contents;
    }

    .visualizer {
        grid-column: 1;
        flex-shrink: 0;

    }

    .now-playing {
        grid-column: 2;
        display: flex;
        flex: 1;
    }

    .playing-info {
        display: flex;
        flex-direction: column;
    }

    .playing-artist {
        font-size: 16px;
        color: var(--dim);
    }

    .playing-title {
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

    .bottom {
        display: contents;
    }

    .sidebar {
        grid-column: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 3px solid var(--dim);
    }

    nav {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .navitem {
        display: flex;
    }

    .navicon {
        margin-right: 0.5rem;
        color: var(--primary);
    }

    .panel {
        grid-column: 2;
        overflow-y: auto;
        flex: 1;
        border: 3px solid var(--dim);
    }
</style>
