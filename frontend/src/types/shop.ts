export type MerchandisePaymentMethod = 'MPESA' | 'BNPL' | 'Cash on Delivery'

export type MerchandisePaymentStatus =
  | 'Pending'
  | 'Prompt Sent'
  | 'Callback Received'
  | 'Paid'
  | 'Partially Paid'
  | 'Failed'
  | 'Cancelled'
  | 'Timeout'

export type MerchandiseFulfillmentStatus =
  | 'Draft'
  | 'Confirmed'
  | 'Processing'
  | 'Packed'
  | 'Shipped'
  | 'Delivered'
  | 'Cancelled'

export interface MerchandiseCategory {
  name: string
  slug: string
  description: string
  hero_copy: string
  accent: string
  image_url: string
  featured: boolean
  sort_order: number
}

export interface MerchandiseReview {
  id: string
  customer_name: string
  rating: number
  title: string
  review_text: string
  created_at: string
  verified_purchase: boolean
  helpful_count: number
}

export interface MerchandiseItem {
  item_code: string
  slug: string
  item_name: string
  category_slug: string
  category_name: string
  short_description: string
  description: string
  selling_price: number
  discount_price?: number | null
  average_rating: number
  review_count: number
  image_url: string
  gallery_urls: string[]
  highlights: string[]
  materials: string[]
  badges: string[]
  inventory_qty: number
  available_colors: string[]
  available_sizes: string[]
  estimated_dispatch: string
  is_featured: boolean
  is_active: boolean
  bnpl_eligible: boolean
  bnpl_min_amount: number
  featured_copy?: string
  reviews?: MerchandiseReview[]
}

export interface CatalogFilters {
  search?: string
  category?: string
  featured_only?: boolean
  min_price?: number
  max_price?: number
  sort_by?: 'featured' | 'price-asc' | 'price-desc' | 'rating' | 'newest'
}

export interface CatalogResponse {
  data: MerchandiseItem[]
  total: number
  categories: MerchandiseCategory[]
  featured: MerchandiseItem[]
}

export interface CouponValidationResult {
  valid: boolean
  code: string
  description?: string
  discount_type?: 'flat' | 'percentage' | 'shipping'
  discount_value?: number
  max_discount?: number
  min_subtotal?: number
  error?: string
}

export interface CartLineItem {
  line_id: string
  item_code: string
  quantity: number
  selected_color?: string
  selected_size?: string
  product: MerchandiseItem
}

export interface OrderTimelineEntry {
  label: string
  detail: string
  happened_at: string
}

export interface BnplInstallment {
  installment_number: number
  amount: number
  due_date: string
  status: 'Pending' | 'Paid'
}

export interface BnplPlanSummary {
  upfront_amount: number
  remaining_amount: number
  installments: BnplInstallment[]
}

export interface MerchandiseOrderItem {
  item_code: string
  item_name: string
  quantity: number
  unit_price: number
  selected_color?: string
  selected_size?: string
  line_total: number
}

export interface MerchandiseOrder {
  id: string
  order_number: string
  customer_name: string
  customer_email: string
  customer_phone: string
  delivery_address: string
  delivery_city: string
  delivery_notes?: string
  payment_method: MerchandisePaymentMethod
  payment_status: MerchandisePaymentStatus
  fulfillment_status: MerchandiseFulfillmentStatus
  subtotal_amount: number
  shipping_amount: number
  discount_amount: number
  total_amount: number
  amount_due_now: number
  amount_remaining: number
  coupon_code?: string
  mpesa_phone_number?: string
  mpesa_payment_id?: string
  mpesa_ticket_id?: string
  payment_detail?: {
    payment_id: string
    status: MerchandisePaymentStatus
    paid: boolean
    failed: boolean
    is_terminal?: boolean
    message: string
    ticket_id?: string
    ticket_status?: string
    checkout_request_id?: string
    merchant_request_id?: string
    receipt_number?: string
    provider_transaction_id?: string
    provider_status_code?: string
    provider_status_message?: string
    failure_reason?: string
    amount: number
    phone_number?: string
    paid_on?: string
    callback_received_on?: string
  }
  tracking_number?: string
  estimated_delivery_window: string
  items: MerchandiseOrderItem[]
  timeline: OrderTimelineEntry[]
  bnpl_plan?: BnplPlanSummary
  created_at: string
  updated_at: string
}

export interface CreateMerchandiseOrderPayload {
  items: Array<{
    item_code: string
    quantity: number
    selected_color?: string
    selected_size?: string
  }>
  customer_name: string
  customer_email: string
  customer_phone: string
  delivery_address: string
  delivery_city: string
  delivery_notes?: string
  payment_method: MerchandisePaymentMethod
  coupon_code?: string
  mpesa_phone_number?: string
}

export interface CheckoutDraft {
  customer_name: string
  customer_email: string
  customer_phone: string
  delivery_address: string
  delivery_city: string
  delivery_notes: string
  payment_method: MerchandisePaymentMethod
  mpesa_phone_number: string
}

export interface CheckoutStep {
  id: 'delivery' | 'payment' | 'review'
  title: string
  description: string
}
