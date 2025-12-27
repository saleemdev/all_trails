import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type { Trail, TrailBooking, User, TrailFilters, PaginatedResponse } from '../types/index';
import { mockTrails, mockBookings, mockCurrentUser } from './mockData';

// Configuration flag for mock vs real API
const USE_MOCK_DATA = true; // Set to false when backend is ready

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: '/api/method/all_trails',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // ============ TRAILS ============

  async getTrails(filters?: TrailFilters, page: number = 1, pageSize: number = 10): Promise<PaginatedResponse<Trail>> {
    if (USE_MOCK_DATA) {
      return this.mockGetTrails(filters, page, pageSize);
    }
    const response = await this.axiosInstance.get('/get_trails', { 
      params: { 
        filters: filters ? JSON.stringify(filters) : undefined, 
        page, 
        page_size: pageSize 
      } 
    });
    return response.data.message || response.data;
  }

  async getTrailById(trailId: string): Promise<Trail> {
    if (USE_MOCK_DATA) {
      return this.mockGetTrailById(trailId);
    }
    const response = await this.axiosInstance.get(`/get_trail_detail?trail_id=${trailId}`);
    const trail = response.data.message || response.data;
    trail.id = trail.name || trail.id;
    return trail;
  }

  // ============ BOOKINGS ============

  async createBooking(trailId: string, spotsBooked: number): Promise<TrailBooking> {
    if (USE_MOCK_DATA) {
      return this.mockCreateBooking(trailId, spotsBooked);
    }
    const response = await this.axiosInstance.post('/create_booking', { trail_id: trailId, spots_booked: spotsBooked });
    const booking = response.data.message || response.data;
    booking.id = booking.name || booking.id;
    return booking;
  }

  async getUserBookings(status?: string): Promise<TrailBooking[]> {
    if (USE_MOCK_DATA) {
      return this.mockGetUserBookings(status);
    }
    const response = await this.axiosInstance.get('/get_user_bookings', { params: { status } });
    const bookings = response.data.message || response.data;
    return bookings.map((b: any) => ({ ...b, id: b.name || b.id }));
  }

  async getBookingById(bookingId: string): Promise<TrailBooking> {
    if (USE_MOCK_DATA) {
      return this.mockGetBookingById(bookingId);
    }
    const response = await this.axiosInstance.get(`/get_booking_detail?booking_id=${bookingId}`);
    const booking = response.data.message || response.data;
    booking.id = booking.name || booking.id;
    return booking;
  }

  async cancelBooking(bookingId: string, reason: string): Promise<{ success: boolean }> {
    if (USE_MOCK_DATA) {
      return this.mockCancelBooking(bookingId, reason);
    }
    const response = await this.axiosInstance.post('/cancel_booking', { booking_id: bookingId, reason });
    return response.data.message || response.data;
  }

  // MPESA Payment Methods
  async initiateMpesaPayment(bookingId: string, phoneNumber: string): Promise<any> {
    if (USE_MOCK_DATA) {
      return this.mockInitiateMpesaPayment(bookingId, phoneNumber);
    }
    const response = await this.axiosInstance.post('/initiate_mpesa_payment', {
      booking_id: bookingId,
      phone_number: phoneNumber
    });
    return response.data.message || response.data;
  }

  async confirmMpesaPayment(bookingId: string, receiptNumber: string, transactionId: string): Promise<any> {
    if (USE_MOCK_DATA) {
      return this.mockConfirmMpesaPayment(bookingId, receiptNumber, transactionId);
    }
    const response = await this.axiosInstance.post('/confirm_mpesa_payment', {
      booking_id: bookingId,
      receipt_number: receiptNumber,
      transaction_id: transactionId
    });
    return response.data.message || response.data;
  }

  // ============ USER ============

  async getCurrentUser(): Promise<User> {
    if (USE_MOCK_DATA) {
      return this.mockGetCurrentUser();
    }
    const response = await this.axiosInstance.get('/get_current_user');
    return response.data.message || response.data;
  }

  async getUserStats(): Promise<any> {
    if (USE_MOCK_DATA) {
      return {
        total_bookings: 5,
        confirmed_bookings: 3,
        completed_bookings: 2,
        total_spent: 15000
      };
    }
    const response = await this.axiosInstance.get('/get_user_stats');
    return response.data.message || response.data;
  }

  // ============ MOCK IMPLEMENTATIONS ============

  private mockGetTrails(filters?: TrailFilters, page: number = 1, pageSize: number = 10): PaginatedResponse<Trail> {
    let filtered = [...mockTrails];

    if (filters?.search) {
      const search = filters.search.toLowerCase();
      filtered = filtered.filter(t => t.title.toLowerCase().includes(search) || t.location.toLowerCase().includes(search));
    }

    if (filters?.difficulty_level) {
      filtered = filtered.filter(t => t.difficulty_level === filters.difficulty_level);
    }

    if (filters?.min_price) {
      filtered = filtered.filter(t => t.price_kshs >= filters.min_price!);
    }

    if (filters?.max_price) {
      filtered = filtered.filter(t => t.price_kshs <= filters.max_price!);
    }

    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    const paginated = filtered.slice(start, end);

    return {
      data: paginated,
      total: filtered.length,
      page,
      page_size: pageSize,
    };
  }

  private mockGetTrailById(trailId: string): Trail {
    const trail = mockTrails.find(t => t.id === trailId);
    if (!trail) throw new Error(`Trail ${trailId} not found`);
    return trail;
  }

  private mockCreateBooking(trailId: string, spotsBooked: number): TrailBooking {
    const trail = mockTrails.find(t => t.id === trailId);
    if (!trail) throw new Error(`Trail ${trailId} not found`);
    if (trail.available_spots < spotsBooked) throw new Error('Not enough spots available');

    const booking: TrailBooking = {
      id: `booking-${Date.now()}`,
      user: mockCurrentUser.name,
      trail_id: trailId,
      booking_date: new Date().toISOString(),
      status: 'Pending',
      spots_booked: spotsBooked,
      total_price: trail.price_kshs * spotsBooked,
      payment_status: 'Pending',
      confirmation_code: `CONF-${Math.random().toString(36).substring(7).toUpperCase()}`,
      trail_title: trail.title,
      trail_location: trail.location,
      trail_scheduled_date: trail.scheduled_date,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    // Add to mock bookings array
    mockBookings.push(booking);

    return booking;
  }

  private mockGetUserBookings(status?: string): TrailBooking[] {
    let bookings = mockBookings.filter(b => b.user === mockCurrentUser.name);
    if (status) {
      bookings = bookings.filter(b => b.status === status);
    }
    return bookings;
  }

  private mockGetBookingById(bookingId: string): TrailBooking {
    const booking = mockBookings.find(b => b.id === bookingId);
    if (!booking) throw new Error(`Booking ${bookingId} not found`);
    return booking;
  }

  private mockCancelBooking(bookingId: string, reason: string): { success: boolean } {
    const booking = mockBookings.find(b => b.id === bookingId);
    if (!booking) throw new Error(`Booking ${bookingId} not found`);
    booking.status = 'Cancelled';
    booking.cancellation_reason = reason;
    booking.cancellation_date = new Date().toISOString();
    return { success: true };
  }

  private mockGetCurrentUser(): User {
    return mockCurrentUser;
  }

  private mockInitiateMpesaPayment(_bookingId: string, phoneNumber: string): any {
    // Simulate payment initiation
    return {
      success: true,
      payment_request_id: `PR-${Date.now()}`,
      amount: 0, // Will be set by booking
      phone_number: phoneNumber,
      message: `Payment request created. Please complete MPESA payment.`
    };
  }

  private mockConfirmMpesaPayment(bookingId: string, receiptNumber: string, transactionId: string): any {
    // Update booking in mock data
    const booking = mockBookings.find(b => b.id === bookingId);
    if (booking) {
      booking.payment_status = 'Completed';
      booking.status = 'Confirmed';
      booking.mpesa_receipt_number = receiptNumber;
      booking.mpesa_transaction_id = transactionId;
      booking.payment_method = 'MPESA';
    }
    return {
      success: true,
      message: 'Payment confirmed successfully'
    };
  }
}

export const apiService = new ApiService();

