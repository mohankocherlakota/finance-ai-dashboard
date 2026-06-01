import { defineStore } from "pinia";
import { ref } from "vue";

export type ToastTone = "success" | "error" | "info";

export interface Toast {
  id: number;
  title: string;
  message?: string;
  tone: ToastTone;
}

export const useToastStore = defineStore("toast", () => {
  const toasts = ref<Toast[]>([]);

  function push(toast: Omit<Toast, "id">) {
    const id = Date.now() + Math.random();
    toasts.value.push({ ...toast, id });
    window.setTimeout(() => remove(id), 4200);
  }

  function success(title: string, message?: string) {
    push({ title, message, tone: "success" });
  }

  function error(title: string, message?: string) {
    push({ title, message, tone: "error" });
  }

  function info(title: string, message?: string) {
    push({ title, message, tone: "info" });
  }

  function remove(id: number) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id);
  }

  return { toasts, push, success, error, info, remove };
});
