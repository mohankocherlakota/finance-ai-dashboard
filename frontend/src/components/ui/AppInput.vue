<template>
  <label class="block">
    <span v-if="label" class="mb-1.5 block text-xs font-semibold uppercase tracking-wide text-slate-500">{{ label }}</span>
    <div class="relative">
      <component v-if="icon" :is="icon" class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
      <input
        v-bind="$attrs"
        :value="modelValue"
        :class="[
          'h-10 w-full rounded-lg border border-slate-200 bg-white text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:ring-blue-950',
          icon ? 'pl-9 pr-3' : 'px-3',
        ]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
    </div>
  </label>
</template>

<script setup lang="ts">
defineOptions({ inheritAttrs: false });
defineProps<{ modelValue?: string | number; label?: string; icon?: any }>();
defineEmits<{ "update:modelValue": [value: string] }>();
</script>
