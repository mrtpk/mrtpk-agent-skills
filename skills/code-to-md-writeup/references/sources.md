# Sources that are not only code

A project often comes with a paper, a demo video, data files and old documents. Use them, but keep track of where each fact comes from.

## Kinds of sources and their tags

| Source | Tag | Pin it with |
|---|---|---|
| Code that you can read | `[code]` | path and line range (and the commit) |
| Code by a third party (paper authors, a library) | `[ref]` | repo and tag, file:line |
| Paper | `[ref]` | arXiv id and version; section, figure, table or equation |
| Video, slides, old documents | `[doc]` | file or URL; timestamp, page or section; date read |
| Data files | `[sim]` | the script that measures them, and its output |
| The owner or a team member, in this session | `[owner]` | the name of the person and the date of the answer |

## Rules

- **Ownership.** For each source, record who made it. Describe third-party code as the third party's method.
- **Check the reference.** Read the method section of a paper before you use it. A paper that only cites the method is not the reference.
- **Video.** Extract frames (`ffmpeg -i <video> -vf fps=1 notes/video_frames/%04d.png`). Read every frame with text. Record facts with timestamps.
- **Web pages.** Fetch them to record the title and the claims. When a page cannot be fetched, keep the link and mark the content `[unknown]`. Do not download videos from the web.
- **Code that cannot run.** Do not try to rebuild an old framework. Re-implement the cited lines in a short script when a number is needed.
- **Conflicts.** When two sources disagree, record both, and ask the owner. The owner's answer wins.
- **Restricted content.** Mark content that must not go into the write-up "NOT FOR WRITE-UP" in the KB (for example third-party data statistics, or private documents).
