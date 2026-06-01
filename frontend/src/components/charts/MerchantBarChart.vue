<template>
  <VChart class="h-72 w-full" :option="option" autoresize />
</template>

<script setup lang="ts">
import { computed } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent } from "echarts/components";

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent]);
const props = defineProps<{ rows: any[] }>();
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
const option = computed(() => ({
  tooltip: {
    trigger: "axis",
    valueFormatter: (value: number) => money(value),
    backgroundColor: "rgba(15, 23, 42, 0.92)",
    borderWidth: 0,
    textStyle: { color: "#fff" },
  },
  grid: { left: 150, right: 20, top: 12, bottom: 28 },
  xAxis: { type: "value", axisLabel: { formatter: (value: number) => money(value) }, splitLine: { lineStyle: { color: "#e2e8f0" } } },
  yAxis: { type: "category", data: props.rows.map((r) => r.merchant).reverse(), axisLabel: { formatter: (value: string) => (value.length > 20 ? `${value.slice(0, 18)}...` : value) } },
  series: [{ type: "bar", data: props.rows.map((r) => r.amount).reverse(), itemStyle: { color: "#2563eb", borderRadius: 6 } }],
}));
</script>
