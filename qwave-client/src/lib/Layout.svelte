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
        color: var(--secondary);
        font-family: 'ProFont', monospace;
        font-size: var(--font-titles);
        height: 90vh;
        overflow: hidden;
    }

    .main {
        display: grid;
        grid-template-columns: 24vmin 1fr;
        grid-template-rows: auto 1fr;
        grid-template-areas: "visualizer nowplaying" "sidebar panel";
        flex: 1;
        overflow: hidden;
        min-height: 0;
    }

    .top, .bottom {
        display: contents;
    }

    @media (max-width: 540px) {
        .main {
            grid-template-rows: 0.8fr auto auto 0.2fr;
            grid-template-areas: "sidebar panel" "nowplaying nowplaying" "visualizer visualizer";
        }
    }
</style>
