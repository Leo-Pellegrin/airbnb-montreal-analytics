<template>
  <div style="height:30vh; width:72vw">
    <LMap ref="map" :zoom="zoom" :center="[45.5017, -73.5673]" :use-global-leaflet="false"
      :options="{ zoomControl: true }">
      <LTileLayer url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        attribution="&amp;copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors"
        layer-type="base" name="OpenStreetMap" />
      <LControl position="topright">
        <div class="legend">
          <h4>{{ selectedKPI }}</h4>
          <div v-for="(color, index) in colorScale" :key="index" class="legend-item">
            <span :style="{ backgroundColor: color }"></span>
            <span>{{ legendLabels[index] }}</span>
          </div>
        </div>
      </LControl>
      <LGeoJson v-if="geoJsonData" :geojson="geoJsonData" :options-style="styleFeature"
        :onEachFeature="onEachFeature" />
    </LMap>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const zoom = ref(11)
const selectedKPI = ref('Prix médian')
const map = ref(null)
const geoJsonData = ref(null)

const kpiData = {
  'Prix médian': [50, 75, 100, 125, 150, 175, 200],
  'Taux d\'occupation': [0.2, 0.4, 0.6, 0.8, 1.0],
  'Sentiment moyen': [-1, -0.5, 0, 0.5, 1]
}

const colorScale = computed(() => {
  const colors = ['#FFE5E5', '#FFB2B2', '#FF7F7F', '#FF4C4C', '#FF1919']
  return colors.slice(0, kpiData[selectedKPI.value].length - 1)
})

const legendLabels = computed(() => {
  const values = kpiData[selectedKPI.value]
  return values.slice(0, -1).map((v, i) => `${v}-${values[i + 1]}`)
})

const styleFeature = (feature) => {
  const value = feature.properties[selectedKPI.value]
  const colorIndex = kpiData[selectedKPI.value].findIndex(threshold => value < threshold)
  return {
    fillColor: colorScale.value[colorIndex] || '#FFF',
    weight: 1,
    opacity: 1,
    color: '#333',
    fillOpacity: 0.7
  }
}

const onEachFeature = (feature, layer) => {
  layer.bindPopup(`<b>${feature.properties.name}</b><br>${selectedKPI.value}: ${feature.properties[selectedKPI.value]}`)
}

const loadGeoJSON = async () => {
  geoJsonData.value = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: {
          name: 'Plateau-Mont-Royal',
          'Prix médian': 125,
          'Taux d\'occupation': 0.75,
          'Sentiment moyen': 0.4
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[[-73.59, 45.52], [-73.58, 45.52], [-73.58, 45.53], [-73.59, 45.53], [-73.59, 45.52]]]
        }
      },
      {
        type: 'Feature',
        properties: {
          name: 'Vieux-Montréal',
          'Prix médian': 150,
          'Taux d\'occupation': 0.85,
          'Sentiment moyen': 0.6
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[[-73.56, 45.50], [-73.55, 45.50], [-73.55, 45.51], [-73.56, 45.51], [-73.56, 45.50]]]
        }
      },
      {
        type: 'Feature',
        properties: {
          name: 'Côte-des-Neiges',
          'Prix médian': 100,
          'Taux d\'occupation': 0.65,
          'Sentiment moyen': 0.3
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[[-73.62, 45.49], [-73.61, 45.49], [-73.61, 45.50], [-73.62, 45.50], [-73.62, 45.49]]]
        }
      }
    ]
  }
}

onMounted(() => {
  loadGeoJSON()
})

</script>

<style scoped>
.legend {
  background: white;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

.legend h4 {
  margin: 0 0 5px;
  color: #333;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 2px;
}

.legend-item span:first-child {
  width: 20px;
  height: 20px;
  margin-right: 5px;
  display: inline-block;
}
</style>
