import { defineStore } from "pinia";
import { ref } from "vue";
import { financeApi, type Insights } from "../services/api";
import { useToastStore } from "./toastStore";

export const useInsightsStore = defineStore("insights", () => {
  const insights = ref<Insights | null>(null);
  const loading = ref(false);
  const error = ref("");

  async function generate() {
    loading.value = true;
    error.value = "";
    try {
      insights.value = await financeApi.generateInsights();
      useToastStore().success("Insights generated", "AI recommendations were refreshed from summarized data.");
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unable to generate insights";
      useToastStore().error("Unable to generate insights", error.value);
    } finally {
      loading.value = false;
    }
  }

  return { insights, loading, error, generate };
});
