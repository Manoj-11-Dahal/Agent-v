---
name: capability-aware-router
description: "Choose relevant skills using actual available tools, runtimes, permissions, and budgets, with honest fallbacks."
---
# Capability-aware router

1. Identify the requested outcome and required capabilities before picking a workflow.
2. Inspect available tools and narrowly relevant runtimes; do not enumerate secrets.
3. Choose one process skill plus a small number of domain specialists. Read entry points
   and only the references needed for the current step. Resolve packed references through
   `.agentic/bin/skill-files.py` if its archive index marks the skill as packed.
4. Distinguish installed guidance, installed runtime, configured service, connected tool,
   tested integration, and granted permission. None implies the next.
5. Use real subagents only if exposed by the host. Otherwise sequence the work. Use CLI
   graph commands if native MCP tools are absent; read source if neither is available.
6. When a critical capability is missing, explain the blocker and propose a bounded
   setup action. Do not install services or incur paid API costs just because a skill says so.
7. Re-evaluate capabilities after failures; do not repeatedly retry unsupported operations.

Output a short plan: goal, selected skills, available tools, missing capabilities,
fallbacks, required approvals, and verification. Trivial tasks need no elaborate plan.
