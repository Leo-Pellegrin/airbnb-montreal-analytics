<template>
    <div class="p-4 md:p-6 lg:p-8 space-y-6 bg-[#d0d0d076] container h-full">
        <!-- Résumé global -->
        <div class="flex flex-wrap gap-6 mb-6 justify-center">
            <div
                class="flex gap-6 bg-white/80 rounded-xl shadow-md border border-primary px-8 py-4 items-center w-full md:w-auto justify-center">
                <div class="flex flex-col items-center px-4">
                    <span class="text-3xl md:text-4xl font-extrabold text-airbnb-pink-600 flex items-center gap-2">
                        {{ neighbourhoods.length }}
                    </span>
                    <span class="text-gray-500 text-xs mt-1">quartiers</span>
                </div>
                <USeparator orientation="vertical" color="primary" />
                <div class="flex flex-col items-center px-4">
                    <span class="text-3xl md:text-4xl font-extrabold text-airbnb-graydark flex items-center gap-2">
                        {{ avgPrice }} $
                    </span>
                    <span class="text-gray-500 text-xs mt-1">prix médian</span>
                </div>
                <USeparator orientation="vertical" color="primary" />
                <div class="flex flex-col items-center px-4">
                    <span class="text-3xl md:text-4xl font-extrabold text-airbnb-green-600 flex items-center gap-2">
                        {{ avgOccupancy }} %
                    </span>
                    <span class="text-gray-500 text-xs mt-1">occupation moyenne</span>
                </div>
            </div>
        </div>

        <!-- Barre de recherche et filtres -->
        <div class="flex flex-wrap gap-4 mb-8 items-end">
            <input v-model="search" type="text" placeholder="Rechercher un quartier..."
                class="border rounded px-3 py-2 w-64" />
            <div>
                <label class="text-xs text-gray-500">Prix max</label>
                <input v-model.number="filters.maxPrice" type="number" min="0"
                    class="border rounded px-2 py-1 w-20 ml-2" />
            </div>
            <div>
                <label class="text-xs text-gray-500">Occupation min (%)</label>
                <input v-model.number="filters.minOccupancy" type="number" min="0" max="100"
                    class="border rounded px-2 py-1 w-20 ml-2" />
            </div>
            <div>
                <label class="text-xs text-gray-500">Sentiment min</label>
                <input v-model.number="filters.minSentiment" type="number" min="0" max="5" step="0.1"
                    class="border rounded px-2 py-1 w-20 ml-2" />
            </div>
        </div>

        <!-- Grille de cards quartiers -->
        <transition-group name="fade-list" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <UNeighbourhoodCard v-for="neigh in filteredNeighbourhoods" :key="neigh.name" :name="neigh.name"
                :medianPrice="neigh.median_price" :occupancy="neigh.occupancy_pct" :avg_sentiment="neigh.avg_sentiment"
                :trend="neigh.trend" :description="neigh.description" :image="neigh.image"
                @click="goToDetails(neigh.name)" />
        </transition-group>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const neighbourhoods = ref<Array<{
    name: string
    median_price: number
    occupancy_pct: number
    avg_sentiment: number
    trend?: 'up' | 'down' | 'stable'
    description?: string
    image?: string
}>>([])

const search = ref('')
const filters = ref({
    maxPrice: 999,
    minOccupancy: 0,
    minSentiment: 0
})

const router = useRouter()

const avgPrice = computed(() =>
    neighbourhoods.value.length
        ? (neighbourhoods.value.reduce((sum, n) => sum + n.median_price, 0) / neighbourhoods.value.length).toFixed(0)
        : '-'
)
const avgOccupancy = computed(() =>
    neighbourhoods.value.length
        ? (neighbourhoods.value.reduce((sum, n) => sum + n.occupancy_pct, 0) / neighbourhoods.value.length).toFixed(0)
        : '-'
)

const filteredNeighbourhoods = computed(() =>
    neighbourhoods.value.filter(n =>
        n.name.toLowerCase().includes(search.value.toLowerCase()) &&
        n.median_price <= filters.value.maxPrice &&
        n.occupancy_pct * 1 >= filters.value.minOccupancy &&
        n.avg_sentiment >= filters.value.minSentiment
    )
)

function goToDetails(name: string) {
    router.push(`/neighbourhoods/${encodeURIComponent(name)}`)
}

async function load() {
    // Fake data enrichie avec images, descriptions, tendances
    neighbourhoods.value = [
        {
            name: 'Le Marais',
            median_price: 120,
            occupancy_pct: 87,
            avg_sentiment: 4.5,
            trend: 'up',
            description: 'Quartier historique et branché, réputé pour ses galeries d\'art et ses cafés.',
            // image: '/neigh-marais.jpg'
        },
        {
            name: 'Montmartre',
            median_price: 110,
            occupancy_pct: 82,
            avg_sentiment: 4.2,
            trend: 'stable',
            description: 'Célèbre pour la basilique du Sacré-Cœur et son ambiance bohème.',
            // image: '/neigh-montmartre.jpg'
        },
        {
            name: 'Latin Quarter',
            median_price: 105,
            occupancy_pct: 79,
            avg_sentiment: 4.0,
            trend: 'down',
            description: 'Quartier étudiant animé, connu pour ses librairies et ses bistrots.',
            // image: '/neigh-latin.jpg'
        },
        {
            name: 'Saint-Germain',
            median_price: 130,
            occupancy_pct: 90,
            avg_sentiment: 4.7,
            trend: 'up',
            description: 'Chic et littéraire, avec de nombreux cafés historiques.',
            // image: '/neigh-stgermain.jpg'
        },
        {
            name: 'Belleville',
            median_price: 95,
            occupancy_pct: 75,
            avg_sentiment: 3.8,
            trend: 'stable',
            description: 'Quartier cosmopolite, réputé pour son street art et ses vues sur Paris.',
            // image: '/neigh-belleville.jpg'
        },
        {
            name: 'Bastille',
            median_price: 100,
            occupancy_pct: 80,
            avg_sentiment: 4.1,
            trend: 'up',
            description: 'Dynamique et festif, célèbre pour ses bars et son histoire révolutionnaire.',
            // image: '/neigh-bastille.jpg'
        }
    ]
}

onMounted(load)
</script>

<style scoped>
input:focus {
    outline: 2px solid #FF5A5F;
}

.fade-list-enter-active,
.fade-list-leave-active {
    transition: all 0.4s cubic-bezier(.39, .575, .565, 1.000);
}

.fade-list-enter-from,
.fade-list-leave-to {
    opacity: 0;
    transform: translateY(30px);
}

.fade-list-leave-from,
.fade-list-enter-to {
    opacity: 1;
    transform: none;
}
</style>
