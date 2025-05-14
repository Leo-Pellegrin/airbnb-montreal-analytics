<template>
  <div class="h-full">
    <canvas ref="canvas" class="w-full h-full" aria-label="Graphique de tendance"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

interface DataPoint {
  date: string
  value: number
  compareValue: number
}

const props = defineProps<{
  data: DataPoint[]
  loading: boolean
}>()

const canvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: import('chart.js').Chart<keyof import('chart.js').ChartTypeRegistry> | null = null

function destroyChart() {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
}

onMounted(async () => {
  if (!canvas.value || !props.data.length) return

  try {
    // import dynamique de Chart.js
    const { Chart, registerables } = await import('chart.js')
    // enregistrer tous les controllers, éléments, plugins, etc.
    Chart.register(...registerables)

    const ctx = canvas.value.getContext('2d')
    if (!ctx) return

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: props.data.map(d => d.date),
        datasets: [
          {
            label: 'Cette période',
            data: props.data.map(d => d.value),
            borderColor: '#4F46E5',
            backgroundColor: 'rgba(79, 70, 229, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 2,
            borderWidth: 2
          },
          {
            label: 'Période précédente',
            data: props.data.map(d => d.compareValue),
            borderColor: '#D1D5DB',
            backgroundColor: 'rgba(209, 213, 219, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 0,
            borderWidth: 1.5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              label(context) {
                // exemple : "Cette période: 43.5%"
                const value = context.parsed.y
                return `${context.dataset.label}: ${value}%`
              }
            }
          }
        },
        scales: {
          x: {
            display: false,
            grid: { display: false }
          },
          y: {
            display: false,
            grid: { display: false },
            min: 0
          }
        }
      }
    })
  } catch (err) {
    console.error('Erreur lors du chargement de Chart.js:', err)
  }
})

watch(
  () => props.data,
  (newData) => {
    if (chartInstance && newData.length) {
      chartInstance.data.labels = newData.map(d => d.date)
      chartInstance.data.datasets[0].data = newData.map(d => d.value)
      chartInstance.data.datasets[1].data = newData.map(d => d.compareValue)
      chartInstance.update()
    }
  }
)

onBeforeUnmount(() => {
  destroyChart()
})
</script>