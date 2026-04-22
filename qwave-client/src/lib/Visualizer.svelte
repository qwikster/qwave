<script></script>

<div class="visualizer">
    <span></span>
</div>

<style>
    .visualizer {
        background: var(--black);
        grid-column: 1;
        flex-shrink: 0;
        border: var(--border-tile) solid var(--primary);
        margin: 0.2rem;
        gap: 1rem;
        padding: 0.5rem;

        color: var(--accent);
    }

    @media (max-width: 540px) {
        .visualizer { min-height: 8vh; }
    }
    @media (max-height: 540px) and (max-width: 540px) {
        .visualizer { display: none; }
    }
</style>
