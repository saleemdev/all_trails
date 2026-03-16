<script setup lang="ts">
import { computed } from 'vue'
import type { TrailWeather } from '../../../types'

const props = defineProps<{
  weather: TrailWeather | null
  loading?: boolean
  compact?: boolean
}>()

const weatherRiskPillClass = computed(() => {
  const risk = props.weather?.risk_level
  if (risk === 'good') return 'info-pill info-pill--risk-good'
  if (risk === 'caution') return 'info-pill info-pill--risk-caution'
  if (risk === 'risky') return 'info-pill info-pill--risk-risky'
  return 'soft-badge soft-badge--neutral'
})

const weatherSunrise = computed(() =>
  props.weather?.sunrise
    ? new Date(props.weather.sunrise).toLocaleTimeString('en-KE', { hour: '2-digit', minute: '2-digit' })
    : null
)

const weatherSunset = computed(() =>
  props.weather?.sunset
    ? new Date(props.weather.sunset).toLocaleTimeString('en-KE', { hour: '2-digit', minute: '2-digit' })
    : null
)

const metrics = computed(() => {
  if (!props.weather?.available) {
    return []
  }

  return [
    {
      label: 'Temperature',
      value:
        props.weather.temperature_min_c !== undefined && props.weather.temperature_max_c !== undefined
          ? `${props.weather.temperature_min_c}° - ${props.weather.temperature_max_c}°C`
          : 'Unavailable',
    },
    {
      label: 'Rain chance',
      value:
        props.weather.precipitation_probability_max !== undefined
          ? `${props.weather.precipitation_probability_max}%`
          : 'Unavailable',
    },
    {
      label: 'Wind gusts',
      value:
        props.weather.wind_gusts_10m_max_kmh !== undefined
          ? `${props.weather.wind_gusts_10m_max_kmh} km/h`
          : 'Unavailable',
    },
    {
      label: 'UV index',
      value: props.weather.uv_index_max !== undefined ? String(props.weather.uv_index_max) : 'Unavailable',
    },
    ...(weatherSunrise.value ? [{ label: 'Sunrise', value: weatherSunrise.value }] : []),
    ...(weatherSunset.value ? [{ label: 'Sunset', value: weatherSunset.value }] : []),
  ]
})
</script>

<template>
  <section class="weather-highlight rounded-[1.6rem] overflow-hidden text-white" :class="{ 'weather-highlight--compact': compact }">
    <div class="weather-highlight__glow weather-highlight__glow--one"></div>
    <div class="weather-highlight__glow weather-highlight__glow--two"></div>
    <div class="relative z-10 p-5 sm:p-6 lg:p-7">
      <div class="flex items-start justify-between gap-4 flex-wrap mb-4">
        <div>
          <p class="soft-kicker mb-3">Weather outlook</p>
          <h2 class="text-[clamp(1.55rem,3vw,2.3rem)] font-display font-semibold leading-[1.05] tracking-[-0.03em] mb-2">
            Trail day weather
          </h2>
          <p v-if="loading" class="text-white/80 text-sm mb-0">Checking the latest forecast...</p>
          <p v-else-if="weather?.available" class="text-white/85 text-base mb-0">
            {{ weather.summary || 'Forecast available for your trail day.' }}
          </p>
          <p v-else class="text-white/80 text-sm mb-0">
            {{ weather?.message || 'Weather forecast is unavailable right now.' }}
          </p>
        </div>
        <span v-if="weather?.available" :class="weatherRiskPillClass">
          {{ weather.risk_label || 'Weather' }}
        </span>
      </div>

      <div v-if="loading" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div v-for="item in 4" :key="item" class="weather-metric animate-pulse">
          <div class="h-3 w-20 rounded bg-white/15 mb-3"></div>
          <div class="h-6 w-24 rounded bg-white/20"></div>
        </div>
      </div>

      <div v-else-if="weather?.available" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <article v-for="metric in metrics" :key="metric.label" class="weather-metric">
          <p class="weather-metric__label">{{ metric.label }}</p>
          <p class="weather-metric__value">{{ metric.value }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.weather-highlight {
  position: relative;
  background:
    radial-gradient(circle at top left, rgba(143, 200, 255, 0.28), transparent 36%),
    radial-gradient(circle at bottom right, rgba(255, 255, 255, 0.14), transparent 32%),
    linear-gradient(135deg, #103247 0%, #1f5468 42%, #315348 100%);
  box-shadow: 0 24px 60px rgba(16, 50, 71, 0.2);
}

.weather-highlight--compact {
  border-radius: 1.35rem;
}

.weather-highlight__glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(42px);
  opacity: 0.28;
}

.weather-highlight__glow--one {
  width: 12rem;
  height: 12rem;
  top: -3rem;
  right: -2rem;
  background: rgba(255, 255, 255, 0.28);
}

.weather-highlight__glow--two {
  width: 10rem;
  height: 10rem;
  bottom: -2rem;
  left: -2rem;
  background: rgba(126, 214, 255, 0.28);
}

.weather-metric {
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  padding: 1rem;
}

.weather-metric__label {
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.72);
  margin-bottom: 0.45rem;
}

.weather-metric__value {
  font-size: 1.15rem;
  font-weight: 600;
  color: white;
  margin: 0;
}
</style>
