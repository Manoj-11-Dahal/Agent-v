---
name: agentic-sandbox
description: "Design and verify bounded agent execution with least privilege, scoped filesystem access, resource limits, and explicit network policy."
---
# Agentic sandbox

Read the existing `agent-sandbox` skill when implementing platform-specific isolation.
This skill is an orchestration checklist; installing it creates no new sandbox.

1. Define trusted inputs, untrusted code, allowed outputs, threat model, and stop conditions.
2. Select an available isolation mechanism. Do not claim a normal subprocess is a secure
   sandbox. Container isolation alone is not equivalent to a hardened virtual machine.
3. Default to a non-root identity, read-only source where practical, a separate writable
   output directory, bounded CPU/memory/PIDs/time, and no host credential directories.
4. Do not mount Docker sockets, broad host paths, SSH agents, or cloud credentials into
   untrusted execution. Never grant privileged mode merely to make a command work.
5. Define egress allowlists and approved secrets individually. Browser-facing code must
   use the host's supported routing, not sandbox-local addresses as if they were remote.
6. Test allowed and denied behavior on harmless fixtures: writes outside scope denied,
   unapproved network blocked when enforcement exists, resource timeout effective,
   cleanup completed. If enforcement is unavailable, report it and do not run untrusted code.
7. Keep audit logs free of secrets and obtain approval before relaxing isolation.

Arena's supplied workspace sandbox remains the execution boundary; this guidance does
not change its privileges, add Docker support, or install a new isolation runtime.
