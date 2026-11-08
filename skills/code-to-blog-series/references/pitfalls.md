# Pitfalls

| Pitfall | Example | Rule |
|---|---|---|
| Reference from memory | Notes describe a library kernel in a way that its pinned code does not support. | Clone the reference at a tag. Cite file:line. |
| Overclaim | The text says "8x" when the count gives 16x; a constraint "explains" a constant without evidence; "library X requires Y". | Each ratio comes from the script. Each cause comes from the author or the code. |
| Invented anecdote | A debugging story appears that the author never told. | Write only what the code, the scripts or the author give. |
| Wrong reading of results | A short results file is called a failed run, but the runs were real. | Ask before you judge a result. Do not cite internal results without approval. |
| Harsh tone | "Leaks" and "mistakes" for old gaps. | "Gaps" and "refinements", unless the author wants another tone. |
| Ownership implied | "In our code it is commented out" implies that the author still has the code. | Describe the design. Do not refer to the original code when the author does not want it. |
| Credit | "I did the math" for team work that someone guided. | "We" for team work. Credit the people. |
| RNG order | A new script section moves the RNG state and changes published numbers. | One fixed seed per section. Re-check every number after a script change. |
| Collapsed spaces | The PNG renderer collapses aligned columns. | `figkit.code()` with `\t`, or separate text. |
| Overlaps | Connectors and labels overlap in the first builds. | Read every PNG after every build. |
| Image links 404 | Posts hotlink images from the main branch, and the branch is not merged yet. | Render local HTML for review. Merge only on request. |
| Global git identity | A repo script overwrites the global git user. | Set the author name and email in the repo config only. |
| Lost numbers | The final results of the old project are lost, or only the author's documents give them. | Publish a result only when the author approves it, as the author approved it (`[author]` or `[doc]`). Otherwise use a sentence that the author approves, supported by script numbers only. |
| Wrong reference | The author gives a paper that only cites the method (a follow-up or a fusion paper). | Read the method section first. Compare with the code and the media. Tell the author when they do not match. |
| Third-party code as the author's | The training code in the folder is by the paper authors. | Ask who wrote each part. Do not describe third-party code as the author's work. |
| Conflicting sources | The resume, the video and the file dates give different years or numbers. | Record all of them. The author decides. Do not publish a precision (month, digit) the author did not confirm. |
