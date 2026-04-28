import Login from "../panels/Login.svelte"
import { activeTab } from "./ui"

export const BASE = import.meta.env.DEV ? "/api" : ""

async function get(path) {
  const token = localStorage.getItem("token")
  const res = await fetch(BASE + path, {
    method: "GET",
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  })
  if (res.status == 401) activeTab.set("login")
  if (!res.ok) throw new Error(`${res.status} ${path}`)
  return res.json()
}

async function post(path, body) {
  const token = localStorage.getItem("token")
  const res = await fetch(BASE + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? {Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(body)
  })
  if (!res.ok) throw new Error(`${res.status} ${path}`)
  return res.json()
}

export const api = {
  tracks: (params = {}) => get("/tracks?" + new URLSearchParams(params)),
  track: (id) => get(`/tracks/${id}`),
  albums: (params = {}) => get("/albums?" + new URLSearchParams(params)),
  album: (id) => get(`/albums/${id}`),
  artists: (params = {}) => get("/artists?" + new URLSearchParams(params)),
  artist: (id) => get(`/artists/${id}/tracks`),
  artistName: (id) => get(`/artists/${id}`),
  search: (query, type = "all") => get(`/search?query=${encodeURIComponent(query)}&type=${type}`),
  stream: (id) => `${BASE}/stream/${id}`,
  me: () => get("/auth/me"),
  login: (username, password) => post("/auth/login", { username, password }),
  register: (username, password) => post("/auth/register", { username, password }),
  logout:  () => post("/auth/logout", {}),
}
