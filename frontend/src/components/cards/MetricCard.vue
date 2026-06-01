<template>
  <AppCard>
    <div class="flex items-start justify-between">
      <div>
        <p class="text-sm font-medium text-slate-500">{{ label }}</p>
        <p class="mt-2 text-2xl font-bold">{{ value }}</p>
        <p class="mt-2 text-xs" :class="trend >= 0 ? 'text-emerald-600' : 'text-rose-600'">{{ trendLabel }}</p>
      </div>
      <div :class="['rounded-lg p-2', toneClass]">
        <component :is="icon" class="h-5 w-5" />
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { computed } from "vue";
import AppCard from "../ui/AppCard.vue";

const props = defineProps<{ label: string; value: string; trend: number; icon: any; tone?: "blue" | "green" | "rose" }>();
const trendLabel = computed(() => `${props.trend >= 0 ? "+" : ""}${props.trend}% vs prior month`);
const toneClass = computed(() => ({
  blue: "bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-300",
  green: "bg-emerald-50 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-300",
  rose: "bg-rose-50 text-rose-600 dark:bg-rose-950 dark:text-rose-300",
}[props.tone ?? "blue"]));
</script>
