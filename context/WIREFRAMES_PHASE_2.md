# All Trails Phase 2: UI/UX Wireframes & Design Specifications

---

## Wireframe 1: Shop Catalog Page (Mobile & Desktop)

### Mobile View (375px)

```
┌─────────────────────────────┐
│  ◄  Shop  [Search]  [Cart:1] │  Header with back nav
├─────────────────────────────┤
│                              │
│  ╔════════════════════════╗  │  Filter Chips
│  ║ All   Gear   Apparel   ║  │  (Horizontal scroll)
│  ║ Shoes Accessories      ║  │
│  ╚════════════════════════╝  │
│                              │
├─────────────────────────────┤
│                              │  Product Cards
│  ╔════════════════════════╗  │  (Stacked, 1 col)
│  ║                        ║  │
│  ║  [Hero Image]    ★4.5  ║  │
│  ║                   (23)  ║  │
│  ║                        ║  │
│  ║ Premium Hiking         ║  │
│  ║ Backpack 65L           ║  │
│  ║                        ║  │
│  ║ KES 7,200 (Was 8,500)  ║  │
│  ║ ████████░░ -15%        ║  │
│  ║                        ║  │
│  ║ [+ Add to Cart  ]      ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │
│  ║                        ║  │
│  ║  [Hero Image]    ★4.7  ║  │
│  ║                   (34)  ║  │
│  ║                        ║  │
│  ║ Trekking Boots         ║  │
│  ║ Mountain Pro           ║  │
│  ║                        ║  │
│  ║ KES 6,500              ║  │
│  ║                        ║  │
│  ║ [+ Add to Cart  ]      ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │  Loading indicator
│  ║    Loading more...     ║  │  or "Load More" button
│  ╚════════════════════════╝  │
│                              │
└─────────────────────────────┘
```

### Desktop View (1024px)

```
┌────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ◄ Shop                    [Search .............]  [Cart: 2]    │
│                                                                  │
├────────────────────────────────────────────────────────────────┤
│  Left Sidebar (250px)       │  Main Content (774px)            │
│ ─────────────────────────   │                                  │
│ CATEGORIES                  │  ╔════════╦════════╦════════╗   │
│ ☑ All Items (200)          │  ║        ║        ║        ║   │
│ ☐ Hiking Gear (87)         │  ║[Image] ║[Image] ║[Image] ║   │
│ ☐ Apparel (45)             │  ║ ★4.5   ║ ★4.7   ║ ★4.2   ║   │
│ ☐ Accessories (32)         │  ║ (23)   ║ (34)   ║ (12)   ║   │
│ ☐ Experience (18)          │  ║        ║        ║        ║   │
│                             │  ║Backp.  ║Boots   ║Jacket  ║   │
│ PRICE RANGE                │  ║        ║        ║        ║   │
│ ├─────── [●]────┤          │  ║7,200   ║6,500   ║4,800   ║   │
│ KES 0      10,000          │  ║        ║        ║        ║   │
│                             │  ║[Add]   ║[Add]   ║[Add]   ║   │
│ RATING                      │  ╠════════╬════════╬════════╣   │
│ ☑ 4+ stars                 │  ║        ║        ║        ║   │
│ ☐ 3+ stars                 │  ║[Image] ║[Image] ║[Image] ║   │
│ ☐ 2+ stars                 │  ║ ★4.3   ║ ★4.1   ║ ★4.6   ║   │
│                             │  ║ (18)   ║ (8)    ║ (41)   ║   │
│ IN STOCK                    │  ║        ║        ║        ║   │
│ ☑ In Stock Only            │  ║Water   ║Jacket  ║Socks   ║   │
│                             │  ║        ║        ║        ║   │
│ [Clear All Filters]         │  ║2,400   ║5,200   ║800     ║   │
│                             │  ║        ║        ║        ║   │
│                             │  ║[Add]   ║[Add]   ║[Add]   ║   │
│                             │  ╚════════╩════════╩════════╝   │
│                             │                                  │
│                             │  Showing 6 of 87 results         │
│                             │  [← Previous] [Page 1] [Next →]  │
│                             │                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## Wireframe 2: Product Detail Page

### Mobile View

```
┌─────────────────────────────┐
│  ◄                  [Cart:1] │
├─────────────────────────────┤
│                              │
│  ╔════════════════════════╗  │
│  ║                        ║  │  Hero Image
│  ║    [Image Gallery]     ║  │  with carousel
│  ║                        ║  │  • • • •
│  ╚════════════════════════╝  │
│                              │
│  ★ 4.5 (23 reviews)          │  Rating
│                              │
│  Premium Hiking              │  Title
│  Backpack 65L                │
│                              │
│  Brand: Summit Gear          │  Meta
│  SKU: PACK-650-BLK          │
│                              │
│  KES 7,200                   │  Price
│  Was KES 8,500  [Save 15%]   │
│                              │
│  ┌─────────────────────────┐ │  Stock indicator
│  │ ✓ In Stock (15 left)    │ │
│  └─────────────────────────┘ │
│                              │
│  DETAILS                     │  Expandable sections
│  ▼ Description              │
│  Premium 65L hiking          │
│  backpack made from          │
│  durable polyester. Ideal    │
│  for 3-5 day treks.          │
│                              │
│  ▶ Specifications            │
│  ▶ Care Instructions         │
│  ▶ Suitable for Hikes        │
│                              │
│  REVIEWS                     │
│  ▼ Show All (23)             │
│                              │
│  ╔════════════════════════╗  │
│  ║ John D.  ★★★★★        ║  │
│  ║ "Best backpack!"       ║  │
│  ║ Verified purchase      ║  │
│  ║ 👍 23 found helpful    ║  │
│  ╚════════════════════════╝  │
│                              │
│  QUANTITY                    │
│  [−] 1 [+]                   │
│                              │
│  ╔════════════════════════╗  │
│  ║ [+ Add to Cart      ]  ║  │ Button
│  ╚════════════════════════╝  │
│                              │
│  BNPL Option                 │
│  ╔════════════════════════╗  │
│  ║ Or 2 x KES 3,600      ║  │
│  ║ with 0% interest       ║  │
│  ║ [Pay in Installments]  ║  │
│  ╚════════════════════════╝  │
│                              │
│  RELATED ITEMS               │
│  [Jacket] [Socks] [Shoes]   │
│                              │
└─────────────────────────────┘
```

### Desktop View

```
┌────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ◄ Shop › Hiking Gear › Backpacks            [Search] [Cart:2]  │
│                                                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ╔═══════════════════════╗  │  Details Section (Right)        │
│  ║                       ║  │                                  │
│  ║  [Main Image]    ★4.5  │  │  Premium Hiking Backpack 65L    │
│  ║                   (23) │  │  Brand: Summit Gear             │
│  ║                       ║  │  SKU: PACK-650-BLK              │
│  ║                       ║  │                                  │
│  ║                       ║  │  KES 7,200 (Was 8,500) -15%      │
│  ║   [T] [T] [T] [T]     ║  │  ████████░░                      │
│  ╚═══════════════════════╝  │                                  │
│                             │  ✓ In Stock (15 units left)      │
│  Image Gallery              │                                  │
│  (5 thumbnails)             │  ═════════════════════════════  │
│                             │                                  │
│                             │  DESCRIPTION                     │
│                             │  Premium 65L hiking backpack     │
│                             │  made from durable polyester.    │
│                             │  Ideal for 3-5 day treks with   │
│                             │  advanced ventilation system.    │
│                             │                                  │
│                             │  ▼ Specifications                │
│                             │    Material: Polyester           │
│                             │    Capacity: 65L                 │
│                             │    Weight: 1.8kg                 │
│                             │    Color: Black, Blue, Green     │
│                             │                                  │
│                             │  ▼ Care Instructions             │
│                             │    Hand wash only...             │
│                             │                                  │
│                             │  ▼ Suitable For                  │
│                             │    Moderate to Expert hikes      │
│                             │                                  │
│                             │  ═════════════════════════════  │
│                             │                                  │
│                             │  QUANTITY: [−] 1 [+]             │
│                             │                                  │
│                             │  ╔═════════════════════════╗    │
│                             │  ║ [+ Add to Cart      ]   ║    │
│                             │  ╚═════════════════════════╝    │
│                             │                                  │
│                             │  ╔═════════════════════════╗    │
│                             │  ║ ◎ Pay Full: KES 7,200   ║    │
│                             │  ║ ◎ 2 x KES 3,600 BNPL    ║    │
│                             │  ╚═════════════════════════╝    │
│                             │                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CUSTOMER REVIEWS                                                │
│                                                                  │
│  ★★★★★ 4.5/5 (23 reviews)                                      │
│  ████████░░ 80%  ★★★★★                                         │
│  ░░░░░░░░░░ 15%  ★★★★                                          │
│  ░░░░░░░░░░ 5%   ★★★                                           │
│                                                                  │
│  Top Reviews:                                                    │
│                                                                  │
│  ╔══════════════════════════════╗  ╔══════════════════════════╗│
│  ║ ★★★★★ John D.              ║  ║ ★★★★ Sarah K.           ║│
│  ║ "Best backpack ever!"       ║  ║ "Great but a bit heavy"  ║│
│  ║ ✓ Verified Purchase         ║  ║ ✓ Verified Purchase      ║│
│  ║ 👍 23                       ║  ║ 👍 12                    ║│
│  ╚══════════════════════════════╝  ╚══════════════════════════╝│
│                                                                  │
│  [Show All Reviews] or [Write a Review]                         │
│                                                                  │
├────────────────────────────────────────────────────────────────┤
│  RELATED ITEMS                                                   │
│  ╔════════╗  ╔════════╗  ╔════════╗  ╔════════╗                │
│  ║[Image] ║  ║[Image] ║  ║[Image] ║  ║[Image] ║                │
│  ║Trekking║  ║Mountain║  ║Hydration║ ║Compass ║               │
│  ║Boots   ║  ║Jacket  ║  ║Pack    ║  ║        ║                │
│  ║KES6,500║  ║KES4,800║  ║KES1,800║  ║KES2,200║               │
│  ║[Add]   ║  ║[Add]   ║  ║[Add]   ║  ║[Add]   ║                │
│  ╚════════╝  ╚════════╝  ╚════════╝  ╚════════╝                │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## Wireframe 3: Shopping Cart

### Mobile View

```
┌─────────────────────────────┐
│  ◄  Your Cart (2 items)  × │  Header
├─────────────────────────────┤
│                              │
│  ╔════════════════════════╗  │  Item 1
│  ║  [Thumb] Premium       ║  │
│  ║          Backpack      ║  │
│  ║                        ║  │
│  ║          KES 7,200     ║  │
│  ║          [−] 1 [+]     ║  │
│  ║                  [✕]   ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │  Item 2
│  ║  [Thumb] Trekking      ║  │
│  ║          Boots         ║  │
│  ║                        ║  │
│  ║          KES 6,500     ║  │
│  ║          [−] 1 [+]     ║  │
│  ║                  [✕]   ║  │
│  ╚════════════════════════╝  │
│                              │
│  ─────────────────────────── │
│                              │  Summary Section
│  Subtotal       KES 13,700   │
│  Discount           −        │
│  Shipping       KES   300    │
│  Tax (16%)      KES 2,240    │
│  ─────────────────────────── │
│  TOTAL          KES 16,240   │
│                              │
│  ┌─────────────────────────┐ │  Promo code
│  │ Promo Code [    ]       │ │  input
│  │ [ Apply ]               │ │
│  └─────────────────────────┘ │
│                              │
│  ╔════════════════════════╗  │  Checkout buttons
│  ║ [Proceed to Checkout]  ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │
│  ║ [Continue Shopping]    ║  │
│  ╚════════════════════════╝  │
│                              │
└─────────────────────────────┘
```

### Desktop View (Side Panel)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Main Content                │  Shopping Cart (350px)           │
│                              │                                  │
│  [Shop continues...]         │  ╔════════════════════════════╗ │
│                              │  ║ Your Cart (2 items)   ×    ║ │
│                              │  ╠════════════════════════════╣ │
│                              │  ║                            ║ │
│                              │  ║ Premium Backpack 65L      ║ │
│                              │  ║ KES 7,200  [−] 1 [+]      ║ │
│                              │  ║                       [×]  ║ │
│                              │  ║                            ║ │
│                              │  ║ Trekking Boots            ║ │
│                              │  ║ KES 6,500  [−] 1 [+]      ║ │
│                              │  ║                       [×]  ║ │
│                              │  ║                            ║ │
│                              │  ╠════════════════════════════╣ │
│                              │  ║ Subtotal: KES 13,700      ║ │
│                              │  ║ Tax (16%): KES 2,192      ║ │
│                              │  ║ Shipping: KES 300         ║ │
│                              │  ╠════════════════════════════╣ │
│                              │  ║ TOTAL: KES 16,192         ║ │
│                              │  ╠════════════════════════════╣ │
│                              │  ║ [Promo Code...] [Apply]   ║ │
│                              │  ║                            ║ │
│                              │  ║ [Proceed to Checkout   ]   ║ │
│                              │  ║ [Continue Shopping    ]    ║ │
│                              │  ╚════════════════════════════╝ │
│                              │                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Wireframe 4: Checkout Flow - Step 1 (Delivery)

### Mobile View

```
┌─────────────────────────────┐
│  ◄  Checkout        [Step 1] │
├─────────────────────────────┤
│                              │
│  Progress: • ○ ○             │  Step indicator
│                              │
│  DELIVERY ADDRESS            │
│                              │
│  ┌─────────────────────────┐ │  Input fields
│  │ Delivery Address        │ │
│  │ 123 Nairobi Road, ...   │ │
│  │                         │ │
│  │                         │ │
│  └─────────────────────────┘ │
│                              │
│  ┌─────────────────────────┐ │
│  │ Phone Number            │ │
│  │ 254700123456            │ │
│  └─────────────────────────┘ │
│                              │
│  [Continue to Payment    ]   │
│                              │
│  ─────────────────────────── │  Order summary
│  Order Summary              │
│  2 items        KES 13,700  │
│  Tax            KES  2,192  │
│  Shipping       KES    300  │
│  ─────────────────────────── │
│  Total          KES 16,192  │
│                              │
└─────────────────────────────┘
```

---

## Wireframe 5: Checkout Flow - Step 2 (Payment Method)

### Mobile View

```
┌─────────────────────────────┐
│  ◄  Checkout        [Step 2] │
├─────────────────────────────┤
│                              │
│  Progress: • • ○             │  Step indicator
│                              │
│  PAYMENT METHOD              │
│                              │
│  ╔════════════════════════╗  │  M-PESA Option
│  ║  M-Pesa Pay Now       ║  │  (Selected)
│  ║                        ║  │
│  ║  ✓ Full payment today  ║  │
│  ║    KES 16,192          ║  │
│  ║                        ║  │
│  ║  [Selected]            ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │  BNPL Option
│  ║  Buy Now, Pay Later   ║  │
│  ║                        ║  │
│  ║  2 payments of:        ║  │
│  ║  KES 8,096             ║  │
│  ║                        ║  │
│  ║  • Today               ║  │
│  ║  • In 30 days          ║  │
│  ║                        ║  │
│  ║  [Select]              ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │
│  ║ [Back]  [Continue]     ║  │
│  ╚════════════════════════╝  │
│                              │
└─────────────────────────────┘
```

---

## Wireframe 6: Checkout Flow - Step 3 (Review & Pay)

### Mobile View

```
┌─────────────────────────────┐
│  ◄  Checkout        [Step 3] │
├─────────────────────────────┤
│                              │
│  Progress: • • •             │
│                              │
│  ORDER REVIEW               │
│                              │
│  Items                       │
│  ╔════════════════════════╗  │
│  ║ Premium Backpack  ×1   ║  │
│  ║ KES 7,200              ║  │
│  ║                        ║  │
│  ║ Trekking Boots    ×1   ║  │
│  ║ KES 6,500              ║  │
│  ╚════════════════════════╝  │
│                              │
│  Delivery                     │
│  To: 123 Nairobi Road       │
│  Phone: 254700123456        │
│  Est. Delivery: March 18    │
│                              │
│  Payment                      │
│  Method: M-Pesa             │
│  Amount: KES 16,192         │
│                              │
│  ─────────────────────────── │
│  Subtotal    KES 13,700     │
│  Tax (16%)   KES  2,192     │
│  Shipping    KES    300     │
│  ─────────────────────────── │
│  TOTAL       KES 16,192     │
│                              │
│  ╔════════════════════════╗  │
│  ║ [Place Order       ]   ║  │
│  ║  Pay with M-Pesa       ║  │
│  ╚════════════════════════╝  │
│                              │
│  ╔════════════════════════╗  │
│  ║ [Back]                 ║  │
│  ╚════════════════════════╝  │
│                              │
└─────────────────────────────┘
```

---

## Wireframe 7: MPESA Payment Modal

### Mobile/Desktop View

```
┌─────────────────────────────────────┐
│                                     │
│      MPESA PAYMENT PENDING          │  Modal Title
│                                     │
│  ─────────────────────────────────  │
│                                     │
│      Order: MO-2024-00157          │  Order details
│      Amount: KES 16,192             │
│      Status: Waiting for PIN entry  │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│      🔔 STK PUSH SENT               │  Status message
│                                     │
│      A payment prompt has been      │
│      sent to 254700123456           │
│                                     │
│      Enter your M-Pesa PIN on       │
│      your phone to complete         │
│      payment                        │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│      [Processing...] 📱             │  Loading indicator
│      (Checking for 30 minutes)      │
│                                     │
│      Time remaining: 28:45           │
│                                     │
│  ─────────────────────────────────  │
│                                     │
│      ⚠️ PAYMENT ISSUES?             │  Help section
│                                     │
│      [Resend STK] [Cancel]          │
│                                     │
│  ─────────────────────────────────  │
│                                     │
```

---

## Wireframe 8: Order Confirmation Page

### Mobile View

```
┌─────────────────────────────┐
│                              │
│        ✓ ORDER PLACED!       │  Success badge
│                              │
├─────────────────────────────┤
│                              │
│  Order ID: MO-2024-00157     │  Order details
│  Placed: March 14, 10:30 AM  │
│                              │
│  ─────────────────────────── │
│                              │
│  DELIVERY DETAILS            │
│                              │
│  📍 123 Nairobi Road         │  Address
│    Nairobi 00100            │
│                              │
│  📦 Est. Delivery            │
│     March 18, 2024           │
│                              │
│  ─────────────────────────── │
│                              │
│  ITEMS                       │  Order items
│                              │
│  ✓ Premium Backpack ×1       │
│    KES 7,200                 │
│                              │
│  ✓ Trekking Boots ×1         │
│    KES 6,500                 │
│                              │
│  ─────────────────────────── │
│  Total: KES 16,192           │
│  Status: Payment Received     │
│                              │
│  ─────────────────────────── │
│                              │
│  NEXT STEPS                  │
│                              │
│  ✓ Payment confirmed         │
│  ⊙ Picking & packing         │  Timeline
│  ○ Shipped                   │
│  ○ Delivered                 │
│                              │
│  ─────────────────────────── │
│                              │
│  [Track Order] [Continue Shop]
│                              │
│  ⚡ Confirmation email sent  │  Email notification
│  to user@example.com         │
│                              │
└─────────────────────────────┘
```

---

## Wireframe 9: Order Tracking Page

### Mobile View

```
┌─────────────────────────────┐
│  ◄  Order MO-2024-00157      │
├─────────────────────────────┤
│                              │
│  Status: PROCESSING          │  Current status
│  2/4 Steps Complete          │
│                              │
│  ─────────────────────────── │
│                              │
│  TIMELINE                    │
│                              │
│  ✓ Confirmed                 │  Timeline steps
│    March 14, 10:30 AM        │  with checkmarks/dots
│    Payment received           │
│                              │
│  ✓ Processing                │
│    March 14, 3:00 PM         │
│    Items picked & packed     │
│                              │
│  ⊙ Shipped                   │
│    Tracking: TRK-9K8L7M6N5O │
│    Expected: March 18        │
│                              │
│  ○ Delivered                 │
│    Pending                    │
│                              │
│  ─────────────────────────── │
│                              │
│  TRACKING LINK               │
│                              │
│  [View on Tracking Site]     │
│                              │
│  ─────────────────────────── │
│                              │
│  ORDER DETAILS               │
│                              │
│  Items:                       │
│  • Premium Backpack ×1        │
│  • Trekking Boots ×1          │
│                              │
│  Subtotal: KES 13,700        │
│  Tax: KES 2,192              │
│  Shipping: KES 300           │
│  ─────────────────────────── │
│  Total: KES 16,192           │
│                              │
│  Delivery To:                │
│  123 Nairobi Road           │
│  Nairobi 00100              │
│                              │
│  [Contact Support]           │
│                              │
└─────────────────────────────┘
```

---

## Design System: Glass Component Examples

### Glass Button States

```
Normal (Primary)              Hover                    Disabled
┌──────────────────┐        ┌──────────────────┐      ┌──────────────────┐
│ Pay Now (KES 16K)│        │ Pay Now (KES 16K)│      │ Pay Now (KES 16K)│
│                  │        │ ↑ (lifted)       │      │ (opacity: 50%)   │
│ (Orange bg)      │        │ (enhanced shadow)│      │                  │
└──────────────────┘        └──────────────────┘      └──────────────────┘

Loading                      Secondary                Error
┌──────────────────┐        ┌──────────────────┐      ┌──────────────────┐
│ ⟳ Processing...  │        │ Continue Shopping│      │ Retry Payment    │
│ (spinner)        │        │ (glass border)   │      │ (red border)     │
│                  │        │ (hover brighten) │      │                  │
└──────────────────┘        └──────────────────┘      └──────────────────┘
```

### Glass Input Focus States

```
Normal                       Focus                    Error
┌────────────────────────┐  ┌────────────────────────┐ ┌────────────────────┐
│ Delivery Address       │  │ Delivery Address       │ │ Delivery Address   │
│ ████████████████       │  │ ████████████████       │ │ ████████████████   │
│ (glass border)         │  │ (orange border glow)   │ │ (red border)       │
│ (placeholder text)     │  │ (cursor blinking)      │ │ ⚠ Required field   │
└────────────────────────┘  └────────────────────────┘ └────────────────────┘
```

### Glass Card Hover Effects

```
Rest State                   Hover (Lift)              Hover (Brighten)
┌──────────────────┐        ┌──────────────────┐      ┌──────────────────┐
│  [Image]         │        │  [Image]         │      │  [Image]         │
│  Product Name    │    ↑   │  Product Name    │      │  Product Name    │
│  KES 5,000       │        │  KES 5,000       │      │  KES 5,000       │
│  ★ 4.5 (12)      │        │  ★ 4.5 (12)      │      │  ★ 4.5 (12)      │
│  [Add to Cart]   │        │  [Add to Cart]   │      │  [Add to Cart]    │
└──────────────────┘        └──────────────────┘      └──────────────────┘
(Normal glass)              (Lifted + shadow)         (Border highlighted)
```

---

## Color & Typography Specifications

### Color Palette

```
Primary Glass Background
    Background: rgba(27, 58, 45, 0.85)    [Forest Dark at 85% opacity]
    Backdrop: blur(30px on desktop, 20px on mobile)
    Border: rgba(255, 255, 255, 0.2)      [Subtle white]
    Inner Glow: inset 0 0 20px rgba(255, 255, 255, 0.2)

Accent Colors
    Orange: #E85D1F                        [Call-to-action buttons]
    Orange Light: #F07D3F                 [Hover states]
    Success Green: #10B981                [Confirmations]
    Warning Yellow: #F59E0B                [Alerts]
    Error Red: #EF4444                    [Errors]

Text Colors
    Primary: #F5F5F5                      [Body text]
    Secondary: #CBD5E0                    [Helper text]
    Muted: #9CA3AF                        [Disabled text]
    Divider: rgba(255, 255, 255, 0.1)     [Line separators]
```

### Typography

```
Display (Hero)
    Font: Sora Bold
    Size: 32px (mobile), 48px (desktop)
    Line Height: 1.2
    Letter Spacing: -1px

Heading H1
    Font: Sora SemiBold
    Size: 24px (mobile), 32px (desktop)
    Line Height: 1.3
    Letter Spacing: 0

Heading H2
    Font: Sora SemiBold
    Size: 20px (mobile), 24px (desktop)
    Line Height: 1.4

Heading H3
    Font: Sora Medium
    Size: 18px (mobile), 20px (desktop)
    Line Height: 1.4

Body Regular
    Font: Inter Regular
    Size: 16px
    Line Height: 1.6
    Letter Spacing: 0.5px

Body Small
    Font: Inter Regular
    Size: 14px
    Line Height: 1.5

Caption/Helper
    Font: Inter Regular
    Size: 12px
    Line Height: 1.4
    Color: Secondary

Button Text
    Font: Inter SemiBold
    Size: 16px
    Line Height: 1
    Text Transform: Sentence case

Price/Amount
    Font: JetBrains Mono Bold
    Size: 18px
    Line Height: 1
```

---

## Responsive Breakpoints

```
Mobile Small:  320px - 375px    (iPhone SE, small phones)
Mobile:        375px - 640px    (Standard mobile)
Tablet Small:  640px - 768px    (Portrait tablet)
Tablet:        768px - 1024px   (Landscape tablet)
Desktop:       1024px - 1440px  (Standard desktop)
Desktop Large: 1440px+          (Large screens, 4K)

Key Layout Changes:
- <640px:  1-column layout, full-width cards
- 640-768: 2-column grid, slight padding reduction
- 768+:    Multi-column, sidebar navigation
```

---

## Animation & Micro-interactions

### Transitions
```
Fast:     150ms (buttons, icons)
Standard: 300ms (modals, cards, hover)
Slow:     500ms (page transitions)
Easing:   ease-out for entrances, ease-in-out for interactions
```

### Loading States
```
Spinner:     60px circular spinner, orange accent
Pulse:       Subtle opacity pulse (0.7 → 1.0 → 0.7)
Skeleton:    Placeholder cards with shimmer effect
Progress:    Linear progress bar for multi-step forms
```

### Feedback Animations
```
Success:     Green checkmark + slide-in toast (500ms)
Error:       Red shake animation + error banner
Warning:     Yellow alert icon + fade-in tooltip
Info:        Blue info icon + gentle fade-in
```

---

This wireframe document serves as the visual specification for developers and designers. All mockups should be created in Figma using these wireframes as the foundation, with the glassmorphic design system applied consistently across all screens.
