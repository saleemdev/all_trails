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
        'Accept': 'application/json',
      },
      withCredentials: true, // Enable cookies for session management
    });

    // Request interceptor for CSRF token
    this.axiosInstance.interceptors.request.use(
      (config) => {
        // SECURITY: Validate CSRF token exists before making request
        if (!(window as any).csrf_token) {
          console.warn('[SECURITY] CSRF token is missing or undefined. Request may be rejected by server.');
        }

        // Add CSRF token if available
        if ((window as any).csrf_token) {
          config.headers['X-Frappe-CSRF-Token'] = (window as any).csrf_token;
        }

        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling and session expiry
    this.axiosInstance.interceptors.response.use(
      (response) => {
        // Frappe returns data in response.data.message for method calls
        if (response.data && response.data.message !== undefined) {
          return {
            ...response,
            data: response.data.message
          };
        }
        return response;
      },
      (error) => {
        // Handle common Frappe errors
        if (error.response) {
          const { status, data } = error.response;

          switch (status) {
            case 401:
              // SECURITY: Unauthorized - session expired or invalid
              console.error('[SECURITY] 401 Unauthorized - Session may have expired. User should re-authenticate.');
              // Dispatch event for app to handle re-authentication
              window.dispatchEvent(new CustomEvent('session-expired', { detail: { status: 401 } }));
              break;
            case 403:
              // SECURITY: Forbidden - user lacks permissions
              console.error('[SECURITY] 403 Forbidden - User lacks required permissions.');
              window.dispatchEvent(new CustomEvent('permission-denied', { detail: { status: 403 } }));
              break;
            case 404:
              // Not found
              break;
            case 500:
              // Server error
              break;
            default:
              // Handle error
          }

          // Return structured error
          return Promise.reject({
            status,
            message: data?.message || error.message,
            data: data
          });
        }

        // Network or other errors
        return Promise.reject({
          status: 0,
          message: error.message || 'Network error',
          data: null
        });
      }
    );
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

  async createBooking(
    trailId: string,
    spotsBooked: number,
    selectedActivities?: Array<{
      activity_id: string;
      activity_name: string;
      quantity: number;
      price: number;
    }>
  ): Promise<TrailBooking> {
    if (USE_MOCK_DATA) {
      return this.mockCreateBooking(trailId, spotsBooked, selectedActivities);
    }
    const response = await this.axiosInstance.post('/create_booking', {
      trail_id: trailId,
      spots_booked: spotsBooked,
      selected_activities: selectedActivities || []
    });
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

  async getCurrentUser(): Promise<User | null> {
    // Check if user has valid session cookies first
    const cookies = document.cookie.split(';').reduce((acc: Record<string, string>, cookie) => {
      const [key, value] = cookie.trim().split('=');
      acc[key] = value;
      return acc;
    }, {});

    // If no session cookies (sid or user_id), user is not logged in
    if (!cookies.sid && !cookies.user_id) {
      return null;
    }

    // If Frappe session data is available in window, use it
    if ((window as any).frappe?.session?.user && (window as any).frappe.session.user !== 'Guest') {
      return {
        name: (window as any).frappe.session.user,
        email: (window as any).frappe.session.user,
        full_name: (window as any).frappe.session.user_fullname || (window as any).frappe.session.user,
        user_image: (window as any).frappe.session.user_image || null
      };
    }

    // Try to fetch current user from Frappe API
    try {
      const response = await axios.get('/api/method/frappe.auth.get_logged_user', {
        headers: {
          'X-Frappe-CSRF-Token': (window as any).csrf_token || '',
        },
        withCredentials: true // Critical for cookie-based sessions
      });

      if (response.data && response.data.message && response.data.message !== 'Guest') {
        const userName = response.data.message;
        // Fetch full user details
        const userResponse = await axios.get(`/api/resource/User/${userName}`, {
          headers: {
            'X-Frappe-CSRF-Token': (window as any).csrf_token || '',
          },
          withCredentials: true // Critical for cookie-based sessions
        });

        const userData = userResponse.data?.data || {};
        return {
          name: userName,
          email: userData.email || userName,
          full_name: userData.full_name || userName,
          user_image: userData.user_image || null
        };
      } else {
        // User is Guest, not authenticated
        return null;
      }
    } catch (error) {
      console.error('Failed to fetch user session:', error);
      return null;
    }
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

  private mockCreateBooking(
    trailId: string,
    spotsBooked: number,
    selectedActivities?: Array<{
      activity_id: string;
      activity_name: string;
      quantity: number;
      price: number;
    }>
  ): TrailBooking {
    const trail = mockTrails.find(t => t.id === trailId);
    if (!trail) throw new Error(`Trail ${trailId} not found`);
    if (trail.available_spots < spotsBooked) throw new Error('Not enough spots available');

    // Calculate base price
    const basePrice = trail.price_kshs * spotsBooked;
    
    // Calculate activities price
    const activitiesPrice = selectedActivities?.reduce((sum, activity) => {
      return sum + (activity.price * activity.quantity);
    }, 0) || 0;

    const totalPrice = basePrice + activitiesPrice;

    const booking: TrailBooking = {
      id: `booking-${Date.now()}`,
      user: mockCurrentUser.name,
      trail_id: trailId,
      booking_date: new Date().toISOString(),
      status: 'Pending',
      spots_booked: spotsBooked,
      total_price: totalPrice,
      payment_status: 'Pending',
      confirmation_code: `CONF-${Math.random().toString(36).substring(7).toUpperCase()}`,
      trail_title: trail.title,
      trail_location: trail.location,
      trail_scheduled_date: trail.scheduled_date,
      selected_activities: selectedActivities || [],
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

