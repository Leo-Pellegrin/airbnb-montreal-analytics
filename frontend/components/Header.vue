<template>
    <header class="top-0 left-0 w-full h-16 bg-white  flex items-center z-30">
        <div class="flex-1 flex justify-start items-center h-full">
            <h1 class="text-2xl pl-10 font-bold text-primary">Airbnb Montréal Analytics</h1>
        </div>
        <div class="flex items-center justify-end h-full px-4 w-1/3">

            <UAvatar src="https://github.com/benjamincanac.png" class="mx-2" />

            <UButton @click="exportPDF" label="Export to PDF" color="primary" class="mx-2"></UButton>
            <UButton icon="i-heroicons-share" color="secondary" class="mx-2" variant="solid"></UButton>
        </div>
    </header>
</template>

<script setup lang="ts">
/**
 * Header Airbnb Montréal Analytics
 * Props: none
 * Events: toggleSidebar (mobile)
 */
function exportPDF() {
    return
}
</script>

<style scoped>
header {
    font-family: 'Circular', 'Helvetica Neue', sans-serif;
    height: 64px;
}
</style>