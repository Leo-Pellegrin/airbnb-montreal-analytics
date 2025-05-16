<template>
  <UCard class="hover:scale-105 hover:shadow-2xl transition-transform duration-200 cursor-pointer group">
    <div class="p-4 space-y-2">
      <div class="flex items-center gap-3 mb-2">
        <img v-if="image" :src="image" :alt="name" class="w-14 h-14 rounded-lg object-cover shadow-md border" />
        <div>
          <h2 class="text-lg font-semibold">{{ name }}</h2>
          <div class="text-xs text-gray-400">{{ description }}</div>
        </div>
        <span v-if="trend" :class="[
          'ml-auto flex items-center px-2 py-1 rounded-full text-xs font-bold',
          trend === 'up' ? 'bg-green-100 text-green-700' : trend === 'down' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-500'
        ]">
          <span v-if="trend === 'up'">▲</span>
          <span v-else-if="trend === 'down'">▼</span>
          <span v-else>•</span>
        </span>
      </div>
      <div class="text-sm text-gray-600">Prix médian : <strong>{{ typeof medianPrice === 'number' ? medianPrice : '-' }}
          $</strong></div>
      <div class="text-sm text-gray-600">Occ. : <strong>{{ typeof occupancy === 'number' ? occupancy.toFixed(0) : '-' }}
          %</strong></div>
      <div class="text-sm text-gray-600">
        Sentiment :
        <span :class="[
          'inline-block px-2 py-1 rounded-full text-xs font-bold',
          avg_sentiment > 4 ? 'bg-green-100 text-green-700' : avg_sentiment > 3 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
        ]">
          {{ typeof avg_sentiment === 'number' ? avg_sentiment.toFixed(2) : '-' }}
        </span>
      </div>
      <!-- Sparkline minimaliste en SVG ou Canvas -->
      <div class="mt-2">
        <!-- <Sparkline :data="history" /> -->
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// import Sparkline from '@/components/Sparkline.vue'

interface Props {
  name: string
  medianPrice: number
  occupancy: number
  avg_sentiment: number
  trend?: 'up' | 'down' | 'stable'
  description?: string
  image?: string
}
const props = defineProps<Props>()

// Historique condensé pour la mini‐courbe
const history = ref<number[]>([])

async function loadHistory() {
  // Pour la démo, on ne charge pas l'historique
  // const res = await fetch(`/api/v1/stats/${encodeURIComponent(props.name)}/history`)
  // const rows = await res.json()
  // history.value = rows.map((r: any) => r.median_price)
}

onMounted(loadHistory)
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