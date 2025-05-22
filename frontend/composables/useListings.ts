import { ref } from 'vue'

export function useListings() {
    const listings = ref<any[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    const config = useRuntimeConfig()
    const API_BASE = config.public.apiBase

    const fetchListings = async () => {
        loading.value = true
        error.value = null
        try {
            const { data, error: fetchError } = await useFetch(`${API_BASE}/api/v1/listings`)
            if (fetchError.value) throw fetchError.value
            listings.value = Array.isArray(data.value) ? data.value : []
            console.log("listings", listings.value)
        } catch (e: any) {
            error.value = e.message || 'Erreur lors du chargement des listings'
        } finally {
            loading.value = false
        }
    }

    return {
        listings,
        loading,
        error,
        fetchListings
    }
} 