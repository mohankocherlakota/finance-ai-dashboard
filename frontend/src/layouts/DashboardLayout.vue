<template>
  <div :class="{ dark: darkMode }" class="min-h-screen">
    <div class="min-h-screen bg-slate-50 text-slate-950 dark:bg-slate-950 dark:text-slate-100">
      <AppSidebar v-model:collapsed="sidebarCollapsed" v-model:mobile-open="mobileSidebarOpen" />
      <div :class="['transition-[padding] duration-300 ease-out', sidebarCollapsed ? 'lg:pl-20' : 'lg:pl-72']">
        <AppTopbar
          :title="routeName"
          :dark-mode="darkMode"
          :sidebar-collapsed="sidebarCollapsed"
          @toggle-theme="toggleTheme"
          @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed"
          @open-mobile-sidebar="mobileSidebarOpen = true"
        />
        <main class="mx-auto max-w-[1500px] px-4 py-6 sm:px-6 lg:px-8">
          <RouterView />
        </main>
      </div>
      <AppToastHost />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import AppSidebar from "../components/ui/AppSidebar.vue";
import AppTopbar from "../components/ui/AppTopbar.vue";
import AppToastHost from "../components/ui/AppToastHost.vue";

const route = useRoute();
const darkMode = ref(localStorage.getItem("theme") === "dark");
const sidebarCollapsed = ref(localStorage.getItem("sidebar") === "collapsed");
const mobileSidebarOpen = ref(false);
const routeName = computed(() => String(route.name ?? "Dashboard"));

function toggleTheme() {
  darkMode.value = !darkMode.value;
  localStorage.setItem("theme", darkMode.value ? "dark" : "light");
}

watch(sidebarCollapsed, (value) => localStorage.setItem("sidebar", value ? "collapsed" : "expanded"));
watch(route, () => {
  mobileSidebarOpen.value = false;
});
onMounted(() => {
  document.documentElement.classList.toggle("dark", darkMode.value);
});
watch(darkMode, (value) => {
  document.documentElement.classList.toggle("dark", value);
});
</script>
