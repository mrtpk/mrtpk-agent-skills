# Pitfalls and lessons

Read this once before Phase 1. These are common problems.

Part of the `codebase-explainer` skill. Placeholders: `{PROJECT}`, `{SHA}`, `{SHORT_SHA}`, `{REPO_URL}`, `{SITE_NAME}`.

## Pitfalls and lessons

**Process**
- The survey is a guide, not a source. It can name an empty `__init__.py` as a dispatcher. Writers must
  open every file they cite.
- Fact checking is not optional: a part of the claims is wrong after writing. The writer cannot find its
  own errors well; use a separate agent.
- Errors repeat across pages. A fact fixed in one batch can still be wrong in pages from earlier
  batches. Record it as a FINAL-PASS TODO with the page list, and sweep at the end.
- Plan the look **before** Phase 1 samples. A late restyle costs a full subagent run and a diagram pass.
  Show the user a reference site and get a yes.
- Diagram readability: a 1500 canvas in a ~950 px column gives 7-8 px text. Use 1100 from the start.
- Put every planned page in the nav files in Phase 1. Then links to future pages work and give only
  warnings, and parallel writers do not edit shared files.
- Keep page-local `<style>` blocks out of pages; put shared styles in `site.css`. (A TODO to move
  them later is easily forgotten.)
- Keep "Next step" in `progress.md` current. A stale line misleads a new session.

**Tooling**
- Parallel builds clash (one build deletes `site/` while another reads it) → atomic swap of a temp folder.
  On `/mnt/c` the old folder is sometimes not deleted (`.site-old-<pid>` stays); ignore it in git and
  delete it by hand.
- One broken page blocked every writer's preview → `--preview`.
- `mtime` is unreliable on Windows mounts → content-hash stamps for diagrams. Without them, a diagram
  did not rebuild after a script edit.
- Glossary duplicate ids across parallel batches → merge-time error. Assign term ownership per batch.
- A `.json` search index does not load from `file://` → write it as a `.js` file that sets a global.
- Bool and int parsing in the target code can surprise (for example, a value such as `=off` can turn a feature on, and an empty
  int can raise an error). Generated reference tables catch these; hand-written ones do not.
- Docs and examples can disagree with code defaults (a README can give a default that the code does not use).
  Always cite the code for defaults.
- Headless browsers may lack CJK fonts; Chinese shows as boxes only in screenshots.

**Look**
- Dark and busy pages read badly as learning material. Light always, dark only by toggle.
- Few boxes, borders and badges. Long-form article layout. Large body text.

**People and limits**
- Usage limits cut subagents off mid-file. Write resume notes; continue, do not restart.
- A safety classifier may stop a writer on a harmless technical topic. Do not retry. Ask the user, defer
  the page, keep it as "soon".
- Ask concrete questions with a proposed default. Users answer those faster.

**Cost and accuracy**
- Cost is the main risk. Usage limits can stop the build more than once.
  Agree on a budget and a subagent limit before the full build (process.md, "Budget").
- Subagents can start their own subagents. Forbid it in every brief from the start.
- A fact checker can be wrong too. A false "bug" note (for example an indentation misread) can reach many pages. The
  supervisor verifies bug claims; pages stay neutral.
- The docs can be older than the code in many places. Write from the code;
  use docs only as hints.
- Defaults set in a config class can change later in argument parsing. Writers then cite the class field. Put
  such traps in the shared briefs as "accuracy lessons" after the first fact check.
- Facts can change more than once (for example a count that is corrected more than once). The
  status tags in `notes/facts.md` and the FINAL-PASS TODO list keep the pages consistent.
- A cut-off can leave unchecked work that gets committed. Commit after the writer, and again after the
  fact check, so each commit says what was checked.
- A browser setup in `/tmp` is gone after a restart. Keep the setup commands in `progress.md`.
- A literal `{{cite}}` inside `<code>` on a page broke the build. Escape tag syntax that is text.
- A scheduled resume job and a new agent definition are tied to the session (SKILL.md, "Keep the project
  resumable").
- A sibling site can save pages: basics that it already teaches get a one-line recap and a link.

**Known limits of the starter kit**

- `STYLE.md` §4.3 asks for `level` and a quiz on module pages, but `build.py` does not require them there.
  Keep the rule; optionally add `code` to `SECTIONS_NEED_LEVEL`.
- The STE check counts only the 25-word limit; the 20-word limit for instructions is not checked.

---
