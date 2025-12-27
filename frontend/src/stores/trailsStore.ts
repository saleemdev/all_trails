import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Trail, TrailFilters } from '../types/index';
import { apiService } from '../services/api';

export const useTrailsStore = defineStore('trails', () => {
  const trails = ref<Trail[]>([]);
  const selectedTrail = ref<Trail | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const totalTrails = ref(0);

  const filters = ref<TrailFilters>({
    search: '',
    difficulty_level: undefined,
    min_price: undefined,
    max_price: undefined,
  });

  const filteredTrails = computed(() => trails.value);

  const totalPages = computed(() => Math.ceil(totalTrails.value / pageSize.value));

  const fetchTrails = async (page: number = 1) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await apiService.getTrails(filters.value, page, pageSize.value);
      trails.value = response.data;
      totalTrails.value = response.total;
      currentPage.value = page;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch trails';
      console.error('Fetch trails error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchTrailById = async (trailId: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      selectedTrail.value = await apiService.getTrailById(trailId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch trail';
      console.error('Fetch trail error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const setFilters = (newFilters: Partial<TrailFilters>) => {
    filters.value = { ...filters.value, ...newFilters };
    currentPage.value = 1; // Reset to first page when filters change
  };

  const clearFilters = () => {
    filters.value = {
      search: '',
      difficulty_level: undefined,
      min_price: undefined,
      max_price: undefined,
    };
    currentPage.value = 1;
  };

  const setPage = (page: number) => {
    currentPage.value = page;
  };

  return {
    trails,
    selectedTrail,
    isLoading,
    error,
    filters,
    currentPage,
    pageSize,
    totalTrails,
    totalPages,
    filteredTrails,
    fetchTrails,
    fetchTrailById,
    setFilters,
    clearFilters,
    setPage,
  };
});

