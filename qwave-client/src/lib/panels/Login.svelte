<script>
    import { activeTab, activePanel } from "../stores/ui";
    import { api } from "../stores/api"

    let username = ""
    let password = ""
    let rusername = ""
    let rpassword = ""
    let error = ""
    let rerror = ""
    let loading = false

    async function login() {
      error = ""
      loading = true
      try {
        const res = await api.login(username, password)
        localStorage.setItem("token", res.token)
        activeTab.set("nav")
        activePanel.set("songs")
        console.log(res)
      } catch {
        error = "Invalid username or password"
      } finally {
        loading = false
      }
    }

    async function register() {
      error = ""
      loading = true
      try {
        const res = await api.register(rusername, rpassword)
        localStorage.setItem("token", res.token)
        activeTab.set("nav")
        activePanel.set("songs")
        console.log(res)
      } catch {
        rerror = "Invalid username or password"
      } finally {
        loading = false
      }
    }
</script>

<div class="login">
    <div class="title">LOG IN OR REGISTER</div>
    <div class="login-box">
        <input bind:value={username} type="text" placeholder="USERNAME" disabled={loading} />
        <input bind:value={password} type="password" placeholder="PASSWORD" disabled={loading} on:keydown={e => e.key === "Enter" && login()} />
        <button on:click={login} disabled={loading}>
            {loading ? '...' : "LOGIN"}
        </button>
        {#if error}
        <div class="error">{error}</div>
        {/if}
    </div>
    <hr>
    <div class="register-box">
        <input bind:value={rusername} type="text" placeholder="USERNAME" disabled={loading} />
        <input bind:value={rpassword} type="password" placeholder="PASSWORD" disabled={loading} on:keydown={e => e.key === "Enter" && register()} />
        <button on:click={register} disabled={loading}>
            {loading ? '...' : "REGISTER"}
        </button>
        {#if rerror}
        <div class="error">{error}</div>
        {/if}
    </div>
</div>


<style>
    .login {
        display: flex;
        flex-direction: column;
        place-items: center;
        justify-content: center;
        flex: 1;
    }

    .login-box, .register-box {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        min-width: 20vw;
    }

    .title {
        color: var(--primary);
        font-size: var(--font-titles);
        margin-bottom: 0.5rem;
    }

    .error {
        color: var(--accent);
        font-size: var(--font-info);
        text-align: center;
    }

    input {
        font-family: "ProFont";
        font-size: var(--font-artist);
        text-align: center;
        background: var(--bg);
        color: var(--primary);
        border: var(--border-small) solid var(--dim);
        padding: 0.2rem;
        width: 42vw;
    }

    input:focus { outline: none; border-color: var(--primary); }

    button {
        font-family: "ProFont";
        font-size: var(--font-artist);
        background: var(--dim);
        color: var(--accent);
        border-color: var(--primary);
        border-width: var(--border-small);
    }

    button:hover { background: #FF499E22; }

    hr { width: 90%; border: 0.3vh solid var(--dim); }
</style>
