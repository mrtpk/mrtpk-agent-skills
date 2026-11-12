---
name: design-plan-presentation
description: Build an interactive, non-scrolling, click-to-reveal HTML presentation from a design document or plan, served locally to a team. Use this skill whenever the user wants to present a design, plan, architecture, proposal, or technical document to people — as a "presentation", "walkthrough for the meeting", "interactive presentation" or "demo page" — even if they do not name a format. Also use it to change or extend such a presentation that already exists in the repository. Do not use it to publish a Markdown report as a page (report-to-page), to build a site that teaches a codebase (codebase-explainer), for a written write-up (code-to-md-writeup), or for a .pptx deck.
---

# Design-plan presentation

Build one self-contained HTML page that presents a design document to a
room. The audience explores it by clicking; nothing scrolls. The presenter
serves it from a local machine (`python3 -m http.server <port>`), so the
page must work with no build step and no network beyond optional fonts.

## Process

1. **Fix the requirements first.** Read the design document. Then agree
   with the user on: the hub nodes (one per takeaway), what is on screen
   against what hides behind a click, the audience's prior knowledge (a
   primer?), the theme, the serving port, and what to leave out. Use
   AskUserQuestion. Do not build before this is fixed.
2. **Build** one file, e.g. `assets/presentation/<name>.html`.
3. **Verify with screenshots** (section "Verify"). Never declare a layout
   done without looking at it.
4. **Iterate on feedback.** When the user corrects one pane, treat the
   correction as a page-wide rule and apply it everywhere the same
   pattern appears. Record each rule; do not regress it later.

## Page architecture

- **The hub is the system itself.** The landing screen draws the
  architecture (the machines, the link, the components). Each region is a
  click target that opens an "act". The map and the system are the same
  picture. Extra topics (workload, validation, primer) become header
  pills.
- **Numbered nav pills, one style.** Every act opener is the same pill:
  one accent color, a filled number badge, a label. Pick an accent no
  content role uses.
- **Acts** are full-screen fixed overlays (`position:fixed; inset:0`)
  with a header (badge, title, one-line subtitle, "Esc · back") and an
  `overflow:auto` body. Esc closes the top-most modal, then the act.
- **The core act animates the document's worked example** stage by stage:
  prev/next buttons, arrow keys, progress dots, and a caption bar that
  explains the current stage in one or two sentences. Payload frames fly
  across the screen with CSS `left`/`opacity` transitions. No animation
  library; class toggles and transitions cover everything.
- **A variant toggle** (e.g. design option A/B) replays the same example
  with different payloads. The toggle resets to stage 0 and swaps every
  dependent label: shapes, byte counts, captions, panel footers, grids.
  Keep the per-variant strings in small JS lookup tables keyed by
  variant, never inline in conditionals.
- **Hidden depth.** Fine print (wire headers, handshakes, timeouts,
  failure rules, rejected alternatives) goes in a modal behind one
  button. The presenter opens it only for questions.
- **A primer** (background the audience may lack) hides behind a "?"
  pill. Twenty seconds of content, one screen.
- **Deep links** for rehearsal: `#act-id/stage/variant` opens an act at a
  stage; `?theme=dark` overrides the theme. Implement both; they also
  make your own screenshot verification possible.

## Style

Default to the project's diagram style guide if one exists. Else use
the rules of the `svg-figures` skill (`svg-figures/references/style.md`),
when it is installed. Its rules carry over to HTML: flat, no gradients or shadows; one accent = one meaning; neutral
ink and gray for everything the reader need not track; sans for prose,
mono for every number, shape, and identifier; numbered badges for
reading order. Light theme default, dark toggle: define all colors as
CSS variables on `:root` and redefine them under `[data-theme="dark"]`;
persist the choice in `localStorage` inside try/catch.

Fonts via Google Fonts (Inter + JetBrains Mono) are the only acceptable
network dependency, with system stacks as fallback. No JS frameworks.

## Projector scaling

Laptop-readable is projector-illegible. Scale the whole page:

```css
body { zoom:1.18; }
#app { height:calc(100vh / 1.18); }  /* vh ignores zoom — correct it */
```

`vh` units do not shrink with `zoom`, so every `100vh` box must divide by
the same factor or the page clips at the bottom. Act overlays with
`inset:0` need no correction. Within panes, body text below ~13px
(pre-zoom) is too small; data lines live at 11–12px mono minimum.

## Content rules (do not regress them)

- **Pills for every list of items, workers, or IDs.** A line like
  `worker0 ← job1, job2 · ids = [1, 2]` is hard to read; render one row
  per item: a colored name, an arrow, colored chips. Bind each chip's
  color to its owner (categorical series), the same color everywhere it
  appears: lists, tables, formulas, grids.
- **One value per line in payload frames.** A frame shows: type tag,
  then each field or shape on its own line, then the size (muted). Never
  chain them with middle dots into one string.
- **Data carries the information; header noise does not.** Show the
  payload (`batch [32, 512] float32`), not bookkeeping (`step 7 · n 2`).
  Counters and echo fields belong in the fine print.
- **Name fields by their real names** (`user_ids`, not `ids`) and spell
  out a shape once in the caption ("`[2, 3]` = 2 requests × 3 IDs") —
  shapes get misread as counts.
- **No cross-reference citations.** Never "(decision 7)", "(fact 1)",
  "(rule 6.2.2)" on screen. Keep the claim, drop the tag.
- **No us/them wording.** Name components (the client, the server),
  never a team as "us", "ours", or "them". The audience can own the
  other half of the system.
- **Boxes stay terse.** Two to four lines each. If a pane needs a
  paragraph, the paragraph belongs behind a click.
- Write page prose in ASD-STE100 (section "Communication style").

## Communication style

Apply these rules to all text that this skill produces (page prose, captions and replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Layout gotchas (each cost a debug round)

- A `position:relative` flight zone inside a flex column collapses to
  zero height; absolutely positioned children stack at the top. Give it
  `flex:1; min-height:0`.
- Do not reveal panels with a `max-height` transition; content clips at
  the border unpredictably. Use `display:none` → `display:block` with a
  fade/slide keyframe animation.
- When a late stage adds a panel to a fixed column, hide an earlier
  panel that already served its purpose, or the column overflows.
- Stagger frame flights with `transition-delay`, and reverse flights by
  swapping a `left` value, not by animating `right`.

## Verify

Serve and screenshot before telling the user anything is done. This
needs Playwright with Chromium. If it is not installed, ask the user
before you install it (`uvx playwright install chromium`).

```bash
python3 -m http.server <port> --directory <dir> &
SERVER=$!
uvx playwright screenshot --viewport-size="1600, 900" --wait-for-timeout=5000 \
  "http://127.0.0.1:<port>/<page>.html#<deep-link>" <out>.png
kill $SERVER   # stop the server when the screenshots are done
```

Run a long-lived presentation server in tmux, not as a background job
of the shell.

Check: the hub, every act, every stage of the worked example in every
variant, every modal, and the dark theme — read each screenshot and look
for clipped text, overflowing columns, and mid-animation states. Counter
animations may appear unfinished in headless shots; transitions of
fixed-duration complete. Commit only when the user asks, and only after
the screenshots pass.
