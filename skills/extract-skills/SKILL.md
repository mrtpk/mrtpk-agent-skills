---
name: extract-skills
description: Mine the current conversation for reusable knowledge and turn what is worth keeping into skills, memories, docs or scripts. Use this when the user asks what skills could come out of this session, whether anything here is worth reusing or saving, to turn this work or workflow into a skill, or to capture what was learned before the context is lost. Also use it at the end of a long or painful session, when a problem took several wrong turns to solve, or when you notice you have re-derived the same sequence of steps more than once - the knowledge that cost the most to get is the knowledge most likely to be thrown away. Do not use it to build or edit one skill that the user already named (use a skill-creator skill), or to make skills when nobody asked to keep anything.
---

# Extracting reusable skills from a conversation

## Hard rule: propose before you build

Do not write a skill, memory, doc or script before the user selects it. This applies also when the user says
"turn this into skills". First show the recommendation. Then build only what the user selects.

Most candidates are not skills. Many weak skills are worse than no skills: each one costs context when it loads,
and it drifts from its source.

## Step 1: List the candidates

Read the transcript (or the history that the user gives), not your memory of it. List each candidate before you
judge it. Look for:

- a sequence that ran more than once,
- a fact that cost time to find, for example a wrong obvious command or an order constraint,
- the same problem that occurred two or more times (the second time is the evidence),
- a correction from the user,
- a dead end, and a wrong assumption that stayed for some time.

## Step 2: Route each candidate

| The knowledge is... | Put it in |
|---|---|
| a workflow with decisions and traps | a skill |
| a fact about the user, the setup or a preference | memory |
| how the system works, or why it has this design | a doc in the repo |
| a fixed sequence of commands with no decisions | a script or a make target |
| reference data: IDs, mappings, measured numbers | a doc or config |
| a task that a competent agent does well alone | nothing |

- When a script or doc already exists, refer to it. Do not copy it into a skill.
- Prefer a script to a skill when the only value is "run these commands in this order".

## Step 3: Filter

Keep a skill candidate only when you can answer all three questions:

1. Which sentence does a user type to trigger it?
2. What specific failure occurs without it (time lost, wrong result)?
3. Did it occur more than once, or will it clearly occur again?

Also reject scope that is too wide, scope that is one command, and knowledge that will soon be out of date.
Recommend at most 3 skills. Rejecting most candidates is normal.

## Step 4: Show the recommendation

For each candidate, show:

- **Proposed:** the form, the trigger sentence (for a skill), and an approximate cost to build.
- **Rejected:** its own reason. A shortlist without reasons cannot be corrected.

Keep each trap exact: the wrong order or command, the correct one, the reason, and the cost (for example
"40 minutes lost"). Then ask the user which items to build. Stop.

## Step 5: Build the selected items

- Build from the transcript, not from memory. Copy the exact commands and traps.
- Put a helper script that you already wrote into the skill.
- Use a skill-creator skill for the format, when one is available.

## Step 6: Say what you verified

State which parts you checked: the commands run, the script works on real and failure cases. Say that the
guidance itself is not verified until an eval compares agents with and without the skill.

## Communication style

Apply these rules to all text that this skill produces (the recommendation and every skill, memory or doc that you write). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- In reviews: be honest and brutal. State the verdict and the defects first.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
