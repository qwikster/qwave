<script>
    import { onMount } from "svelte"
    import { api } from "../stores/api"
    import { play, playNext, queueItem, currentTrack } from "../stores/player";

    let tracks = []
    let loading = true
    let error = ""

    onMount(async () => {
      try {
        const res = await api.tracks({ limit: 512 })
        tracks = res.tracks.sort((a, b) => a.title.localeCompare(b.title))
      } catch (e) {
        error = e.message
      } finally {
        loading = false
      }
    })

    function getDuration(seconds) {
      const m = Math.floor(seconds / 60).toString().padStart(2, "0")
      const s = Math.floor(seconds % 60).toString().padStart(2, "0")
      return `${m}:${s}`
    }

    function primaryArtist(track) {
      return track.artists.find(a => a.is_primary)?.name
        ?? track.artists[0]?.name
        ?? "Unknown"
    }

</script>
