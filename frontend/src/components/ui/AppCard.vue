<template>
  <section class="enterprise-panel overflow-hidden">
    <div v-if="$slots.header" class="border-b border-slate-100 bg-white/60 px-5 py-4 dark:border-slate-800 dark:bg-slate-900/60">
      <slot name="header" />
    </div>
    <div class="p-5">
      <slot />
    </div>
  </section>
</template>
