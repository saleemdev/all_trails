import axios, { type AxiosInstance } from 'axios'
import { mockCoupons, mockMerchandiseCategories, mockMerchandiseItems, mockReviewsByItem } from './mockShopData'
import type {
  CatalogFilters,
  CatalogResponse,
  CouponValidationResult,
  CreateMerchandiseOrderPayload,
  MerchandiseItem,
  MerchandiseOrder,
  MerchandisePaymentMethod,
} from '../types/shop'

const STORAGE_KEY = 'all-trails-shop-orders'
const USE_MOCK_SHOP_DATA = import.meta.env.VITE_USE_MOCK_SHOP_DATA === 'true'

const normalizeMoney = (value: number) => Math.round(value)

const publicPrice = (item: MerchandiseItem) => item.discount_price ?? item.selling_price

const buildOrderNumber = () => {
  const stamp = new Date()
  const year = stamp.getFullYear()
  const tail = Math.floor(Math.random() * 9000 + 1000)
  return `MO-${year}-${tail}`
}

const readOrders = (): MerchandiseOrder[] => {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as MerchandiseOrder[]) : []
  } catch {
    return []
  }
}

const writeOrders = (orders: MerchandiseOrder[]) => {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(orders))
}

const withReviews = (item: MerchandiseItem): MerchandiseItem => ({
  ...item,
  reviews: mockReviewsByItem[item.item_code] || [],
})

class ShopApiService {
  private axiosInstance: AxiosInstance

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: '/api/method',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    })

    this.axiosInstance.interceptors.request.use((config) => {
      if ((window as any).csrf_token) {
        config.headers['X-Frappe-CSRF-Token'] = (window as any).csrf_token
      }

      return config
    })
  }

  usesMockData() {
    return USE_MOCK_SHOP_DATA
  }

  async getCatalog(filters: CatalogFilters = {}): Promise<CatalogResponse> {
    if (USE_MOCK_SHOP_DATA) {
      return this.getMockCatalog(filters)
    }

    const response = await this.axiosInstance.get('/all_trails.api.get_merchandise_catalog', {
      params: filters,
    })
    return response.data.message || response.data
  }

  async getCategories() {
    if (USE_MOCK_SHOP_DATA) {
      return [...mockMerchandiseCategories].sort((left, right) => left.sort_order - right.sort_order)
    }

    const response = await this.axiosInstance.get('/all_trails.api.get_merchandise_categories')
    return response.data.message || response.data
  }

  async getItemDetails(itemCode: string): Promise<MerchandiseItem> {
    if (USE_MOCK_SHOP_DATA) {
      const item = mockMerchandiseItems.find((entry) => entry.item_code === itemCode || entry.slug === itemCode)
      if (!item) {
        throw new Error('Product not found')
      }

      return withReviews(item)
    }

    const response = await this.axiosInstance.get('/all_trails.api.get_merchandise_item_details', {
      params: { item_code: itemCode },
    })
    return response.data.message || response.data
  }

  async validateCoupon(code: string, subtotal: number): Promise<CouponValidationResult> {
    if (USE_MOCK_SHOP_DATA) {
      const normalizedCode = code.trim().toUpperCase()
      const coupon = mockCoupons[normalizedCode]
      if (!coupon) {
        return {
          valid: false,
          code: normalizedCode,
          error: 'Coupon code not recognised.',
        }
      }

      if (coupon.min_subtotal && subtotal < coupon.min_subtotal) {
        return {
          valid: false,
          code: normalizedCode,
          error: `This code unlocks from KES ${coupon.min_subtotal.toLocaleString()}.`,
        }
      }

      return coupon
    }

    const response = await this.axiosInstance.post('/all_trails.api.validate_merchandise_coupon', {
      code,
      subtotal,
    })
    return response.data.message || response.data
  }

  async createOrder(payload: CreateMerchandiseOrderPayload): Promise<MerchandiseOrder> {
    if (USE_MOCK_SHOP_DATA) {
      return this.createMockOrder(payload)
    }

    const response = await this.axiosInstance.post('/all_trails.api.create_merchandise_order', payload)
    return response.data.message || response.data
  }

  async getOrderStatus(orderId: string): Promise<MerchandiseOrder> {
    if (USE_MOCK_SHOP_DATA) {
      const order = readOrders().find((entry) => entry.id === orderId || entry.order_number === orderId)
      if (!order) {
        throw new Error('Order not found')
      }
      return order
    }

    const response = await this.axiosInstance.get('/all_trails.api.get_merchandise_order_status', {
      params: { order_id: orderId },
    })
    return response.data.message || response.data
  }

  async listOrders(customerEmail?: string): Promise<MerchandiseOrder[]> {
    if (USE_MOCK_SHOP_DATA) {
      const orders = readOrders()
      if (!customerEmail) {
        return orders
      }

      return orders.filter((entry) => entry.customer_email.toLowerCase() === customerEmail.toLowerCase())
    }

    const response = await this.axiosInstance.get('/all_trails.api.list_merchandise_orders', {
      params: { customer_email: customerEmail },
    })
    return response.data.message || response.data
  }

  async completeMockPayment(orderId: string): Promise<MerchandiseOrder> {
    const orders = readOrders()
    const orderIndex = orders.findIndex((entry) => entry.id === orderId)
    if (orderIndex === -1) {
      throw new Error('Order not found')
    }

    const current = orders[orderIndex]
    const paidAt = new Date().toISOString()
    const paymentMethod: MerchandisePaymentMethod = current.payment_method

    const nextOrder: MerchandiseOrder = {
      ...current,
      payment_status: paymentMethod === 'BNPL' ? 'Partially Paid' : 'Paid',
      fulfillment_status: 'Confirmed',
      amount_remaining: paymentMethod === 'BNPL' ? current.amount_remaining : 0,
      timeline: [
        ...current.timeline,
        {
          label: paymentMethod === 'BNPL' ? 'Deposit received' : 'Payment received',
          detail:
            paymentMethod === 'BNPL'
              ? 'The first installment cleared successfully. Remaining balance is scheduled automatically.'
              : 'Your MPESA payment cleared successfully and the order is moving into fulfillment.',
          happened_at: paidAt,
        },
      ],
      updated_at: paidAt,
    }

    orders.splice(orderIndex, 1, nextOrder)
    writeOrders(orders)
    return nextOrder
  }

  private getMockCatalog(filters: CatalogFilters): CatalogResponse {
    const search = filters.search?.trim().toLowerCase()
    const category = filters.category?.trim()
    const minPrice = filters.min_price
    const maxPrice = filters.max_price
    const sortBy = filters.sort_by || 'featured'

    let data = mockMerchandiseItems.filter((item) => item.is_active)

    if (search) {
      data = data.filter((item) => {
        const target = [
          item.item_name,
          item.short_description,
          item.category_name,
          item.highlights.join(' '),
        ]
          .join(' ')
          .toLowerCase()
        return target.includes(search)
      })
    }

    if (category) {
      data = data.filter((item) => item.category_slug === category)
    }

    if (filters.featured_only) {
      data = data.filter((item) => item.is_featured)
    }

    if (typeof minPrice === 'number') {
      data = data.filter((item) => publicPrice(item) >= minPrice)
    }

    if (typeof maxPrice === 'number') {
      data = data.filter((item) => publicPrice(item) <= maxPrice)
    }

    data.sort((left, right) => {
      if (sortBy === 'price-asc') {
        return publicPrice(left) - publicPrice(right)
      }
      if (sortBy === 'price-desc') {
        return publicPrice(right) - publicPrice(left)
      }
      if (sortBy === 'rating') {
        return right.average_rating - left.average_rating
      }
      if (sortBy === 'newest') {
        return right.item_code.localeCompare(left.item_code)
      }

      return Number(right.is_featured) - Number(left.is_featured) || right.average_rating - left.average_rating
    })

    return {
      data,
      total: data.length,
      categories: [...mockMerchandiseCategories].sort((left, right) => left.sort_order - right.sort_order),
      featured: mockMerchandiseItems.filter((item) => item.is_featured).slice(0, 4),
    }
  }

  private createMockOrder(payload: CreateMerchandiseOrderPayload): MerchandiseOrder {
    const items = payload.items.map((line) => {
      const product = mockMerchandiseItems.find((item) => item.item_code === line.item_code)
      if (!product) {
        throw new Error(`Product ${line.item_code} is unavailable.`)
      }

      const unitPrice = publicPrice(product)

      return {
        item_code: product.item_code,
        item_name: product.item_name,
        quantity: line.quantity,
        unit_price: unitPrice,
        selected_color: line.selected_color,
        selected_size: line.selected_size,
        line_total: normalizeMoney(unitPrice * line.quantity),
      }
    })

    const subtotal = normalizeMoney(items.reduce((sum, item) => sum + item.line_total, 0))
    const shipping = subtotal >= 15000 ? 0 : 650
    const coupon = payload.coupon_code ? mockCoupons[payload.coupon_code.toUpperCase()] : undefined
    const discount = coupon?.valid
      ? this.computeDiscount(coupon, subtotal, shipping)
      : 0
    const total = normalizeMoney(subtotal + shipping - discount)
    const createdAt = new Date().toISOString()
    const orderId = `shop-order-${Date.now()}`
    const upfrontAmount = payload.payment_method === 'BNPL' ? normalizeMoney(total / 2) : total
    const remainingAmount = payload.payment_method === 'BNPL' ? total - upfrontAmount : 0

    const order: MerchandiseOrder = {
      id: orderId,
      order_number: buildOrderNumber(),
      customer_name: payload.customer_name,
      customer_email: payload.customer_email,
      customer_phone: payload.customer_phone,
      delivery_address: payload.delivery_address,
      delivery_city: payload.delivery_city,
      delivery_notes: payload.delivery_notes,
      payment_method: payload.payment_method,
      payment_status: payload.payment_method === 'Cash on Delivery' ? 'Pending' : 'Prompt Sent',
      fulfillment_status: 'Draft',
      subtotal_amount: subtotal,
      shipping_amount: shipping,
      discount_amount: discount,
      total_amount: total,
      amount_due_now: upfrontAmount,
      amount_remaining: remainingAmount,
      coupon_code: coupon?.valid ? coupon.code : undefined,
      mpesa_phone_number: payload.mpesa_phone_number,
      mpesa_payment_id: payload.payment_method === 'Cash on Delivery' ? undefined : `PAY-${Date.now()}`,
      tracking_number: undefined,
      estimated_delivery_window: '2 to 4 business days',
      items,
      timeline: [
        {
          label: 'Order created',
          detail: 'We captured your basket and reserved stock for payment confirmation.',
          happened_at: createdAt,
        },
        {
          label: payload.payment_method === 'Cash on Delivery' ? 'Awaiting confirmation' : 'Payment initiated',
          detail:
            payload.payment_method === 'Cash on Delivery'
              ? 'Your order will be confirmed by the team before dispatch.'
              : 'A payment prompt has been prepared for the selected phone number.',
          happened_at: createdAt,
        },
      ],
      bnpl_plan:
        payload.payment_method === 'BNPL'
          ? {
              upfront_amount: upfrontAmount,
              remaining_amount: remainingAmount,
              installments: [
                {
                  installment_number: 1,
                  amount: upfrontAmount,
                  due_date: createdAt,
                  status: 'Pending',
                },
                {
                  installment_number: 2,
                  amount: remainingAmount,
                  due_date: new Date(Date.now() + 1000 * 60 * 60 * 24 * 30).toISOString(),
                  status: 'Pending',
                },
              ],
            }
          : undefined,
      created_at: createdAt,
      updated_at: createdAt,
    }

    const orders = readOrders()
    orders.unshift(order)
    writeOrders(orders)
    return order
  }

  private computeDiscount(coupon: CouponValidationResult, subtotal: number, shipping: number) {
    if (!coupon.valid || !coupon.discount_type || !coupon.discount_value) {
      return 0
    }

    if (coupon.discount_type === 'shipping') {
      return Math.min(shipping, coupon.discount_value)
    }

    if (coupon.discount_type === 'flat') {
      return Math.min(subtotal, coupon.discount_value)
    }

    const calculated = subtotal * (coupon.discount_value / 100)
    return normalizeMoney(Math.min(coupon.max_discount || calculated, calculated))
  }
}

export const shopApi = new ShopApiService()
