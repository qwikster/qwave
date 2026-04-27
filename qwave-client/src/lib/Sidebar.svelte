<script>
    import { activePanel, activeTab } from "./stores/ui.js";
    import { volume } from "./stores/player.js";
</script>

<aside class="sidebar">
    <nav>
        <button class:active={$activePanel === "songs" && $activeTab === "nav"} class="navitem" on:click={() => { $activePanel = "songs"; $activeTab = "nav" }}>
            <span class="navicon">󰎇</span><span class="navlink">SONGS</span>
        </button>
        <button class:active={$activePanel === "artists" && $activeTab === "nav"} class="navitem" on:click={() => { $activePanel = "artists"; $activeTab = "nav" }}>
            <span class="navicon"></span><span class="navlink">ARTISTS</span>
        </button>
        <!-- <button class:active={$activePanel === "albums" && $activeTab === "nav"} class="navitem" on:click={() => { $activePanel = "albums"; $activeTab = "nav" }}>
            <span class="navicon"></span><span class="navlink">ALBUMS</span>
        </button> shhhhhhh it doesnt exist shhhh -->
        <button class:active={$activePanel === "playlists" && $activeTab === "nav"} class="navitem" on:click={() => { $activePanel = "playlists"; $activeTab = "nav" }}>
            <span class="navicon">󰐑</span><span class="navlink">LISTS</span>
        </button>
        <button class:active={$activePanel === "recent" && $activeTab === "nav"} class="navitem" on:click={() => { $activePanel = "recent"; $activeTab = "nav" }}>
            <span class="navicon"></span><span class="navlink">RECENT</span>
        </button>
        <button class="navitem" on:click={() => null}>
            <span class="navicon"></span><span class="navlink">RANDOM</span>
        </button>
    </nav>
    <div class="sidebar-bottom">
        <span class="navitem volume">
            <span class="navicon" style="font-size: var(--font-info)">VOL</span>
            <input class="volume-control" type="range" min="0" max="1" step="0.01" style="--volume: {$volume * 100}%" bind:value={$volume}>
        </span>
        <hr>
        <button class:active={$activeTab === "settings"} class="navitem" on:click={() => { $activeTab = "settings"; $activePanel = "none" }}>
            <span class="navicon"></span><span class="navlink">SETTINGS</span>
        </button>
        <button class:active={$activeTab === "upload"} class="navitem" on:click={() => { $activeTab = "upload"; $activePanel = "none" }}>
            <span class="navicon"></span><span class="navlink">UPLOAD</span>
        </button>
    </div>
</aside>

<style>
    hr {
        border: 1px solid var(--dim);
        margin: 0.2rem;
    }

    nav {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .sidebar {
        grid-area: sidebar;
        /* min-height: 50vh; */
        background: var(--bg);
        grid-column: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: var(--border-tile) solid var(--dim);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;
        padding-left: 0.1rem;
    }

    .sidebar-bottom {
        display: flex;
        flex-direction: column;
    }

    .volume {
        display: flex;
        align-items: center;
        padding-right: 10px;
    }

    .volume-control {
        -webkit-appearance: none;
        appearance: none;
        flex: 1;
        min-width: 0;
        height: 0.2vmin;
        background: transparent;
        outline: none;
        cursor: pointer;
        padding: 0 10px;
        box-sizing: border-box;
    }

    .volume-control::-webkit-slider-runnable-track {
        height: 0.8vmin;
        background: linear-gradient(
            to right,
            var(--primary) 0%,
            var(--primary) var(--volume, 0%),
            var(--dim) var(--volume, 0%),
            var(--dim) 100%
        );
        border-radius: 1vmin;
    }

    .volume-control::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 2vmin;
        height: 2vmin;
        border: 0.5vmin solid var(--dim);
        border-radius: 50%;
        background: var(--secondary);
        cursor: pointer;
        margin-top: -0.6vmin;
        position: relative;
        z-index: 2;
    }

    .volume-control::-moz-range-track {
        background: var(--dim);
        height: 1.2vmin;
        border-radius: 1vmin;
    }

    .volume-control::-moz-range-progress {
        background: var(--primary);
        height: 1.2vmin;
        border-radius: 1vmin;
    }

    .volume-control::-moz-range-thumb {
        width: 2vmin;
        height: 2vmin;
        border-color: #4C6460;
        border-radius: 50%;
        border-width: 4px;
        background: var(--secondary);
    }

    .navitem {
        text-shadow: 0.03ex 0 0 currentcolor;
        display: flex;
        border: none;
        outline-offset: -2px;
        cursor: pointer;
        transition: all 0.2s ease;
        padding: 0.2rem;
        padding-left: 8px;
        border-radius: 0vmin;
        font-family: "ProFont";
        font-size: var(--font-artist);
        background-color: var(--bg);
        color: var(--secondary);
    }

    .navitem:hover {
        background: #2C7B6166;
    }

    .navitem.active {
        background: #2C7B6122;
        color: var(--accent);
        border-left: 4px solid var(--primary);
        padding-left: 3px;
    }

    .navitem:active {
        transform:scale(0.97);
    }

    .navicon {
        margin-right: 0.5rem;
        color: var(--primary);
    }
</style>
