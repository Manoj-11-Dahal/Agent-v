---
name: neural-memory-design
description: "Compare external retrieval memory and neural memory architectures, plan bounded experiments, and evaluate memory quality without overstating capabilities."
---
# Neural memory design

1. Clarify whether the user needs external RAG memory, recurrent hidden state, model
   fine-tuning, episodic workflow retrieval, or a research architecture. These are distinct.
2. Record data ownership, task distribution, retention needs, model interface, compute
   budget, privacy constraints, and whether weight access is actually available.
3. Establish a simple baseline: local approved summaries plus deterministic lookup.
   Compare embedding retrieval only when a retrieval task justifies it.
4. For external memory, use `agent-memory` and `nn-memory-sharing`. For actual model
   training, select relevant installed AI-research skills and confirm dataset license,
   training hardware, framework compatibility, evaluation split, and checkpoint policy.
5. Never promise to alter the underlying Arena model's weights or hidden state. APIs may
   not expose training or persistent state. File persistence is not neural learning.
6. Evaluate task success, factual provenance, retention/retrieval errors, forgetting,
   contamination, latency, cost, and privacy leakage on held-out data.
7. Keep dataset and evaluation versions separate from model checkpoints; never train
   on test answers. Use synthetic or consented data and require approval for paid jobs.
8. Present the measured result and limitations. Promote a memory mechanism only after
   it improves the intended task without unacceptable privacy or reliability regressions.

Output: architecture comparison, baseline, experiment plan, evaluation criteria,
dependencies, approval requirements, and an honest statement of what is not implemented.
