<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { Trail } from '../../../types/index'

const props = defineProps<{
  trails: Trail[]
}>()

const emit = defineEmits<{
  trailClick: [trail: Trail]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
let map: L.Map | null = null
let markers: L.Marker[] = []

// Default to Kenya center if no trails
const defaultCenter: [number, number] = [-0.0236, 37.9062] // Kenya center

const hasValidCoordinates = (trail: Trail): boolean => {
  const lat = trail.coordinates?.lat
  const lng = trail.coordinates?.lng
  return typeof lat === 'number' && typeof lng === 'number' && Number.isFinite(lat) && Number.isFinite(lng)
}

const escapeHtml = (value: unknown): string => {
  const text = String(value ?? '')
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

const getDifficultyColor = (difficulty: string): string => {
  const colors: Record<string, string> = {
    'Easy': '#22c55e',      // green
    'Moderate': '#eab308',   // yellow
    'Hard': '#f97316',       // orange
    'Expert': '#ef4444'      // red
  }
  return colors[difficulty] || '#6b7280'
}

const createCustomIcon = (difficulty: string) => {
  const color = getDifficultyColor(difficulty)
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      "></div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 24],
    popupAnchor: [0, -24]
  })
}

const initializeMap = () => {
  if (!mapContainer.value) return

  // Initialize map centered on Kenya
  map = L.map(mapContainer.value, {
    center: defaultCenter,
    zoom: 6,
    zoomControl: true,
  })

  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map)

  // Add markers for trails
  updateMarkers()
}

const updateMarkers = () => {
  if (!map) return

  // Clear existing markers
  markers.forEach(marker => marker.remove())
  markers = []

  // Add markers for trails with coordinates
  const trailsWithCoords = props.trails.filter(hasValidCoordinates)
  
  if (trailsWithCoords.length === 0) return

  // Fit map to show all markers
  const bounds: L.LatLngBoundsExpression = trailsWithCoords.map(trail => [
    trail.coordinates!.lat,
    trail.coordinates!.lng
  ])

  trailsWithCoords.forEach(trail => {
    const { lat, lng } = trail.coordinates!
    const marker = L.marker([lat, lng], {
      icon: createCustomIcon(trail.difficulty_level)
    }).addTo(map!)

    // Create popup content
    const popupContent = `
      <div style="min-width: 200px; padding: 8px;">
        <h3 style="margin: 0 0 8px 0; font-weight: bold; color: #1f2937;">${escapeHtml(trail.title)}</h3>
        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">📍 ${escapeHtml(trail.location)}</p>
        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">📅 ${escapeHtml(new Date(trail.scheduled_date).toLocaleDateString())}</p>
        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">⏰ ${escapeHtml(trail.start_time)}</p>
        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">💰 ${new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', minimumFractionDigits: 0 }).format(trail.price_kshs)}</p>
        <p style="margin: 4px 0; color: #6b7280; font-size: 14px;">👥 ${trail.available_spots} spots available</p>
        <button 
          data-role="view-trail-details"
          class="trail-map-popup-button"
          style="
            margin-top: 8px;
            padding: 6px 12px;
            background-color: #10b981;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            width: 100%;
          "
        >
          View Details
        </button>
      </div>
    `

    marker.bindPopup(popupContent)
    marker.on('popupopen', () => {
      const popupContainer = marker.getPopup()?.getElement()
      const button = popupContainer?.querySelector('.trail-map-popup-button[data-role="view-trail-details"]')
      if (button) {
        button.addEventListener('click', () => {
          emit('trailClick', trail)
          map?.closePopup()
        })
      }
    })
    markers.push(marker)
  })

  // Fit map to show all markers with padding
  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [50, 50] })
  }
}

onMounted(() => {
  initializeMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
  markers = []
})

// Update markers when trails change
watch(() => props.trails, () => {
  if (map) {
    updateMarkers()
  }
})
</script>

<template>
  <div class="trail-map-container">
    <div ref="mapContainer" class="map" style="height: 600px; width: 100%; border-radius: 1rem; overflow: hidden;"></div>
    <div v-if="trails.filter(hasValidCoordinates).length === 0" class="map-empty-state">
      <p class="text-gray-500">No trails with location data available</p>
    </div>
  </div>
</template>

<style scoped>
.trail-map-container {
  position: relative;
  width: 100%;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.map {
  z-index: 0;
}

.map-empty-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background: white;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Fix Leaflet marker icon issue */
:deep(.leaflet-container) {
  font-family: inherit;
}

:deep(.custom-marker) {
  background: transparent;
  border: none;
}
</style>
