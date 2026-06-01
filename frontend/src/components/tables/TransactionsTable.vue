<template>
  <div class="space-y-4">
    <div v-if="!compact" class="grid gap-3 lg:grid-cols-[1.4fr_.9fr_.8fr_.7fr]">
      <AppInput v-model="search" :icon="Search" placeholder="Search merchant or transaction" />
      <AppSelect v-model="category">
        <option value="">All categories</option>
        <option v-for="item in categories" :key="item" :value="item">{{ humanize(item) }}</option>
      </AppSelect>
      <AppSelect v-model="type">
        <option value="">All types</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </AppSelect>
      <AppSelect v-model="pageSize">
        <option value="8">8 / page</option>
        <option value="12">12 / page</option>
        <option value="20">20 / page</option>
      </AppSelect>
    </div>

    <div class="overflow-x-auto rounded-lg border border-slate-100 dark:border-slate-800">
      <table class="min-w-full divide-y divide-slate-100 dark:divide-slate-800">
        <thead class="bg-slate-50 dark:bg-slate-900/70">
          <tr class="text-left text-xs uppercase tracking-wide text-slate-500">
            <th v-for="column in columns" :key="column.key" class="table-cell">
              <button
                class="inline-flex items-center gap-1 font-bold hover:text-slate-900 dark:hover:text-slate-100"
                :class="column.align === 'right' && 'ml-auto'"
                @click="setSort(column.key)"
              >
                {{ column.label }}
                <ArrowUpDown class="h-3.5 w-3.5" />
              </button>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 bg-white dark:divide-slate-800 dark:bg-slate-900">
          <tr v-for="tx in pageRows" :key="tx.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/60">
            <td class="table-cell text-slate-500">{{ tx.date }}</td>
            <td class="table-cell">
              <p class="font-semibold text-slate-950 dark:text-slate-100">{{ tx.merchant_name || tx.name }}</p>
              <p class="text-xs text-slate-500">{{ tx.name }}</p>
            </td>
            <td class="table-cell">
              <span class="inline-flex rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">{{ humanize(tx.category_primary) }}</span>
            </td>
            <td class="table-cell text-right font-bold" :class="tx.amount < 0 ? 'text-emerald-600' : 'text-slate-900 dark:text-slate-100'">
              {{ tx.amount < 0 ? "+" : "-" }}{{ money(Math.abs(tx.amount)) }}
            </td>
            <td class="table-cell">
              <AppBadge :tone="tx.amount < 0 ? 'success' : 'danger'">{{ tx.amount < 0 ? "Income" : "Expense" }}</AppBadge>
            </td>
          </tr>
          <tr v-if="pageRows.length === 0">
            <td class="px-4 py-10 text-center text-sm text-slate-500" colspan="5">No transactions match the current filters.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!compact" class="flex flex-col justify-between gap-3 text-sm text-slate-500 sm:flex-row sm:items-center">
      <span>Showing {{ pageStart + 1 }}-{{ Math.min(pageStart + Number(pageSize), sortedRows.length) }} of {{ sortedRows.length }}</span>
      <div class="flex items-center gap-2">
        <AppButton variant="secondary" :disabled="page === 1" @click="page--">Previous</AppButton>
        <span class="rounded-lg border border-slate-200 bg-white px-3 py-2 font-semibold text-slate-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100">{{ page }} / {{ totalPages }}</span>
        <AppButton variant="secondary" :disabled="page === totalPages" @click="page++">Next</AppButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ArrowUpDown, Search } from "lucide-vue-next";
import type { Transaction } from "../../services/api";
import AppBadge from "../ui/AppBadge.vue";
import AppButton from "../ui/AppButton.vue";
import AppInput from "../ui/AppInput.vue";
import AppSelect from "../ui/AppSelect.vue";

const props = withDefaults(defineProps<{ rows: Transaction[]; compact?: boolean }>(), { compact: false });
type SortKey = "date" | "merchant" | "category" | "amount" | "type";
const columns: { key: SortKey; label: string; align?: "right" }[] = [
  { key: "date", label: "Date" },
  { key: "merchant", label: "Merchant" },
  { key: "category", label: "Category" },
  { key: "amount", label: "Amount", align: "right" },
  { key: "type", label: "Type" },
];
const search = ref("");
const category = ref("");
const type = ref("");
const pageSize = ref(props.compact ? "6" : "8");
const page = ref(1);
const sortKey = ref<SortKey>("date");
const sortDirection = ref<"asc" | "desc">("desc");

const categories = computed(() => Array.from(new Set(props.rows.map((tx) => tx.category_primary))).sort());
const filteredRows = computed(() =>
  props.rows
    .filter((tx) => `${tx.name} ${tx.merchant_name}`.toLowerCase().includes(search.value.toLowerCase()))
    .filter((tx) => !category.value || tx.category_primary === category.value)
    .filter((tx) => !type.value || (type.value === "income" ? tx.amount < 0 : tx.amount > 0)),
);
const sortedRows = computed(() => {
  const direction = sortDirection.value === "asc" ? 1 : -1;
  return [...filteredRows.value].sort((a, b) => {
    const aValue = sortValue(a, sortKey.value);
    const bValue = sortValue(b, sortKey.value);
    if (aValue > bValue) return direction;
    if (aValue < bValue) return -direction;
    return 0;
  });
});
const totalPages = computed(() => Math.max(1, Math.ceil(sortedRows.value.length / Number(pageSize.value))));
const pageStart = computed(() => (page.value - 1) * Number(pageSize.value));
const pageRows = computed(() => sortedRows.value.slice(pageStart.value, pageStart.value + Number(pageSize.value)));

function setSort(key: SortKey) {
  if (sortKey.value === key) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortKey.value = key;
    sortDirection.value = key === "amount" ? "desc" : "asc";
  }
}

function sortValue(tx: Transaction, key: SortKey): string | number {
  if (key === "merchant") return tx.merchant_name || tx.name;
  if (key === "category") return tx.category_primary;
  if (key === "type") return tx.amount < 0 ? "income" : "expense";
  return tx[key];
}

watch([search, category, type, pageSize], () => {
  page.value = 1;
});
watch(totalPages, (value) => {
  if (page.value > value) page.value = value;
});

const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
const humanize = (value: string) => value.replace(/_/g, " ").toLowerCase().replace(/\b\w/g, (char: string) => char.toUpperCase());
</script>
