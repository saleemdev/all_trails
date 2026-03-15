export const normalizeKenyanMpesaPhone = (input: string): string => {
  const digits = String(input || '').replace(/\D/g, '');

  if (digits.length === 10 && digits.startsWith('0')) {
    return `254${digits.slice(1)}`;
  }

  if (digits.length === 9 && digits.startsWith('7')) {
    return `254${digits}`;
  }

  if (digits.length === 12 && digits.startsWith('254')) {
    return digits;
  }

  return digits;
};

export const isValidKenyanMpesaPhone = (input: string): boolean => {
  return /^254\d{9}$/.test(normalizeKenyanMpesaPhone(input));
};

export const maskKenyanPhone = (input: string): string => {
  const normalized = normalizeKenyanMpesaPhone(input);
  if (normalized.length < 4) {
    return normalized;
  }

  return `${'*'.repeat(normalized.length - 4)}${normalized.slice(-4)}`;
};
