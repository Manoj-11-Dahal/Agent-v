# Memory, Context & Knowledge Sharing

**14 folder skills** · Category: `memory-context`

[Quick index](../../QUICK-INDEX.md) · [Searchable catalog](../../catalog.html) · [Detailed CSV](../skills.csv) · [JSON manifest](../index.json)

Full descriptions and entry-point links are retained here. Detailed metadata, file inventories and outlines are stored once in the shared CSV tables; use the lookup helper to retrieve a selected record as JSON. No tool or permission is enabled by this directory.

`python3 /home/user/skills/_catalog/find.py --category memory-context --limit 10`

| Skill / entry point | Description | Available files | Missing | Recorded warning |
|---|---|---:|---:|---|
| <a id="skill-22a9405c3d21"></a>[agent-memory](../../memory-context/agent-memory/SKILL.md) | Add persistent memory to AI coding agents — file-based, vector, and semantic search memory systems that survive between sessions. Use when a user asks to "remember this", "add memory to my agent", "persist context between sessions", "build a knowledge base for my agent", "set up agent memory", or "make my AI remember things". Covers file-based memory (MEMORY.md), SQLite with embeddings, vector databases (ChromaDB, Pinecone), semantic search, memory consolidation, and automatic context injection. | 2 | 0 | — |
| <a id="skill-ba06e5e485a0"></a>[checkpoint-resume](../../memory-context/checkpoint-resume/SKILL.md) | Save and restore concise, evidence-backed project checkpoints without persisting secrets or private reasoning. | 1 | 0 | — |
| <a id="skill-ccbad17e7346"></a>[context-engineering](../../memory-context/context-engineering/SKILL.md) | Optimizes agent context setup for maximum output quality. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when configuring rules files and context for AI-assisted development. Covers the context hierarchy, packing strategies, and confusion management. | 2 | 0 | — |
| <a id="skill-27ff10bbce77"></a>[context-shunt](../../memory-context/context-shunt/SKILL.md) | Offload large / multi-file reads to a cheap worker model so raw files never enter Claude's context (token savings) | 1 | 0 | — |
| <a id="skill-15f61deea870"></a>[im-local-kb](../../memory-context/im-local-kb/SKILL.md) | IM 知识整理和分析技能，专注于从聊天记录中提取高价值的知识 | 1 | 19 | — |
| <a id="skill-a9aff9e0737a"></a>[mem0](../../memory-context/mem0/SKILL.md) | You are an expert in Mem0, the memory infrastructure for AI applications. You help developers add persistent, personalized memory to LLM-powered apps and agents — storing user preferences, conversation history, facts, and context that persists across sessions, enabling AI that remembers users, learns from interactions, and provides increasingly personalized responses. | 2 | 0 | — |
| <a id="skill-606e9033fcb6"></a>[mnemos](../../memory-context/mnemos/SKILL.md) | Task-scoped memory lifecycle — typed MnemoGraph prevents lossy context compaction by treating facts/decisions/code-refs/handoffs as distinct node types with per-type eviction policies | 1 | 0 | — |
| <a id="skill-cddb6d698985"></a>[neural-memory-design](../../memory-context/neural-memory-design/SKILL.md) | Compare external retrieval memory and neural memory architectures, plan bounded experiments, and evaluate memory quality without overstating capabilities. | 1 | 0 | — |
| <a id="skill-f8facdfe0940"></a>[nn-memory-sharing](../../memory-context/nn-memory-sharing/SKILL.md) | Design permissioned shared retrieval memory for multiple agents without claiming to share neural weights or hidden model state. | 3 | 0 | — |
| <a id="skill-59dc00cc6ef3"></a>[offline-ai-toolkit](../../memory-context/offline-ai-toolkit/SKILL.md) | Build offline-capable AI systems with local models, embedded knowledge bases, and no internet dependency. Use when: building AI tools for offline use, creating self-contained knowledge systems, deploying AI in air-gapped environments. | 2 | 0 | — |
| <a id="skill-3f34a5f1c93e"></a>[online-skill-learning-guide](../../memory-context/online-skill-learning-guide/SKILL.md) | Guide isolated experiments in state-grounded dynamic skill retrieval and online workflow learning using the upstream SGDR research project. | 3 | 0 | — |
| <a id="skill-3cbadf53d5a7"></a>[project-learner](../../memory-context/project-learner/SKILL.md) | 结构化交互式学习助手，当用户希望学习项目相关知识、特定代码文件或底层技术时使用此技能，它会将学习过程记录为持久化的 Markdown 日志 | 1 | 0 | — |
| <a id="skill-b2d582d61f1f"></a>[session-management](../../memory-context/session-management/SKILL.md) | Context preservation, tiered summarization, resumability | 1 | 0 | — |
| <a id="skill-682ad9f9a721"></a>[supermemory](../../memory-context/supermemory/SKILL.md) | Add persistent memory to AI agents using Supermemory API -- the #1 ranked AI memory engine. Use when: building AI assistants that remember users, adding long-term memory to chatbots, creating personalized AI products, storing conversation context across sessions. | 2 | 0 | — |

A blank warning is not a safety certification. Use `--skill NAME --detail`, `--files`, `--outline`, or `--links` for complete details without loading the entire library.

