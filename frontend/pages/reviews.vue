<template>
    <div class="p-4 md:p-6 lg:p-8 space-y-6 bg-[#d0d0d076] container h-full">

        <!-- Résumé global -->
        <div class="flex flex-wrap gap-6 mb-10 justify-center">
            <div
                class="flex gap-6 bg-white/80 rounded-xl shadow-md border border-primary px-8 py-4 items-center w-full md:w-auto justify-center">
                <div class="flex flex-col items-center px-4">
                    <span class="text-3xl md:text-4xl font-extrabold text-airbnb-pink-600 flex items-center gap-2">
                        {{ reviews.length }}
                    </span>
                    <span class="text-gray-500 text-xs mt-1">avis</span>
                </div>
                <USeparator orientation="vertical" color="primary" />
                <div class="flex flex-col items-center px-4">
                    <span class="text-3xl md:text-4xl font-extrabold text-airbnb-yellow-500 flex items-center gap-2">
                        {{ avgRating }} ★
                    </span>
                    <span class="text-gray-500 text-xs mt-1">note moyenne</span>
                </div>
            </div>
        </div>
        <!-- Filtres -->
        <div class="flex gap-4 mb-6 flex-wrap items-center">
            <UInput size="xl" v-model="search" placeholder="Rechercher un avis..."
                class="rounded px-3 py-2 w-64 focus:outline-primary" />
            <div>                
                <USelect size="xl" v-model="filterRating" :items="ratingOptions" placeholder="Select Rating"
                    class="w-32 ml-2" color="primary" />
            </div>
        </div>
        <!-- Liste des avis -->
        <transition-group name="fade-list" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ReviewCard v-for="review in filteredReviews" :key="review.id" :review="review" />
        </transition-group>
        <div v-if="filteredReviews.length === 0" class="text-center text-airbnb-graydark text-lg py-12 transition-all duration-300">
            Aucun avis ne correspond à votre recherche.
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const reviews = ref([
    {
        id: 1,
        author: 'Alice',
        avatar: '/avatar-alice.jpg',
        date: '2024-06-01',
        rating: 5,
        text: 'Super séjour à Montmartre, hôte très accueillant !',
        neighbourhood: 'Montmartre',
        sentiment: 1
    },
    {
        id: 2,
        author: 'Bob',
        avatar: '/avatar-bob.jpg',
        date: '2024-05-20',
        rating: 3,
        text: 'Appartement bien situé mais un peu bruyant.',
        neighbourhood: 'Le Marais',
        sentiment: 0
    },
    {
        id: 3,
        author: 'Chloé',
        avatar: '/avatar-chloe.jpg',
        date: '2024-05-10',
        rating: 4,
        text: 'Quartier agréable, logement propre et fonctionnel.',
        neighbourhood: 'Saint-Germain',
        sentiment: 1
    },
    {
        id: 4,
        author: 'David',
        avatar: '',
        date: '2024-04-28',
        rating: 2,
        text: 'Déçu par le manque de propreté, mais bon emplacement.',
        neighbourhood: 'Belleville',
        sentiment: -1
    },
    {
        id: 5,
        author: '',
        avatar: '',
        date: '2024-04-15',
        rating: 5,
        text: 'Expérience parfaite, je recommande vivement !',
        neighbourhood: 'Bastille',
        sentiment: 1
    }
])

const search = ref('')
const filterRating = ref('Toutes')

const ratingOptions = [
    { label: 'Toutes', value: 'Toutes' },
    { label: '5 ★', value: 5 },
    { label: '4 ★', value: 4 },
    { label: '3 ★', value: 3 },
    { label: '2 ★', value: 2 },
    { label: '1 ★', value: 1 },
]

const avgRating = computed(() => {
    if (!reviews.value.length) return '-'
    return (
        reviews.value.reduce((sum, r) => sum + r.rating, 0) / reviews.value.length
    ).toFixed(1)
})

const filteredReviews = computed(() =>
    reviews.value.filter(r =>
        (filterRating.value === 'Toutes' || r.rating === Number(filterRating.value)) &&
        (r.text.toLowerCase().includes(search.value.toLowerCase()) ||
            r.author.toLowerCase().includes(search.value.toLowerCase()) ||
            r.neighbourhood.toLowerCase().includes(search.value.toLowerCase()))
    )
)

const ratingCounts = computed(() => {
    const counts: Record<number, number> = {}
    for (let n = 1; n <= 5; n++) counts[n] = 0
    reviews.value.forEach(r => { counts[r.rating] = (counts[r.rating] || 0) + 1 })
    return counts
})

const ratingDistribution = computed(() => {
    const max = Math.max(...Object.values(ratingCounts.value)) || 1
    const dist: Record<number, number> = {}
    for (let n = 1; n <= 5; n++) {
        dist[n] = Math.round((ratingCounts.value[n] / max) * 100)
    }
    return dist
})
</script>

<style scoped>
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