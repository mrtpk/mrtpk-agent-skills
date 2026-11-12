# Fact-check review

Start one subagent for the review. Use the model and the effort that the owner names. Do not give it your conclusions. Give it the files.

## Prompt template

```
You fact-check a technical write-up before it is shared. Be strict. Report defects only.

Inputs:
- Write-up: <writeup folder>/*.md (parts <list>)
- Check scripts: <writeup>/scripts/*.py. Run each with `uv run --with numpy python <script>`.
- Figure scripts: <writeup>/diagrams/*.py and the PNGs in <writeup>/resources/.
- Internal knowledge base (the source of truth for the design): <path to KB>
- Source code at the pinned commit: <repo path or URL, commit hash>
- Pinned reference (if any): <repo and tag, or paper arXiv id and version, or document URL>
- Mode: <internal | public>. Public mode only: publishing rules in <path to publishing-safety.md> and banned names: <list>

Check:
1. Each number in the write-up matches the script output.
2. Each code block runs and prints what the text says.
3. Each claim about the design matches the KB. Internal mode: each citation link points to the pinned commit, and the cited lines support the claim.
4. Each claim about the reference matches the pinned reference. A number quoted from a paper names the paper and matches it exactly.
5. Overclaims: causes, motives or "requires" statements without evidence.
6. Public mode only: banned names, citations of the original code, results that the owner did not clear.
7. Figures: the values in each figure script match the text and the script. Titles, subtitles, labels and footnotes are claims too.

Report a table: part, quote, defect, evidence (file:line or script output), proposed fix.
Do not edit files.
```

## Triage

- Check each finding yourself. A subagent can be wrong as confidently as it is right.
- Reject a finding when the evidence does not support it. Record why.
- Apply the confirmed fixes. Tell the owner what you rejected and why.
