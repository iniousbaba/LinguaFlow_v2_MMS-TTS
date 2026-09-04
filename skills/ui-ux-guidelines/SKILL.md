---
name: ui-ux-guidelines
description: Use when designing, building, or reviewing any part of the LinguaFlow web UI — recording button, language selectors, results display, audio player, or any new page element
---

# UI/UX Guidelines

## Overview

Design rules for LinguaFlow's plain HTML/CSS/JS web interface. Follow priority order 1→5 when deciding what to fix first.

**Source:** Adapted from [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for plain web (not React Native / Tailwind).

## Priority 1 — Accessibility (CRITICAL)

These must never be skipped.

- **Contrast 4.5:1** — All body text against its background; 3:1 minimum for large text (18px+ bold or 24px+)
- **Focus rings** — Every interactive element (`button`, `select`, `a`) must have a visible focus ring (2–4px outline); never `outline: none` without a replacement
- **Alt text** — All `<img>` tags get descriptive `alt`; decorative images get `alt=""`
- **aria-labels** — Icon-only buttons need `aria-label` (e.g. the recording button: `aria-label="Start recording"`)
- **Keyboard nav** — Tab order must match visual order; recording button and language selectors must be fully keyboard-operable
- **Form labels** — Every `<select>` and `<input>` needs a `<label for="...">`, not just placeholder text
- **Heading hierarchy** — Sequential h1→h2→h3, never skip levels
- **Color not only** — Don't use color alone to convey status (e.g. recording state); add text or icon too
- **Reduced motion** — Respect `prefers-reduced-motion: reduce`; disable or simplify animations when set

## Priority 2 — Touch & Interaction (CRITICAL)

LinguaFlow is used on mobile (microphone recording). These are non-negotiable.

- **Touch target size** — Recording button and all controls: minimum **44×44px** interactive area
- **Touch spacing** — At least 8px gap between adjacent interactive elements
- **No hover-only** — Never make a feature accessible only via `:hover`; `click`/`tap` must always work
- **Loading feedback** — Disable the record button while audio is being processed; show a spinner or progress indicator
- **Error near the source** — Show recognition/translation errors near the relevant UI element, not just in a banner
- **cursor: pointer** — All clickable elements that are not `<a>` or `<button>` must have `cursor: pointer`
- **tap-action: manipulation** — Add `touch-action: manipulation` to buttons to remove the 300ms tap delay on mobile

## Priority 3 — Layout & Responsive (HIGH)

- **Viewport meta** — `<meta name="viewport" content="width=device-width, initial-scale=1">` — never disable zoom
- **Mobile-first** — Design for 375px first; scale up to tablet/desktop
- **No horizontal scroll** — Content must fit viewport width on all screen sizes
- **Readable body text** — Minimum 16px on mobile (avoids iOS auto-zoom)
- **Line length** — 35–60 chars per line on mobile; 60–75 on desktop
- **Spacing scale** — Use multiples of 4px or 8px for all padding/margin; no arbitrary values

## Priority 4 — Forms & Feedback (MEDIUM)

LinguaFlow's core interaction is form-based (language selection + record).

- **Visible labels** — Language selectors must have visible `<label>` elements, not just placeholder text
- **Submit feedback** — After recording stops: show loading → then success (transcription text) or error
- **Error message content** — State what went wrong and how to fix it: not "Error" but "Microphone access denied. Allow microphone access in your browser settings."
- **Empty states** — If no translation yet, show a prompt ("Record speech to see translation here"), not a blank space
- **Toast dismiss** — Auto-dismiss status messages after 3–5 seconds; also provide a manual close button
- **Destructive confirmation** — If clearing results, confirm before discarding

## Priority 5 — Typography & Color (MEDIUM)

- **Base font size** — 16px body text minimum
- **Line height** — 1.5–1.75 for body text
- **Semantic color tokens** — Use CSS custom properties for color, not raw hex in component styles (see `design-tokens` skill)
- **Text contrast** — Dark text on light backgrounds; re-verify after any color change
- **Font scale** — Consistent type scale (e.g. 12 / 14 / 16 / 18 / 24 / 32px); avoid arbitrary sizes

## LinguaFlow-Specific Checklist

Run this before any UI change ships:

**Recording Button:**
- [ ] Minimum 44×44px tap area
- [ ] `aria-label` present and descriptive (`"Start recording"` / `"Stop recording"`)
- [ ] Disabled + spinner shown while processing
- [ ] Focus ring visible on keyboard tab
- [ ] State change (recording vs idle) communicated via text/icon, not color alone

**Language Selectors:**
- [ ] `<label for="...">` for each `<select>`
- [ ] Sufficient size for touch (44px height minimum on mobile)
- [ ] Works with keyboard (Tab + arrow keys)

**Results Display:**
- [ ] Empty state message when no translation exists
- [ ] Error messages describe cause + fix
- [ ] Text contrast ≥4.5:1

**Audio Player:**
- [ ] Native `<audio controls>` (fully accessible) unless custom — if custom, full keyboard + ARIA support required
- [ ] Does not autoplay (let user initiate)

**Overall:**
- [ ] No horizontal scroll at 375px viewport width
- [ ] All body text ≥16px
- [ ] Focus rings visible on all interactive elements
- [ ] `prefers-reduced-motion` respected

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `outline: none` on focused elements | Replace with a visible custom focus ring |
| Icon-only recording button with no label | Add `aria-label="Start recording"` |
| Placeholder text used as label | Add `<label for="...">` above the field |
| "Error" as the full error message | State cause + recovery action |
| Processing with no feedback | Disable button + show spinner during `fetch()` |
| Emoji used as icons | Use SVG icons instead |
