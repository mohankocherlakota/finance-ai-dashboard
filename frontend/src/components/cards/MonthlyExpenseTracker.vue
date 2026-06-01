<template>
  <AppCard>
    <template #header>
      <div class="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <h2 class="font-semibold">Monthly expense tracker</h2>
          <p class="mt-1 text-xs text-slate-500">Real synced spending by month</p>
        </div>
        <AppBadge tone="info">{{ rows.length }} months</AppBadge>
      </div>
    </template>
    <div class="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
      <div class="rounded-lg bg-slate-50 p-4 dark:bg-slate-800/70">
        <p class="text-sm font-medium text-slate-500">Latest spending month</p>
        <p class="mt-2 text-3xl font-bold">{{ money(latestSpendingMonth?.expenses ?? 0) }}</p>
        <p class="mt-2 text-sm" :class="change <= 0 ? 'text-emerald-600' : 'text-rose-600'">
          {{ changeLabel }} vs prior month
        </p>
        <div class="mt-5 grid grid-cols-2 gap-3 text-sm">
          <div>
            <p class="text-slate-500">Average</p>
            <p class="font-bold">{{ money(averageExpenses) }}</p>
          </div>
          <div>
            <p class="text-slate-500">Peak month</p>
            <p class="font-bold">{{ peak?.month ?? "-" }}</p>
          </div>
        </div>
      </div>
      <div class="space-y-3">
        <div v-for="row in rowsDescending" :key="row.month" class="grid grid-cols-[5rem_1fr_6rem] items-center gap-3 text-sm">
          <span class="font-semibold text-slate-600 dark:text-slate-300">{{ row.month }}</span>
          <div class="h-2.5 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
            <div class="h-full rounded-full bg-rose-500" :style="{ width: `${barWidth(row.expenses)}%` }" />
          </div>
          <span class="text-right font-bold">{{ money(row.expenses) }}</span>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { computed } from "vue";
import AppBadge from "../ui/AppBadge.vue";
import AppCard from "../ui/AppCard.vue";

const props = defineProps<{ rows: { month: string; income: number; expenses: number; net: number }[] }>();
const rowsDescending = computed(() => [...props.rows].reverse());
const latestSpendingIndex = computed(() => {
  for (let index = props.rows.length - 1; index >= 0; index -= 1) {
    if (props.rows[index].expenses > 0) return index;
  }
  return props.rows.length - 1;
});
const latestSpendingMonth = computed(() => props.rows[latestSpendingIndex.value]);
const previous = computed(() => props.rows[latestSpendingIndex.value - 1]);
const peak = computed(() => [...props.rows].sort((a, b) => b.expenses - a.expenses)[0]);
const maxExpense = computed(() => Math.max(1, ...props.rows.map((row) => row.expenses)));
const averageExpenses = computed(() => {
  if (!props.rows.length) return 0;
  return props.rows.reduce((sum, row) => sum + row.expenses, 0) / props.rows.length;
});
const change = computed(() => {
  if (!latestSpendingMonth.value || !previous.value || previous.value.expenses === 0) return 0;
  return ((latestSpendingMonth.value.expenses - previous.value.expenses) / previous.value.expenses) * 100;
});
const changeLabel = computed(() => `${change.value >= 0 ? "+" : ""}${change.value.toFixed(1)}%`);
const barWidth = (value: number) => Math.max(4, Math.round((value / maxExpense.value) * 100));
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
</script>
