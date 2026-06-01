<template>
  <div class="grid gap-6 xl:grid-cols-[1fr_.9fr]">
    <AppCard>
      <template #header><h2 class="font-semibold">Plaid Sandbox connection</h2></template>
      <div class="space-y-4">
        <div class="rounded-lg bg-slate-50 p-4 text-sm text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          Full Plaid Link will mount here in production. For the MVP, create a Sandbox link token or paste a Sandbox public_token and exchange it server-side.
        </div>
        <AppButton :disabled="plaid.loading" @click="plaid.createLinkToken">Create Link Token</AppButton>
        <textarea v-model="plaid.linkToken" class="h-24 w-full rounded-lg border border-slate-200 bg-white p-3 text-sm dark:border-slate-700 dark:bg-slate-900" placeholder="Link token output" />
        <input v-model="publicToken" class="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-900" placeholder="Paste Sandbox public_token" />
        <div class="flex flex-wrap gap-2">
          <AppButton :disabled="plaid.loading || !publicToken" @click="plaid.exchangePublicToken(publicToken)">Exchange Token</AppButton>
          <AppButton variant="secondary" :disabled="plaid.loading" @click="sync">Sync Transactions</AppButton>
        </div>
      </div>
    </AppCard>
    <AppCard>
      <template #header><h2 class="font-semibold">Connection status</h2></template>
      <AppBadge tone="info">{{ plaid.status }}</AppBadge>
      <p class="mt-4 text-sm text-slate-500">Secrets remain in the backend .env file. Access tokens are never sent to the Vue app.</p>
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { usePlaidStore } from "../stores/plaidStore";
import { useFinanceStore } from "../stores/financeStore";
import AppBadge from "../components/ui/AppBadge.vue";
import AppButton from "../components/ui/AppButton.vue";
import AppCard from "../components/ui/AppCard.vue";

const plaid = usePlaidStore();
const finance = useFinanceStore();
const publicToken = ref("");
async function sync() {
  await plaid.syncTransactions();
  await finance.loadAll();
}
</script>
