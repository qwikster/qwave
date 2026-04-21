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
    }

    .main {
        display: grid;
        flex-direction: column;
        flex: 1;
        overflow: hidden;
    }

    .top {
        display: flex;
    }

    .bottom {
        display: flex;
    }

    @media (max-width: 540px) {
        .main {
            display: flex;
            flex-direction: column-reverse;
        }

        .top {
            flex-direction: column;
        }
    }
</style>
