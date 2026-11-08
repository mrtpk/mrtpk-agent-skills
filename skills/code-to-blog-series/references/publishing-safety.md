# Publishing safety

Apply this check to every published file: posts, scripts, figure scripts, SVG, PNG text, LinkedIn text, commit messages.

## Before each commit

1. Grep the blog repo changes for every banned name (case-insensitive). The author gives the list in Phase 1. Include:
   - product and hardware names
   - the internal project name
   - organisation names in old URLs (for example a GitHub org in an eval script)
   - internal constant names, file names and paths of the original code
2. Grep for code ownership phrases: "my code", "our code", "the code I have", "in the code", "commented out", "the original source", and line citations. Use word boundaries, so that "line" does not match "pipeline" or "online": `grep -rniE '\bline [0-9]+|\blines? [0-9]+-[0-9]+|\.py:[0-9]+' <files>`.
3. Grep for accuracy claims: "%", "top-1", "top1", "accuracy", "F1", "FPS". Each one must come from a script in the post, a named reference, or a result that the author approved.
4. Check that no file in `notes/` or the KB is in the blog repo.
5. Check the figure scripts: the docstrings cite the series scripts, not the original source files.

## Content rules

- Describe the design as "our reference model" or a neutral name that the author approves.
- The series scripts are new code, written for the post. Say "Let's look at the code." for them. Do not imply that they are the original code.
- Never publish file:line citations of the original code.
- Do not describe internal results that the author did not clear (old evaluation files, internal reports).
- The author's email and private data do not go to external services.
