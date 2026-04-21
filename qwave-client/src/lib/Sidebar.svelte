<script></script>

<aside class="sidebar">
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
        <div class="navitem">
            <span class="navicon"></span><span class="navlink">SETTINGS</span>
        </div>
        <hr>
        <div class="navitem">
            <span class="navicon"></span><span class="navlink">UPLOAD</span>
        </div>
    </div>
</aside>

<style>
    hr {
        border: 1px solid var(--dim);
        margin: 0.2rem;
    }

    .sidebar {
        min-width: 20vw;
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
        font-size: var(--font-artist)
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
</style>
