<script>
    import { onDestroy, onMount } from "svelte";
    import { analyser, audioctx } from "./stores/audio";

    // =tuning=
    const BAR_COUNT = 16
    const SEG_COUNT = 32
    const SEG_GAP   = 0.15 // fraction of segH
    const SMOOTHING = 0.85 // 0 (fast) to 1 (slow)
    const HI_COLOR  = "#FF499E"
    const MID_COLOR = "#FFC60A"
    const LOW_COLOR = "#14F5AA"
    const PEAK_HOLD = 30  // frames
    const PEAK_FALL = 0.2 // segments per frame
    const MID_THRES = 0.5
    const HI_THRES  = 0.75
    // ========

    let canvas
    let raf
    let peaks = new Array(BAR_COUNT).fill(0)
    let peakHold = new Array(BAR_COUNT).fill(0)

    analyser.fftSize = 4096
    analyser.smoothingTimeConstant = SMOOTHING

    const bufferLength = analyser.frequencyBinCount
    const data = new Uint8Array(bufferLength)

    function bcolor(fraction) {
      if (fraction >= HI_THRES) return HI_COLOR
      if (fraction >= MID_THRES) return MID_COLOR
      return LOW_COLOR
    }

    function draw() {
      raf = requestAnimationFrame(draw)
      if (!canvas) return

      analyser.getByteFrequencyData(data)

      const ctx = canvas.getContext("2d")
      const W = canvas.width
      const H = canvas.height

      ctx.clearRect(0, 0, W, H)

      const barW = W / BAR_COUNT
      const segH = H / SEG_COUNT
      const gap = segH * SEG_GAP

      ctx.fillStyle = "#000000"
      ctx.fillRect(0, 0, W, H)

      const minFreq = 20
      const maxFreq = audioctx.sampleRate / 2
      const freqRange = Math.log(maxFreq / minFreq)

      for (let b = 0; b < BAR_COUNT; b++) {
        const targetFreq = minFreq * Math.exp((b / BAR_COUNT) * freqRange)
        const binIndex = Math.floor(targetFreq / (audioctx.sampleRate / analyser.fftSize))
        const value    = data[Math.min(binIndex, bufferLength - 1)] / 255
        const filled   = Math.round(value * SEG_COUNT)

        if (filled >= peaks[b]) {
          peaks[b] = filled
          peakHold[b] = PEAK_HOLD
        } else {
          if (peakHold[b] > 0) {
            peakHold[b]--
          } else {
            peaks[b] = Math.max(0, peaks[b] - PEAK_FALL)
          }
        }

        const x = b * barW
        const peakSeg = Math.floor(peaks[b])

        for (let s = 0; s < filled; s++) {
          const fraction = s / SEG_COUNT
          const y = H - (s + 1) * segH
          ctx.fillStyle = bcolor(fraction)
          ctx.fillRect(x + 1, y + gap, barW - 2, segH - gap)
        }

        if (peakSeg > 0 && peakSeg < SEG_COUNT) {
          const fraction = peakSeg / SEG_COUNT
          const y = H - (peakSeg + 1) * segH
          ctx.fillStyle = bcolor(fraction)
          ctx.fillRect(x + 1, y + gap, barW - 2, segH - gap)
        }
      }
    }

    onMount(() => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight

      const ro = new ResizeObserver(() => {
        canvas.width = canvas.offsetWidth
        canvas.height = canvas.offsetHeight
      })
      ro.observe(canvas)
      draw()
      return () => ro.disconnect()
    })

    onDestroy(() => cancelAnimationFrame(raf))

</script>

<div class="visualizer">
    <canvas bind:this={canvas}></canvas>
</div>

<style>
    canvas {
        width: 100%;
        height: 100%;
        display: block;
    }

    .visualizer {
        grid-area: visualizer;
        border: var(--border-tile) solid var(--primary);
        margin: 0.2rem;
        overflow: hidden;
    }

    @media (max-width: 540px) {
        .visualizer { min-height: 8vh; grid-column: span 2; }
    }
    @media (max-height: 540px) and (max-width: 540px) {
        .visualizer { display: none; }
    }
</style>
