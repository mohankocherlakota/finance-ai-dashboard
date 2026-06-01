<template>
  <header class="sticky top-0 z-30 border-b border-slate-200 bg-slate-50/85 px-4 py-3 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/85 sm:px-6 lg:px-8">
    <div class="mx-auto flex max-w-[1500px] items-center justify-between gap-3">
      <div class="flex min-w-0 items-center gap-3">
        <button class="rounded-lg border border-slate-200 bg-white p-2 text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 lg:hidden" @click="$emit('openMobileSidebar')">
          <Menu class="h-4 w-4" />
        </button>
        <button class="hidden rounded-lg border border-slate-200 bg-white p-2 text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 lg:inline-flex" @click="$emit('toggleSidebar')">
          <PanelLeftClose v-if="!sidebarCollapsed" class="h-4 w-4" />
          <PanelLeftOpen v-else class="h-4 w-4" />
        </button>
        <div class="min-w-0">
          <p class="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Workspace</p>
          <h1 class="truncate text-xl font-bold">{{ title }}</h1>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <select class="hidden h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm font-medium text-slate-700 shadow-sm outline-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 sm:block">
          <option>Last 6 months</option>
          <option>Last 90 days</option>
          <option>This month</option>
        </select>
        <button class="inline-flex h-10 items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800" @click="$emit('toggleTheme')">
          <Sun v-if="darkMode" class="h-4 w-4" />
          <Moon v-else class="h-4 w-4" />
          <span class="hidden sm:inline">{{ darkMode ? "Light" : "Dark" }}</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Menu, Moon, PanelLeftClose, PanelLeftOpen, Sun } from "lucide-vue-next";

defineProps<{ title: string; darkMode: boolean; sidebarCollapsed: boolean }>();
defineEmits<{ toggleTheme: []; toggleSidebar: []; openMobileSidebar: [] }>();
</script>
