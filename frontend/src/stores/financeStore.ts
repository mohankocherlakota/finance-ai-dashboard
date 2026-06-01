import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { financeApi, type Summary, type Transaction } from "../services/api";
import { useToastStore } from "./toastStore";

export const useFinanceStore = defineStore("finance", () => {
  const transactions = ref<Transaction[]>([]);
  const summary = ref<Summary | null>(null);
  const monthly = ref<any[]>([]);
  const categories = ref<any[]>([]);
  const merchants = ref<any[]>([]);
  const recurring = ref<any[]>([]);
  const loading = ref(false);
  const error = ref("");
  const mockSeedAttempted = ref(false);

  const recentTransactions = computed(() => transactions.value.slice(0, 8));

  async function loadAll() {
    loading.value = true;
    error.value = "";
    try {
      let [tx, sum, mon, cat, mer, rec] = await Promise.all([
        financeApi.transactions(),
        financeApi.summary(),
        financeApi.monthly(),
        financeApi.categories(),
        financeApi.merchants(),
        financeApi.recurring(),
      ]);
      if (tx.length === 0 && !mockSeedAttempted.value) {
        mockSeedAttempted.value = true;
        await financeApi.seedMockData();
        [tx, sum, mon, cat, mer, rec] = await Promise.all([
          financeApi.transactions(),
          financeApi.summary(),
          financeApi.monthly(),
          financeApi.categories(),
          financeApi.merchants(),
          financeApi.recurring(),
        ]);
      }
      transactions.value = tx;
      summary.value = sum;
      monthly.value = mon;
      categories.value = cat;
      merchants.value = mer;
      recurring.value = rec;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unable to load finance data";
      useToastStore().error("Unable to load finance data", error.value);
    } finally {
      loading.value = false;
    }
  }

  async function seed() {
    await financeApi.seedMockData();
    useToastStore().success("Mock data seeded", "Dashboard analytics now use the demo transaction set.");
    await loadAll();
  }

  async function reset() {
    await financeApi.resetData();
    mockSeedAttempted.value = false;
    useToastStore().success("Data reset", "Local accounts and transactions were cleared.");
    await loadAll();
  }

  return { transactions, summary, monthly, categories, merchants, recurring, loading, error, recentTransactions, loadAll, seed, reset };
});
