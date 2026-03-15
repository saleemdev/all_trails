<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-[9999] overflow-y-auto bg-slate-950/55 backdrop-blur-[2px]">
      <div class="flex min-h-dvh items-start justify-center px-4 pb-6 pt-4 sm:items-center sm:px-6 sm:pt-8">
        <section
          class="w-full max-w-2xl overflow-hidden rounded-[1.25rem] border border-white/20 bg-[color:var(--color-surface-strong)] shadow-[var(--shadow-xl)]"
          role="status"
          aria-live="polite"
        >
          <div class="bg-gradient-to-r from-[rgba(49,83,72,0.14)] via-[rgba(184,140,98,0.12)] to-[rgba(49,83,72,0.1)] px-6 py-5 sm:px-8">
            <span class="inline-flex items-center gap-2 rounded-full border border-[color:var(--color-border-soft)] bg-white/70 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.12em] text-[color:var(--color-text-tertiary)]">
              <span class="relative flex h-2 w-2">
                <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-500/60" />
                <span class="relative inline-flex h-2 w-2 rounded-full bg-amber-500" />
              </span>
              Maintenance window
            </span>
            <h2 class="mt-3 text-[clamp(1.35rem,2.6vw,2.1rem)] font-semibold leading-[1.08] tone-heading">
              Shop is temporarily under maintenance
            </h2>
            <p class="mt-2 text-sm leading-6 tone-body">
              We are polishing the merchandising experience and payment flow. The section will be back shortly.
            </p>
          </div>

          <div class="px-6 pb-6 pt-5 sm:px-8 sm:pb-8">
            <div class="grid gap-4 md:grid-cols-[1.05fr_0.95fr] md:items-center">
              <div class="rounded-[1rem] border border-[color:var(--color-border-soft)] bg-white/70 p-4 sm:p-5">
                <div class="mb-3 flex items-center gap-1.5">
                  <span class="h-2.5 w-2.5 rounded-full bg-rose-400/75" />
                  <span class="h-2.5 w-2.5 rounded-full bg-amber-400/80" />
                  <span class="h-2.5 w-2.5 rounded-full bg-emerald-400/80" />
                </div>

                <div class="rounded-[0.9rem] border border-[color:var(--color-border-soft)] bg-[color:var(--color-surface)] p-4">
                  <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[rgba(217,149,76,0.14)] text-[color:var(--color-accent-dark)] ring-1 ring-[rgba(217,149,76,0.36)]">
                    <svg class="h-7 w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path d="M10.5 7.5 6 12l6 6 4.5-4.5-6-6Z" />
                      <path d="m14 4 6 6" />
                      <path d="m17 1 6 6" />
                      <path d="m3 21 6-6" />
                    </svg>
                  </div>
                  <p class="mt-3 text-center text-[13px] font-medium tone-heading">Page under maintenance</p>
                  <div class="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-200/85">
                    <span class="block h-full w-2/3 animate-pulse rounded-full bg-[color:var(--color-primary)]/70" />
                  </div>
                </div>
              </div>

              <ul class="space-y-2.5 text-[13px] leading-5 tone-body">
                <li class="flex items-start gap-2">
                  <span class="mt-1.5 h-2 w-2 rounded-full bg-[color:var(--color-primary-light)]" aria-hidden="true" />
                  <span>Checkout and payment reliability improvements are in progress.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="mt-1.5 h-2 w-2 rounded-full bg-[color:var(--color-primary-light)]" aria-hidden="true" />
                  <span>Your trails, bookings, and profile sections remain fully available.</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="mt-1.5 h-2 w-2 rounded-full bg-[color:var(--color-primary-light)]" aria-hidden="true" />
                  <span>We will reopen this section once end-to-end checks are complete.</span>
                </li>
              </ul>
            </div>

            <div class="mt-5 flex flex-wrap gap-2.5">
              <RouterLink
                to="/trails"
                class="inline-flex items-center rounded-[0.82rem] border border-[color:var(--color-border-soft)] bg-[color:var(--color-surface-control)] px-4 py-2 text-[13px] font-medium tone-heading transition-colors hover:bg-[color:var(--color-surface-control-hover)]"
              >
                Browse trails
              </RouterLink>
              <RouterLink
                to="/"
                class="inline-flex items-center rounded-[0.82rem] border border-[color:var(--color-border-soft)] bg-white/55 px-4 py-2 text-[13px] font-medium tone-heading transition-colors hover:bg-white/75"
              >
                Back home
              </RouterLink>
            </div>
          </div>
        </section>
      </div>
    </div>
  </Teleport>
</template>
