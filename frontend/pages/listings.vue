<script setup lang="ts">
import { ref, computed } from 'vue'

interface Listing {
    id: number
    price: number
    latitude: number
    longitude: number
    neighbourhood: string
    room_type: string
    name: string
}

// Beaucoup plus de données fictives pour tester le scroll
const mockListings: Listing[] = [
    // Downtown
    { id: 1, name: 'Loft Moderne', price: 120, latitude: 45.5, longitude: -73.6, neighbourhood: 'Downtown', room_type: 'Entire Home' },
    { id: 2, name: 'Appartement lumineux', price: 110, latitude: 45.54, longitude: -73.57, neighbourhood: 'Downtown', room_type: 'Private Room' },
    { id: 3, name: 'Loft industriel', price: 130, latitude: 45.5, longitude: -73.61, neighbourhood: 'Downtown', room_type: 'Entire Home' },
    { id: 4, name: 'Appartement familial', price: 140, latitude: 45.54, longitude: -73.56, neighbourhood: 'Downtown', room_type: 'Entire Home' },
    { id: 5, name: 'Studio central', price: 90, latitude: 45.53, longitude: -73.62, neighbourhood: 'Downtown', room_type: 'Private Room' },
    { id: 6, name: 'Penthouse urbain', price: 200, latitude: 45.55, longitude: -73.60, neighbourhood: 'Downtown', room_type: 'Entire Home' },
    { id: 7, name: 'Chambre design', price: 85, latitude: 45.56, longitude: -73.59, neighbourhood: 'Downtown', room_type: 'Shared Room' },
    { id: 8, name: 'Loft panoramique', price: 175, latitude: 45.57, longitude: -73.58, neighbourhood: 'Downtown', room_type: 'Entire Home' },
    { id: 9, name: 'Appartement cosy', price: 100, latitude: 45.58, longitude: -73.57, neighbourhood: 'Downtown', room_type: 'Private Room' },
    { id: 10, name: 'Studio chic', price: 95, latitude: 45.59, longitude: -73.56, neighbourhood: 'Downtown', room_type: 'Private Room' },
    // Plateau
    { id: 11, name: 'Studio Plateau', price: 80, latitude: 45.52, longitude: -73.58, neighbourhood: 'Plateau', room_type: 'Private Room' },
    { id: 12, name: 'Chambre cosy', price: 60, latitude: 45.53, longitude: -73.59, neighbourhood: 'Plateau', room_type: 'Shared Room' },
    { id: 13, name: 'Chambre étudiante', price: 55, latitude: 45.52, longitude: -73.60, neighbourhood: 'Plateau', room_type: 'Shared Room' },
    { id: 14, name: 'Petit studio', price: 75, latitude: 45.53, longitude: -73.58, neighbourhood: 'Plateau', room_type: 'Private Room' },
    { id: 15, name: 'Appartement arty', price: 105, latitude: 45.54, longitude: -73.57, neighbourhood: 'Plateau', room_type: 'Entire Home' },
    { id: 16, name: 'Loft créatif', price: 115, latitude: 45.55, longitude: -73.56, neighbourhood: 'Plateau', room_type: 'Entire Home' },
    { id: 17, name: 'Chambre bohème', price: 65, latitude: 45.56, longitude: -73.55, neighbourhood: 'Plateau', room_type: 'Shared Room' },
    { id: 18, name: 'Studio vintage', price: 85, latitude: 45.57, longitude: -73.54, neighbourhood: 'Plateau', room_type: 'Private Room' },
    { id: 19, name: 'Appartement pop', price: 110, latitude: 45.58, longitude: -73.53, neighbourhood: 'Plateau', room_type: 'Entire Home' },
    { id: 20, name: 'Chambre zen', price: 70, latitude: 45.59, longitude: -73.52, neighbourhood: 'Plateau', room_type: 'Shared Room' },
    // Old Montreal
    { id: 21, name: 'Condo Vieux-Montréal', price: 150, latitude: 45.51, longitude: -73.55, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 22, name: 'Condo chic', price: 170, latitude: 45.51, longitude: -73.54, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 23, name: 'Appartement historique', price: 160, latitude: 45.50, longitude: -73.53, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 24, name: 'Loft patrimonial', price: 180, latitude: 45.49, longitude: -73.52, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 25, name: 'Studio pierre', price: 100, latitude: 45.48, longitude: -73.51, neighbourhood: 'Old Montreal', room_type: 'Private Room' },
    { id: 26, name: 'Chambre voûtée', price: 90, latitude: 45.47, longitude: -73.50, neighbourhood: 'Old Montreal', room_type: 'Shared Room' },
    { id: 27, name: 'Appartement musée', price: 155, latitude: 45.46, longitude: -73.49, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 28, name: 'Condo design', price: 165, latitude: 45.45, longitude: -73.48, neighbourhood: 'Old Montreal', room_type: 'Entire Home' },
    { id: 29, name: 'Studio charme', price: 105, latitude: 45.44, longitude: -73.47, neighbourhood: 'Old Montreal', room_type: 'Private Room' },
    { id: 30, name: 'Chambre médiévale', price: 95, latitude: 45.43, longitude: -73.46, neighbourhood: 'Old Montreal', room_type: 'Shared Room' },
]

// Nombre de listings à afficher par quartier au départ
const INITIAL_COUNT = 4

// Regrouper les listings par quartier
const listingsByNeighbourhood = computed(() => {
    const grouped: Record<string, Listing[]> = {}
    for (const l of mockListings) {
        if (!grouped[l.neighbourhood]) grouped[l.neighbourhood] = []
        grouped[l.neighbourhood].push(l)
    }
    return grouped
})

// Suivi du nombre de listings affichés par quartier
const shownCounts = ref<Record<string, number>>({})

// Initialiser le nombre de listings affichés
for (const neigh in listingsByNeighbourhood.value) {
    shownCounts.value[neigh] = INITIAL_COUNT
}

function showMore(neigh: string) {
    shownCounts.value[neigh] += INITIAL_COUNT
}
</script>

<template>
    <div class="p-4 md:p-6 lg:p-8 space-y-6 bg-[#d0d0d076] container h-full">
        <div>

            <div v-for="(listings, neigh) in listingsByNeighbourhood" :key="neigh" class="mb-10">
                <h2 class="text-xl font-semibold mb-3">{{ neigh }}</h2>
                <div class="overflow-x-auto no-scrollbar max-w-full">
                    <div class="flex space-x-10 pb-2 flex-nowrap">
                        <UCard v-for="listing in listings" :key="listing.id"
                            class="min-w-[260px] max-w-xs flex-shrink-0 shadow-md border border-gray-200 bg-white hover:shadow-lg transition-shadow cursor-pointer">
                            <div class="flex flex-col gap-2">
                                <div class="font-bold text-lg text-primary">{{ listing.name }}</div>
                                <div class="text-sm text-gray-500">{{ listing.room_type }}</div>
                                <div class="text-base font-semibold">Prix : <span class="text-secondary">${{
                                    listing.price
                                        }}</span></div>
                                <div class="text-xs text-gray-400">Lat: {{ listing.latitude }}, Lng: {{
                                    listing.longitude }}
                                </div>
                            </div>
                        </UCard>
                    </div>
                </div>
            </div>
            <div v-if="Object.keys(listingsByNeighbourhood).length === 0" class="text-center text-gray-500 py-8">
                Aucun quartier ou logement à afficher.
            </div>
        </div>
    </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
    display: none;
}

.no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

</style>
