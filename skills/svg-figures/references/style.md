# Figure style

The tokens are in `tools/svglib.py`. The `codebase-explainer` skill has a copy of the same drawing code (`templates/diagrams/svglib.py`; only the docstring is different). When you change one copy, change the other copy too.

## Canvas

- Width 1100. White background. The height follows the content: `d.save(height=end + 10)`.
- Keep 20-30 px margin on each side.

## Typography

- Sans: Inter, Segoe UI, Helvetica, Arial. Mono: ui-monospace, SFMono-Regular, Menlo, Consolas.
- Title 26 bold. Panel title 17 bold. Box title 13.5 bold. Body 12-12.5.
- No text smaller than 11.
- Mono 12-13 for numbers, identifiers, shapes and code.

## Layout

- At most 3 panels in one figure. At most 3 boxes side by side. Split a bigger figure into two figures.
- Each panel title is a question. Its subtitle is the answer in one sentence.
- Header subtitle: `<Document>  ·  <section>  ·  <scope>`.
- The parameter line (`params=`) gives the key parameters in mono, in one line.

## Colour

- One colour has one meaning in the figure. Use the same meaning in all figures of one document.
- 3-5 accents in one figure. Gray (`NEUTRAL`) for the rest: baselines, inactive items.
- Put every accent colour in the legend.
- `SERIES` is for categories only (for example 8 channels). Do not mix it with the role accents.

## Arrows

- Arrows do not cross boxes or labels. Route them with `path_arrow` when a straight arrow crosses something.
- Solid arrows for the main path. Dashed arrows for secondary paths.
- An arrow colour has the same meaning as the box colours.

## Content

- Real values from a named source: a check script and its section, or a file:line. Write the source in the script docstring.
- A footnote says what the figure simplifies.
- No internal names in a figure for a public document. Figure text is published like the document text.

## In the document

```
![Panel 1 shows ... Panel 2 shows ...](resources/<name>.png)

*Figure: <one sentence>.*
```

- The alt text describes each panel.
- Use the PNG in Markdown. Keep the SVG beside it for zoom and for later edits.
- 4-6 figures per long part is a good range. Draw as many as the ideas need, not more.
