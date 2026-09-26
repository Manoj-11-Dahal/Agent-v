---
name: cad-agent
description: Guide an authorized CAD design task using the upstream CAD Agent rendering server, build123d modeling, visual review, measurements, and export. Requires a separately configured CAD backend.
---
# CAD Agent — locally repaired entry point

This repository ships a SKILL.md without required YAML metadata. This wrapper
adds valid discovery metadata and preserves its guide in references/upstream-SKILL.md.
It does not install or start the rendering server.

## Workflow
1. Clarify units, dimensions, tolerances, material, manufacturing process, and export format.
2. Verify the user has a configured CAD Agent backend and permission to use it.
   Do not assume Docker, CAD libraries, GPU, or native MCP tools are available.
3. Read references/upstream-SKILL.md for the upstream API and modeling workflow.
4. Review any installation or container commands before running them. Do not
   expose a code-executing modeling endpoint publicly; restrict its access and mounts.
5. Create the model in the approved backend, inspect returned renders, verify
   numerical dimensions, and iterate. A render is not proof of dimensional accuracy.
6. Export into the approved project directory and report format, dimensions,
   tolerances checked, and untested manufacturing constraints.

## License and limitations
The upstream code has a PolyForm Small Business License with a Perimeter addendum;
review LICENSE and NOTICES.md before organizational or commercial use.
Backend, container, and all API examples are untested in this workspace.
