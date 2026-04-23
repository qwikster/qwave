<script>
    import { activeTab, activePanel } from "../stores/ui"
    import { api } from "../stores/api";

    async function logout() {
      try {
        const res = await api.logout()
        activeTab.set("login")
        activePanel.set("null")
        console.log(res)
      } catch {
        console.log("ERROR")
      }
    }
</script>

<button on:click={logout}>LOGOUT</button>

<style>
    button {
        font-family: "ProFont";
        font-size: var(--font-artist);
        background: var(--dim);
        color: var(--accent);
        border-color: var(--primary);
        border-width: var(--border-small);
    }

    button:hover { background: #FF499E22; }
</style>
