# Writing the posts

The posts use the blog's voice, not ASD-STE100. When the blog repo has a style guide (for example `STYLE.md`), it is the source of truth, also for the title and date format. When the style guide and an existing series in the repo disagree, follow the style guide and tell the author. Otherwise use this file and `voice.md`.

## Voice

The voice rules are in `voice.md` (a copy of the kaizen `STYLE.md` voice, synced from `brand-kit`). Read it before you write. The short form:

- First person, conversational, short paragraphs.
- Open with the problem, a question or a concrete fact, in one sentence. Then: "This note is about ...".
- Never open with "Lately" or "I have been". Do not open two posts in a row with the same words.
- In a series, each part opens with its own problem, not with the series name.
- Close with "So, in short: ..." in one or two sentences.
- No hype words: robust, seamless, powerful, leverage, game-changer.

## Structure of one part

1. Opening line (the problem of this part), then "This note is about ..." and a link to the previous part.
2. "Before diving in": the minimum background.
3. The idea, with the formula and one worked example.
4. "Let's look at the code.": a short check that prints `<what>. Is pass?`. A deliberate counter-example may print `False`, with a comment that says so.
5. A figure per main idea, with alt text and a caption "*Figure: ...*".
6. What the reference implementation does differently, and why we chose our way. No citations.
7. The gaps, with measured numbers, in the agreed tone.
8. "So, in short: ...".
9. A link to the full script: "The full script is available [here](...)".
10. `**Reference:**` list with link references.
11. The link to the next part.

## Front matter (Jekyll; default only, the blog's style guide wins)

```
---
layout: post
title:  "<Series> - <topic>"
date:   <yyyy-mm-dd> 00:00:00 +0530
categories: <space separated>
mathjax: true
---
```

Math: `$$ ... $$`. Code: `{% highlight python %} ... {% endhighlight %}`.

## Numbers and claims

- Copy each measured number from the script output. If you change the script, re-run it and re-check every number in the post.
- A number from a paper or another reference is fine when the post names the source ("the paper reports ...", with a link). Copy it exactly. Keep it apart from the numbers that the post's script measures.
- Treat the author's style rules (for example "no months", "no exact dates") as guidance unless the author calls them hard rules. Ask when a real link or a quote breaks one.
- Say what a number measures: "2.8 % of 200,000 outputs differ from exact rounding, by at most 1".
- Do not write "X requires Y" about a library unless the pinned code shows it.
- Do not round a count into a ratio that changes it.
- Do not write a motive, an anecdote or a debugging story that the author did not tell you.
- When the author does not remember a number, say so in a sentence that the author approves (for example: "on par with the reference in our tests; I no longer have the final numbers").

## Voice of credit

- Team work is "we": "The other team gave us the constraints, we did the math and tested it on real data."
- "I" for the author's own part and for the new analysis ("this week I re-ran ...").
- Credit the people who guided the work, in the first and the last part.
