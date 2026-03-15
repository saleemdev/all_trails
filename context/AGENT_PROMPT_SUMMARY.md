# All Trails Phase 2: AI Agent Implementation Prompt (Summary)

## Quick Reference for AI Agent

You are tasked with implementing the complete Phase 2 Merchandise System for All Trails. Here's what you need to do:

### 📋 Resources Available

1. **Detailed Technical Specifications**: `TECHNICAL_SPECS_PHASE_2.md`
   - Backend DocType schemas
   - API endpoint specifications
   - Payment flow implementations
   - Background job specs

2. **UI/UX Wireframes**: `WIREFRAMES_PHASE_2.md`
   - Mobile & desktop layouts
   - Component designs
   - Design system tokens
   - Responsive breakpoints

3. **Business Requirements**: `PHASE_2_BRD_MERCHANDISE_SYSTEM.md`
   - Complete feature list
   - Success metrics
   - Timeline & resources
   - Risk assessment

### 🎯 Phase Breakdown (4 Weeks)

#### Phase 1: Setup (Days 1-2)
- [ ] Environment verification
- [ ] Dependency checks
- [ ] Codebase pattern review
- [ ] Database schema validation

#### Phase 2: Backend (Days 3-7)
- [ ] Create 5 DocTypes (Item, Order, BNPL Plan, Review, Category)
- [ ] Implement 8+ API endpoints
- [ ] Create 4+ background jobs
- [ ] Build 7+ email templates

#### Phase 3: Frontend (Days 8-14)
- [ ] Build 8+ glass components
- [ ] Create 7+ shop pages
- [ ] Implement Pinia store
- [ ] Create API client service

#### Phase 4: Testing (Days 15-21)
- [ ] MPESA integration tests
- [ ] BNPL integration tests
- [ ] API endpoint tests
- [ ] Component tests
- [ ] Load testing

#### Phase 5: Launch (Days 22-28)
- [ ] Pre-deployment checklist
- [ ] Database migration
- [ ] Deployment steps
- [ ] Monitoring setup
- [ ] Support team training

### 🔧 Key Implementation Tasks

#### Backend (Python/Frappe)

1. **5 DocTypes to Create**
   ```
   - Merchandise Item (product catalog)
   - Merchandise Order (order record)
   - BNPL Plan (installment schedule)
   - Merchandise Review (ratings & feedback)
   - Merchandise Category (product hierarchy)
   ```

2. **8+ API Endpoints** (in `all_trails/api/shop.py`)
   ```python
   - get_merchandise_catalog() - Browse products with filters
   - get_item_details() - Product details + reviews
   - validate_coupon() - Validate promo codes
   - create_order() - Create order, initiate payment
   - initiate_mpesa_payment() - STK push for MPESA
   - initiate_bnpl_payment() - Create BNPL plan
   - handle_merchandise_payment_callback() - MPESA callback handler
   - get_order_status() - Track order
   ```

3. **4+ Background Jobs** (in `all_trails/tasks.py`)
   ```
   - process_bnpl_payments() - Auto-retry due installments (hourly)
   - send_bnpl_payment_reminders() - Email reminders (daily)
   - update_low_stock_alerts() - Inventory alerts (6 hourly)
   - auto_confirm_orders() - Create invoices (30 min)
   ```

4. **Email Templates** (7 templates for customer communication)
   ```
   - Order confirmation
   - Shipping notification
   - Delivery confirmation
   - BNPL payment reminder
   - BNPL payment failure
   - Review request
   - Low stock alert (internal)
   ```

#### Frontend (Vue 3/TypeScript)

1. **8+ Glass Components** (in `frontend/src/components/glass/`)
   ```vue
   - GlassCard.vue - Base container with glass effect
   - GlassButton.vue - Interactive button (primary/secondary)
   - GlassInput.vue - Form input with validation
   - GlassModal.vue - Modal dialog overlay
   - GlassProductCard.vue - Product display card
   - GlassCart.vue - Shopping cart display
   - GlassCheckoutFlow.vue - Multi-step checkout
   - Plus: Checkbox, Radio, Select, Alert, Spinner
   ```

2. **7+ Shop Pages** (in `frontend/src/pages/shop/`)
   ```vue
   - Browse.vue - Catalog with filters
   - Detail.vue - Product detail view
   - Cart.vue - Shopping cart
   - Checkout.vue - Multi-step checkout (3 steps)
   - PaymentProcessing.vue - MPESA STK display
   - Confirmation.vue - Order confirmation
   - Tracking.vue - Order tracking
   ```

3. **Pinia Store** (in `frontend/src/stores/merchandiseStore.ts`)
   ```typescript
   State: cart, products, currentProduct, currentOrder, paymentStatus
   Actions: addToCart, removeFromCart, createOrder, getOrderStatus
   Getters: cartTotal, cartItemCount, isCheckoutValid
   ```

4. **API Client** (in `frontend/src/services/shopApi.ts`)
   ```typescript
   - getCatalog(filters, pagination)
   - getProductDetails(itemCode)
   - createOrder(orderData)
   - getOrderStatus(orderId)
   - validateCoupon(code, total)
   - initiatePayment(orderId, phone)
   - checkPaymentStatus(ticketId)
   ```

### 💾 Directory Structure to Create

```
all_trails/
├── doctype/
│   ├── merchandise_item/
│   │   ├── merchandise_item.json
│   │   └── merchandise_item.py
│   ├── merchandise_order/
│   │   ├── merchandise_order.json
│   │   └── merchandise_order.py
│   ├── bnpl_plan/
│   │   ├── bnpl_plan.json
│   │   └── bnpl_plan.py
│   ├── merchandise_review/
│   │   ├── merchandise_review.json
│   │   └── merchandise_review.py
│   └── merchandise_category/
│       ├── merchandise_category.json
│       └── merchandise_category.py
├── api/
│   ├── shop.py (8+ endpoints)
│   └── payment_handler.py (MPESA integration)
├── tasks.py (4+ background jobs)
├── templates/
│   ├── merchandise_order_confirmation.html
│   ├── merchandise_shipping_notification.html
│   ├── bnpl_payment_reminder.html
│   └── (3+ more)
└── migrations/
    └── 0001_create_merchandise_doctypes.py

frontend/src/
├── components/glass/
│   ├── GlassCard.vue
│   ├── GlassButton.vue
│   ├── GlassInput.vue
│   ├── GlassModal.vue
│   ├── GlassProductCard.vue
│   ├── GlassCart.vue
│   ├── GlassCheckoutFlow.vue
│   └── (2+ more)
├── pages/shop/
│   ├── Browse.vue
│   ├── Detail.vue
│   ├── Cart.vue
│   ├── Checkout.vue
│   ├── PaymentProcessing.vue
│   ├── Confirmation.vue
│   └── Tracking.vue
├── stores/
│   └── merchandiseStore.ts
├── services/
│   └── shopApi.ts
└── types/
    └── shop.ts
```

### 🔌 Integration Points

1. **MPESA_TX Module** (existing payment system)
   - Use `MPESAHandler` for STK push
   - Extend callback handler for merchandise orders
   - Link MPESA Ticket → Merchandise Order
   - Verify idempotent callback processing

2. **ERPNext DocTypes**
   - Sales Order (created from Merchandise Order)
   - Sales Invoice (created on payment success)
   - Payment Entry (links payment to invoice)
   - Stock Entry (reduces inventory)
   - Warehouse (inventory location)

3. **Frappe Features**
   - Background jobs via `frappe.enqueue()`
   - Scheduler for cron jobs
   - Email templates & sending
   - Document workflows
   - Permissions & validation

### ✅ Success Criteria

- [ ] All 5 DocTypes created & tested
- [ ] All 8+ API endpoints functional
- [ ] All 7+ shop pages responsive & working
- [ ] MPESA payment flow end-to-end tested
- [ ] BNPL 2-installment flow working
- [ ] >90% test coverage on critical paths
- [ ] Handles 100+ concurrent users
- [ ] Payment success rate >95%
- [ ] Deployed to production
- [ ] No critical errors in logs

### 📊 Testing Checklist

**Backend:**
- [ ] All DocType validations work
- [ ] API endpoints return correct data
- [ ] MPESA idempotency verified
- [ ] BNPL auto-retry working
- [ ] Callbacks processed correctly
- [ ] Background jobs run on schedule

**Frontend:**
- [ ] All components render without errors
- [ ] All pages load and display correctly
- [ ] Forms validate input properly
- [ ] Cart calculations correct
- [ ] Checkout flow complete
- [ ] Payment processing works
- [ ] Order tracking updates
- [ ] Mobile responsive (375px, 768px, 1024px+)

**Integration:**
- [ ] Create order → MPESA STK push → Payment → Invoice
- [ ] Create order → BNPL plan → First payment → Schedule second
- [ ] Callback received → Order confirmed → Inventory reduced
- [ ] BNPL auto-retry → Second payment success
- [ ] Stock checks prevent overselling
- [ ] Emails sent at all key points

### 🚀 Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Security reviewed
- [ ] Database migrated
- [ ] API documentation complete
- [ ] Email templates tested
- [ ] Error handling comprehensive
- [ ] Logging configured
- [ ] Monitoring alerts setup
- [ ] Initial product data seeded
- [ ] Payment webhook configured
- [ ] Support team trained

### 📚 Reference Documents

1. **TECHNICAL_SPECS_PHASE_2.md** - Detailed backend & frontend specifications
2. **WIREFRAMES_PHASE_2.md** - UI/UX designs & layout specifications
3. **PHASE_2_BRD_MERCHANDISE_SYSTEM.md** - Complete business requirements
4. **MPESA_REFACTOR.md** - Payment callback architecture
5. **UIUX.md** - Design system (if available)

### 🎨 Design System

**Glass Effect CSS Variables:**
```css
--glass-bg: rgba(27, 58, 45, 0.85)
--glass-backdrop-blur: 30px (desktop), 20px (mobile)
--glass-border: rgba(255, 255, 255, 0.2)
--accent-orange: #E85D1F
--accent-success: #10B981
--color-text: #F5F5F5
```

**Typography:**
- Display: Sora Bold 32px/48px
- Heading: Sora SemiBold 20px/24px
- Body: Inter Regular 16px
- Price: JetBrains Mono 18px

**Responsive Breakpoints:**
- Mobile: 320px - 640px
- Tablet: 640px - 1024px
- Desktop: 1024px - 1440px
- Large: 1440px+

### 🤝 Working with Existing Code

1. **Reuse Existing Patterns:**
   - API response formats from existing endpoints
   - Vue component structure from existing pages
   - Store patterns from authStore, trailsStore
   - Styling approach using Tailwind + CSS variables

2. **Integration with All Trails:**
   - Shop section accessible from main navigation
   - Use existing user authentication
   - Leverage existing Booking model for "created_from_booking" links
   - Use existing Trail model for product recommendations

3. **Follow Conventions:**
   - API endpoints: `/api/method/all_trails.api.shop.*`
   - Doctype naming: Pascal case (MerchandiseItem, BNPLPlan)
   - Vue files: PascalCase (GlassCard.vue, Browse.vue)
   - Store functions: camelCase (addToCart, createOrder)
   - Validation: Server-side first, client-side second

---

## Start Here

1. **Read TECHNICAL_SPECS_PHASE_2.md** for implementation details
2. **Review WIREFRAMES_PHASE_2.md** for UI reference
3. **Create feature branch**: `git checkout -b feature/phase-2-merchandise`
4. **Start with Phase 1 setup tasks** (environment, patterns, schema validation)
5. **Proceed to Phase 2 backend** (DocTypes, APIs, jobs)
6. **Build Phase 3 frontend** (components, pages, store)
7. **Test Phase 4** (integration, E2E, load)
8. **Deploy Phase 5** (launch, monitoring, support)

---

**You have all the information needed to implement Phase 2 end-to-end. Let's build a great merchandise system for All Trails! 🚀**
