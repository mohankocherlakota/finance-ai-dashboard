<template>
  <VChart class="h-80 w-full" :option="option" autoresize />
</template>

<script setup lang="ts">
import { computed } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import { GridComponent, LegendComponent, TooltipComponent } from "echarts/components";

use([CanvasRenderer, BarChart, LineChart, GridComponent, LegendComponent, TooltipComponent]);
const props = defineProps<{ rows: any[] }>();
const money = (value: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
const option = computed(() => ({
  textStyle: { color: "#64748b", fontFamily: "Inter, system-ui, sans-serif" },
  tooltip: {
    trigger: "axis",
    valueFormatter: (value: number) => money(value),
    backgroundColor: "rgba(15, 23, 42, 0.92)",
    borderWidth: 0,
    textStyle: { color: "#fff" },
  },
  legend: { top: 0, itemWidth: 12, itemHeight: 8 },
  grid: { left: 58, right: 18, top: 46, bottom: 34 },
  xAxis: { type: "category", data: props.rows.map((r) => r.month), axisTick: { show: false } },
  yAxis: { type: "value", axisLabel: { formatter: (value: number) => money(value) }, splitLine: { lineStyle: { color: "#e2e8f0" } } },
  series: [
    { name: "Income", type: "bar", data: props.rows.map((r) => r.income), itemStyle: { color: "#059669", borderRadius: [6, 6, 0, 0] }, barMaxWidth: 32 },
    { name: "Expenses", type: "bar", data: props.rows.map((r) => r.expenses), itemStyle: { color: "#e11d48", borderRadius: [6, 6, 0, 0] }, barMaxWidth: 32 },
    { name: "Net", type: "line", data: props.rows.map((r) => r.net), smooth: true, symbolSize: 7, lineStyle: { width: 3 }, itemStyle: { color: "#2563eb" } },
  ],
}));
</script>
