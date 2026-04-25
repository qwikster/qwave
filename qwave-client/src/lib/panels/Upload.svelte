<script>
    import * as mm from "music-metadata"
    import { writeID3 } from "../id3";
    import { slide } from "svelte/transition";

    let file = null
    let meta = { title: "", artist: "", album: "", track: "", year: "" }
    let status = ""
    let loading = false
    let error = ""

    async function onFileChange(e) {
      file = e.target.files[0]
      if (!file) return
      error = ""
      meta = { title: "", artist: "", album: "", track: "", year: "" }

      try {
        const parsed = await mm.parseBlob(file)
        const t = parsed.common
        meta.title =  t.title  ?? ""
        meta.artist = t.artist ?? ""
        meta.album =  t.album  ?? ""
        meta.track =  t.track?.no?.toString() ?? ""
        meta.year =   t.year?.toString() ?? ""
      } catch {} // unreadable
    }

    async function upload() {
      if (!file) return
      loading = true
      error = ""
      status = "writing tags..."

      try {
        const token = localStorage.getItem("token")
        let uploadFile

        if (file.type === "audio/mpeg" || file.name.endsWith(".mp3")) {
          uploadFile = await writeID3(file, meta)
        } else {
          uploadFile = file
        }

        status = "uploading..."
        const form = new FormData()
        form.append("file", uploadFile)

        const res = await fetch("/api/tracks/upload", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: form,
        })

        if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
        const data = await res.json()

        status = `done!! id: ${data.track_id}`
        file = null
        meta = { title: "", artist: "", album: "", track: "", year: "" }
      } catch (e) {
        error = e.message
        status = ""
      } finally {
        loading = false
      }
    }
</script>

<div class="upload">
    <label class="file-input-wrapper" class:disabled={loading}>
        {file ? file.name : "Pick an audio file..."}
        <input type="file" accept="audio/*" on:change={onFileChange} disabled={loading} />
    </label>

    {#if file}
        <div class="meta-form" transition:slide>
            <label>TITLE<input type="text" bind:value={meta.title} disabled={loading} /></label>
            <label>ARTIST<input type="text" bind:value={meta.artist} disabled={loading} /></label>
            <label>ALBUM<input type="text" bind:value={meta.album} disabled={loading} /></label>
            <div class="row">
                <label>TRACK<input type="number" bind:value={meta.track} disabled={loading} /></label>
                <label>YEAR<input type="number" bind:value={meta.year} disabled={loading} /></label>
            </div>
            <button on:click={upload} disabled={loading}>
                {loading ? "..." : "UPLOAD"}
            </button>
        </div>
    {/if}

    {#if status}
        <div class="status">{status}</div>
    {/if}
    {#if error}
        <div class="error">{error}</div>
    {/if}
</div>

<style>
    .upload {
        display: flex;
        flex-direction: column;
        padding: 0.5rem;
        align-items: center;
    }

    label {
        display: block;
        font-size: var(--font-artist);
        color: var(--dim);
        margin-top: 0.2rem;
    }

    input[type="text"], input[type="number"] {
        width: 100%;
        min-width: 0;
        font-family: "ProFont";
        font-size: var(--font-artist);
        background: var(--bg);
        color: var(--primary);
        border: var(--border-small) solid var(--dim);
        padding: 0.1rem;
        padding-left: 0.3rem;
        box-sizing: border-box;
    }

    input[type="file"] {
        display: none;
    }

    .file-input-wrapper {
        display: block;
        font-family: "ProFont";
        font-size: var(--font-artist);
        background: var(--dimmer);
        color: var(--secondary);
        border: var(--border-small) solid var(--dimish);
        padding: 0.2rem 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        box-sizing: border-box;
        max-width: 55vw;
    }

    .file-input-wrapper:hover { border-color: var(--primary); background: var(--dim); color: var(--accent); }

    input:focus { outline: none; border-color: var(--primary); }

    .row {
        display: flex;
        gap: 0.8rem;
        justify-content: center;
        margin: 0.2rem 0rem;
        max-width: 55vw;
    }

    button {
        font-family: "ProFont";
        font-size: var(--font-artist);
        background: var(--dimmer);
        color: var(--secondary);
        border: var(--border-small) solid var(--dimish);
        cursor: pointer;
        padding: 0.2rem 1rem;
        width: 100%;
        margin: 0.2rem 0rem;
        transition: all 0.2s;
    }

    button:hover { border-color: var(--primary); background: var(--dim); color: var(--accent); }
    button:disabled { opacity: 0.5; cursor: default; }

    .status { color: var(--primary); font-size: var(--font-info); }
    .error { color: var(--accent); font-size: var(--font-info); }

</style>
