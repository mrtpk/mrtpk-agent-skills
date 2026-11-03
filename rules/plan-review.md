---
description: Review each new plan with the model recorded for plan review
alwaysApply: true
---

# Plan review

Review each new plan before implementation.

## Model

Read `plan-review-model.txt` in the same directory as this rule.

When that file is missing or empty, ask the user for the model id. Write the model id as the only line of `plan-review-model.txt`.

Use that model id for this review and for every later plan review. Do not ask again while the file has a model id.

When the user asks to change the model, write the new model id in that file. Use the new model id after that.

## Review

Start a review subagent immediately after you draft a plan. Give that subagent the recorded model id.

Apply the review comments before you start the implementation.
