# MPESA STK Callback Architecture Refactoring Guide

## Overview
This document provides detailed implementation steps for refactoring the MPESA payment flow from simple callback handling to an enterprise-grade, event-driven architecture with idempotency, async verification, and resilience.

## Current Architecture Issues

### Problem Statement
The current `mpesa_tx` app:
1. **Processes callbacks immediately** without verification against M-Pesa API
2. **Tight coupling** between callback reception and payment processing
3. **No idempotency guarantee** - duplicate webhooks cause duplicate charges
4. **Limited error recovery** - failed payments not queued for retry
5. **Missing audit trail** - insufficient logging of state transitions
6. **Synchronous operations** - blocks on network calls during callback

### Impact
- Payment failures lead to manual intervention
- Duplicate charges possible on webhook retry
- Poor user experience with failed payment recovery
- Difficult debugging of transaction issues

---

## Phase 1: Architecture Design

### Step 1.1: State Machine Definition

**File**: `mpesa_tx/mpesa_tx/doctype/mpesa_ticket/mpesa_ticket_state_machine.py`

Create a new file for state machine logic:

```python
from enum import Enum
from typing import List, Optional

class TicketStatus(Enum):
    """MPESA Ticket lifecycle states"""
    INITIATED = 'Initiated'
    AWAITING_PIN = 'Awaiting Pin'
    CALLBACK_RECEIVED = 'Callback Received'
    VERIFIED = 'Verified'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    TIMEOUT = 'Timeout'

class StateTransition:
    """Defines valid state transitions"""

    VALID_TRANSITIONS = {
        TicketStatus.INITIATED: [
            TicketStatus.AWAITING_PIN,
            TicketStatus.TIMEOUT
        ],
        TicketStatus.AWAITING_PIN: [
            TicketStatus.CALLBACK_RECEIVED,
            TicketStatus.TIMEOUT
        ],
        TicketStatus.CALLBACK_RECEIVED: [
            TicketStatus.VERIFIED,
            TicketStatus.FAILED
        ],
        TicketStatus.VERIFIED: [
            TicketStatus.COMPLETED,
            TicketStatus.FAILED
        ],
        # Terminal states - no further transitions
        TicketStatus.COMPLETED: [],
        TicketStatus.FAILED: [],
        TicketStatus.TIMEOUT: []
    }

    @staticmethod
    def is_valid(current: TicketStatus, next_state: TicketStatus) -> bool:
        """Check if transition is valid"""
        valid_next_states = StateTransition.VALID_TRANSITIONS.get(current, [])
        return next_state in valid_next_states

    @staticmethod
    def get_valid_next_states(current: TicketStatus) -> List[TicketStatus]:
        """Get list of valid next states"""
        return StateTransition.VALID_TRANSITIONS.get(current, [])

    @staticmethod
    def is_terminal(status: TicketStatus) -> bool:
        """Check if status is terminal (no further transitions)"""
        return status in [
            TicketStatus.COMPLETED,
            TicketStatus.FAILED,
            TicketStatus.TIMEOUT
        ]
```

### Step 1.2: Callback Handler Class

**File**: `mpesa_tx/api/callback_handler.py`

Create idempotent webhook handler:

```python
import frappe
import json
from datetime import datetime
from frappe.utils import get_datetime, now_datetime
from mpesa_tx.mpesa_tx.doctype.mpesa_ticket.mpesa_ticket_state_machine import (
    TicketStatus,
    StateTransition
)

class MPESACallbackHandler:
    """
    Idempotent webhook handler for M-Pesa STK callbacks.

    Design Principles:
    1. Idempotent: Safe to call multiple times with same payload
    2. Async-first: Queues verification job instead of blocking
    3. Resilient: Handles missing tickets gracefully
    4. Audited: Logs all transitions with timestamps
    """

    def __init__(self, payload: dict):
        """Initialize handler with M-Pesa callback payload"""
        self.payload = payload
        self.body = payload.get('Body', {}).get('stkCallback', {})

        # Extract M-Pesa fields
        self.checkout_request_id = self.body.get('CheckoutRequestID', '')
        self.result_code = self.body.get('ResultCode')
        self.result_desc = self.body.get('ResultDesc', '')

        # Extract callback metadata
        callback_metadata = self.body.get('CallbackMetadata', {}).get('Item', [])
        self.callback_items = {item.get('Name'): item.get('Value') for item in callback_metadata}

        self.receipt_number = self.callback_items.get('ReceiptNumber', '')
        self.amount = self.callback_items.get('Amount', 0)
        self.phone_number = self.callback_items.get('PhoneNumber', '')
        self.merchant_request_id = self.body.get('MerchantRequestID', '')

        # Timestamp callback reception
        self.callback_received_at = now_datetime()

    def handle(self) -> dict:
        """
        Main handler - entry point for webhook processing.

        Returns: {success: bool, message: str, ticket_id?: str, error?: str}
        """
        try:
            # Step 1: Find the MPESA Ticket
            ticket = self._get_or_create_ticket()

            # Step 2: Idempotency check - if already processed, return success
            if StateTransition.is_terminal(TicketStatus[ticket.ticket_status.upper()]):
                frappe.logger().info(
                    f"Callback already processed for ticket {ticket.name}. Ignoring duplicate."
                )
                return {
                    'success': True,
                    'message': f'Callback already processed for {ticket.name}',
                    'ticket_id': ticket.name
                }

            # Step 3: Process based on result code
            if self.result_code == 0:  # Success
                return self._handle_successful_callback(ticket)
            else:  # User cancelled or timeout
                return self._handle_failed_callback(ticket)

        except Exception as e:
            frappe.logger().error(f"Fatal error in callback handling: {str(e)}")
            # Re-raise - Frappe will retry webhook
            raise

    def _get_or_create_ticket(self) -> 'MPESATicket':
        """
        Find existing MPESA Ticket or create placeholder.
        Handles case where callback arrives before STK push is queued.
        """
        try:
            ticket = frappe.get_doc('MPESA Ticket', self.checkout_request_id)
            frappe.logger().debug(f"Found existing ticket: {ticket.name}")
            return ticket

        except frappe.DoesNotExistError:
            # Callback arrived before ticket creation (rare)
            frappe.logger().warning(
                f"Callback received for unknown ticket {self.checkout_request_id}. "
                f"Creating placeholder."
            )

            ticket = frappe.new_doc('MPESA Ticket')
            ticket.name = self.checkout_request_id
            ticket.ticket_status = 'Awaiting Pin'
            ticket.msisdn = self.phone_number
            ticket.amount = self.amount
            # Don't save - let caller save after processing

            return ticket

    def _handle_successful_callback(self, ticket: 'MPESATicket') -> dict:
        """
        Process successful STK callback.

        Flow:
        1. Create MPESA Payload with callback data
        2. Update ticket status to CALLBACK_RECEIVED
        3. Enqueue async verification job
        4. Return immediately (non-blocking)
        """
        try:
            # Create MPESA Payload to record the callback
            mpesa_payload = frappe.new_doc('MPESA Payload')
            mpesa_payload.account_number = ticket.name
            mpesa_payload.phone = self.phone_number
            mpesa_payload.amount = self.amount
            mpesa_payload.transaction_reference = self.receipt_number
            mpesa_payload.merchant_request_id = self.merchant_request_id
            mpesa_payload.json_dump = frappe.as_json(self.payload)
            mpesa_payload.is_processed = False
            mpesa_payload.retry_count = 0
            mpesa_payload.insert()

            # Update ticket status
            self._transition_ticket_status(
                ticket,
                TicketStatus.CALLBACK_RECEIVED,
                f'Callback received. Receipt: {self.receipt_number}'
            )

            # Enqueue verification job (async)
            frappe.enqueue(
                'mpesa_tx.api.callback_handler.verify_and_process_payment',
                ticket_id=ticket.name,
                payload_id=mpesa_payload.name,
                job_name=f'mpesa_verify_{ticket.name}',
                timeout=120,
                retries=0  # Handled by fallback job
            )

            frappe.logger().info(
                f"Callback handled successfully for ticket {ticket.name}. "
                f"Verification queued."
            )

            return {
                'success': True,
                'message': 'Callback received and queued for verification',
                'ticket_id': ticket.name
            }

        except Exception as e:
            frappe.logger().error(f"Error handling successful callback: {str(e)}")
            # Still return success to acknowledge webhook reception
            return {
                'success': True,
                'message': 'Callback received (processing deferred)',
                'ticket_id': ticket.name
            }

    def _handle_failed_callback(self, ticket: 'MPESATicket') -> dict:
        """
        Process failed or cancelled STK request.

        User either:
        - Cancelled the STK prompt
        - Request timed out
        - Enter wrong PIN multiple times
        """
        try:
            # Update ticket status
            reason = self._get_failure_reason()
            self._transition_ticket_status(
                ticket,
                TicketStatus.FAILED,
                f'User action: {reason}'
            )

            # Enqueue notification job
            frappe.enqueue(
                'mpesa_tx.tasks.notify_payment_failed',
                ticket_id=ticket.name,
                reason=reason,
                job_name=f'mpesa_notify_failed_{ticket.name}'
            )

            frappe.logger().warning(
                f"Payment failed for ticket {ticket.name}. Reason: {reason}"
            )

            return {
                'success': True,
                'message': f'Payment failed: {reason}',
                'ticket_id': ticket.name
            }

        except Exception as e:
            frappe.logger().error(f"Error handling failed callback: {str(e)}")
            return {
                'success': True,
                'message': 'Failure notification queued',
                'ticket_id': ticket.name
            }

    def _transition_ticket_status(
        self,
        ticket: 'MPESATicket',
        new_status: TicketStatus,
        reason: str = ''
    ):
        """
        Safely transition ticket status with audit logging.

        Validates transition, updates ticket, logs change.
        """
        old_status = TicketStatus[ticket.ticket_status.upper()]

        # Validate transition
        if not StateTransition.is_valid(old_status, new_status):
            frappe.throw(
                f'Invalid state transition: {old_status.value} → {new_status.value}',
                exc=frappe.ValidationError
            )

        # Update status
        ticket.ticket_status = new_status.value
        ticket.save()

        # Audit log
        timestamp = now_datetime().isoformat()
        ticket.add_comment(
            'Comment',
            f'[{timestamp}] Status: {old_status.value} → {new_status.value}\n'
            f'Reason: {reason}',
            comment_type='Info'
        )

        frappe.logger().info(
            f"Ticket {ticket.name}: {old_status.value} → {new_status.value}"
        )

    def _get_failure_reason(self) -> str:
        """Map M-Pesa result code to user-friendly message"""
        reasons = {
            1: 'User cancelled the transaction',
            2: 'Request timeout',
            17: 'Transaction timeout',
        }
        return reasons.get(self.result_code, 'Payment declined by M-Pesa')


def verify_and_process_payment(ticket_id: str, payload_id: str):
    """
    Background job: Verify callback with M-Pesa API, then process payment.

    This is the critical step that prevents processing unverified payments.

    Flow:
    1. Query M-Pesa API for transaction status
    2. If valid, create Payment Entry and settle charges
    3. If invalid, mark ticket as FAILED
    4. Audit all state changes
    """
    try:
        # Load documents
        ticket = frappe.get_doc('MPESA Ticket', ticket_id)
        payload = frappe.get_doc('MPESA Payload', payload_id)

        # Step 1: Verify with M-Pesa
        is_valid = _verify_transaction_with_mpesa(ticket)

        if not is_valid:
            # Transaction not confirmed by M-Pesa - reject it
            ticket.ticket_status = TicketStatus.FAILED.value
            ticket.add_comment(
                'Comment',
                'Callback verification failed - transaction not found in M-Pesa API',
                comment_type='Alert'
            )
            ticket.save()

            frappe.logger().warning(
                f"Callback verification failed for {ticket_id}. "
                f"Transaction not found in M-Pesa."
            )
            return

        # Step 2: Process payment
        try:
            # This creates Payment Entry, links to customer, submits charges
            payload.process_payment()

            # Step 3: Mark as completed
            ticket.ticket_status = TicketStatus.COMPLETED.value
            ticket.add_comment(
                'Comment',
                f'Payment verified and processed. Payment Entry created.',
                comment_type='Success'
            )
            ticket.save()

            frappe.logger().info(f"Payment verified and processed for {ticket_id}")

        except Exception as process_error:
            # Payment processing failed - mark as failed
            ticket.ticket_status = TicketStatus.FAILED.value
            ticket.add_comment(
                'Comment',
                f'Payment processing failed: {str(process_error)}',
                comment_type='Alert'
            )
            ticket.save()

            frappe.logger().error(
                f"Payment processing failed for {ticket_id}: {str(process_error)}"
            )
            # Don't re-raise - allow fallback job to retry

    except Exception as e:
        frappe.logger().error(
            f"Fatal error in verify_and_process_payment for {ticket_id}: {str(e)}"
        )
        raise  # Re-raise to fail the job and trigger retries


def _verify_transaction_with_mpesa(ticket: 'MPESATicket') -> bool:
    """
    Query M-Pesa API to verify transaction actually occurred.

    Returns: True if transaction found and matches expected amount/phone
    """
    from mpesa_tx.api.mpesa_handler import MPESAHandler

    handler = MPESAHandler()

    try:
        # Query M-Pesa for transaction status
        is_valid = handler.get_stk_transaction_status(ticket)

        if not is_valid:
            frappe.logger().warning(
                f"Transaction {ticket.name} not found in M-Pesa API"
            )
            return False

        frappe.logger().debug(f"Transaction {ticket.name} verified with M-Pesa API")
        return True

    except Exception as e:
        frappe.logger().error(f"Error verifying transaction with M-Pesa: {str(e)}")
        # On API error, fail conservatively (don't process unverified payment)
        return False


@frappe.whitelist(allow_guest=True)  # M-Pesa cannot authenticate as Frappe user
def handle_mpesa_callback():
    """
    Frappe endpoint for M-Pesa webhooks.

    Route: POST /api/method/mpesa_tx.api.callback_handler.handle_mpesa_callback
    Called by M-Pesa's callback system
    """
    from flask import request

    try:
        # Parse callback payload
        payload = request.get_json() or {}

        # Validate signature (if required)
        # _validate_mpesa_signature(payload, request.headers)

        # Handle callback
        handler = MPESACallbackHandler(payload)
        result = handler.handle()

        # Return M-Pesa-compatible response
        return {
            'ResultCode': 0 if result['success'] else 1,
            'ResultDesc': result['message']
        }

    except Exception as e:
        frappe.logger().error(f"Webhook handler error: {str(e)}")
        # Still return 0 to prevent M-Pesa retries
        return {
            'ResultCode': 0,
            'ResultDesc': 'Notification received'
        }
```

---

## Phase 2: Background Job Infrastructure

### Step 2.1: Retry Job Configuration

**File**: `mpesa_tx/hooks.py`

Update hooks to add background jobs:

```python
# Existing hooks
app_name = "mpesa_tx"
app_title = "M-Pesa Payment Integration"
# ... other hooks ...

# Add webhook configuration
webhooks = {
    "mpesa_tx.api.callback_handler.handle_mpesa_callback": {
        "on_request": "mpesa_tx.api.callback_handler.handle_mpesa_callback"
    }
}

# Add background jobs for processing
background_jobs = {
    'mpesa_tx.tasks.process_pending_callbacks': {
        'method': 'mpesa_tx.tasks.process_pending_callbacks',
        'cron': '*/15 * * * *',  # Every 15 minutes
        'timeout': 600
    },
    'mpesa_tx.tasks.timeout_pending_tickets': {
        'method': 'mpesa_tx.tasks.timeout_pending_tickets',
        'cron': '0 * * * *',  # Hourly
        'timeout': 300
    },
    'mpesa_tx.tasks.cleanup_old_tickets': {
        'method': 'mpesa_tx.tasks.cleanup_old_tickets',
        'cron': '0 2 * * *',  # Daily at 2 AM
        'timeout': 600
    }
}

# Add scheduled jobs
scheduled_jobs = [
    {
        'method': 'mpesa_tx.tasks.process_pending_callbacks',
        'cron': '*/15 * * * *'
    },
    {
        'method': 'mpesa_tx.tasks.timeout_pending_tickets',
        'cron': '0 * * * *'
    }
]
```

### Step 2.2: Task Module for Background Jobs

**File**: `mpesa_tx/tasks.py`

Create comprehensive background job handlers:

```python
import frappe
from frappe.utils import add_days, now_datetime, get_datetime
from datetime import timedelta
from mpesa_tx.mpesa_tx.doctype.mpesa_ticket.mpesa_ticket_state_machine import TicketStatus

def process_pending_callbacks():
    """
    Periodically reprocess callbacks that failed initial handling.

    Called every 15 minutes to handle transient failures.
    Uses exponential backoff for retry attempts.
    """
    try:
        # Find unprocessed payloads with retry attempts remaining
        failed_payloads = frappe.get_list(
            'MPESA Payload',
            filters=[
                ['is_processed', '=', False],
                ['retry_count', '<', 5]
            ],
            fields=['name', 'retry_count', 'modified'],
            order_by='creation asc',
            limit=50
        )

        for payload_record in failed_payloads:
            payload = frappe.get_doc('MPESA Payload', payload_record.name)

            # Check if enough time elapsed for retry (exponential backoff)
            if not _should_retry(payload_record):
                continue

            try:
                # Attempt to process payment
                payload.process_payment()

                payload.is_processed = True
                payload.save()

                frappe.logger().info(
                    f"Successfully processed payload {payload.name} "
                    f"on attempt {payload.retry_count + 1}"
                )

            except Exception as e:
                # Increment retry counter
                payload.retry_count = (payload.retry_count or 0) + 1
                payload.last_error = str(e)
                payload.last_retry_at = now_datetime()
                payload.save()

                frappe.logger().warning(
                    f"Payload {payload.name} retry {payload.retry_count} failed: {str(e)}"
                )

    except Exception as e:
        frappe.logger().error(f"Error in process_pending_callbacks: {str(e)}")


def timeout_pending_tickets():
    """
    Mark tickets as TIMEOUT if no callback received within 30 minutes.

    Called hourly to clean up stale STK push requests.
    """
    try:
        # Find tickets awaiting PIN for >30 minutes
        thirty_mins_ago = get_datetime() - timedelta(minutes=30)

        stale_tickets = frappe.get_list(
            'MPESA Ticket',
            filters=[
                ['ticket_status', '=', 'Awaiting Pin'],
                ['creation', '<', thirty_mins_ago]
            ],
            fields=['name', 'msisdn', 'customer_email'],
            limit=100
        )

        for ticket_record in stale_tickets:
            ticket = frappe.get_doc('MPESA Ticket', ticket_record.name)

            # Update status to TIMEOUT
            ticket.ticket_status = TicketStatus.TIMEOUT.value
            ticket.add_comment(
                'Comment',
                'No callback received within 30 minutes. Marked as timeout.',
                comment_type='Alert'
            )
            ticket.save()

            # Notify customer
            frappe.enqueue(
                'mpesa_tx.tasks.notify_payment_timeout',
                ticket_id=ticket.name,
                customer_email=ticket_record.get('customer_email'),
                job_name=f'mpesa_notify_timeout_{ticket.name}'
            )

            frappe.logger().warning(f"Ticket {ticket.name} marked as TIMEOUT")

    except Exception as e:
        frappe.logger().error(f"Error in timeout_pending_tickets: {str(e)}")


def cleanup_old_tickets():
    """
    Archive/delete old completed tickets (>90 days).

    Keeps database clean while maintaining audit trail.
    """
    try:
        ninety_days_ago = get_datetime() - timedelta(days=90)

        old_tickets = frappe.get_list(
            'MPESA Ticket',
            filters=[
                ['ticket_status', 'in', ['Completed', 'Failed', 'Timeout']],
                ['creation', '<', ninety_days_ago]
            ],
            fields=['name'],
            limit=500
        )

        for ticket_record in old_tickets:
            ticket = frappe.get_doc('MPESA Ticket', ticket_record.name)
            ticket.delete()

        frappe.logger().info(f"Cleaned up {len(old_tickets)} old tickets")

    except Exception as e:
        frappe.logger().error(f"Error in cleanup_old_tickets: {str(e)}")


def notify_payment_timeout(ticket_id: str, customer_email: str):
    """Send notification to customer about payment timeout"""
    try:
        ticket = frappe.get_doc('MPESA Ticket', ticket_id)

        frappe.sendmail(
            recipients=[customer_email],
            subject='M-Pesa Payment Request Expired',
            template='mpesa_timeout_notification',
            args={
                'ticket_id': ticket_id,
                'amount': ticket.amount,
                'phone': ticket.msisdn
            }
        )

        frappe.logger().info(f"Timeout notification sent for {ticket_id}")

    except Exception as e:
        frappe.logger().error(
            f"Error sending timeout notification for {ticket_id}: {str(e)}"
        )


def notify_payment_failed(ticket_id: str, reason: str):
    """Send notification to customer about payment failure"""
    try:
        ticket = frappe.get_doc('MPESA Ticket', ticket_id)

        frappe.sendmail(
            recipients=[ticket.customer_email],
            subject='M-Pesa Payment Failed',
            template='mpesa_failure_notification',
            args={
                'ticket_id': ticket_id,
                'reason': reason,
                'amount': ticket.amount
            }
        )

    except Exception as e:
        frappe.logger().error(f"Error notifying payment failure for {ticket_id}: {str(e)}")


def _should_retry(payload_record: dict) -> bool:
    """
    Determine if payload should be retried based on exponential backoff.

    Retry delays: 1 min, 5 min, 15 min, 1 hour, 2 hours
    """
    retry_delays = [60, 300, 900, 3600, 7200]  # seconds
    retry_count = payload_record.get('retry_count', 0)

    if retry_count >= len(retry_delays):
        return False

    required_delay = retry_delays[retry_count]
    time_since_last_retry = (
        now_datetime() - payload_record.get('last_retry_at', payload_record['modified'])
    ).total_seconds()

    return time_since_last_retry >= required_delay
```

---

## Phase 3: Enhanced MPESA Ticket DocType

### Step 3.1: Update MPESA Ticket Fields

**File**: `mpesa_tx/mpesa_tx/doctype/mpesa_ticket/mpesa_ticket.py`

```python
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from mpesa_tx.mpesa_tx.doctype.mpesa_ticket.mpesa_ticket_state_machine import (
    TicketStatus,
    StateTransition
)

class MPESATicket(Document):
    """
    MPESA Ticket represents a pending or completed payment request.

    State Machine:
    INITIATED → AWAITING_PIN → CALLBACK_RECEIVED → VERIFIED → COMPLETED
                                         ↓
                                      FAILED
                                         ↑
                        AWAITING_PIN → TIMEOUT
    """

    def before_save(self):
        """Validate state transitions and log changes"""
        # Validate status transition
        if self.has_value_changed('ticket_status'):
            self._validate_status_transition()
            self._log_status_change()

        # Update timestamp for state change
        if self.has_value_changed('ticket_status'):
            self.status_changed_at = now_datetime()

    def _validate_status_transition(self):
        """Prevent invalid state transitions"""
        old_status_str = self.db_get('ticket_status') or 'Initiated'
        new_status_str = self.ticket_status

        try:
            old_status = TicketStatus[old_status_str.upper()]
            new_status = TicketStatus[new_status_str.upper()]
        except KeyError:
            frappe.throw(f'Invalid status: {new_status_str}')

        if not StateTransition.is_valid(old_status, new_status):
            frappe.throw(
                f'Invalid state transition: {old_status.value} → {new_status.value}',
                exc=frappe.ValidationError
            )

    def _log_status_change(self):
        """Audit trail for state transitions"""
        old_status = self.db_get('ticket_status') or 'Initiated'
        new_status = self.ticket_status

        timestamp = now_datetime().isoformat()
        self.add_comment(
            'Comment',
            f'Status changed [{timestamp}]: {old_status} → {new_status}',
            comment_type='Info'
        )

    def enqueue_payment_initiation(self):
        """Queue STK push as background job"""
        frappe.enqueue(
            'mpesa_tx.api.mpesa_handler.initiate_payment',
            ticket_id=self.name,
            job_name=f'mpesa_initiate_{self.name}',
            timeout=60
        )

        self.ticket_status = TicketStatus.INITIATED.value
        self.save()

        frappe.logger().info(f"STK push queued for ticket {self.name}")

    def get_callback_wait_time(self) -> int:
        """Get seconds elapsed since ticket creation"""
        elapsed = (now_datetime() - self.creation).total_seconds()
        return int(elapsed)

    def has_callback_timeout(self) -> bool:
        """Check if ticket should be considered timeout (30 min)"""
        return self.get_callback_wait_time() > 1800

    def mark_failed(self, reason: str):
        """Safely mark ticket as failed"""
        self.ticket_status = TicketStatus.FAILED.value
        self.add_comment('Comment', f'Failed: {reason}')
        self.save()

    def mark_completed(self):
        """Safely mark ticket as completed"""
        self.ticket_status = TicketStatus.COMPLETED.value
        self.save()
```

### Step 3.2: Update Field Definitions

Add these fields to MPESA Ticket doctype:

```python
# In doctype JSON or via database migrations
new_fields = [
    {
        'fieldname': 'status_changed_at',
        'fieldtype': 'Datetime',
        'label': 'Status Changed At',
        'read_only': 1
    },
    {
        'fieldname': 'callback_received_at',
        'fieldtype': 'Datetime',
        'label': 'Callback Received At',
        'read_only': 1
    },
    {
        'fieldname': 'callback_verified_at',
        'fieldtype': 'Datetime',
        'label': 'Callback Verified At',
        'read_only': 1
    },
    {
        'fieldname': 'retry_count',
        'fieldtype': 'Int',
        'label': 'Retry Count',
        'default': 0,
        'read_only': 1
    },
    {
        'fieldname': 'last_error',
        'fieldtype': 'Text',
        'label': 'Last Error',
        'read_only': 1
    },
    {
        'fieldname': 'stk_response_code',
        'fieldtype': 'Code',
        'fieldtype': 'JSON',
        'label': 'STK Response',
        'read_only': 1
    }
]
```

---

## Phase 4: Frontend Integration

### Step 4.1: Update Payment Store

**File**: `frontend/src/stores/paymentStore.ts`

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface PaymentState {
  status: string
  bookingId: string
  phoneNumber: string
  ticketId: string
  startTime: number
  transactionRef?: string
  receipt?: string
  error?: string
}

export const usePaymentStore = defineStore('payment', () => {
  // State
  const currentPayment = ref<PaymentState | null>(null)
  const paymentHistory = ref<PaymentState[]>([])
  const isPolling = ref(false)
  const pollInterval = ref<NodeJS.Timeout | null>(null)

  const PaymentStatuses = {
    IDLE: 'idle',
    INITIATING: 'initiating',
    STK_SHOWN: 'stk_shown',
    AWAITING_PIN: 'awaiting_pin',
    PROCESSING: 'processing',
    COMPLETED: 'completed',
    FAILED: 'failed',
    TIMEOUT: 'timeout'
  }

  // Actions
  async function initiatePayment(bookingId: string, phoneNumber: string) {
    try {
      currentPayment.value = {
        status: PaymentStatuses.INITIATING,
        bookingId,
        phoneNumber,
        startTime: Date.now(),
        ticketId: ''
      }

      // Call backend API
      const response = await api.call(
        'mpesa_tx.api.mpesa_handler.initiate_stk_transaction',
        {
          booking_id: bookingId,
          msisdn: phoneNumber
        }
      )

      currentPayment.value.ticketId = response.ticket_id
      currentPayment.value.status = PaymentStatuses.STK_SHOWN

      // Start polling for callback
      startPaymentPolling(response.ticket_id)

    } catch (error) {
      if (currentPayment.value) {
        currentPayment.value.status = PaymentStatuses.FAILED
        currentPayment.value.error = error.message
      }
    }
  }

  function startPaymentPolling(ticketId: string) {
    if (isPolling.value) return

    isPolling.value = true
    let pollCount = 0
    const maxPolls = 600  // 30 mins with 3-sec interval = 600 polls

    pollInterval.value = setInterval(async () => {
      pollCount++

      if (pollCount > maxPolls) {
        // Timeout after 30 minutes
        stopPaymentPolling()
        if (currentPayment.value) {
          currentPayment.value.status = PaymentStatuses.TIMEOUT
        }
        return
      }

      try {
        // Poll backend for status
        const response = await api.call(
          'mpesa_tx.api.mpesa_handler.get_stk_status',
          { ticket_id: ticketId }
        )

        updatePaymentStatus(response)

        // Stop on terminal state
        if (isTerminalStatus(response.ticket_status)) {
          stopPaymentPolling()
        }

      } catch (error) {
        console.error('Polling error:', error)
        // Continue polling on error
      }
    }, 3000)  // Poll every 3 seconds
  }

  function stopPaymentPolling() {
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
      pollInterval.value = null
    }
    isPolling.value = false
  }

  function updatePaymentStatus(response: any) {
    if (!currentPayment.value) return

    const statusMap: Record<string, string> = {
      'Initiated': PaymentStatuses.INITIATING,
      'Awaiting Pin': PaymentStatuses.AWAITING_PIN,
      'Callback Received': PaymentStatuses.PROCESSING,
      'Verified': PaymentStatuses.PROCESSING,
      'Completed': PaymentStatuses.COMPLETED,
      'Failed': PaymentStatuses.FAILED,
      'Timeout': PaymentStatuses.TIMEOUT
    }

    currentPayment.value.status = statusMap[response.ticket_status] || PaymentStatuses.IDLE
    currentPayment.value.transactionRef = response.transaction_ref
    currentPayment.value.receipt = response.receipt_number
  }

  function isTerminalStatus(status: string): boolean {
    return ['Completed', 'Failed', 'Timeout'].includes(status)
  }

  function resetPayment() {
    stopPaymentPolling()
    currentPayment.value = null
  }

  // Computed
  const isPaymentInProgress = computed(() =>
    currentPayment.value &&
    ![PaymentStatuses.COMPLETED, PaymentStatuses.FAILED, PaymentStatuses.TIMEOUT]
      .includes(currentPayment.value.status)
  )

  const paymentMessage = computed(() => {
    const messages: Record<string, string> = {
      [PaymentStatuses.INITIATING]: 'Initiating payment...',
      [PaymentStatuses.STK_SHOWN]: 'Payment prompt sent to your phone',
      [PaymentStatuses.AWAITING_PIN]: 'Waiting for PIN entry...',
      [PaymentStatuses.PROCESSING]: 'Verifying payment...',
      [PaymentStatuses.COMPLETED]: 'Payment successful!',
      [PaymentStatuses.FAILED]: 'Payment failed. Please try again.',
      [PaymentStatuses.TIMEOUT]: 'Payment timed out. Please retry.'
    }
    return messages[currentPayment.value?.status] || ''
  })

  return {
    currentPayment,
    paymentHistory,
    paymentStatuses: PaymentStatuses,
    initiatePayment,
    resetPayment,
    isPaymentInProgress,
    paymentMessage
  }
})
```

---

## Security: Signature Verification

### Step 4.2: HMAC Signature Validation

**File**: `mpesa_tx/api/security.py`

```python
import hmac
import hashlib
import json
from typing import Tuple

def verify_mpesa_callback_signature(
    payload: dict,
    signature: str,
    shared_secret: str
) -> bool:
    """
    Verify M-Pesa webhook signature using HMAC-SHA256.

    Prevents spoofed callbacks.

    Args:
        payload: Full callback payload dict
        signature: X-MPESA-Signature header value
        shared_secret: Shared secret from M-Pesa

    Returns:
        True if signature is valid
    """
    # Convert payload to JSON string (must match M-Pesa's format)
    payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)

    # Calculate expected signature
    expected_sig = hmac.new(
        shared_secret.encode('utf-8'),
        payload_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_sig.lower(), signature.lower())


def validate_callback_signature(flask_request) -> Tuple[bool, str]:
    """
    Middleware to validate callback signature.

    Returns: (is_valid, error_message)
    """
    try:
        # Get signature from header
        signature = flask_request.headers.get('X-MPESA-Signature')
        if not signature:
            return False, 'Missing X-MPESA-Signature header'

        # Get payload
        payload = flask_request.get_json() or {}

        # Get shared secret from settings
        settings = frappe.get_doc('MPESA Settings', 'MPESA Settings')
        shared_secret = settings.callback_secret

        if not shared_secret:
            frappe.logger().error('MPESA callback secret not configured')
            return False, 'Server misconfiguration'

        # Verify signature
        is_valid = verify_mpesa_callback_signature(payload, signature, shared_secret)

        if not is_valid:
            frappe.logger().warning(
                f'Invalid callback signature. Expected: {signature}'
            )
            return False, 'Invalid signature'

        return True, ''

    except Exception as e:
        frappe.logger().error(f'Signature validation error: {str(e)}')
        return False, 'Validation error'
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_callback_handler.py

def test_callback_idempotency():
    """Test that duplicate callbacks don't cause duplicate charges"""
    payload = {...}
    handler1 = MPESACallbackHandler(payload)
    handler2 = MPESACallbackHandler(payload)

    result1 = handler1.handle()
    result2 = handler2.handle()

    # Both should succeed
    assert result1['success'] and result2['success']

    # But only one Payment Entry should exist
    payment_entries = frappe.get_list('Payment Entry', {...})
    assert len(payment_entries) == 1


def test_state_machine_validation():
    """Test that invalid transitions are rejected"""
    ticket = frappe.get_doc('MPESA Ticket', {'name': 'TEST-001'})
    ticket.ticket_status = 'Completed'
    ticket.save()

    # Try invalid transition
    ticket.ticket_status = 'Awaiting Pin'
    with pytest.raises(frappe.ValidationError):
        ticket.save()
```

### Integration Tests

```python
def test_full_payment_flow():
    """Test complete flow: STK → Callback → Verification → Payment"""
    # 1. Initiate payment
    # 2. Simulate callback
    # 3. Verify async job completes
    # 4. Check Payment Entry created
    # 5. Check Booking status updated
```

---

## Deployment Checklist

- [ ] Database migrations for new fields
- [ ] Background job configuration in Frappe
- [ ] MPESA Settings configured with callback secret
- [ ] Webhook endpoint registered with M-Pesa
- [ ] Email templates created (timeout, failure notifications)
- [ ] Monitoring/alerts configured for failed callbacks
- [ ] Rollback procedure documented
- [ ] Load testing with simulated callbacks
- [ ] Audit logs enabled for all transactions

