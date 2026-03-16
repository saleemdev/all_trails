// Extra Activity Types
export interface ExtraActivity {
  id: string;
  name: string;
  description: string;
  price_kshs: number;
  icon?: string;
  available: boolean;
  requires_booking?: boolean; // Some activities might need separate booking
  max_participants?: number;
  available_spots?: number;
}

// Trail Types
export interface Trail {
  id: string;
  title: string;
  description: string;
  difficulty_level: 'Easy' | 'Moderate' | 'Hard' | 'Expert';
  trail_type?: 'Loop' | 'Out and Back' | 'Point to Point' | 'Summit Push' | 'Traverse';
  location: string;
  latitude?: number;
  longitude?: number;
  county?: string;
  coordinates?: { lat: number; lng: number };
  distance_km: number;
  elevation_gain_m: number;
  duration_hours: number;
  scheduled_date: string;
  start_time: string;
  end_time: string;
  meeting_point?: string;
  meeting_time?: string;
  meeting_notes?: string;
  meeting_point_maps_url?: string;
  terrain_summary?: string;
  trail_highlights?: string;
  altitude_start_m?: number;
  altitude_max_m?: number;
  fitness_level?: string;
  water_requirement_litres?: number;
  transport_notes?: string;
  packing_list?: string;
  safety_notes?: string;
  inclusions?: string;
  exclusions?: string;
  best_season?: string;
  max_capacity: number;
  available_spots: number;
  price_kshs: number;
  host: string;
  featured_image?: string;
  route_geojson?: string;
  status: 'Active' | 'Cancelled' | 'Completed';
  extra_activities?: ExtraActivity[]; // Optional extra activities
  is_long_weekend?: boolean; // Special flag for long weekend availability
  created_at: string;
  updated_at: string;
}

export interface TrailWeather {
  available: boolean;
  message?: string;
  date: string;
  summary?: string;
  weather_code?: number;
  risk_level?: 'good' | 'caution' | 'risky';
  risk_label?: string;
  temperature_max_c?: number;
  temperature_min_c?: number;
  precipitation_probability_max?: number;
  wind_speed_10m_max_kmh?: number;
  wind_gusts_10m_max_kmh?: number;
  uv_index_max?: number;
  sunrise?: string;
  sunset?: string;
  coordinates?: { lat: number; lng: number };
}

// Trail Booking Types
export interface TrailBooking {
  id: string;
  user: string;
  trail_id: string;
  trail_title?: string;
  trail_location?: string;
  trail_county?: string;
  trail_scheduled_date?: string;
  trail_start_time?: string;
  trail_end_time?: string;
  trail_meeting_point?: string;
  trail_meeting_time?: string;
  trail_difficulty_level?: string;
  trail_type?: string;
  trail_distance_km?: number;
  trail_duration_hours?: number;
  trail_elevation_gain_m?: number;
  trail_altitude_max_m?: number;
  trail_fitness_level?: string;
  trail_water_requirement_litres?: number;
  trail_terrain_summary?: string;
  trail_transport_notes?: string;
  trail_packing_list?: string;
  trail_safety_notes?: string;
  booking_date: string;
  status: 'Pending' | 'Confirmed' | 'Cancelled' | 'Completed';
  spots_booked: number;
  base_price?: number;
  activities_price?: number;
  total_price: number;
  payment_status:
    | 'Pending'
    | 'Prompt Sent'
    | 'Callback Received'
    | 'Paid'
    | 'Failed'
    | 'Cancelled'
    | 'Timeout'
    | 'Completed';
  payment?: string | null;
  payment_ticket?: string | null;
  payment_method?: 'MPESA' | 'Stripe' | 'Cash';
  payment_attempt_count?: number;
  last_payment_attempt_on?: string | null;
  mpesa_receipt_number?: string;
  mpesa_phone_number?: string;
  mpesa_transaction_id?: string;
  confirmation_code: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  transport_needed?: boolean;
  pickup_location?: string;
  fitness_self_rating?: string;
  medical_notes?: string;
  dietary_notes?: string;
  gear_notes?: string;
  special_requests?: string;
  cancellation_reason?: string;
  cancellation_date?: string;
  selected_activities?: Array<{
    activity_id: string;
    activity_name: string;
    quantity: number;
    price: number;
    total_price?: number;
  }>; // Selected extra activities
  created_at: string;
  updated_at: string;
}

export type MpesaPaymentStatus =
  | 'Pending'
  | 'Prompt Sent'
  | 'Callback Received'
  | 'Paid'
  | 'Failed'
  | 'Cancelled'
  | 'Timeout';

export interface MpesaPaymentRequest {
  journey_type: string;
  reference_name: string;
  amount: number;
  phone_number: string;
  reference_doctype?: string;
  company?: string;
  metadata?: Record<string, unknown>;
}

export interface MpesaPaymentInitiation {
  success: boolean;
  payment_id: string;
  status: MpesaPaymentStatus;
  message: string;
  provider_status_code?: string;
  provider_status_message?: string;
  failure_reason?: string;
  checkout_request_id?: string;
  merchant_request_id?: string;
  ticket_id?: string;
  ticket_status?: string;
  amount: number;
  phone_number: string;
  callback_url?: string;
}

export interface MpesaPaymentState {
  payment_id: string;
  status: MpesaPaymentStatus;
  paid: boolean;
  failed: boolean;
  is_terminal?: boolean;
  message: string;
  checkout_request_id?: string;
  merchant_request_id?: string;
  ticket_id?: string;
  ticket_status?: string;
  receipt_number?: string;
  provider_transaction_id?: string;
  provider_status_code?: string;
  provider_status_message?: string;
  failure_reason?: string;
  amount: number;
  phone_number: string;
  reference_name: string;
  reference_doctype?: string;
  payment_journey: string;
  paid_on?: string;
  callback_received_on?: string;
  attempt_no?: number;
  stale_callback_count?: number;
  attempt_history?: Array<{
    attempt_no: number;
    initiated_at?: string;
    checkout_request_id?: string;
    merchant_request_id?: string;
    status_after_callback?: string;
    callback_received_on?: string;
  }>;
}

// User Types
export interface User {
  name: string;
  email: string;
  full_name: string;
  user_image?: string;
}

// Filter Types
export interface TrailFilters {
  search?: string;
  difficulty_level?: string;
  min_price?: number;
  max_price?: number;
  date_from?: string;
  date_to?: string;
  location?: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}

// UI State Types
export interface LoadingState {
  isLoading: boolean;
  error?: string;
}

export interface ModalState {
  isOpen: boolean;
  type?: string;
  data?: any;
}

export interface NotificationState {
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

// Blog Types
export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  featured_image?: string;
  author: string;
  author_image?: string;
  category: string;
  tags: string[];
  published_date: string;
  read_time: number;
  status: 'Published' | 'Draft';
  created_at: string;
  updated_at: string;
}

export interface PhotoGallery {
  id: string;
  title: string;
  description: string;
  trail_id?: string;
  category: string;
  images: GalleryImage[];
  created_date: string;
  photographer?: string;
}

export interface GalleryImage {
  id: string;
  url: string;
  caption: string;
  thumbnail_url?: string;
}

export interface BlogFilters {
  search?: string;
  category?: string;
  tag?: string;
}

export interface BlogComment {
  id: string;
  author: string;
  email?: string;
  content: string;
  created_at: string;
}

export interface BlogPostInput {
  title: string;
  content: string;
  slug?: string;
  excerpt?: string;
  featured_image?: string;
  published?: 0 | 1;
}

export interface RegisterMemberPayload {
  email: string;
  password: string;
  first_name: string;
  last_name?: string;
  phone?: string;
}

export interface RegisterMemberResponse {
  success: boolean;
  user: string;
  member: string;
  message: string;
}

export interface BookingPaymentStatusResponse {
  booking: TrailBooking;
  payment: MpesaPaymentState;
}
