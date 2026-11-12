# Process

## Phase 0: Survey

1. Find the code root and everything around it: docs, tests, eval reports, data folders, archives, images, videos, old documents (.docx, .pdf).
2. Read the entry points, the core modules (the main algorithm, the model, the data pipeline) and the tests. Use a search subagent for a large repo. Spot-check 3-5 claims of the subagent in the code.
3. For each part of the code, find out who wrote it: the team, or a third party (paper authors, a library). Ask when you cannot tell.
4. Record what is missing or broken: missing files, code that cannot run here, data that is not in the folder, results that no file reproduces.
5. Look at the media. Extract video frames with ffmpeg (for example 1 frame per second) into `notes/` and read the frames with text. Record each fact with its timestamp.
6. List the conflicts between sources (dates, numbers, versions). Do not resolve them yourself; they go to the owner.
7. Write `notes/survey.md`: a 10-line summary (what the system does, the data flow, the main constraints), the source list, the ownership list, the missing items and the conflicts.
8. Tell the owner your guess of what the system is. Let the owner correct it. Record the correction as `[owner]`.

Gate: the owner confirms what the system is.

## Phase 1: Questions

Ask the questions in `questions.md`. Write them, with your proposed defaults, to `notes/questions.md`. Record each answer there (with the date) and in the outline "Ground rules" section.

Gate: the owner agrees on the mode (internal or public), the readers, the scope, the split into parts and the target folder. Internal mode: the repository URL and the commit hash are recorded.

## Phase 2: Knowledge base

1. Copy `templates/kb.md` to `notes/<project>_kb.md`.
2. Fill one section per subsystem. Each claim has a tag and a citation (`path/file.py:120-134`).
3. Add a "Gaps and lessons" section. Use neutral words.
4. Add an "Open questions" section. Ask the owner about each item. Mark the rest `[unknown]`.

Gate: no untagged claim. No `[code]` or `[ref]` claim without a pinned location.

## Phase 3: Compare with a reference (optional)

Do this phase when the owner names a reference, or when the design follows a known method.

1. Pin the reference. A repo: clone it at a fixed tag into a temporary folder (`git clone --depth 1 -b <tag> <url>`). A paper: download the arXiv PDF at a fixed version (`<id>v<n>`). A document or video: record the URL and the date you read it.
2. Check that the reference describes this method. Read the abstract and the method section. When it does not match, stop and tell the owner. A paper that only cites the method is not the reference.
3. For each design point, find the reference location (file:line, or section, figure, table, equation). Write it into the KB.
4. Write small simulations that run both versions on the same inputs. Record the results as `[sim]` with counts.
5. When a version cannot run, re-implement the cited lines in a short script, and say "re-implementation of <location>" in the `[sim]` claim.

Gate: every comparison in the outline has a `[ref]` or `[sim]` source.

## Phase 4: Outline

1. Copy `templates/outline.md` to `notes/outline.md`.
2. One idea per part. Each part lists: the question it answers, the script, the numbers it needs, the figures.
3. Put the basics in a first part when the readers need them.
4. A last part or section: gaps, lessons, what to keep, what to change.

Gate: the owner approves the outline.

## Phase 5: Scripts, parts, figures (one part at a time)

For each part:

1. Write `scripts/NN_<slug>.py` from `templates/check_part.py`. Fix one RNG seed per section. Run it. Save the output in `notes/`.
2. Write `NN-<slug>.md` from `templates/part.md`. Copy each number from the output.
3. Draw the figures with the svg-figures skill (`figures.md`). Read each PNG. Fix overlaps and clipping.
4. Extract every code block of the part into a temporary file and run it. The output must match the text.
5. Update `README.md` from `templates/readme.md`.

When the owner says "run unattended", do all parts, then report once.

## Phase 6: Review

1. Start a fact-check subagent with the prompt in `review.md`. Use the model and effort that the owner names.
2. Triage each finding. Check it in the code or in the script output. Reject findings that are wrong; tell the owner why.
3. Apply the confirmed fixes. Re-run the scripts and rebuild the figures.

## Phase 7: Owner review

1. Render: `uv run --with markdown python -I <skill>/scripts/md2html.py <writeup>/*.md`. The HTML files are written beside the Markdown files.
2. Give the owner the path of the HTML files.
3. Apply each comment. Re-render.
4. Delete the HTML files when the owner does not want them in the repo.
5. Commit only when the owner asks: one commit per part, on the branch that the owner names.
