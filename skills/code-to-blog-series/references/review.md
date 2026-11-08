# Fact-check review

Start one subagent for the review. Use the model and the effort that the author names. Do not give it your conclusions. Give it the files.

## Prompt template

```
You fact-check a technical blog series before publication. Be strict. Report defects only.

Inputs:
- Posts: <blog repo>/learnings/<folder>/*.markdown (parts <list>)
- Scripts beside each post: <names>. Run each with `uv run --with numpy python <script>`.
- Internal knowledge base (the source of truth for the original design): <path to KB>
- Pinned reference: <repo path and tag, or paper arXiv id and version, or document URL>
- Publishing rules: <path to publishing-safety.md> and this list of banned names: <list>

Check:
1. Each number in a post matches the script output.
2. Each code block runs and prints what the post says.
3. Each claim about the original design matches the KB. Each claim about the reference matches the pinned reference (code at file:line, or paper at section, figure, table or equation). A number quoted from a paper names the paper and matches it exactly.
4. Overclaims: causes, motives or "requires" statements without evidence.
5. Publishing rules: banned names, implied ownership of the original code, unapproved accuracy numbers.
6. Figures: the values in each diagram script match the post and the script. Check the text too: titles, subtitles, labels and footnotes. Each ratio, count or claim in a figure title comes from the script output or the KB, like a claim in the post.

Report a table: part, quote, defect, evidence (file:line or script output), proposed fix.
Do not edit files.
```

## Triage

- Check each finding yourself. A subagent can be wrong as confidently as it is right.
- Reject a finding when the evidence does not support it. Record why (for example: "the check must print True" is wrong when the style guide allows a deliberate `False` counter-example).
- Apply the confirmed fixes. Tell the author what you rejected and why.
