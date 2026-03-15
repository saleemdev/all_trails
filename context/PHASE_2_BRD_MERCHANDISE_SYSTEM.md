# All Trails Phase 2: Merchandise System - Business Requirements Document

**Version**: 1.0
**Date**: 2026-03-14
**Status**: Draft for Review
**Owner**: Product Team
**Stakeholders**: Marketing, Operations, Finance, Engineering

---

## Executive Summary

Phase 2 introduces an integrated merchandise/shop system to All Trails, allowing users to purchase hiking gear, apparel, and experience products directly from the platform. This phase combines:

1. **Glassmorphic Shopping Cart** - Modern, premium UI matching All Trails brand aesthetics
2. **Flexible Payment Options** - Order Now (immediate) & Order Later (BNPL) payment flows
3. **ERPNext Integration** - Leveraging inventory, sales, and payment management
4. **MPESA Integration** - Secondary payment method using MPESA_TX architecture
5. **Inventory Management** - Real-time stock tracking with warehouse support

**Expected Impact**:
- Additional revenue stream: 15-25% of hiking bookings
- 30-40% higher customer LTV through merchandise
- Premium positioning with curated product selection
- Partnerships with local gear companies & artisans

---

## Business Objectives

### Primary Goals
1. **Monetization**: Generate incremental revenue from merchandise sales
2. **User Engagement**: Increase platform stickiness through product discovery & recommendations
3. **Brand Enhancement**: Position All Trails as premium hiking ecosystem (not just bookings)
4. **Operational Efficiency**: Leverage ERPNext for inventory & payments to reduce manual work

### Success Metrics
- **Conversion Rate**: 8-12% of hiking bookers purchase merchandise
- **AOV (Average Order Value)**: KES 2,500-3,500 per order
- **Repeat Purchase Rate**: 25%+ within 60 days
- **Customer Satisfaction**: 4.5+/5.0 NPS score
- **Operational Cost**: <15% of merchandise revenue (fulfillment, support, payment processing)

---

## Product Overview

### Merchandise Categories

#### 1. **Hiking Gear** (Functional)
- Backpacks, hydration packs, trekking poles
- Rope, carabiners, safety equipment
- Camping: tents, sleeping bags, mats
- Navigation: maps, compass, GPS devices
- Average Price: KES 1,500-10,000

#### 2. **Apparel** (Branded)
- All Trails branded t-shirts, jackets, hats
- Moisture-wicking performance wear
- Seasonal collections (winter layers, rain gear)
- Average Price: KES 800-3,000

#### 3. **Accessories** (High Margin)
- Water bottles, coolers
- Trail snacks, energy products
- Photography gear (tripods, lens protectors)
- Guidebooks, maps, journals
- Average Price: KES 200-1,500

#### 4. **Experience Products** (Digital + Physical)
- Trail guidebooks (PDF + printed)
- Hiking training programs
- Photo prints from trail moments
- Experience vouchers (gift cards for bookings)
- Average Price: KES 500-5,000

#### 5. **Artisan/Local Products** (Marketplace)
- Local craftspeople partnerships
- Handmade jewelry, baskets, textiles
- Local honey, coffee, tea from hiking regions
- Community sourced products
- Average Price: KES 400-2,500

### Initial Launch Scope (MVP)
- 50-100 curated products
- Gear + Apparel focus
- Simplified inventory (single warehouse)
- Expand to artisan/experience products in Phase 3

---

## User Flows & Use Cases

### Use Case 1: Browse & Buy After Booking

```
User books hiking trail → Browse recommended merchandise
  → Add hiking boots to cart → Continue shopping
  → View cart (glassmorphic UI) → Proceed to checkout
  → Choose payment: "Pay Now" or "Pay Later"
  → Complete order
```

**Trigger**: Post-booking recommended products (email + in-app notification)
**Goal**: Convert hiking buyers to merchandise buyers

### Use Case 2: Plan Hiking Trip, Buy Gear

```
User planning trip to Mount Kenya → Shop section
  → Filter by "High Altitude Gear" → Browse products
  → Read reviews from other hikers
  → Add multiple items to cart
  → Apply coupon/loyalty discount
  → "Pay Later" option (BNPL) for expensive items
  → Schedule delivery to arrive before trip date
```

**Trigger**: Trip planning mode in booking flow
**Goal**: Complete gear setup before trip

### Use Case 3: Order Later (BNPL)

```
User finds expensive backpack (KES 8,000)
  → Selects "Pay Later" option
  → Creates installment plan (e.g., 2 x KES 4,000)
  → First payment via MPESA (immediate)
  → Second payment auto-deducted after 30 days
  → 0% interest for orders <KES 10,000
  → Receives email reminders before each payment
```

**Trigger**: Cart total > KES 5,000 with "Pay Later" enabled
**Goal**: Reduce payment friction for high-ticket items

### Use Case 4: Repeat Purchases & Loyalty

```
User has purchased before → Loyalty badge/discount
  → Browse recommendations based on trail history
  → "Exclusive Member Price" on selected items
  → 1-click reorder for favorite items
  → Subscribe to seasonal sales notifications
```

**Trigger**: Customer has 2+ purchases
**Goal**: Drive repeat purchases

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Vue 3 Frontend                             │
├─────────────────────────────────────────────────────────────┤
│  GlassCart     GlassCheckout    GlassProduct    GlassOrder   │
└────────────┬──────────────────────────────────┬──────────────┘
             │                                  │
    ┌────────▼──────────────────────┬──────────▼──────┐
    │     Frappe Backend API        │   State Manager  │
    │  all_trails.api.shop.*        │   (Pinia Store)  │
    └────────┬──────────────────────┴──────────┬───────┘
             │                                  │
    ┌────────▼──────────────────────────────────▼──────┐
    │           Frappe DocTypes & Workflows            │
    ├────────────────────────────────────────────────────┤
    │  • Item (catalog)                                  │
    │  • Warehouse (inventory locations)                 │
    │  • Stock Entry (inventory adjustments)             │
    │  • Sales Order (order record)                      │
    │  • Sales Invoice (billable order)                  │
    │  • Payment Entry (payment tracking)                │
    │  • BNPL Plan (installment setup)                   │
    │  • Merchandise Order (custom doctype)              │
    └────────┬────────────────────────────┬─────────────┘
             │                            │
    ┌────────▼─────────────┐    ┌────────▼──────────────┐
    │   MPESA_TX Module    │    │   Payment Processing  │
    │  (Payment Handler)   │    │   (Background Jobs)   │
    └──────────────────────┘    └───────────────────────┘
```

### New DocTypes

#### 1. **Merchandise Item**
```
DocType: Merchandise Item
Purpose: Extended Item catalog with merchandising metadata

Fields:
  - item_code (FK: Item)
  - item_name (string)
  - description (text)
  - category (link: Merchandise Category)
  - sub_category (string)
  - sku (string, unique)

  # Pricing
  - cost_price (currency)
  - selling_price (currency)
  - discount_price (currency)
  - bnpl_installment_count (int, default: 2)
  - bnpl_min_amount (currency, default: 5000)

  # Inventory
  - warehouse (link: Warehouse)
  - low_stock_threshold (int)
  - is_active (bool)
  - brand (string)

  # Media & Content
  - image_urls (text[], JSON array)
  - gallery_images (child table)
  - description_html (HTML rich text)
  - care_instructions (text)
  - specifications (JSON)
  - hikable_difficulty (select: Easy/Moderate/Hard/Expert)
  - suitable_for_trails (link: Trail, multi-select)

  # Reviews & Ratings
  - average_rating (decimal, read_only)
  - review_count (int, read_only)
  - hikers_who_bought (int, read_only)

  # Metadata
  - featured (bool)
  - position_in_category (int)
  - tags (text, comma-separated)
  - search_keywords (text)

Indexes: category, is_active, warehouse
Audit Trail: Yes
```

#### 2. **Merchandise Order**
```
DocType: Merchandise Order
Purpose: Custom order wrapper for merchandise sales

Fields:
  - order_id (string, auto-generated: MO-XXXX-XXXX)
  - customer_id (link: Contact/User)
  - customer_email (string)
  - customer_phone (string)
  - order_date (datetime)

  # Order Items
  - items (child table: Merchandise Order Item)
    - item_code (FK: Merchandise Item)
    - quantity (int)
    - unit_price (currency)
    - discount_percentage (decimal)
    - line_total (currency, calculated)

  # Totals
  - subtotal (currency, calculated)
  - discount_amount (currency)
  - shipping_cost (currency)
  - tax_amount (currency)
  - total_amount (currency, calculated)

  # Payment
  - payment_method (select: MPESA/Card/BNPL)
  - payment_status (select: Pending/Partial/Completed/Failed)
  - payment_mode (select: Full/Installment)

  # BNPL Specific
  - bnpl_plan_id (link: BNPL Plan, if payment_mode = Installment)
  - bnpl_total_installments (int)
  - bnpl_remaining_installments (int)
  - bnpl_next_payment_date (date)
  - bnpl_next_payment_amount (currency)

  # Fulfillment
  - fulfillment_status (select: Draft/Confirmed/Processing/Shipped/Delivered/Cancelled)
  - shipping_address (text)
  - estimated_delivery_date (date)
  - actual_delivery_date (date)
  - tracking_number (string)
  - notes (text)

  # Links to ERPNext
  - sales_order_id (link: Sales Order)
  - sales_invoice_id (link: Sales Invoice)
  - payment_entry_ids (link: Payment Entry, multi-select, child table)

  # Metadata
  - created_from_hiking_booking (link: Booking if applicable)
  - referral_source (string: homepage/booking/email/trail_page)
  - utm_source (string)

Workflows:
  - Draft → Confirmed (validate stock)
  - Confirmed → Processing (payment confirmed)
  - Processing → Shipped (pickup initiated)
  - Shipped → Delivered (customer confirmed)
  - Any → Cancelled (before processing)

Audit Trail: Yes
Permissions: Customer can view own, Staff can manage all
```

#### 3. **BNPL Plan** (Buy Now Pay Later)
```
DocType: BNPL Plan
Purpose: Track installment payment schedules

Fields:
  - plan_id (string, auto-generated)
  - merchandise_order (link: Merchandise Order)
  - total_amount (currency)
  - installment_count (int)
  - installment_amount (currency)
  - first_payment_date (date)
  - payment_frequency (select: Weekly/Bi-weekly/Monthly)
  - status (select: Active/Completed/Defaulted)
  - payment_method (select: MPESA/Card)

  # Installments
  - installments (child table)
    - installment_number (int)
    - due_date (date)
    - amount (currency)
    - payment_status (select: Pending/Paid/Overdue)
    - payment_date (date)
    - payment_entry_id (link: Payment Entry)
    - notes (text)

  # Risk & Compliance
  - customer_credit_score (int, if third-party BNPL)
  - approval_status (select: Approved/Pending/Rejected)
  - declined_reason (text)
  - automatic_retry (bool, default: true)
  - max_retries (int, default: 3)

  # Metadata
  - created_date (datetime)
  - next_payment_reminder_sent (date)

Triggers:
  - Auto-send payment reminders 3 days before due date
  - Auto-attempt payment on due date via MPESA_TX
  - Mark as Defaulted if 3 retries fail
  - Escalate to support if overdue >7 days

Audit Trail: Yes
```

#### 4. **Merchandise Review**
```
DocType: Merchandise Review
Purpose: Customer reviews & ratings

Fields:
  - review_id (string, auto-generated)
  - item_code (link: Merchandise Item)
  - customer (link: Contact)
  - rating (int: 1-5)
  - title (string)
  - review_text (text)
  - verified_purchase (bool)
  - helpful_count (int)

  # Metadata
  - created_date (datetime)
  - status (select: Pending/Approved/Rejected)
  - hiking_difficulty_purchased_for (select)
  - would_recommend (bool)

Workflow: Pending → Approved (moderation)
```

#### 5. **Merchandise Category**
```
DocType: Merchandise Category
Purpose: Product categorization & navigation

Fields:
  - category_id (string)
  - category_name (string)
  - parent_category (link: Merchandise Category)
  - description (text)
  - icon (string/image)
  - sort_order (int)
  - is_active (bool)

Examples:
  - Hiking Gear
    - Backpacks
    - Footwear
    - Navigation
    - Safety Equipment
  - Apparel
    - T-Shirts
    - Jackets
    - Accessories
  - Experience Products
    - Digital Downloads
    - Guidebooks
    - Photo Prints
```

---

## Frontend Implementation

### Glassmorphic Shopping Cart UI

#### Design System (CSS Variables)

```css
/* Glass Effect Variables */
--glass-bg: rgba(27, 58, 45, 0.85);              /* Forest Dark + 85% opacity */
--glass-border: rgba(255, 255, 255, 0.2);        /* Subtle white border */
--glass-backdrop-blur: 30px;                     /* Desktop blur */
--glass-backdrop-blur-mobile: 20px;              /* Mobile (reduced for perf) */
--glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);  /* Depth */
--glass-inner-glow: inset 0 0 20px rgba(255, 255, 255, 0.2); /* Premium feel */
--glass-hover-opacity: 0.95;                     /* Hover brightens */

/* Accent Colors */
--accent-orange: #E85D1F;
--accent-orange-light: #F07D3F;
--accent-success: #10B981;
--accent-warning: #F59E0B;
--accent-error: #EF4444;

/* Base Colors (Dark Mode Support) */
--color-bg: #0F2818;                            /* Darker forest for glass */
--color-text: #F5F5F5;
--color-text-secondary: #CBD5E0;
--color-divider: rgba(255, 255, 255, 0.1);

[data-theme='light'] {
  --glass-bg: rgba(255, 255, 255, 0.9);
  --glass-border: rgba(232, 93, 31, 0.2);
  --glass-inner-glow: inset 0 0 20px rgba(232, 93, 31, 0.1);
}
```

#### Component Architecture

```
GlassCart (Container)
├── GlassCartHeader
│   ├── Title & Item Count
│   └── Close Button
├── GlassCartItems
│   └── CartItem (repeating)
│       ├── ProductImage
│       ├── ProductInfo
│       │   ├── Name
│       │   ├── Price
│       │   └── Removal Button
│       └── QuantityControl
│           ├── Decrement
│           ├── Input
│           └── Increment
├── GlassCartDivider
├── GlassCartSummary
│   ├── Subtotal
│   ├── Discount (if applied)
│   ├── Shipping
│   ├── Tax
│   └── Total (highlighted)
├── GlassPromoCode
│   ├── Input
│   └── Apply Button
└── GlassCheckoutButtons
    ├── "Pay Now" (primary)
    └── "Pay Later" (secondary)
```

#### Key Components to Build

1. **GlassCard**
   - Base component with glass effect
   - Props: padding, rounded, border, shadow, glow
   - Hover state: opacity increase + shadow enhance

2. **GlassButton**
   - Primary: Orange accent, white text, shadow
   - Secondary: Transparent glass, white border, shadow
   - Loading state: spinner overlay
   - Disabled state: opacity 50%, cursor disabled

3. **GlassInput**
   - Transparent background with glass border
   - Focus state: color change to orange border
   - Placeholder text in secondary color
   - Supports icons (prefix/suffix)

4. **GlassModal** (for checkout overlay)
   - Backdrop: semi-transparent dark
   - Content: glass card centered
   - Animations: fade-in (200ms), slide-up (300ms)
   - Escape key closes

5. **GlassProductCard**
   - Image carousel (glassmorphic nav dots)
   - Title, description, ratings
   - Price with discount badge
   - "Add to Cart" button
   - Stock status indicator

6. **GlassCheckoutFlow**
   - Multi-step form with glass cards
   - Step indicators (glassmorphic dots)
   - Validation feedback (inline, red highlight)
   - Form persistence (localStorage)

#### Vue 3 Store Structure (Pinia)

```typescript
// stores/merchandiseStore.ts

export interface CartItem {
  itemCode: string
  itemName: string
  quantity: number
  unitPrice: number
  discountPercentage: number
  lineTotal: number
  image: string
}

export interface Cart {
  items: CartItem[]
  subtotal: number
  discountAmount: number
  shippingCost: number
  taxAmount: number
  total: number
  appliedCoupon?: string
}

export interface Order {
  orderId: string
  status: 'draft' | 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered'
  paymentMethod: 'mpesa' | 'card' | 'bnpl'
  paymentStatus: 'pending' | 'partial' | 'completed' | 'failed'
  items: CartItem[]
  total: number
  createdAt: string
}

export const useMerchandiseStore = defineStore('merchandise', () => {
  // State
  const cart = ref<Cart>({
    items: [],
    subtotal: 0,
    discountAmount: 0,
    shippingCost: 0,
    taxAmount: 0,
    total: 0
  })
  const orders = ref<Order[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  const addToCart = (item: CartItem) => {
    const existing = cart.value.items.find(i => i.itemCode === item.itemCode)
    if (existing) {
      existing.quantity += item.quantity
    } else {
      cart.value.items.push(item)
    }
    recalculateCart()
  }

  const removeFromCart = (itemCode: string) => {
    cart.value.items = cart.value.items.filter(i => i.itemCode !== itemCode)
    recalculateCart()
  }

  const updateQuantity = (itemCode: string, quantity: number) => {
    const item = cart.value.items.find(i => i.itemCode === itemCode)
    if (item) {
      item.quantity = Math.max(1, quantity)
      recalculateCart()
    }
  }

  const applyCoupon = async (couponCode: string) => {
    try {
      isLoading.value = true
      const response = await api.call('all_trails.api.shop.validate_coupon', {
        code: couponCode,
        order_total: cart.value.subtotal
      })
      cart.value.appliedCoupon = couponCode
      cart.value.discountAmount = response.discount_amount
      recalculateCart()
    } catch (err) {
      error.value = 'Invalid coupon code'
    } finally {
      isLoading.value = false
    }
  }

  const recalculateCart = () => {
    cart.value.subtotal = cart.value.items.reduce((sum, item) => sum + item.lineTotal, 0)
    cart.value.taxAmount = cart.value.subtotal * 0.16  // 16% VAT in Kenya
    cart.value.shippingCost = calculateShipping()
    cart.value.total = cart.value.subtotal + cart.value.taxAmount + cart.value.shippingCost - (cart.value.discountAmount || 0)
  }

  const proceedToCheckout = async (paymentMethod: 'mpesa' | 'card' | 'bnpl') => {
    // Implementation in next section
  }

  const createOrder = async (orderData: any) => {
    try {
      isLoading.value = true
      const response = await api.call('all_trails.api.shop.create_order', orderData)
      orders.value.push(response)
      clearCart()
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearCart = () => {
    cart.value = { items: [], subtotal: 0, discountAmount: 0, shippingCost: 0, taxAmount: 0, total: 0 }
  }

  return {
    cart,
    orders,
    isLoading,
    error,
    addToCart,
    removeFromCart,
    updateQuantity,
    applyCoupon,
    proceedToCheckout,
    createOrder,
    clearCart
  }
})
```

---

## Payment Integration

### Payment Flows

#### Flow 1: Order Now (Full Payment - MPESA)

```
Customer Cart → "Pay Now" Button
    ↓
Merchandise Order (Draft) created
    ↓
Checkout Modal: Delivery Address & Phone
    ↓
Order Summary Review (Glass Card)
    ↓
MPESA Payment Modal
    ├─ STK Push via MPESA_TX
    ├─ Poll status every 3 seconds
    └─ 30-minute timeout
         ↓ (Success)
         └→ Payment Entry created
            └→ Sales Invoice generated
               └→ Sales Order linked
                  └→ Merchandise Order status: Confirmed
                     └→ Fulfillment: Processing
                        └→ Email confirmation sent
                           └→ Inventory reduced (Stock Entry)

         ↓ (Failed)
         └→ Merchandise Order status: Failed
            └→ User offered retry or cancel
```

**Implementation**:
- Reuse `MPESA_TX` architecture (idempotent callback handler)
- Create async verification job
- Handle duplicate callbacks gracefully
- Link MPESA Ticket → Merchandise Order

#### Flow 2: Order Later (BNPL - 2 Installments)

```
Customer Cart (Total: KES 6,500) → "Pay Later" Button
    ↓
BNPL Eligibility Check
    ├─ First-time buyer: KES limit 3,000 - 10,000
    ├─ Returning buyer: KES limit up to 25,000
    └─ No prior defaults
         ↓
         └→ BNPL Plan created (2 x KES 3,250)
            ├─ Payment 1: Today (50%)
            ├─ Payment 2: 30 days (50%)
            └─ 0% interest
                 ↓
                 └→ First MPESA payment (Flow 1)
                    ├─ Payment Entry created for first installment
                    ├─ Merchandise Order status: Confirmed
                    ├─ Fulfillment: Processing
                    └─ Email: "You have 1 pending payment due in 30 days"
                         ↓ (30 days later)
                         └→ Auto-retry MPESA second payment
                            ├─ 3 retries with 24-hour spacing
                            └─ Payment Entry created for second installment
                               └→ Merchandise Order fully paid
                                  └→ Email: "Payment complete. Thank you!"

         ↓ (Auto-payment fails 3x)
         └→ BNPL Plan marked: Defaulted
            └→ Email escalation to customer
               └→ Manual follow-up by support team
```

**Implementation**:
- BNPL Plan DocType with installment schedule
- Async background job: check due dates, auto-attempt MPESA payment
- Fallback: manual retry UI if auto-payment fails
- Credit worthiness: basic checks (first-time buyer limits)

#### Flow 3: Inventory Deduction

**Timing**: After payment confirmation, before fulfillment

```
Payment Entry submitted (via MPESA_TX)
    ↓
Sales Invoice automatically created
    ↓
Trigger: Sales Invoice.on_submit()
    ├─ Create Stock Entry (Material Issue)
    ├─ Link to Merchandise Order items
    ├─ Warehouse → Customer
    └─ Reduce stock quantities
         ↓
         └→ Stock Ledger Entry created
            └→ Real-time stock updated
               └→ Low-stock alerts if needed
```

**Edge Cases**:
- Overselling prevention: Check stock before confirming order
- Reserved stock: Mark items as reserved after payment until shipment
- Backorders: If stock insufficient, offer backorder with delivery estimate

---

## Backend API Endpoints

### Shop Service Layer (`all_trails/api/shop.py`)

```python
# all_trails/api/shop.py

import frappe
from frappe import _
from frappe.utils import now_datetime, add_days
from decimal import Decimal

@frappe.whitelist()
def get_merchandise_catalog(category=None, limit=20, offset=0):
    """
    GET /api/method/all_trails.api.shop.get_merchandise_catalog

    Returns active merchandise items with filtering

    Args:
        category: Optional category filter (string)
        limit: Items per page (default 20)
        offset: Pagination offset (default 0)

    Returns:
        {
            "items": [
                {
                    "item_code": "STR-BACKPACK-001",
                    "item_name": "Premium Hiking Backpack",
                    "category": "Hiking Gear",
                    "price": 8500,
                    "discount_price": 7200,
                    "rating": 4.5,
                    "reviews_count": 23,
                    "in_stock": true,
                    "stock_quantity": 15,
                    "image_url": "...",
                    "bnpl_eligible": true
                }
            ],
            "total_count": 87,
            "has_more": true
        }
    """
    filters = [['is_active', '=', True]]
    if category:
        filters.append(['category', '=', category])

    items = frappe.get_list(
        'Merchandise Item',
        filters=filters,
        fields=['item_code', 'item_name', 'category', 'selling_price', 'discount_price',
                'average_rating', 'review_count', 'warehouse', 'image_urls'],
        limit=limit,
        offset=offset,
        order_by='position_in_category asc'
    )

    # Enrich with stock
    for item in items:
        stock_balance = get_stock_balance(item['item_code'], item['warehouse'])
        item['in_stock'] = stock_balance > 0
        item['stock_quantity'] = stock_balance
        item['bnpl_eligible'] = item['selling_price'] >= 3000

    return {
        'items': items,
        'total_count': frappe.get_value('Merchandise Item', filters, 'count(*)'),
        'has_more': offset + limit < frappe.get_value('Merchandise Item', filters, 'count(*)')
    }


@frappe.whitelist()
def get_item_details(item_code):
    """
    GET /api/method/all_trails.api.shop.get_item_details?item_code=STR-BACKPACK-001

    Returns detailed item information with reviews
    """
    item = frappe.get_doc('Merchandise Item', item_code)

    reviews = frappe.get_list(
        'Merchandise Review',
        filters=[['item_code', '=', item_code], ['status', '=', 'Approved']],
        fields=['rating', 'title', 'review_text', 'customer', 'verified_purchase', 'helpful_count'],
        order_by='helpful_count desc',
        limit=10
    )

    return {
        'item_code': item.item_code,
        'item_name': item.item_name,
        'description': item.description_html,
        'price': item.selling_price,
        'discount_price': item.discount_price,
        'category': item.category,
        'sku': item.sku,
        'images': item.image_urls,
        'specifications': item.specifications,
        'care_instructions': item.care_instructions,
        'suitable_for_trails': item.suitable_for_trails,
        'hikers_who_bought': item.hikers_who_bought,
        'average_rating': item.average_rating,
        'reviews': reviews,
        'in_stock': get_stock_balance(item.item_code, item.warehouse) > 0,
        'bnpl_eligible': item.selling_price >= item.bnpl_min_amount
    }


@frappe.whitelist()
def validate_coupon(code, order_total):
    """
    POST /api/method/all_trails.api.shop.validate_coupon

    Validates promotional code and returns discount
    """
    coupon = frappe.get_value(
        'Promotional Code',
        {'code': code, 'active': True},
        ['discount_percentage', 'discount_amount', 'min_order_amount', 'max_uses', 'usage_count']
    )

    if not coupon:
        frappe.throw('Invalid or expired coupon code')

    discount_percent, discount_amt, min_amt, max_uses, usage_count = coupon

    if order_total < min_amt:
        frappe.throw(f'Coupon valid only for orders above KES {min_amt}')

    if usage_count >= max_uses:
        frappe.throw('Coupon usage limit reached')

    discount_amount = discount_amt or (order_total * discount_percent / 100)

    return {
        'valid': True,
        'discount_amount': discount_amount,
        'discount_percentage': discount_percent
    }


@frappe.whitelist()
def create_order(items, delivery_address, customer_phone, coupon_code=None, payment_method='mpesa'):
    """
    POST /api/method/all_trails.api.shop.create_order

    Creates Merchandise Order and initiates payment

    Args:
        items: List of {item_code, quantity}
        delivery_address: Delivery address string
        customer_phone: Phone for delivery & payment
        coupon_code: Optional promotional code
        payment_method: 'mpesa' or 'bnpl'

    Returns:
        {
            'order_id': 'MO-2024-0001',
            'total': 8500,
            'payment_method': 'mpesa',
            'mpesa_ticket_id': 'STK-...'  // if payment_method = mpesa
        }
    """
    user = frappe.session.user
    customer = frappe.get_doc('User', user)

    # Validate stock
    for item in items:
        stock = get_stock_balance(item['item_code'], get_warehouse())
        if stock < item['quantity']:
            frappe.throw(f"Insufficient stock for {item['item_code']}")

    # Create order
    order = frappe.new_doc('Merchandise Order')
    order.customer_id = customer.name
    order.customer_email = customer.email
    order.customer_phone = customer_phone
    order.payment_method = payment_method
    order.shipping_address = delivery_address

    # Add items
    subtotal = Decimal('0')
    for item_data in items:
        item = frappe.get_doc('Merchandise Item', item_data['item_code'])
        order.append('items', {
            'item_code': item.item_code,
            'quantity': item_data['quantity'],
            'unit_price': item.selling_price,
            'discount_percentage': 0,
            'line_total': item.selling_price * item_data['quantity']
        })
        subtotal += Decimal(str(item.selling_price * item_data['quantity']))

    # Apply coupon
    if coupon_code:
        discount = frappe.get_value('Promotional Code', {'code': coupon_code}, 'discount_amount') or 0
        order.discount_amount = discount

    # Calculate totals
    order.subtotal = float(subtotal)
    order.tax_amount = float(subtotal) * 0.16  # 16% VAT
    order.shipping_cost = calculate_shipping(delivery_address)
    order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost - (order.discount_amount or 0)

    order.insert()

    # Initiate payment
    if payment_method == 'mpesa':
        return initiate_mpesa_payment(order.name, customer_phone)
    elif payment_method == 'bnpl':
        return initiate_bnpl_payment(order.name, customer_phone)


@frappe.whitelist()
def initiate_mpesa_payment(order_id, phone_number):
    """
    Initiates MPESA STK push for merchandise order
    Uses MPESA_TX architecture
    """
    order = frappe.get_doc('Merchandise Order', order_id)

    # Create MPESA Ticket
    ticket = frappe.new_doc('MPESA Ticket')
    ticket.name = frappe.generate_hash(length=16)
    ticket.msisdn = phone_number
    ticket.amount = order.total_amount
    ticket.account_number = order_id  # Link to merchandise order
    ticket.description = f'Merchandise Order {order_id}'
    ticket.ticket_status = 'Initiated'
    ticket.insert()

    # Initiate STK push
    from mpesa_tx.api.mpesa_handler import MPESAHandler
    handler = MPESAHandler()
    response = handler.initiate_stk_push(
        phone_number=phone_number,
        amount=int(order.total_amount),
        account_reference=order_id
    )

    if response['ResponseCode'] == '0':
        # Success
        order.payment_status = 'Pending'
        order.save()

        return {
            'success': True,
            'order_id': order_id,
            'ticket_id': ticket.name,
            'total': order.total_amount,
            'message': 'STK push sent. Enter PIN on your phone.'
        }
    else:
        frappe.throw(f"Payment initiation failed: {response.get('ResponseDesc')}")


def initiate_bnpl_payment(order_id, phone_number):
    """
    Initiates BNPL (2-installment) payment
    """
    order = frappe.get_doc('Merchandise Order', order_id)

    # Create BNPL Plan
    plan = frappe.new_doc('BNPL Plan')
    plan.merchandise_order = order_id
    plan.total_amount = order.total_amount
    plan.installment_count = 2
    plan.installment_amount = order.total_amount / 2
    plan.first_payment_date = frappe.utils.today()
    plan.payment_frequency = 'Monthly'
    plan.payment_method = 'mpesa'
    plan.status = 'Active'

    # Add installments
    plan.append('installments', {
        'installment_number': 1,
        'due_date': frappe.utils.today(),
        'amount': order.total_amount / 2,
        'payment_status': 'Pending'
    })
    plan.append('installments', {
        'installment_number': 2,
        'due_date': add_days(frappe.utils.today(), 30),
        'amount': order.total_amount / 2,
        'payment_status': 'Pending'
    })

    plan.insert()

    # Initiate first payment
    order.bnpl_plan_id = plan.name
    order.payment_mode = 'Installment'
    order.bnpl_total_installments = 2
    order.bnpl_remaining_installments = 2
    order.save()

    return initiate_mpesa_payment(order_id, phone_number)


@frappe.whitelist()
def get_order_status(order_id):
    """
    GET /api/method/all_trails.api.shop.get_order_status?order_id=MO-2024-0001

    Returns current order status
    """
    order = frappe.get_doc('Merchandise Order', order_id)

    return {
        'order_id': order.name,
        'status': order.fulfillment_status,
        'payment_status': order.payment_status,
        'payment_method': order.payment_method,
        'total': order.total_amount,
        'items': [
            {'item_code': item.item_code, 'quantity': item.quantity, 'price': item.unit_price}
            for item in order.items
        ],
        'shipping_address': order.shipping_address,
        'estimated_delivery': order.estimated_delivery_date,
        'tracking_number': order.tracking_number
    }


# Helper functions

def get_stock_balance(item_code, warehouse):
    """Query current stock balance"""
    from erpnext.stock.utils import get_stock_balance as erpnext_get_stock_balance
    return erpnext_get_stock_balance(item_code, warehouse) or 0

def get_warehouse():
    """Get default warehouse for merchandise"""
    return frappe.get_value('Stock Settings', filters={}, fieldname='default_warehouse') or 'Stores'

def calculate_shipping(delivery_address):
    """Calculate shipping cost based on address"""
    # Simple logic: KES 300 flat + distance-based
    # In production, integrate with shipping provider API
    return 300
```

### Payment Callback Handler (Integration with MPESA_TX)

```python
# all_trails/api/payment_handler.py

import frappe
from frappe.utils import now_datetime
from mpesa_tx.api.callback_handler import MPESACallbackHandler

class MerchandisePaymentHandler(MPESACallbackHandler):
    """
    Extended callback handler for merchandise orders
    Links MPESA callback to Merchandise Order
    """

    def handle(self) -> dict:
        """Override parent to link merchandise order"""
        try:
            # Get merchandise order from account_number (mapped in initiate_mpesa_payment)
            order_id = self.checkout_request_id  # Actually: merchandise order ID
            order = frappe.get_doc('Merchandise Order', order_id)

            # Call parent handler
            result = super().handle()

            if result['success']:
                # Update merchandise order
                if self.result_code == 0:  # Success
                    order.payment_status = 'Completed'
                    order.fulfillment_status = 'Confirmed'
                else:
                    order.payment_status = 'Failed'

                order.save()

            return result
        except Exception as e:
            frappe.logger().error(f"Merchandise payment error: {str(e)}")
            raise


@frappe.whitelist(allow_guest=True)
def handle_merchandise_payment_callback():
    """
    Webhook endpoint for merchandise payment callbacks
    Route: POST /api/method/all_trails.api.payment_handler.handle_merchandise_payment_callback
    """
    from flask import request

    try:
        payload = request.get_json() or {}
        handler = MerchandisePaymentHandler(payload)
        result = handler.handle()

        return {
            'ResultCode': 0 if result['success'] else 1,
            'ResultDesc': result['message']
        }
    except Exception as e:
        frappe.logger().error(f"Merchandise callback error: {str(e)}")
        return {
            'ResultCode': 0,
            'ResultDesc': 'Callback received'
        }
```

---

## Data Schema & Relationships

### Entity Relationship Diagram

```
┌─────────────────────┐
│  Merchandise Item   │
├─────────────────────┤
│ item_code (PK)      │ ◄─────┐
│ item_name           │       │
│ category            │       │ 1:N
│ selling_price       │       │
│ warehouse           │       │
└─────────────────────┘       │
                              │
                    ┌─────────────────────┐
                    │ Merchandise Order   │
                    ├─────────────────────┤
                    │ order_id (PK)       │
                    │ customer_id         │ ──┐
                    │ payment_method      │   │ N:1
                    │ total_amount        │   │
                    │ bnpl_plan_id        │   │
                    │ sales_order_id      │   │
                    │ sales_invoice_id    │   │
                    └─────────────────────┘   │
                             │ │              │
                    ┌────────┴─┴──────┐       │
                    │                 │       │
              1:N   │                 │ N:1   │
                    ▼                 ▼       │
         ┌──────────────────┐  ┌──────────────────┐
         │ BNPL Plan        │  │ Contact/User     │
         ├──────────────────┤  ├──────────────────┤
         │ plan_id (PK)     │  │ name (PK)        │
         │ total_amount     │  │ email            │
         │ installment_count│  │ phone            │
         └──────────────────┘  └──────────────────┘
                    │
             1:N    │
                    ▼
         ┌──────────────────┐
         │ Installment      │
         ├──────────────────┤
         │ id (PK)          │
         │ due_date         │
         │ amount           │
         │ payment_entry_id │
         └──────────────────┘
                    │
             N:1    │
                    ▼
         ┌──────────────────┐
         │ Payment Entry    │
         │ (ERPNext)        │
         └──────────────────┘

        ┌──────────────────────────────────────┐
        │ Merchandise Order ──► Sales Order    │
        │                    (ERPNext linking) │
        │                                      │
        │ Merchandise Order ──► Sales Invoice  │
        │                    (ERPNext linking) │
        │                                      │
        │ Merchandise Order ──► Payment Entry  │
        │                    (ERPNext linking) │
        └──────────────────────────────────────┘
```

### Database Tables

```sql
-- Additional indices for performance

CREATE INDEX idx_merchandise_item_category ON `tabMerchandise Item` (category, is_active);
CREATE INDEX idx_merchandise_item_warehouse ON `tabMerchandise Item` (warehouse, is_active);
CREATE INDEX idx_merchandise_order_customer ON `tabMerchandise Order` (customer_id, order_date);
CREATE INDEX idx_merchandise_order_status ON `tabMerchandise Order` (fulfillment_status, payment_status);
CREATE INDEX idx_bnpl_plan_status ON `tabBNPL Plan` (status, next_payment_date);
CREATE INDEX idx_bnpl_installment_due ON `tabBNPL Installment` (due_date, payment_status);
```

---

## Background Jobs & Automation

### Scheduled Tasks

#### 1. BNPL Payment Auto-Retry (Hourly)

```python
# all_trails/tasks.py

@frappe.whitelist()
def process_bnpl_payments():
    """
    Scheduled job: Every hour
    Attempts auto-payment for due BNPL installments
    """
    # Find due installments
    due_installments = frappe.get_list(
        'BNPL Installment',
        filters=[
            ['payment_status', '=', 'Pending'],
            ['due_date', '<=', frappe.utils.today()]
        ],
        fields=['name', 'amount', 'plan'],
        limit=100
    )

    for installment_record in due_installments:
        plan = frappe.get_doc('BNPL Plan', installment_record['plan'])
        order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

        try:
            # Attempt MPESA payment
            response = initiate_mpesa_payment(order.name, order.customer_phone)

            if response['success']:
                installment = frappe.get_doc('BNPL Installment', installment_record['name'])
                installment.payment_status = 'Paid'
                installment.payment_date = now_datetime()
                installment.save()
        except Exception as e:
            frappe.logger().warning(f"Auto-retry failed for {installment_record['name']}: {str(e)}")


@frappe.whitelist()
def send_bnpl_reminders():
    """
    Scheduled job: Daily at 9 AM
    Sends payment reminders for upcoming BNPL installments (3 days before)
    """
    reminder_date = add_days(frappe.utils.today(), 3)

    due_soon = frappe.get_list(
        'BNPL Installment',
        filters=[
            ['payment_status', '=', 'Pending'],
            ['due_date', '=', reminder_date]
        ],
        fields=['name', 'plan', 'amount']
    )

    for inst_record in due_soon:
        plan = frappe.get_doc('BNPL Plan', inst_record['plan'])
        order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

        frappe.sendmail(
            recipients=[order.customer_email],
            subject='Reminder: Payment Due for All Trails Order',
            template='bnpl_payment_reminder',
            args={
                'order_id': order.name,
                'amount': inst_record['amount'],
                'due_date': inst_record['due_date'],
                'payment_link': f"{frappe.utils.get_url()}/order/{order.name}"
            }
        )


@frappe.whitelist()
def update_low_stock_alerts():
    """
    Scheduled job: Every 6 hours
    Updates low stock status and sends alerts
    """
    from erpnext.stock.utils import get_stock_balance

    low_stock_items = frappe.get_list(
        'Merchandise Item',
        filters=[['is_active', '=', True]],
        fields=['item_code', 'item_name', 'warehouse', 'low_stock_threshold'],
        limit=500
    )

    for item in low_stock_items:
        balance = get_stock_balance(item['item_code'], item['warehouse'])

        if balance <= item['low_stock_threshold']:
            frappe.logger().warning(
                f"Low stock alert: {item['item_code']} ({balance} units)"
            )
            # Send email to inventory manager
            send_low_stock_alert(item)
```

#### 2. Merchandise Order Fulfillment Automation

```python
@frappe.whitelist()
def auto_confirm_orders():
    """
    Scheduled job: Every 30 minutes
    Confirms orders with full payment received
    """
    orders_to_confirm = frappe.get_list(
        'Merchandise Order',
        filters=[
            ['fulfillment_status', '=', 'Pending'],
            ['payment_status', '=', 'Completed'],
            ['creation', '<=', add_hours(now_datetime(), -1)]  # At least 1 hour old
        ],
        fields=['name'],
        limit=50
    )

    for order_record in orders_to_confirm:
        order = frappe.get_doc('Merchandise Order', order_record['name'])

        # Create Sales Order and Invoice
        try:
            create_sales_order(order)
            order.fulfillment_status = 'Processing'
            order.save()

            frappe.logger().info(f"Order {order.name} confirmed and processing")
        except Exception as e:
            frappe.logger().error(f"Order confirmation failed: {str(e)}")
            order.add_comment('Comment', f'Confirmation failed: {str(e)}', 'Alert')
```

#### 3. Inventory Reduction (On Sales Invoice Submission)

```python
# In Merchandise Order DocType

def on_sales_invoice_submitted(sales_invoice):
    """
    Hook: When Sales Invoice is submitted
    Creates Stock Entry to reduce inventory
    """
    # Find linked Merchandise Order
    order = frappe.get_doc('Merchandise Order', sales_invoice.custom_merchandise_order_id)

    # Create Stock Entry
    stock_entry = frappe.new_doc('Stock Entry')
    stock_entry.stock_entry_type = 'Material Issue'
    stock_entry.company = frappe.defaults.get_user_default('company')
    stock_entry.posting_date = frappe.utils.today()

    for item in order.items:
        stock_entry.append('items', {
            'item_code': item.item_code,
            'qty': item.quantity,
            's_warehouse': get_warehouse(),
            't_warehouse': None,  # Issue to customer
            'basic_rate': item.unit_price
        })

    stock_entry.insert()
    stock_entry.submit()

    frappe.logger().info(f"Inventory reduced for order {order.name}")
```

---

## Security & Compliance

### Payment Security

1. **Signature Verification**
   - All MPESA callbacks validated with HMAC-SHA256
   - Constant-time comparison to prevent timing attacks
   - Missing signature = request rejected

2. **Idempotency**
   - Duplicate callbacks with same CheckoutRequestID ignored
   - State machine prevents double-processing
   - Payment Entry created once per transaction

3. **PCI Compliance**
   - No card storage (MPESA handles)
   - No payment data logged
   - Sensitive fields encrypted at rest

### Data Protection

1. **PII Handling**
   - Phone numbers masked in UI (show last 4 digits)
   - Customer email stored securely
   - Delivery addresses encrypted

2. **Audit Trail**
   - All order status changes logged with timestamp
   - Payment transitions recorded
   - Admin can view full history

3. **GDPR Compliance**
   - User can request data export
   - Right to be forgotten: anonymize old orders (>2 years)
   - Consent management for marketing emails

---

## Testing Strategy

### Unit Tests

```python
# tests/test_shop_api.py

def test_get_merchandise_catalog():
    """Test catalog retrieval with pagination"""
    result = frappe.get_method('all_trails.api.shop.get_merchandise_catalog')(limit=10)
    assert 'items' in result
    assert len(result['items']) <= 10

def test_validate_coupon():
    """Test coupon validation"""
    # Create test coupon
    coupon = frappe.new_doc('Promotional Code')
    coupon.code = 'TEST10'
    coupon.discount_percentage = 10
    coupon.active = True
    coupon.insert()

    result = frappe.get_method('all_trails.api.shop.validate_coupon')('TEST10', 5000)
    assert result['valid']
    assert result['discount_amount'] == 500

def test_merchandise_order_creation():
    """Test order creation with stock validation"""
    items = [{'item_code': 'ITEM-001', 'quantity': 1}]
    result = frappe.get_method('all_trails.api.shop.create_order')(
        items=items,
        delivery_address='123 Main St',
        customer_phone='254700000000'
    )
    assert 'order_id' in result
    assert result['total'] > 0

def test_bnpl_plan_creation():
    """Test BNPL plan logic"""
    order = create_test_order(total=6000)
    plan = frappe.new_doc('BNPL Plan')
    plan.merchandise_order = order.name
    plan.total_amount = 6000
    plan.installment_count = 2
    plan.insert()

    assert len(plan.installments) == 2
    assert plan.installments[0].amount == 3000
    assert plan.installments[1].due_date > plan.installments[0].due_date
```

### Integration Tests

```python
# tests/test_shop_integration.py

def test_full_order_to_payment_flow():
    """Test complete: Order → Payment → Invoice → Inventory"""
    # 1. Create order
    order = create_test_merchandise_order()

    # 2. Simulate MPESA callback
    callback_payload = create_mpesa_callback(
        checkout_request_id=order.mpesa_ticket_id,
        result_code=0
    )
    response = frappe.get_method('all_trails.api.payment_handler.handle_merchandise_payment_callback')(
        json.dumps(callback_payload)
    )
    assert response['ResultCode'] == 0

    # 3. Verify order updated
    order.reload()
    assert order.payment_status == 'Completed'

    # 4. Verify Sales Invoice created
    invoices = frappe.get_list('Sales Invoice', {'merchandise_order_id': order.name})
    assert len(invoices) == 1

    # 5. Verify stock reduced
    stock_balance = get_stock_balance(order.items[0].item_code, 'Stores')
    assert stock_balance < initial_stock

def test_bnpl_installment_auto_payment():
    """Test auto-retry of BNPL payments"""
    # 1. Create BNPL plan with 2 installments
    plan = create_test_bnpl_plan()

    # 2. Verify first installment paid
    assert plan.installments[0].payment_status == 'Paid'

    # 3. Simulate 30 days passing
    frappe.utils.now = lambda: add_days(now_datetime(), 30)

    # 4. Run auto-payment job
    frappe.get_method('all_trails.tasks.process_bnpl_payments')()

    # 5. Verify second installment attempted
    plan.reload()
    assert plan.installments[1].payment_status in ['Paid', 'Pending']

def test_duplicate_callback_handling():
    """Test idempotency: same callback twice = one order"""
    callback = create_mpesa_callback()

    # Send same callback twice
    response1 = handle_callback(callback)
    response2 = handle_callback(callback)

    # Both should succeed
    assert response1['ResultCode'] == 0
    assert response2['ResultCode'] == 0

    # But only one payment entry should exist
    payment_entries = frappe.get_list('Payment Entry', {
        'reference_no': callback['CheckoutRequestID']
    })
    assert len(payment_entries) == 1
```

### E2E Tests (Frontend)

```typescript
// tests/e2e/shopping.spec.ts

describe('Shopping Cart & Checkout Flow', () => {
  it('should allow user to browse and purchase merchandise', async () => {
    // 1. Navigate to shop
    await page.goto('/all-trails/shop')

    // 2. Browse catalog
    const items = await page.$$('.glass-product-card')
    expect(items.length).toBeGreaterThan(0)

    // 3. Add item to cart
    await items[0].click()
    await page.click('[data-test=add-to-cart]')

    // 4. Verify cart updated
    const cartCount = await page.textContent('[data-test=cart-count]')
    expect(cartCount).toBe('1')

    // 5. Open cart
    await page.click('[data-test=cart-button]')

    // 6. Proceed to checkout
    await page.click('[data-test=checkout-button]')

    // 7. Fill delivery address
    await page.fill('[name=delivery_address]', '123 Main St')

    // 8. Select payment method
    await page.click('[data-test=payment-now]')

    // 9. Verify MPESA modal
    await page.waitForSelector('[data-test=mpesa-modal]')
    expect(await page.isVisible('[data-test=mpesa-modal]')).toBeTruthy()
  })
})
```

---

## Deployment Plan

### Pre-Launch Checklist

- [ ] Database schema: All new DocTypes created and migrated
- [ ] Frontend components: All glass components built and tested
- [ ] Payment integration: MPESA_TX linkage complete
- [ ] ERPNext workflows: Sales Order → Invoice → Payment configured
- [ ] Inventory: Test warehouse setup, stock entries working
- [ ] BNPL: Auto-payment scheduling configured
- [ ] Email templates: Confirmation, reminder, receipt emails created
- [ ] Analytics: Track conversion metrics, order value, repeat rates
- [ ] Security: Payment signature validation tested
- [ ] Load testing: 100 concurrent users × 1000 orders
- [ ] UAT: End-to-end flows by actual users
- [ ] Documentation: API docs, user guides, admin guides
- [ ] Monitoring: Alerts for failed payments, low stock, BNPL defaults
- [ ] Rollback plan: Documented steps to revert changes

### Launch Phases

**Phase 2a (Week 1-2)**: MVP Launch
- 50 products (gear + apparel)
- Single warehouse inventory
- Order now (MPESA full payment)
- Basic UI (glass cart, product list)
- Internal testing only

**Phase 2b (Week 3-4)**: BNPL & Full Release
- Order later (BNPL 2-installment)
- Auto-retry background jobs
- Public launch with marketing push
- Monitor first 100 orders carefully
- 24/7 support standby

**Phase 2c (Week 5)**: Optimization & Expansion
- Expand product catalog to 100+ items
- Add experience products & guidebooks
- Implement product recommendations
- Multi-warehouse support
- Advanced reporting (inventory, sales, margins)

---

## Success Metrics & KPIs

### Business Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Merchandise Revenue | KES 500K/month | Sales Invoice total |
| Order Conversion Rate | 8-12% | Merchandise orders / hiking bookings |
| Average Order Value | KES 2,500-3,500 | Total amount / order count |
| Repeat Purchase Rate | 25%+ | Customers with 2+ orders |
| BNPL Adoption | 40%+ | BNPL orders / total orders |
| Payment Success Rate | 95%+ | Successful payments / attempts |
| Customer Satisfaction | 4.5+/5.0 | Average review rating |
| Operational Margin | 15%+ | (Revenue - COGS - Fulfillment) / Revenue |

### Operational Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Order Fulfillment Time | <24 hours | Confirmed → Shipped |
| Payment Processing Time | <5 minutes | Order created → Payment confirmed |
| Inventory Accuracy | 99%+ | Physical count / system count |
| BNPL Default Rate | <2% | Defaulted / total BNPL orders |
| System Uptime | 99.9% | (Total time - downtime) / total time |
| Page Load Time | <2 seconds | Shop catalog page |
| API Response Time | <500ms | 95th percentile |

### User Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cart Abandonment Rate | <40% | Carts abandoned / carts created |
| Checkout Completion Time | <3 minutes | Add to cart → Payment success |
| Mobile Conversion | 60%+ | Mobile orders / total orders |
| Review Submission Rate | 30%+ | Reviews / delivered orders |
| Support Ticket Rate | <5% | Tickets / orders |

---

## Timeline & Resource Estimate

### Development Timeline: 4 Weeks

| Week | Task | Owner | Deliverable |
|------|------|-------|-------------|
| W1 | Backend: DocTypes, API endpoints | Backend Lead | All CRUD endpoints working |
| W1 | Frontend: Glass components | Frontend Lead | Reusable component library |
| W2 | MPESA integration | Payments Team | Payment flow working end-to-end |
| W2 | ERPNext workflows | Backend Lead | Sales Order → Invoice → Stock Entry |
| W3 | BNPL implementation | Backend Lead | Auto-payment scheduling working |
| W3 | Testing & bug fixes | QA Lead | All unit & integration tests passing |
| W4 | UAT & refinements | Product Manager | Launch ready with customer feedback |
| W4 | Deployment & monitoring | DevOps Lead | Live on production with alerts |

### Resource Requirements

- **Backend Engineer**: 1.5 FTE (80 hours)
- **Frontend Engineer**: 1.5 FTE (85 hours)
- **QA Engineer**: 0.75 FTE (35 hours)
- **DevOps/Infrastructure**: 0.5 FTE (25 hours)
- **Product Manager**: 0.5 FTE (oversight)
- **Total**: ~230 hours, 4 weeks

---

## Risk Assessment

### High-Risk Items

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| MPESA API downtime during launch | Revenue loss, reputational damage | Medium | Fallback payment method (card), queue callbacks |
| Overselling (inventory sync lag) | Customer unhappiness, refunds | Medium | Real-time stock checks, reserved inventory |
| BNPL payment default surge | Revenue loss, write-offs | Medium | Conservative credit limits, escalation process |
| Payment callback losses | Unreconciled orders, disputes | Medium | Idempotent handlers, webhook retries, audit logs |

### Medium-Risk Items

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| Slow page load (high product count) | Reduced conversion | Medium | Product pagination, caching, CDN |
| Poor mobile UX | <50% mobile conversion | Medium | Mobile-first design, test on real devices |
| Customer support overload | CSAT <4.0 | Low | Comprehensive FAQ, auto-replies, clear shipping info |

---

## Next Steps

1. **Design Review** (2 days)
   - Frontend team reviews glass component specs
   - Backend team reviews DocType schema
   - Payment team validates MPESA integration

2. **Approval & Kickoff** (1 day)
   - Product stakeholder sign-off
   - Team planning & sprint setup
   - Development environment setup

3. **Parallel Development** (3 weeks)
   - Backend: API & DocTypes in parallel with frontend UI
   - Integration testing checkpoints at end of each week
   - Daily standup for blockers

4. **QA & Launch** (1 week)
   - Full regression testing
   - Load testing
   - UAT with internal & beta users
   - Final deployment & monitoring

---

## Appendices

### A. Glassmorphic Design Tokens

See `UIUX.md` for complete design system documentation

### B. MPESA_TX Integration Reference

See `MPESA_REFACTOR.md` for payment architecture details

### C. ERPNext Configuration

- Stock Settings: Default warehouse → "Merchandise Store"
- Accounting: Debtors account, Sales account configured
- Taxes: 16% VAT set up for merchandise items
- Payment Terms: "Net 30" for wholesale, "Immediate" for retail

### D. Email Templates Required

1. `merchandise_order_confirmation.html` - Order confirmed
2. `merchandise_shipping_notification.html` - Item shipped
3. `merchandise_delivery_confirmation.html` - Delivered
4. `bnpl_payment_reminder.html` - Installment due soon
5. `bnpl_payment_failure_alert.html` - Payment failed, retry scheduled
6. `merchandise_review_request.html` - Request review after delivery
7. `merchandise_reorder_notification.html` - Previously purchased items

### E. Analytics & Reporting

**Reports to Build**:
- Merchandise Sales by Category (weekly)
- BNPL Plan Performance (default rates, collection %age)
- Inventory Turnover (items sold vs. in stock)
- Customer Repeat Purchase Analysis
- Revenue Attribution (from hiking bookings vs. standalone)

---

**Document Prepared By**: Product & Engineering Team
**Last Updated**: 2026-03-14
**Version**: 1.0 - DRAFT

---

*This BRD is a living document. Changes may be requested during development based on technical feasibility or market feedback.*
