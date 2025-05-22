<template>
    <div class="bg-white rounded-lg p-4 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
            <UInput v-model="search" placeholder="Rechercher par nom..." class="flex-1" />
            <div class="flex gap-2 flex-wrap">
                <UInput v-model.number="filters.priceMin" type="number" min="0" placeholder="Prix min" class="w-24" />
                <UInput v-model.number="filters.priceMax" type="number" min="0" placeholder="Prix max" class="w-24" />
                <USelect v-model="filters.roomType" :items="roomTypes" placeholder="Type de chambre" />
                <USelect v-model="filters.neighborhood" :items="neighborhoodOptions" placeholder="Quartier" />
            </div>
        </div>

        <div class="flex flex-col gap-4">
            <UTable :data="paginatedListings" :columns="columns" />
            <UPagination class="mx-auto" :default-page="(pagination.pageIndex || 0) + 1"
                :items-per-page="pagination.pageSize" :total="filteredListings.length"
                @update:page="(p) => pagination.pageIndex = p - 1" />
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'


const neighborhoodOptions = computed(() => {
    const values = Array.from(new Set(props.listings.map((l: any) => l.neighbourhood).filter(Boolean)))
    return [{ value: 'all', label: 'Tous les quartiers' }, ...values.map(v => ({ value: v, label: v }))]
})

const roomTypes = computed(() => {
    const values = Array.from(new Set(props.listings.map((l: any) => l.room_type).filter(Boolean)))
    return [{ value: 'any', label: 'Type' }, ...values.map(v => ({ value: v, label: v }))]
})

const columns = [
    { accessorKey: 'name', header: 'Name' },
    { accessorKey: 'neighbourhood', header: 'Neighbourhood' },
    { accessorKey: 'price', header: 'Price' },
    { accessorKey: 'minimum_nights', header: 'Min Nights' },
    { accessorKey: 'number_of_reviews', header: 'Num Reviews' },
]

const props = defineProps({
    listings: { type: Array, required: true },
    loading: { type: Boolean, default: false },
    error: { type: String, default: null }
})

const emit = defineEmits(['update:filters'])

const search = ref('')
const filters = ref({ priceMin: '', priceMax: '', roomType: '', neighborhood: '' })
const pagination = ref({
    pageIndex: 0,
    pageSize: 5
})

const paginatedListings = computed(() => {
    const start = pagination.value.pageIndex * pagination.value.pageSize
    const end = start + pagination.value.pageSize
    return filteredListings.value.slice(start, end)
})

const filteredListings = computed(() => {
    // let res = props.listings
    let res = props.listings
    if (search.value) {
        const s = search.value.toLowerCase()
        res = res.filter((l: any) => (l.name && l.name.toLowerCase().includes(s)) || (l.description && l.description.toLowerCase().includes(s)))
    }
    if (filters.value.priceMin) res = res.filter((l: any) => l.price && l.price >= filters.value.priceMin)
    if (filters.value.priceMax) res = res.filter((l: any) => l.price && l.price <= filters.value.priceMax)
    if (filters.value.roomType && filters.value.roomType !== 'any') res = res.filter((l: any) => l.room_type && l.room_type === filters.value.roomType)
    if (filters.value.neighborhood && filters.value.neighborhood !== 'all') res = res.filter((l: any) => l.neighbourhood && l.neighbourhood === filters.value.neighborhood)
    return res
})

watch(filters, () => emit('update:filters', filters.value), { deep: true })
</script>