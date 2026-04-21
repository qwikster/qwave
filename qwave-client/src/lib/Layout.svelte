<script>
    import Header from "./Header.svelte"
    import Sidebar from "./Sidebar.svelte"
    import Panel from "./Panel.svelte"
    import Visualizer from "./Visualizer.svelte"
    import NowPlaying from "./NowPlaying.svelte"
</script>

<div class="app">
    <Header />
    <div class="main">
        <div class="top">
            <Visualizer />
            <NowPlaying />
        </div>
        <div class="bottom">
            <Sidebar />
            <Panel />
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

    .main {
        display: grid;
        grid-template-columns: 200px 1fr;
        flex-direction: column;
        flex: 1;
        overflow: hidden;
    }

    .top {
        display: contents;
    }

    .bottom {
        display: contents;
    }
</style>
