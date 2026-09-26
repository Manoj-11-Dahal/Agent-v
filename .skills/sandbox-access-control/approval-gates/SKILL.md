---
name: approval-gates
description: "Define and record explicit approval boundaries for sensitive agent actions without granting permissions automatically."
---
# Approval gates

Before a consequential action, describe its target, exact change, expected side effects,
reversibility, data destination, and cost. Request approval only where needed; do not
interrupt routine reversible work that the user has already authorized.

Require a scoped decision before destructive changes, publishing, deployment, changing
access controls, paid external actions, sharing private memory, broad scans, or modifying
production resources. Security testing must remain within authorized scope and applicable
platform rules. Approval for one action does not authorize a broader target or technique.

Record action ID, target, permitted operations, exclusions, time window, approving user
message reference, decision, and expiry. Do not invent a signature or store credentials.
An absent or ambiguous decision is not approval. Reconfirm when scope materially changes.

Before execution, compare the actual command or operation with the approved action.
Afterward, record result and rollback availability. This Markdown skill is a checklist,
not a technical policy enforcement engine; use host permissions for enforcement.
