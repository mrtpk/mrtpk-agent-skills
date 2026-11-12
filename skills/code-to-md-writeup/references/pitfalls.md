# Pitfalls

| Pitfall | Example | Rule |
|---|---|---|
| Reference from memory | The notes describe a library function in a way that its pinned code does not support. | Clone the reference at a tag. Cite file:line. |
| Overclaim | The text says "4x faster" when the measured ratio is 2.6x; a constraint "explains" a constant without evidence; "library X requires Y". | Each ratio comes from the script. Each cause comes from the owner or the code. |
| Invented anecdote | A debugging story appears that nobody told. | Write only what the code, the scripts or the owner give. |
| Wrong reading of results | A short results file is called a failed run, but the run was real. | Ask before you judge a result. |
| Harsh tone | "Broken" and "mistake" for old gaps. | "Gap" and "refinement", with the measured effect, unless the owner wants another tone. |
| Moving citations | Citation links point to `main`, and the lines move after the next merge. | Link to the pinned commit hash. |
| Third-party code as the team's | The training code in the folder is by the paper authors. | Ask who wrote each part. |
| RNG order | A new script section moves the RNG state and changes the numbers in the text. | One fixed seed per section. Re-check every number after a script change. |
| Collapsed spaces | The PNG renderer collapses aligned columns. | `figkit.code()` with `\t`, or separate text. |
| Overlaps | Connectors and labels overlap in the first builds. | Read every PNG after every build. |
| Lost numbers | The final results of an old project are lost. | Use a result only when the owner approves it (`[owner]` or `[doc]`). Otherwise write a sentence that the owner approves, supported by script numbers only. |
| Wrong reference | The owner gives a paper that only cites the method. | Read the method section first. Tell the owner when it does not match. |
| Conflicting sources | The design doc, the code and the file dates give different numbers. | Record all of them. The owner decides. |
| Global git identity | A repo script overwrites the global git user. | Do not change the git configuration. |
