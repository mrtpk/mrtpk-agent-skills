---
name: code-to-blog-series
description: Read a codebase (old or current), build an internal knowledge base with file:line citations, compare the design with a pinned reference implementation, and write a publishable technical blog series in the author's voice (first person, small check scripts, svglib figures as PNG, Jekyll posts). Every number in the posts comes from a script that the agent runs. Use this skill when the user wants to preserve, document or write up a project, wants "a blog about this code", "a technical write-up of this repo", "notes before I forget this project", or a technical blog series from a codebase. Do not use it for API docs, a README, or an explainer website (use codebase-explainer for that).
---

# Code to blog series

This skill turns a codebase into two outputs:

1. An **internal knowledge base (KB)**. It has every fact, with file:line citations and a status tag. It is never published.
2. A **public blog series**. It has no citations, no internal names and no implication that the author still has the code (when the author asks for that). Every number comes from a script beside the post.

You are the supervisor. You read the code, talk with the author, run scripts and review. Use subagents for long reads and for the fact check.

## Files in this skill

| Path | Read it when |
|---|---|
| `references/process.md` | before you start; it has the phases and the gates |
| `references/questions.md` | before the first discussion with the author |
| `references/knowledge-base.md` | when you write the KB |
| `references/writing.md` | before you write or edit a post |
| `references/publishing-safety.md` | before you write a post, and before each commit |
| `references/figures.md` | before you draw a figure |
| `references/review.md` | when you start the fact-check subagent |
| `references/pitfalls.md` | once, before Phase 3 |
| `templates/` | copy into the notes folder or the post folder |
| `tools/` | `svglib.py`, `figkit.py`, `build_figures.py`: the figure toolkit |
| `scripts/render_review.py` | to render the posts to local HTML for the author |
| `scripts/md2html.py` | to render the notes (KB, outline) to HTML |

## Workflow (short form)

1. **Survey.** Read the code. Do not change it. Write down what the system is. Ask the author to confirm. Do not write a guess about the purpose into the KB as fact.
2. **Discuss.** Ask the questions in `references/questions.md`. Do not build before the author agrees on the scope and the rules.
3. **KB.** Write `notes/<project>_kb.md` from `templates/kb.md`. Tag each claim: `[code]`, `[author]`, `[ref]`, `[sim]`, `[unknown]`.
4. **Compare.** Check the design against a reference implementation, cloned at a fixed tag. Cite its file:line in the KB. Never cite a reference from memory.
5. **Outline.** Write `notes/blog_outline.md`. Split a long topic into a series: one idea per part, 1500-2500 words per part.
6. **Scripts first.** For each part, write the check script. Run it. Put every number of the part in the script output.
7. **Write.** Write the post in the author's voice (`references/writing.md`). Copy numbers from the script output only.
8. **Figures.** One svglib script per figure. Build the PNG. Look at every PNG.
9. **Review.** Start one fact-check subagent per batch (`references/review.md`). Verify each finding yourself before you apply it.
10. **Render.** Render HTML for the author with `scripts/render_review.py`. Wait for the author's review.
11. **Commit.** One commit per post, on a branch. Merge and push only when the author asks.

Details and gates: `references/process.md`.

## Hard rules

- Every number in a post comes from a script output. Do not type a number by hand.
- Every code block in a post runs. Extract and run each block before you commit.
- Every claim about a third-party library cites a pinned file:line in the KB. The post does not cite it.
- The KB is never published. Keep it out of the blog repo.
- Apply `references/publishing-safety.md` to every published file.
- Facts that only the author knows get the tag `[author]`. Do not invent an anecdote, a date, a motive or a result.
- Save the author's decisions to memory as you get them.
- Use the workspace Python environment (uv by default): `uv run --with numpy python <script>.py`.
- Do not push, merge or publish without an explicit request.
