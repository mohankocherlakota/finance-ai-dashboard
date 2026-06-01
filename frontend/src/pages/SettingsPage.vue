<template>
  <div class="grid gap-6 lg:grid-cols-2">
    <AppCard>
      <template #header><h2 class="font-semibold">System status</h2></template>
      <div class="space-y-4 text-sm">
        <div class="flex justify-between"><span>API health</span><AppBadge :tone="health === 'ok' ? 'success' : 'danger'">{{ health }}</AppBadge></div>
        <div class="flex justify-between"><span>Plaid connection</span><AppBadge tone="neutral">Sandbox-ready</AppBadge></div>
        <div class="flex justify-between"><span>Theme</span><AppBadge tone="info">Use topbar toggle</AppBadge></div>
      </div>
    </AppCard>
    <AppCard>
      <template #header><h2 class="font-semibold">Data controls</h2></template>
      <div class="flex flex-wrap gap-3">
        <AppButton @click="seed">Seed Mock Data</AppButton>
        <AppButton variant="danger" @click="reset">Data Reset</AppButton>
      </div>
      <p class="mt-4 text-sm text-slate-500">{{ message }}</p>
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { financeApi } from "../services/api";
import { useFinanceStore } from "../stores/financeStore";
import AppBadge from "../components/ui/AppBadge.vue";
import AppButton from "../components/ui/AppButton.vue";
import AppCard from "../components/ui/AppCard.vue";

const finance = useFinanceStore();
const health = ref("checking");
const message = ref("");
async function seed() {
  await finance.seed();
  message.value = "Mock data seeded.";
}
async function reset() {
  await finance.reset();
  message.value = "Local data reset.";
}
onMounted(async () => {
  try {
    health.value = (await financeApi.health()).status;
  } catch {
    health.value = "offline";
  }
});
</script>
