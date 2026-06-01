# finance-ai-dashboard Review Checklist

## Security

- Verify `backend/.env`, `backend/finance_ai.db`, venv, node_modules, and build outputs are ignored.
- Search frontend source for secret names or token usage:

```bash
rg "PLAID_SECRET|PLAID_ACCESS_TOKEN|OPENAI_API_KEY|plaid_secret|access_token" frontend/src
```

- Confirm frontend HTTP calls stay centralized:

```bash
rg "axios|fetch\(" frontend/src
```

- Confirm OpenAI requests use `summarize_for_ai` aggregates, not raw transactions.
- Confirm Plaid token values are never printed in commands, logs, screenshots, or docs.

## Backend

- Check `backend/app/config.py` for safe env loading and no secret defaults.
- Check `backend/app/plaid_client.py` for correct Plaid environment host selection and initial sync cursor handling.
- Check `backend/app/routers/plaid.py` for multi-token sync behavior, duplicate transaction handling, and token storage TODOs.
- Check `backend/app/services/analytics_service.py` for income/expense sign assumptions, recurring detection, debt detection, and month-over-month math.
- Check `backend/app/services/ai_insights_service.py` for schema normalization, fallback behavior, and disclaimer enforcement.
- Run `backend/venv/bin/pytest` after backend changes.

## Frontend

- Check `frontend/src/services/api.ts` for all API calls and no secret-bearing env vars.
- Check `DashboardPage.vue` against real synced data, not mock-only labels.
- Check `TransactionsPage.vue`, `MonthlyExpenseTracker.vue`, and `TransactionsTable.vue` for sorting/filtering/pagination edge cases.
- Check ECharts components for readable labels, currency formatting, responsive behavior, and no clipped text.
- Check layout components for collapsible sidebar, mobile drawer, dark mode, skeleton loaders, and toasts.
- Run `npm run build` after frontend changes.

## Render QA

For visible UI changes, verify:

- Desktop dashboard at `1440x1000`.
- Mobile dashboard at approximately `390x844`.
- Transactions page with real synced data.
- Insights page after clicking Generate AI insights.
- No framework error overlay, blank screen, clipped primary content, or misleading mock/sandbox copy.

## Review Output Template

```text
Findings
- [P1/P2/P3] Title — file:line
  Why it matters, reproduction or evidence, and suggested fix.

Open Questions
- ...

Tests
- Passed/failed/not run, with reason.
```
