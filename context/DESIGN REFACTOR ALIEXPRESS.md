Refactor the existing sign-up page component only. Do not touch any 
other page, route, or auth logic. Visual and interaction refactor only —
no changes to form submission, validation logic, API calls, or routing.

You are refactoring toward a crisp, sequential, progressive sign-up flow.
Not a wall of fields. Not a multi-page wizard with back-ends and progress 
bars. A single card that reveals one meaningful step at a time — each 
step earning the next.

Reference aesthetic: Google account creation, Apple ID setup, 
Shopee onboarding. The user never feels the form's full length.

## The Core Interaction Model: 3-Step Progressive Reveal

Step 1 — Identity
  Fields:   Full name (single field, not split first/last)
  CTA:      "Continue"
  Subtext:  "Create your account"

Step 2 — Credentials  
  Fields:   Email or phone (single field)
            Password (below email, revealed after email is filled)
  CTA:      "Continue"
  Subtext:  "Hi [name from Step 1] — set up your login details"
  ← Name from Step 1 appears in subheading. Personal. Not generic.

Step 3 — Verification / Confirmation
  Fields:   OTP / verification code (if applicable to your auth flow)
            OR a single "Confirm password" field if OTP not in scope
  CTA:      "Create account"
  Subtext:  "Almost there — just confirm and you're in"

If OTP is not in the codebase, Step 3 becomes confirm password only.
Do not add OTP infrastructure if it does not already exist.

Step transition mechanics — identical to sign-in refactor:
  Exit:   translateX(-24px) + opacity 0, 200ms ease-accelerate
  Enter:  translateX(24px) → 0 + opacity 0 → 1, 
          260ms ease-decelerate, 60ms delay
  Auto-focus incoming field on transition
  Inactive step: visibility hidden + pointer-events none
  Active step:   absolute positioned, full width of card

Progress indicator — minimal, not a progress bar:
  Three dots, top-center of card
    Default dot:  6px, border-radius 50%, bg: var(--border-default)
    Active dot:   18px wide, 6px tall, border-radius 9999px, 
                  bg: var(--accent-primary)
                  ← pill shape for active, circle for inactive
    Transition:   width 250ms var(--ease-spring)
    
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
  
  No step numbers. No "Step 2 of 3" text. 
  The dots are enough — they respect the user's intelligence.

## Page Layout

Identical container to sign-in refactor:
  Full viewport, card centered
  Card: 400px wide, max-width: 92vw
  padding: 40px 36px
  background: var(--bg-card)
  border: 1px solid var(--border-default)
  border-radius: 16px
  box-shadow: var(--shadow-float)
  overflow: hidden

  Dark mode inner glow:
    box-shadow: var(--shadow-float), 
                inset 0 1px 0 rgba(167,240,221,0.06)

Logo / wordmark: inside card, top, small
  font-size: 15px, font-weight: 500
  color: var(--text-primary)
  letter-spacing: -0.2px
  margin-bottom: 20px

Progress dots: below logo, above heading
  display: flex, gap: 6px, justify-content: flex-start
  ← left-aligned, not centered — more editorial, less app-wizard

## Typography Per Step

Step 1:
  Heading:    "Create account"
  Subheading: "What should we call you?"

Step 2:
  Heading:    "Hi [name]"   ← dynamic, pulled from Step 1 input
  Subheading: "Set up your login details"

Step 3:
  Heading:    "Almost done"
  Subheading: "Confirm and you're in"

All headings:
  font-size: 22px, font-weight: 400
  color: var(--text-primary)
  letter-spacing: -0.4px
  margin-bottom: 6px

All subheadings:
  font-size: 13px, font-weight: 400
  color: var(--text-secondary)
  letter-spacing: 0.1px
  margin-bottom: 28px
  transition: opacity 150ms ease

## Input Fields — Same System as Sign-in

Floating label behavior (identical spec):
  Default:       label inside field, 14px, var(--text-tertiary)
  Focus/filled:  floats top-left, 11px, var(--accent-primary)
  Transition:    150ms var(--ease-standard)

Field styling:
  height: 52px
  border: 1.5px solid var(--border-default)
  border-radius: 10px
  background: var(--bg-card)
  padding: 18px 14px 6px
  font-size: 15px
  font-weight: 400
  color: var(--text-primary)
  width: 100%

  Dark mode input bg: --bg-input-dark: #1f3320

  Focus:
    border-color: var(--accent-primary)
    box-shadow: 0 0 0 3px rgba(156,172,84,0.18)
    outline: none

  Error:
    border-color: #c0392b
    box-shadow: 0 0 0 3px rgba(192,57,43,0.12)
    
  Filled not focused:
    border-color: var(--border-hover)
    box-shadow: none
    
  Valid / verified:
    border-color: var(--accent-primary)
    ← right side of field shows a 14px checkmark SVG
    color: var(--accent-primary)
    This is the one addition sign-up has that sign-in does not —
    positive confirmation that a field is good before moving on

## Step 2 — Password Field Reveal Within Step

Password field is NOT shown on step load.
It appears after the email field is filled and blurred:

  Email filled + blur → password field slides down:
    max-height: 0, opacity: 0 → max-height: 72px, opacity: 1
    transition: max-height 240ms var(--ease-decelerate),
                opacity 200ms var(--ease-decelerate)
    Auto-focus password on reveal

Password field extras:
  Show/hide toggle: eye icon, right side, 16px
  color: var(--text-tertiary), hover: var(--text-secondary)
  padding-right: 44px on input

Password strength indicator — beneath password field:
  4-segment bar, full width, gap: 3px between segments
  
  Segment styling:
    height: 3px
    border-radius: 9999px
    background: var(--border-default)   ← default all segments
    transition: background 300ms var(--ease-standard)
    
  Strength levels (based on character count + complexity):
    Weak (1 seg):    segment 1 → background: #c0392b
    Fair (2 segs):   segments 1-2 → background: #e67e22
    Good (3 segs):   segments 1-3 → background: var(--accent-primary)
    Strong (4 segs): all segments → background: var(--color-forest)
    
  Strength label — right-aligned, 11px, matching color:
    "Weak" / "Fair" / "Good" / "Strong"
    transition: color 300ms var(--ease-standard)

  Do not use a library. Implement strength as:
    score = 0
    if length >= 8: score++
    if /[A-Z]/.test(val): score++
    if /[0-9]/.test(val): score++
    if /[^A-Za-z0-9]/.test(val): score++
  Only add this logic if a password strength check does not 
  already exist in the codebase. If one exists, wire to it.

## Step 3 — Confirm Password or OTP

If confirm password:
  Single field, floating label "Confirm password"
  On blur — compare to Step 2 password:
    Match:    green border + checkmark (same as valid state above)
    No match: error border + shake + inline error "Passwords don't match"
    
  Shake animation — identical to sign-in spec:
    @keyframes shake {
      0%, 100% { transform: translateX(0) }
      20%       { transform: translateX(-6px) }
      40%       { transform: translateX(6px) }
      60%       { transform: translateX(-4px) }
      80%       { transform: translateX(4px) }
    }
    animation: shake 400ms var(--ease-standard)
    One shake only — never loops

If OTP fields exist in codebase:
  6 individual digit inputs, side by side
  Each input:
    width: 44px, height: 52px
    border: 1.5px solid var(--border-default)
    border-radius: 10px
    text-align: center
    font-size: 20px, font-weight: 400
    color: var(--text-primary)
    background: var(--bg-card)
    
    Focus:
      border-color: var(--accent-primary)
      box-shadow: 0 0 0 3px rgba(156,172,84,0.18)
      
    Filled:
      border-color: var(--border-hover)
      background: var(--bg-badge)   ← subtle fill on completed digit
      
  Auto-advance on digit entry (if logic exists — do not add)
  Paste handling (if exists — do not add)
  
  Gap between digits: 8px
  No label — the 6-box pattern is self-explanatory
  
  Below OTP boxes:
    "Didn't receive a code? Resend"
    font-size: 12px, color: var(--text-secondary)
    "Resend" → color: var(--accent-dark), font-weight: 500
    Hover: color: var(--accent-primary)
    
    Resend cooldown (if timer exists in codebase):
      "Resend in 0:42" — color: var(--text-tertiary)
      Do not add timer logic if not present

## CTA Button — Identical to Sign-in Spec

  height: 48px, width: 100%, border-radius: 10px
  background: var(--accent-dark), color: var(--text-on-dark)
  font-size: 15px, font-weight: 500, letter-spacing: 0.1px
  margin-top: 20px

  Hover:
    background: var(--accent-primary)
    color: var(--accent-dark)
    transform: translateY(-1px)
    box-shadow: var(--shadow-float)

  Active:
    transform: scale(0.98) translateY(0)
    box-shadow: var(--shadow-flush)

  Loading:
    CSS spinner, 16px
    border: 2px solid rgba(255,255,255,0.3)
    border-top-color: white
    border-radius: 50%
    animation: spin 0.7s linear infinite
    Button stays full width, disabled, opacity-80

  Step 1 + 2 CTA: disabled until field(s) have value
    Disabled: opacity-40, cursor-not-allowed
    Do not change color — opacity preserves palette integrity
    Transition from disabled → enabled: 
      opacity 200ms var(--ease-standard)
      ← the button coming alive as the user types 
        is a micro-moment of encouragement

## Back Navigation

Steps 2 and 3 only. Identical to sign-in spec:
  "← Back"
  position: top-left above heading
  font-size: 12px, color: var(--text-secondary)
  Hover: var(--text-primary)
  Appear: opacity 0→1, translateY(-4px)→0, 200ms delay 200ms

## Secondary Actions

Below CTA button, center-aligned:

  "Already have an account? Sign in"
    font-size: 13px
    "Already have an account?" → color: var(--text-secondary)
    "Sign in" → color: var(--accent-dark), font-weight: 500
    Hover on "Sign in": color: var(--accent-primary)
    
  Show on Step 1 only — once they're past Step 1, 
  they're committed. Don't offer the exit ramp.
  
  Disappears on Step 2+ with:
    opacity 1→0, height collapses, 
    200ms var(--ease-accelerate)

## Error Messaging — Global Rule

Inline only. Never toast. Never top-of-card banner.
  font-size: 12px
  color: #c0392b
  margin-top: 6px
  letter-spacing: 0.1px
  Appear: translateY(-4px)→0, opacity 0→1
  duration: 180ms var(--ease-decelerate)

## Social / OAuth Buttons (if they exist in codebase)

If Google / Apple / social login buttons exist:
  Move them above the form steps, not below
  Separated from the form by:
    A divider with centered "or" text
    1px solid var(--border-default), opacity 0.5
    "or" → font-size: 12px, color: var(--text-tertiary), 
            background: var(--bg-card), px-3
            ← inline with the divider line

  Social button styling:
    height: 44px, width: 100%
    border: 1.5px solid var(--border-default)
    border-radius: 10px
    background: transparent
    color: var(--text-primary)
    font-size: 14px, font-weight: 400
    display: flex, align-items: center, gap: 10px
    padding: 0 16px
    
    Hover:
      background: var(--bg-badge)
      border-color: var(--border-hover)
      ← flat hover — no elevation, no shadow
      Social buttons are secondary. Primary gets the elevation.
      
  If social buttons do not exist — do not add them.

## Consistency Enforcement With Sign-in Page

The sign-up and sign-in pages must feel like 
the same designer touched them on the same day:

  ✓ Same card dimensions (400px vs 380px — sign-up is slightly 
    wider to accommodate Step 2 two-field layout comfortably)
  ✓ Same border-radius system (card: 16px, inputs: 10px, button: 10px)
  ✓ Same floating label behavior
  ✓ Same button states and easing curves
  ✓ Same back navigation treatment
  ✓ Same error shake animation
  ✓ Same CSS variable set — no new variables introduced 
    unless strictly required (if new vars needed, 
    define them in the same :root block as sign-in vars)
  ✓ Same logo/wordmark treatment inside card

The user switching between sign-in and sign-up 
should feel like moving between rooms in the same house —
not clicking between two different products.

## What You Must NOT Change

  - Form onSubmit handler
  - Input name, id, type attributes
  - Validation logic
  - Auth state management
  - Redirect logic post-registration
  - API or service calls
  - Accessibility attributes (aria-*, role, htmlFor, autocomplete)
  - Router or navigation calls
  - OTP send/resend logic
  - Password strength logic if already implemented

## Audit Output

  File changed:              [filename]
  Steps implemented:         [1 / 2 / 3 — confirm which apply]
  Progress dots:             implemented / VERIFY
  Name echo in Step 2:       implemented / VERIFY
  Password reveal in Step 2: implemented / VERIFY
  Strength bar:              implemented / wired to existing / VERIFY
  OTP or confirm password:   [which was found] / VERIFY
  Valid checkmark state:     implemented / VERIFY
  Social buttons found:      [yes/no] — restyled / untouched
  Dark mode verified:        yes / VERIFY
  Consistency with sign-in:  verified / VERIFY
  Auth logic touched:        NO (confirm explicitly)
  New CSS variables added:   [list any] / none
  Flags:                     // VERIFY inline on anything uncertain