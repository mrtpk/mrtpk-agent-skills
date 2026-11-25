---
name: unattended-run
description: Run a long series of experiments (training, evaluation, benchmarks, parameter sweeps) while the user is away, with logs, findings, decisions, and short status replies. Use when the user asks to run or continue an experiment series unattended ("I will be back in N hours", "continue the experiments"), or asks "how is it?" or "progress?" during such a run. Do not use it when "unattended" only means "do not ask questions" inside another skill (for example a write-up or an explainer site); follow that skill instead.
---

# Unattended experiment runs

## Before the user leaves

At the start of a new series, ask for each item below that the user did not give. Ask all of them in one message. Do not start a job before the user answers. Do not invent the answers.

- When the user is already gone, do the read-only preparation (read the scripts and configs, check the paths). Write the open questions in `progress-log.md`. Do not record an assumed user answer as a decision.
- When you have no shell and no background-task tool, say so in your first reply. Do not give the jobs to a subagent instead.

The items:

- The goal and the stop rule (a score, a time, a count of runs).
- The permissions (GPU or other shared hardware, downloads, installs, deletes, restarts of jobs or servers).
- The stall time: how long a log can stay unchanged before you treat the job as hung. Default to 30 minutes and tell the user.
- The disk limit: the free space at which you stop and record the problem. Default to 10 % free and tell the user.
- Any other limit. Do not add a limit of your own beyond these two. If a protocol has a limit, show it and ask.
- What to do when a job fails or hangs: restart it, skip it, or stop the series.

## During the run

- Run every long command in one tmux session (or the background-task feature of the agent). Write each job's output to its own log file.
- Do not say that a job runs until you see its process and its log growth.
- Make Python output unbuffered (`python -u` or `PYTHONUNBUFFERED=1`). Buffered output makes a healthy job look hung.
- Start each job with a wrapper. The wrapper writes the exit code to a marker on success and on failure. Use one marker name per job:

  ```bash
  rm -f jobs/run3.done
  ( set -o pipefail; <command> > jobs/run3.log 2>&1; echo $? > jobs/run3.done ) &
  echo $! > jobs/run3.pid
  ```

- Wait with a blocking wait, not with short sleeps: a background-task notification, a monitor tool, or one loop. The loop also stops when the process is gone with no marker (a killed shell or tmux session writes no marker):

  ```bash
  until [ -f jobs/run3.done ] || ! kill -0 "$(cat jobs/run3.pid)" 2>/dev/null; do sleep 60; done
  sleep 1; cat jobs/run3.done 2>/dev/null || echo crashed
  ```

- Read the exit code in the marker. Do not treat "marker exists" as success. Code `0` is success. Another code, or `crashed`, is a failure: follow the user's rule for failures.
- Check that a long job's log grows. When the log does not change for the stall time, treat the job as hung. A hung job with an idle server is common. Restart it only when the user gave permission for restarts. Else record the problem and follow the user's rule for failures.
- Check the free disk space before each job. At the disk limit, stop and record the problem.
- Get each time from `date`. Never estimate a time in a log.
- Keep three files in the run folder that the user names (default: the folder of the experiment series). Append to them:
  - `progress-log.md`: time, action, result. One line per event.
  - `findings.md`: numbered findings (F1, F2, ...), each with the numbers and the source file.
  - `decisions.md`: numbered decisions (D1, D2, ...) with the reason and the rejected options.
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
- In replies to the user: be blunt. Do not patronize. Do not praise, soften, or pad.
- Text that this skill makes for other readers (pages, documents, reports, figures) follows the tone rules of this skill, for example neutral words for gaps.
- Be brief and to the point.
- Sentence limits: at most 20 words in an instruction, at most 25 words in a description.
- Code, file names, identifiers and technical names stay as they are.

## At the end

- Write the final state in the progress log and the findings.
- Give the verdict first: the best result, the kept configuration or model, and the gap to the goal.
- List what did not work, the open items, and the disk use of the work folders.
- Do not delete anything without a request.
