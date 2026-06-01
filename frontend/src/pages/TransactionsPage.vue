<template>
  <div class="space-y-5">
    <AppCard>
      <div class="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h2 class="text-xl font-bold">Transaction workbench</h2>
          <p class="mt-1 text-sm text-slate-500">Search, sort, filter, and page through synced Plaid transactions.</p>
        </div>
        <AppButton variant="secondary" @click="store.loadAll">
          <RefreshCcw class="h-4 w-4" /> Refresh
        </AppButton>
      </div>
    </AppCard>
    <DashboardSkeleton v-if="store.loading" />
    <template v-else-if="store.transactions.length">
      <MonthlyExpenseTracker :rows="store.monthly" />
      <AppCard>
        <template #header><h2 class="font-semibold">Transactions</h2></template>
        <TransactionsTable :rows="store.transactions" />
      </AppCard>
    </template>
    <EmptyState v-else title="No transactions found" message="Sync Plaid transactions to populate this table." />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { RefreshCcw } from "lucide-vue-next";
import { useFinanceStore } from "../stores/financeStore";
import AppCard from "../components/ui/AppCard.vue";
import AppButton from "../components/ui/AppButton.vue";
import DashboardSkeleton from "../components/ui/DashboardSkeleton.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import MonthlyExpenseTracker from "../components/cards/MonthlyExpenseTracker.vue";
import TransactionsTable from "../components/tables/TransactionsTable.vue";

const store = useFinanceStore();
onMounted(() => store.loadAll());
</script>
