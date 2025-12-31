<details>
<summary><h2>Authentication</h2></summary>

<h3>`POST /auth/register`</h3>
<table>
    <!-- <thead>
        <tr><th>Property</th></tr>
    </thead> -->
    <tbody>
        <tr><td>Auth    </td><td>None</td></tr>
        <tr><td>Body    </td><td>{"username": "string", "password": "string"}</td></tr>
        <tr><td>Response</td><td>{"user_id": int, "username": "string", "created_at": "timestamp"}</td></tr>
        <tr><td>Actions </td><td>Hash password (bcrypt), add db entry, return info (not session)</td></tr>
    </tbody>
</table>

</details>