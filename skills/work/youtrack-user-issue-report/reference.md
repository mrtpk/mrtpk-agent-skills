# YouTrack MCP — reference & gotchas

## Environment
- Find the YouTrack MCP tools by name (`search_users`, `advanced_search`, `get_issue_raw`). When the client
  exposes MCP servers as a dynamic-tool namespace, discover it with `GetDynamicTools` using
  `{ "pattern": "youtrack" }`.
- Base URL: `<YOUTRACK_URL>`, the URL of your YouTrack instance. The MCP does not expose it. Read it from the
  MCP configuration of the client, or ask the user.
- Issue link format: `<YOUTRACK_URL>/issue/<idReadable>`
  (e.g. `.../issue/PROJ-803`). `idReadable` is the human key like `PROJ-803`; the
  internal `id` looks like `3-3587` — use `idReadable` for links.
- With a dynamic-tool namespace, call `GetDynamicTools` (namespace + toolName) to read
  the schema, then `CallDynamicTool`. Large results can be written to a file;
  read/parse it with the Read tool, `grep`, or `jq`.

## Gotchas (each caused rework)
1. **`search_issues` caps at ~100 and returns only IDs.** Use `advanced_search`
   (`limit: 500`) or `search_with_filter` for a complete list with `idReadable`
   and `summary`.
2. **Search strips custom-field values.** State/Assignee etc. come back as bare
   `$type` with no value. State is only reliably available from `get_issue_raw`.
3. **Search is non-deterministic.** The same query returned different result sets
   across calls (16 then 5). Verify counts; cross-check against a user-supplied
   count; re-run if numbers disagree.
4. **`#Unresolved` is not portable across projects.** "In Review" is a *resolved*
   state in one project (`PROJA`) but *open* in others (`PROJB`, `PROJC`). Categorize by the real State field
   value, never by the resolved flag.
5. **State-bucketing (`State: {X}`) is an unreliable cross-check only** — inherits
   the non-determinism above. Do not use it for the authoritative answer.
6. Issues can span multiple projects (`PROJA`, `PROJB`, ...). Group by project
   prefix of `idReadable` when useful.

## Useful tools
- `search_users` — resolve a name/email fragment to an exact login/email.
- `get_current_user` — confirm the caller identity.
- `advanced_search` / `search_with_filter` — full lists (high `limit`).
- `get_issue_raw` — authoritative per-issue State + fields.
- `get_issue_comments` — issue discussion (used by contributor-work-profile).

## Subagent prompt template (for 50+ issues)

Delegate the heavy `get_issue_raw` fetches to a general-purpose subagent:

> You have the YouTrack MCP tools (namespace: <namespace, if the client uses one>).
> For each of these issue IDs: <ordered list>. For each, call `get_issue_raw` and
> read the real `State` field value. Write `<output file>` as a markdown table
> `Issue | Summary | State` where Issue is a link
> `<YOUTRACK_URL>/issue/<idReadable>`, preserving the given order.
> Add a total and a by-state count line at the top. Return only: total count and the
> by-state breakdown. Do not paste the whole table back.
