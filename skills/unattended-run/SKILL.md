---
name: unattended-run
description: Run a long series of experiments (training, evaluation, benchmarks, parameter sweeps) while the user is away, with logs, findings, decisions, and short status replies. Use when the user asks to run or continue an experiment series unattended ("I will be back in N hours", "continue the experiments"), or asks "how is it?" or "progress?" during such a run. Do not use it when "unattended" only means "do not ask questions" inside another skill (for example a write-up or an explainer site); follow that skill instead.
---

# Unattended experiment runs

## Before the user leaves

Get these from the user. Do not invent them.

- The goal and the stop rule (a score, a time, a count of runs).
- The permissions (GPU or other shared hardware, downloads, installs, deletes, restarts of jobs or servers).
- Any limit. Do not add a limit of your own. If a protocol has a limit, show it and ask.
- What to do when a job fails or hangs: restart it, skip it, or stop the series.

## During the run

- Run every long command in one tmux session (or the background-task feature of the agent). Write each job's output to a log file.
- Write a `.done` marker file when a job ends. Wait for it with a blocking wait, not with short sleeps: a background-task notification, a monitor tool, or one loop such as `until [ -f job.done ]; do sleep 60; done`.
- Check that a long job's log grows. A hung job with an idle server is common. Restart it only when the user gave permission for restarts. Else record the problem and follow the user's rule for failures.
- Get each time from `date`. Never estimate a time in a log.
- Keep three files and append to them:
  - `progress-log.md`: time, action, result. One line per event.
  - `findings.md`: numbered findings (G1, G2, ...), each with the numbers and the source file.
  - `decisions.md`: numbered decisions with the reason and the rejected options.
- Record a negative result as a finding. Record each result that is not kept, and why.
- Do not change folders that the user marked read only.
- Before you choose between two close results, check the noise (seeds). Run one more seed if needed.

## Status reply ("how is it?", "progress?")

Use this form. Keep it under ten lines.

```
State: <running X | waiting for Y | done>
Last result: <number, compared with the base and the best so far>
Next: <the next step and its ETA from date>
Problem: <none | the problem and what you did>
```

## Communication style

Apply these rules to all text that this skill produces (logs, findings, decisions, status replies and the final report). Use another language style only when the user or the style guide of the target repo asks for it.

- Always write in ASD-STE100 (Simplified Technical English): short sentences, active voice, one instruction per sentence, approved words with one meaning, no idioms.
- Be blunt. Do not patronize. Do not praise, soften, or pad.
- Reviews must be honest and brutal. State the verdict and the defects first.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## At the end

- Write the final state in the progress log and the findings.
- Give the verdict first: the best result, the kept configuration or model, and the gap to the goal.
- List what did not work, the open items, and the disk use of the work folders.
- Do not delete anything without a request.
