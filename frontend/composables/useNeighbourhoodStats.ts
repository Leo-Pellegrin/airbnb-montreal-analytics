import { ref } from 'vue'

const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

export function useNeighbourhoodStats() {
    const geoJsonData = ref(null)
    const minPrice = ref(0)
    const maxPrice = ref(0)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const colorScale = ['#FFE5E5', '#FFB2B2', '#FF7F7F', '#FF4C4C', '#FF1919']

    // Fonction pour obtenir la couleur selon le prix
    function getColor(value: number, min: number, max: number) {
        if (value === null || value === undefined) return '#FFF'
        const idx = Math.floor(((value - min) / (max - min)) * (colorScale.length - 1))
        return colorScale[Math.max(0, Math.min(idx, colorScale.length - 1))]
    }

    const loadGeoJSONAndStats = async () => {
        loading.value = true
        error.value = null
        try {
            // 1. Charger le geojson
            const response = await fetch('/neighbourhoods.geojson')
            const geojson = await response.json()

            // 2. Récupérer la liste des quartiers
            const features = geojson.features
            const neighs = features.map((f: any) => f.properties.neighbourhood)

            // 3. Appeler l'API pour chaque quartier (en parallèle)
            const stats = await Promise.all(
                neighs.map(async (neigh: string) => {
                    try {
                        if (neigh !== undefined) {
                            const res = await fetch(`${API_BASE}/api/v1/stats/${encodeURIComponent(neigh)}`)
                            if (!res.ok) return { neigh, medianPrice: null }
                            const data = await res.json()
                            return { neigh, medianPrice: data.median_price }
                        }
                    } catch {
                        return { neigh, medianPrice: null }
                    }
                })
            )

            // 4. Fusionner les prix dans le geojson
            let prices: number[] = []
            for (const feature of features) {
                const stat = stats.find(s => s && s.neigh === feature.properties.neighbourhood)
                feature.properties['Prix médian'] = stat ? stat.medianPrice : null
                prices.push(feature.properties['Prix médian'])
            }

            // 5. Trier les quartiers par prix médian décroissant
            features.sort((a: any, b: any) => (b.properties['Prix médian'] || 0) - (a.properties['Prix médian'] || 0))

            // 6. Calculer min/max pour le dégradé
            prices = prices.filter(p => typeof p === 'number')
            minPrice.value = Math.min(...prices)
            maxPrice.value = Math.max(...prices)

            geoJsonData.value = geojson
        } catch (e: any) {
            error.value = e.message || 'Erreur lors du chargement des données'
        } finally {
            loading.value = false
        }
    }

    return {
        geoJsonData,
        minPrice,
        maxPrice,
        colorScale,
        getColor,
        loadGeoJSONAndStats,
        loading,
        error
    }
}
