import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { TrailBooking } from '../types/index';
import { apiService } from '../services/api';

export const useBookingsStore = defineStore('bookings', () => {
  const bookings = ref<TrailBooking[]>([]);
  const selectedBooking = ref<TrailBooking | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const upcomingBookings = computed(() =>
    bookings.value.filter(b => b.status === 'Confirmed' || b.status === 'Pending')
  );

  const pastBookings = computed(() =>
    bookings.value.filter(b => b.status === 'Completed' || b.status === 'Cancelled')
  );

  const fetchUserBookings = async (status?: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      bookings.value = await apiService.getUserBookings(status);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch bookings';
      console.error('Fetch bookings error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchBookingById = async (bookingId: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      selectedBooking.value = await apiService.getBookingById(bookingId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch booking';
      console.error('Fetch booking error:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const createBooking = async (
    trailId: string,
    spotsBooked: number,
    selectedActivities?: Array<{
      activity_id: string;
      activity_name: string;
      quantity: number;
      price: number;
    }>
  ) => {
    isLoading.value = true;
    error.value = null;
    try {
      const newBooking = await apiService.createBooking(trailId, spotsBooked, selectedActivities);
      bookings.value.push(newBooking);
      return newBooking;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create booking';
      console.error('Create booking error:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const cancelBooking = async (bookingId: string, reason: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      await apiService.cancelBooking(bookingId, reason);
      const booking = bookings.value.find(b => b.id === bookingId);
      if (booking) {
        booking.status = 'Cancelled';
        booking.cancellation_reason = reason;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to cancel booking';
      console.error('Cancel booking error:', err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    bookings,
    selectedBooking,
    isLoading,
    error,
    upcomingBookings,
    pastBookings,
    fetchUserBookings,
    fetchBookingById,
    createBooking,
    cancelBooking,
  };
});

