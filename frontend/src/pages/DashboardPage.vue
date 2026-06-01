<template>
  <div class="space-y-6">
    <div class="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
      <div>
        <p class="text-sm font-medium text-slate-500">Portfolio-ready overview</p>
        <h2 class="mt-1 text-2xl font-bold tracking-tight">Financial command center</h2>
      </div>
      <div class="flex flex-wrap gap-2">
        <AppBadge tone="info">Synced Plaid data</AppBadge>
        <AppBadge tone="success">{{ store.transactions.length }} transactions</AppBadge>
      </div>
    </div>
    <div v-if="store.error" class="rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950 dark:text-rose-200">{{ store.error }}</div>
    <DashboardSkeleton v-if="store.loading" />
    <template v-else>
      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Income" :value="money(store.summary?.income ?? 0)" :trend="store.summary?.mom_change.income_change ?? 0" :icon="Wallet" tone="green" />
        <MetricCard label="Expenses" :value="money(store.summary?.expenses ?? 0)" :trend="store.summary?.mom_change.expense_change ?? 0" :icon="Receipt" tone="rose" />
        <CashFlowCard :value="money(store.summary?.net_cash_flow ?? 0)" :trend="store.summary?.mom_change.net_change ?? 0" />
        <SavingsRateCard :value="`${store.summary?.savings_rate ?? 0}%`" :trend="2.4" />
      </div>
      <div class="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <AppCard>
          <template #header>
            <div class="flex items-center justify-between">
              <div>
                <h2 class="font-semibold">Monthly cashflow</h2>
                <p class="mt-1 text-xs text-slate-500">Income, expenses, and net movement</p>
              </div>
            </div>
          </template>
          <MonthlyCashflowChart :rows="store.monthly" />
        </AppCard>
        <AppCard>
          <template #header><h2 class="font-semibold">Category mix</h2></template>
          <CategoryPieChart :rows="store.categories" />
        </AppCard>
      </div>
      <div class="grid gap-6 xl:grid-cols-[1fr_1.35fr]">
        <AppCard>
          <template #header><h2 class="font-semibold">Top merchants</h2></template>
          <MerchantBarChart :rows="store.merchants" />
        </AppCard>
        <AppCard>
          <template #header><h2 class="font-semibold">Recent transactions</h2></template>
          <TransactionsTable :rows="store.recentTransactions" compact />
        </AppCard>
      </div>
      <AppCard>
        <template #header><h2 class="font-semibold">AI summary preview</h2></template>
        <p class="text-sm text-slate-600 dark:text-slate-300">
          Current cash flow is {{ money(store.summary?.net_cash_flow ?? 0) }} with a {{ store.summary?.savings_rate ?? 0 }}% savings rate.
          Generate detailed AI insights from aggregated data on the Insights page.
        </p>
      </AppCard>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { Receipt, Wallet } from "lucide-vue-next";
import { useFinanceStore } from "../stores/financeStore";
import AppCard from "../components/ui/AppCard.vue";
import AppBadge from "../components/ui/AppBadge.vue";
import DashboardSkeleton from "../components/ui/DashboardSkeleton.vue";
import MetricCard from "../components/cards/MetricCard.vue";
import CashFlowCard from "../components/cards/CashFlowCard.vue";
import SavingsRateCard from "../components/cards/SavingsRateCard.vue";
import MonthlyCashflowChart from "../components/charts/MonthlyCashflowChart.vue";
import CategoryPieChart from "../components/charts/CategoryPieChart.vue";
import MerchantBarChart from "../components/charts/MerchantBarChart.vue";
import TransactionsTable from "../components/tables/TransactionsTable.vue";

const store = useFinanceStore();
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
onMounted(() => store.loadAll());
</script>
