---
name: outline-wiki-author-report
description: >-
  Enumerate every Outline wiki page authored by a person and write a grouped
  markdown report with dated links. Use when asked for the wiki/Outline
  documents created by a user (e.g. "wiki pages authored by X", "Outline docs
  I created", "list the pages me/<name> wrote").
---

# Outline Wiki Author Report

List all Outline wiki documents a person authored (by `createdBy`), then write a
grouped, dated markdown report with links.

This skill needs an Outline MCP server. Read [reference.md](reference.md) for
how to find its tools, the base URL, and gotchas.

## Inputs

- **author**: a name or email. Never hardcode a specific user — take it from the request.
- **output file**: the markdown path the user names (default `<user>-wikis.md`).

## Why this is not a one-liner

`list_documents` has **no author filter** and its default "recent feed" is capped
at 100 per page. A single call under-counts badly (it returned 18 docs when the
true author count was much higher). You MUST paginate the full corpus and then
filter locally on `createdBy.id`.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Resolve the author's user id via list_users
- [ ] 2. Page through ALL documents (offset 0,100,200,... until a short page)
- [ ] 3. Merge pages, filter on createdBy.id, dedupe by id
- [ ] 4. Write the grouped, dated markdown report
```

**1. Resolve the user id.** `list_users` with the name/email → capture the user's
UUID `id` (e.g. `6623bd3d-...`).

**2. Page through everything.** Call `list_documents` with `limit: 100` and
`offset` = 0, 100, 200, ... Large results can be saved to a file. Keep going until a page returns **fewer than 100** documents
(that's the last page). Count docs per page with
`grep -c '"document"' <file>` to know when to stop.

**3. Merge + filter + dedupe.** Run the helper script over all page files:

```bash
bash <this skill>/scripts/filter_author_docs.sh <userId> <page1.txt> <page2.txt> ...
```

It prints one TSV row per authored doc: `created<TAB>title<TAB>url<TAB>archived<TAB>breadcrumb`,
deduped by document id and sorted newest-first. See the script for details.

**4. Write the report.** Use the template below. Use the `url` field **directly
from the API** (do not construct wiki URLs by hand). Group by area/collection
(the `breadcrumb`) and mark archived/draft docs.

## Output template

```markdown
# Wiki pages authored by <Display Name> (`<email>`)

Source: Outline (`<OUTLINE_URL>`), filtered on `createdBy` across all
paginated documents. **<N>** documents authored.

## <Area / breadcrumb>
- [<title>](<url>) — <created date> <(archived) if applicable>
```

Verify the reported total equals the number of TSV rows from the script.

## Communication style

Apply these rules to all text that this skill produces (the report and the replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Reports and evaluations about a person use factual, neutral words.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
