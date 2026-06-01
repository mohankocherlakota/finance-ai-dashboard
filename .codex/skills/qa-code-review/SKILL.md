---
name: qa-code-review
description: Review this finance-ai-dashboard repository for production bugs, security risks, missing tests, UI regressions, data-handling issues, and deployment readiness. Use when the user asks for code review, QA review, security review, PR review, release readiness, slash-command-style review, or wants a QA-agent/code-review skill for the Vue 3 frontend, FastAPI backend, Plaid sync, OpenAI insights, SQLite data layer, or GitHub portfolio repo.
---

# QA Code Review

## Review Posture

- Lead with findings, ordered by severity.
- Focus on defects that can break production behavior, leak secrets, corrupt financial data, mislead users, or make the app hard to verify.
- Cite exact files and lines when possible.
- Do not rewrite code during a review unless the user explicitly asks for fixes.
- Never print `.env` values, Plaid access tokens, OpenAI keys, or raw real transaction data.

## Review Workflow

1. Read the project workflow skill first if available:

```text
.codex/skills/finance-ai-dashboard/references/project-workflow.md
```

2. Inspect the current diff or target files:

```bash
git status --short
git diff --stat
git diff
```

3. Check high-risk areas:

- Backend: Plaid sync, OpenAI insights, analytics math, DB writes, exception handling, CORS/config.
- Frontend: API centralization, transaction rendering, charts, dashboard metrics, dark/mobile UI, loading/error/toast states.
- Security: `.env`, DB files, token logging, frontend secret exposure, OpenAI raw-data leakage.
- Tests: backend pytest coverage and frontend build coverage.

4. Run verification only when needed for the review:

```bash
cd backend && venv/bin/pytest
cd frontend && npm run build
```

5. Write the review in this order:

- Findings
- Open questions or assumptions
- Test/build notes
- Short change summary only if useful

## Slash-Style Usage

Codex skills are invoked as `$qa-code-review` in this environment. Treat prompts like `/review`, `/qa`, or “run qa-agent” as requests to use this skill when this repo is the target.

## Reference

Read `references/review-checklist.md` for the project-specific checklist.
