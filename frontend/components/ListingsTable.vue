<template>
    <div class="bg-white rounded-lg p-4 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
            <UInput v-model="search" placeholder="Rechercher par titre ou description..." class="flex-1" />
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
import type { TableColumn } from '@nuxt/ui'



const neighborhoodOptions = [
    { value: 'all', label: 'Tous les quartiers' },
    { value: 'Plateau-Mont-Royal', label: 'Plateau-Mont-Royal' },
    { value: 'Vieux-Montréal', label: 'Vieux-Montréal' },
    { value: 'Outremont', label: 'Outremont' },
    { value: 'Rosemont-La Petite-Patrie', label: 'Rosemont-La Petite-Patrie' },
    { value: 'Côte-des-Neiges', label: 'Côte-des-Neiges' }
]

const roomTypes = [
    { value: 'any', label: 'Type' },
    { value: 'Entire home/apt', label: 'Logement entier' },
    { value: 'Private room', label: 'Chambre privée' },
    { value: 'Shared room', label: 'Chambre partagée' }
]

interface Listing {
    id: number
    name: string
    neighbourhood: string
    price: number
    min_nights: number
    num_reviews: number
    rating: number
}

const listingsTest = ref<Listing[]>([
    { id: 1, name: 'Appartement moderne', neighbourhood: 'Plateau-Mont-Royal', price: 120, min_nights: 2, num_reviews: 45, rating: 4.7 },
    { id: 2, name: 'Chambre cosy', neighbourhood: 'Vieux-Montréal', price: 80, min_nights: 1, num_reviews: 32, rating: 4.5 },
    { id: 3, name: 'Loft spacieux', neighbourhood: 'Outremont', price: 150, min_nights: 3, num_reviews: 56, rating: 4.8 },
    { id: 4, name: 'Studio lumineux', neighbourhood: 'Rosemont-La Petite-Patrie', price: 95, min_nights: 2, num_reviews: 28, rating: 4.6 },
    { id: 5, name: 'Maison entière', neighbourhood: 'Côte-des-Neiges', price: 200, min_nights: 4, num_reviews: 62, rating: 4.9 },
    { id: 6, name: 'Duplex chic', neighbourhood: 'Le Sud-Ouest', price: 180, min_nights: 3, num_reviews: 48, rating: 4.7 },
    { id: 7, name: 'Appartement design', neighbourhood: 'Ville-Marie', price: 250, min_nights: 2, num_reviews: 72, rating: 4.9 },
    { id: 8, name: 'Loft industriel', neighbourhood: 'Mercier-Hochelaga-Maisonneuve', price: 130, min_nights: 2, num_reviews: 36, rating: 4.4 },
    { id: 9, name: 'Studio bohème', neighbourhood: 'Ahuntsic-Cartierville', price: 90, min_nights: 1, num_reviews: 25, rating: 4.3 },
    { id: 10, name: 'Maison de ville', neighbourhood: 'Rivière-des-Prairies', price: 300, min_nights: 4, num_reviews: 60, rating: 4.8 }
])

const columns: TableColumn<Listing>[] = [
    {
        accessorKey: 'id',
        header: 'ID'
    },
    {
        accessorKey: 'name',
        header: 'Name'
    },
    {
        accessorKey: 'neighbourhood',
        header: 'Neighbourhood'
    },
    {
        accessorKey: 'price',
        header: 'Price'
    },
    {
        accessorKey: 'min_nights',
        header: 'Min Nights'
    },
    {
        accessorKey: 'num_reviews',
        header: 'Num Reviews'
    },
    {
        accessorKey: 'rating',
        header: 'Rating'
    }
]

const props = defineProps({
    listings: {
        type: Array, default: () => [

        ]
    },
    loading: { type: Boolean, default: false }
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
    let res = listingsTest.value
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