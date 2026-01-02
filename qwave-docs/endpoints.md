<h1>qWave Server Endpoints (subject to change)</h1>
<h5>(expect auth required when not listed)</h5>
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
    <tr><td>Body    </td><td>{"username": "string", "password": "string"}</td></tr>
    <tr><td>Response</td><td>{"token": "uuid", "user_id": int, "expires_at": "timestamp"}</td></tr>
    <tr><td>Actions </td><td>Verify hash, generate token, create 30d db entry, return token</td></tr>
</tbody></table>

<h3><code>POST /auth/logout</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Token in header</td></tr>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>Delete token from db</td></tr>
</tbody></table>

<h3><code>GET /auth/me</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"user_id": int, "username": "string", "created_at": "timestamp"}</td></tr>
    <tr><td>Actions </td><td>Lookup token in db</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Tracks</h2></summary>

<h3><code>GET /tracks</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>artist_id (int), album_id (int), genre_id (int), added_by (int), date_from (ISO), date_to (ISO), limit (int, default 100), offset (int, default 0)</td></tr>
    <tr><td>Response</td><td>{"tracks": [{"id": int, "title": "string", "duration": intm "artists": [{"id": int, "name": "string", "is_primary": bool}], "album": {"id": int, "title": "string"} or null, "added_date": "timestamp"}], "total": int}</td></tr>
    <tr><td>Actions </td><td>Query and filter db, join artist and album tables, return results. use /search for specific songs</td></tr>
</tbody></table>

<h3><code>GET /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"id": int, "title": "string", "duration": int, "track_number": int or null, "artists": [{"id": int, "name": "string", "is_primary": bool}], "album": {"id": int, "title": "string", "release_date": "date"} or null, "genres": [{"id": int, "name": "string"}], "lyrics": "string" or null, "added_date": "timestamp", "added_by": {"id": int, "username": "string"}}</td></tr>
    <tr><td>Actions </td><td>query db for track</td></tr>
</tbody></table>

<h3><code>POST /tracks/upload</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>Audio file, max 200MB</td></tr>
    <tr><td>Response</td><td>{"job_id": int, "Track_id": int, "status": "pending"}</td></tr>
    <tr><td>Actions </td><td>Validate file type and size, save to temp, extract metadata (`mutagen`), search MusicBrainz, create track record and file paths, create job record, return job ID</td></tr>
</tbody></table>

<h3><code>PATCH /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>all optional fields like {"title": "string"} to update</td></tr>
    <tr><td>Response</td><td>(full track object as in GET /tracks/{id})</td></tr>
    <tr><td>Actions </td><td>patch it lmao</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Uploader</td></tr>
    <tr><td>Response</td><td>{"message": "status", "id": int}</td></tr>
    <tr><td>Actions </td><td>delete both files and all related db records, delete related jobs</td></tr>
</tbody></table>

<h3><code>GET /tracks/{id}/artists</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"artists": [{"id": int, "name": "string", "is_primary": bool}]}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>POST /tracks/{id}/artists</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"artist_id": int, "is_primary": bool}</td></tr>
    <tr><td>Response</td><td>{"message": "status", "track_id": int, "artist": {"id": int, "name": "string"}}</td></tr>
    <tr><td>Actions </td><td>add entry</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}/artists/{artist_id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>delete entry from track_artsts junction table</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Albums</h2></summary>

<h3><code>GET /albums</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>artist_id (int), year (int), limit (int), offset (int)</td></tr>
    <tr><td>Response</td><td>{"albums": [{"id": int, "title": "string", "release_date": "date" or null, "album_artist": {"id": int, "name": "string"} or null, "track_count": int}], "total": int}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>GET /albums/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"id": int, "title": "string", "release_date": "date" or null, "album_artist": {"id": "name": "string"} or null, "tracks": [{"id": int, "title": "string", "track_number": int, "duration": int, "artists": [...]}]}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>PATCH /albums/{id}</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"title": "string", "release_date": "date"} (optional)</td></tr>
    <tr><td>Response</td><td>{"id": int, "updated_fields": ["title", ...], "album": {...album object...}}</td></tr>
    <tr><td>Actions </td><td>update db</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Artists</h2></summary>

<h3><code>GET /artists</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>limit (int), offset (int)</td></tr>
    <tr><td>Response</td><td>{"artists": [{"id": int, "name": "string", "track_count": int, "album_count": int}], "total" int}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"id": int, "name": "string", "track_count": int, "album_count": int}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}/tracks</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>limit (int), offset (int)</td></tr>
    <tr><td>Response</td><td>{"tracks": [{"id": int, "title": "string", "duration": int, "album": {...} or null}], "total": int}</td></tr>
    <tr><td>Actions </td><td>query db (all tracks with artist in track_artists)</td></tr>
</tbody></table>

<h3><code>GET /artists/{id}/albums</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"albums": [{"id": int, "title": "string", "release_date": "date", "track_count": int}]}</td></tr>
    <tr><td>Actions </td><td>query albums where artist is album_artist or appears on any track</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Genres</h2></summary>

<h3><code>GET /genres</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"genres": [{"id": int, "name": "string", "track_count": int}]}</td></tr>
    <tr><td>Actions </td><td>query db</td></tr>
</tbody></table>

<h3><code>POST /genres</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"name": "string"}</td></tr>
    <tr><td>Response</td><td>{"id": int, "name": "string"}</td></tr>
    <tr><td>Actions </td><td>Create a genre if it doesn't exist and return</td></tr>
</tbody></table>

<h3><code>GET /genres/{id}/tracks</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>limit (int), offset (int)</td></tr>
    <tr><td>Response</td><td>{"tracks": [{"id": int, "title": "string", "artists": [...], "duration": int}], "total": int}</td></tr>
    <tr><td>Actions </td><td>query db via track_genres table</td></tr>
</tbody></table>

<h3><code>POST /tracks/{id}/genres</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"genre_id": int}</td></tr>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>create entry</td></tr>
</tbody></table>

<h3><code>DELETE /tracks/{id}/genres/{genre_id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>delete entry</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Playlists</h2></summary>

<h3><code>GET /playlists</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>user_id (int - optional, defaults to current</td></tr>
    <tr><td>Response</td><td>{"playlists": [{"id": int, "name": "string", "is_public": bool, "owner": {"id": int, "username": "string"}, "track_count": int, "created_at": "timestamp"}]}</td></tr>
    <tr><td>Actions </td><td>query playlists where owner is current or is_public = true</td></tr>
</tbody></table>

<h3><code>GET /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"id": int, "name": "string", "is_public": bool, "owner": {"id": int, "username": "string"}, "tracks": [{"id": int, "title": "string", "artists": [...], "duration": int, "position": int}], "created_at": "tmestamp"}</td></tr>
    <tr><td>Actions </td><td>Verify user owns or is_public, query tracks by position</td></tr>
</tbody></table>

<h3><code>POST /playlists</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"name": "string", "is_public": bool}</td></tr>
    <tr><td>Response</td><td>{"id": int, "name": "string", "is_public": bool, "owner": {"id": int, "username": "string"}, "created_at": "timestamp"}</td></tr>
    <tr><td>Actions </td><td>create db entry</td></tr>
</tbody></table>

<h3><code>PATCH /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Must be owner of playlist</td></tr>
    <tr><td>Body    </td><td>{"name": "string", "is_public": bool} (both optional)</td></tr>
    <tr><td>Response</td><td>{"id": int, "updated_fields": ["name"], "playlist": {...playlist object...}}</td></tr>
    <tr><td>Actions </td><td>Update db entry</td></tr>
</tbody></table>

<h3><code>DELETE /playlists/{id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Must be owner of playlist</td></tr>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>delete and cascade delete playlist_tracks entries</td></tr>
</tbody></table>

<h3><code>POST /playlists/id/{tracks}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Must be owner of playlist</td></tr>
    <tr><td>Body    </td><td>{"track_id": int} or {"track_ids": [int, int, ...]}</td></tr>
    <tr><td>Response</td><td>{"message": "status", "positions": [int, int]}</td></tr>
    <tr><td>Actions </td><td>Append track(s) at max pos</td></tr>
</tbody></table>

<h3><code>DELETE /playlists/{id}/tracks/{track_id}</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Must be owner of playlist</td></tr>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>delete entry, reorder rest of tracks</td></tr>
</tbody></table>

<h3><code>PUT /playlists/{id}/reorder</code></h3>
<table><tbody>
    <tr><td>Auth    </td><td>Must be owner of playlist</td></tr>
    <tr><td>Body    </td><td>{"track_order": [int, int, int...]} (track IDs in order)</td></tr>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>Check that all IDs are present and reorder by array order</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Search</h2></summary>

<h3><code>GET /search</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>query (string), type (string: "tracks", "albums", "all", default "all), limit (int)</td></tr>
    <tr><td>Response</td><td>{"tracks": [{"id": int, "title": "string", "artists": [...]}], "albums": [{"id": int, "title": "string"}], "artists": [{"id": int, "name": "string"}]}</td></tr>
    <tr><td>Actions </td><td>Use SQLite FTS5 on tracks.title, match against albums.title andartists.name using LIKE, return grouped by type</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Streaming</h2></summary>

<h3><code>GET /stream/{track_id}</code></h3>
<table><tbody>
    <tr><td>Header  </td><td>Range: bytes=0-1023 (optional for seeking)</td></tr>
    <tr><td>Response</td><td>Audio bytes with headers <code>Content-Type: audio/opus, Content-Length: int, Accept-Ranges: bytes, Content-Range: bytes 0-1023/total</code> (if range requested)</td></tr>
    <tr><td>Actions </td><td>Look up track opus_path, open, if Range header is present extract start-end bytes and 206, otherwise 200 and return/stream full file bytes</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Jobs</h2></summary>

<h3><code>GET /jobs/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"id": int, "type": "transcode", "status": "running", "track_id": int, "created_at": "timestamp", "started_at": "timestamp" or null, "completed_at": "timestamp" or null, "error_message": "string" or null}</td></tr>
    <tr><td>Actions </td><td>query record</td></tr>
</tbody></table>

<h3><code>GET /jobs</code></h3>
<table><tbody>
    <tr><td>Params  </td><td>{status (string: "pending", "running", "complete", "failed"), limit (int), offset (int)}</td></tr>
    <tr><td>Response</td><td>{"jobs": [{"id": int, "type": "string", "status": "string", "track_id": int, "created_at": "timestamp"}], "total": int}</td></tr>
    <tr><td>Actions </td><td>query jobs and filter by status if provided</td></tr>
</tbody></table>

<h3><code>DELETE /jobs/{id}</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"message": "status"}</td></tr>
    <tr><td>Actions </td><td>if status pending, delete job and track record. If running or complete, error</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Import Review</h2></summary>

<h3><code>GET /import/pending</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"pending_tracks": [{"id": int, "filename": "string", "guessed_title": "string", "guessed_artist": "string", "needs_review": bool}]}</td></tr>
    <tr><td>Actions </td><td>Query tracks where needs_review is true, return list</td></tr>
</tbody></table>

<h3><code>PATCH /import/pending/{track_id}</code></h3>
<table><tbody>
    <tr><td>Body    </td><td>{"title": "string", "artist_name": "string", "album_title": "string" or null, "track_number": int or null}</td></tr>
    <tr><td>Response</td><td>{"message": "status", "job_id": int}</td></tr>
    <tr><td>Actions </td><td>Update metadata, set needs_review false, create/find album records, create track_artists entry, create transcode job</td></tr>
</tbody></table>
</details>

<details>
<summary><h2>Server Details</h2></summary>

<h3><code>GET /server/info</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"name": "string", "theme_colors": {"primary": "#hex", "secondary": "#hex"}, "logo_url": "string" or null, "background_url": "string" or null}</td></tr>
    <tr><td>Actions </td><td>read config.yaml</td></tr>
</tbody></table>

<h3><code>GET /server/config</code></h3>
<table><tbody>
    <tr><td>Response</td><td>{"opus_bitrate": int, "acoustid_enabled": bool, "max_upload_size_mb": 200}</td></tr>
    <tr><td>Actions </td><td>read config.yaml</td></tr>
</tbody></table>
</details>