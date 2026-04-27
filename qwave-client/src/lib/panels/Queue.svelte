<script>
    import { queue } from "../stores/player";
    import { get } from "svelte/store";
</script>

{#each get(queue) as track}
<div>{track.title}</div>
{/each}
