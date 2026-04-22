const BASE = "/api"

async function get(path) {
  const token = localStorage.getItem("token")
  const res = await fetch(BASE + path, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  })
  if (!res.ok) throw new Error(`${res.status} ${path}`)
  return res.json()
}

export const api = {
  tracks:  (params = {}) => get("/tracks?" + new URLSearchParams(params)),
  track:   (id) => get(`/tracks/${id}`),
  albums:  (params = {}) => get("/albums?" + new URLSearchParams(params)),
  album:   (id) => get(`/albums/${id}`),
  artists: (params = {}) => get("/artists?" + new URLSearchParams(params)),
  artist:  (id) => get(`/artists/${id}`),
  search:  (query, type = "all") => get(`/search?query=${encodeURIComponent(query)}&type=${type}`),
  stream:  (id) => `${BASE}/stream/${id}`
}
