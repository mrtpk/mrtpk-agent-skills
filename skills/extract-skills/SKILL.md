---
name: extract-skills
description: Mine the current conversation for reusable knowledge and turn what is worth keeping into skills, memories, docs or scripts. Use this when the user asks what skills could come out of this session, whether anything here is worth reusing or saving, to turn this work or workflow into a skill, or to capture what was learned before the context is lost. Also use it at the end of a long or painful session, when a problem took several wrong turns to solve, or when you notice you have re-derived the same sequence of steps more than once - the knowledge that cost the most to get is the knowledge most likely to be thrown away.
---

# Extracting reusable skills from a conversation

A long session produces two things: the work, and everything you had to learn
to do the work. The work gets committed. The learning usually evaporates — the
dead end you backed out of, the flag that had to come first, the command that
looked right and silently did nothing. The next session pays for it again.

This is about harvesting the second thing. The hard part is not spotting
candidates; it is refusing most of them. A pile of mediocre skills is worse
than none, because each one costs context to load and attention to maintain,
and a skill that duplicates a document will drift away from it.

## Step 1: Scan the conversation for candidates

Re-read the session — the actual transcript, not your memory of it, because
what you remember is the clean version. Look for:

- **A sequence you ran more than once.** Three steps in a fixed order, done
  twice, is a workflow. The second time you did it is the evidence.
- **Facts that cost time to discover.** A command whose obvious form is wrong,
  a default that does not do what it says, an ordering constraint, a tool
  missing where you assumed it existed. Measure the cost in minutes lost, not
  in how clever the finding was.
- **Corrections the user made.** Where they redirected your approach, that is a
  preference you will otherwise violate again.
- **Anything you worked out by reading source or docs.** If you had to derive
  it, so will the next agent.
- **Dead ends.** What did not work, and why, is as reusable as what did — it is
  just never written down.
- **Where you were wrong.** A wrong assumption that survived a while is the
  highest-value thing in the transcript.

List candidates plainly before judging them. Judging while gathering makes you
miss things.

## Step 2: Route each candidate — most are not skills

This is the step that does the work. For each candidate, ask what form it
should take:

| the knowledge is... | put it in | why |
|---|---|---|
| a multi-step workflow with judgement and traps | **a skill** | it needs to load at the right moment and shape behaviour |
| a fact about the user, their setup or their preferences | **memory** | it applies everywhere, not just when a task triggers |
| how this specific system works or why it is built this way | **a doc in the repo** | it belongs beside the code and is read by humans too |
| a deterministic sequence of commands with no judgement | **a script** | code beats prose for anything a machine can just do |
| reference data — mappings, IDs, measured numbers | **a doc or config** | a skill copy of it will drift from the real source |
| something a competent agent does well unaided | **nothing** | instructions for the obvious are noise |

Two routing mistakes to avoid:

**Duplicating something that already exists.** If the fact is in a README, a
config comment and a memory, a skill copy makes four places to update and three
chances to be wrong. Point at the source instead.

**Wrapping a script in a skill.** If the whole value is "run these commands in
this order", write the script. A skill is for when something has to decide.

## Step 3: Filter hard

Reject a candidate unless you can answer all three:

1. **Who triggers it, and in what words?** If you cannot write the sentence a
   user would type, it will never load. A skill nobody triggers is dead weight.
2. **What goes wrong without it?** Name the concrete failure — time lost, a
   wrong turn, an expensive mistake repeated. "It would be nice to document" is
   not an answer.
3. **Has it happened more than once, or will it obviously recur?** One
   occurrence with no reason to expect another is a note, not a skill.

Also reject:

- **Scope that is too broad.** "Backend development" helps nobody. A skill
  earns its place by being specific enough to carry real traps.
- **Scope that is too narrow.** A single command with one flag is a line in a
  README.
- **Knowledge that will expire soon.** Pinned to a version about to change, or
  a workaround for a bug being fixed.

Expect to reject most candidates. Surfacing four and building one is a normal,
healthy ratio.

## Step 4: Propose before building

Show the user the shortlist with the rejects and the reason for each. The
rejects matter — they show the thinking and let the user overrule you, and they
often know a candidate will recur when you cannot tell.

Say roughly what building each one costs. Then build what they pick. Do not
speculatively build several skills and present them as a surprise; that spends
their tokens on a decision that was theirs.

## Step 5: Build it from the transcript, not from memory

When building, go back to what actually happened:

- **Put the traps in verbatim.** The exact wrong command next to the right one
  is worth more than a paragraph of advice. Concrete beats general.
- **Keep the cost attached.** "This wastes an hour" earns compliance that
  "prefer X" does not.
- **Explain why, not just what.** An agent that understands the reason handles
  the case you did not foresee; one following rules fails differently.
- **Bundle the script you already wrote.** If you built a helper during the
  session, ship it with the skill rather than describing it. You already paid
  for it.
- **Strip project specifics if it is meant to travel.** Decide up front whether
  this skill is for one repository or for anywhere, because that changes every
  example in it.

Use a skill-authoring skill if one is available rather than inventing the
format.

## Step 6: Say what you verified

A freshly written skill is untested. Be precise about which part you checked:

- Its commands run as written — you ran them.
- Its bundled script works — you ran it against real cases, including
  failures.
- Its *guidance* changes an agent's behaviour — almost certainly unverified,
  since that needs an evaluation with and without the skill.

Write that distinction down where the user will see it. "Skill added" implies
all three, and it is usually only the first.

## Communication style

Apply these rules to all text that this skill produces (the recommendation and every skill, memory or doc that you write). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Anti-patterns

- **Harvesting everything.** The reflex to capture each detail produces bloat
  that buries the few things that mattered.
- **Writing the skill you wish you had needed.** Capture the session that
  happened, not an idealised version of it.
- **Generic advice.** "Test your code", "be careful with migrations" — if it
  would fit any project, it carries no information.
- **Skipping the rejects when reporting.** The shortlist without the reasoning
  looks arbitrary and cannot be corrected.
