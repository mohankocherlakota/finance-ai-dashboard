<template>
  <div class="grid gap-6 xl:grid-cols-[1.4fr_.8fr]">
    <AppCard>
      <template #header><h2 class="font-semibold">Category budgets</h2></template>
      <div class="space-y-5">
        <div v-for="row in budgetRows" :key="row.category">
          <div class="mb-2 flex items-center justify-between text-sm">
            <span class="font-medium">{{ row.category }}</span>
            <span>{{ money(row.amount) }} / {{ money(row.budget) }}</span>
          </div>
          <div class="h-2 rounded-full bg-slate-100 dark:bg-slate-800">
            <div class="h-2 rounded-full" :class="row.amount > row.budget ? 'bg-rose-500' : 'bg-blue-600'" :style="{ width: `${Math.min(100, (row.amount / row.budget) * 100)}%` }" />
          </div>
          <p v-if="row.amount > row.budget" class="mt-1 text-xs text-rose-600">Overspending alert</p>
        </div>
      </div>
    </AppCard>
    <AppCard>
      <template #header><h2 class="font-semibold">Budget summary</h2></template>
      <p class="text-3xl font-bold">{{ money(totalBudget) }}</p>
      <p class="mt-2 text-sm text-slate-500">Manual monthly budget</p>
      <div class="mt-6 rounded-lg bg-blue-50 p-4 text-sm text-blue-800 dark:bg-blue-950 dark:text-blue-200">
        Suggested adjustment: reduce any category above 95% utilization by 10% next month and redirect surplus to debt payoff.
      </div>
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useFinanceStore } from "../stores/financeStore";
import AppCard from "../components/ui/AppCard.vue";

const store = useFinanceStore();
const budgets: Record<string, number> = { RENT_AND_UTILITIES: 2600, FOOD_AND_DRINK: 850, LOAN_PAYMENTS: 2500, TRAVEL: 600, ENTERTAINMENT: 150 };
const budgetRows = computed(() => store.categories.map((row) => ({ ...row, budget: budgets[row.category] ?? 500 })));
const totalBudget = computed(() => budgetRows.value.reduce((sum, row) => sum + row.budget, 0));
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
onMounted(() => store.loadAll());
</script>
