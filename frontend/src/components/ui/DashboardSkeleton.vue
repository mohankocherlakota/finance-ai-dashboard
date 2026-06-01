<template>
  <div class="space-y-6">
    <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <AppCard v-for="idx in 4" :key="idx">
        <div class="flex items-start justify-between">
          <div class="w-2/3 space-y-3">
            <SkeletonBlock width="55%" />
            <SkeletonBlock height="2rem" />
            <SkeletonBlock width="70%" />
          </div>
          <SkeletonBlock width="2.5rem" height="2.5rem" />
        </div>
      </AppCard>
    </div>
    <div class="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
      <AppCard><SkeletonBlock height="20rem" /></AppCard>
      <AppCard><SkeletonBlock height="20rem" /></AppCard>
    </div>
    <div class="grid gap-6 xl:grid-cols-[1fr_1.35fr]">
      <AppCard><SkeletonBlock height="17rem" /></AppCard>
      <AppCard><SkeletonBlock height="17rem" /></AppCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppCard from "./AppCard.vue";
import SkeletonBlock from "./SkeletonBlock.vue";
</script>
