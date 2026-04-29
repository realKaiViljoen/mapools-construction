---
name: Premium Pool Care System
colors:
  surface: '#f7fafd'
  surface-dim: '#d7dade'
  surface-bright: '#f7fafd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f7'
  surface-container: '#ebeef2'
  surface-container-high: '#e5e8ec'
  surface-container-highest: '#e0e3e6'
  on-surface: '#181c1f'
  on-surface-variant: '#44474e'
  inverse-surface: '#2d3134'
  inverse-on-surface: '#eef1f4'
  outline: '#74777e'
  outline-variant: '#c4c6cf'
  surface-tint: '#4a5f81'
  primary: '#000d22'
  on-primary: '#ffffff'
  primary-container: '#0a2342'
  on-primary-container: '#768baf'
  inverse-primary: '#b2c7ef'
  secondary: '#5d5f5f'
  on-secondary: '#ffffff'
  secondary-container: '#dfe0e0'
  on-secondary-container: '#616363'
  tertiary: '#140b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#302000'
  on-tertiary-container: '#a78541'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d5e3ff'
  primary-fixed-dim: '#b2c7ef'
  on-primary-fixed: '#021c3a'
  on-primary-fixed-variant: '#324768'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#ffdea5'
  tertiary-fixed-dim: '#e9c176'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5d4201'
  background: '#f7fafd'
  on-background: '#181c1f'
  surface-variant: '#e0e3e6'
typography:
  display-xl:
    fontFamily: Noto Serif
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Noto Serif
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Noto Serif
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-upper:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.4'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 32px
  margin-mobile: 24px
  margin-desktop: 80px
---

## Brand & Style

This design system is built to evoke the atmosphere of a high-end private estate in Gauteng—combining the refreshing clarity of a pristine swimming pool with the architectural permanence of a luxury home. The brand personality is **authoritative, serene, and exclusive.** It targets discerning homeowners who value precision, reliability, and a frictionless service experience.

The visual style follows a **Minimalist** approach with a **Modern Corporate** foundation. It prioritizes heavy whitespace to represent cleanliness and utilizes subtle **Glassmorphism** for overlay elements to mimic the translucency of water. Every interaction should feel intentional and calm, reinforcing the "set-and-forget" reliability of the service.

## Colors

The palette is anchored in **Deep Navy (#0A2342)**, providing a sense of depth and professional stability. This is balanced by **Crisp White (#FFFFFF)** to ensure the UI feels airy and hygienic. 

**Champagne Gold (#C5A059)** is used sparingly as a premium accent for call-to-actions and high-value status indicators, representing the "gold standard" of service. A **Cool Silver (#E2E8F0)** is used for secondary borders and inactive states. The default mode is Light to maximize the "sun-drenched" feel appropriate for the South African climate, though deep-blue backgrounds are used for high-impact editorial sections.

## Typography

This design system utilizes a high-contrast typographic pairing to establish a premium editorial feel. 

**Noto Serif** is used for headlines to convey heritage and sophistication. It should be typeset with generous leading and slight negative letter-spacing for larger display sizes to maintain a tight, professional appearance. 

**Manrope** serves as the functional workhorse for body copy and UI labels. It was selected for its modern, geometric construction and high legibility. All small labels should be set in uppercase with increased letter-spacing to reinforce the luxurious, organized nature of the brand.

## Layout & Spacing

The layout philosophy follows a **Fixed Grid** model to ensure content feels curated and centered. On desktop, a 12-column grid is used with a generous 80px outer margin to create a "gallery" effect. 

Spacing follows a strict 8px rhythmic scale. To emphasize exclusivity and "breathing room," vertical padding between major sections should be aggressive (typically 120px to 160px). Elements should be grouped using proximity, but those groups must be isolated by significant whitespace to prevent the UI from feeling cluttered or "cheap."

## Elevation & Depth

Hierarchy is communicated through **Tonal Layers** and **Ambient Shadows**. Surfaces do not "float" aggressively; instead, they sit just above the base layer with soft, extra-diffused shadows (0% offset, 20px blur, 4% opacity of the Primary color).

A signature depth effect in this design system is the use of **Backdrop Blurs**. Modals and navigation bars should use a 12px blur with an 80% white opacity tint, creating a "frosted water" aesthetic. This keeps the user connected to the background context while providing the necessary contrast for interaction.

## Shapes

The shape language is **Structured and Architectural**. A "Soft" (0.25rem) corner radius is applied to standard UI components like input fields and small buttons. This retains a sense of precision and professional sharpness.

Large cards and containers use a "Rounded" (0.5rem) radius to feel more approachable. Circles are reserved exclusively for avatars and floating status indicators. High-contrast, 1px borders in Silver or Gold are used to define shapes without relying on heavy fills, maintaining the minimalist aesthetic.

## Components

### Buttons
Primary buttons use the Deep Navy fill with white Manrope text, utilizing a "Champagne Gold" 2px bottom-border on hover for a subtle luxury touch. Secondary buttons are "Ghost" style with a 1px Silver border.

### Input Fields
Inputs are minimalist: a bottom-border only (1px Silver) that transitions to Deep Navy on focus. Labels sit above the line in the "label-upper" typographic style.

### Cards
Cards are white with a very faint Silver border (no shadow by default). On hover, they lift slightly using the ambient shadow defined in the Elevation section.

### Status Chips
Service status (e.g., "Chemicals Balanced") should use a subtle pill-shaped chip with a light tint of the status color and a high-contrast text color. 

### Featured Services List
Lists representing premium packages should use Noto Serif for the title and include a thin horizontal divider between items to emphasize order and cleanliness.

### Exclusive Elements
Include a "Signature Stamp" component—a gold-outlined seal used to certify a pool's water quality or technician's arrival, reinforcing the premium service guarantee.