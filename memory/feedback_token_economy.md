---
name: feedback-token-economy
description: User treats LLM token saving as a hard obligation, not a nice-to-have. Always optimize prompts and choose cheapest viable backend.
metadata:
  type: feedback
---

LLM token efficiency is a "kewajiban" (obligation) for this user, not a soft preference.

**Why:** User said directly: "penghematan token LLM juga merupakan 'kewajiban'". Combined with the project's [[project-budget-ceiling]] of <$5 per provider remaining, every wasted token is a real cost. Plus CLAUDE.md `data/processed/` API cost-control mode is the active default policy.

**How to apply:**

- Default to **offline / local Ollama** for any prototyping, sanity check, smoke test. Never burn paid API tokens on iteration.
- Indonesian-only prompts (shorter than bilingual). Compact phrasing.
- Force **structured output only** (JSON `{"label": "...", "alasan": "..."}`) — no chain-of-thought, no reasoning trace in the response unless explicitly needed for the experiment.
- Use **prompt caching** on every provider that supports it (DeepSeek context cache, Anthropic prompt cache, etc.). Cache the system prompt + rules once, vary only the case narrative.
- **Batch APIs** where available (DeepSeek/OpenAI batch ≈ 50% discount).
- **Stratified sampling first**: run 10-15 cases before scaling to full benchmark; verify the pipeline, then scale.
- Estimate token budget BEFORE running and report it to user; never run a paid sweep without showing the bill estimate first.
- Prefer 1-shot direct prompts over multi-turn / agentic / debate setups (Exp 07 already proved debate is more expensive AND worse on this task — see [[feedback-no-debate-orchestration]] if it exists).
