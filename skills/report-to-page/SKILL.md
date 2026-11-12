---
name: report-to-page
description: Turn a long Markdown study or experiment report into one HTML page with a contents rail, a verdict box, key figures, and kept/not-kept labels in tables, then publish it as an Artifact. Use when the user asks to publish, share, or show an existing Markdown report as a static page that people read alone. Needs the Artifact tool to publish; without it, the skill writes a standalone HTML file. Do not use it to write the report itself (code-to-md-writeup), for a live click-through presentation in a meeting (design-plan-presentation), for a site that teaches a codebase (codebase-explainer), or for a dashboard of live data.
---

# Markdown report to a page

Script: `build_report_page.py` in this skill folder. Do not edit it for one report. Give the report data through `header.json`.

## Steps

1. Load the `artifact-design` skill if the Artifact tool is present.
2. Make sure the report has numbered H2 sections (`## 1. Verdict`, `## 2. ...`).
   The script makes the contents rail from them. Section 1 becomes the verdict box.
3. Write `header.json` in a temporary folder, not in the skill folder:

   ```json
   {
     "title": "Short page title",
     "eyebrow": "Subject · data · scope",
     "lede": "Two or three sentences: what the study did and what it found.",
     "figures": [{"value": "12.4 -> 15.1", "label": "what the number measures"}],
     "footer": "Sources: ..."
   }
   ```

   Use at most four figures. Take each number from the report. Do not invent a number.
4. If a table has a column of `yes`/`no` decisions, give its header name with `--kept-column`.
   Only the cells of that column become "kept" and "not kept" labels.
5. Run:

   ```
   uv run --with markdown python <skill>/build_report_page.py REPORT.md page.html --header header.json [--kept-column Kept]
   ```

   It prints the size and the section count. Check that the count equals the H2 count.
6. Publish `page.html` with the Artifact tool (icon `report`). Republish with the same path
   after each report change, so the URL stays the same.
7. When the Artifact tool is not present, add `--standalone` to the command in step 5. The script then
   writes a full HTML document. Give the user the path of the file.

## Communication style

Apply these rules to all text that this skill produces (the header text and the replies; do not rewrite the report itself). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Page properties

- Light and dark colors as tokens on `:root`. Dark mode by media query and by `data-theme`.
- Wide tables scroll inside their box. No horizontal page scroll at phone width.
- The contents rail is sticky on wide screens and a two-column list below 860 px.
- Fonts from Google Fonts only (Archivo, Source Sans 3, JetBrains Mono). These are report-page fonts; they differ
  from the figure fonts of `svg-figures` on purpose. No scripts.
