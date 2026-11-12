---
name: extract-skills
description: Mine the current conversation for reusable knowledge and turn what is worth keeping into skills, memories, docs or scripts. Use this when the user asks what skills could come out of this session, whether anything here is worth reusing or saving, to turn this work or workflow into a skill, or to capture what was learned before the context is lost. Also use it at the end of a long or painful session, when a problem took several wrong turns to solve, or when you notice you have re-derived the same sequence of steps more than once - the knowledge that cost the most to get is the knowledge most likely to be thrown away.
---

# Extracting reusable skills from a conversation

A long session makes two things: the work, and the knowledge that you got to
do the work. The work goes into a commit. The knowledge is usually lost. For
example: the dead end that you stopped, the flag that had to come first, the
command that looked correct but did nothing and gave no error. The next
session must find this knowledge again.

This skill collects that knowledge. The difficult part is not to find candidates.
The difficult part is to reject most of them. Many weak skills are worse than no skills.
Each skill uses context when it loads and attention when you maintain it. A
skill that copies a document becomes different from that document over time.

## Step 1: Scan the conversation for candidates

Read the session again. Read the transcript, not your memory of it. Your memory
keeps only the clean version. Look for:

- **A sequence you ran more than once.** Three steps in a fixed order, done
  two times, is a workflow. The second run is the evidence.
- **Facts that cost time to find.** Examples: a command whose obvious form is
  wrong, a default that does not do what its name says, a constraint on
  order, a tool that was not where you thought. Measure the cost in minutes
  lost, not in how clever the finding was.
- **Corrections the user made.** When the user changed your approach, that is
  a preference. Without a record, you will break it again.
- **Anything you found by reading source code or docs.** If you had to
  derive it, the next agent must also derive it.
- **Dead ends.** What did not work, and why, is as reusable as what did work.
  Nobody writes it down.
- **Where you were wrong.** A wrong assumption that stayed for some time is
  the item with the highest value in the transcript.

Make a plain list of candidates before you judge them. If you judge while you
collect, you will miss items.

## Step 2: Route each candidate — most are not skills

This step does the main work. For each candidate, decide which form it must
have:

| the knowledge is... | put it in | why |
|---|---|---|
| a workflow with many steps, decisions and traps | **a skill** | it must load at the correct time and control behaviour |
| a fact about the user, their setup or their preferences | **memory** | it applies to all tasks, not only when a task triggers it |
| how this system works or why it has this design | **a doc in the repo** | it belongs next to the code, and humans also read it |
| a fixed sequence of commands with no decisions | **a script** | code is better than prose for work that a machine can do alone |
| reference data: mappings, IDs, measured numbers | **a doc or config** | a copy in a skill will become different from the real source |
| a task that a competent agent does well without help | **nothing** | instructions for obvious tasks are noise |

Do not make these two routing mistakes:

**Copying something that already exists.** If the fact is in a README, a
config comment and a memory, a skill copy makes four places to update. It also
makes three chances to be wrong. Refer to the source instead.

**Putting a script inside a skill.** If the only value is "run these commands
in this order", write the script. Use a skill only when something must make a
decision.

## Step 3: Filter hard

Reject a candidate unless you can answer all three questions:

1. **Who triggers it, and with which words?** Write the sentence that a user
   types. If you cannot, the skill will never load. A skill that nobody
   triggers has no value.
2. **What goes wrong without it?** Name the specific failure: time lost, a
   wrong turn, or an expensive mistake that occurs again. "It would be nice to
   document" is not an answer.
3. **Did it occur more than once, or will it clearly occur again?** One
   occurrence with no reason to expect another is a note, not a skill.

Also reject:

- **Scope that is too wide.** "Backend development" helps nobody. A skill is
  useful only when it is specific enough to hold real traps.
- **Scope that is too narrow.** A single command with one flag is one line in
  a README.
- **Knowledge that will soon be out of date.** For example: knowledge tied to
  a version that will change soon, or a workaround for a bug that someone is
  fixing.

Expect to reject most candidates. Find four and build one: that is a normal
ratio.

## Step 4: Propose before building

Show the user the shortlist. Also show the rejected candidates and the reason
for each. The rejects are important. They show your reasoning, and the user can
overrule you. The user often knows that a candidate will occur again when you
cannot know.

Give an approximate cost to build each one. Then build the ones that the user
selects. Do not build several skills before the user selects them and then show
them as a surprise. That uses the user's tokens on a decision that belongs to
the user.

## Step 5: Build it from the transcript, not from memory

When you build, use what really occurred:

- **Copy the traps exactly.** Put the exact wrong command next to the correct
  one. This has more value than a paragraph of advice. Specific text is better
  than general text.
- **Keep the cost with the trap.** "This wastes an hour" makes agents obey.
  "Prefer X" does not.
- **Explain why, not only what.** An agent that knows the reason can handle a
  case that you did not expect. An agent that only follows rules fails in
  other ways.
- **Include the script that you already wrote.** If you made a helper during
  the session, put it in the skill. Do not only describe it. You already paid
  for it.
- **Remove project details if the skill must work in other places.** Decide at
  the start: is this skill for one repository or for all? That decision
  changes every example in it.

If a skill for writing skills is available, use it. Do not make up the format.

## Step 6: Say what you verified

A new skill is not tested. State exactly which part you checked:

- Its commands run as written: you ran them.
- Its included script works: you ran it on real cases, and on failure cases.
- Its *guidance* changes the behaviour of an agent: this is almost always not
  verified. To verify it, you must evaluate agents with the skill and without
  the skill.

Write this difference where the user will see it. "Skill added" tells the user
that all three are true. Usually only the first is true.

## Communication style

Apply these rules to all text that this skill produces (the recommendation and every skill, memory or doc that you write). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## Anti-patterns

- **Collecting everything.** If you record each detail, the skill becomes too
  large. The few important items are then hard to find.
- **Writing the skill that you wanted to have.** Record the session that
  occurred, not a better version of it.
- **General advice.** For example: "Test your code", "be careful with
  migrations". If the advice applies to all projects, it gives no information.
- **Not reporting the rejects.** A shortlist without the reasons looks random.
  The user cannot correct it.
