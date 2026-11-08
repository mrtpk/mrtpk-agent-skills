# Process

## Phase 0: Survey

1. Find the code root and the folders around it (docs, apps, test suites, eval reports, old docs such as .docx).
2. Read the entry points, the operator registry, the core kernels and the tests. Use an Explore subagent for a large repo. Spot-check 3-5 claims of the subagent in the code.
3. Write a 10-line summary: what the system does, the data flow, the main constraints.
4. Tell the author your guess of what the system is. Let the author correct it. Record the correction as `[author]`.

Gate: the author confirms what the system is.

## Phase 1: Discuss

Ask the questions in `questions.md`. Record each answer in memory and in the outline "Ground rules" section.

Gate: the author agrees on the audience, the publishing rules, the series split and the target repo.

## Phase 2: Knowledge base

1. Copy `templates/kb.md` to `notes/<project>_kb.md`.
2. Fill one section per subsystem. Each claim has a tag and a citation (`path/file.py:120-134`).
3. Add a "Defects and lessons" section. Use neutral words: "gap", "refinement".
4. Add an "Open questions" section. Ask the author about each item. Mark the rest `[unknown]`.

Gate: no untagged claim. No `[ref]` claim without a pinned file:line.

## Phase 3: Compare with the reference

1. Clone the reference at a fixed tag into the scratchpad (for example `git clone --depth 1 -b <tag> <url>`).
2. For each design point, find the reference code. Write the citation into the KB.
3. Write small simulations that run both versions on the same inputs. Record the results as `[sim]` with counts ("2.8 % of outputs differ, max difference 1").

Gate: every comparison in the outline has a `[ref]` or `[sim]` source.

## Phase 4: Outline and series split

1. Copy `templates/outline.md` to `notes/blog_outline.md`.
2. Put the basics in a prequel when the reader needs them (for example a rewrite of an earlier answer or note by the author).
3. One idea per part. Each part lists: the question it answers, the script, the numbers it needs, the figures.
4. A last part: lessons, what held up, what you would do again.

Gate: the author approves the outline.

## Phase 5: Scripts, posts, figures (one part at a time)

For each part:

1. Write `<slug>.py` from `templates/check_script.py`. Fix the RNG seed. Run it. Save the output.
2. Write the post from `templates/post.markdown`. Copy each number from the output.
3. Write the figure scripts from `templates/figure.py`. Build them. Read each PNG with the Read tool. Fix overlaps and clipping.
4. Extract every code block of the post into a temporary file and run it. The output must match the post.
5. Write `linkedin-post.md` from `templates/linkedin-post.md` (optional).
6. Commit the part on the branch.

When the author says "run unattended", do all parts, then report once.

## Phase 6: Review

1. Start a fact-check subagent with the prompt in `review.md`. Give it the post folders, the KB and the scripts. Use the model and effort that the author names.
2. Triage each finding. Check it in the code or in the script output. Reject findings that are wrong; tell the author why.
3. Apply the confirmed fixes. Re-run the scripts and the figures.

## Phase 7: Author review

1. Render: `cd <blog repo> && uv run --with markdown python -I <skill>/scripts/render_review.py learnings <notes>/blog_review --posts <folder> <folder> ... --raw <image URL prefix> --tree <folder URL prefix>`
2. Tell the author the path of `blog_review/index.html`.
3. Apply each comment. Re-render. Commit per post.
4. When the author asks: merge to the main branch and push. Image links that point to the main branch return 404 until the merge.
