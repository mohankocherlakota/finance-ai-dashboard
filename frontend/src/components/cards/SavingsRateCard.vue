<template>
  <MetricCard label="Savings rate" :value="value" :trend="trend" :icon="PiggyBank" tone="green" />
</template>

<script setup lang="ts">
import { PiggyBank } from "lucide-vue-next";
import MetricCard from "./MetricCard.vue";
defineProps<{ value: string; trend: number }>();
</script>
