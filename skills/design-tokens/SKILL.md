---
name: design-tokens
description: Use when adding or changing colors, spacing, typography, or shadows in CSS — ensures all visual values go through CSS custom properties instead of hardcoded hex/px values
---

# Design Tokens

## Overview

Replace hardcoded CSS values with a three-layer token architecture using CSS custom properties. Prevents inconsistency, makes theming trivial, and makes dark mode possible.

**Core principle:** No raw hex colors or magic numbers in component styles — every visual value is a named token.

**Source:** Adapted from [ui-ux-pro-max design-system skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).

## When to Use

- Adding any new color, spacing, or typography value to CSS
- Refactoring existing hardcoded values in `templates/index.html` or any CSS
- Implementing dark mode
- Making the UI consistent across components

## The Three-Layer Model

```
Primitive → Semantic → Component
```

### Layer 1: Primitives (raw values)

These are your palette — not used directly in components.

```css
:root {
  /* Color primitives */
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-50:  #f9fafb;
  --color-gray-900: #111827;
  --color-red-500:  #ef4444;
  --color-green-500: #22c55e;
  --color-white:    #ffffff;

  /* Spacing primitives */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;

  /* Typography primitives */
  --font-size-sm:  14px;
  --font-size-base: 16px;
  --font-size-lg:  18px;
  --font-size-xl:  24px;
  --font-size-2xl: 32px;

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold:   700;

  --line-height-tight:  1.25;
  --line-height-normal: 1.5;
  --line-height-loose:  1.75;
}
```

### Layer 2: Semantics (purpose aliases)

These map primitives to meaning. These are what you use in components.

```css
:root {
  /* Brand */
  --color-primary:         var(--color-blue-500);
  --color-primary-hover:   var(--color-blue-600);

  /* Surfaces */
  --color-background:      var(--color-gray-50);
  --color-surface:         var(--color-white);

  /* Text */
  --color-text-primary:    var(--color-gray-900);
  --color-text-secondary:  #6b7280;  /* gray-500 */
  --color-text-on-primary: var(--color-white);

  /* Feedback */
  --color-error:    var(--color-red-500);
  --color-success:  var(--color-green-500);

  /* Spacing semantic */
  --spacing-component-padding: var(--space-4);
  --spacing-section-gap:       var(--space-8);
  --spacing-button-height:     44px;  /* touch target minimum */
}
```

### Layer 3: Components (component-specific)

Only override when a component genuinely needs to deviate from semantic defaults.

```css
.record-button {
  background:   var(--color-primary);
  color:        var(--color-text-on-primary);
  padding:      var(--space-3) var(--space-6);
  min-height:   var(--spacing-button-height);
  min-width:    var(--spacing-button-height);
  font-size:    var(--font-size-base);
  font-weight:  var(--font-weight-bold);
}

.record-button:hover {
  background: var(--color-primary-hover);
}

.language-select {
  font-size:    var(--font-size-base);
  padding:      var(--space-2) var(--space-3);
  min-height:   var(--spacing-button-height);
}
```

## Dark Mode

Once tokens are in place, dark mode is just a layer swap:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-background:   #111827;
    --color-surface:      #1f2937;
    --color-text-primary: #f9fafb;
    --color-text-secondary: #9ca3af;
  }
  /* Component tokens automatically inherit the new semantic values */
}
```

## LinguaFlow Token Starter

Create a `<style>` block at the top of `templates/index.html` (or a linked `static/tokens.css`) with these tokens as a starting point:

```css
:root {
  /* Primitives */
  --color-blue-500:  #3b82f6;
  --color-blue-600:  #2563eb;
  --color-gray-50:   #f9fafb;
  --color-gray-500:  #6b7280;
  --color-gray-900:  #111827;
  --color-red-500:   #ef4444;
  --color-green-500: #22c55e;
  --color-white:     #ffffff;

  --space-2: 8px;  --space-3: 12px;  --space-4: 16px;
  --space-6: 24px; --space-8: 32px;  --space-12: 48px;

  --font-size-base: 16px;
  --font-size-lg:   18px;
  --font-size-xl:   24px;
  --line-height-normal: 1.5;

  /* Semantics */
  --color-primary:          var(--color-blue-500);
  --color-primary-hover:    var(--color-blue-600);
  --color-background:       var(--color-gray-50);
  --color-surface:          var(--color-white);
  --color-text-primary:     var(--color-gray-900);
  --color-text-secondary:   var(--color-gray-500);
  --color-text-on-primary:  var(--color-white);
  --color-error:            var(--color-red-500);
  --color-success:          var(--color-green-500);

  --spacing-touch-target:   44px;
  --spacing-component-gap:  var(--space-4);
  --spacing-section-gap:    var(--space-8);
}
```

## Rules

- **Never** put raw hex (`#3b82f6`) directly in a component rule
- **Never** put magic numbers (`16px`, `8px`) directly in a component rule — use a token
- **Always** add a new primitive if the value doesn't exist yet, then a semantic alias, then use the semantic in the component
- **One source of truth** — if you need to change the primary color, change one primitive

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `.btn { color: #3b82f6; }` | `.btn { color: var(--color-primary); }` |
| `.card { padding: 16px; }` | `.card { padding: var(--space-4); }` |
| Semantic token used as primitive | Only use semantic tokens in components |
| Dark mode by duplicating all component CSS | Dark mode only overrides semantic tokens in a media query |
| Skipping Layer 2 | Always alias primitives to semantics before using in components |
