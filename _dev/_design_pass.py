#!/usr/bin/env python3
"""Round 1 + Round 3 design-pass script: deterministic bulk fixes from the
multi-agent design audit.

Handles:
  - Nav: remove redundant Pools+Estates entries; rename Contact→About; ensure
    consistent destinations across all 6 main pages
  - CTA standardization: 'Book a Consult'/'Request a Quote'/'Submit Inquiry'/etc
    → 'Get a Free Quote' / unified action labels
  - Container width: max-w-[1440px] → max-w-[1280px]
  - Mobile padding: standalone px-20 → px-6 md:px-12 lg:px-20
  - Vertical spacing: py-32 md:py-48 / pb-48 / py-40 → consistent py-20 md:py-28 lg:py-32
  - Top padding: pt-40, pt-48, pt-[140px] → pt-32
  - Hero H1: text-display-xl → text-4xl md:text-5xl lg:text-display-xl
  - Strip orphan dark: classes (no toggle exists, half-implemented)
  - Contrast: nav text-slate-500 → text-[#0A2342]/85; footer text-slate-400 →
    text-slate-600; form placeholder text-outline/40 → text-slate-500;
    submit terms text-outline/50/[10px] → text-slate-600 text-xs;
    signature-stamp body gold #a78541 → #7a5e1f
  - WhatsApp float: bottom-6 right-6 → bottom-6 left-6 on book.html + services.html
  - Broken Material icons: concierge→support_agent; colors_spark→auto_awesome
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
         "book.html", "about.html", "privacy.html", "terms.html",
         "404.html", "thank-you.html"]

# ============================================================================
# 1) NAV: remove Pools + Estates rows; rename Contact→About; standardize hrefs
# ============================================================================
# Pattern: an <a> link line whose text is exactly "Pools" or "Estates" and
# whose href is /gallery.html — these are duplicates we delete entirely.
NAV_LINK_DELETE_RE = re.compile(
    r'^[ \t]*<a[^>]*href="/gallery\.html"[^>]*>(Pools|Estates)</a>[ \t]*\r?\n',
    re.IGNORECASE | re.MULTILINE,
)

# Rename the visible "Contact" link → "About", and force href to /about.html
def rename_contact_to_about(text):
    """Match an <a ...>Contact</a>, set href=/about.html, change inner text."""
    pat = re.compile(
        r'(<a\b[^>]*?)href="(/book\.html|/about\.html|#)"([^>]*>)\s*Contact\s*</a>',
        re.IGNORECASE | re.DOTALL,
    )
    return pat.sub(lambda m: m.group(1) + 'href="/about.html"' + m.group(3) + 'About</a>',
                   text)

# ============================================================================
# 2) CTA STANDARDIZATION
# ============================================================================
CTA_TEXT_PAIRS = [
    # Inside <button>/<a>/<span> visible text — be careful to match only inner text
    (">Book a Consult<",          ">Get a Free Quote<"),
    (">Book a Consultation<",     ">Get a Free Quote<"),
    (">Request a Consultation<",  ">Get a Free Quote<"),
    (">Request Consultation<",    ">Get a Free Quote<"),
    (">REQUEST CONSULTATION<",    ">GET A FREE QUOTE<"),
    (">Request a Quote<",         ">Get a Free Quote<"),
    (">Submit Inquiry<",          ">Send my request<"),
    (">SUBMIT INQUIRY<",          ">SEND MY REQUEST<"),
    (">Schedule a Consultation<", ">Get a Free Quote<"),
    (">Begin Consultation<",      ">Get a Free Quote<"),
    (">ENQUIRE ABOUT THIS PACKAGE<", ">GET A FREE QUOTE<"),
    # Trailing whitespace-tolerant variants
    (">Book a Consult\n",         ">Get a Free Quote\n"),
    (">Book a Consultation\n",    ">Get a Free Quote\n"),
]

# ============================================================================
# 3) LAYOUT: containers, padding, spacing, hero H1 responsive
# ============================================================================
LAYOUT_PAIRS = [
    # Standardise container width — pick 1280 as canonical
    ("max-w-[1440px]",    "max-w-[1280px]"),
    # Mobile-respect: standalone px-20 → responsive
    # Use word boundaries so we don't clobber md:px-20 etc.
    # Handled in regex below.
    # Vertical rhythm normalisation (least-to-most-specific)
    ("py-32 md:py-48",    "py-20 md:py-28 lg:py-32"),
    ("py-32 md:py-40",    "py-20 md:py-28 lg:py-32"),
    ("md:py-48",          "md:py-32"),
    ("pb-48",             "pb-20 md:pb-28 lg:pb-32"),
    ("py-48",             "py-20 md:py-28 lg:py-32"),
    ("py-40",             "py-20 md:py-28 lg:py-32"),
    ("mb-40 ",            "mb-20 md:mb-28 "),
    ("mb-32 ",            "mb-16 md:mb-24 "),
    # Top-padding under fixed floating nav — make consistent
    ("pt-[140px]",        "pt-32"),
    ("pt-48",             "pt-32"),
    ("pt-40",             "pt-32"),
    # Hero H1 responsive — only target visible H1 patterns (display-xl + serif family)
    ('text-display-xl font-display-xl',
     'text-4xl md:text-5xl lg:text-display-xl font-display-xl'),
    # Avoid double-applying if already responsive; idempotency check via marker
]

PX_20_STANDALONE_RE = re.compile(r'(?<![:\-])\bpx-20\b')

def fix_px_20(text):
    """Replace standalone `px-20` with responsive equivalent (not md:px-20 etc)."""
    return PX_20_STANDALONE_RE.sub("px-6 md:px-12 lg:px-20", text)

# Idempotency: don't double-apply the H1 responsive replacement
H1_ALREADY_RESPONSIVE = "text-4xl md:text-5xl lg:text-display-xl"

def fix_h1_responsive(text):
    """Make `text-display-xl font-display-xl` responsive — idempotent."""
    if H1_ALREADY_RESPONSIVE in text and "text-display-xl font-display-xl" not in text:
        return text  # already done
    return text.replace("text-display-xl font-display-xl",
                        "text-4xl md:text-5xl lg:text-display-xl font-display-xl")

# ============================================================================
# 4) STRIP ORPHAN dark: CLASSES (no toggle exists)
# ============================================================================
# Strip every `dark:xxx-xxx` token from class strings — they fire only on
# system-forced dark mode and produce inverted contrast in a half-built theme.
DARK_CLASS_RE = re.compile(r'\bdark:[A-Za-z0-9:_\[\]\#\-/.\(\)\,]+\b')

def strip_dark_classes(text):
    """Remove all dark:* utility classes."""
    # Keep CSS rules `.dark { ... }` in <style> blocks (we don't have any) —
    # this only targets the utility classes inside class="..." attributes.
    new = DARK_CLASS_RE.sub("", text)
    # Collapse double-spaces inside class attrs that resulted
    new = re.sub(r'class="\s+', 'class="', new)
    new = re.sub(r'\s+"', '"', new)
    new = re.sub(r'class="([^"]*?)\s{2,}([^"]*?)"',
                 lambda m: f'class="{m.group(1)} {m.group(2)}"'.replace("  ", " "),
                 new)
    return new

# ============================================================================
# 5) CONTRAST FIXES
# ============================================================================
CONTRAST_PAIRS = [
    # Nav inactive links — slate-500 over translucent white glass fails on photos
    ("text-slate-500 hover:text-[#0A2342]",
     "text-[#0A2342]/85 hover:text-[#0A2342]"),
    # Footer & secondary muted text
    ("text-slate-400 hover:text-[#0A2342]",
     "text-slate-600 hover:text-[#0A2342]"),
    ("text-slate-400 leading-relaxed",
     "text-slate-600 leading-relaxed"),
    ("text-slate-400 max-w-xs",
     "text-slate-600 max-w-xs"),
    ("text-slate-400 max-w-sm",
     "text-slate-600 max-w-sm"),
    ("text-slate-400\"",  "text-slate-600\""),
    ("text-slate-400 ",   "text-slate-600 "),
    # Form placeholder
    ("placeholder:text-outline/40",  "placeholder:text-slate-500"),
    # Submit terms microcopy
    ("text-outline/50 ",             "text-slate-600 "),
    ("text-[10px]",                  "text-xs"),
    # Signature-stamp body color (gold→darker gold for AA on white)
    ("color: #a78541;",              "color: #7a5e1f;"),
    # Decorative outline-variant strip on contact icons (now anchors get colour)
    ("text-outline ",                "text-slate-500 "),
]

# ============================================================================
# 6) WHATSAPP FLOAT — flip side on book + services to avoid overlap
# ============================================================================
def move_wa_float_left(text):
    """For book.html + services.html only: bottom-6 right-6 → bottom-6 left-6
    inside the AE:WA-FLOAT block."""
    return text.replace(
        'fixed bottom-6 right-6 z-[100]',
        'fixed bottom-6 left-6 z-[100]',
    )

# ============================================================================
# 7) BROKEN MATERIAL ICONS
# ============================================================================
ICON_PAIRS = [
    # services.html: data-icon="sparkles" with text "colors_spark" — both wrong
    ('data-icon="sparkles">colors_spark</span>',
     'data-icon="auto_awesome">auto_awesome</span>'),
    # index.html: `concierge` is not a valid Material Symbol
    ('data-icon="concierge">concierge</span>',
     'data-icon="support_agent">support_agent</span>'),
    # Stragglers
    ('>colors_spark<',  '>auto_awesome<'),
    ('>concierge<',     '>support_agent<'),
]

# ============================================================================
# Apply
# ============================================================================
report = []

for page in PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    original = p.read_text(encoding="utf-8")
    text = original
    counters = {"nav": 0, "cta": 0, "layout": 0, "px20": 0, "h1": 0,
                "dark": 0, "contrast": 0, "wa": 0, "icon": 0}

    # 1) Nav cleanup
    pre = text
    text = NAV_LINK_DELETE_RE.sub("", text)
    counters["nav"] += pre.count('>Pools</a>') + pre.count('>Estates</a>') - \
                       (text.count('>Pools</a>') + text.count('>Estates</a>'))
    pre = text
    text = rename_contact_to_about(text)
    if text != pre:
        counters["nav"] += pre.count('>Contact</a>')

    # 2) CTA standardisation
    for old, new in CTA_TEXT_PAIRS:
        if old in text:
            counters["cta"] += text.count(old)
            text = text.replace(old, new)

    # 3) Layout
    for old, new in LAYOUT_PAIRS:
        if old in text:
            counters["layout"] += text.count(old)
            text = text.replace(old, new)
    pre = text
    text = fix_px_20(text)
    counters["px20"] = pre.count("px-20") - text.count("px-20") - \
                       (pre.count("md:px-20") - text.count("md:px-20")) - \
                       (pre.count("lg:px-20") - text.count("lg:px-20"))
    pre = text
    text = fix_h1_responsive(text)
    if text != pre:
        counters["h1"] += 1

    # 4) dark: cleanup
    pre = text
    text = strip_dark_classes(text)
    counters["dark"] = len(DARK_CLASS_RE.findall(pre))

    # 5) Contrast
    for old, new in CONTRAST_PAIRS:
        if old in text:
            counters["contrast"] += text.count(old)
            text = text.replace(old, new)

    # 6) WhatsApp float side-flip — only on book + services
    if page in ("book.html", "services.html"):
        pre = text
        text = move_wa_float_left(text)
        if text != pre:
            counters["wa"] += 1

    # 7) Broken icons
    for old, new in ICON_PAIRS:
        if old in text:
            counters["icon"] += text.count(old)
            text = text.replace(old, new)

    if text != original:
        p.write_text(text, encoding="utf-8")
        report.append((page, counters))

# Print
print(f"{'PAGE':22s}  nav  cta  layout  px20  h1  dark  contrast  wa  icon")
totals = {k: 0 for k in ("nav","cta","layout","px20","h1","dark","contrast","wa","icon")}
for page, c in report:
    for k in totals: totals[k] += c[k]
    print(f"{page:22s}  {c['nav']:>3}  {c['cta']:>3}  {c['layout']:>6}  {c['px20']:>4}  {c['h1']:>2}  {c['dark']:>4}  {c['contrast']:>8}  {c['wa']:>2}  {c['icon']:>4}")
print(f"{'TOTAL':22s}  {totals['nav']:>3}  {totals['cta']:>3}  {totals['layout']:>6}  {totals['px20']:>4}  {totals['h1']:>2}  {totals['dark']:>4}  {totals['contrast']:>8}  {totals['wa']:>2}  {totals['icon']:>4}")
