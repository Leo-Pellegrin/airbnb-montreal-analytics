<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch, computed, reactive } from 'vue'
interface Listing {
    id: string
    name: string
    neighborhood: string
    roomType: string
    price: number
    occupancyRate: number
    rating: number
}

const listings = ref<Listing[]>([
    { id: '12345', name: 'Cozy Loft', neighborhood: 'Downtown', roomType: 'Entire Home', price: 150, occupancyRate: 80, rating: 4.5 },
    { id: '67890', name: 'Sunny Apartment', neighborhood: 'Plateau', roomType: 'Private Room', price: 95, occupancyRate: 65, rating: 4.3 },
    { id: '11223', name: 'Modern Condo', neighborhood: 'Old Montreal', roomType: 'Shared Room', price: 70, occupancyRate: 50, rating: 4.7 },
])

// KPI cards
const kpiData = {
    price: { icon: 'i-heroicons-currency-dollar', label: 'Median Price', value: '93' },
    occupancy: { icon: 'i-heroicons-chart-bar', label: 'Occupancy Rate', value: '43.5%' },
    sentiment: { icon: 'i-heroicons-face-smile', label: 'Avg Review Sentiment', value: '0.64' },
}

// Map & chart data (mock)
const geoData = ref<any>(null)
const trendData = ref([])
const selectedKpi = ref<'price' | 'occupancy' | 'sentiment'>('price')

// listings table columns
const columns = [
    { title: 'Listing ID', key: 'id' },
    { title: 'Name', key: 'name' },
    { title: 'Neighborhood', key: 'neighborhood' },
    { title: 'Room Type', key: 'roomType' },
    { title: 'Price', key: 'price', render: (r: any) => `$${r.price}` },
    { title: 'Occupancy %', key: 'occupancyRate', render: (r: any) => `${r.occupancyRate}%` },
    { title: 'Rating', key: 'rating' },
]

// filtre options
const neighOptions = [
    { label: 'All Neighborhoods', value: '' },
    { label: 'Downtown', value: 'Downtown' },
    { label: 'Plateau', value: 'Plateau' },
    { label: 'Old Montreal', value: 'Old Montreal' },
]
const kpiOptions = [
    { label: 'Prix médian', value: 'price' },
    { label: 'Taux d’occupation', value: 'occupancy' },
    { label: 'Sentiment', value: 'sentiment' },
]
const roomOptions = [
    { label: 'Any Room Type', value: '' },
    { label: 'Entire Home', value: 'Entire Home' },
    { label: 'Private Room', value: 'Private Room' },
    { label: 'Shared Room', value: 'Shared Room' },
]
const periodOptions = [
    { label: 'This Week', value: 'this-week' },
    { label: 'Last Week', value: 'last-week' },
    { label: 'This Month', value: 'this-month' },
    { label: 'Last Month', value: 'last-month' },
]

// configuration des filtres pour le v-for
const filtersConfig = [
    { modelKey: 'neighborhood', placeholder: 'Neighborhood', options: neighOptions },
    { modelKey: 'kpi', placeholder: 'KPI', options: kpiOptions },
    { modelKey: 'roomType', placeholder: 'Room Type', options: roomOptions },
    { modelKey: 'period', placeholder: 'Period', options: periodOptions }
]

// handlers
function applyFilters() {
    // accès aux valeurs via filterModels.neighborhood, .kpi, etc.
    console.log('Apply', filterModels)
}

function clearFilters() {
    // remise à zéro
    filterModels.neighborhood = null
    filterModels.kpi = 'price'
    filterModels.roomType = null
    filterModels.period = 'weekly'
}
// modèles liés aux selects
const filterModels = reactive({
    neighborhood: null as string | null,
    kpi: 'price',
    roomType: null as string | null,
    period: 'weekly'
})

const filterNeighborhood = ref<string>('')
const filterRoomType = ref<string>('')
const filterPeriod = ref<string>('')

const filteredListings = computed(() =>
    listings.value.filter((l: any) =>
        (!filterNeighborhood.value || l.neighborhood === filterNeighborhood.value) &&
        (!filterRoomType.value || l.roomType === filterRoomType.value)
    )
)

onMounted(async () => {
    // mock fetch geoData & trendData
    // geoData.value = await fetch('/montreal-neighbourhoods.json').then(r => r.json())
    // trendData.value = ...
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
            <!-- <UCard>
                <TrendChart :data="trendData" :loading="false" />
            </UCard> -->
        </div>

        <!-- FILTERS -->
      
        <UCard>
            <ListingsTable/>
        </UCard>
    </div>
</template>

<style scoped>
/* tout le styling est géré par Nuxt UI */
</style>