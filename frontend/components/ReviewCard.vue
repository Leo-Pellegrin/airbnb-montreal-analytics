<template>
    <UCard class="hover:shadow-lg transition-shadow duration-200">
        <div class="p-4 space-y-2">
            <div class="flex items-center gap-3">
                <UAvatar v-if="review.avatar" :src="review.avatar" />
                <UAvatar v-else src="https://github.com/benjamincanac.png" />
                <div>
                    <div class="font-semibold text-airbnb-graydark">{{ review.author || 'Voyageur anonyme' }}</div>
                    <div class="text-xs text-gray-400">{{ review.date }}</div>
                </div>
                <span class="ml-auto text-lg font-bold text-yellow-500">{{ review.rating }} ★</span>
            </div>
            <div class="text-sm text-gray-700 mt-1">{{ review.text }}</div>
            <div class="flex gap-2 mt-2 flex-wrap">
                <span class="bg-primary text-airbnb-pink-700 text-white font-bold p-2 rounded text-xs">{{
                    review.neighbourhood
                    }}</span>
                <UBadge v-if="review.sentiment !== undefined" variant="outline"
                    :color="review.sentiment > 0 ? 'success' : review.sentiment < 0 ? 'error' : 'neutral'"
                    class="p-2 rounded text-xs">
                    {{ review.sentiment > 0 ? 'Positif' : review.sentiment < 0 ? 'Négatif' : 'Neutre' }} </UBadge>
            </div>
        </div>
    </UCard>
</template>

<script setup lang="ts">

const props = defineProps<{
    review: {
        id: number
        author: string
        avatar?: string
        date: string
        rating: number
        text: string
        neighbourhood: string
        sentiment?: number
    }
}>()
</script>

<style scoped>
.UCard {
    animation: fadeInUp 0.5s cubic-bezier(.39, .575, .565, 1.000);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 30px, 0);
    }

    to {
        opacity: 1;
        transform: none;
    }
}
</style>