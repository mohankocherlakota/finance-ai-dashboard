<template>
  <label class="block">
    <span v-if="label" class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-500">{{ label }}</span>
    <select
      :value="modelValue"
      class="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm text-slate-900 outline-none transition focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:ring-blue-950"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <slot />
    </select>
  </label>
</template>

<script setup lang="ts">
defineProps<{ modelValue?: string; label?: string }>();
defineEmits<{ "update:modelValue": [value: string] }>();
</script>
