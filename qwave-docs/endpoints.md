<details>
<summary><h2>Authentication</h2></summary>

<h3><code>POST /auth/register</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{"username": "string", "password": "string"}</td></tr>
    <tr><td>Response</td><td>{"user_id": int, "username": "string", "created_at": "timestamp"}</td></tr>
    <tr><td>Actions </td><td>Hash password (bcrypt), add db entry, return info (not session)</td></tr>
</tbody></table>

<h3><code>POST /auth/login</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /auth/logout</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /auth/me</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Tracks</h2></summary>

<h3><code>GET /tracks</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /tracks/upload</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>PATCH /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /tracks/{id}/artists</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /tracks/{id}/artists</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}/artists/{artist_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

</details>

<details>
<summary><h2>Albums</h2></summary>

<h3><code>GET /albums</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /albums/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>PATCH /albums/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Artists</h2></summary>

<h3><code>GET /artists</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}/tracks</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}/albums</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Genres</h2></summary>

<h3><code>GET /genres</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /genres</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /genres/{id}/tracks</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /tracks/{id}/genres</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}/genres/{genre_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Playlists</h2></summary>

<h3><code>GET /playlists</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /playlists</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>PATCH /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>POST /playlists/id/{tracks}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /playlists/{id}/tracks/{track_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>PUT /playlists/{id}/reorder</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Search</h2></summary>

<h3><code>GET /search</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Streaming</h2></summary>

<h3><code>GET /stream/{track_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Jobs</h2></summary>

<h3><code>GET /jobs/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /jobs</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>DELETE /jobs/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Import Review</h2></summary>

<h3><code>GET /import/pending</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>PATCH /import/pending/{track_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Server Details</h2></summary>

<h3><code>GET /server/info</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>

<h3><code>GET /server/config</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>None</td></tr>
    <tr><td>Body    </td><td>{}</td></tr>
    <tr><td>Response</td><td>{}</td></tr>
    <tr><td>Actions </td><td>a</td></tr>
</tbody></table>
</details>