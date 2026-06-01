<template>
  <MetricCard label="Net cash flow" :value="value" :trend="trend" :icon="ArrowUpRight" tone="blue" />
</template>

<script setup lang="ts">
import { ArrowUpRight } from "lucide-vue-next";
import MetricCard from "./MetricCard.vue";
defineProps<{ value: string; trend: number }>();
</script>
