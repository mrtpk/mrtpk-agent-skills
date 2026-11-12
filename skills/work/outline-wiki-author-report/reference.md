# Outline wiki MCP — reference & gotchas

## Environment
- Find the Outline MCP tools by name (`list_users`, `list_documents`). When the client exposes MCP servers
  as a dynamic-tool namespace, discover it with `GetDynamicTools` using `{ "pattern": "outline|wiki" }`.
- Base URL: `<OUTLINE_URL>`, the URL of your Outline instance. Document URLs come straight from the
  API in `.document.url` — never construct them by hand.
- With a dynamic-tool namespace, call `GetDynamicTools` (schema) then `CallDynamicTool`. Large
  results can be written to a file; parse with `jq`/`grep`.

## Gotchas
1. **No author filter.** `list_documents` cannot filter by author; you filter
   locally on `.document.createdBy.id`.
2. **Recent feed is capped.** The unpaginated feed returns ~100 docs and looks
   complete but is not (it showed 18 vs a true 50). Always paginate.
3. **Paginate to exhaustion.** `limit: 100`, `offset` 0,100,200,...; stop when a
   page returns `< 100` documents.
4. `createdBy` vs `updatedBy`/collaborators: match on `createdBy.id` only, or you
   over-count docs the user merely edited.
5. Dedupe by `.document.id` when merging pages (feeds can overlap).

## Useful tools
- `list_users` — resolve a name/email to a user UUID.
- `list_documents` — paginated feed (`limit`, `offset`); includes `createdBy`.
- `list_collections` / `list_collection_documents` — collection trees, but the
  tree does NOT include author info, so it is not a shortcut for authorship.
- `fetch` — full content of a single document when needed.
