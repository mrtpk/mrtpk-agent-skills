# Publishing safety (public mode only)

Apply this check to every published file: Markdown parts, the index, check scripts, figure scripts, SVG and PNG text, commit messages.

## Before each commit

1. Grep the changed files for every banned name (case-insensitive). The owner gives the list in Phase 1. Include:
   - product, customer and hardware names
   - the internal project name
   - organisation names in old URLs
   - internal constant names, file names and paths of the original code
2. Grep for citations of the original code: `grep -rniE '\bline [0-9]+|\blines? [0-9]+-[0-9]+|\.py:[0-9]+|/blob/[0-9a-f]{7,}' <files>`.
3. Grep for result claims: "%", "accuracy", "F1", "FPS", "latency", "throughput". Each one must come from a script in the write-up, a named reference, or a result that the owner approved.
4. Check that no file from `notes/` or the KB is in the published folder.
5. Check the figure scripts: the docstrings cite the check scripts, not the original source files.

## Content rules

- Describe the design with a neutral name that the owner approves.
- The check scripts are new code, written for the write-up. Do not present them as the original code.
- Do not describe internal results that the owner did not clear.
- Private data of the owner or the team does not go to external services.
