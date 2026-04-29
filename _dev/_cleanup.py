#!/usr/bin/env python3
"""Cleanup pass: strip fictional content (testimonials + team), add real
contact links, fix OG image refs. Idempotent (markers protect each insert)."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
         "book.html", "about.html", "privacy.html", "terms.html",
         "404.html", "thank-you.html"]

# ---------------------------------------------------------------------------
# 1) testimonials.html — strip review JSON-LD; replace cards with placeholder
# ---------------------------------------------------------------------------
def clean_testimonials():
    p = ROOT / "testimonials.html"
    txt = p.read_text(encoding="utf-8")

    # 1a) Empty the review array in the testimonials_page JSON-LD
    txt = re.sub(
        r'"review"\s*:\s*\[\s*(?:\{.*?\}\s*,?\s*)+\s*\]',
        '"review": []',
        txt, flags=re.DOTALL,
    )

    # 1b) Replace visible <main> content with a clean placeholder (no fabrications)
    placeholder_main = """<main class="pt-48 pb-32">
<section class="max-w-[1440px] mx-auto px-6 md:px-20 mb-24">
<div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-end">
<div>
<span class="font-label-upper text-on-tertiary-container uppercase mb-4 block">Client Feedback</span>
<h1 class="font-display-xl text-display-xl text-primary leading-none mb-8">Building a track record.</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-md">
Ma Pools Construction is a working pool construction and maintenance business serving Gauteng. We let our work speak first and publish verified customer feedback here as it comes in.
</p>
</div>
<div class="flex flex-col items-end">
<div class="signature-stamp">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">verified</span>
DIRECTOR-LED SERVICE
</div>
</div>
</div>
</section>

<section class="max-w-[1280px] mx-auto px-6 md:px-20 mb-32">
<div class="bg-white p-12 md:p-20 rounded-3xl border border-slate-100 shadow-sm text-center">
<span class="material-symbols-outlined text-primary-container text-5xl mb-8">format_quote</span>
<h2 class="font-headline-lg text-headline-lg text-primary mb-6">Our reviews are coming.</h2>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto mb-12">
If we've worked on your pool, paving, plumbing, or jacuzzi — we&#39;d be grateful for your honest review on Google. We&#39;ll publish verified customer feedback on this page as it arrives.
</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
<a class="bg-primary-container text-white px-8 py-4 rounded-full font-serif text-sm tracking-wide uppercase hover:scale-[1.02] transition-transform" href="/book.html" role="button">Request a Quote</a>
<a class="bg-[#25D366] text-white px-8 py-4 rounded-full font-serif text-sm tracking-wide uppercase hover:scale-[1.02] transition-transform inline-flex items-center gap-2" href="https://wa.me/27656430603" target="_blank" rel="noopener" role="button"><span class="material-symbols-outlined">chat</span>WhatsApp 065 643 0603</a>
<a class="border border-primary text-primary px-8 py-4 rounded-full font-serif text-sm tracking-wide uppercase hover:bg-primary hover:text-white transition-colors" href="tel:+27787122157" role="button">Call 078 712 2157</a>
</div>
</div>
</section>
</main>"""
    txt = re.sub(r'<main\b[^>]*>.*?</main>', placeholder_main, txt,
                 count=1, flags=re.DOTALL)
    p.write_text(txt, encoding="utf-8")
    return "testimonials.html: stripped reviews; replaced main with placeholder"

# ---------------------------------------------------------------------------
# 2) about.html — drop fictional team; strip "since 2014" mentions; clean schema
# ---------------------------------------------------------------------------
def clean_about():
    p = ROOT / "about.html"
    txt = p.read_text(encoding="utf-8")

    # 2a) Strip "Since 2014" / "since 2014" / "for over a decade"-style claims
    txt = re.sub(r'Since\s+2014', 'Locally Owned & Operated', txt)
    txt = re.sub(r'since\s+2014', 'in our community', txt)
    txt = re.sub(r'for over a decade,\s*', '', txt, flags=re.IGNORECASE)
    txt = re.sub(r'company history since 2014, ', '', txt, flags=re.IGNORECASE)
    txt = re.sub(r'\| Gauteng&#x27;s Premier Pool Care Firm Since 2014',
                 '| Director-led pool construction & care, Gauteng', txt)
    txt = re.sub(r'15 years of estate management expertise with a focus on chemical thermodynamic balance\.',
                 'Founder and operating director — leading every project from new pool builds to renovations, plumbing, and pool care across Gauteng.', txt)

    # 2b) Strip the 2 fictional team-member cards (Sarah Mokoena + Pieter van Wyk)
    # Pattern matches each <!-- Member 2 / 3 --> block through to its </div>.
    txt = re.sub(
        r'<!-- Member 2 -->.*?<!-- Member 3 -->.*?</div>\s*</div>\s*</div>',
        '',
        txt, count=1, flags=re.DOTALL,
    )
    # Also tighten the section header
    txt = txt.replace(
        '<h2 class="text-4xl font-semibold text-primary mb-4">Our Elite Technicians</h2>',
        '<h2 class="text-4xl font-semibold text-primary mb-4">Director-led service.</h2>'
    )
    txt = txt.replace(
        '<p class="text-lg text-on-surface-variant max-w-xl mx-auto">Vetted professionals dedicated to the art of aquatic preservation.</p>',
        '<p class="text-lg text-on-surface-variant max-w-xl mx-auto">Every project at Ma Pools Construction is led personally by our founding director, with a trusted field team supporting installations and on-site work.</p>'
    )
    # Make the single team grid centred (no longer a 3-col layout)
    txt = txt.replace(
        '<div class="grid grid-cols-1 md:grid-cols-3 gap-8">',
        '<div class="max-w-md mx-auto">',
        1,
    )

    # 2c) Strip employee schema entries for Sarah Mokoena / Pieter van Wyk
    txt = re.sub(
        r'\s*,\s*\{\s*"@type"\s*:\s*"Person"\s*,\s*"name"\s*:\s*"Sarah Mokoena"[^}]*\}',
        '', txt, flags=re.DOTALL,
    )
    txt = re.sub(
        r'\s*,\s*\{\s*"@type"\s*:\s*"Person"\s*,\s*"name"\s*:\s*"Pieter van Wyk"[^}]*\}',
        '', txt, flags=re.DOTALL,
    )

    p.write_text(txt, encoding="utf-8")
    return "about.html: removed 2 fictional team members; stripped 'since 2014'"

# ---------------------------------------------------------------------------
# 3) Add floating WhatsApp button to every page (idempotent via marker)
# ---------------------------------------------------------------------------
WA_FLOAT_START = "<!-- AE:WA-FLOAT:START -->"
WA_FLOAT_END   = "<!-- AE:WA-FLOAT:END -->"
WA_FLOAT = f"""{WA_FLOAT_START}
<a href="https://wa.me/27656430603?text=Hi%20Ma%20Pools%20Construction%2C%20I%27d%20like%20to%20book%20a%20pool%20service" target="_blank" rel="noopener noreferrer" aria-label="Chat with Ma Pools Construction on WhatsApp" class="fixed bottom-6 right-6 z-[100] bg-[#25D366] hover:bg-[#1ebe57] text-white rounded-full w-14 h-14 flex items-center justify-center shadow-2xl hover:scale-110 transition-transform duration-300" style="box-shadow: 0 10px 30px rgba(37,211,102,0.45);">
<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 0 1-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 0 1 8.413 3.488 11.824 11.824 0 0 1 3.48 8.414c-.003 6.554-5.338 11.89-11.893 11.89a11.9 11.9 0 0 1-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.149-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.521.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>
</a>
{WA_FLOAT_END}"""

def inject_wa_float(txt: str) -> str:
    """Inject floating WhatsApp button right before </body>. Idempotent."""
    txt = re.sub(re.escape(WA_FLOAT_START) + r".*?" + re.escape(WA_FLOAT_END),
                 "", txt, flags=re.DOTALL)
    if "</body>" not in txt:
        return txt
    return txt.replace("</body>", WA_FLOAT + "\n</body>", 1)

# ---------------------------------------------------------------------------
# 4) Footer contact block (idempotent via marker)
# ---------------------------------------------------------------------------
FOOTER_START = "<!-- AE:FOOTER-CONTACT:START -->"
FOOTER_END   = "<!-- AE:FOOTER-CONTACT:END -->"
FOOTER_CONTACT = f"""{FOOTER_START}
<div class="max-w-[1280px] mx-auto mt-12 pt-12 border-t border-slate-200 dark:border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-10 font-serif text-sm antialiased text-slate-500 dark:text-slate-400">
<div>
<p class="font-label-upper uppercase tracking-widest text-[11px] text-[#0A2342] dark:text-slate-300 mb-3">Visit</p>
<p class="leading-relaxed">Ma Pools Construction<br/>331B Utekwane Street, Zone 7<br/>Meadowlands, 1852<br/>Soweto, Gauteng</p>
</div>
<div>
<p class="font-label-upper uppercase tracking-widest text-[11px] text-[#0A2342] dark:text-slate-300 mb-3">Talk</p>
<p class="leading-relaxed">
<a class="block hover:text-[#0A2342] dark:hover:text-white" href="https://wa.me/27656430603" target="_blank" rel="noopener">WhatsApp 065 643 0603</a>
<a class="block hover:text-[#0A2342] dark:hover:text-white" href="tel:+27787122157">Call 078 712 2157</a>
<a class="block hover:text-[#0A2342] dark:hover:text-white" href="mailto:mapoolsconstruction@gmail.com">mapoolsconstruction@gmail.com</a>
</p>
</div>
<div>
<p class="font-label-upper uppercase tracking-widest text-[11px] text-[#0A2342] dark:text-slate-300 mb-3">Director</p>
<p class="leading-relaxed">Mkhacani Amos Chauke<br/>Founder &amp; Operating Director</p>
</div>
</div>
{FOOTER_END}"""

def inject_footer_contact(txt: str) -> str:
    """Inject contact block immediately before </footer>. Idempotent."""
    txt = re.sub(re.escape(FOOTER_START) + r".*?" + re.escape(FOOTER_END),
                 "", txt, flags=re.DOTALL)
    if "</footer>" not in txt:
        return txt
    return txt.replace("</footer>", FOOTER_CONTACT + "\n</footer>", 1)

# ---------------------------------------------------------------------------
# 5) Fix OG image refs to point to existing real images
# ---------------------------------------------------------------------------
OG_IMAGE_PER_PAGE = {
    "index.html":        "/assets/images/hero-luxury-infinity-pool-gauteng.png",
    "services.html":     "/assets/images/service-weekly-maintenance-luxury-pool.png",
    "gallery.html":      "/assets/images/gallery-azure-pool-deck-loungers.png",
    "testimonials.html": "/assets/images/testimonial-obsidian-residence-infinity-pool.png",
    "book.html":         "/assets/images/book-hero-rectangular-estate-pool.png",
    "about.html":        "/assets/images/about-hero-minimalist-infinity-pool-sunset.png",
    "privacy.html":      "/assets/images/hero-luxury-infinity-pool-gauteng.png",
    "terms.html":        "/assets/images/hero-luxury-infinity-pool-gauteng.png",
    "404.html":          "/assets/images/hero-luxury-infinity-pool-gauteng.png",
    "thank-you.html":    "/assets/images/hero-luxury-infinity-pool-gauteng.png",
}
DOMAIN = "https://www.mapoolsconstruction.co.za"

def fix_og_image(txt: str, page: str) -> str:
    """Replace any og-aquaestate-*.jpg or og-mapoolsconstruction-*.jpg ref with
    the page-appropriate real image."""
    new_path = OG_IMAGE_PER_PAGE.get(page, OG_IMAGE_PER_PAGE["index.html"])
    new_full = DOMAIN + new_path
    # Replace any reference to /assets/images/og-*.jpg with new_full or new_path
    txt = re.sub(
        r'(?:https?://[^"\s]*?)?/assets/images/og-[a-z\-]*\.jpg',
        new_full,
        txt,
    )
    return txt

# ---------------------------------------------------------------------------
# Run everything
# ---------------------------------------------------------------------------
report = []
report.append(clean_testimonials())
report.append(clean_about())

for page in PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    txt = fix_og_image(txt, page)
    txt = inject_wa_float(txt)
    txt = inject_footer_contact(txt)
    p.write_text(txt, encoding="utf-8")

print("Cleanup applied across all pages:")
print("  - WhatsApp floating button (every page)")
print("  - Footer contact block (every page)")
print("  - OG image refs swapped to real existing PNG hero images")
print()
for line in report:
    print(f"  - {line}")
