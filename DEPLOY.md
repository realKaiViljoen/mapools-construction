# Ma Pools Construction — Deployment Guide

Static site for Ma Pools Construction (premium pool care, Gauteng). Generated from Google Stitch designs and prepared for production hosting on Netlify or Vercel.

## What's in here

```
/                              ← deploy root (publish dir)
  index.html                   ← landing
  services.html
  gallery.html
  testimonials.html
  book.html                    ← booking form (wired to Netlify Forms)
  about.html
  privacy.html                 ← POPIA-compliant privacy policy
  terms.html
  thank-you.html               ← form success page
  404.html
  robots.txt
  sitemap.xml
  llms.txt                     ← AI-search index per llmstxt.org
  llms-full.txt                ← full content corpus for LLM ingestion
  favicon.svg
  netlify.toml                 ← Netlify config (headers, redirects, plugins)
  _redirects                   ← Netlify URL rules
  vercel.json                  ← Vercel config (clean URLs, headers, ignore)
  .vercelignore                ← Vercel exclusions
  /assets/
    /images/                   ← 28 brand images (PNG, ~12 MB total)
    site-config.json           ← brand contacts, service areas (single source)
    meta-tags.json             ← per-page SEO meta (reference)
    schema-templates.json      ← JSON-LD reference (already injected into pages)
  /_archive/                   ← old (non-modern) Stitch design variants — NOT deployed
  /_design_reference/          ← original Stitch exports + design-system docs — NOT deployed
  /_dev/                       ← one-shot migration scripts — NOT deployed
```

## Deploy to Netlify

**Option A — drag & drop (fastest):**
1. Open [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag the project root folder into the page
3. Netlify reads `netlify.toml` automatically and applies headers, redirects, security policy
4. Connect your custom domain in Site Settings → Domain Management

**Option B — git-connected (recommended):**
1. Push this repo to GitHub/GitLab
2. Netlify → "Add new site" → "Import an existing project" → select repo
3. Build command: *leave blank*
4. Publish directory: `.`
5. Deploy. The booking form auto-registers under Forms → "consultation"

**Form notification setup:**
- Netlify dashboard → Forms → "consultation" → Settings → email notifications
- Set up a forwarding address so the team gets every booking

## Deploy to Vercel

1. `vercel` CLI → `vercel --prod` from the project root, OR
2. vercel.com → Import Project → connect repo
3. Framework preset: **Other**
4. Build command: leave default (the `ignoreCommand` in `vercel.json` handles it)
5. Output directory: `.`
6. ⚠️  **Vercel does not host forms.** If you go with Vercel, replace the booking form action with one of:
   - Formspree (`action="https://formspree.io/f/<id>"`)
   - Web3Forms
   - A Vercel serverless function under `/api/booking.ts`

## Pre-launch placeholders to replace

These are search-and-replace items. Most live in `assets/site-config.json`, `assets/schema-templates.json` (already injected into HTML), `privacy.html`, `terms.html`, `llms.txt`, and `robots.txt`.

| Placeholder | Used in | Replace with |
|---|---|---|
| `https://www.mapoolsconstruction.co.za` | every page (canonicals, OG, JSON-LD, sitemap, robots, llms) | the real production domain (search-replace globally) |
| `+27 78 712 2157` | schema, privacy, terms | real phone number |
| `concierge@mapoolsconstruction.co.za` | schema, contact | real concierge inbox |
| `privacy@mapoolsconstruction.co.za` | privacy.html | real DPO/privacy contact |
| `331B Utekwane Street, Zone 7, Sandhurst, 2196` | schema, address | real registered address |
| Lat `-26.10760` / lng `28.05680` | LocalBusiness `geo` | real business coordinates |
| `aggregateRating: 4.9 / 47 reviews` | LocalBusiness schema | **must reflect verified Google Business Profile data** before launch — fabricated ratings violate Google guidelines |
| `https://www.instagram.com/mapoolsconstruction` etc. | LocalBusiness `sameAs` | real social URLs (or remove entries) |
| `@aquaestate` | Twitter card meta | real Twitter handle |
| OG image paths (`og-aquaestate-*.jpg`) | meta tags on every page | designer to produce 1200×630 share images and drop into `/assets/images/` |

After replacing, run a quick search to confirm:
```bash
grep -RIn "mapoolsconstruction.co.za\|+27 78 712 2157\|@aquaestate" *.html assets/
```

## Image work owed to the designer (UNR)

The 28 images currently in `/assets/images/` are AI-generated placeholders pulled off Stitch's CDN. Replace with real photography for production:

- **Hero shots** — `hero-luxury-infinity-pool-gauteng.png` (used as the home hero background)
- **Service photography** — `service-weekly-maintenance-luxury-pool.png`, `service-pool-technician-water-testing.png`
- **Gallery / portfolio** — 8 gallery images of real estate pools the company has serviced
- **Team portraits** — `team-adrian-thorne-director.png`, `team-pieter-van-wyk-head-technician.png`, `team-sarah-mokoena-client-relations.png` (currently AI faces — replace with real team photos and update names if needed)
- **Testimonial avatars** — 4 client portraits (likely best replaced with logo/initials if clients prefer privacy)
- **OG share images** — designer must create 7 × 1200×630 JPGs (`og-aquaestate-default.jpg`, `-home`, `-services`, `-gallery`, `-testimonials`, `-book`, `-about`)

Filenames should be **kept as-is** so no HTML edits are needed — the designer just drops replacements into `/assets/images/` with the same filename. After replacing, optimize:
- 6 images currently >500 KB are flagged in `assets/images/_url-mapping.json` (`needs_optimization: true`)
- Convert to WebP or compress JPG — target <250 KB per image
- Add a real `favicon.png` (32×32) and `apple-touch-icon.png` (180×180) alongside the existing `favicon.svg`

## Six pre-launch checks (5 minutes)

1. **Domain pointed?** DNS A/CNAME records updated; HTTPS auto-issued by host.
2. **Forms work?** Submit `book.html` once; confirm email arrives.
3. **Sitemap submitted?** Google Search Console → add property → submit `https://www.mapoolsconstruction.co.za/sitemap.xml`.
4. **Schema valid?** Paste each page URL into [Schema.org Validator](https://validator.schema.org). All 11 JSON-LD blocks should parse green.
5. **Lighthouse?** Chrome DevTools → Lighthouse → mobile audit. Target 90+ on Performance / 100 on SEO / 100 on Best Practices. The Tailwind CDN warning is acceptable for v1; v2 should bundle Tailwind.
6. **Tighten CSP after image migration:** the CSP in `netlify.toml` and `vercel.json` still whitelists `lh3.googleusercontent.com` — remove that entry once you've confirmed no lh3 references remain.

## Known limitations / V2 roadmap

- **Tailwind CDN** is loaded via `<script>` (Stitch default). Production-grade move: install Tailwind locally, build a single minified CSS file, drop the CDN. Saves ~200 KB on first paint.
- **Analytics not installed** (your call — deferred to v2). When you add it, the CSP already permits `plausible.io`. Drop the script in each `<head>` between `<!-- AE:META:START -->` markers.
- **No FAQ content** — Stitch didn't generate FAQ sections. Adding 6–10 Q&As + `FAQPage` schema would meaningfully help AI-search visibility.
- **Service-area landing pages** (e.g. `/pool-care-sandton`, `/pool-care-pretoria`) are a high-impact local-SEO play for v2 — generate one per suburb listed in `site-config.json`.
- **Real testimonials with verified names** strengthen the existing review schema — replace the 4 placeholder testimonials with real, attributable ones if possible.
