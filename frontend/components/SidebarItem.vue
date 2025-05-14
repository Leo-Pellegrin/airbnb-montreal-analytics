<template>
    <NuxtLink :to="to"
        class="flex items-center px-6 py-3 mb-2 transition-colors duration-200 group focus:outline-none focus:ring-2 focus:ring-airbnb-rose"
        :class="[active ? 'bg-[#2D3748]' : '', 'hover:bg-[#aabad6]']" :aria-label="label">
        <Icon :name="icon" class="w-6 h-6 mr-4 text-white" aria-hidden="true" />
        <span class="font-circular font-medium text-white text-sm">{{ label }}</span>
    </NuxtLink>
</template>

<script setup lang="ts">
/**
 * SidebarItem
 * Props:
 * - icon (string, requis)
 * - label (string, requis)
 * - to (string, requis)
 * - active (bool, optionnel)
 */
const props = defineProps({
    icon: { type: String, required: true },
    label: { type: String, required: true },
    to: { type: String, required: true },
    active: { type: Boolean, default: false }
})
</script>