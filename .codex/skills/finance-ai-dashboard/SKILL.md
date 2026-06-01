---
name: finance-ai-dashboard
description: Work on the local finance-ai-dashboard project, a Vue 3/Vite/TypeScript frontend and FastAPI/SQLAlchemy backend with Plaid transaction sync, OpenAI financial insights, SQLite local data, and strict secret-handling requirements. Use when modifying this repo, syncing Plaid data, fixing dashboard UI, debugging AI insights, running tests/builds, preparing GitHub pushes, or writing portfolio/demo updates for the app.
---

# Finance AI Dashboard

## Core Rules

- Treat `backend/.env`, Plaid access tokens, OpenAI keys, and `backend/finance_ai.db` as local-only secrets/data. Never print token values, commit them, or expose them to frontend code.
- Keep all frontend API calls centralized in `frontend/src/services/api.ts`.
- Send only summarized financial aggregates to OpenAI. Do not send raw transaction dumps.
- Prefer small, targeted changes. Do not rewrite the backend unless a route or service must change.
- Preserve the polished enterprise SaaS UI direction: collapsible sidebar, dense cards, clean charts, responsive layout, dark mode, toasts, and skeleton loaders.

## Workflow

1. Read the relevant files before changing code.
2. If touching Plaid or OpenAI behavior, inspect only key presence/counts, not secret values.
3. After backend changes, run:

```bash
cd backend
venv/bin/pytest
```

4. After frontend changes, run:

```bash
cd frontend
npm run build
```

5. For rendered UI changes, run the backend and frontend locally, then capture desktop and mobile screenshots with headless Chrome or the Browser plugin if available.
6. Before commits or pushes, verify ignored files remain untracked:

```bash
git status --ignored --short
```

## Project Reference

Read `references/project-workflow.md` when you need concrete paths, commands, endpoint details, Plaid/OpenAI notes, or GitHub push guidance.
