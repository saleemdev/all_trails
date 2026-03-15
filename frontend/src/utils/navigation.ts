const DEFAULT_APP_REDIRECT = '/';

const ALLOWED_APP_PREFIXES = [
  '/',
  '/trails',
  '/bookings',
  '/profile',
  '/blog',
  '/gallery',
  '/login',
];

const BLOCKED_PROTOCOLS = /^(https?:|\/\/|javascript:|data:|vbscript:)/i;

export const sanitizeAppRedirectPath = (
  rawPath: unknown,
  fallback: string = DEFAULT_APP_REDIRECT
): string => {
  if (typeof rawPath !== 'string' || !rawPath.trim()) {
    return fallback;
  }

  let value = rawPath.trim();
  try {
    value = decodeURIComponent(value);
  } catch {
    // Keep original value if decode fails.
  }

  if (BLOCKED_PROTOCOLS.test(value)) {
    return fallback;
  }

  if (!value.startsWith('/')) {
    value = `/${value.replace(/^\/+/, '')}`;
  }

  // Accept both `/all-trails/...` and app-internal `/...` paths.
  if (value.startsWith('/all-trails')) {
    value = value.slice('/all-trails'.length) || '/';
    if (!value.startsWith('/')) {
      value = `/${value}`;
    }
  }

  if (!ALLOWED_APP_PREFIXES.some(prefix => value === prefix || value.startsWith(`${prefix}/`))) {
    return fallback;
  }

  return value;
};

export const isSafeAuthUrl = (authUrl: unknown): authUrl is string => {
  if (typeof authUrl !== 'string') {
    return false;
  }

  const value = authUrl.trim();
  if (!value) {
    return false;
  }

  if (/^(javascript:|data:|vbscript:)/i.test(value)) {
    return false;
  }

  // OAuth providers can be external or local.
  return value.startsWith('/') || /^https?:\/\//i.test(value);
};
