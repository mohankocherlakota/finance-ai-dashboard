<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-slate-100 dark:divide-slate-800">
      <thead>
        <tr class="text-left text-xs uppercase tracking-wide text-slate-500">
          <th class="table-cell">Merchant</th>
          <th class="table-cell">Category</th>
          <th class="table-cell">Frequency</th>
          <th class="table-cell text-right">Avg Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.merchant">
          <td class="table-cell font-medium">{{ row.merchant }}</td>
          <td class="table-cell">{{ row.category }}</td>
          <td class="table-cell">{{ row.frequency }}</td>
          <td class="table-cell text-right font-semibold">{{ money(row.amount) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps<{ rows: any[] }>();
const money = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);
</script>
