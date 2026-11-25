---
name: evaluate-skills
description: Decide with evidence whether agent skills are worth their context. Review each skill, run its bundled scripts, test when it starts (trigger eval), and compare runs with and without it (behaviour eval with claude plugin eval). Then give each skill a score and a keep, fix or drop verdict. Use this skill when the user asks to evaluate, test, score or rank skills, asks whether a skill is worth keeping, or asks to run or write skill evals. Do not use it to write or change a skill (use a skill-creator skill), to find reusable knowledge in a session (extract-skills), or to review application code.
---

# Evaluate skills

A skill costs context each time it loads. It earns that cost only when an agent with the skill does better than an
agent without it. Text quality alone proves nothing. Measure the difference.

## Files in this skill

| Path | Read it when |
|---|---|
| `references/plugin-eval.md` | before you write or run a behaviour eval; it has the case format and the traps |
| `scripts/trigger_eval.py` | to run trigger evals (level 3) |

## Four levels, cheapest first

| Level | Question | How |
|---|---|---|
| 1. Review | Is it well made? | Read the skill. Score the criteria below. No runs. |
| 2. Tools | Do its parts work? | Run each bundled script and template on real input and on failure input. |
| 3. Trigger | Does it start at the right time? | `python3 <this skill>/scripts/trigger_eval.py <skills dir> --runs 3` (finds skills one folder down too, for example `skills/work/*`) |
| 4. Behaviour | Does it make the result better? | `claude plugin eval <skill folder>`, with and without the skill. |

Levels 1 and 2 find broken and weak skills cheaply. Only level 4 shows value. A text-only skill can be tested only
at level 4.

## Criteria (level 1)

- **Unique value:** knowledge that a strong agent does not have: traps, a fixed order, house rules.
- **Trigger text:** when to use it and when not, with the names of sibling skills.
- **Context cost:** the lines that load, against the lines that are necessary.
- **Correctness:** commands and scripts run as written; no contradictions with its own reference files.
- **Maintenance:** copied text, and files that it needs from outside its folder.

## Trigger evals (level 3)

- Input: `<skill>/evals/trigger_evals.json`, a list of `{"query", "should_trigger"}`.
- Make most negative queries near misses that belong to a sibling skill. Easy negatives prove nothing.
- Make each query self-contained. Each run starts a new, empty session.
- Run `--dry-run` first. Tell the user the run count before a full run.
- A run counts as correct when the skill starts within the first 5 tool calls. Agents often search before they load a skill.

## Behaviour evals (level 4)

1. Write one case per skill first. Test one phase of a long workflow, not the whole workflow.
2. Write each grader as one claim that a plain agent can fail. Before you keep a grader, ask: "Does plain Claude
   pass this too?" If yes, it shows nothing.
3. Do a smoke run: one case, `--runs 1`, `--ablation none`. Check that the fixture and the graders work.
4. Run both arms, 3 or more runs each. Use `--judge-model sonnet` and `--max-cost-usd`.
5. Read the evidence of each failed grader. Judge errors and test defects are common. Fix the test, or fix the
   skill, then run only the affected case again.

## Score and verdict

Give each skill a score from 0 to 10 and a verdict:

- **keep**: measured gain at level 4, and levels 1 to 3 are clean.
- **fix**: measured gain, but defects at any level. Name the defects.
- **drop**: no measured gain after a fair test. A skill with no measured gain scores at most 6.

For a second opinion, give a separate scorer the skills and the evidence, not your earlier scores.

## Rules

- Ask the user before each batch of runs. State the run count and an approximate cost. Start with a small sample.
- Report what each level tested and what it did not. Do not call a skill "valuable" without a level-4 result.
- Report the cost and the number of runs.
- Do not change a skill to pass its own eval. Change it only when a transcript shows a real defect.

## Communication style

Apply these rules to all text that this skill produces (reports, scores and replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
