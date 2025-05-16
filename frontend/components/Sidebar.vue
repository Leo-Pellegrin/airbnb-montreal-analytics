<template>
    <aside
        :class="['top-0 left-0 h-full bg-[#1A202C] z-20 transition-transform duration-200', sidebarOpen ? 'translate-x-0' : '-translate-x-full', 'w-60']"
        aria-label="Navigation principale" :aria-expanded="sidebarOpen">
        <nav class="flex flex-col pt-5 pb-4">
            <SidebarItem icon="i-heroicons-home" label="DASHBOARD" to="/" :active="route.path === '/'" />
            <SidebarItem icon="i-heroicons-clipboard-document-list" label="LISTINGS" to="/listings"
                :active="route.path === '/listings'" />
            <SidebarItem icon="i-heroicons-map" label="NEIGHBORHOOD STATS" to="/neighbourhoods"
                :active="route.path === '/neighbourhoods'" />
            <SidebarItem icon="i-heroicons-chat-bubble-left-right" label="REVIEWS" to="/reviews"
                :active="route.path === '/reviews'" />
            <SidebarItem icon="i-heroicons-cog-6-tooth" label="SETTINGS" to="/settings"
                :active="route.path === '/settings'" />
        </nav>
    </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
/**
 * Sidebar de navigation principale
 * Props: sidebarOpen (bool)
 * Events: closeSidebar (mobile)
 */
const props = defineProps({
    sidebarOpen: {
        type: Boolean,
        default: true
    }
})
const emit = defineEmits(['closeSidebar'])

const route = useRoute()
</script>

<style scoped>
.w-60 {
    width: 240px;
}

@media (max-width: 640px) {
    aside {
        box-shadow: 0 2px 8px 0 rgba(72, 72, 72, 0.08);
    }
}
</style>

<!-- SidebarItem.vue à créer pour factoriser chaque item -->