import axios from "axios";

export interface Transaction {
  id: number;
  plaid_transaction_id: string;
  date: string;
  name: string;
  merchant_name: string;
  amount: number;
  category_primary: string;
  category_detailed: string;
  account_id: number;
  pending: boolean;
}

export interface Summary {
  income: number;
  expenses: number;
  net_cash_flow: number;
  savings_rate: number;
  mom_change: Record<string, number>;
  debt_payments: number;
}

export interface Insights {
  observations: string[];
  risks: string[];
  recommended_actions: string[];
  budget_adjustment: string;
  debt_payoff_suggestion: string;
  motivational_summary: string;
  disclaimer: string;
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  timeout: 15000,
});

export const financeApi = {
  health: () => api.get<{ status: string }>("/health").then((r) => r.data),
  transactions: () => api.get<Transaction[]>("/api/transactions").then((r) => r.data),
  seedMockData: () => api.post("/api/transactions/seed").then((r) => r.data),
  resetData: () => api.post("/api/transactions/reset").then((r) => r.data),
  summary: () => api.get<Summary>("/api/analytics/summary").then((r) => r.data),
  monthly: () => api.get("/api/analytics/monthly").then((r) => r.data),
  categories: () => api.get("/api/analytics/categories").then((r) => r.data),
  merchants: () => api.get("/api/analytics/merchants").then((r) => r.data),
  recurring: () => api.get("/api/analytics/recurring").then((r) => r.data),
  generateInsights: () => api.post<Insights>("/api/insights/generate").then((r) => r.data),
  createLinkToken: () => api.post<{ link_token: string }>("/api/plaid/create_link_token").then((r) => r.data),
  exchangePublicToken: (public_token: string) => api.post("/api/plaid/exchange_public_token", { public_token }).then((r) => r.data),
  syncTransactions: () => api.post("/api/plaid/sync_transactions").then((r) => r.data),
  debtPayoff: (payload: { loan_balance: number; interest_rate: number; monthly_payment: number; extra_payment: number }) =>
    api.post("/api/goals/debt-payoff", payload).then((r) => r.data),
};
