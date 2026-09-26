---
name: evidence-ledger
description: "Track claims, commands, artifacts, timestamps, and verification limits so agent completion reports are supported by evidence."
---
# Evidence ledger

Create a small JSONL or Markdown record in the approved project directory. For each
material claim record an ID, claim, evidence type, command or artifact path, timestamp,
exit status or observed result, scope, and limitations. Redact secrets and private data.

Use statuses: observed, tested, inferred, not-tested, failed, or superseded. Do not convert
an inference into a test result. Installation is not configuration; a smoke test is not
full coverage; a screenshot is not proof of all interaction paths.

Link build/test reports to exact revisions or file hashes when practical. Prefer bounded
logs and reproducible commands over huge transcripts. Keep source provenance for factual
research, and record contrary results rather than selecting only successes.

Before a final report, reconcile claims against records. State untested areas and failed
checks explicitly. After changes invalidate evidence, mark it stale and rerun affected tests.

Acceptance: each major success statement has inspectable evidence and a clear tested scope.
