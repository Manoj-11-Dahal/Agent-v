---
name: vscode-skills-marketplace
description: "Guide setup and use of the VS Code Agent Skills Marketplace extension without duplicating the canonical skill library."
---
# VS Code Skills Marketplace — local guidance

This is a locally authored guidance skill, not an upstream SKILL.md. The source
repository is a VS Code extension, not a skill pack. Read references/upstream-README.md.

1. Confirm that the user is working in VS Code on the machine being configured.
2. Verify the extension identity `formulahendry.agent-skills` and its requested permissions.
3. Ask before installing the extension or changing its configured repositories.
4. Configure sources and inspect the destination used by the installed extension
   version; do not assume it supports `.agentic/skills/` directly.
5. Keep this workspace's canonical library and lock file intact. Stage extension
   downloads and merge reviewed entries instead of creating competing libraries.
6. Keep optional GitHub tokens in the client's secret storage; never in skill files.
7. Verify discovery on a small known skill and record the actual client result.

The extension is not installed here. This file does not enable an editor or its APIs.
