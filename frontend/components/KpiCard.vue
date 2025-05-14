<template>
    <UCard class="min-h-[80px] shadow-lg">
        <div class="flex items-center">
            <div class="flex items-center justify-center">
                <Icon :name="icon" class="w-6 h-6 mr-4 text-primary" aria-hidden="true" />
            </div>
            <div class="flex flex-col">
                <div class="mb-1">
                    <span class="font-circular text-primary font-bold">{{ label }}</span>
                </div>
                <div class="flex items-center">
                    <span v-if="showCurrencySymbol" class="font-circular font-bold text-2xl mr-1">CAD $</span>
                    <span class="font-circular font-bold text-2xl">{{ value }}</span>
                </div>
            </div>
        </div>
    </UCard>
</template>

<script setup lang="ts">
/**
 * KpiCard
 * Props :
 * - label (string, requis) - Le titre de la carte KPI
 * - value (string|number, requis) - La valeur à afficher
 * - showCurrencySymbol (boolean, optionnel) - Affiche le symbole $ avant la valeur
 */
import { computed } from 'vue'
const props = defineProps({
    label: { type: String, required: true },
    value: { type: [String, Number], required: true },
    showCurrencySymbol: { type: Boolean, default: false },
    icon: { type: String, required: true }
})
</script>