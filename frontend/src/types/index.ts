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
  location: string;
  coordinates?: { lat: number; lng: number };
  distance_km: number;
  elevation_gain_m: number;
  duration_hours: number;
  scheduled_date: string;
  start_time: string;
  end_time: string;
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

// Trail Booking Types
export interface TrailBooking {
  id: string;
  user: string;
  trail_id: string;
  booking_date: string;
  status: 'Pending' | 'Confirmed' | 'Cancelled' | 'Completed';
  spots_booked: number;
  total_price: number;
  payment_status: 'Pending' | 'Completed' | 'Failed' | 'Refunded';
  payment_method?: 'MPESA' | 'Stripe' | 'Cash';
  mpesa_receipt_number?: string;
  mpesa_phone_number?: string;
  mpesa_transaction_id?: string;
  confirmation_code: string;
  cancellation_reason?: string;
  cancellation_date?: string;
  trail_title?: string;
  trail_location?: string;
  trail_scheduled_date?: string;
  selected_activities?: Array<{
    activity_id: string;
    activity_name: string;
    quantity: number;
    price: number;
  }>; // Selected extra activities
  created_at: string;
  updated_at: string;
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
  featured_image: string;
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

