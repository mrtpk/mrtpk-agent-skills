# Writing and accuracy rules

Read this before you write or fact-check text. Give it to every writer and fact checker.

Part of the `codebase-explainer` skill. Placeholders: `{PROJECT}`, `{SHA}`, `{SHORT_SHA}`, `{REPO_URL}`, `{SITE_NAME}`.

## Writing and accuracy rules

### Language style (configurable)

The site language is a project choice (goal-and-questions.md, question 6; `language_style` in
`explainer.json`). **Suggested default: ASD-STE100** (`ste`). With plain English, keep
rules 3, 6, 7, 8 and 10 in `references/voice.md` and drop the word limits.

The ASD-STE100 rules 1-10 and the word substitutions are in `references/voice.md` (synced from `brand-kit`).
Give it to every writer and fact checker with this file. `templates/STYLE.md` §6 is the project copy of the
same rules: keep its rule list and substitution table equal to `references/voice.md`.

**Fixed vocabulary.** Write a table in `STYLE.md` of the project's words: one word per thing, and the
words not to use for it. LLM engine example: request (what a user sends) / sequence (the engine object);
step (one engine iteration), not tick or round; rank (one process) / device (one GPU);
block (KV cache block), not page or chunk; kernel (device program), not op.

**Technical terms.** Define each term at its first use on the page and link it with `{{term id}}`.
Link only the first use (and again in a far deep dive).

### Accuracy rules

1. **Every claim about the code has a source**: `{{cite path:line}}` or an `<x-code>` excerpt.
   No source, no claim.
2. **Read the code yourself.** Surveys, notes and `facts.md` are a guide only.
   (For example, a survey can name an empty `__init__.py` as the dispatcher.)
3. Cite the **narrowest** line range that proves the claim.
4. Mark every simplification with `<x-simplified>` and say what the full truth is.
5. **Open questions are written as open questions.** When the code does not answer a question, say so on
   the page (and in the FAQ "Known open questions"). Do not guess. "It probably ..." is not allowed.
6. When code and docs disagree, describe the code and mention the difference. Collect these in the FAQ.
   When a code comment is wrong, say so (example: a comment can disagree with the code that follows it).
7. Derived claims (for example "the first batch runs in step N") must say "earliest possible" or show
   the derivation. Mark them for a hard fact check.
8. Inferred values that are not in the repo (for example a size that comes from a checkpoint file) are
   marked "inferred".
9. Vendor libraries and submodules that are not checked out: explain only how the project calls them
   (arguments, shapes, when). Do not describe their inside.
10. Comments in other languages: translate when it helps, and mark them as translated (`<x-tr>`).
11. General knowledge that is not about this repo needs no citation, but it must be correct and short.
    If you are not sure, leave it out.
12. Line numbers are for the pinned commit. The build fails when the checkout is at another commit.
13. **Defaults: trace the value to where it is finally set.** A config class field is often only the first
    value. Argument parsing, post-init hooks, usage context, hardware size or platform code can change it.
    (Example: a feature flag can get its real default in the argument-parsing module, not in the config class.)
14. **"Always", "every", "all", "never"** only when you checked every path. Otherwise write "only when ...".
15. **No bug claims on pages.** Say what the code does, in neutral words. Report a suspected bug to the
    supervisor with exact lines. (example: a checker misread an indentation level and called correct code a bug.)
16. **Counts and call order** ("runs 5 times", "called before X") need a check of every call site.
    (example: a hook count can need corrections in more than one fact check.)
17. A recap of a sibling site (one line + link) must be true to that page. The fact checker opens it.

### Quizzes, notes and warnings

- 3-5 questions per page; mix easy, medium and hard; at least one hard question needs the deep dive.
  Answers say *why* and cite the code.
- `<x-note>` for a useful extra fact; `<x-simplified>` for every simplification; `<x-warning>` for a real
  trap, placed before the text it is about.

---
