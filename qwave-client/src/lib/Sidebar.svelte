<script>
    import { activePanel } from "./stores/ui.js";
</script>

<aside class="sidebar">
    <nav>
        <button class:active={$activePanel === "songs"} class="navitem" on:click={() => $activePanel = "songs"}>
            <span class="navicon">󰎇</span><span class="navlink">SONGS</span>
        </button>
        <button class:active={$activePanel === "artists"} class="navitem" on:click={() => $activePanel = "artists"}>
            <span class="navicon"></span><span class="navlink">ARTISTS</span>
        </button>
        <button class:active={$activePanel === "albums"} class="navitem" on:click={() => $activePanel = "albums"}>
            <span class="navicon"></span><span class="navlink">ALBUMS</span>
        </button>
        <button class:active={$activePanel === "playlists"} class="navitem" on:click={() => $activePanel = "playlists"}>
            <span class="navicon">󰐑</span><span class="navlink">PLAYLISTS</span>
        </button>
        <button class:active={$activePanel === "recent"} class="navitem" on:click={() => $activePanel = "recent"}>
            <span class="navicon"></span><span class="navlink">RECENT</span>
        </button>
        <button class="navitem" on:click={() => null}>
            <span class="navicon"></span><span class="navlink">RANDOM</span>
        </button>
    </nav>
    <div class="sidebar-bottom">
        <hr>
        <button class:active={$activePanel === "settings"} class="navitem" on:click={() => $activePanel = "settings"}>
            <span class="navicon"></span><span class="navlink">SETTINGS</span>
        </button>
        <button class:active={$activePanel === "upload"} class="navitem" on:click={() => $activePanel = "upload"}>
            <span class="navicon"></span><span class="navlink">UPLOAD</span>
        </button>
    </div>
</aside>

<style>
    hr {
        border: 1px solid var(--dim);
        margin: 0.2rem;
    }

    .sidebar {
        min-height: 50vh;
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

    nav {
        display: flex;
        flex-direction: column;
        overflow: hidden;
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
