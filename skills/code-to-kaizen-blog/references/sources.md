# Sources that are not only code

A project often comes with a paper, a demo video, data files, old posts and a resume. Use them, but keep track of where each fact comes from.

## Kinds of sources and their tags

| Source | Tag | Pin it with |
|---|---|---|
| Code that you can read | `[code]` | path and line range |
| Code by a third party (paper authors, a library) | `[ref]` | repo and tag, or "not the author's" in the survey |
| Paper | `[ref]` | arXiv id and version; section, figure, table or equation |
| Video, slides, old posts, resume | `[doc]` | file or URL; timestamp, page or section; date read |
| Data files | `[sim]` | the script that measures them, and its output |
| The author, in this session | `[author]` | the date of the answer |

## Rules

- **Ownership.** For each source, record who made it. Third-party code is described as the paper's method, not as the author's work.
- **Check the reference.** Read the method section of a paper before you use it. A paper that only cites the method is not the reference. When it does not match the code or the media, tell the author.
- **Video.** Extract frames (for example `ffmpeg -i <video> -vf fps=1 notes/video_frames/%04d.png`). Read every frame with text. Record facts with timestamps. A demo video is often the best source for the deployed system; ask the author.
- **Web pages.** Fetch them to record the title and the claims. When a page cannot be fetched, keep the link and mark the content `[unknown]`. Do not download videos from the web.
- **Code that cannot run.** Do not try to rebuild an old framework. Re-implement the cited lines in a short script when a number is needed.
- **Conflicts.** When two sources disagree, record both, and ask the author. The author's answer wins. Do not publish a precision (a month, a decimal) that the author did not confirm.
- **Not for publication.** Statistics from third-party data, frames with people, and private documents stay in the KB, marked "NOT FOR PUBLICATION", unless the author approves them.
- **Links.** Keep every link that the author asks for in the reference list of each post.
