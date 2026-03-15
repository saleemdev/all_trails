import axios from 'axios'
import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'
import type {
  BlogComment,
  BlogPost,
  BlogPostInput,
  BookingPaymentStatusResponse,
  MpesaPaymentInitiation,
  MpesaPaymentRequest,
  MpesaPaymentState,
  PaginatedResponse,
  RegisterMemberPayload,
  RegisterMemberResponse,
  Trail,
  TrailBooking,
  TrailFilters,
  User,
} from '../types/index'

class ApiService {
  private axiosInstance: AxiosInstance
  private currentUserRequest: Promise<User | null> | null = null

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: '/api/method',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      withCredentials: true,
    })

    this.axiosInstance.interceptors.request.use((config) => {
      const token = this.getCsrfToken()
      if (token) {
        config.headers['X-Frappe-CSRF-Token'] = token
      }
      return config
    })

    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError<any>) => {
        const status = error.response?.status || 0
        const message =
          error.response?.data?.message ||
          error.response?.data?._server_messages ||
          error.message ||
          'Request failed'

        if (status === 401) {
          window.dispatchEvent(new CustomEvent('session-expired', { detail: { status: 401 } }))
        } else if (status === 403) {
          window.dispatchEvent(new CustomEvent('permission-denied', { detail: { status: 403 } }))
        }

        return Promise.reject({ status, message, data: error.response?.data })
      }
    )
  }

  private getCsrfToken(): string {
    return (window as any).csrf_token || ''
  }

  private extractData<T>(response: AxiosResponse<any>): T {
    if (response.data && response.data.message !== undefined) {
      return response.data.message as T
    }
    return response.data as T
  }

  private generateIdempotencyKey(prefix: string): string {
    const randomPart = Math.random().toString(36).slice(2, 12)
    return `${prefix}-${Date.now()}-${randomPart}`
  }

  private normalizeTrail(raw: any): Trail {
    const activities = Array.isArray(raw?.extra_activities)
      ? raw.extra_activities.map((activity: any) => ({
          id: activity.id || activity.activity_id || activity.name,
          name: activity.name || activity.activity_name || 'Activity',
          description: activity.description || '',
          price_kshs: Number(activity.price_kshs ?? activity.price ?? 0),
          icon: activity.icon || undefined,
          available: Boolean(activity.available),
          requires_booking: Boolean(activity.requires_booking),
          max_participants:
            activity.max_participants === null || activity.max_participants === undefined
              ? undefined
              : Number(activity.max_participants),
          available_spots:
            activity.available_spots === null || activity.available_spots === undefined
              ? undefined
              : Number(activity.available_spots),
        }))
      : []

    return {
      id: raw.id || raw.name,
      title: raw.title || '',
      description: raw.description || '',
      difficulty_level: raw.difficulty_level || 'Moderate',
      location: raw.location || '',
      distance_km: Number(raw.distance_km || 0),
      elevation_gain_m: Number(raw.elevation_gain_m || 0),
      duration_hours: Number(raw.duration_hours || 0),
      scheduled_date: raw.scheduled_date || '',
      start_time: raw.start_time || '',
      end_time: raw.end_time || '',
      max_capacity: Number(raw.max_capacity || 0),
      available_spots: Number(raw.available_spots || 0),
      price_kshs: Number(raw.price_kshs || 0),
      host: raw.host || '',
      featured_image: raw.featured_image || undefined,
      route_geojson: raw.route_geojson || undefined,
      status: raw.status || 'Active',
      extra_activities: activities,
      is_long_weekend: Boolean(raw.is_long_weekend),
      created_at: raw.created_at || raw.creation || '',
      updated_at: raw.updated_at || raw.modified || '',
    }
  }

  private normalizeBooking(raw: any): TrailBooking {
    const activities = Array.isArray(raw?.selected_activities)
      ? raw.selected_activities.map((activity: any) => ({
          activity_id: activity.activity_id,
          activity_name: activity.activity_name,
          quantity: Number(activity.quantity || 0),
          price: Number(activity.price || activity.unit_price || 0),
          total_price: Number(activity.total_price || 0),
        }))
      : []

    return {
      id: raw.id || raw.name,
      user: raw.user,
      trail_id: raw.trail_id || raw.trail,
      booking_date: raw.booking_date,
      status: raw.status,
      spots_booked: Number(raw.spots_booked || 0),
      base_price: Number(raw.base_price || 0),
      activities_price: Number(raw.activities_price || 0),
      total_price: Number(raw.total_price || 0),
      payment_status: raw.payment_status || 'Pending',
      payment: raw.payment || null,
      payment_ticket: raw.payment_ticket || null,
      payment_method: raw.payment_method || undefined,
      payment_attempt_count: Number(raw.payment_attempt_count || 0),
      last_payment_attempt_on: raw.last_payment_attempt_on || null,
      mpesa_receipt_number: raw.mpesa_receipt_number || undefined,
      mpesa_phone_number: raw.mpesa_phone_number || undefined,
      mpesa_transaction_id: raw.mpesa_transaction_id || undefined,
      confirmation_code: raw.confirmation_code,
      cancellation_reason: raw.cancellation_reason || undefined,
      cancellation_date: raw.cancellation_date || raw.cancelled_on || undefined,
      completed_on: raw.completed_on || undefined,
      trail_title: raw.trail_title || undefined,
      trail_location: raw.trail_location || undefined,
      trail_scheduled_date: raw.trail_scheduled_date || undefined,
      selected_activities: activities,
      created_at: raw.created_at || raw.creation || '',
      updated_at: raw.updated_at || raw.modified || '',
    }
  }

  private normalizeBlogPost(raw: any): BlogPost {
    return {
      id: raw.id || raw.name,
      title: raw.title || '',
      slug: raw.slug || '',
      excerpt: raw.excerpt || '',
      content: raw.content || '',
      featured_image: raw.featured_image || undefined,
      author: raw.author || raw.owner || 'All Trails',
      author_image: raw.author_image || undefined,
      category: raw.category || 'Trail Stories',
      tags: Array.isArray(raw.tags) ? raw.tags : [],
      published_date: raw.published_date || raw.creation || raw.created_at || '',
      read_time: Number(raw.read_time || 1),
      status: raw.status === 'Draft' ? 'Draft' : 'Published',
      created_at: raw.created_at || raw.creation || '',
      updated_at: raw.updated_at || raw.modified || '',
    }
  }

  private normalizePaymentState(raw: any): MpesaPaymentState {
    return {
      payment_id: raw.payment_id,
      status: raw.status || 'Pending',
      paid: Boolean(raw.paid),
      failed: Boolean(raw.failed),
      is_terminal: Boolean(raw.is_terminal),
      message: raw.message || raw.status || 'Pending',
      checkout_request_id: raw.checkout_request_id || undefined,
      merchant_request_id: raw.merchant_request_id || undefined,
      ticket_id: raw.ticket_id || undefined,
      ticket_status: raw.ticket_status || undefined,
      receipt_number: raw.receipt_number || undefined,
      provider_transaction_id: raw.provider_transaction_id || undefined,
      provider_status_code: raw.provider_status_code || undefined,
      provider_status_message: raw.provider_status_message || undefined,
      failure_reason: raw.failure_reason || undefined,
      amount: Number(raw.amount || 0),
      phone_number: raw.phone_number || '',
      reference_name: raw.reference_name || '',
      reference_doctype: raw.reference_doctype || undefined,
      payment_journey: raw.payment_journey || 'Generic',
      paid_on: raw.paid_on || undefined,
      callback_received_on: raw.callback_received_on || undefined,
      attempt_no: Number(raw.attempt_no || 0),
      stale_callback_count: Number(raw.stale_callback_count || 0),
      attempt_history: Array.isArray(raw.attempt_history)
        ? raw.attempt_history.map((attempt: any) => ({
            attempt_no: Number(attempt.attempt_no || 0),
            initiated_at: attempt.initiated_at || undefined,
            checkout_request_id: attempt.checkout_request_id || undefined,
            merchant_request_id: attempt.merchant_request_id || undefined,
            status_after_callback: attempt.status_after_callback || undefined,
            callback_received_on: attempt.callback_received_on || undefined,
          }))
        : [],
    }
  }

  async registerMember(payload: RegisterMemberPayload): Promise<RegisterMemberResponse> {
    const response = await this.axiosInstance.post('/all_trails.api.register_member', payload)
    return this.extractData<RegisterMemberResponse>(response)
  }

  async getTrails(filters?: TrailFilters, page = 1, pageSize = 10): Promise<PaginatedResponse<Trail>> {
    const response = await this.axiosInstance.get('/all_trails.api.get_trails', {
      params: {
        filters: filters ? JSON.stringify(filters) : undefined,
        page,
        page_size: pageSize,
      },
    })

    const payload = this.extractData<PaginatedResponse<any>>(response)
    return {
      data: (payload.data || []).map((trail: any) => this.normalizeTrail(trail)),
      total: Number(payload.total || 0),
      page: Number(payload.page || page),
      page_size: Number(payload.page_size || pageSize),
    }
  }

  async getTrailById(trailId: string): Promise<Trail> {
    const response = await this.axiosInstance.get('/all_trails.api.get_trail_detail', {
      params: { trail_id: trailId },
    })
    return this.normalizeTrail(this.extractData<any>(response))
  }

  async createBooking(
    trailId: string,
    spotsBooked: number,
    selectedActivities?: Array<{
      activity_id: string
      activity_name: string
      quantity: number
      price: number
    }>
  ): Promise<TrailBooking> {
    const response = await this.axiosInstance.post('/all_trails.api.create_booking', {
      trail_id: trailId,
      spots_booked: spotsBooked,
      selected_activities: (selectedActivities || []).map((activity) => ({
        activity_id: activity.activity_id,
        quantity: activity.quantity,
      })),
      idempotency_key: this.generateIdempotencyKey('booking'),
    })

    return this.normalizeBooking(this.extractData<any>(response))
  }

  async getUserBookings(status?: string): Promise<TrailBooking[]> {
    const response = await this.axiosInstance.get('/all_trails.api.get_user_bookings', {
      params: { status },
    })

    const payload = this.extractData<any[]>(response)
    return (payload || []).map((booking) => this.normalizeBooking(booking))
  }

  async getBookingById(bookingId: string): Promise<TrailBooking> {
    const response = await this.axiosInstance.get('/all_trails.api.get_booking_detail', {
      params: { booking_id: bookingId },
    })

    return this.normalizeBooking(this.extractData<any>(response))
  }

  async cancelBooking(bookingId: string, reason: string): Promise<{ success: boolean; booking?: TrailBooking }> {
    const response = await this.axiosInstance.post('/all_trails.api.cancel_booking', {
      booking_id: bookingId,
      reason,
    })

    const payload = this.extractData<any>(response)
    return {
      success: Boolean(payload.success),
      booking: payload.booking ? this.normalizeBooking(payload.booking) : undefined,
    }
  }

  async initiateBookingPayment(
    bookingId: string,
    phoneNumber: string
  ): Promise<(MpesaPaymentInitiation & { booking: TrailBooking; payment?: MpesaPaymentState })> {
    const response = await this.axiosInstance.post('/all_trails.api.initiate_booking_payment', {
      booking_id: bookingId,
      phone_number: phoneNumber,
      idempotency_key: this.generateIdempotencyKey('booking-payment'),
    })

    const payload = this.extractData<any>(response)
    return {
      ...(payload as MpesaPaymentInitiation),
      booking: this.normalizeBooking(payload.booking),
      payment: payload.payment ? this.normalizePaymentState(payload.payment) : undefined,
    }
  }

  async getBookingPaymentStatus(bookingId: string): Promise<BookingPaymentStatusResponse> {
    const response = await this.axiosInstance.get('/all_trails.api.get_booking_payment_status', {
      params: { booking_id: bookingId },
    })

    const payload = this.extractData<any>(response)
    return {
      booking: this.normalizeBooking(payload.booking),
      payment: this.normalizePaymentState(payload.payment),
    }
  }

  async initiateMpesaPayment(
    requestOrReferenceName: MpesaPaymentRequest | string,
    phoneNumber?: string,
    amount?: number
  ): Promise<MpesaPaymentInitiation> {
    const request: MpesaPaymentRequest =
      typeof requestOrReferenceName === 'string'
        ? {
            journey_type: 'Trail Booking',
            reference_name: requestOrReferenceName,
            reference_doctype: 'Trail Booking',
            phone_number: phoneNumber || '',
            amount: Number(amount || 0),
            metadata: {},
          }
        : requestOrReferenceName

    const response = await this.axiosInstance.post('/all_trails.api.initiate_mpesa_payment', {
      journey_type: request.journey_type,
      reference_name: request.reference_name,
      reference_doctype: request.reference_doctype,
      phone_number: request.phone_number,
      amount: request.amount,
      company: request.company,
      metadata: request.metadata || {},
      idempotency_key: this.generateIdempotencyKey('mpesa'),
    })

    return this.extractData<MpesaPaymentInitiation>(response)
  }

  async getMpesaPaymentStatus(paymentId: string): Promise<MpesaPaymentState> {
    const response = await this.axiosInstance.get('/all_trails.api.get_mpesa_payment_status', {
      params: { payment_id: paymentId },
    })

    return this.normalizePaymentState(this.extractData<any>(response))
  }

  async getBlogPosts(search?: string, page = 1, pageSize = 12): Promise<PaginatedResponse<BlogPost>> {
    const response = await this.axiosInstance.get('/all_trails.api.get_blog_posts', {
      params: {
        search: search || undefined,
        page,
        page_size: pageSize,
      },
    })

    const payload = this.extractData<PaginatedResponse<any>>(response)
    return {
      data: (payload.data || []).map((post: any) => this.normalizeBlogPost(post)),
      total: Number(payload.total || 0),
      page: Number(payload.page || page),
      page_size: Number(payload.page_size || pageSize),
    }
  }

  async getBlogPost(slug: string): Promise<BlogPost> {
    const response = await this.axiosInstance.get('/all_trails.api.get_blog_post', {
      params: { slug },
    })

    return this.normalizeBlogPost(this.extractData<any>(response))
  }

  async createBlogPost(payload: BlogPostInput): Promise<BlogPost> {
    const response = await this.axiosInstance.post('/all_trails.api.create_blog_post', {
      title: payload.title,
      content: payload.content,
      slug: payload.slug,
      excerpt: payload.excerpt,
      featured_image: payload.featured_image,
      published: payload.published ?? 1,
    })

    return this.normalizeBlogPost(this.extractData<any>(response))
  }

  async getBlogComments(slug: string, page = 1, pageSize = 20): Promise<PaginatedResponse<BlogComment>> {
    const response = await this.axiosInstance.get('/all_trails.api.get_blog_comments', {
      params: {
        slug,
        page,
        page_size: pageSize,
      },
    })

    const payload = this.extractData<PaginatedResponse<any>>(response)
    return {
      data: (payload.data || []).map((comment: any) => ({
        id: comment.id || comment.name,
        author: comment.author || comment.comment_by || 'Guest',
        email: comment.email || comment.comment_email || undefined,
        content: comment.content || '',
        created_at: comment.created_at || comment.creation || '',
      })),
      total: Number(payload.total || 0),
      page: Number(payload.page || page),
      page_size: Number(payload.page_size || pageSize),
    }
  }

  async createBlogComment(payload: {
    slug: string
    content: string
    comment_by?: string
    comment_email?: string
  }): Promise<{ success: boolean; message: string; comment_id: string; published: number }> {
    const response = await this.axiosInstance.post('/all_trails.api.create_blog_comment', payload)
    return this.extractData<{ success: boolean; message: string; comment_id: string; published: number }>(response)
  }

  async submitTrailFeedback(payload: {
    trail_id: string
    rating: number
    feedback_text: string
    title?: string
    booking_id?: string
  }): Promise<{ success: boolean; message: string; feedback_id: string }> {
    const response = await this.axiosInstance.post('/all_trails.api.submit_trail_feedback', payload)
    return this.extractData<{ success: boolean; message: string; feedback_id: string }>(response)
  }

  async getTrailFeedback(trailId: string, page = 1, pageSize = 10): Promise<PaginatedResponse<any>> {
    const response = await this.axiosInstance.get('/all_trails.api.get_trail_feedback', {
      params: {
        trail_id: trailId,
        page,
        page_size: pageSize,
      },
    })

    return this.extractData<PaginatedResponse<any>>(response)
  }

  async getCurrentUser(): Promise<User | null> {
    if (this.currentUserRequest) {
      return this.currentUserRequest
    }

    this.currentUserRequest = (async () => {
      try {
        const authResponse = await axios.get('/api/method/frappe.auth.get_logged_user', {
          headers: {
            'X-Frappe-CSRF-Token': this.getCsrfToken(),
          },
          withCredentials: true,
        })

        const userName = authResponse.data?.message
        if (!userName || userName === 'Guest') {
          return null
        }

        const safeUserName = encodeURIComponent(userName)
        const userResponse = await axios.get(`/api/resource/User/${safeUserName}`, {
          headers: {
            'X-Frappe-CSRF-Token': this.getCsrfToken(),
          },
          withCredentials: true,
        })

        const userData = userResponse.data?.data || {}
        return {
          name: userName,
          email: userData.email || userName,
          full_name: userData.full_name || userName,
          user_image: userData.user_image || undefined,
        }
      } catch {
        return null
      }
    })()

    try {
      return await this.currentUserRequest
    } finally {
      this.currentUserRequest = null
    }
  }

  async getUserStats(): Promise<{ total_bookings: number; confirmed_bookings: number; completed_bookings: number; total_spent: number }> {
    const bookings = await this.getUserBookings()

    return {
      total_bookings: bookings.length,
      confirmed_bookings: bookings.filter((booking) => ['Confirmed', 'Pending'].includes(booking.status)).length,
      completed_bookings: bookings.filter((booking) => booking.status === 'Completed').length,
      total_spent: bookings
        .filter((booking) => ['Paid', 'Completed'].includes(booking.payment_status))
        .reduce((sum, booking) => sum + Number(booking.total_price || 0), 0),
    }
  }
}

export const apiService = new ApiService()
