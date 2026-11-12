---
name: code-to-md-writeup
description: Write a Markdown technical write-up of a codebase (one document or a series of parts) from the code, its docs, papers and media. The agent builds an internal knowledge base with file:line citations and status tags, optionally compares the design with a pinned reference implementation or paper, runs small check scripts for every measured number, draws figures with the svg-figures skill, and has a subagent fact-check the result. Use this skill when the user asks for a technical write-up, technical report, design notes, a deep dive or "notes before we forget this project" from a repository, in Markdown. Do not use it for an HTML explainer or study site (codebase-explainer), an HTTP API reference, slides (design-plan-presentation), publishing a finished report as a page (report-to-page), or a README.
---

# Code to Markdown write-up

This skill turns a codebase, and the documents around it, into two outputs:

1. An **internal knowledge base (KB)**. It has every fact, with a file:line citation and a status tag.
2. A **Markdown write-up**: one document, or an index and one file per part. Every measured number comes from a check script beside the write-up.

The write-up has one of two modes. The owner (the person who asked for the write-up) selects the mode in Phase 1.

| | internal (default) | public |
|---|---|---|
| Readers | the team | anyone |
| Citations in the text | allowed, as links to the repo at a pinned commit | none |
| KB location | `notes/` beside the write-up or in the project | outside the published folder |
| Extra rules | none | `references/publishing-safety.md` |

You are the supervisor. You read the code, talk with the owner, run scripts and review. Use subagents for long reads and for the fact check.

## Files in this skill

| Path | Read it when |
|---|---|
| `references/process.md` | before you start; it has the phases and the gates |
| `references/questions.md` | before the first discussion with the owner |
| `references/sources.md` | when the sources are not only code, or when they disagree |
| `references/knowledge-base.md` | when you write the KB |
| `references/writing.md` | before you write or edit a part |
| `references/figures.md` | before you draw a figure |
| `references/publishing-safety.md` | public mode only: before you write, and before each commit |
| `references/review.md` | when you start the fact-check subagent |
| `references/pitfalls.md` | once, before Phase 3 |
| `templates/` | KB, outline, check script, part, index |
| `scripts/md2html.py` | to render Markdown to local HTML for the owner's review |

## Output layout

```
<writeup folder>/            name chosen by the owner, default writeup/
  README.md                  index: summary, parts, how to re-run the scripts and the figures
  01-<slug>.md ...           one file per part (or one file for a single document)
  scripts/01_<slug>.py       one check script per part
  diagrams/01_fig1_<name>.py one script per figure (svg-figures skill)
  resources/                 SVG and PNG of each figure
  tools/                     copy of the svg-figures toolkit, so that the team can rebuild the figures
notes/                       survey, questions, KB, outline (public mode: never in the published folder)
```

## Workflow (short form; details and gates in `references/process.md`)

0. **Survey.** Read the code and the other sources. Do not change them. Write `notes/survey.md`. Ask the owner to confirm what the system is.
1. **Questions.** Ask the questions in `references/questions.md`. Record the answers in `notes/questions.md`. Do not build before the owner agrees on the mode, the scope, the readers and the target folder.
2. **KB.** Write `notes/<project>_kb.md` from `templates/kb.md`. Tag each claim.
3. **Compare (optional).** Check the design against a pinned reference. First check that the reference describes this method.
4. **Outline.** Write `notes/outline.md`. One idea per part. Get the owner's approval.
5. **Scripts, parts, figures.** For each part: write and run the check script, write the part with numbers from the output only, draw the figures and read each PNG.
6. **Review.** Start a fact-check subagent (`references/review.md`). Verify each finding yourself before you apply it.
7. **Owner review and commit.** Render HTML with `scripts/md2html.py`. Apply the comments. Commit only when the owner asks.

## Communication style

Apply these rules to all text that this skill produces (the write-up, the KB, the notes and the replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Hard rules

- Measured numbers come from a script output. Do not type a measured number by hand. A number from a cited paper or reference is allowed when the text names the source. A number that the owner gives is allowed when the KB tags it `[owner]` and the owner approves the sentence.
- Every code block in the write-up runs. Extract and run each block before the review.
- Each check script uses one fixed RNG seed per section. Re-check every number after a script change.
- Every claim in the KB has a tag. Every `[code]` and `[ref]` claim has a pinned location.
- Every claim about a third-party library cites a pinned file:line in the KB.
- Do not invent a motive, an anecdote, a date or a result.
- Save the owner's decisions in `notes/questions.md` as you get them, and in persistent memory when the agent has one.
- Internal mode: record the repository URL and the commit hash before Phase 2. All citation links use that commit.
- Public mode: apply `references/publishing-safety.md` to every published file. The KB stays out of the published folder.
- Use the workspace Python environment (uv by default): `uv run --with numpy python <script>.py`.
- Do not commit, push, merge or publish without an explicit request.
