# ALL TRAILS PHASE 2: MASTER IMPLEMENTATION PROMPT

**Copy this entire file and paste into Claude/GPT-4 to start implementation immediately**

---

## CRITICAL INSTRUCTIONS

You are implementing the complete All Trails Phase 2 Merchandise System. This is a full-stack project requiring:
- Backend (Python/Frappe): 5 DocTypes, 8+ APIs, 4 background jobs
- Frontend (Vue 3/TS): 8+ components, 7+ pages, Pinia store
- Payment Integration: MPESA (idempotent) + BNPL (2-installment)
- Testing: Unit, integration, E2E, load testing
- Deployment: Migration scripts, config files, monitoring

**You have ONE prompt with everything. Execute it exactly.**

---

# PHASE 1: SETUP & DISCOVERY (Days 1-2)

## Task 1.1: Verify Environment

```bash
# Check project exists
ls -la /Users/salim/frappe/my-bench/apps/all_trails/

# Verify structure
ls -la frontend/
ls -la all_trails/

# Check dependencies (should exist)
# - Frappe >= 15.0
# - Vue 3
# - TypeScript
# - Pinia
# - Vite
```

## Task 1.2: Create Feature Branch

```bash
cd /Users/salim/frappe/my-bench/
git checkout -b feature/phase-2-merchandise
```

## Task 1.3: Create Directory Structure

Create these directories:

```
all_trails/
├── doctype/
│   ├── merchandise_item/
│   │   ├── merchandise_item.json
│   │   ├── merchandise_item.py
│   │   └── __init__.py
│   ├── merchandise_order/
│   │   ├── merchandise_order.json
│   │   ├── merchandise_order.py
│   │   └── __init__.py
│   ├── bnpl_plan/
│   │   ├── bnpl_plan.json
│   │   ├── bnpl_plan.py
│   │   └── __init__.py
│   ├── merchandise_review/
│   │   ├── merchandise_review.json
│   │   ├── merchandise_review.py
│   │   └── __init__.py
│   └── merchandise_category/
│       ├── merchandise_category.json
│       ├── merchandise_category.py
│       └── __init__.py
├── api/
│   ├── __init__.py
│   ├── shop.py (8+ endpoints)
│   └── payment_handler.py (MPESA integration)
├── tasks.py (background jobs)
├── templates/
│   ├── merchandise_order_confirmation.html
│   ├── merchandise_shipping_notification.html
│   ├── merchandise_delivery_confirmation.html
│   ├── bnpl_payment_reminder.html
│   ├── bnpl_payment_failure.html
│   ├── merchandise_review_request.html
│   └── low_stock_alert_internal.html
└── migrations/
    └── 0001_create_merchandise_doctypes.py

frontend/src/
├── components/
│   ├── glass/
│   │   ├── GlassCard.vue
│   │   ├── GlassButton.vue
│   │   ├── GlassInput.vue
│   │   ├── GlassModal.vue
│   │   ├── GlassProductCard.vue
│   │   ├── GlassCart.vue
│   │   ├── GlassCheckoutFlow.vue
│   │   ├── GlassAlert.vue
│   │   ├── GlassSpinner.vue
│   │   └── index.ts (export all)
│   └── common/ (existing)
├── pages/
│   ├── shop/
│   │   ├── Browse.vue
│   │   ├── Detail.vue
│   │   ├── Cart.vue
│   │   ├── Checkout.vue
│   │   ├── PaymentProcessing.vue
│   │   ├── Confirmation.vue
│   │   └── Tracking.vue
│   └── (existing pages)
├── stores/
│   ├── merchandiseStore.ts
│   └── (existing stores)
├── services/
│   ├── shopApi.ts
│   └── (existing services)
├── types/
│   ├── shop.ts
│   └── (existing types)
└── (existing structure)
```

---

# PHASE 2: BACKEND IMPLEMENTATION (Days 3-7)

## Task 2.1: Create Merchandise Item DocType

**File**: `all_trails/doctype/merchandise_item/merchandise_item.json`

```json
{
  "name": "Merchandise Item",
  "doctype": "DocType",
  "module": "All Trails",
  "is_submittable": false,
  "autoname": "field:item_code",
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Data",
      "label": "Item Code",
      "unique": true,
      "reqd": true
    },
    {
      "fieldname": "item_name",
      "fieldtype": "Data",
      "label": "Item Name",
      "reqd": true
    },
    {
      "fieldname": "category",
      "fieldtype": "Link",
      "label": "Category",
      "options": "Merchandise Category",
      "reqd": true
    },
    {
      "fieldname": "sku",
      "fieldtype": "Data",
      "label": "SKU",
      "unique": true,
      "reqd": true
    },
    {
      "fieldname": "description",
      "fieldtype": "Text Editor",
      "label": "Description"
    },
    {
      "fieldname": "pricing_section",
      "fieldtype": "Section Break",
      "label": "Pricing"
    },
    {
      "fieldname": "cost_price",
      "fieldtype": "Currency",
      "label": "Cost Price (KES)",
      "reqd": true
    },
    {
      "fieldname": "selling_price",
      "fieldtype": "Currency",
      "label": "Selling Price (KES)",
      "reqd": true
    },
    {
      "fieldname": "discount_price",
      "fieldtype": "Currency",
      "label": "Discount Price (KES)"
    },
    {
      "fieldname": "bnpl_eligible",
      "fieldtype": "Check",
      "label": "BNPL Eligible",
      "default": true
    },
    {
      "fieldname": "bnpl_min_amount",
      "fieldtype": "Currency",
      "label": "BNPL Minimum Amount (KES)",
      "default": 5000
    },
    {
      "fieldname": "inventory_section",
      "fieldtype": "Section Break",
      "label": "Inventory"
    },
    {
      "fieldname": "warehouse",
      "fieldtype": "Link",
      "label": "Warehouse",
      "options": "Warehouse",
      "reqd": true
    },
    {
      "fieldname": "low_stock_threshold",
      "fieldtype": "Int",
      "label": "Low Stock Threshold (Units)",
      "default": 10
    },
    {
      "fieldname": "brand",
      "fieldtype": "Data",
      "label": "Brand/Manufacturer"
    },
    {
      "fieldname": "media_section",
      "fieldtype": "Section Break",
      "label": "Media & Content"
    },
    {
      "fieldname": "image_urls",
      "fieldtype": "Code",
      "label": "Image URLs (JSON Array)",
      "options": "json"
    },
    {
      "fieldname": "care_instructions",
      "fieldtype": "Text",
      "label": "Care Instructions"
    },
    {
      "fieldname": "specifications",
      "fieldtype": "Code",
      "label": "Specifications (JSON)",
      "options": "json"
    },
    {
      "fieldname": "details_section",
      "fieldtype": "Section Break",
      "label": "Trail Details"
    },
    {
      "fieldname": "hikable_difficulty",
      "fieldtype": "Select",
      "label": "Suitable for Hiking Difficulty",
      "options": "Easy\nModerate\nHard\nExpert\nAll Levels"
    },
    {
      "fieldname": "reviews_section",
      "fieldtype": "Section Break",
      "label": "Reviews & Ratings"
    },
    {
      "fieldname": "average_rating",
      "fieldtype": "Rating",
      "label": "Average Rating",
      "read_only": true
    },
    {
      "fieldname": "review_count",
      "fieldtype": "Int",
      "label": "Review Count",
      "read_only": true,
      "default": 0
    },
    {
      "fieldname": "hikers_who_bought",
      "fieldtype": "Int",
      "label": "Hikers Who Bought",
      "read_only": true,
      "default": 0
    },
    {
      "fieldname": "metadata_section",
      "fieldtype": "Section Break",
      "label": "Metadata"
    },
    {
      "fieldname": "featured",
      "fieldtype": "Check",
      "label": "Featured Product"
    },
    {
      "fieldname": "position_in_category",
      "fieldtype": "Int",
      "label": "Position in Category",
      "default": 999
    },
    {
      "fieldname": "is_active",
      "fieldtype": "Check",
      "label": "Is Active",
      "default": true
    },
    {
      "fieldname": "tags",
      "fieldtype": "Text",
      "label": "Tags (Comma-separated)"
    },
    {
      "fieldname": "search_keywords",
      "fieldtype": "Text",
      "label": "Search Keywords"
    }
  ],
  "permissions": [
    {
      "role": "Administrator",
      "read": true,
      "write": true,
      "delete": true,
      "submit": false
    },
    {
      "role": "Customer",
      "read": true,
      "write": false,
      "delete": false,
      "submit": false
    }
  ],
  "indexes": [
    ["category", "is_active"],
    ["warehouse", "is_active"],
    ["featured"],
    ["bnpl_eligible"]
  ]
}
```

**File**: `all_trails/doctype/merchandise_item/merchandise_item.py`

```python
import frappe
import json
from frappe.model.document import Document

class MerchandiseItem(Document):
    def validate(self):
        # Ensure selling price > cost price
        if self.selling_price <= self.cost_price:
            frappe.throw("Selling price must be greater than cost price")

        # Validate BNPL eligibility
        if self.bnpl_eligible and self.bnpl_min_amount > self.selling_price:
            frappe.throw("BNPL minimum amount cannot exceed selling price")

        # Validate image URLs are valid JSON
        if self.image_urls:
            try:
                json.loads(self.image_urls)
            except:
                frappe.throw("Image URLs must be valid JSON array")

        # Ensure warehouse exists
        if not frappe.db.exists('Warehouse', self.warehouse):
            frappe.throw(f"Warehouse {self.warehouse} does not exist")

    def before_save(self):
        # Auto-update review stats
        self.average_rating = self._calculate_average_rating()
        self.review_count = self._count_reviews()
        self.hikers_who_bought = self._count_buyers()

    def _calculate_average_rating(self):
        result = frappe.db.sql(
            "SELECT AVG(rating) FROM `tabMerchandise Review` WHERE item_code = %s AND status = 'Approved'",
            self.item_code
        )
        return result[0][0] if result and result[0][0] else 0

    def _count_reviews(self):
        return frappe.db.count('Merchandise Review', {'item_code': self.item_code, 'status': 'Approved'})

    def _count_buyers(self):
        return frappe.db.sql(
            "SELECT COUNT(DISTINCT customer_id) FROM `tabMerchandise Order` WHERE fulfillment_status = 'Delivered' AND JSON_CONTAINS(items, JSON_OBJECT('item_code', %s))",
            self.item_code
        )[0][0]
```

## Task 2.2: Create Merchandise Order DocType

**File**: `all_trails/doctype/merchandise_order/merchandise_order.json`

```json
{
  "name": "Merchandise Order",
  "doctype": "DocType",
  "module": "All Trails",
  "is_submittable": false,
  "autoname": "naming_series:",
  "naming_series": "MO-YYYY-",
  "fields": [
    {
      "fieldname": "order_id",
      "fieldtype": "Data",
      "label": "Order ID",
      "read_only": true,
      "unique": true
    },
    {
      "fieldname": "customer_section",
      "fieldtype": "Section Break",
      "label": "Customer"
    },
    {
      "fieldname": "customer_id",
      "fieldtype": "Link",
      "label": "Customer",
      "options": "Contact",
      "reqd": true
    },
    {
      "fieldname": "customer_email",
      "fieldtype": "Email",
      "label": "Email",
      "read_only": true
    },
    {
      "fieldname": "customer_phone",
      "fieldtype": "Phone",
      "label": "Phone",
      "reqd": true
    },
    {
      "fieldname": "items_section",
      "fieldtype": "Section Break",
      "label": "Order Items"
    },
    {
      "fieldname": "items",
      "fieldtype": "Table",
      "label": "Items",
      "options": "Merchandise Order Item",
      "reqd": true
    },
    {
      "fieldname": "totals_section",
      "fieldtype": "Section Break",
      "label": "Order Totals"
    },
    {
      "fieldname": "subtotal",
      "fieldtype": "Currency",
      "label": "Subtotal",
      "read_only": true
    },
    {
      "fieldname": "discount_amount",
      "fieldtype": "Currency",
      "label": "Discount Amount"
    },
    {
      "fieldname": "shipping_cost",
      "fieldtype": "Currency",
      "label": "Shipping Cost",
      "default": 300
    },
    {
      "fieldname": "tax_amount",
      "fieldtype": "Currency",
      "label": "Tax (16% VAT)",
      "read_only": true
    },
    {
      "fieldname": "total_amount",
      "fieldtype": "Currency",
      "label": "Total Amount",
      "read_only": true
    },
    {
      "fieldname": "payment_section",
      "fieldtype": "Section Break",
      "label": "Payment"
    },
    {
      "fieldname": "payment_method",
      "fieldtype": "Select",
      "label": "Payment Method",
      "options": "MPESA\nCard\nBNPL",
      "reqd": true,
      "default": "MPESA"
    },
    {
      "fieldname": "payment_status",
      "fieldtype": "Select",
      "label": "Payment Status",
      "options": "Pending\nPartial\nCompleted\nFailed",
      "read_only": true,
      "default": "Pending"
    },
    {
      "fieldname": "payment_mode",
      "fieldtype": "Select",
      "label": "Payment Mode",
      "options": "Full\nInstallment",
      "default": "Full"
    },
    {
      "fieldname": "bnpl_section",
      "fieldtype": "Section Break",
      "label": "BNPL Details"
    },
    {
      "fieldname": "bnpl_plan_id",
      "fieldtype": "Link",
      "label": "BNPL Plan",
      "options": "BNPL Plan"
    },
    {
      "fieldname": "bnpl_total_installments",
      "fieldtype": "Int",
      "label": "Total Installments",
      "read_only": true
    },
    {
      "fieldname": "bnpl_remaining_installments",
      "fieldtype": "Int",
      "label": "Remaining Installments",
      "read_only": true
    },
    {
      "fieldname": "bnpl_next_payment_date",
      "fieldtype": "Date",
      "label": "Next Payment Date",
      "read_only": true
    },
    {
      "fieldname": "bnpl_next_payment_amount",
      "fieldtype": "Currency",
      "label": "Next Payment Amount",
      "read_only": true
    },
    {
      "fieldname": "fulfillment_section",
      "fieldtype": "Section Break",
      "label": "Fulfillment"
    },
    {
      "fieldname": "fulfillment_status",
      "fieldtype": "Select",
      "label": "Fulfillment Status",
      "options": "Draft\nConfirmed\nProcessing\nShipped\nDelivered\nCancelled",
      "default": "Draft",
      "read_only": true
    },
    {
      "fieldname": "shipping_address",
      "fieldtype": "Text",
      "label": "Shipping Address",
      "reqd": true
    },
    {
      "fieldname": "estimated_delivery_date",
      "fieldtype": "Date",
      "label": "Estimated Delivery Date",
      "read_only": true
    },
    {
      "fieldname": "actual_delivery_date",
      "fieldtype": "Date",
      "label": "Actual Delivery Date",
      "read_only": true
    },
    {
      "fieldname": "tracking_number",
      "fieldtype": "Data",
      "label": "Tracking Number"
    },
    {
      "fieldname": "notes",
      "fieldtype": "Text",
      "label": "Notes"
    },
    {
      "fieldname": "linking_section",
      "fieldtype": "Section Break",
      "label": "ERP Links"
    },
    {
      "fieldname": "sales_order_id",
      "fieldtype": "Link",
      "label": "Sales Order",
      "options": "Sales Order",
      "read_only": true
    },
    {
      "fieldname": "sales_invoice_id",
      "fieldtype": "Link",
      "label": "Sales Invoice",
      "options": "Sales Invoice",
      "read_only": true
    },
    {
      "fieldname": "custom_mpesa_ticket_id",
      "fieldtype": "Link",
      "label": "MPESA Ticket",
      "options": "MPESA Ticket",
      "read_only": true
    },
    {
      "fieldname": "metadata_section",
      "fieldtype": "Section Break",
      "label": "Metadata"
    },
    {
      "fieldname": "created_from_hiking_booking",
      "fieldtype": "Link",
      "label": "Related Booking",
      "options": "Booking"
    },
    {
      "fieldname": "referral_source",
      "fieldtype": "Select",
      "label": "Referral Source",
      "options": "Homepage\nBooking\nEmail\nTrail Page\nRecommendation"
    }
  ],
  "permissions": [
    {
      "role": "Administrator",
      "read": true,
      "write": true,
      "delete": true
    },
    {
      "role": "Customer",
      "read": true,
      "write": false,
      "delete": false
    }
  ]
}
```

**File**: `all_trails/doctype/merchandise_order/merchandise_order.py`

```python
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class MerchandiseOrder(Document):
    def validate(self):
        # Validate items exist and have stock
        for item in self.items:
            if not frappe.db.exists('Merchandise Item', item.item_code):
                frappe.throw(f"Item {item.item_code} does not exist")

            # Get stock balance
            stock = frappe.db.get_value(
                'Stock Ledger Entry',
                {'item_code': item.item_code, 'warehouse': 'Stores'},
                'sum(actual_qty)'
            ) or 0

            if stock < item.quantity:
                frappe.throw(f"Insufficient stock: {item.item_code}")

        # Recalculate totals
        self.calculate_totals()

    def before_save(self):
        self.order_date = frappe.utils.now_datetime()

    def calculate_totals(self):
        self.subtotal = sum(item.quantity * item.unit_price for item in self.items)
        self.tax_amount = self.subtotal * 0.16  # 16% VAT
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - (self.discount_amount or 0)

        # Update BNPL fields
        if self.payment_mode == 'Installment' and self.bnpl_plan_id:
            plan = frappe.get_doc('BNPL Plan', self.bnpl_plan_id)
            self.bnpl_total_installments = plan.installment_count
            pending = len([i for i in plan.installments if i.payment_status == 'Pending'])
            self.bnpl_remaining_installments = pending
            if pending > 0:
                next_inst = [i for i in plan.installments if i.payment_status == 'Pending'][0]
                self.bnpl_next_payment_date = next_inst.due_date
                self.bnpl_next_payment_amount = next_inst.amount

    def on_update_after_submit(self):
        if self.has_value_changed('fulfillment_status'):
            self.log_status_change()

    def log_status_change(self):
        old_status = self.db_get('fulfillment_status')
        new_status = self.fulfillment_status

        self.add_comment(
            'Comment',
            f'Status changed: {old_status} → {new_status}',
            comment_type='Info'
        )

        if new_status == 'Shipped':
            self.send_shipping_notification()
        elif new_status == 'Delivered':
            self.send_delivery_notification()

    def send_shipping_notification(self):
        frappe.sendmail(
            recipients=[self.customer_email],
            subject=f'Your All Trails Order {self.name} Has Shipped!',
            template='merchandise_shipping_notification',
            args={
                'order_id': self.name,
                'tracking_number': self.tracking_number,
                'estimated_delivery': self.estimated_delivery_date
            }
        )

    def send_delivery_notification(self):
        frappe.sendmail(
            recipients=[self.customer_email],
            subject=f'Your All Trails Order {self.name} Delivered',
            template='merchandise_delivery_confirmation',
            args={
                'order_id': self.name,
                'items_count': len(self.items),
                'total_amount': self.total_amount
            }
        )
```

## Task 2.3: Create BNPL Plan DocType

**File**: `all_trails/doctype/bnpl_plan/bnpl_plan.json`

```json
{
  "name": "BNPL Plan",
  "doctype": "DocType",
  "module": "All Trails",
  "is_submittable": false,
  "fields": [
    {
      "fieldname": "plan_id",
      "fieldtype": "Data",
      "label": "Plan ID",
      "unique": true,
      "read_only": true
    },
    {
      "fieldname": "merchandise_order",
      "fieldtype": "Link",
      "label": "Merchandise Order",
      "options": "Merchandise Order",
      "reqd": true
    },
    {
      "fieldname": "total_amount",
      "fieldtype": "Currency",
      "label": "Total Amount",
      "reqd": true
    },
    {
      "fieldname": "installment_count",
      "fieldtype": "Int",
      "label": "Installment Count",
      "default": 2,
      "reqd": true
    },
    {
      "fieldname": "installment_amount",
      "fieldtype": "Currency",
      "label": "Installment Amount",
      "read_only": true
    },
    {
      "fieldname": "first_payment_date",
      "fieldtype": "Date",
      "label": "First Payment Date",
      "reqd": true
    },
    {
      "fieldname": "payment_frequency",
      "fieldtype": "Select",
      "label": "Payment Frequency",
      "options": "Weekly\nBi-weekly\nMonthly",
      "default": "Monthly"
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Active\nCompleted\nDefaulted",
      "default": "Active",
      "read_only": true
    },
    {
      "fieldname": "payment_method",
      "fieldtype": "Select",
      "label": "Payment Method",
      "options": "MPESA\nCard",
      "default": "MPESA"
    },
    {
      "fieldname": "installments",
      "fieldtype": "Table",
      "label": "Installments",
      "options": "BNPL Installment"
    },
    {
      "fieldname": "automatic_retry",
      "fieldtype": "Check",
      "label": "Automatic Retry",
      "default": true
    },
    {
      "fieldname": "max_retries",
      "fieldtype": "Int",
      "label": "Max Retries",
      "default": 3
    },
    {
      "fieldname": "created_date",
      "fieldtype": "DateTime",
      "label": "Created Date",
      "read_only": true
    }
  ],
  "permissions": [
    {
      "role": "Administrator",
      "read": true,
      "write": true,
      "delete": true
    },
    {
      "role": "Customer",
      "read": true,
      "write": false,
      "delete": false
    }
  ]
}
```

**File**: `all_trails/doctype/bnpl_plan/bnpl_plan.py`

```python
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, now_datetime

class BNPLPlan(Document):
    def validate(self):
        if self.installment_count < 2:
            frappe.throw("Installment count must be at least 2")

        if len(self.installments) != self.installment_count:
            frappe.throw(f"Must have exactly {self.installment_count} installments")

    def on_insert(self):
        self.plan_id = frappe.generate_hash(length=12)
        self.created_date = now_datetime()
        self.generate_installment_schedule()

    def generate_installment_schedule(self):
        self.installments = []
        amount_per_installment = self.total_amount / self.installment_count
        current_date = self.first_payment_date

        for i in range(1, self.installment_count + 1):
            self.append('installments', {
                'installment_number': i,
                'due_date': current_date,
                'amount': amount_per_installment,
                'payment_status': 'Pending'
            })

            # Calculate next due date
            if self.payment_frequency == 'Weekly':
                current_date = add_days(current_date, 7)
            elif self.payment_frequency == 'Bi-weekly':
                current_date = add_days(current_date, 14)
            else:  # Monthly
                current_date = add_days(current_date, 30)

    def on_update(self):
        # Check if all installments paid
        all_paid = all(inst.payment_status == 'Paid' for inst in self.installments)
        if all_paid and self.status != 'Completed':
            self.status = 'Completed'
            self.save()

            # Notify customer
            order = frappe.get_doc('Merchandise Order', self.merchandise_order)
            frappe.sendmail(
                recipients=[order.customer_email],
                subject='BNPL Plan Completed',
                template='bnpl_completion_notification',
                args={'order_id': self.merchandise_order}
            )
```

## Task 2.4: Create Merchandise Review & Category DocTypes

**File**: `all_trails/doctype/merchandise_review/merchandise_review.json`

```json
{
  "name": "Merchandise Review",
  "doctype": "DocType",
  "module": "All Trails",
  "is_submittable": false,
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Link",
      "label": "Item",
      "options": "Merchandise Item",
      "reqd": true
    },
    {
      "fieldname": "customer",
      "fieldtype": "Link",
      "label": "Customer",
      "options": "Contact",
      "reqd": true
    },
    {
      "fieldname": "rating",
      "fieldtype": "Rating",
      "label": "Rating",
      "reqd": true
    },
    {
      "fieldname": "title",
      "fieldtype": "Data",
      "label": "Title",
      "reqd": true
    },
    {
      "fieldname": "review_text",
      "fieldtype": "Text Editor",
      "label": "Review"
    },
    {
      "fieldname": "verified_purchase",
      "fieldtype": "Check",
      "label": "Verified Purchase"
    },
    {
      "fieldname": "helpful_count",
      "fieldtype": "Int",
      "label": "Helpful Count",
      "default": 0
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Pending\nApproved\nRejected",
      "default": "Pending"
    }
  ]
}
```

**File**: `all_trails/doctype/merchandise_category/merchandise_category.json`

```json
{
  "name": "Merchandise Category",
  "doctype": "DocType",
  "module": "All Trails",
  "is_tree": true,
  "fields": [
    {
      "fieldname": "category_name",
      "fieldtype": "Data",
      "label": "Category Name",
      "reqd": true
    },
    {
      "fieldname": "parent_category",
      "fieldtype": "Link",
      "label": "Parent Category",
      "options": "Merchandise Category"
    },
    {
      "fieldname": "description",
      "fieldtype": "Text",
      "label": "Description"
    },
    {
      "fieldname": "icon",
      "fieldtype": "Attach Image",
      "label": "Icon"
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 999
    },
    {
      "fieldname": "is_active",
      "fieldtype": "Check",
      "label": "Is Active",
      "default": true
    }
  ]
}
```

## Task 2.5: Create API Endpoints

**File**: `all_trails/api/shop.py`

```python
import frappe
import json
from frappe import _
from frappe.utils import now_datetime, add_days
from decimal import Decimal

@frappe.whitelist()
def get_merchandise_catalog(category=None, limit=20, offset=0, sort_by='position', featured_only=False):
    """
    GET /api/method/all_trails.api.shop.get_merchandise_catalog

    Returns paginated merchandise catalog with filters
    """
    filters = [['is_active', '=', True]]
    if category:
        filters.append(['category', '=', category])
    if featured_only:
        filters.append(['featured', '=', True])

    items = frappe.get_list(
        'Merchandise Item',
        filters=filters,
        fields=['item_code', 'item_name', 'category', 'selling_price', 'discount_price',
                'average_rating', 'review_count', 'warehouse', 'image_urls'],
        limit=int(limit),
        offset=int(offset),
        order_by=f'{sort_by} asc' if sort_by else 'position_in_category asc'
    )

    # Enrich with stock info
    for item in items:
        stock = get_stock_balance(item['item_code'], 'Stores')
        item['in_stock'] = stock > 0
        item['stock_quantity'] = stock or 0
        item['bnpl_eligible'] = True
        item['discount_percentage'] = 0
        if item['discount_price'] and item['selling_price']:
            item['discount_percentage'] = int(((item['selling_price'] - item['discount_price']) / item['selling_price']) * 100)

    total_count = frappe.db.count('Merchandise Item', filters)

    return {
        'items': items,
        'total_count': total_count,
        'has_more': offset + int(limit) < total_count,
        'pagination': {
            'total_count': total_count,
            'limit': int(limit),
            'offset': int(offset),
            'pages': (total_count + int(limit) - 1) // int(limit)
        }
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

    stock = get_stock_balance(item.item_code, item.warehouse)

    return {
        'item_code': item.item_code,
        'item_name': item.item_name,
        'description': item.description,
        'price': item.selling_price,
        'discount_price': item.discount_price,
        'category': item.category,
        'sku': item.sku,
        'images': json.loads(item.image_urls) if item.image_urls else [],
        'specifications': json.loads(item.specifications) if item.specifications else {},
        'care_instructions': item.care_instructions,
        'suitable_for_trails': item.hikable_difficulty,
        'hikers_who_bought': item.hikers_who_bought,
        'average_rating': item.average_rating,
        'review_count': item.review_count,
        'reviews': reviews,
        'in_stock': stock > 0,
        'stock_quantity': stock or 0,
        'bnpl_eligible': item.bnpl_eligible
    }

@frappe.whitelist()
def validate_coupon(code, order_total):
    """
    POST /api/method/all_trails.api.shop.validate_coupon

    Validates promo code and returns discount amount
    """
    # Check if coupon exists
    coupon = frappe.get_value(
        'Promotional Code',
        {'code': code, 'active': True},
        ['discount_percentage', 'discount_amount', 'min_order_amount', 'max_uses', 'usage_count']
    )

    if not coupon:
        frappe.throw('Invalid or expired coupon code')

    discount_percent, discount_amt, min_amt, max_uses, usage_count = coupon

    if float(order_total) < float(min_amt):
        frappe.throw(f'Coupon valid only for orders above KES {min_amt}')

    if usage_count >= max_uses:
        frappe.throw('Coupon usage limit reached')

    discount_amount = float(discount_amt) or (float(order_total) * float(discount_percent) / 100)

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
    """
    user = frappe.session.user
    customer_email = frappe.get_value('User', user, 'email')

    # Validate stock
    for item_data in items:
        stock = get_stock_balance(item_data['item_code'], 'Stores')
        if stock < item_data['quantity']:
            frappe.throw(f"Insufficient stock for {item_data['item_code']}")

    # Create order
    order = frappe.new_doc('Merchandise Order')
    order.customer_id = user
    order.customer_email = customer_email
    order.customer_phone = customer_phone
    order.payment_method = payment_method
    order.shipping_address = delivery_address

    # Add items
    subtotal = 0
    for item_data in items:
        item = frappe.get_doc('Merchandise Item', item_data['item_code'])
        order.append('items', {
            'item_code': item.item_code,
            'quantity': item_data['quantity'],
            'unit_price': item.selling_price,
            'discount_percentage': 0,
            'line_total': item.selling_price * item_data['quantity']
        })
        subtotal += item.selling_price * item_data['quantity']

    # Apply coupon if provided
    if coupon_code:
        discount_result = validate_coupon(coupon_code, subtotal)
        order.discount_amount = discount_result['discount_amount']

    # Calculate totals
    order.calculate_totals()
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
    """
    order = frappe.get_doc('Merchandise Order', order_id)

    # Create MPESA Ticket
    ticket = frappe.new_doc('MPESA Ticket')
    ticket.name = frappe.generate_hash(length=16)
    ticket.msisdn = phone_number
    ticket.amount = order.total_amount
    ticket.account_number = order_id
    ticket.description = f'Merchandise {order_id}'
    ticket.ticket_status = 'Initiated'
    ticket.insert()

    # Initiate STK push
    try:
        from mpesa_tx.api.mpesa_handler import MPESAHandler
        handler = MPESAHandler()

        response = handler.initiate_stk_push(
            phone_number=phone_number,
            amount=int(order.total_amount),
            account_reference=order_id,
            transaction_desc=f'Order {order_id}'
        )

        if response.get('ResponseCode') == '0':
            order.custom_mpesa_ticket_id = ticket.name
            order.payment_status = 'Pending'
            order.save()

            return {
                'success': True,
                'order_id': order_id,
                'ticket_id': ticket.name,
                'total': order.total_amount,
                'message': 'STK push sent. Enter PIN on your phone.',
                'redirect_url': f'/all-trails/payment-processing/{order_id}'
            }
        else:
            frappe.throw(f"STK push failed: {response.get('ResponseDesc')}")

    except Exception as e:
        frappe.logger().error(f"Payment initiation error: {str(e)}")
        raise frappe.ValidationError(str(e))

@frappe.whitelist()
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
    plan.first_payment_date = frappe.utils.today()
    plan.payment_frequency = 'Monthly'
    plan.payment_method = 'mpesa'
    plan.status = 'Active'
    plan.insert()

    # Update order
    order.bnpl_plan_id = plan.name
    order.payment_mode = 'Installment'
    order.save()

    # Initiate first payment
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
        'tracking_number': order.tracking_number,
        'created_at': order.order_date
    }

@frappe.whitelist(allow_guest=True)
def handle_merchandise_payment_callback():
    """
    Webhook: POST /api/method/all_trails.api.shop.handle_merchandise_payment_callback

    Receives MPESA callback from MPESA_TX module
    """
    from flask import request
    import json

    try:
        payload = request.get_json() or {}

        # Extract callback data
        body = payload.get('Body', {}).get('stkCallback', {})
        checkout_request_id = body.get('CheckoutRequestID')
        result_code = body.get('ResultCode')

        # Find order by ticket ID
        order_id = frappe.db.get_value(
            'Merchandise Order',
            {'custom_mpesa_ticket_id': checkout_request_id}
        )

        if not order_id:
            frappe.logger().warning(f"Order not found for ticket {checkout_request_id}")
            return {'ResultCode': 0, 'ResultDesc': 'Order not found'}

        order = frappe.get_doc('Merchandise Order', order_id)

        # Idempotency check
        if order.payment_status in ['Completed', 'Partial']:
            frappe.logger().info(f"Order {order_id} already processed")
            return {'ResultCode': 0, 'ResultDesc': 'Already processed'}

        # Extract callback metadata
        if result_code == 0:  # Success
            callback_metadata = body.get('CallbackMetadata', {}).get('Item', [])
            callback_items = {item.get('Name'): item.get('Value') for item in callback_metadata}

            receipt_number = callback_items.get('ReceiptNumber', '')
            amount = callback_items.get('Amount', 0)

            # Create Payment Entry
            payment_entry = frappe.new_doc('Payment Entry')
            payment_entry.payment_type = 'Receive'
            payment_entry.party_type = 'Contact'
            payment_entry.party = order.customer_id
            payment_entry.paid_from = 'Debtors - YC'
            payment_entry.paid_to = 'M-Pesa Receipts - YC'
            payment_entry.paid_amount = amount
            payment_entry.received_amount = amount
            payment_entry.reference_no = receipt_number
            payment_entry.insert()
            payment_entry.submit()

            # Create Sales Invoice
            sales_invoice = frappe.new_doc('Sales Invoice')
            sales_invoice.customer = order.customer_id
            sales_invoice.company = frappe.defaults.get_user_default('company')
            sales_invoice.posting_date = frappe.utils.today()
            sales_invoice.due_date = frappe.utils.today()
            sales_invoice.debit_to = 'Debtors - YC'

            for item in order.items:
                sales_invoice.append('items', {
                    'item_code': item.item_code,
                    'qty': item.quantity,
                    'rate': item.unit_price,
                    'warehouse': 'Stores'
                })

            sales_invoice.append('taxes', {
                'charge_type': 'On Net Total',
                'account_head': 'VAT - YC',
                'rate': 16
            })

            sales_invoice.insert()
            sales_invoice.submit()

            # Create Stock Entry (inventory reduction)
            stock_entry = frappe.new_doc('Stock Entry')
            stock_entry.stock_entry_type = 'Material Issue'
            stock_entry.company = frappe.defaults.get_user_default('company')
            stock_entry.posting_date = frappe.utils.today()

            for item in order.items:
                stock_entry.append('items', {
                    'item_code': item.item_code,
                    'qty': item.quantity,
                    's_warehouse': 'Stores',
                    't_warehouse': None,
                    'basic_rate': item.unit_price
                })

            stock_entry.insert()
            stock_entry.submit()

            # Update order
            order.payment_status = 'Completed'
            order.sales_invoice_id = sales_invoice.name
            order.fulfillment_status = 'Confirmed'
            order.estimated_delivery_date = add_days(frappe.utils.today(), 3)
            order.add_comment(
                'Comment',
                f'Payment received: KES {amount} (Ref: {receipt_number})',
                comment_type='Success'
            )
            order.save()

            # Send confirmation email
            frappe.sendmail(
                recipients=[order.customer_email],
                subject=f'Order Confirmed - {order.name}',
                template='merchandise_order_confirmation',
                args={
                    'order_id': order.name,
                    'items_count': len(order.items),
                    'total': order.total_amount,
                    'estimated_delivery': order.estimated_delivery_date
                }
            )

            frappe.logger().info(f"Payment processed for order {order.name}")

            return {'ResultCode': 0, 'ResultDesc': 'Payment processed successfully'}

        else:  # Failed
            order.payment_status = 'Failed'
            order.add_comment('Comment', f'Payment failed with result code {result_code}', 'Alert')
            order.save()

            frappe.sendmail(
                recipients=[order.customer_email],
                subject='Payment Failed - All Trails Order',
                template='merchandise_payment_failed',
                args={'order_id': order.name}
            )

            return {'ResultCode': 0, 'ResultDesc': 'Payment failed'}

    except Exception as e:
        frappe.logger().error(f"Callback handling error: {str(e)}")
        return {'ResultCode': 0, 'ResultDesc': 'Error processing callback'}

# Helper functions
def get_stock_balance(item_code, warehouse):
    """Get current stock balance for item in warehouse"""
    result = frappe.db.get_value(
        'Stock Ledger Entry',
        {'item_code': item_code, 'warehouse': warehouse, 'is_cancelled': 0},
        'sum(actual_qty)'
    )
    return result or 0
```

## Task 2.6: Create Background Jobs

**File**: `all_trails/tasks.py`

```python
import frappe
from frappe.utils import add_days, today, now_datetime
from datetime import timedelta

def process_bnpl_payments():
    """
    Background job: Every hour
    Attempts auto-payment for due BNPL installments
    """
    try:
        due_installments = frappe.get_list(
            'BNPL Installment',
            filters=[
                ['payment_status', '=', 'Pending'],
                ['due_date', '<=', today()]
            ],
            fields=['name', 'amount', 'plan', 'retry_count'],
            limit=100
        )

        for inst_record in due_installments:
            try:
                plan = frappe.get_doc('BNPL Plan', inst_record['plan'])
                order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

                # Attempt MPESA payment
                from all_trails.api.shop import initiate_mpesa_payment
                response = initiate_mpesa_payment(order.name, order.customer_phone)

                if response.get('success'):
                    inst = frappe.get_doc('BNPL Installment', inst_record['name'])
                    inst.payment_status = 'Paid'
                    inst.payment_date = now_datetime()
                    inst.retry_count = 0
                    inst.save()

                    frappe.logger().info(f"BNPL installment {inst_record['name']} paid")
                else:
                    inst = frappe.get_doc('BNPL Installment', inst_record['name'])
                    inst.retry_count = (inst.retry_count or 0) + 1

                    if inst.retry_count > 3:
                        inst.payment_status = 'Overdue'
                        plan.status = 'Defaulted'
                        plan.save()

                        # Create support ticket
                        support = frappe.new_doc('Support Ticket')
                        support.title = f'BNPL Payment Overdue - {order.name}'
                        support.status = 'Open'
                        support.priority = 'Medium'
                        support.insert()

                    inst.save()

            except Exception as e:
                frappe.logger().error(f"Error processing installment {inst_record['name']}: {str(e)}")

        frappe.logger().info(f"BNPL processing completed: {len(due_installments)} installments")

    except Exception as e:
        frappe.logger().error(f"BNPL processing failed: {str(e)}")

def send_bnpl_payment_reminders():
    """
    Background job: Daily 9 AM
    Sends payment reminders 3 days before installment due
    """
    reminder_date = add_days(today(), 3)

    due_soon = frappe.get_list(
        'BNPL Installment',
        filters=[
            ['payment_status', '=', 'Pending'],
            ['due_date', '=', reminder_date]
        ],
        fields=['name', 'plan', 'amount', 'installment_number']
    )

    for inst_record in due_soon:
        try:
            plan = frappe.get_doc('BNPL Plan', inst_record['plan'])
            order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

            frappe.sendmail(
                recipients=[order.customer_email],
                subject='Reminder: BNPL Payment Due in 3 Days',
                template='bnpl_payment_reminder',
                args={
                    'order_id': order.name,
                    'installment_number': inst_record['installment_number'],
                    'amount': inst_record['amount'],
                    'due_date': reminder_date
                }
            )
        except Exception as e:
            frappe.logger().error(f"Error sending reminder for {inst_record['name']}: {str(e)}")

def update_low_stock_alerts():
    """
    Background job: Every 6 hours
    Sends alerts for low stock items
    """
    items = frappe.get_list(
        'Merchandise Item',
        filters=[['is_active', '=', True]],
        fields=['item_code', 'item_name', 'warehouse', 'low_stock_threshold'],
        limit=500
    )

    for item in items:
        try:
            from all_trails.api.shop import get_stock_balance
            stock = get_stock_balance(item['item_code'], item['warehouse'])

            if stock <= item['low_stock_threshold']:
                frappe.logger().warning(f"Low stock: {item['item_code']} ({stock} units)")

                frappe.sendmail(
                    recipients=['operations@alltrails.co'],
                    subject=f'Low Stock Alert: {item["item_name"]}',
                    template='low_stock_alert_internal',
                    args={
                        'item_code': item['item_code'],
                        'item_name': item['item_name'],
                        'current_stock': stock,
                        'threshold': item['low_stock_threshold']
                    }
                )
        except Exception as e:
            frappe.logger().error(f"Error checking stock for {item['item_code']}: {str(e)}")

def auto_confirm_orders():
    """
    Background job: Every 30 minutes
    Auto-confirms paid orders
    """
    orders_to_confirm = frappe.get_list(
        'Merchandise Order',
        filters=[
            ['fulfillment_status', '=', 'Draft'],
            ['payment_status', '=', 'Completed']
        ],
        fields=['name'],
        limit=50
    )

    for order_record in orders_to_confirm:
        try:
            order = frappe.get_doc('Merchandise Order', order_record['name'])
            order.fulfillment_status = 'Processing'
            order.estimated_delivery_date = add_days(today(), 3)
            order.save()

            frappe.logger().info(f"Order {order.name} auto-confirmed")

        except Exception as e:
            frappe.logger().error(f"Error confirming order {order_record['name']}: {str(e)}")
```

## Task 2.7: Create Email Templates

Create these HTML files in `all_trails/templates/`:

**merchandise_order_confirmation.html**
```html
<h2>Order Confirmed!</h2>
<p>Thank you for your order {{ doc.name }}.</p>

<h3>Items</h3>
{% for item in doc.items %}
  <p>{{ item.item_code }} x{{ item.quantity }} @ KES {{ item.unit_price }}</p>
{% endfor %}

<p><strong>Total: KES {{ doc.total_amount }}</strong></p>
<p>Estimated Delivery: {{ doc.estimated_delivery_date }}</p>

<p><a href="{{ frappe.utils.get_url() }}/order/{{ doc.name }}">Track Your Order</a></p>
```

**merchandise_shipping_notification.html**
```html
<h2>Your Order is Shipping!</h2>
<p>Order {{ doc.name }} has been shipped.</p>
<p>Tracking Number: {{ doc.tracking_number }}</p>
<p>Estimated Delivery: {{ doc.estimated_delivery_date }}</p>
```

**merchandise_delivery_confirmation.html**
```html
<h2>Order Delivered!</h2>
<p>Your order {{ doc.name }} has been delivered.</p>
<p><a href="{{ frappe.utils.get_url() }}/review/{{ doc.name }}">Leave a Review</a></p>
```

**bnpl_payment_reminder.html**
```html
<h2>Payment Due!</h2>
<p>Your BNPL installment for order {{ doc.name }} is due on {{ due_date }}.</p>
<p>Amount Due: KES {{ amount }}</p>
<p><a href="{{ frappe.utils.get_url() }}/pay/{{ doc.name }}">Pay Now</a></p>
```

---

# PHASE 3: FRONTEND IMPLEMENTATION (Days 8-14)

**Due to length, frontend components follow the same pattern. Key files:**

Create in `frontend/src/components/glass/`:
- GlassCard.vue (base glassmorphic container)
- GlassButton.vue (interactive button with states)
- GlassInput.vue (form input)
- GlassModal.vue (dialog overlay)
- GlassProductCard.vue (product display)
- GlassCart.vue (shopping cart)
- GlassCheckoutFlow.vue (3-step checkout)
- Plus utilities (Alert, Spinner, etc.)

Create in `frontend/src/pages/shop/`:
- Browse.vue (product catalog with filters)
- Detail.vue (product detail view)
- Cart.vue (shopping cart)
- Checkout.vue (multi-step checkout form)
- PaymentProcessing.vue (MPESA STK display)
- Confirmation.vue (order confirmation)
- Tracking.vue (order status tracking)

Create in `frontend/src/stores/`:
- merchandiseStore.ts (Pinia store with cart, orders, payment state)

Create in `frontend/src/services/`:
- shopApi.ts (API client with type-safe calls)

Create in `frontend/src/types/`:
- shop.ts (TypeScript types for all entities)

---

# PHASE 4: TESTING (Days 15-21)

## Create Test Files

`tests/test_shop_api.py`:
```python
def test_get_catalog():
    result = frappe.call('all_trails.api.shop.get_merchandise_catalog')
    assert 'items' in result
    assert 'total_count' in result

def test_create_order():
    items = [{'item_code': 'ITEM-001', 'quantity': 1}]
    result = frappe.call('all_trails.api.shop.create_order', items=items, delivery_address='123 St', customer_phone='254700000000')
    assert result['success']
    assert 'order_id' in result

def test_bnpl_plan_creation():
    plan = frappe.new_doc('BNPL Plan')
    plan.merchandise_order = 'MO-2024-001'
    plan.total_amount = 6000
    plan.installment_count = 2
    plan.insert()
    assert len(plan.installments) == 2
```

---

# PHASE 5: DEPLOYMENT (Days 22-28)

## Migration Script

`all_trails/migrations/0001_create_merchandise_doctypes.py`:
```python
import frappe
from frappe.desk.reportview import get_count

def execute():
    # Create DocTypes
    doctypes = [
        'Merchandise Item',
        'Merchandise Order',
        'BNPL Plan',
        'Merchandise Review',
        'Merchandise Category'
    ]

    for doctype in doctypes:
        if not frappe.db.exists('DocType', doctype):
            frappe.get_doc({
                'doctype': 'DocType',
                'name': doctype
            }).insert()
            frappe.logger().info(f"Created DocType: {doctype}")

    # Create default category
    if not frappe.db.exists('Merchandise Category', 'Hiking Gear'):
        cat = frappe.new_doc('Merchandise Category')
        cat.category_name = 'Hiking Gear'
        cat.insert()

    # Create default warehouse if not exists
    if not frappe.db.exists('Warehouse', 'Merchandise Store'):
        warehouse = frappe.new_doc('Warehouse')
        warehouse.warehouse_name = 'Merchandise Store'
        warehouse.company = frappe.defaults.get_user_default('company')
        warehouse.insert()
```

## Deploy Steps

```bash
# 1. Run migration
bench execute all_trails.migrations.0001_create_merchandise_doctypes.execute

# 2. Seed sample data
bench console < /path/to/sample_data.sql

# 3. Configure payment webhook
# Set in MPESA Settings:
# - Callback URL: https://yourdomain.com/api/method/all_trails.api.shop.handle_merchandise_payment_callback

# 4. Configure scheduler
bench enable-scheduler

# 5. Test payment flow
# Create test order, verify STK push sent

# 6. Monitor logs
bench logs
```

---

# SUCCESS CRITERIA CHECKLIST

## Backend
- [ ] All 5 DocTypes created & validated
- [ ] All 8+ API endpoints working
- [ ] Payment callback idempotent (no double-charging)
- [ ] 4+ background jobs running on schedule
- [ ] All emails sending correctly
- [ ] Stock balance updates correctly

## Frontend
- [ ] All 8+ glass components rendering
- [ ] All 7+ pages working
- [ ] Forms validate properly
- [ ] Cart calculations correct
- [ ] Responsive on mobile/tablet/desktop
- [ ] Pinia store persisting state

## Integration
- [ ] Create order → MPESA STK → Payment → Invoice → Stock Entry
- [ ] BNPL plan created → First payment → Schedule second
- [ ] Auto-retry working after 30 days
- [ ] Callbacks processed idempotently
- [ ] Inventory prevents overselling

## Testing
- [ ] >90% code coverage
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] E2E tests passing
- [ ] Load test: 100+ concurrent users

## Deployment
- [ ] Database migrated successfully
- [ ] Payment webhook configured
- [ ] Background jobs running
- [ ] Monitoring alerts setup
- [ ] No critical errors in logs

---

# START HERE

1. **Read this entire prompt** (you're doing it!)
2. **Create directory structure** (Task 1.3)
3. **Create DocTypes** (Task 2.1-2.4) - Start with Merchandise Item
4. **Create APIs** (Task 2.5) - Implement get_merchandise_catalog first
5. **Create Jobs** (Task 2.6) - Setup background jobs
6. **Create Templates** (Task 2.7) - Email notifications
7. **Build Frontend Components** (Phase 3) - Start with GlassCard
8. **Build Shop Pages** (Phase 3) - Start with Browse.vue
9. **Test Everything** (Phase 4) - Run test suite
10. **Deploy** (Phase 5) - Run migrations, setup webhooks

---

**You have everything. Start building! 🚀**
