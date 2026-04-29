---
name: Luxury Pool Care Design System
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#44474e'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#74777e'
  outline-variant: '#c4c6cf'
  surface-tint: '#4a5f81'
  primary: '#000d22'
  on-primary: '#ffffff'
  primary-container: '#0a2342'
  on-primary-container: '#768baf'
  inverse-primary: '#b2c7ef'
  secondary: '#5c5f60'
  on-secondary: '#ffffff'
  secondary-container: '#e1e3e4'
  on-secondary-container: '#626566'
  tertiary: '#060d1d'
  on-tertiary: '#ffffff'
  tertiary-container: '#1b2334'
  on-tertiary-container: '#838a9f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d5e3ff'
  primary-fixed-dim: '#b2c7ef'
  on-primary-fixed: '#021c3a'
  on-primary-fixed-variant: '#324768'
  secondary-fixed: '#e1e3e4'
  secondary-fixed-dim: '#c5c7c8'
  on-secondary-fixed: '#191c1d'
  on-secondary-fixed-variant: '#454748'
  tertiary-fixed: '#dbe2fa'
  tertiary-fixed-dim: '#bfc6dd'
  on-tertiary-fixed: '#141b2c'
  on-tertiary-fixed-variant: '#3f4759'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Noto Serif
    fontSize: 64px
    fontWeight: '400'
    lineHeight: '1.1'
    letterSpacing: 0.05em
  headline-lg:
    fontFamily: Noto Serif
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: 0.03em
  headline-md:
    fontFamily: Noto Serif
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.3'
    letterSpacing: 0.02em
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.08em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 32px
  margin-x: 64px
  section-gap: 120px
---

## Brand & Style
The design system embodies a "Framer-style" aesthetic—a fusion of editorial elegance and cutting-edge digital craftsmanship. It is designed for a high-end luxury pool care brand, prioritizing tranquility, precision, and architectural beauty. 

The style utilizes **Glassmorphism** and **Minimalism** to create an interface that feels as clear and inviting as pristine water. By leveraging expansive whitespace, refined serif typography, and soft, organic shapes, the design system evokes an emotional response of calm reliability and exclusive sophistication.

## Colors
The palette is anchored by a deep, authoritative navy that represents depth and stability. This is contrasted against a series of "Liquid Off-Whites" used for surfaces to prevent the clinical feel of pure white.

- **Primary (#0A2342):** Deep Navy. Used for core branding, primary headings, and high-emphasis CTAs.
- **Surface (Off-White):** A range of soft whites (e.g., #F8F9FA, #F1F5F9) provide a warm, premium canvas.
- **Glass Effects:** Semi-transparent layers use white at 40-70% opacity with a `backdrop-filter: blur(12px)` to simulate frosted glass.
- **Accents:** Subtle slate and muted indigo tones are used for secondary UI elements to maintain a monochromatic, high-end feel.

## Typography
The typographic scales emphasize a contrast between heritage and modernity. **Noto Serif** is reserved for headlines, utilized with generous letter-spacing (tracking) to achieve a "Vogue-like" editorial quality.

For functional text, **Manrope** provides a highly legible, modern sans-serif experience. It maintains a clean, architectural look that balances the decorative nature of the serif. All labels should use increased letter-spacing and uppercase styling to denote premium status and clear hierarchy.

## Layout & Spacing
The design system employs a **Fixed Grid** model for desktop, centered within a 1280px container to maintain focus and luxury proportions. 

A 12-column grid system is used with wide 32px gutters to allow the layout to "breathe." Vertical rhythm is governed by a 120px section gap, ensuring that every content block feels intentional and distinct. This generous use of negative space is a hallmark of the brand's premium positioning.

## Elevation & Depth
Hierarchy is established through a multi-layered shadow system and glassmorphism. This design system avoids harsh borders in favor of "Floating Layers."

- **Shadow Style:** Shadows must be extremely diffused and low-opacity. Use a three-layer stack: a very soft ambient occlusion shadow, a medium-range mid-tone, and a wide-spread, low-opacity (5-8%) outer glow to simulate a light source.
- **Glass Layers:** Floating panels (cards, navigation) use a semi-transparent background with a subtle 1px inner border (white at 20% opacity) to catch the light, enhancing the "glass" effect.
- **Tonal Depth:** Backgrounds should use subtle radial gradients (e.g., from #FFFFFF to #F1F5F9) to create a soft "spotlight" effect behind primary content.

## Shapes
The shape language is defined by softness and fluidity. Following a "Superellipse" philosophy, corner radii are kept large to mimic the smoothed edges of luxury pool tiles or rounded architectural features.

Standard elements like buttons and input fields use a **12px** radius, while larger containers and featured cards utilize a **24px** radius. This high degree of rounding contributes to the "soft-modern" aesthetic and makes the interface feel approachable yet meticulously designed.

## Components
- **Buttons:** Primary buttons feature the Deep Navy background with white Manrope text. They should have a subtle scale-up interaction (1.02x) on hover. Secondary buttons should use the glassmorphism effect with a 1px border.
- **Cards:** Cards are the primary vessel for content. They must feature a 24px border radius and the multi-layered shadow system. Avoid heavy text; prioritize high-quality imagery and serif headlines.
- **Inputs:** Form fields should be "Soft-Flush"—utilizing a very light off-white background (#F1F5F9) with a 12px radius, moving to a Deep Navy 1px border on focus.
- **Micro-interactions:** Elements should "float" into view using a `0.6s cubic-bezier(0.22, 1, 0.36, 1)` transition. 
- **Scroll Animations:** Implement a "Reveal & Shift" style. As the user scrolls, content should fade in from 0% to 100% opacity while simultaneously shifting upwards by 20px, creating a sense of graceful emergence.
- **Navigation:** The header should be a floating glassmorphism "pill" that stays pinned to the top, utilizing a backdrop blur to maintain legibility over varying background content.