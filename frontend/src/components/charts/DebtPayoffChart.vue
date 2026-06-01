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
const props = defineProps<{ scenarios: any[] }>();
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
const option = computed(() => ({
  tooltip: {
    trigger: "axis",
    formatter: (params: any[]) => {
      const item = params[0];
      return `${item.axisValue}<br/>${item.value} months`;
    },
    backgroundColor: "rgba(15, 23, 42, 0.92)",
    borderWidth: 0,
    textStyle: { color: "#fff" },
  },
  grid: { left: 58, right: 16, top: 12, bottom: 34 },
  xAxis: { type: "category", data: props.scenarios.map((s) => `$${s.monthly_payment}`) },
  yAxis: { type: "value", name: "Months" },
  series: [{ type: "bar", data: props.scenarios.map((s) => s.months ?? 0), itemStyle: { color: "#2563eb", borderRadius: 6 } }],
}));
</script>
