# brand-kit

The one source of the brand that the skills use: colours, fonts, the tp logo and the writing voice.
The values are the ones in published work: the blog figures (`svg-figures`) and the explainer sites
(`codebase-explainer`).

## Files

| Path | What it holds |
|---|---|
| `tokens.json` | fonts, the page palette (light and dark), the figure palette, the status colours, the favicon |
| `voice/tech-docs.md` | language and tone for technical documents (ASD-STE100) |
| `voice/blog.md` | the blog voice, copied from the kaizen blog `STYLE.md` |
| `logo/tp-192.png` | the tp logo from thomaspaul.dev; `logo/tp-32.png` is the favicon made from it |
| `allowlist.json` | colour literals in the skills that are not brand colours, each with a reason |
| `tools/sync_brand.py` | writes the tokens and voice files into the skills, and checks them |

Two palettes, on purpose:

- **Page** (`page`): reading pages. The link blue is `#1a5fb4`.
- **Figure** (`figure`): SVG figures and data series. The role blue is `#2563eb`.

The logo is only the favicon of pages that have no project mark (report pages, presentations).
It never goes into figures or explainer sites.

## How skills get the brand

Each skill folder holds a synced copy, so that the folder stays installable alone.

- **Regions.** A file has lines between `BEGIN brand-kit:<name>` and `END brand-kit:<name>` markers.
  `sync_brand.py` rewrites only those lines. The `REGIONS` table in `sync_brand.py` lists each file,
  region and renderer. That table is the consumer list.
- **Copies.** `references/voice.md` in a skill is a copy of one voice file. The `COPIES` table lists them.
- **Literal scan.** Every other colour literal (`#rgb`, `#rrggbb`) in the consumer skills must be a current
  token value or be in `allowlist.json`. After a token change, each old copy in a document fails the check.

## Change the brand

1. Edit `tokens.json`, a voice file or the logo. For a new favicon, write `logo/tp-32.png` too.
2. Run `python3 brand-kit/tools/sync_brand.py`. It updates every region and copy.
3. Fix each literal that the run reports: change the document, or add the colour to `allowlist.json`
   with a reason.
4. Run `python3 brand-kit/tools/sync_brand.py --check`. It must report 0 problems.
5. Rebuild and look at the output: figures, an explainer page, a report page.

Old copies in other repos (for example `tools/diagrams/svglib.py` in a blog repo) do not change. The drift
check of `svg-figures` reports them.
