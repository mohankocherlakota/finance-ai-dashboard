<template>
  <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-slate-950/40 backdrop-blur-sm lg:hidden" @click="$emit('update:mobileOpen', false)" />
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-50 flex flex-col border-r border-slate-200 bg-white/95 px-3 py-4 shadow-soft backdrop-blur-xl transition-all duration-300 dark:border-slate-800 dark:bg-slate-950/95',
      collapsed ? 'lg:w-20' : 'lg:w-72',
      mobileOpen ? 'w-72 translate-x-0' : 'w-72 -translate-x-full lg:translate-x-0',
    ]"
  >
    <div class="mb-6 flex items-center justify-between gap-3 px-2">
      <div class="flex min-w-0 items-center gap-3">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-600 text-white shadow-lg shadow-blue-600/20">
          <LineChart class="h-5 w-5" />
        </div>
        <div v-if="!collapsed" class="min-w-0">
          <p class="truncate text-base font-bold tracking-tight">finance-ai-dashboard</p>
          <p class="truncate text-xs text-slate-500">Enterprise finance cockpit</p>
        </div>
      </div>
      <button class="rounded-lg p-2 text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-900 lg:hidden" @click="$emit('update:mobileOpen', false)">
        <X class="h-4 w-4" />
      </button>
    </div>
    <nav class="space-y-1">
      <RouterLink
        v-for="item in nav"
        :key="item.path"
        :to="item.path"
        :title="collapsed ? item.label : undefined"
        :class="[
          'group flex h-11 items-center rounded-lg text-sm font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-900 dark:hover:text-white',
          collapsed ? 'justify-center px-0' : 'gap-3 px-3',
        ]"
        exact-active-class="!bg-blue-50 !text-blue-700 dark:!bg-blue-950 dark:!text-blue-300"
      >
        <component :is="item.icon" class="h-4 w-4 shrink-0" />
        <span v-if="!collapsed">{{ item.label }}</span>
      </RouterLink>
    </nav>
    <div class="mt-auto rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-900" :class="collapsed && 'hidden'">
      <p class="text-xs font-semibold text-slate-700 dark:text-slate-200">Data status</p>
      <p class="mt-1 text-xs text-slate-500">Synced Plaid data is active. Demo data only loads when no transactions exist.</p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { BarChart3, Bot, CreditCard, LayoutDashboard, LineChart, Plug, Settings, Target, X } from "lucide-vue-next";

defineProps<{ collapsed: boolean; mobileOpen: boolean }>();
defineEmits<{ "update:collapsed": [value: boolean]; "update:mobileOpen": [value: boolean] }>();

const nav = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/transactions", label: "Transactions", icon: CreditCard },
  { path: "/budget", label: "Budget", icon: BarChart3 },
  { path: "/debt-goals", label: "Debt Goals", icon: Target },
  { path: "/insights", label: "Insights", icon: Bot },
  { path: "/plaid", label: "Plaid Connect", icon: Plug },
  { path: "/settings", label: "Settings", icon: Settings },
];
</script>
