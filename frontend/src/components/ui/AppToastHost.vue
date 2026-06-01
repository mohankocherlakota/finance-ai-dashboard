<template>
  <div class="fixed right-4 top-4 z-[80] flex w-[calc(100vw-2rem)] max-w-sm flex-col gap-3 sm:right-6 sm:top-6">
    <TransitionGroup
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-2 opacity-0"
    >
      <div
        v-for="toast in store.toasts"
        :key="toast.id"
        class="rounded-lg border bg-white p-4 shadow-soft ring-1 ring-black/5 dark:bg-slate-900"
        :class="toneClass(toast.tone)"
      >
        <div class="flex gap-3">
          <component :is="toneIcon(toast.tone)" class="mt-0.5 h-5 w-5 shrink-0" />
          <div class="min-w-0 flex-1">
            <p class="text-sm font-semibold text-slate-950 dark:text-white">{{ toast.title }}</p>
            <p v-if="toast.message" class="mt-1 text-sm text-slate-600 dark:text-slate-300">{{ toast.message }}</p>
          </div>
          <button class="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-200" @click="store.remove(toast.id)">
            <X class="h-4 w-4" />
          </button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { AlertCircle, CheckCircle2, Info, X } from "lucide-vue-next";
import { useToastStore, type ToastTone } from "../../stores/toastStore";

const store = useToastStore();
const toneClass = (tone: ToastTone) =>
  ({
    success: "border-emerald-200 text-emerald-600 dark:border-emerald-900",
    error: "border-rose-200 text-rose-600 dark:border-rose-900",
    info: "border-blue-200 text-blue-600 dark:border-blue-900",
  })[tone];
const toneIcon = (tone: ToastTone) => ({ success: CheckCircle2, error: AlertCircle, info: Info })[tone];
</script>
