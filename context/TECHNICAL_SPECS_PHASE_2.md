# All Trails Phase 2: Detailed Technical Specifications

**Version**: 1.0
**Date**: 2026-03-14
**Status**: Ready for Development

---

## Part 1: Backend Technical Specifications

### Section 1.1: DocType Specifications

#### DocType: Merchandise Item

**Purpose**: Product catalog with merchandising metadata, pricing, inventory, media, and reviews

**JSON Schema Definition**:
```json
{
  "name": "Merchandise Item",
  "doctype": "DocType",
  "module": "All Trails",
  "is_submittable": false,
  "is_tree": false,
  "autoname": "field:item_code",
  "fields": [
    {
      "fieldname": "item_code",
      "fieldtype": "Data",
      "label": "Item Code",
      "unique": true,
      "reqd": true,
      "read_only": false,
      "allow_on_submit": false
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
      "fieldname": "sub_category",
      "fieldtype": "Data",
      "label": "Sub-Category"
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
      "label": "Description (Plain)"
    },
    {
      "fieldname": "description_html",
      "fieldtype": "Text Editor",
      "label": "Description (HTML Rich Text)"
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
      "label": "Discount Price (KES)",
      "help": "Optional discounted price for promotions"
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
      "fieldname": "bnpl_installment_count",
      "fieldtype": "Int",
      "label": "BNPL Installment Count",
      "default": 2
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
      "options": "json",
      "help": "[\"https://...\", \"https://...\"]"
    },
    {
      "fieldname": "gallery_images",
      "fieldtype": "Table",
      "label": "Gallery Images",
      "options": "Merchandise Item Gallery",
      "fields": [
        {
          "fieldname": "image_url",
          "fieldtype": "Attach Image",
          "label": "Image",
          "reqd": true
        },
        {
          "fieldname": "alt_text",
          "fieldtype": "Data",
          "label": "Alt Text"
        },
        {
          "fieldname": "caption",
          "fieldtype": "Data",
          "label": "Caption"
        }
      ]
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
      "options": "json",
      "help": "{\"material\": \"polyester\", \"weight\": \"500g\", \"color\": \"blue\"}"
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
      "fieldname": "suitable_for_trails",
      "fieldtype": "Link",
      "label": "Suitable for Trails (Multi)",
      "options": "Trail",
      "help": "Comma-separated trail names"
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

**Validation Rules** (in `merchandise_item.py`):
```python
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

        # Ensure warehouse exists and has stock capability
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
        # Count distinct customers who purchased this item
        return frappe.db.sql(
            """
            SELECT COUNT(DISTINCT customer_id) FROM `tabMerchandise Order`
            WHERE fulfillment_status = 'Delivered'
            AND items CONTAINS (SELECT JSON_EXTRACT(item_code, '$.item_code') = %s)
            """,
            self.item_code
        )[0][0]
```

---

#### DocType: Merchandise Order

**Purpose**: Order record linking customer, items, payment, and fulfillment

**JSON Schema** (excerpt):
```json
{
  "name": "Merchandise Order",
  "doctype": "DocType",
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
      "reqd": true,
      "fields": [
        {
          "fieldname": "item_code",
          "fieldtype": "Link",
          "label": "Item",
          "options": "Merchandise Item",
          "reqd": true
        },
        {
          "fieldname": "quantity",
          "fieldtype": "Int",
          "label": "Quantity",
          "reqd": true,
          "default": 1
        },
        {
          "fieldname": "unit_price",
          "fieldtype": "Currency",
          "label": "Unit Price",
          "read_only": true
        },
        {
          "fieldname": "discount_percentage",
          "fieldtype": "Percent",
          "label": "Discount %"
        },
        {
          "fieldname": "line_total",
          "fieldtype": "Currency",
          "label": "Line Total",
          "read_only": true
        }
      ]
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
      "label": "Discount Amount",
      "read_only": true
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
      "label": "BNPL Details",
      "depends_on": "eval:doc.payment_mode == 'Installment'"
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
  "workflows": [
    {
      "workflow_name": "Merchandise Order Workflow",
      "transitions": [
        {"from_state": "Draft", "to_state": "Confirmed", "action": "Confirm"},
        {"from_state": "Confirmed", "to_state": "Processing", "action": "Process"},
        {"from_state": "Processing", "to_state": "Shipped", "action": "Ship"},
        {"from_state": "Shipped", "to_state": "Delivered", "action": "Deliver"},
        {"from_state": "Any", "to_state": "Cancelled", "action": "Cancel"}
      ]
    }
  ]
}
```

**Validation & Hooks** (`merchandise_order.py`):
```python
class MerchandiseOrder(Document):
    def validate(self):
        # Validate items exist and have stock
        for item in self.items:
            from all_trails.api.shop import get_stock_balance
            stock = get_stock_balance(item.item_code, get_warehouse())
            if stock < item.quantity:
                frappe.throw(f"Insufficient stock: {item.item_code} (available: {stock}, requested: {item.quantity})")

        # Recalculate totals
        self.calculate_totals()

    def before_submit(self):
        # Set timestamps
        self.order_date = frappe.utils.now_datetime()

    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items)
        self.tax_amount = self.subtotal * 0.16  # 16% VAT
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - (self.discount_amount or 0)

    def on_update_after_submit(self):
        # Track status changes
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

        # Send customer notification
        if new_status == 'Shipped':
            self.send_shipping_notification()
        elif new_status == 'Delivered':
            self.send_delivery_notification()
            self.send_review_request()

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
            template='merchandise_delivery_notification',
            args={
                'order_id': self.name,
                'items_count': len(self.items),
                'total_amount': self.total_amount
            }
        )

    def send_review_request(self):
        frappe.enqueue(
            'all_trails.tasks.send_review_request_email',
            order_id=self.name,
            delay=86400  # Send after 1 day
        )
```

---

#### DocType: BNPL Plan

**Schema Excerpt**:
```python
{
  "name": "BNPL Plan",
  "fields": [
    {"fieldname": "plan_id", "fieldtype": "Data", "unique": true, "read_only": true},
    {"fieldname": "merchandise_order", "fieldtype": "Link", "options": "Merchandise Order", "reqd": true},
    {"fieldname": "total_amount", "fieldtype": "Currency", "reqd": true},
    {"fieldname": "installment_count", "fieldtype": "Int", "default": 2},
    {"fieldname": "installment_amount", "fieldtype": "Currency", "computed": true},
    {"fieldname": "first_payment_date", "fieldtype": "Date", "reqd": true},
    {"fieldname": "payment_frequency", "fieldtype": "Select", "options": "Weekly\nBi-weekly\nMonthly"},
    {"fieldname": "status", "fieldtype": "Select", "options": "Active\nCompleted\nDefaulted", "default": "Active"},
    {"fieldname": "payment_method", "fieldtype": "Select", "options": "MPESA\nCard", "default": "MPESA"},

    # Child table for installments
    {
      "fieldname": "installments",
      "fieldtype": "Table",
      "options": "BNPL Installment",
      "fields": [
        {"fieldname": "installment_number", "fieldtype": "Int"},
        {"fieldname": "due_date", "fieldtype": "Date"},
        {"fieldname": "amount", "fieldtype": "Currency"},
        {"fieldname": "payment_status", "fieldtype": "Select", "options": "Pending\nPaid\nOverdue"},
        {"fieldname": "payment_date", "fieldtype": "DateTime"},
        {"fieldname": "payment_entry_id", "fieldtype": "Link", "options": "Payment Entry"},
        {"fieldname": "retry_count", "fieldtype": "Int", "default": 0},
        {"fieldname": "last_error", "fieldtype": "Text"}
      ]
    },

    # Risk management
    {"fieldname": "customer_credit_score", "fieldtype": "Int"},
    {"fieldname": "approval_status", "fieldtype": "Select", "options": "Approved\nPending\nRejected"},
    {"fieldname": "declined_reason", "fieldtype": "Text"},
    {"fieldname": "automatic_retry", "fieldtype": "Check", "default": true},
    {"fieldname": "max_retries", "fieldtype": "Int", "default": 3},

    # Metadata
    {"fieldname": "created_date", "fieldtype": "DateTime", "read_only": true},
    {"fieldname": "next_payment_reminder_sent", "fieldtype": "Date"}
  ]
}
```

**Triggers & Logic** (`bnpl_plan.py`):
```python
class BNPLPlan(Document):
    def validate(self):
        if self.installment_count < 2:
            frappe.throw("Installment count must be at least 2")

        if len(self.installments) != self.installment_count:
            frappe.throw(f"Must have exactly {self.installment_count} installments")

    def on_insert(self):
        # Generate installment schedule
        self.generate_installment_schedule()

    def generate_installment_schedule(self):
        from frappe.utils import add_days

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

            # Calculate next due date based on frequency
            if self.payment_frequency == 'Weekly':
                current_date = add_days(current_date, 7)
            elif self.payment_frequency == 'Bi-weekly':
                current_date = add_days(current_date, 14)
            else:  # Monthly
                current_date = add_days(current_date, 30)

        self.save()

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

---

### Section 1.2: API Endpoint Specifications

#### Endpoint: GET /api/method/all_trails.api.shop.get_merchandise_catalog

**Request**:
```bash
curl -X GET "https://your-site.com/api/method/all_trails.api.shop.get_merchandise_catalog?category=Hiking%20Gear&limit=20&offset=0"
```

**Parameters**:
| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| category | string | No | - | Filter by category name |
| featured_only | bool | No | false | Show only featured items |
| limit | int | No | 20 | Items per page (max 100) |
| offset | int | No | 0 | Pagination offset |
| sort_by | string | No | position | Sort field: position/price/rating |
| sort_order | string | No | asc | asc or desc |

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "item_code": "STR-BACKPACK-001",
        "item_name": "Premium Hiking Backpack 65L",
        "category": "Hiking Gear",
        "sku": "PACK-650-BLK",
        "price": 8500,
        "discount_price": 7200,
        "discount_percentage": 15,
        "rating": 4.5,
        "reviews_count": 23,
        "image_url": "https://cdn.alltrails.co/backpack-001.jpg",
        "in_stock": true,
        "stock_quantity": 15,
        "bnpl_eligible": true,
        "bnpl_installment_count": 2,
        "brand": "Summit Gear"
      },
      {
        "item_code": "STR-BOOTS-002",
        "item_name": "Trekking Boots - Mountain Pro",
        "category": "Hiking Gear",
        "sku": "BOOT-MP-BRN",
        "price": 6500,
        "discount_price": null,
        "discount_percentage": 0,
        "rating": 4.7,
        "reviews_count": 34,
        "image_url": "https://cdn.alltrails.co/boots-002.jpg",
        "in_stock": true,
        "stock_quantity": 24,
        "bnpl_eligible": true,
        "bnpl_installment_count": 2,
        "brand": "Merrell"
      }
    ],
    "pagination": {
      "total_count": 87,
      "limit": 20,
      "offset": 0,
      "has_more": true,
      "pages": 5
    }
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "status": "error",
  "message": "Invalid category",
  "code": "INVALID_CATEGORY"
}
```

---

#### Endpoint: POST /api/method/all_trails.api.shop.create_order

**Request Body**:
```json
{
  "items": [
    {
      "item_code": "STR-BACKPACK-001",
      "quantity": 1
    },
    {
      "item_code": "STR-BOOTS-002",
      "quantity": 1
    }
  ],
  "delivery_address": "123 Nairobi Road, Nairobi 00100",
  "customer_phone": "254700123456",
  "coupon_code": "WELCOME10",
  "payment_method": "mpesa",
  "payment_mode": "full"
}
```

**Validation Rules**:
```python
def validate_create_order_request(data):
    errors = []

    # Validate items
    if not data.get('items') or len(data['items']) == 0:
        errors.append("At least one item required")

    for item in data.get('items', []):
        if not item.get('item_code'):
            errors.append("Item code required")
        if not item.get('quantity') or item['quantity'] < 1:
            errors.append("Quantity must be >= 1")

    # Validate phone
    phone = data.get('customer_phone', '').strip()
    if not phone or not phone.startswith('254') or len(phone) != 12:
        errors.append("Valid Kenyan phone required (254XXXXXXXXX)")

    # Validate address
    if not data.get('delivery_address') or len(data['delivery_address']) < 10:
        errors.append("Valid delivery address required")

    # Validate payment method
    if data.get('payment_method') not in ['mpesa', 'card', 'bnpl']:
        errors.append("Invalid payment method")

    return errors
```

**Response** (201 Created):
```json
{
  "status": "success",
  "data": {
    "order_id": "MO-2024-00157",
    "order_date": "2026-03-14T10:30:00Z",
    "customer_email": "user@example.com",
    "items_count": 2,
    "subtotal": 14700,
    "discount_amount": 1470,
    "shipping_cost": 300,
    "tax_amount": 2131.2,
    "total_amount": 15661.2,
    "payment_method": "mpesa",
    "payment_status": "pending",
    "fulfillment_status": "draft",
    "mpesa_ticket_id": "STK-62f7e9e7-6c4e-11eb-ae93-0242ac150002",
    "redirect_url": "/all-trails/checkout/MO-2024-00157"
  }
}
```

---

#### Endpoint: POST /api/method/all_trails.api.shop.validate_coupon

**Request**:
```json
{
  "code": "WELCOME10",
  "order_total": 14700
}
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "valid": true,
    "code": "WELCOME10",
    "discount_type": "percentage",
    "discount_percentage": 10,
    "discount_amount": 1470,
    "min_order_amount": 5000,
    "max_uses": 100,
    "usage_count": 45,
    "remaining_uses": 55,
    "valid_until": "2026-12-31",
    "message": "Coupon applied successfully!"
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "status": "error",
  "message": "Invalid or expired coupon code",
  "code": "INVALID_COUPON"
}
```

---

#### Endpoint: GET /api/method/all_trails.api.shop.get_order_status

**Request**:
```bash
curl -X GET "https://your-site.com/api/method/all_trails.api.shop.get_order_status?order_id=MO-2024-00157"
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "order_id": "MO-2024-00157",
    "order_date": "2026-03-14T10:30:00Z",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "254700123456",
    "fulfillment_status": "processing",
    "payment_status": "completed",
    "payment_method": "mpesa",
    "payment_mode": "full",
    "items": [
      {
        "item_code": "STR-BACKPACK-001",
        "item_name": "Premium Hiking Backpack 65L",
        "quantity": 1,
        "unit_price": 8500,
        "line_total": 8500
      },
      {
        "item_code": "STR-BOOTS-002",
        "item_name": "Trekking Boots - Mountain Pro",
        "quantity": 1,
        "unit_price": 6200,
        "line_total": 6200
      }
    ],
    "subtotal": 14700,
    "tax_amount": 2352,
    "shipping_cost": 300,
    "total_amount": 17352,
    "shipping_address": "123 Nairobi Road, Nairobi 00100",
    "estimated_delivery_date": "2026-03-18",
    "actual_delivery_date": null,
    "tracking_number": "TRK-9K8L7M6N5O",
    "tracking_url": "https://tracking.alltrails.co/TRK-9K8L7M6N5O",
    "timeline": [
      {
        "status": "Confirmed",
        "timestamp": "2026-03-14T10:35:00Z",
        "message": "Order confirmed and payment verified"
      },
      {
        "status": "Processing",
        "timestamp": "2026-03-14T14:20:00Z",
        "message": "Items picked and packed"
      }
    ],
    "next_action": "Awaiting shipment"
  }
}
```

---

### Section 1.3: Background Job Specifications

#### Job 1: Process BNPL Payments (Hourly)

**Schedule**: Every hour at minute 0
**Timeout**: 10 minutes
**Failure Recovery**: Retry up to 3 times with 5-minute intervals

```python
@frappe.whitelist()
def process_bnpl_payments():
    """
    Process due BNPL installments
    - Find installments with due_date <= today
    - Attempt MPESA payment via MPESA_TX
    - Handle failures gracefully
    - Mark as paid if successful
    """
    try:
        due_installments = get_due_installments()

        for installment_record in due_installments:
            process_single_installment(installment_record)

        frappe.logger().info(f"BNPL processing completed: {len(due_installments)} installments")

    except Exception as e:
        frappe.logger().error(f"BNPL processing failed: {str(e)}")
        raise

def get_due_installments():
    """Find pending installments due today or overdue"""
    return frappe.get_list(
        'BNPL Installment',
        filters=[
            ['payment_status', '=', 'Pending'],
            ['due_date', '<=', frappe.utils.today()],
            ['retry_count', '<', 3]
        ],
        fields=['name', 'amount', 'plan', 'retry_count'],
        order_by='due_date asc',
        limit=100
    )

def process_single_installment(installment_record):
    """Attempt payment for single installment"""
    try:
        installment = frappe.get_doc('BNPL Installment', installment_record['name'])
        plan = frappe.get_doc('BNPL Plan', installment_record['plan'])
        order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

        # Attempt MPESA payment
        response = initiate_mpesa_payment_for_bnpl(
            order_id=order.name,
            phone_number=order.customer_phone,
            amount=installment.amount,
            installment_id=installment.name
        )

        if response.get('success'):
            # Mark as paid
            installment.payment_status = 'Paid'
            installment.payment_date = frappe.utils.now_datetime()
            installment.retry_count = 0
            installment.save()

            frappe.logger().info(f"BNPL installment {installment.name} processed successfully")
        else:
            # Increment retry count
            installment.retry_count = (installment.retry_count or 0) + 1
            installment.last_error = response.get('message', 'Unknown error')

            # Check if overdue (>7 days)
            if (frappe.utils.today() - installment.due_date).days > 7:
                installment.payment_status = 'Overdue'
                escalate_to_support(installment)

            installment.save()
            frappe.logger().warning(f"BNPL installment {installment.name} retry {installment.retry_count}")

    except Exception as e:
        frappe.logger().error(f"Error processing installment {installment_record['name']}: {str(e)}")

def escalate_to_support(installment):
    """Create support ticket for overdue installment"""
    plan = frappe.get_doc('BNPL Plan', installment.plan)
    order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

    support_ticket = frappe.new_doc('Support Ticket')
    support_ticket.title = f'BNPL Payment Overdue - {order.name}'
    support_ticket.description = f'Installment {installment.installment_number} for order {order.name} is overdue'
    support_ticket.priority = 'Medium'
    support_ticket.status = 'Open'
    support_ticket.insert()

    # Send email to support team
    frappe.sendmail(
        recipients=['support@alltrails.co'],
        subject=f'BNPL Payment Escalation - {order.name}',
        template='bnpl_escalation',
        args={'order_id': order.name, 'installment_id': installment.name}
    )
```

---

#### Job 2: Send BNPL Payment Reminders (Daily at 9 AM)

```python
@frappe.whitelist()
def send_bnpl_payment_reminders():
    """
    Send payment reminders 3 days before installment due date
    """
    reminder_date = frappe.utils.add_days(frappe.utils.today(), 3)

    due_soon = frappe.get_list(
        'BNPL Installment',
        filters=[
            ['payment_status', '=', 'Pending'],
            ['due_date', '=', reminder_date]
        ],
        fields=['name', 'plan', 'amount', 'installment_number']
    )

    for inst_record in due_soon:
        send_reminder_email(inst_record)

def send_reminder_email(installment_record):
    plan = frappe.get_doc('BNPL Plan', installment_record['plan'])
    order = frappe.get_doc('Merchandise Order', plan.merchandise_order)

    frappe.sendmail(
        recipients=[order.customer_email],
        subject=f'Reminder: BNPL Payment Due in 3 Days',
        template='bnpl_payment_reminder',
        args={
            'order_id': order.name,
            'installment_number': installment_record['installment_number'],
            'amount': installment_record['amount'],
            'due_date': frappe.utils.add_days(frappe.utils.today(), 3),
            'payment_link': f"{frappe.utils.get_url()}/order/{order.name}/pay"
        }
    )
```

---

### Section 1.4: Payment Flow Implementation

#### Flow: MPESA Full Payment

```python
# all_trails/api/payment_handler.py

@frappe.whitelist()
def initiate_mpesa_payment(order_id, phone_number):
    """
    Initiates MPESA STK push for merchandise order

    Returns:
        {
            'success': bool,
            'order_id': str,
            'ticket_id': str,
            'total': float,
            'message': str
        }
    """
    try:
        order = frappe.get_doc('Merchandise Order', order_id)

        # Validate order state
        if order.payment_status != 'Pending':
            frappe.throw(f"Order {order_id} already processed")

        # Create MPESA Ticket
        ticket = frappe.new_doc('MPESA Ticket')
        ticket.name = frappe.generate_hash(length=16)
        ticket.msisdn = phone_number
        ticket.amount = order.total_amount
        ticket.account_number = order_id
        ticket.description = f'Merchandise {order_id}'
        ticket.ticket_status = 'Initiated'
        ticket.insert()

        # Initiate STK via MPESA_TX
        from mpesa_tx.api.mpesa_handler import MPESAHandler
        handler = MPESAHandler()

        response = handler.initiate_stk_push(
            phone_number=phone_number,
            amount=int(order.total_amount),
            account_reference=order_id,
            transaction_desc=f'Order {order_id}'
        )

        if response.get('ResponseCode') == '0':
            # Store ticket ID in order for later linking
            order.custom_mpesa_ticket_id = ticket.name
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
            frappe.throw(f"STK push failed: {response.get('ResponseDesc')}")

    except Exception as e:
        frappe.logger().error(f"Payment initiation error: {str(e)}")
        raise frappe.ValidationError(str(e))


@frappe.whitelist(allow_guest=True)
def handle_merchandise_payment_callback():
    """
    Webhook: POST /api/method/all_trails.api.payment_handler.handle_merchandise_payment_callback

    Receives MPESA callback from MPESA_TX module
    Links to merchandise order and updates status
    """
    from flask import request
    import json

    try:
        payload = request.get_json() or {}

        # Extract callback data
        callback_handler = MerchandisePaymentCallbackHandler(payload)
        result = callback_handler.handle()

        # Return M-Pesa compatible response
        return {
            'ResultCode': 0,  # Always return 0 to prevent retries
            'ResultDesc': result['message']
        }

    except Exception as e:
        frappe.logger().error(f"Callback handling error: {str(e)}")
        return {
            'ResultCode': 0,
            'ResultDesc': 'Callback received'
        }


class MerchandisePaymentCallbackHandler:
    """
    Idempotent callback handler extending MPESA_TX architecture
    """

    def __init__(self, payload):
        self.payload = payload
        self.body = payload.get('Body', {}).get('stkCallback', {})

        self.checkout_request_id = self.body.get('CheckoutRequestID')
        self.result_code = self.body.get('ResultCode')
        self.result_desc = self.body.get('ResultDesc', '')
        self.merchant_request_id = self.body.get('MerchantRequestID', '')

        # Extract callback metadata
        callback_metadata = self.body.get('CallbackMetadata', {}).get('Item', [])
        self.callback_items = {item.get('Name'): item.get('Value') for item in callback_metadata}

        self.receipt_number = self.callback_items.get('ReceiptNumber', '')
        self.amount = self.callback_items.get('Amount', 0)
        self.phone_number = self.callback_items.get('PhoneNumber', '')

    def handle(self):
        """Main callback handler"""
        try:
            # Find order by account_number (which is order_id)
            order_id = self.checkout_request_id
            order = frappe.get_doc('Merchandise Order', order_id)

            # Check if already processed (idempotency)
            if order.payment_status in ['Completed', 'Partial']:
                frappe.logger().info(f"Order {order_id} already processed")
                return {
                    'success': True,
                    'message': f'Order {order_id} already processed',
                    'order_id': order_id
                }

            # Process based on result code
            if self.result_code == 0:
                return self._handle_successful_payment(order)
            else:
                return self._handle_failed_payment(order)

        except frappe.DoesNotExistError:
            frappe.logger().warning(f"Order {order_id} not found")
            return {
                'success': False,
                'message': 'Order not found',
                'order_id': order_id
            }

    def _handle_successful_payment(self, order):
        """Process successful MPESA payment"""
        try:
            # Create Payment Entry
            payment_entry = frappe.new_doc('Payment Entry')
            payment_entry.payment_type = 'Receive'
            payment_entry.party_type = 'Contact'
            payment_entry.party = order.customer_id
            payment_entry.paid_from = 'Debtors - YC'
            payment_entry.paid_to = 'M-Pesa Receipts - YC'
            payment_entry.paid_amount = self.amount
            payment_entry.received_amount = self.amount
            payment_entry.reference_no = self.receipt_number
            payment_entry.reference_date = frappe.utils.today()
            payment_entry.insert()
            payment_entry.submit()

            # Create Sales Invoice (if not exists)
            sales_invoice = create_sales_invoice_from_order(order)

            # Create Stock Entry (inventory reduction)
            stock_entry = create_stock_entry_from_order(order)

            # Update order
            order.payment_status = 'Completed'
            order.sales_invoice_id = sales_invoice.name if sales_invoice else None
            order.fulfillment_status = 'Confirmed'
            order.estimated_delivery_date = frappe.utils.add_days(frappe.utils.today(), 3)
            order.add_comment(
                'Comment',
                f'Payment received: KES {self.amount} (M-Pesa Ref: {self.receipt_number})',
                comment_type='Success'
            )
            order.save()

            # Send confirmation email
            send_order_confirmation_email(order)

            frappe.logger().info(f"Payment processed successfully for order {order.name}")

            return {
                'success': True,
                'message': 'Payment processed successfully',
                'order_id': order.name
            }

        except Exception as e:
            frappe.logger().error(f"Payment processing error: {str(e)}")
            order.payment_status = 'Failed'
            order.add_comment('Comment', f'Payment error: {str(e)}', 'Alert')
            order.save()
            return {
                'success': False,
                'message': str(e),
                'order_id': order.name
            }

    def _handle_failed_payment(self, order):
        """Process failed MPESA payment"""
        failure_reasons = {
            1: 'User cancelled the transaction',
            2: 'Request timeout',
            17: 'Transaction timeout'
        }
        reason = failure_reasons.get(self.result_code, 'Payment declined')

        order.payment_status = 'Failed'
        order.add_comment('Comment', f'Payment failed: {reason}', 'Alert')
        order.save()

        # Send failure notification
        frappe.sendmail(
            recipients=[order.customer_email],
            subject='Payment Failed - All Trails Order',
            template='merchandise_payment_failed',
            args={'order_id': order.name, 'reason': reason}
        )

        frappe.logger().warning(f"Payment failed for order {order.name}: {reason}")

        return {
            'success': True,
            'message': f'Payment failed: {reason}',
            'order_id': order.name
        }


def create_sales_invoice_from_order(order):
    """
    Create Sales Invoice from Merchandise Order
    Links to customer and items
    """
    sales_invoice = frappe.new_doc('Sales Invoice')
    sales_invoice.customer = order.customer_id
    sales_invoice.company = frappe.defaults.get_user_default('company')
    sales_invoice.posting_date = frappe.utils.today()
    sales_invoice.due_date = frappe.utils.today()
    sales_invoice.debit_to = 'Debtors - YC'

    # Add items
    for item in order.items:
        sales_invoice.append('items', {
            'item_code': item.item_code,
            'qty': item.quantity,
            'rate': item.unit_price,
            'warehouse': get_warehouse()
        })

    # Add tax
    sales_invoice.append('taxes', {
        'charge_type': 'On Net Total',
        'account_head': 'VAT - YC',
        'rate': 16
    })

    sales_invoice.custom_merchandise_order_id = order.name
    sales_invoice.insert()
    sales_invoice.submit()

    return sales_invoice


def create_stock_entry_from_order(order):
    """
    Create Stock Entry to reduce inventory
    """
    stock_entry = frappe.new_doc('Stock Entry')
    stock_entry.stock_entry_type = 'Material Issue'
    stock_entry.company = frappe.defaults.get_user_default('company')
    stock_entry.posting_date = frappe.utils.today()

    for item in order.items:
        stock_entry.append('items', {
            'item_code': item.item_code,
            'qty': item.quantity,
            's_warehouse': get_warehouse(),
            't_warehouse': None,
            'basic_rate': item.unit_price
        })

    stock_entry.custom_merchandise_order_id = order.name
    stock_entry.insert()
    stock_entry.submit()

    return stock_entry
```

---

## Part 2: Frontend Technical Specifications

### Section 2.1: Component Specifications

#### Component: GlassCard

**Purpose**: Base glassmorphic container component

**Props**:
```typescript
interface GlassCardProps {
  padding?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' // default: 'md'
  rounded?: 'sm' | 'md' | 'lg' | 'xl' // default: 'lg'
  border?: boolean // default: true
  shadow?: 'sm' | 'md' | 'lg' // default: 'md'
  glow?: boolean // default: true
  hoverEffect?: 'none' | 'lift' | 'brighten' // default: 'lift'
  darkMode?: boolean
  children: React.ReactNode
  className?: string
  onClick?: () => void
}
```

**CSS Implementation**:
```css
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-backdrop-blur));
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  border-radius: var(--radius-lg);
  transition: all 300ms ease-out;
}

.glass-card.glow {
  box-shadow:
    var(--glass-shadow),
    var(--glass-inner-glow);
}

.glass-card.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow:
    0 12px 40px rgba(0, 0, 0, 0.15),
    var(--glass-inner-glow);
  background: rgba(27, 58, 45, 0.95);
}

.glass-card.hover-brighten:hover {
  background: rgba(27, 58, 45, 0.95);
  border-color: var(--accent-orange);
}

@media (max-width: 768px) {
  .glass-card {
    backdrop-filter: blur(var(--glass-backdrop-blur-mobile));
  }
}
```

**Vue 3 Implementation**:
```vue
<template>
  <div
    :class="[
      'glass-card',
      `padding-${padding}`,
      `rounded-${rounded}`,
      { 'border': border },
      `shadow-${shadow}`,
      { 'glow': glow },
      `hover-${hoverEffect}`,
      { 'dark-mode': darkMode },
      className
    ]"
    @click="onClick"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  padding?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  rounded?: 'sm' | 'md' | 'lg' | 'xl'
  border?: boolean
  shadow?: 'sm' | 'md' | 'lg'
  glow?: boolean
  hoverEffect?: 'none' | 'lift' | 'brighten'
  darkMode?: boolean
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  rounded: 'lg',
  border: true,
  shadow: 'md',
  glow: true,
  hoverEffect: 'lift',
  darkMode: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const onClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>

<style scoped>
/* Padding variants */
.padding-xs { padding: 0.5rem; }
.padding-sm { padding: 0.75rem; }
.padding-md { padding: 1rem; }
.padding-lg { padding: 1.5rem; }
.padding-xl { padding: 2rem; }

/* Rounded variants */
.rounded-sm { border-radius: 4px; }
.rounded-md { border-radius: 8px; }
.rounded-lg { border-radius: 12px; }
.rounded-xl { border-radius: 16px; }

/* Shadow variants */
.shadow-sm {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.shadow-md {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
.shadow-lg {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
}
</style>
```

---

#### Component: GlassCart

**Purpose**: Shopping cart display with item management

**Slot Structure**:
```vue
<GlassCart
  :items="cartItems"
  :subtotal="cartTotal"
  :discount="appliedDiscount"
  :shipping="shippingCost"
  :tax="taxAmount"
  :total="finalTotal"
  :isLoading="isProcessing"
  @update-quantity="handleQuantityUpdate"
  @remove-item="handleItemRemoval"
  @apply-coupon="handleCouponApplication"
  @checkout="handleCheckout"
>
  <template #header>
    <h2>Your Cart ({{ itemCount }} items)</h2>
  </template>

  <template #item="{ item }">
    <GlassCartItem
      :item="item"
      @update-quantity="$emit('update-quantity', $event)"
      @remove="$emit('remove-item', $event)"
    />
  </template>

  <template #empty>
    <div class="empty-state">
      <p>Your cart is empty</p>
      <GlassButton @click="$router.push('/all-trails/shop')">
        Continue Shopping
      </GlassButton>
    </div>
  </template>

  <template #summary>
    <CartSummary
      :subtotal="subtotal"
      :discount="discount"
      :shipping="shipping"
      :tax="tax"
      :total="total"
    />
  </template>

  <template #actions>
    <GlassButton
      variant="primary"
      size="lg"
      :loading="isLoading"
      @click="@checkout"
    >
      Proceed to Checkout
    </GlassButton>
  </template>
</GlassCart>
```

**Implementation**:
```vue
<template>
  <GlassCard class="glass-cart" :glow="true">
    <!-- Header -->
    <div class="cart-header">
      <slot name="header">
        <h2>Shopping Cart</h2>
      </slot>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>

    <!-- Items List -->
    <div class="cart-items">
      <div v-if="items.length === 0" class="empty-state">
        <slot name="empty">
          <p>Your cart is empty</p>
        </slot>
      </div>

      <div v-else class="items-list">
        <slot
          v-for="item in items"
          :key="item.itemCode"
          name="item"
          :item="item"
        />
      </div>
    </div>

    <!-- Divider -->
    <div class="cart-divider"></div>

    <!-- Summary -->
    <div class="cart-summary">
      <slot name="summary">
        <CartSummary
          :subtotal="subtotal"
          :discount="discount"
          :shipping="shipping"
          :tax="tax"
          :total="total"
        />
      </slot>
    </div>

    <!-- Promo Code -->
    <div class="promo-section">
      <GlassInput
        v-model="couponCode"
        placeholder="Enter promo code"
        @keyup.enter="applyCoupon"
      />
      <GlassButton
        variant="secondary"
        @click="applyCoupon"
        :loading="isApplyingCoupon"
      >
        Apply
      </GlassButton>
    </div>

    <!-- Action Buttons -->
    <div class="cart-actions">
      <slot name="actions">
        <GlassButton
          variant="primary"
          size="lg"
          @click="proceedToCheckout"
          :loading="isLoading"
          :disabled="items.length === 0"
        >
          Checkout
        </GlassButton>
      </slot>
    </div>
  </GlassCard>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface CartItem {
  itemCode: string
  itemName: string
  quantity: number
  unitPrice: number
  image: string
  discountPercentage?: number
}

interface Props {
  items: CartItem[]
  subtotal: number
  discount?: number
  shipping: number
  tax: number
  total: number
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  discount: 0,
  isLoading: false
})

const emit = defineEmits<{
  'update-quantity': [{ itemCode: string; quantity: number }]
  'remove-item': [itemCode: string]
  'apply-coupon': [code: string]
  'checkout': []
  'close': []
}>()

const couponCode = ref('')
const isApplyingCoupon = ref(false)

const itemCount = computed(() =>
  props.items.reduce((sum, item) => sum + item.quantity, 0)
)

const applyCoupon = async () => {
  if (!couponCode.value.trim()) return

  isApplyingCoupon.value = true
  try {
    emit('apply-coupon', couponCode.value)
    couponCode.value = ''
  } finally {
    isApplyingCoupon.value = false
  }
}

const proceedToCheckout = () => {
  emit('checkout')
}
</script>

<style scoped>
.glass-cart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-height: 90vh;
  overflow-y: auto;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--glass-border);
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: var(--color-text);
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background 200ms;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 2rem 0;
  color: var(--color-text-secondary);
}

.cart-divider {
  height: 1px;
  background: var(--glass-border);
  margin: 0.5rem 0;
}

.promo-section {
  display: flex;
  gap: 0.5rem;
}

.cart-actions {
  display: flex;
  gap: 0.75rem;
}

@media (max-width: 768px) {
  .glass-cart {
    max-height: 100vh;
  }
}
</style>
```

---

#### Component: GlassCheckoutFlow

**Purpose**: Multi-step checkout form

**States & Steps**:
```typescript
enum CheckoutStep {
  DELIVERY = 'delivery',
  PAYMENT = 'payment',
  CONFIRMATION = 'confirmation'
}

interface CheckoutState {
  step: CheckoutStep
  deliveryAddress: string
  customerPhone: string
  paymentMethod: 'mpesa' | 'card' | 'bnpl'
  paymentMode: 'full' | 'installment'
  isProcessing: boolean
  error?: string
}
```

**Component Structure**:
```vue
<template>
  <GlassModal @close="closeModal">
    <div class="checkout-container">
      <!-- Progress Indicator -->
      <div class="progress-bar">
        <div
          v-for="(step, index) in steps"
          :key="step"
          :class="[
            'progress-step',
            { 'active': currentStepIndex === index },
            { 'completed': currentStepIndex > index }
          ]"
        >
          {{ index + 1 }}
        </div>
      </div>

      <!-- Step Content -->
      <div class="checkout-content">
        <!-- Step 1: Delivery -->
        <div v-if="step === 'delivery'" class="checkout-step">
          <h3>Delivery Address</h3>
          <GlassInput
            v-model="form.deliveryAddress"
            type="textarea"
            label="Full Address"
            placeholder="123 Main Street, Nairobi..."
            :error="errors.deliveryAddress"
            required
          />
          <GlassInput
            v-model="form.customerPhone"
            label="Phone Number"
            placeholder="254700000000"
            type="tel"
            :error="errors.customerPhone"
            required
          />
          <GlassButton
            variant="primary"
            @click="nextStep"
            :disabled="!isStepValid('delivery')"
          >
            Continue to Payment
          </GlassButton>
        </div>

        <!-- Step 2: Payment -->
        <div v-if="step === 'payment'" class="checkout-step">
          <h3>Choose Payment Method</h3>

          <!-- Payment Method Selection -->
          <div class="payment-methods">
            <GlassCard
              class="payment-option"
              :class="{ 'selected': form.paymentMethod === 'mpesa' }"
              @click="selectPaymentMethod('mpesa')"
            >
              <h4>M-Pesa</h4>
              <p>Pay now with M-Pesa</p>
            </GlassCard>

            <GlassCard
              class="payment-option"
              :class="{ 'selected': form.paymentMethod === 'bnpl' }"
              @click="selectPaymentMethod('bnpl')"
            >
              <h4>Buy Now, Pay Later</h4>
              <p>2 installments, 0% interest</p>
            </GlassCard>
          </div>

          <!-- BNPL Details -->
          <div v-if="form.paymentMethod === 'bnpl'" class="bnpl-details">
            <p>Total: KES {{ total }}</p>
            <p class="installment-info">
              2 payments of KES {{ (total / 2).toFixed(0) }}
            </p>
            <p class="fine-print">
              First payment due today, second payment in 30 days
            </p>
          </div>

          <div class="button-group">
            <GlassButton variant="secondary" @click="previousStep">
              Back
            </GlassButton>
            <GlassButton
              variant="primary"
              @click="nextStep"
            >
              Continue
            </GlassButton>
          </div>
        </div>

        <!-- Step 3: Confirmation -->
        <div v-if="step === 'confirmation'" class="checkout-step">
          <h3>Order Summary</h3>
          <OrderReview :order="orderSummary" />

          <div class="button-group">
            <GlassButton variant="secondary" @click="previousStep">
              Back
            </GlassButton>
            <GlassButton
              variant="primary"
              @click="processPayment"
              :loading="isProcessing"
            >
              Place Order
            </GlassButton>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="error-alert">
        {{ error }}
      </div>
    </div>
  </GlassModal>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const steps = ['delivery', 'payment', 'confirmation']
const step = ref('delivery')
const isProcessing = ref(false)
const error = ref('')

const form = reactive({
  deliveryAddress: '',
  customerPhone: '',
  paymentMethod: 'mpesa' as 'mpesa' | 'bnpl',
  paymentMode: 'full' as 'full' | 'installment'
})

const errors = reactive({
  deliveryAddress: '',
  customerPhone: ''
})

const currentStepIndex = computed(() => steps.indexOf(step.value))

const selectPaymentMethod = (method: string) => {
  form.paymentMethod = method as 'mpesa' | 'bnpl'
  if (method === 'bnpl') {
    form.paymentMode = 'installment'
  } else {
    form.paymentMode = 'full'
  }
}

const isStepValid = (stepName: string) => {
  if (stepName === 'delivery') {
    return form.deliveryAddress.length > 10 && form.customerPhone.length === 12
  }
  return true
}

const nextStep = () => {
  const nextIndex = currentStepIndex.value + 1
  if (nextIndex < steps.length) {
    step.value = steps[nextIndex]
  }
}

const previousStep = () => {
  const prevIndex = currentStepIndex.value - 1
  if (prevIndex >= 0) {
    step.value = steps[prevIndex]
  }
}

const processPayment = async () => {
  isProcessing.value = true
  try {
    // Call API to create order
    const response = await createOrder({
      items: [],  // Cart items from parent
      delivery_address: form.deliveryAddress,
      customer_phone: form.customerPhone,
      payment_method: form.paymentMethod,
      payment_mode: form.paymentMode
    })

    // Redirect to payment
    window.location.href = response.redirect_url
  } catch (err: any) {
    error.value = err.message || 'Checkout failed'
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.checkout-container {
  max-width: 500px;
  margin: 0 auto;
}

.progress-bar {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  gap: 1rem;
}

.progress-step {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid var(--glass-border);
  font-weight: bold;
  transition: all 300ms;
}

.progress-step.active {
  background: var(--accent-orange);
  border-color: var(--accent-orange);
  color: white;
}

.progress-step.completed {
  background: var(--accent-success);
  border-color: var(--accent-success);
}

.checkout-step {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-option {
  cursor: pointer;
  padding: 1rem;
  text-align: center;
  border: 2px solid transparent;
  transition: all 200ms;
}

.payment-option:hover {
  border-color: var(--accent-orange);
}

.payment-option.selected {
  background: rgba(232, 93, 31, 0.1);
  border-color: var(--accent-orange);
}

.bnpl-details {
  background: rgba(16, 185, 129, 0.1);
  border-left: 4px solid var(--accent-success);
  padding: 1rem;
  border-radius: 8px;
}

.installment-info {
  font-weight: bold;
  color: var(--accent-success);
}

.fine-print {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin-top: 0.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.error-alert {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid #EF4444;
  padding: 1rem;
  border-radius: 8px;
  color: #EF4444;
  margin-top: 1rem;
}
</style>
```

---

(Continuing in next response due to length...)
