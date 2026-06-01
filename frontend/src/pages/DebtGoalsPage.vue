<template>
  <div class="grid gap-6 xl:grid-cols-[.8fr_1.2fr]">
    <AppCard>
      <template #header><h2 class="font-semibold">Debt payoff calculator</h2></template>
      <form class="space-y-4" @submit.prevent="calculate">
        <label v-for="field in fields" :key="field.key" class="block text-sm font-medium">
          {{ field.label }}
          <input v-model.number="form[field.key]" type="number" step="0.01" class="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-900" />
        </label>
        <AppButton class="w-full">Calculate payoff</AppButton>
      </form>
    </AppCard>
    <div class="space-y-6">
      <div class="grid gap-4 md:grid-cols-3">
        <AppCard v-for="scenario in result?.scenarios ?? []" :key="scenario.monthly_payment">
          <p class="text-sm text-slate-500">{{ money(scenario.monthly_payment) }}/month</p>
          <p class="mt-2 text-2xl font-bold">{{ scenario.months ?? "N/A" }} mo</p>
          <p class="text-xs text-slate-500">Interest {{ money(scenario.total_interest) }}</p>
        </AppCard>
      </div>
      <AppCard>
        <template #header><h2 class="font-semibold">Scenario comparison</h2></template>
        <DebtPayoffChart :scenarios="result?.scenarios ?? []" />
      </AppCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { financeApi } from "../services/api";
import AppButton from "../components/ui/AppButton.vue";
import AppCard from "../components/ui/AppCard.vue";
import DebtPayoffChart from "../components/charts/DebtPayoffChart.vue";

const form = reactive<Record<string, number>>({ loan_balance: 85000, interest_rate: 6.4, monthly_payment: 1700, extra_payment: 0 });
const result = ref<any>(null);
const fields = [
  { key: "loan_balance", label: "Loan balance" },
  { key: "interest_rate", label: "Interest rate" },
  { key: "monthly_payment", label: "Monthly payment" },
  { key: "extra_payment", label: "Extra payment" },
];
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
async function calculate() {
  result.value = await financeApi.debtPayoff(form as any);
}
calculate();
</script>
