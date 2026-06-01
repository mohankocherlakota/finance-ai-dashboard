import { createRouter, createWebHistory } from "vue-router";
import DashboardLayout from "../layouts/DashboardLayout.vue";
import DashboardPage from "../pages/DashboardPage.vue";
import TransactionsPage from "../pages/TransactionsPage.vue";
import BudgetPage from "../pages/BudgetPage.vue";
import DebtGoalsPage from "../pages/DebtGoalsPage.vue";
import InsightsPage from "../pages/InsightsPage.vue";
import SettingsPage from "../pages/SettingsPage.vue";
import PlaidConnectPage from "../pages/PlaidConnectPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: DashboardLayout,
      children: [
        { path: "", name: "Dashboard", component: DashboardPage },
        { path: "transactions", name: "Transactions", component: TransactionsPage },
        { path: "budget", name: "Budget", component: BudgetPage },
        { path: "debt-goals", name: "Debt Goals", component: DebtGoalsPage },
        { path: "insights", name: "Insights", component: InsightsPage },
        { path: "plaid", name: "Plaid Connect", component: PlaidConnectPage },
        { path: "settings", name: "Settings", component: SettingsPage },
      ],
    },
  ],
});

export default router;
