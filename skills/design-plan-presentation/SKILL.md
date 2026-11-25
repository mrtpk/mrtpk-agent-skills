---
name: design-plan-presentation
description: Build an interactive, non-scrolling, click-to-reveal HTML presentation from a design document or plan, served locally to a team. Use this skill when the user wants to present a design, plan, architecture or proposal live to people in a meeting — as a "presentation", "walkthrough for the meeting", "interactive presentation" or "demo page" that a presenter clicks through. Also use it to change or extend such a presentation that already exists in the repository. Do not use it for a static page that people read alone, such as a Markdown report published as a page (report-to-page), to build a site that teaches a codebase (codebase-explainer), for a written write-up (code-to-md-writeup), or for a .pptx deck.
---

# Design-plan presentation

Build one self-contained HTML page that shows a design document to a room. The
audience examines it with clicks. Nothing scrolls. The presenter serves it from
a local machine (`python3 -m http.server <port>`). Thus the page must work with
no build step. The only permitted network access is for optional fonts.

## Process

1. **Fix the requirements first.** Read the design document. Then ask the user
   about all six items in one message. Give a proposed default for each item:
   1. the hub nodes (one for each takeaway),
   2. the content on screen and the content behind a click,
   3. the prior knowledge of the audience (is a primer necessary?),
   4. the theme (light, dark, or both with a toggle),
   5. the serving port,
   6. the content to leave out.

   Do not build before the user answers. Do not write a file before the answers.
2. **Build** one file, for example `assets/presentation/<name>.html`. Start from
   `templates/presentation.html` in this skill folder. It has the hub, the nav pills, an act with
   stages, the variant toggle, the modals, the deep links and the theme toggle. Replace each
   UPPERCASE placeholder. Keep the structure.
3. **Verify with screenshots** (section "Verify"). Do not say that a layout is
   done before you look at it.
4. **Iterate on feedback.** When the user corrects one pane, make the
   correction a rule for the full page. Apply it at each location that has
   the same pattern. Record each rule. Do not break it later.

## Page architecture

- **The hub is the system itself.** The first screen shows the architecture
  (the services, the connections, the components). Each region is a click target
  that opens an "act". The map and the system are the same picture. Extra
  topics (workload, validation, primer) become header pills.
- **Numbered nav pills, one style.** Each act opener is the same pill: one
  accent color, a filled number badge, a label. Select an accent that no
  content role uses.
- **Acts** are full-screen fixed overlays (`position:fixed; inset:0`). Each
  act has a header (badge, title, one-line subtitle, "Esc · back") and an
  `overflow:auto` body. Esc closes the top modal first, then the act.
- **The core act animates the worked example of the document** one stage at a
  time. It has prev/next buttons, arrow keys, progress dots, and a caption
  bar. The caption bar explains the current stage in one or two sentences.
  Payload frames move across the screen with CSS `left`/`opacity`
  transitions. Do not use an animation library. Class toggles and transitions
  are sufficient for all animations.
- **A variant toggle** (for example design option A/B) plays the same example
  again with different payloads. The toggle goes back to stage 0. It changes
  each dependent label: shapes, byte counts, captions, panel footers, grids.
  Keep the strings for each variant in small JS lookup tables with the variant
  as key. Do not put them inline in conditionals.
- **Hidden depth.** Put the fine print (message formats, retries, timeouts,
  failure rules, rejected alternatives) in a modal behind one button. The
  presenter opens it only for questions.
- **A primer** (background that the audience possibly does not have) is behind
  a "?" pill. It has twenty seconds of content on one screen.
- **Deep links** for rehearsal: `#act-id/stage/variant` opens an act at a
  stage. `?theme=dark` overrides the theme. Implement both. You also need them
  for your own screenshot verification.

## Style

Use the diagram style guide of the project if it exists. If not, use the rules
of the `svg-figures` skill (`svg-figures/references/style.md`) when it is
installed. Its rules also apply to HTML. Use a flat style with no gradients
or shadows. One accent has one meaning. Use neutral ink and gray for all items
that the reader need not follow. Use sans for prose. Use mono for each number,
shape, and identifier. Use numbered badges to show the reading order. The
default theme is light, with a dark toggle. Define all colors as CSS
variables on `:root`. Define them again under `[data-theme="dark"]`. Save the
choice in `localStorage` inside try/catch.

Fonts from Google Fonts (Inter + JetBrains Mono) are the only permitted network
dependency. These are page fonts, chosen for a projector. They differ from the figure fonts of
`svg-figures` on purpose; figures that you embed keep the `svg-figures` style. Use system font stacks as fallback. Do not use JS frameworks.

## Projector scaling

Text that you can read on a laptop is too small on a projector. Scale the full
page:

```css
body { zoom:1.18; }
#app { height:calc(100vh / 1.18); }  /* vh ignores zoom — correct it */
```

`vh` units do not become smaller with `zoom`. Thus divide each `100vh` box by
the same factor. If you do not, the page cuts off at the bottom. Act overlays
with `inset:0` need no correction. In panes, body text below approximately 13px
(before zoom) is too small. Data lines must be 11–12px mono minimum.

## Content rules (do not regress them)

- **Pills for each list of items, workers, or IDs.** A line such as
  `worker0 ← job1, job2 · ids = [1, 2]` is difficult to read. Show one row for
  each item: a colored name, an arrow, colored chips. Give each chip the color
  of its owner (categorical series). Use the same color at each location where
  it shows: lists, tables, formulas, grids.
- **One value on each line in payload frames.** A frame shows the type tag
  first. Then it shows each field or shape on its own line. Then it shows the
  size (muted). Do not join them with middle dots into one string.
- **Show the data, not the header noise.** Show the payload
  (`batch [32, 512] float32`), not bookkeeping (`step 7 · n 2`). Counters and
  echo fields belong in the fine print.
- **Use the real names of fields** (`user_ids`, not `ids`). Explain a shape one
  time in the caption ("`[2, 3]` = 2 requests × 3 IDs"). People often read
  shapes as counts.
- **No cross-reference citations.** Do not show "(decision 7)", "(fact 1)",
  "(rule 4.1)" on screen. Keep the claim and remove the tag.
- **No us/them wording.** Name the components (the client, the server). Do not
  call a team "us", "ours", or "them". People in the audience can own a part
  of the system.
- **Keep boxes short.** Each box has two to four lines. If a pane needs a
  paragraph, put the paragraph behind a click.
- Write page prose in ASD-STE100 (section "Communication style").

## Communication style

Apply these rules to all text that this skill produces (page prose, captions and replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Layout gotchas (each cost a debug round)

- A `position:relative` flight zone in a flex column collapses to zero height.
  Its absolutely positioned children then stack at the top. Give it
  `flex:1; min-height:0`.
- Do not show panels with a `max-height` transition. The content cuts off at
  the border at unpredictable points. Use `display:none` → `display:block`
  with a fade/slide keyframe animation.
- When a late stage adds a panel to a fixed column, hide an earlier panel that
  is no longer necessary. If you do not, the column overflows.
- Use `transition-delay` to start frame flights at different times. To reverse
  a flight, swap a `left` value. Do not animate `right`.

## Verify

Serve and screenshot the page before you tell the user that anything is done.
This needs Playwright with Chromium. If it is not installed, ask the user
before you install it (`uvx playwright install chromium`).

```bash
python3 -m http.server <port> --directory <dir> &
SERVER=$!
uvx playwright screenshot --viewport-size="1600, 900" --wait-for-timeout=5000 \
  "http://127.0.0.1:<port>/<page>.html#<deep-link>" <out>.png
kill $SERVER   # stop the server when the screenshots are done
```

Run a long-lived presentation server in tmux. Do not run it as a background
job of the shell.

Check these screens: the hub, each act, each stage of the worked example in
each variant, each modal, and the dark theme. Read each screenshot. Look for
text that is cut off, columns that overflow, and animations that are not
complete. Counter animations can look incomplete in headless screenshots.
Transitions with a fixed duration complete. Commit only when the user asks.
Commit only after the screenshots pass.
