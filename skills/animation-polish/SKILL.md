---
name: animation-polish
description: Use when adding any animation, transition, or interactive feedback to the LinguaFlow UI — recording button states, results appearing, loading indicators, error messages, or any element that moves or transitions
---

# Animation Polish

## Overview

Every animation detail compounds into something that feels right. The goal is invisible correctness — interactions that feel exactly as expected, with no friction the user can name.

**Source:** Adapted from [Emil Kowalski's design engineering skill](https://emilkowal.ski/skill) for plain HTML/CSS/JS (Framer Motion and React references removed).

**Core principle:** "All those unseen details combine to produce something that's just stunning, like a thousand barely audible voices all singing in tune." — Paul Graham

---

## Step 1 — Should This Even Animate?

Ask: how often will users see this?

| Frequency | Decision |
|-----------|----------|
| Constant (every keystroke, every mic click) | No animation. Ever. |
| Dozens of times per session (hover effects, dropdown open) | Remove or drastically reduce |
| Occasional (results appearing, error messages, status toasts) | Standard animation |
| Rare (first-time onboarding, celebrations) | Can add delight |

**LinguaFlow examples:**
- Recording button toggle → animation OK (occasional)
- Results appearing after translation → animation OK (occasional)
- Language selector dropdown open → minimal only (frequent)
- Mic level indicator while recording → no animation, direct real-time update

---

## Step 2 — Choose the Right Easing

**Built-in CSS easings are too weak.** Use custom cubic-bezier curves:

```css
:root {
  --ease-out:    cubic-bezier(0.23, 1, 0.32, 1);      /* UI interactions — starts fast */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);     /* on-screen movement */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);      /* slides, drawers */
}
```

**Decision tree:**
- Element entering or exiting → `ease-out` (starts fast, feels responsive)
- Element moving/morphing on screen → `ease-in-out`
- Hover/color change → `ease`
- Constant motion (spinner) → `linear`

**Never use `ease-in` for UI.** It starts slow — exactly when the user is watching most closely — making the interface feel sluggish.

---

## Step 3 — Duration

| Element | Duration |
|---------|----------|
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Results/cards appearing | 200–300ms |
| Toast notifications | 300–400ms |

**Rule: stay under 300ms for UI animations.** A 180ms result-appear feels more responsive than a 400ms one, even with identical load time.

---

## LinguaFlow Component Patterns

### Recording Button — Press Feedback

Every pressable element must respond to touch/click instantly:

```css
.record-btn {
  transition: transform 160ms var(--ease-out);
}

.record-btn:active {
  transform: scale(0.97);
}
```

Scale should be subtle (0.95–0.98). This makes the UI feel like it heard the user.

### Recording Button — State Change (Idle → Recording)

```css
.record-btn {
  transition: background-color 200ms ease, transform 160ms var(--ease-out);
}

.record-btn[data-recording="true"] {
  background-color: var(--color-error);  /* red = recording */
}

/* Pulse ring while recording */
@keyframes pulse-ring {
  0%   { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.4); opacity: 0; }
}

.record-btn[data-recording="true"]::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 2px solid var(--color-error);
  animation: pulse-ring 1.2s linear infinite;
}

@media (prefers-reduced-motion: reduce) {
  .record-btn[data-recording="true"]::after {
    animation: none;
  }
}
```

### Results Appearing After Translation

Never animate from `scale(0)` — nothing in the real world appears from nothing. Start from near-visible:

```css
.results-panel {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 250ms var(--ease-out), transform 250ms var(--ease-out);
}

/* CSS entry animation without JavaScript */
@starting-style {
  .results-panel {
    opacity: 0;
    transform: translateY(8px);
  }
}

/* Fallback for browsers without @starting-style */
.results-panel[data-entering] {
  opacity: 0;
  transform: translateY(8px);
}
```

### Status Toast / Error Messages

Toasts enter from below, exit the same direction (spatial consistency makes swipe-dismiss intuitive):

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  /* Use CSS transitions, not keyframes — interruptible when new toasts arrive */
  transition: opacity 300ms ease, transform 300ms var(--ease-out);
}

.toast[data-state="entering"] {
  opacity: 0;
  transform: translateY(100%);
}

.toast[data-state="exiting"] {
  opacity: 0;
  transform: translateY(100%);
  /* Exit faster than enter */
  transition-duration: 200ms;
}
```

**Use CSS transitions, not `@keyframes`, for toasts** — transitions can be retargeted mid-animation when a second toast arrives; keyframes restart from zero.

### Language Selector Hover

Gate hover animations behind a media query — touch devices trigger `:hover` on tap, causing false positives:

```css
@media (hover: hover) and (pointer: fine) {
  .language-select:hover {
    border-color: var(--color-primary);
    transition: border-color 150ms ease;
  }
}
```

---

## Performance Rules

Only these two properties are GPU-accelerated (skip layout + paint):
- `transform`
- `opacity`

**Never animate:** `width`, `height`, `padding`, `margin`, `top`, `left` — these trigger full layout recalculation.

```css
/* Bad — triggers layout */
.panel { transition: height 300ms ease; }

/* Good — GPU only */
.panel { transition: transform 300ms ease, opacity 300ms ease; }
```

**Avoid `transition: all`** — it catches unintended properties and creates performance problems:

```css
/* Bad */
.btn { transition: all 300ms; }

/* Good */
.btn { transition: transform 160ms var(--ease-out), background-color 200ms ease; }
```

---

## Accessibility

### prefers-reduced-motion

Reduced motion means fewer/gentler animations, not zero. Keep opacity/color transitions; remove movement.

```css
@media (prefers-reduced-motion: reduce) {
  .results-panel {
    transition: opacity 200ms ease;
    /* Remove transform animation */
  }

  .record-btn[data-recording="true"]::after {
    animation: none;
  }
}
```

### Review Checklist

| Issue | Fix |
|-------|-----|
| `transition: all` | Specify exact properties |
| `scale(0)` entry | Start from `scale(0.95)` + `opacity: 0` |
| `ease-in` on any UI element | Switch to `ease-out` |
| Duration > 300ms on UI element | Reduce to 150–250ms |
| Hover animation without media query | Add `@media (hover: hover) and (pointer: fine)` |
| `@keyframes` on rapidly-triggered elements | Use CSS transitions |
| No press feedback on recording button | Add `transform: scale(0.97)` on `:active` |
| Animation without `prefers-reduced-motion` check | Add `@media (prefers-reduced-motion: reduce)` |
| Same speed for enter and exit | Exit should be ~60–70% of enter duration |
| Elements all appear at once (multiple results) | Stagger by 30–80ms per item |
