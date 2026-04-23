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
        background: var(--dimmer);
        color: var(--secondary);
        border: var(--dimish) solid var(--border-small);
        transition: 0.2s ease all;
    }

    button:hover { background: var(--dim); color: var(--accent); border-color: var(--primary); }
</style>
