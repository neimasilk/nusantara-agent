---
name: user-api-providers
description: User has DeepSeek, Grok (xAI), and Kimi (Moonshot) API access with <$5 remaining credit each, stored in .env.txt.
metadata:
  type: user
---

Available paid LLM providers (as of 2026-05-18):

- **DeepSeek** — chat & coder models, OpenAI-compatible client at `https://api.deepseek.com`. Cheapest by far; supports context caching.
- **Grok / xAI** — Grok models via xAI API. Mid-priced. OpenAI-compatible client at `https://api.x.ai`. Env var name: `XAI_API_KEY` (NOT `GROK_API_KEY`).
- **Kimi / Moonshot** — Moonshot-v1 family. OpenAI-compatible client at `https://api.moonshot.cn` or `https://api.moonshot.ai`.

**Credit:** less than $5 remaining per provider (~$15 total ceiling).

**Storage:** API keys are in `.env.txt` (note: `.txt` extension, NOT plain `.env`). User chose this name; check the file's gitignore status before any commit.

**Access pattern:** all three are OpenAI-API-compatible. Use the same `openai` Python client with different `base_url` + key.

**No access to:** OpenAI GPT-4o, Anthropic Claude, Google Gemini. Don't propose these in plans unless the user explicitly asks.
