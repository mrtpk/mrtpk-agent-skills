---
name: youtrack-user-issue-report
description: >-
  Enumerate every YouTrack issue assigned to a person and report each issue's
  real workflow State, then write a markdown file with linked issue IDs and a
  by-state count. Use when asked to list the issues assigned to a user (e.g.
  "all issues assigned to X", "my YouTrack issues with their states",
  "which of my issues are open / in progress / blocked / not done").
---

# YouTrack User Issue Report

Produce a complete, count-verified list of the issues assigned to a user, each
with its true workflow State, written to a markdown file.

This skill needs a YouTrack MCP server. Read
[reference.md](reference.md) for how to find its tools, the base URL, the link format, and
the non-obvious gotchas — those gotchas caused repeated rework, so follow them.

## Inputs

- **user**: a login or email (e.g. `jdoe@example.com`) or a display name. Never
  hardcode a specific user — take it from the request.
- **output file**: the markdown path the user names (default
  `<user>-issues.md` in the workspace root).
- **expected count** (optional): if the user gives a manual count, verify against it.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Resolve the user (login/email) via search_users
- [ ] 2. Get the COMPLETE issue list (advanced_search / search_with_filter, high limit)
- [ ] 3. Verify the count (against the user's number if given)
- [ ] 4. Fetch the true State for every issue via get_issue_raw
- [ ] 5. Write the markdown report + by-state breakdown
- [ ] 6. Verify the file row count == issue count
```

**1. Resolve the user.** `search_users` with the name/email fragment to get the
exact login/email (e.g. `jdoe` → `jdoe@example.com`). Use the exact value in queries.

**2. Get the complete list.** `search_issues` caps at ~100 and returns only IDs.
Use `advanced_search` (query `assignee: <email>`, `limit: 500`) or
`search_with_filter` to get all issues. Capture `id`, `idReadable`, and `summary`.

**3. Verify the count.** The MCP search is non-deterministic across calls — do not
trust one call. Count `idReadable` entries; if the user gave a manual count, they
must match. If not, re-run and reconcile before continuing.

**4. Fetch true State.** Search responses STRIP custom-field values (State appears
as only a `$type`), so State is NOT available from search. `get_issue_raw` returns
the real State per issue — this is the authoritative source.
- Do NOT categorize by the `#Unresolved` flag: "In Review" can be a *resolved* state in
  one project but *open* in another, so `#Unresolved` misclassifies across
  projects. Always report the actual State field value.
- State-bucketing queries (`State: {In Progress}`) are an unreliable cross-check
  only (they returned 16 then 5 for the same query today) — never rely on them for
  the final answer.
- For large sets (roughly 50+ issues), delegate the many `get_issue_raw` calls to a
  general-purpose subagent to keep context clean. Give it the exact ordered ID list,
  the output format below, and the base URL; have it write the file directly and
  return only a compact confirmation + by-state counts. See the subagent prompt
  template in [reference.md](reference.md).

**5. Write the report.** Use the template below. Build links as
`<YOUTRACK_URL>/issue/<idReadable>` (see [reference.md](reference.md) for `<YOUTRACK_URL>`).

**6. Verify.** Count the data rows in the file; it must equal the issue count.

## Output template

```markdown
# YouTrack issues assigned to <Display Name> (`<email>`)

Total: **<N>** issues. Source: YouTrack (`<YOUTRACK_URL>`), State from `get_issue_raw`.

By state: <State A> (<n>), <State B> (<n>), ...

| Issue | Summary | State |
| --- | --- | --- |
| [<idReadable>](<YOUTRACK_URL>/issue/<idReadable>) | <summary> | <State> |
```

Preserve the search order (e.g. newest-created first) unless the user asks otherwise.

## Common follow-ups

Users often then ask to filter this report (e.g. exclude one project or topic,
keep only Open/Blocked, or split by state into separate tables/files). Filter from
the already-written report file rather than re-querying, and keep the by-state /
totals accurate whenever rows are added or removed.

## Communication style

Apply these rules to all text that this skill produces (the report and the replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
