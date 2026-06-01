<template>
  <div class="animate-pulse rounded-lg bg-slate-200/80 dark:bg-slate-800" :style="{ height, width }" />
</template>

<script setup lang="ts">
withDefaults(defineProps<{ height?: string; width?: string }>(), { height: "1rem", width: "100%" });
</script>
