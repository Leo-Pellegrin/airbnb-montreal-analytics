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
            <span>
              {{ (minPrice + ((maxPrice - minPrice) * index / (colorScale.length - 1))).toFixed(0) }}
              -
              {{ (minPrice + ((maxPrice - minPrice) * (index + 1) / (colorScale.length - 1))).toFixed(0) }}
            </span>
          </div>
        </div>
      </LControl>
      <LGeoJson v-if="geoJsonData" :geojson="geoJsonData" :options-style="styleFeature"
        :onEachFeature="onEachFeature" />
    </LMap>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useNeighbourhoodStats } from '../composables/useNeighbourhoodStats'

const zoom = ref(11)
const selectedKPI = ref('Prix médian')

const {
  geoJsonData,
  minPrice,
  maxPrice,
  colorScale,
  getColor,
  loadGeoJSONAndStats,
  loading,
  error
} = useNeighbourhoodStats()

const styleFeature = (feature: any) => {
  const value = feature.properties[selectedKPI.value]
  return {
    fillColor: getColor(value, minPrice.value, maxPrice.value),
    weight: 1,
    opacity: 1,
    color: '#333',
    fillOpacity: 0.7
  }
}

const onEachFeature = (feature: any, layer: any) => {
  layer.bindPopup(`<b>${feature.properties.name}</b><br>${selectedKPI.value}: ${feature.properties[selectedKPI.value]}`)
}

onMounted(() => {
  loadGeoJSONAndStats()
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
