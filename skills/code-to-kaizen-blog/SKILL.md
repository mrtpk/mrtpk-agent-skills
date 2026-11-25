---
name: code-to-kaizen-blog
description: Read a codebase (old or current), build an internal knowledge base with file:line citations, compare the design with a pinned reference implementation, and write a publishable technical blog series for the kaizen blog in the author's voice (first person, small check scripts, svglib figures as PNG, Jekyll posts). Every number in the posts comes from a script that the agent runs. Use this skill only when the user wants blog posts for the kaizen blog (or another Jekyll blog in the author's voice) from a codebase: "a blog series about this code", "blog posts from this project". Do not use it for a Markdown technical write-up, design notes or a technical report (use code-to-md-writeup), API docs, a README, or an explainer website (use codebase-explainer).
---

# Code to blog series

This skill turns a codebase, and the documents around it (papers, old posts, videos, a resume), into two outputs:

1. An **internal knowledge base (KB)**. It has every fact, with file:line citations and a status tag. It is never published.
2. A **public blog series**. It has no citations, no internal names and no implication that the author still has the code (when the author asks for that). Every number comes from a script beside the post.

You are the supervisor. You read the code, talk with the author, run scripts and review. Use subagents for long reads and for the fact check.

## Files in this skill

| Path | Read it when |
|---|---|
| `references/process.md` | before you start; it has the phases and the gates |
| `references/questions.md` | before the first discussion with the author |
| `references/sources.md` | when the sources are not only code (paper, video, data, documents), or when they disagree |
| `references/knowledge-base.md` | when you write the KB |
| `references/writing.md` | before you write or edit a post |
| `references/voice.md` | before you write or edit a post: the blog voice (synced from `brand-kit`; a blog repo `STYLE.md` wins) |
| `references/publishing-safety.md` | before you write a post, and before each commit |
| `references/figures.md` | before you draw a figure; figures need the `svg-figures` skill |
| `references/review.md` | when you start the fact-check subagent |
| `references/pitfalls.md` | once, before Phase 3 |
| `templates/` | copy into the notes folder or the post folder |
| `scripts/render_review.py` | to render the posts to local HTML for the author (brand-kit colours and fonts) |
| `code-to-md-writeup/scripts/md2html.py` | to render the notes (KB, outline) to HTML. It is in the `code-to-md-writeup` skill: look first in the folder that contains this skill (`../code-to-md-writeup/`). When it is absent, tell the user to install it |

Brand tokens and the voice file come from `brand-kit/` in the skills repo (`brand-kit/README.md`). Do not edit the lines between `BEGIN brand-kit:` and `END brand-kit:` markers, or `references/voice.md`. Change `brand-kit/`, then run `python3 brand-kit/tools/sync_brand.py`.

## Where the files go

- `notes/` is a folder in the root of the project that you study (not in the blog repo). The KB, the survey, the questions, the outline and the review HTML go there. The author may name another folder.
- The posts, their scripts and figures go in the blog repo.

## Workflow (short form; the numbers are the phases in `references/process.md`)

0. **Survey.** Read the code and the other sources. Do not change them. Write `notes/survey.md`: what the system is, who wrote which part, what is missing. Ask the author to confirm. Do not write a guess about the purpose into the KB as fact.
1. **Discuss.** Ask the questions in `references/questions.md`. Write `notes/questions.md`. Do not build before the author agrees on the scope and the rules.
2. **KB.** Write `notes/<project>_kb.md` from `templates/kb.md`. Tag each claim: `[code]`, `[author]`, `[doc]`, `[ref]`, `[sim]`, `[unknown]`.
3. **Compare.** Check the design against a pinned reference: a repo at a tag, or a paper at an arXiv version. First check that the reference describes this method. Cite it in the KB. Never cite a reference from memory.
4. **Outline.** Write `notes/blog_outline.md`. Split a long topic into a series: one idea per part, 1500-2500 words per part.
5. **Scripts, posts, figures.** For each part: write and run the check script, then write the post in the author's voice (`references/writing.md`) with numbers from the script output only, then one svglib script per figure. Look at every PNG.
6. **Review.** Start one fact-check subagent per batch (`references/review.md`). Verify each finding yourself before you apply it.
7. **Author review and commit.** Render HTML with `scripts/render_review.py`. Apply the comments. One commit per post, on the branch the author names. Merge and push only when the author asks.

Details and gates: `references/process.md`.

## Hard rules

- Measured numbers come from a script output. Do not type a measured number by hand. This is the default, not an absolute rule. Other numbers are allowed when their source is clear in the post and in the KB:
  - results that a cited paper or reference reports (say "the paper reports ..." and link it; tag `[ref]`);
  - results that the author approves from memory or from the author's own documents (tag `[author]` or `[doc]`; see `pitfalls.md`, "Lost numbers").
  Copy them exactly from the source. Do not mix them with script numbers in one claim without saying which is which.
- Every code block in a post runs. Extract and run each block before you commit.
- Every claim about a third-party library cites a pinned file:line in the KB. The post does not cite it.
- The KB is never published. Keep it out of the blog repo.
- Apply `references/publishing-safety.md` to every published file.
- Facts that only the author knows get the tag `[author]`. Do not invent an anecdote, a date, a motive or a result.
- Save the author's decisions as you get them: in the agent's persistent memory when it has one, and always in `notes/questions.md`. The answer date is for the internal notes only; it does not override a date rule for the posts.
- Use the workspace Python environment (uv by default): `uv run --with numpy python <script>.py`.
- Do not push, merge or publish without an explicit request.

## Communication style

These rules apply to the replies, the notes and the KB. The posts follow the blog voice in `references/writing.md`, not ASD-STE100.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
