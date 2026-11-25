# Voice: technical documents

Applies to text that a skill makes for other readers: write-ups, explainer sites, report pages,
presentations and figure text. Blog posts use `blog.md` instead.

When the user or the style guide of the target repo asks for another style, follow that request.
When the skill has its own writing rules (for example a `writing.md`), those rules add to this file.

## Language: ASD-STE100 (Simplified Technical English)

Code, file names, identifiers and technical names stay as they are. Rules 6-8 apply to running text,
not to figure labels or slide fragments. With plain English instead of ASD-STE100, keep rules 3, 6, 7, 8
and 10, and drop the word limits.

1. Use approved, simple words. Use one word for one meaning, and one meaning for one word.
2. Max **20 words** in an instruction sentence. Max **25 words** in a descriptive sentence.
3. Use the active voice ("The scheduler selects ...", not "... is selected by the scheduler").
   Passive is allowed only when the actor is unknown or not important.
4. Use simple tenses: present, simple past, future. Do not use "-ing" forms as verbs.
5. One instruction per sentence. Write the instruction first: "Set both variables to the same value."
6. Max **6 sentences** in a paragraph. One topic per paragraph.
7. Use a numbered list for steps, and a bulleted list for items that have no order.
8. Write warnings and cautions **before** the step they apply to.
9. Use articles ("the", "a") and do not drop words to make a sentence short.
10. No idioms, jokes, slang or rhetorical questions in descriptive text. (Quiz questions are questions.)

**Word substitutions**

| Do not write | Write |
|---|---|
| utilize, leverage | use |
| perform, carry out | do |
| initiate, commence | start |
| terminate | stop, end |
| obtain, retrieve, fetch (in prose) | get |
| create (in prose) | make |
| require | need, must |
| prior to / subsequently | before / after, then |
| in order to | to |
| ensure | make sure |
| approximately | about |
| numerous | many |
| via | through, with |
| due to | because of |
| it is possible to | you can |
| harness (as a verb), robust, seamless, powerful, game-changer, simply | (delete; say the fact) |

## Tone

- Short and calm. Say what the code does, then why.
- A concrete example with real numbers is better than an abstract sentence.
- Use neutral words for gaps and old designs: "gap" and "refinement", not "mistake" or "leak".
- Do not praise the code, the team or the reader.

## Facts

- Every number comes from a named source: a check script, a file:line, or a cited document.
- Do not type a measured number by hand.
- Mark what a figure or a summary simplifies.
