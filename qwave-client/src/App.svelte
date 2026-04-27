<script>
  import { onMount } from "svelte"
  import Layout from "./lib/Layout.svelte"
  import { activePanel, activeTab } from "./lib/stores/ui.js"
  import { api } from "./lib/stores/api.js"

  onMount(async () => {
    const token = localStorage.getItem("token")
    if (!token) {
      activeTab.set("login")
      return
    }
    try {
      await api.me()
      activeTab.set("nav")
      activePanel.set("songs")
    } catch {
      localStorage.removeItem("token")
      activeTab.set("login")
    }
  })
</script>

<Layout />
