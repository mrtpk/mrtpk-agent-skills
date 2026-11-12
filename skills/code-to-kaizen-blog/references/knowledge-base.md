# Knowledge base

The KB is the archive. The posts are a public view of it. The KB keeps what the posts must leave out.

## Rules

- Mark the KB "INTERNAL" in the first line. Keep it out of the blog repo.
- Give the snapshot: which folders and files, and the date you read them.
- Give the path root once ("all paths are relative to ...").
- One claim per bullet. Each bullet has one tag:

| Tag | Meaning |
|---|---|
| `[code]` | read from the source, with file:line |
| `[author]` | the author said it in this session; not in the code |
| `[doc]` | from a document or media file by the author or the team (old post, resume, slides, video); give the file or URL and the page, section or timestamp |
| `[ref]` | from the pinned reference: a repo (tag and file:line) or a paper (arXiv id and version, and section, figure, table or equation) |
| `[sim]` | measured or reproduced by a script in this session (also measurements on data files); give the script name and the numbers |
| `[unknown]` | nobody knows; keep it open |

- Write the formulas exactly as the code computes them: data types, constants, rounding mode, truncation, bounds.
- Record the constants and the reason for each one. If the reason is not known, tag it `[unknown]`. Do not invent a reason.
- Record the gaps with numbers: how many outputs differ, by how much, under which input.
- When two sources disagree (code and document, video and resume, file dates and the stated year), record both with their tags. Ask the author which one wins. Record the answer as `[author]`.
- Mark content that must never reach a post "NOT FOR PUBLICATION" (for example third-party data statistics or defects that the author wants to keep out).
- When a dump, test or log looks wrong, check the code path before you call it a failure. (Two dumps can be identical because the code between them is disabled. A short results file can be a real result, not a failed run.)

## Sections (adapt)

0. Status of claims (the tag table)
1. What the system was (scope, history, direction of the design)
2. The central idea (one diagram's worth)
3. Core arithmetic or core algorithm
4. One section per subsystem or operator family
5. The front end, build or tooling
6. Verification flow (golden files, tests, eval suites)
7. Defects and lessons
8. Open questions
9. Findings from the blog scripts (filled in Phase 5)
