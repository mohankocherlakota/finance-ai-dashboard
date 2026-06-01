<template>
  <div class="space-y-6">
    <AppCard>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 class="font-semibold">AI financial insights</h2>
          <p class="mt-1 text-sm text-slate-500">Insights are generated from summarized monthly, category, merchant, recurring, income, expense, savings, and debt aggregates only.</p>
        </div>
        <AppButton :disabled="store.loading" @click="store.generate">Generate AI insights</AppButton>
      </div>
    </AppCard>
    <div v-if="store.error" class="rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{{ store.error }}</div>
    <LoadingState v-if="store.loading" />
    <div v-else-if="store.insights" class="grid gap-6 lg:grid-cols-3">
      <InsightList title="Observations" :items="store.insights.observations" />
      <InsightList title="Risks" :items="store.insights.risks" />
      <InsightList title="Recommended actions" :items="store.insights.recommended_actions" />
      <AppCard class="lg:col-span-3">
        <div class="grid gap-4 md:grid-cols-3">
          <div><p class="text-sm font-semibold">Budget adjustment</p><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">{{ store.insights.budget_adjustment }}</p></div>
          <div><p class="text-sm font-semibold">Debt payoff suggestion</p><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">{{ store.insights.debt_payoff_suggestion }}</p></div>
          <div><p class="text-sm font-semibold">Summary</p><p class="mt-2 text-sm text-slate-600 dark:text-slate-300">{{ store.insights.motivational_summary }}</p></div>
        </div>
      </AppCard>
      <div class="lg:col-span-3 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800 dark:border-amber-900 dark:bg-amber-950 dark:text-amber-200">
        {{ store.insights.disclaimer }}
      </div>
    </div>
    <EmptyState v-else title="No insights yet" message="Generate insights after seeding mock data or syncing Plaid transactions." />
  </div>
</template>

<script setup lang="ts">
import { defineComponent, h } from "vue";
import { useInsightsStore } from "../stores/insightsStore";
import AppButton from "../components/ui/AppButton.vue";
import AppCard from "../components/ui/AppCard.vue";
import EmptyState from "../components/ui/EmptyState.vue";
import LoadingState from "../components/ui/LoadingState.vue";

const store = useInsightsStore();
const InsightList = defineComponent({
  props: { title: { type: String, required: true }, items: { type: Array<string>, required: true } },
  setup(props) {
    return () =>
      h(AppCard, null, {
        header: () => h("h2", { class: "font-semibold" }, props.title),
        default: () => h("ul", { class: "space-y-3 text-sm text-slate-600 dark:text-slate-300" }, props.items.map((item) => h("li", { class: "rounded-lg bg-slate-50 p-3 dark:bg-slate-800" }, item))),
      });
  },
});
</script>
