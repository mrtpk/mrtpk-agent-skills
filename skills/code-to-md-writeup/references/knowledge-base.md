# Knowledge base

The KB is the archive. The write-up is a view of it. In public mode, the KB keeps what the write-up must leave out.

## Rules

- Mark the KB "INTERNAL" in the first line.
- Public mode: keep the KB out of the published folder. Internal mode: the KB can stay in `notes/` beside the write-up.
- Give the snapshot: the repository, the commit hash, the folders and files, and the date you read them.
- Give the path root once ("all paths are relative to ...").
- One claim per bullet. Each bullet has one tag:

| Tag | Meaning |
|---|---|
| `[code]` | read from the source, with file:line |
| `[owner]` | the owner or a named team member said it in this session; not in the code |
| `[doc]` | from a document or media file (design doc, slides, video); give the file or URL and the page, section or timestamp |
| `[ref]` | from the pinned reference: a repo (tag and file:line) or a paper (arXiv id and version, and section, figure, table or equation) |
| `[sim]` | measured or reproduced by a script in this session; give the script name and the numbers |
| `[unknown]` | nobody knows; keep it open |

- Write the formulas exactly as the code computes them: data types, constants, rounding mode, bounds.
- Record the constants and the reason for each one. If the reason is not known, tag it `[unknown]`. Do not invent a reason.
- Record the gaps with numbers: how many outputs differ, by how much, under which input.
- When two sources disagree, record both with their tags. Ask the owner which one wins. Record the answer as `[owner]`.
- When a dump, test or log looks wrong, check the code path before you call it a failure. (Two dumps can be identical because the code between them is disabled. A short results file can be a real result, not a failed run.)

## Sections (adapt)

0. Status of claims (the tag table)
1. What the system is (scope, history)
2. The central idea (one figure's worth)
3. Core algorithm
4. One section per subsystem
5. Build and tooling
6. Verification (tests, golden files, eval suites)
7. Gaps and lessons
8. Open questions
9. Findings from the check scripts (filled in Phase 5)
