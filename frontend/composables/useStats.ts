import { ref } from 'vue'

const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

interface Stats {
    medianPrice: number | null
    occupancyPct: number | null
    avgSentiment: number | null
    loading: boolean
    error: string | null
}

export const useStats = () => {
    const stats = ref<Stats>({
        medianPrice: null,
        occupancyPct: null,
        avgSentiment: null,
        loading: false,
        error: null
    })

    const fetchStats = async () => {
        stats.value.loading = true
        stats.value.error = null

        try {
            // Fetch median price
            const { data: medianPrice } = await useFetch<number>(`${API_BASE}/api/v1/stats/median_price`)
            if (typeof medianPrice.value !== 'number') throw new Error('Erreur lors de la récupération du prix médian')
            stats.value.medianPrice = medianPrice.value

            // Fetch occupancy percentage
            const { data: occupancy } = await useFetch<number>(`${API_BASE}/api/v1/stats/occupancy_pct`)
            if (!occupancy.value) throw new Error('Erreur lors de la récupération du taux d\'occupation')
            stats.value.occupancyPct = occupancy.value

            // Fetch average sentiment
            const { data: sentiment } = await useFetch<number>(`${API_BASE}/api/v1/stats/avg_sentiment`)                    
            if (typeof sentiment.value !== 'number') throw new Error('Erreur lors de la récupération du sentiment moyen')
            stats.value.avgSentiment = sentiment.value

        } catch (error) {
            stats.value.error = error instanceof Error ? error.message : 'Une erreur est survenue'
            console.error('Erreur lors de la récupération des statistiques:', error)
        } finally {
            stats.value.loading = false
        }
    }

    return {
        stats,
        fetchStats
    }
} 