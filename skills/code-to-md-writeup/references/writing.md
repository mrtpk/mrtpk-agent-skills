# Writing the parts

When the target repo has a style guide, it wins. Otherwise use this file.

## Voice

- ASD-STE100 Simplified Technical English (SKILL.md, "Communication style"). Neutral technical voice.
- "We" for the team. Name a person only for credit, and only when the owner approves it.
- Define each term once, in one sentence, at its first use. Then give a small example with real numbers.
- One idea per section. Start the section with the question it answers or with its conclusion.
- No hype words: robust, seamless, powerful, leverage, game-changer, simply.
- No filler openers or closers. Each part ends with a short "Summary" section of 2-4 bullets.

## Structure of one part

1. Title (`# NN. <topic>`) and one paragraph: what this part answers, and a link to the previous part.
2. "Background": the minimum that the reader needs.
3. The idea, with the formula and one worked example.
4. "Check": a short check script excerpt and its output. The output lines say what is checked and the result, for example `rows dropped: 0 (expected 0) -> OK`. A deliberate counter-example can show a failure, with a comment that says so.
5. A figure per main idea, with alt text and a caption `*Figure: ...*`.
6. "Comparison" (when Phase 3 ran): what the reference does differently, and why this design differs. Internal mode: cite the reference location.
7. "Gaps": with measured numbers, in the agreed tone.
8. "Summary".
9. "Source": a link to the full check script (`scripts/NN_<slug>.py`).
10. "References": a list of link references.
11. A link to the next part.

## Citations (internal mode)

- Link to the pinned commit: `[file.py:120-134](<repo URL>/blob/<commit>/path/file.py#L120-L134)`. Use the URL format of the host (GitHub, GitLab).
- Cite once per claim, at the end of the sentence. Do not cite the same lines twice in one paragraph.
- Do not cite a moving branch.

## Markdown

- GitHub-flavoured Markdown. Fenced code blocks with a language tag.
- Math: use `$$ ... $$` only when the owner confirmed that the renderer shows it. Otherwise write formulas in a code block.
- Tables for comparisons of 3 or more items.
- Relative links between parts and to `resources/`.

## Numbers and claims

- Copy each measured number from the script output. If you change the script, re-run it and re-check every number in the text.
- A number from a paper or another reference names the source ("the paper reports ...", with a link). Copy it exactly. Keep it apart from the numbers that the script measures.
- Say what a number measures: "<share> of <count> outputs differ from <baseline>, by at most <max>".
- Do not write "X requires Y" about a library unless the pinned code shows it.
- Do not round a count into a ratio that changes it.
- Do not write a motive, an anecdote or a debugging story that the owner did not give you.
- When a number is lost, say so in a sentence that the owner approves.
