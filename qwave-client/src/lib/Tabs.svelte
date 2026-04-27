<script>
    import { activePanel, activeTab } from "./stores/ui"

    const mainTabs = ["nav", "queue", "lyrics"]
    const utilityTabs = ["login", "settings", "upload", "artist", "album"]

    $: showUtility = utilityTabs.includes($activeTab)
</script>

<div class="tabs-bar">
    <button class:active={$activeTab === "nav"} on:click={() => $activeTab = "nav"}>NAV</button>
    <button class:active={$activeTab === "queue"} on:click={() => $activeTab = "queue"}>QUEUE</button>
    <button class:active={$activeTab === "lyrics"} on:click={() => $activeTab = "lyrics"}>LYRICS</button>

    {#if showUtility}
        <div class="tab-divider"></div>
        <button class = "utility active" on:click={() => $activeTab = "nav"}>{$activeTab.toUpperCase()} </button>
    {/if}
</div>

<style>
    .tabs-bar {
        margin: 0 1vw -0.2vh 1vw;
        display: flex;
        gap: 0.3rem;
    }

    button {
        font-family: "ProFont";
        font-size: var(--font-info);
        background: var(--bg);
        color: var(--dim);
        border: var(--border-small) solid var(--dim);
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: none;
    }

    button:hover { color: var(--primary); background: var(--dim) }
    button.active { color: var(--primary); border-color: var(--primary)}

    .tab-divider {
        flex: 1;
    }

</style>
