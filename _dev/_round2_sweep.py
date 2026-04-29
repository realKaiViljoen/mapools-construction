#!/usr/bin/env python3
"""Round 2 sitewide sweep: apply the landing-page design system updates to
every page so the whole site feels coherent.

Mechanical changes (per page):
  1) Drop Noto Serif from Google Fonts link → keep Manrope only
  2) Update Tailwind config fontFamily tokens (Noto Serif → Manrope)
  3) Strip dead CSS rules from inline <style>: .signature-stamp,
     .luxury-hover, .dark .backdrop-glass, .signature-seal
  4) Add :root brand vars + pb-safe utility to inline <style>
  5) Update <body> class: add pb-20 md:pb-0 (sticky bar clearance)
  6) Add AE:STICKY-CTA block before AE:WA-FLOAT (mobile-only sticky bar)
  7) Modify AE:WA-FLOAT to use hidden md:flex (desktop-only floating bubble)
  8) Strip gold-accent utility classes from body content where harmless
  9) Idempotent — re-runs produce no diff
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
         "book.html", "about.html", "privacy.html", "terms.html",
         "404.html", "thank-you.html"]

# ============================================================================
# 1) Drop Noto Serif from Google Fonts link
# ============================================================================
NEW_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>'
)
FONT_LINK_RE = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?family=[^"]*?(Manrope|Noto[+ ]Serif)[^"]*"\s+rel="stylesheet"/>',
    re.IGNORECASE,
)

def fix_font_link(txt):
    # If the new preconnect block is already present, skip
    if 'rel="preconnect" href="https://fonts.googleapis.com"' in txt:
        # Just delete any standalone Manrope+NotoSerif link still in place
        return FONT_LINK_RE.sub('', txt, count=1)
    return FONT_LINK_RE.sub(NEW_FONT_LINK, txt, count=1)

# ============================================================================
# 2) Tailwind config — fontFamily tokens to Manrope
# ============================================================================
def fix_tailwind_fonts(txt):
    # Replace any "Noto Serif" → "Manrope" inside the Tailwind config block
    # Conservative: only inside script id="tailwind-config"
    m = re.search(r'<script id="tailwind-config">(.*?)</script>', txt, re.DOTALL)
    if not m:
        return txt
    cfg = m.group(1)
    new_cfg = cfg.replace('"Noto Serif"', '"Manrope"').replace('Noto Serif', 'Manrope')
    # Also override the default `serif` token to Manrope so font-serif → Manrope
    if '"serif":' not in new_cfg and '"fontFamily":' in new_cfg:
        new_cfg = new_cfg.replace(
            '"fontFamily": {',
            '"fontFamily": {"sans": ["Manrope","system-ui","sans-serif"],"serif": ["Manrope","system-ui","sans-serif"],',
            1,
        )
    if new_cfg != cfg:
        txt = txt.replace(cfg, new_cfg, 1)
    return txt

# ============================================================================
# 3 + 4) Strip dead CSS rules; ensure :root vars + .pb-safe present
# ============================================================================
DEAD_CSS_RULES = [
    re.compile(r'\.signature-stamp\s*\{[^}]*\}', re.DOTALL),
    re.compile(r'\.luxury-hover[^{]*\{[^}]*\}', re.DOTALL),
    re.compile(r'\.dark\s+\.backdrop-glass\s*\{[^}]*\}', re.DOTALL),
    re.compile(r'\.signature-seal[^{]*\{[^}]*\}', re.DOTALL),
    re.compile(r'\.signature-seal::after\s*\{[^}]*\}', re.DOTALL),
    re.compile(r'\.btn-primary-luxury[^{]*\{[^}]*\}', re.DOTALL),
]
ROOT_VARS_BLOCK = (
    "        :root { --brand-navy: #0A2342; --brand-green: #25D366; --brand-cyan: #2BA8B8; }\n"
    "        body { font-family: 'Manrope', system-ui, sans-serif; }\n"
)
PB_SAFE_BLOCK = (
    "        /* iOS safe-area for sticky bottom bar */\n"
    "        .pb-safe { padding-bottom: env(safe-area-inset-bottom, 0); }\n"
)

def fix_inline_style(txt):
    style_re = re.compile(r'<style>(.*?)</style>', re.DOTALL)
    m = style_re.search(txt)
    if not m:
        return txt
    style = m.group(1)
    new_style = style
    # Strip dead rules
    for pat in DEAD_CSS_RULES:
        new_style = pat.sub('', new_style)
    # Inject :root vars + body font if missing
    if ':root { --brand-navy' not in new_style:
        new_style = ROOT_VARS_BLOCK + new_style
    # Inject pb-safe utility if missing
    if '.pb-safe' not in new_style:
        new_style = new_style.rstrip() + "\n" + PB_SAFE_BLOCK
    # Collapse whitespace artifacts left by removed rules
    new_style = re.sub(r'\n\s*\n\s*\n+', '\n\n', new_style)
    if new_style != style:
        txt = txt.replace(m.group(0), '<style>' + new_style + '</style>', 1)
    return txt

# ============================================================================
# 5) <body> class — add pb-20 md:pb-0
# ============================================================================
BODY_RE = re.compile(r'<body\b([^>]*)>')

def fix_body(txt):
    m = BODY_RE.search(txt)
    if not m:
        return txt
    attrs = m.group(1)
    if 'pb-20 md:pb-0' in attrs:
        return txt
    # Add to existing class= or insert new class attribute
    if 'class=' in attrs:
        new_attrs = re.sub(
            r'class="([^"]*)"',
            lambda mm: f'class="{mm.group(1)} pb-20 md:pb-0"',
            attrs, count=1,
        )
    else:
        new_attrs = attrs + ' class="pb-20 md:pb-0"'
    return txt.replace(m.group(0), f'<body{new_attrs}>', 1)

# ============================================================================
# 6 + 7) Sticky bottom CTA + hide floating WA on mobile
# ============================================================================
STICKY_START = "<!-- AE:STICKY-CTA:START -->"
STICKY_END   = "<!-- AE:STICKY-CTA:END -->"
STICKY_BLOCK = f"""{STICKY_START}
<div class="md:hidden fixed bottom-0 inset-x-0 z-[90] bg-white border-t border-slate-200 shadow-[0_-10px_30px_rgba(10,35,66,0.12)] grid grid-cols-2 pb-safe">
<a class="flex items-center justify-center gap-2 bg-[#0A2342] text-white py-4 text-sm font-bold tracking-wide uppercase active:scale-95 transition-transform" href="tel:+27787122157">
<span class="material-symbols-outlined">call</span>
Call
</a>
<a class="flex items-center justify-center gap-2 bg-[#25D366] text-white py-4 text-sm font-bold tracking-wide uppercase active:scale-95 transition-transform" href="https://wa.me/27656430603?text=Hi%20Ma%20Pools%20Construction%2C%20I%27d%20like%20a%20free%20quote." target="_blank" rel="noopener">
<span class="material-symbols-outlined">chat</span>
WhatsApp
</a>
</div>
{STICKY_END}"""

def add_sticky(txt):
    # Idempotent: strip any prior block first
    txt = re.sub(re.escape(STICKY_START) + r".*?" + re.escape(STICKY_END),
                 "", txt, flags=re.DOTALL)
    # Insert before AE:WA-FLOAT:START if it exists, else before </body>
    if "<!-- AE:WA-FLOAT:START -->" in txt:
        txt = txt.replace("<!-- AE:WA-FLOAT:START -->",
                          STICKY_BLOCK + "\n<!-- AE:WA-FLOAT:START -->", 1)
    elif "</body>" in txt:
        txt = txt.replace("</body>", STICKY_BLOCK + "\n</body>", 1)
    return txt

def hide_wa_float_on_mobile(txt):
    """Add hidden md:flex (or md:inline-flex) to the WA-float anchor."""
    # Find the WA-float anchor and ensure it has hidden md:flex
    m = re.search(
        r'(<!-- AE:WA-FLOAT:START -->\s*<a\b[^>]*?\bclass=")([^"]*)(")',
        txt, re.DOTALL,
    )
    if not m:
        return txt
    classes = m.group(2)
    if "hidden md:flex" in classes:
        return txt
    # Replace existing 'flex' positioning with 'hidden md:flex'
    new_classes = classes.replace("flex items-center justify-center",
                                  "hidden md:flex items-center justify-center")
    if new_classes == classes:
        # Fallback: prepend
        new_classes = "hidden md:flex " + classes
    return txt.replace(m.group(0), m.group(1) + new_classes + m.group(3), 1)

# ============================================================================
# 8) Strip gold-accent utility classes from body content (light cleanup)
# ============================================================================
GOLD_PAIRS = [
    # decorative gold dividers
    ("group-hover:bg-tertiary-fixed-dim", "group-hover:bg-[#0A2342]/30"),
    ("text-tertiary-fixed-dim",           "text-[#25D366]"),
    ("border-tertiary-fixed-dim",         "border-[#0A2342]/20"),
    ("bg-tertiary-fixed-dim/10",          "bg-[#25D366]/10"),
    ("bg-tertiary-fixed-dim/20",          "bg-[#25D366]/20"),
    ("text-on-tertiary-container",        "text-[#0A2342]/70"),
    ("bg-on-tertiary-container",          "bg-[#0A2342]"),
]

def strip_gold_classes(txt):
    n = 0
    for old, new in GOLD_PAIRS:
        if old in txt:
            n += txt.count(old)
            txt = txt.replace(old, new)
    return txt, n

# ============================================================================
# Run
# ============================================================================
print(f"{'PAGE':22s}  fonts  tw-cfg  style  body  sticky  wa-flt  gold")
totals = dict(fonts=0, tw_cfg=0, style=0, body=0, sticky=0, wa_flt=0, gold=0)

for page in PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    original = p.read_text(encoding="utf-8")
    txt = original
    counts = dict(fonts=0, tw_cfg=0, style=0, body=0, sticky=0, wa_flt=0, gold=0)

    pre = txt; txt = fix_font_link(txt);    counts["fonts"]  = 1 if pre != txt else 0
    pre = txt; txt = fix_tailwind_fonts(txt); counts["tw_cfg"] = 1 if pre != txt else 0
    pre = txt; txt = fix_inline_style(txt); counts["style"]  = 1 if pre != txt else 0
    pre = txt; txt = fix_body(txt);         counts["body"]   = 1 if pre != txt else 0
    pre = txt; txt = add_sticky(txt);       counts["sticky"] = 1 if pre != txt else 0
    pre = txt; txt = hide_wa_float_on_mobile(txt); counts["wa_flt"] = 1 if pre != txt else 0
    pre = txt; txt, gn = strip_gold_classes(txt); counts["gold"] = gn

    if txt != original:
        p.write_text(txt, encoding="utf-8")

    print(f"  {page:22s}  {counts['fonts']:>5}  {counts['tw_cfg']:>6}  {counts['style']:>5}  {counts['body']:>4}  {counts['sticky']:>6}  {counts['wa_flt']:>6}  {counts['gold']:>4}")
    for k in totals: totals[k] += counts[k]

print(f"  {'TOTAL':22s}  {totals['fonts']:>5}  {totals['tw_cfg']:>6}  {totals['style']:>5}  {totals['body']:>4}  {totals['sticky']:>6}  {totals['wa_flt']:>6}  {totals['gold']:>4}")
