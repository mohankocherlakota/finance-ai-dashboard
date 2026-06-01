<template>
  <div class="grid min-h-72 gap-4 lg:grid-cols-[1.15fr_.85fr]">
    <VChart class="h-72 w-full" :option="option" autoresize />
    <div class="flex flex-col justify-center gap-2">
      <div v-for="(row, index) in topRows" :key="row.category" class="flex items-center justify-between gap-3 rounded-lg bg-slate-50 px-3 py-2 text-xs dark:bg-slate-800/70">
        <div class="flex min-w-0 items-center gap-2">
          <span class="h-2.5 w-2.5 shrink-0 rounded-full" :style="{ backgroundColor: colors[index % colors.length] }" />
          <span class="truncate font-semibold text-slate-700 dark:text-slate-200">{{ humanize(row.category) }}</span>
        </div>
        <span class="shrink-0 font-bold text-slate-900 dark:text-white">{{ money(row.amount) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { LegendComponent, TooltipComponent } from "echarts/components";

use([CanvasRenderer, PieChart, LegendComponent, TooltipComponent]);
const props = defineProps<{ rows: any[] }>();
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
const colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4"];
const topRows = computed(() => props.rows.slice(0, 6));
const option = computed(() => ({
  tooltip: {
    trigger: "item",
    formatter: ({ name, value, percent }: { name: string; value: number; percent: number }) => `${name}<br/>${money(value)} (${percent}%)`,
    backgroundColor: "rgba(15, 23, 42, 0.92)",
    borderWidth: 0,
    textStyle: { color: "#fff" },
  },
  color: colors,
  series: [
    {
      type: "pie",
      radius: ["52%", "74%"],
      center: ["50%", "50%"],
      avoidLabelOverlap: true,
      label: { show: false },
      emphasis: { label: { show: true, formatter: ({ name }: { name: string }) => humanize(truncate(name)), fontSize: 12, fontWeight: 700 } },
      data: props.rows.map((r) => ({ name: r.category, value: r.amount })),
    },
  ],
}));
const truncate = (value: string) => (value.length > 18 ? `${value.slice(0, 16)}...` : value);
const humanize = (value: string) => value.replace(/_/g, " ").toLowerCase().replace(/\b\w/g, (char: string) => char.toUpperCase());
</script>
