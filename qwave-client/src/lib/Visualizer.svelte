<script></script>

<div class="visualizer">
    <span></span>
</div>

<style>
    .visualizer {
        background: var(--bg);
        grid-column: 1;
        flex-shrink: 0;
        border: var(--border-tile) solid var(--primary);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;
        min-width: 20vw;

        color: var(--accent);
    }

    @media (max-width: 540px) {
        @media (max-height: 540px) {
            .visualizer {
                display: none;
            }
        }
    }
</style>
