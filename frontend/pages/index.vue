<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch, computed, reactive } from 'vue'
import { useStats } from '../composables/useStats'
import { useListings } from '../composables/useListings'


const { stats, fetchStats } = useStats()
const { listings, loading, fetchListings } = useListings()

// KPI cards
const kpiData = computed(() => ({
    price: {
        icon: 'i-heroicons-currency-dollar',
        label: 'Median Price',
        value: stats.value.medianPrice ? `$${stats.value.medianPrice}` : 'Loading...'
    },
    occupancy: {
        icon: 'i-heroicons-chart-bar',
        label: 'Occupancy Rate',
        value: stats.value.occupancyPct ? `${(stats.value.occupancyPct * 100).toFixed(1)}%` : 'Loading...'
    },
    sentiment: {
        icon: 'i-heroicons-face-smile',
        label: 'Avg Review Sentiment',
        value: stats.value.avgSentiment ? stats.value.avgSentiment.toFixed(2) : 'Loading...'
    },
}))


onMounted(async () => {
    await fetchStats()
    await fetchListings()
})
</script>

<template>
    <div class="p-4 md:p-6 lg:p-8 space-y-6 bg-[#d0d0d076] container">

        <!-- KPI CARDS -->
        <div class="grid grid-cols-3 gap-4">
            <KpiCard v-for="(d, key) in kpiData" :key="key" :label="d.label" :icon="d.icon" :value="d.value"
                :showCurrencySymbol="key === 'price'" />
        </div>

        <!-- MAP + TREND -->
        <div class="grid grid-cols-3 gap-4">
            <UCard class="col-span-4 lg:col-span-3">
                <MapOpenLayer></MapOpenLayer>
            </UCard>
        </div>

        <UCard>
            <ListingsTable :listings="listings" :loading="loading" />
        </UCard>
    </div>
</template>

<style scoped></style>