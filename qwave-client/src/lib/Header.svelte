<script>
    import logo from "/src/assets/logo_lg.png"
</script>

<header>
    <img src="{logo}" alt="n" width="140px" class="logo">
    <input id="search" type="search" class="search" placeholder=" SEARCH..." />
    <span class="clock">10:10PM</span>
</header>

<style>
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
        padding: 0.5rem;
    }

    .clock {
        border: 3px solid var(--dim);
        color: var(--dim);
        padding: 0.2rem;
        font-size: 20px;
    }
</style>
