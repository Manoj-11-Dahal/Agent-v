---
name: agent-budget-guard
description: "Set and monitor time, retry, tool-call, data, and cost budgets for bounded agent workflows."
---
# Agent budget guard

1. Agree on limits proportional to the task: elapsed time, tool calls, parallel jobs,
   retries, output size, request rate, and paid usage where applicable.
2. Assign stage budgets and stop conditions. Avoid nested unbounded retries and blind
   loops; use backoff only for transient failures. Do not retry destructive operations
   unless their idempotence and prior result are known.
3. Distinguish measured usage from estimates. If the host does not expose token or
   billing data, say so rather than inventing exact costs.
4. Use bounded commands and the host's managed process tools for long-running services.
   Do not leave orphaned jobs or public listeners after a temporary test.
5. On exhaustion, checkpoint progress, stop active work safely, and ask whether to expand
   the budget. Do not bypass provider limits or redistribute load to evade them.
6. Report consumed and remaining budget, incomplete stages, and resumable next steps.

This skill documents controls; it does not enforce limits without an implementation.
