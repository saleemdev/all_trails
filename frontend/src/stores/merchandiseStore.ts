import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { shopApi } from '../services/shopApi'
import type {
  CatalogFilters,
  CartLineItem,
  CheckoutDraft,
  CouponValidationResult,
  CreateMerchandiseOrderPayload,
  MerchandiseCategory,
  MerchandiseItem,
  MerchandiseOrder,
} from '../types/shop'

const CART_STORAGE_KEY = 'all-trails-cart'
const COUPON_STORAGE_KEY = 'all-trails-cart-coupon'
const CHECKOUT_STORAGE_KEY = 'all-trails-checkout-draft'

const readJson = <T>(key: string, fallback: T): T => {
  if (typeof window === 'undefined') {
    return fallback
  }

  try {
    const raw = window.localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as T) : fallback
  } catch {
    return fallback
  }
}

const writeJson = (key: string, value: unknown) => {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.setItem(key, JSON.stringify(value))
}

const defaultCheckoutDraft = (): CheckoutDraft => ({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  delivery_address: '',
  delivery_city: 'Nairobi',
  delivery_notes: '',
  payment_method: 'MPESA',
  mpesa_phone_number: '',
})

export const useMerchandiseStore = defineStore('merchandise', () => {
  const items = ref<MerchandiseItem[]>([])
  const featuredItems = ref<MerchandiseItem[]>([])
  const categories = ref<MerchandiseCategory[]>([])
  const selectedItem = ref<MerchandiseItem | null>(null)
  const orders = ref<MerchandiseOrder[]>([])
  const cart = ref<CartLineItem[]>(readJson<CartLineItem[]>(CART_STORAGE_KEY, []))
  const checkoutDraft = ref<CheckoutDraft>(readJson<CheckoutDraft>(CHECKOUT_STORAGE_KEY, defaultCheckoutDraft()))
  const activeCoupon = ref<CouponValidationResult | null>(readJson<CouponValidationResult | null>(COUPON_STORAGE_KEY, null))
  const filters = ref<CatalogFilters>({
    search: '',
    category: '',
    featured_only: false,
    sort_by: 'featured',
  })
  const isLoading = ref(false)
  const isSubmitting = ref(false)
  const error = ref<string | null>(null)
  const currentOrder = ref<MerchandiseOrder | null>(null)

  const cartCount = computed(() => cart.value.reduce((sum, line) => sum + line.quantity, 0))
  const subtotal = computed(() =>
    cart.value.reduce((sum, line) => {
      const unitPrice = line.product.discount_price ?? line.product.selling_price
      return sum + unitPrice * line.quantity
    }, 0)
  )
  const shipping = computed(() => (subtotal.value >= 15000 ? 0 : cart.value.length > 0 ? 650 : 0))
  const discount = computed(() => {
    const coupon = activeCoupon.value
    if (!coupon?.valid || !coupon.discount_type || !coupon.discount_value) {
      return 0
    }

    if (coupon.discount_type === 'shipping') {
      return Math.min(shipping.value, coupon.discount_value)
    }

    if (coupon.discount_type === 'flat') {
      return Math.min(subtotal.value, coupon.discount_value)
    }

    const calculated = subtotal.value * (coupon.discount_value / 100)
    return Math.round(Math.min(coupon.max_discount || calculated, calculated))
  })
  const total = computed(() => Math.max(0, subtotal.value + shipping.value - discount.value))
  const bnplAvailable = computed(() => {
    if (cart.value.length === 0) {
      return false
    }

    const largestMinimum = Math.max(...cart.value.map((line) => line.product.bnpl_min_amount))
    return cart.value.every((line) => line.product.bnpl_eligible) && total.value >= largestMinimum
  })

  watch(
    cart,
    (value) => {
      writeJson(CART_STORAGE_KEY, value)
    },
    { deep: true }
  )

  watch(
    activeCoupon,
    (value) => {
      writeJson(COUPON_STORAGE_KEY, value)
    },
    { deep: true }
  )

  watch(
    checkoutDraft,
    (value) => {
      writeJson(CHECKOUT_STORAGE_KEY, value)
    },
    { deep: true }
  )

  const setFilters = (next: Partial<CatalogFilters>) => {
    filters.value = {
      ...filters.value,
      ...next,
    }
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      category: '',
      featured_only: false,
      sort_by: 'featured',
    }
  }

  const fetchCatalog = async () => {
    isLoading.value = true
    error.value = null

    try {
      const response = await shopApi.getCatalog(filters.value)
      items.value = response.data
      featuredItems.value = response.featured
      categories.value = response.categories
    } catch (reason) {
      error.value = reason instanceof Error ? reason.message : 'Unable to load the shop catalog.'
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    try {
      categories.value = await shopApi.getCategories()
    } catch (reason) {
      error.value = reason instanceof Error ? reason.message : 'Unable to load product categories.'
    }
  }

  const fetchItem = async (itemCode: string) => {
    isLoading.value = true
    error.value = null

    try {
      selectedItem.value = await shopApi.getItemDetails(itemCode)
      return selectedItem.value
    } catch (reason) {
      selectedItem.value = null
      error.value = reason instanceof Error ? reason.message : 'Unable to load this product.'
      return null
    } finally {
      isLoading.value = false
    }
  }

  const upsertOrder = (order: MerchandiseOrder) => {
    const index = orders.value.findIndex((entry) => entry.id === order.id)
    if (index >= 0) {
      orders.value.splice(index, 1, order)
      return
    }

    orders.value.unshift(order)
  }

  const loadOrders = async (customerEmail?: string) => {
    try {
      orders.value = await shopApi.listOrders(customerEmail)
    } catch (reason) {
      error.value = reason instanceof Error ? reason.message : 'Unable to load your orders.'
    }
  }

  const fetchOrderById = async (orderId: string) => {
    isLoading.value = true
    error.value = null

    try {
      const order = await shopApi.getOrderStatus(orderId)
      currentOrder.value = order
      upsertOrder(order)
      return order
    } catch (reason) {
      error.value = reason instanceof Error ? reason.message : 'Unable to load the order.'
      currentOrder.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  const addToCart = (
    product: MerchandiseItem,
    quantity = 1,
    options: { selected_color?: string; selected_size?: string } = {}
  ) => {
    const lineId = [product.item_code, options.selected_color || 'default', options.selected_size || 'default'].join('::')
    const existing = cart.value.find((line) => line.line_id === lineId)

    if (existing) {
      existing.quantity += quantity
      return
    }

    cart.value.unshift({
      line_id: lineId,
      item_code: product.item_code,
      quantity,
      selected_color: options.selected_color,
      selected_size: options.selected_size,
      product,
    })
  }

  const updateQuantity = (lineId: string, quantity: number) => {
    const line = cart.value.find((entry) => entry.line_id === lineId)
    if (!line) {
      return
    }

    if (quantity <= 0) {
      removeFromCart(lineId)
      return
    }

    line.quantity = quantity
  }

  const removeFromCart = (lineId: string) => {
    cart.value = cart.value.filter((entry) => entry.line_id !== lineId)
  }

  const clearCart = () => {
    cart.value = []
  }

  const applyCoupon = async (code: string) => {
    error.value = null
    const validation = await shopApi.validateCoupon(code, subtotal.value)

    if (!validation.valid) {
      activeCoupon.value = null
      error.value = validation.error || 'This coupon cannot be used right now.'
      return validation
    }

    activeCoupon.value = validation
    return validation
  }

  const removeCoupon = () => {
    activeCoupon.value = null
  }

  const createOrderPayload = (): CreateMerchandiseOrderPayload => ({
    items: cart.value.map((line) => ({
      item_code: line.item_code,
      quantity: line.quantity,
      selected_color: line.selected_color,
      selected_size: line.selected_size,
    })),
    customer_name: checkoutDraft.value.customer_name,
    customer_email: checkoutDraft.value.customer_email,
    customer_phone: checkoutDraft.value.customer_phone,
    delivery_address: checkoutDraft.value.delivery_address,
    delivery_city: checkoutDraft.value.delivery_city,
    delivery_notes: checkoutDraft.value.delivery_notes,
    payment_method: checkoutDraft.value.payment_method,
    coupon_code: activeCoupon.value?.code,
    mpesa_phone_number: checkoutDraft.value.mpesa_phone_number || checkoutDraft.value.customer_phone,
  })

  const submitOrder = async () => {
    isSubmitting.value = true
    error.value = null

    try {
      const order = await shopApi.createOrder(createOrderPayload())
      currentOrder.value = order
      upsertOrder(order)
      clearCart()
      activeCoupon.value = null
      checkoutDraft.value = {
        ...defaultCheckoutDraft(),
        customer_name: order.customer_name,
        customer_email: order.customer_email,
        customer_phone: order.customer_phone,
        mpesa_phone_number: order.mpesa_phone_number || order.customer_phone,
        delivery_city: order.delivery_city,
      }
      return order
    } catch (reason) {
      error.value = reason instanceof Error ? reason.message : 'Unable to place this order.'
      return null
    } finally {
      isSubmitting.value = false
    }
  }

  const confirmMockPayment = async (orderId: string) => {
    const order = await shopApi.completeMockPayment(orderId)
    currentOrder.value = order
    upsertOrder(order)
    return order
  }

  return {
    items,
    featuredItems,
    categories,
    selectedItem,
    orders,
    cart,
    checkoutDraft,
    activeCoupon,
    filters,
    isLoading,
    isSubmitting,
    error,
    currentOrder,
    cartCount,
    subtotal,
    shipping,
    discount,
    total,
    bnplAvailable,
    setFilters,
    clearFilters,
    fetchCatalog,
    fetchCategories,
    fetchItem,
    loadOrders,
    fetchOrderById,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    applyCoupon,
    removeCoupon,
    submitOrder,
    confirmMockPayment,
  }
})
