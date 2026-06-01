<template>
  <button
    :class="[
      'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50',
      variant === 'primary' && 'bg-brand text-white shadow-sm shadow-blue-600/20 hover:bg-blue-700',
      variant === 'secondary' && 'border border-slate-200 bg-white text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800',
      variant === 'danger' && 'bg-danger text-white hover:bg-rose-700',
    ]"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ variant?: "primary" | "secondary" | "danger" }>(), { variant: "primary" });
</script>
