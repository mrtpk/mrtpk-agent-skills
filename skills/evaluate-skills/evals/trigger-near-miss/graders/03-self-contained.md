---
type: llm
focus: trace
weight: 1
---

In the trigger evals that the agent wrote, every query that must start sql-review contains the SQL query or names the file that holds it. No query depends on earlier conversation, such as "the query above" or "this one".
