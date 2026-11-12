# Questions for the owner

Ask these before you build. Give a proposed default for each. Ask in groups of at most 4.

## The project

1. What is the system? Who wrote which part? (Do not assume that the team wrote all of it.)
2. What were the external constraints? (Hardware limits, latency budgets, memory, APIs.)
3. Which results does the owner know? Which numbers are lost? Where sources disagree, which one is right?
4. Which code, data and documents are by third parties (paper authors, a library, a vendor)? May the write-up use them?
5. Which source is the primary one for the deployed system, and which reference describes the method? (Check the reference before you rely on it.)

## Mode and readers

6. Internal or public? (Default: internal.)
7. Who are the readers, and what do they know already? (Default: engineers on the team who did not work on this code.)
8. Internal mode: which repository URL and which commit do the citations link to? (Default: the current `HEAD` of the default branch, with its hash.)
9. Public mode: which names must not appear? (Product, hardware, internal project, customer and organisation names, internal paths.) May the organisation be named? Are there confidentiality rules?
10. May the write-up give result numbers (accuracy, speed)? (Default: only numbers that a script in the write-up makes, plus numbers from a named reference.)
11. Licences of third-party data and code. May the write-up show images or statistics from them? (Default: no statistics from third-party data in public mode.)
12. Do images or video frames show people, plates or private places? (Default: do not use such frames in public mode.)
13. Tone about gaps? (Default: neutral. "Gap" and "refinement", with the measured effect.)

## Form

14. Target folder and repo? Does the repo have a style guide? (Default: `writeup/` in the project, in ASD-STE100; the repo style guide wins over `writing.md`.)
15. One document or a series of parts? (Default: parts when the text is more than about 3000 words.)
16. Does the Markdown renderer show math (`$$ ... $$`)? (Default: no math markup; write formulas in code blocks.)
17. Credits: which people guided the work or own the parts? (Default: ask.)
18. Git: commit or not, which branch, push or not? (Default: no commit until the owner asks.)
19. Attended or unattended run?
