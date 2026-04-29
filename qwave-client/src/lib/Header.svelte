<script>
    import logo from "/src/assets/logo_lg.png"
    let time = $state(new Date())

    $effect(() => {
      const interval = setInterval(() => {
        time = new Date()
      }, 1000);
      return () => clearInterval(interval)
    })
</script>

<header>
    <img src="{logo}" alt="n" class="logo">
    <input id="search" type="search" class="search" placeholder=" SEARCH..." />
    <span class="clock">{time.toLocaleTimeString()}</span>
</header>

<style>
    header {
        display: flex;
        align-items: stretch;
        padding: 0rem 0.2rem;
        margin: 0.2rem 0rem;
        flex: 1;
        user-select: none;
        max-height: 6vmin;
    }

    img {
        image-rendering: pixelated;
        width: 20.6vmin;
        height: 6vmin;
    }

    .search {
        flex-grow: 1;
        border: var(--border-tile) solid var(--dim);
        background-color: var(--bg);
        color: var(--primary);
        font-family: 'ProFont';
        font-size: var(--font-artist);
        padding: 0.2rem;
        margin: 0rem 0.4rem;
    }

    .search::placeholder {
        color: var(--dim);
        padding: 0.5rem;
    }

    .clock {
        color: var(--dim);
        font-size: var(--titles);
        padding: 1vmin;
        align-self: center;
    }
</style>
