<template>
  <div class="rounded-lg border border-dashed border-slate-200 bg-white p-8 text-center dark:border-slate-800 dark:bg-slate-900">
    <p class="font-semibold text-slate-800 dark:text-slate-100">{{ title }}</p>
    <p class="mt-2 text-sm text-slate-500">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string; message: string }>();
</script>
