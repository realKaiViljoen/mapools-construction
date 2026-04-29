# Ma Pools Construction — production-prep work log

Date: 2026-04-29
Source: Google Stitch export (12 folders — 6 pages × 2 design variants).
Target: deploy-ready static site for Netlify/Vercel.

## Completed

- [x] Restructured project: production pages at root with semantic filenames; non-"modern" variant moved to `_archive/`; original Stitch exports + design-system docs moved to `_design_reference/`
- [x] Migrated all 28 Stitch CDN images (`lh3.googleusercontent.com`) to local `/assets/images/` with semantic filenames; 0 lh3 references remain in production HTML
- [x] Generated SEO + LLM + hosting assets: `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `netlify.toml`, `_redirects`, `vercel.json`, `.vercelignore`, `404.html`, `privacy.html` (POPIA-compliant), `terms.html`, `favicon.svg`, `thank-you.html`
- [x] Per-page meta injection: title, description, robots, canonical, OG, Twitter card, favicon link — all 6 production pages have unique compelling titles + descriptions
- [x] Schema.org JSON-LD: 11 valid blocks across pages — sitewide LocalBusiness (HomeAndConstructionBusiness subtype), WebSite SearchAction, Service catalog, ImageGallery, Reviews + AggregateRating, ContactPage. All parse OK.
- [x] Replaced every `<img>` alt with SEO-friendly Gauteng-specific descriptions; added `loading="lazy" decoding="async"` to non-hero images, `loading="eager" fetchpriority="high"` to hero images
- [x] Fixed cross-page navigation: 52 anchor `href="#xyz"` rewritten + 6 trailing `href="#"` text-mapped + 1 manual fix for service-package CTA
- [x] Converted 11 prominent CTA `<button>` elements to `<a role="button">` so they actually navigate (skipped genuine `type="submit"` buttons)
- [x] Wired booking form for Netlify: `name="consultation" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/thank-you.html"` + hidden `form-name` field + honeypot
- [x] Verification pass: local Python http.server smoke test — all 16 pages/assets return 200; all per-page image refs resolve; all titles unique; 0 broken anchors; XML sitemap valid; all JSON-LD parses
- [x] Excluded dev artifacts from deploy: `_dev/`, `_archive/`, `_design_reference/`, `tasks/`, `CLAUDE.md` blocked via `_redirects` (Netlify) and `.vercelignore` (Vercel)
- [x] Wrote `DEPLOY.md` with deploy steps, placeholder list, designer handoff, pre-launch checks, v2 roadmap

## Approach summary

Two parallel ultrathink subagents handled the heavy lifting:
- **Agent A (image migration):** read all 6 HTML files, extracted unique CDN URLs, downloaded with semantic filenames, generated SEO-friendly alt text per image, wrote `/assets/images/_url-mapping.json`. Result: 28/28 downloads, 0 failures.
- **Agent B (asset generation):** generated all non-HTML files (robots, sitemap, llms.txt × 2, netlify.toml, _redirects, vercel.json, 404, privacy, terms, favicon, plus reference JSON for meta-tags and JSON-LD schema). Result: 15 files, all validated.

Two deterministic Python scripts (`_dev/_migrate.py` and `_dev/_polish.py`) then applied the agents' outputs to the HTML in idempotent passes — image swaps, alt updates, meta injection, schema injection, nav fixes, CTA-button → anchor conversion, booking form wiring.

## Review

**What shipped:** A site that resolves, validates, and is wired for both hosts. SEO basics are complete (titles, descriptions, OG, Twitter, canonicals, sitemap, robots, JSON-LD). LLM/AI-search readiness is complete (`llms.txt`, `llms-full.txt`, AI crawlers explicitly allowed in `robots.txt`, structured data on every page). Hosting configs include CSP, HSTS, security headers, cache rules, and pretty URLs.

**What's owed before launch:**
1. Real domain (currently `mapoolsconstruction.co.za` placeholder — search-replace).
2. Real phone, email, address, geo coordinates.
3. Verified Google Business Profile rating data — DO NOT ship the placeholder `4.9 / 47` AggregateRating.
4. Designer (UNR) to deliver real photography to replace the 28 AI-generated PNG placeholders, plus 7 OG share images, plus favicon.png/apple-touch-icon.png.
5. Tighten CSP (drop `lh3.googleusercontent.com` whitelist) once images are confirmed migrated.

**Deferred to v2:** analytics (per user), local Tailwind build (drop CDN), FAQ content, per-suburb landing pages.

## Lessons captured

- Stitch CDN URLs are `lh3.googleusercontent.com/aida-public/...` — temporary; download every image before deploy or face guaranteed 404s. They serve PNG without an extension; verify with `file` and save with `.png`.
- Stitch sets a generic 2-word `alt=""` and a longer descriptive `data-alt=""` on every `<img>`. Use the mapping JSON's curated alt instead of either, and strip `data-alt` after.
- Stitch nav links use `href="#"` or `href="#sectionId"` placeholders that don't correspond to real anchors. A heuristic text→destination map (TEXT_MAP in `_polish.py`) catches the long tail.
- `<button>` elements without `onclick` handlers don't navigate. Convert prominent CTA buttons to `<a role="button">` while keeping the visual styling intact.
- For `LocalBusiness` schema on a pool service business there's no first-class type; `["LocalBusiness", "HomeAndConstructionBusiness"]` is the cleanest legitimate parent.
- `FAQPage` schema rich results were restricted by Google in Aug 2023 to government/healthcare — keep template ready but don't ship without real FAQ content visible on-page.
