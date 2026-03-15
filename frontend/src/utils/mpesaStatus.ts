export type MpesaLifecycleStatus =
  | 'Requested'
  | 'Pending'
  | 'Prompt Sent'
  | 'Callback Received'
  | 'Paid'
  | 'Partially Paid'
  | 'Completed'
  | 'Failed'
  | 'Cancelled'
  | 'Timeout'

type MpesaStatusTone = 'info' | 'success' | 'warning' | 'error'

export interface MpesaProgressModel {
  status: MpesaLifecycleStatus
  title: string
  detail: string
  progress: number
  tone: MpesaStatusTone
  isTerminal: boolean
  isSuccess: boolean
  isFailure: boolean
}

const FALLBACK_DETAIL = 'Keep your phone nearby to approve the MPESA prompt.'

const STATUS_CONFIG: Record<
  MpesaLifecycleStatus,
  { title: string; detail: string; progress: number; tone: MpesaStatusTone; terminal: boolean }
> = {
  Requested: {
    title: 'Ticket created',
    detail: 'The MPESA ticket is ready and the STK request is being queued.',
    progress: 18,
    tone: 'info',
    terminal: false,
  },
  Pending: {
    title: 'Preparing payment',
    detail: 'We are preparing the MPESA request.',
    progress: 12,
    tone: 'info',
    terminal: false,
  },
  'Prompt Sent': {
    title: 'Prompt sent',
    detail: FALLBACK_DETAIL,
    progress: 38,
    tone: 'info',
    terminal: false,
  },
  'Callback Received': {
    title: 'Callback received',
    detail: 'We received a response from MPESA and are validating it.',
    progress: 72,
    tone: 'info',
    terminal: false,
  },
  Paid: {
    title: 'Payment confirmed',
    detail: 'Your payment was received successfully.',
    progress: 100,
    tone: 'success',
    terminal: true,
  },
  'Partially Paid': {
    title: 'Deposit confirmed',
    detail: 'The required installment was received successfully.',
    progress: 100,
    tone: 'success',
    terminal: true,
  },
  Completed: {
    title: 'Payment completed',
    detail: 'The transaction completed successfully.',
    progress: 100,
    tone: 'success',
    terminal: true,
  },
  Failed: {
    title: 'Payment failed',
    detail: 'The transaction did not complete. You can retry the payment.',
    progress: 100,
    tone: 'error',
    terminal: true,
  },
  Cancelled: {
    title: 'Payment cancelled',
    detail: 'The MPESA prompt was cancelled before completion.',
    progress: 100,
    tone: 'warning',
    terminal: true,
  },
  Timeout: {
    title: 'Payment timed out',
    detail: 'No callback was received within the expected time window.',
    progress: 100,
    tone: 'warning',
    terminal: true,
  },
}

const TICKET_STATUS_MAP: Record<string, MpesaLifecycleStatus> = {
  Requested: 'Requested',
  Completed: 'Completed',
  Failed: 'Failed',
}

const KNOWN_STATUSES = new Set<MpesaLifecycleStatus>(Object.keys(STATUS_CONFIG) as MpesaLifecycleStatus[])

const toKnownStatus = (status: string | null | undefined): MpesaLifecycleStatus | null => {
  if (!status) {
    return null
  }
  const normalized = String(status).trim()
  if (!normalized) {
    return null
  }
  return (KNOWN_STATUSES.has(normalized as MpesaLifecycleStatus) ? normalized : null) as MpesaLifecycleStatus | null
}

export const resolveMpesaLifecycleStatus = (args: {
  paymentStatus?: string | null
  ticketStatus?: string | null
  fallbackStatus?: string | null
}): MpesaLifecycleStatus => {
  const fromPayment = toKnownStatus(args.paymentStatus)
  if (fromPayment) {
    return fromPayment
  }

  const mappedTicket = args.ticketStatus ? TICKET_STATUS_MAP[String(args.ticketStatus).trim()] : null
  if (mappedTicket) {
    return mappedTicket
  }

  const fromFallback = toKnownStatus(args.fallbackStatus)
  if (fromFallback) {
    return fromFallback
  }

  return 'Pending'
}

export const getMpesaProgressModel = (args: {
  paymentStatus?: string | null
  ticketStatus?: string | null
  fallbackStatus?: string | null
  message?: string | null
}): MpesaProgressModel => {
  const status = resolveMpesaLifecycleStatus({
    paymentStatus: args.paymentStatus,
    ticketStatus: args.ticketStatus,
    fallbackStatus: args.fallbackStatus,
  })
  const config = STATUS_CONFIG[status]
  const detail = String(args.message || '').trim() || config.detail
  return {
    status,
    title: config.title,
    detail,
    progress: config.progress,
    tone: config.tone,
    isTerminal: config.terminal,
    isSuccess: config.tone === 'success',
    isFailure: config.tone === 'error' || config.tone === 'warning',
  }
}
