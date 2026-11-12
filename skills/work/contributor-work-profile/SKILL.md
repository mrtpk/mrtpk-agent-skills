---
name: contributor-work-profile
description: >-
  Synthesize what a person did at the company from their YouTrack issues, Outline
  wiki pages, and mined issue comments, and write a narrative work-summary
  markdown plus an optional impact/leveling evaluation and growth plan. Use when
  asked what a person did/contributed, to assess their impact, judge their level
  (e.g. senior vs staff), or plan how they grow.
---

# Contributor Work Profile

Turn raw issue/wiki data into a narrative account of what a person did, their
impact, and (optionally) a leveling assessment and growth plan — always grounded
in cited issue IDs and wiki links.

## Prerequisites: gather the data first

You need two inputs. If they don't already exist as report files, generate them:
- **Issues with states** → use the `youtrack-user-issue-report` skill.
- **Authored wiki pages** → use the `outline-wiki-author-report` skill.

Read those report files before synthesizing.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Read the issue report + wiki report files
- [ ] 2. Cluster the work into themes (infra, research, demos, etc.)
- [ ] 3. Mine issue comments for substance (parallel subagents by theme)
- [ ] 4. Write the requested doc(s): work summary / evaluation / growth plan
```

**1. Read the inputs.** The issue table (Issue | Summary | State) and the wiki
list give breadth. Titles alone are shallow — comments give the real story.

**2. Cluster into themes.** Group issues + wiki pages into a handful of coherent
tracks (e.g. infrastructure, tooling, research, customer work, internal
demos). This structures both the mining and the final narrative.

**3. Mine comments in parallel.** Issue titles hide real accomplishments (e.g. a
short "demo" issue can hide a shipped application that only the comments
describe). Use `get_issue_comments` via the
YouTrack MCP. For breadth, spawn several general-purpose subagents in parallel,
one per theme, each given its issue IDs and asked to return what the person
actually accomplished (decisions, deliverables, links) with issue-ID citations.
The YouTrack namespace/tools are described in
`../youtrack-user-issue-report/reference.md`; if a subagent can't read that, restate:
the YouTrack MCP tool `get_issue_comments` (with a dynamic-tool namespace, use
`GetDynamicTools` then `CallDynamicTool`).

**4. Write the requested document(s).** Match what the user asked for:
- **Work summary** (`what did X do`): themed narrative, each track citing issues.
- **Evaluation** (`impact` / `senior vs staff`): honest read of impact signals
  (foundational infra others depend on, decision-shaping analysis, end-to-end
  ownership, external/stakeholder-facing work, force-multiplier behavior). State
  that leveling depends on the org's rubric, which you can't see; infer from the
  *nature* of the work, don't assert a title as fact.
- **Growth plan** (`how to reach staff` / next steps): concrete, actionable moves
  tied to work already underway, each grounded in specific issues.

Write to the file the user names (e.g. `<user>-work.md`, `<user>-eval-and-goal.md`).
When the user says "cite examples / be descriptive", attach specific issue IDs and
wiki links to every claim.

## Output template (work summary)

```markdown
# What <Display Name> (`<email>`) did at <Company>

<One-line role framing.>

## <Track 1 name>
<What they built/did and why it mattered> (<issue-id>, <issue-id>).

## <Track 2 name>
...

## Bottom line
<Overall role and scope in 2-3 sentences.>
```

## Principles

- Every claim cites evidence (issue IDs, wiki links, comment findings).
- Distinguish shipped/decided work from planned/blocked work.
- Be honest and specific; avoid inflated or hedged generalities.

## Communication style

Apply these rules to all text that this skill produces (the work summary, the evaluation, the growth plan and the replies). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.
