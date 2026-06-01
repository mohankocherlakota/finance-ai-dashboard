# finance-ai-dashboard Project Workflow

## Repository

Local path:

```bash
/Users/mohankocherlakota/Documents/Codex/finance-ai-dashboard
```

GitHub:

```bash
https://github.com/mohankocherlakota/finance-ai-dashboard
```

## Stack

- Frontend: Vue 3, Vite, TypeScript, Tailwind CSS, Pinia, Vue Router, Axios, ECharts.
- Backend: FastAPI, SQLAlchemy, SQLite, Plaid Python SDK, OpenAI Python SDK, Pydantic, pytest.
- Local DB: `backend/finance_ai.db`, ignored by Git.
- Secrets: `backend/.env`, ignored by Git.

## Important Paths

- Backend app: `backend/app/`
- Backend config: `backend/app/config.py`
- Plaid client: `backend/app/plaid_client.py`
- Plaid routes: `backend/app/routers/plaid.py`
- AI insights service: `backend/app/services/ai_insights_service.py`
- Analytics service: `backend/app/services/analytics_service.py`
- Frontend API client: `frontend/src/services/api.ts`
- Main layout: `frontend/src/layouts/DashboardLayout.vue`
- Dashboard page: `frontend/src/pages/DashboardPage.vue`
- Transactions page: `frontend/src/pages/TransactionsPage.vue`
- Monthly expense tracker: `frontend/src/components/cards/MonthlyExpenseTracker.vue`
- Transactions table: `frontend/src/components/tables/TransactionsTable.vue`

## Local Run Commands

Backend:

```bash
cd /Users/mohankocherlakota/Documents/Codex/finance-ai-dashboard/backend
venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd /Users/mohankocherlakota/Documents/Codex/finance-ai-dashboard/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

URLs:

- Frontend: `http://127.0.0.1:5173/`
- Backend health: `http://127.0.0.1:8000/health`

## Verification Commands

Backend:

```bash
cd backend
venv/bin/pytest
```

Frontend:

```bash
cd frontend
npm run build
```

Secret/API scans:

```bash
rg "PLAID_SECRET|PLAID_ACCESS_TOKEN|OPENAI_API_KEY|plaid_secret|access_token" frontend/src
rg "axios|fetch\(" frontend/src
```

Expected API scan result: Axios only appears in `frontend/src/services/api.ts`.

## Plaid Sync Notes

The backend supports:

- `PLAID_ENV=sandbox|development|production`
- `PLAID_ACCESS_TOKEN`
- Multiple token keys such as `PLAID_ACCESS_TOKEN_CHASE`, `PLAID_ACCESS_TOKEN_DISCOVER`, etc.

Do not print token values. To inspect configuration, print only booleans/counts:

```bash
cd backend
venv/bin/python -c 'from app.config import get_settings; s=get_settings(); print({"PLAID_ENV": s.plaid_env, "TOKEN_COUNT": len(s.plaid_access_tokens), "PLAID_CLIENT_ID_SET": bool(s.plaid_client_id), "PLAID_SECRET_SET": bool(s.plaid_secret)})'
```

Sync endpoint:

```bash
curl -s -X POST http://127.0.0.1:8000/api/plaid/sync_transactions
```

If no server is running, start FastAPI first. Do not log token values.

## AI Insights Notes

Endpoint:

```bash
curl -s -X POST http://127.0.0.1:8000/api/insights/generate
```

The AI service must use summarized aggregates from `summarize_for_ai`, not raw transaction lists. It normalizes model output so `budget_adjustment`, `debt_payoff_suggestion`, and `motivational_summary` can be strings even if the model returns arrays.

## GitHub Push

Before pushing:

```bash
git status --short
git status --ignored --short
```

Ensure these remain ignored/untracked:

- `backend/.env`
- `backend/finance_ai.db`
- `backend/venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- `.DS_Store`

Push:

```bash
git push origin main
```
