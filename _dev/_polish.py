#!/usr/bin/env python3
"""Final polish pass: catch remaining href="#", convert CTA buttons to anchors,
wire the booking form for Netlify Forms, generate thank-you.html.
"""
import re, html
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
         "book.html", "about.html", "404.html", "privacy.html", "terms.html"]

# Same TEXT_MAP as _migrate.py — heuristic for inner text → destination
TEXT_MAP = {
    "philosophy": "/about.html", "sustainability": "/about.html",
    "press": "/about.html", "careers": "/about.html", "team": "/about.html",
    "legal": "/terms.html", "privacy": "/privacy.html",
    "privacy policy": "/privacy.html", "terms": "/terms.html",
    "terms of service": "/terms.html", "contact": "/about.html",
    "contact us": "/about.html", "book": "/book.html",
    "book a consult": "/book.html", "book a consultation": "/book.html",
    "request a consultation": "/book.html",
    "request exclusive consult": "/book.html",
    "schedule a consultation": "/book.html", "services": "/services.html",
    "all services": "/services.html", "view all packages": "/services.html",
    "view all services": "/services.html",
    "explore the full collection": "/gallery.html",
    "explore portfolio": "/gallery.html",
    "view portfolio": "/gallery.html",
    "view collection": "/gallery.html",
    "explore the gallery": "/gallery.html",
    "view gallery": "/gallery.html",
    "view the gallery": "/gallery.html",
    "see all projects": "/gallery.html",
    "see more": "/gallery.html",
    "view full case study": "/gallery.html",
    "read full case study": "/gallery.html",
    "read the case study": "/gallery.html",
    "read more": "/testimonials.html",
    "view more testimonials": "/testimonials.html",
    "see all testimonials": "/testimonials.html",
    "gallery": "/gallery.html", "estates": "/gallery.html",
    "our portfolio": "/gallery.html", "portfolio": "/gallery.html",
    "testimonials": "/testimonials.html",
    "client testimonials": "/testimonials.html",
    "about": "/about.html", "about us": "/about.html",
    "home": "/index.html", "aqua estate": "/index.html",
    "pools": "/gallery.html",
}

# Buttons whose visible text contains any of these phrases → wrap as link to dest
BUTTON_CTA = [
    ("book a consult", "/book.html"),
    ("book a consultation", "/book.html"),
    ("request a consultation", "/book.html"),
    ("request exclusive consult", "/book.html"),
    ("request consult", "/book.html"),
    ("schedule a consultation", "/book.html"),
    ("schedule consultation", "/book.html"),
    ("our portfolio", "/gallery.html"),
    ("view portfolio", "/gallery.html"),
    ("view gallery", "/gallery.html"),
    ("view all packages", "/services.html"),
    ("view all services", "/services.html"),
    ("explore the gallery", "/gallery.html"),
    ("explore portfolio", "/gallery.html"),
    ("explore services", "/services.html"),
    ("learn more", "/services.html"),
    ("get in touch", "/about.html"),
    ("contact us", "/about.html"),
]

def fix_remaining_anchors(txt: str) -> tuple[str, int]:
    """Catch any <a ... href='#' ...>TEXT</a> regardless of attribute order."""
    count = 0
    # Iterate: find every <a ...> ... </a>; check for href="#"; replace if mappable
    a_re = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.IGNORECASE | re.DOTALL)
    href_hash_re = re.compile(r'''\bhref\s*=\s*(["'])#\1''', re.IGNORECASE)

    def repl(m):
        nonlocal count
        attrs, inner = m.group(1), m.group(2)
        if not href_hash_re.search(attrs):
            return m.group(0)
        text = re.sub(r"<[^>]+>", " ", inner)
        text = re.sub(r"\s+", " ", text).strip().lower()
        # Trim trailing material-icons or punctuation
        text = re.sub(r"\s*(arrow_forward|arrow_outward|chevron_right|north_east).*$", "", text)
        if text in TEXT_MAP:
            new_attrs = href_hash_re.sub(f'href="{TEXT_MAP[text]}"', attrs)
            count += 1
            return f"<a{new_attrs}>{inner}</a>"
        return m.group(0)
    txt = a_re.sub(repl, txt)
    return txt, count

def convert_cta_buttons(txt: str) -> tuple[str, int]:
    """Convert CTA <button>...</button> → <a href="..." role="button">...</a>."""
    count = 0
    btn_re = re.compile(r'<button\b([^>]*)>(.*?)</button>', re.IGNORECASE | re.DOTALL)

    def repl(m):
        nonlocal count
        attrs, inner = m.group(1), m.group(2)
        # Skip submit buttons (real form submits)
        if re.search(r'\btype\s*=\s*["\']submit["\']', attrs, re.IGNORECASE):
            return m.group(0)
        text = re.sub(r"<[^>]+>", " ", inner)
        text = re.sub(r"\s+", " ", text).strip().lower()
        for phrase, dest in BUTTON_CTA:
            if phrase in text:
                # Strip type=button if present, keep classes/data-attrs
                clean_attrs = re.sub(r'\btype\s*=\s*["\'][^"\']*["\']', "",
                                     attrs, flags=re.IGNORECASE).strip()
                count += 1
                # role=button improves a11y for screen readers since visually it's a button
                return (f'<a{("" if clean_attrs.startswith(" ") else " ")}'
                        f'{clean_attrs} href="{dest}" role="button">{inner}</a>')
        return m.group(0)

    txt = btn_re.sub(repl, txt)
    return txt, count

# === Run anchor + button polish across all 9 pages ===
totals = {"anchors": 0, "buttons": 0}
for page in PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    txt, a_n = fix_remaining_anchors(txt)
    txt, b_n = convert_cta_buttons(txt)
    p.write_text(txt, encoding="utf-8")
    totals["anchors"] += a_n
    totals["buttons"] += b_n
    print(f"  {page:25s} extra_anchors_fixed={a_n:3d}  cta_buttons_converted={b_n:3d}")

# === Wire the booking form in book.html ===
print()
print("Wiring booking form for Netlify…")
book = ROOT / "book.html"
btxt = book.read_text(encoding="utf-8")

# 1. Add Netlify attributes to the <form> tag (idempotent)
form_open = re.search(r'<form\b[^>]*>', btxt)
if form_open:
    old = form_open.group(0)
    if "data-netlify" not in old:
        # Strip any existing class attr we want to keep, augment attrs
        new = old[:-1]  # drop closing >
        new += (' name="consultation"'
                ' method="POST"'
                ' data-netlify="true"'
                ' data-netlify-honeypot="bot-field"'
                ' action="/thank-you.html"')
        new += ">"
        # Hidden form-name + honeypot fields injected immediately after <form>
        injection = (
            '\n<input type="hidden" name="form-name" value="consultation"/>'
            '\n<p class="hidden" aria-hidden="true" style="display:none">'
            '<label>Don\'t fill this out if you\'re human: '
            '<input name="bot-field"/></label></p>'
        )
        btxt = btxt.replace(old, new + injection, 1)
        print("  added Netlify attrs + hidden fields")
    else:
        print("  form already wired — skipped")
else:
    print("  WARNING: no <form> tag found in book.html")

# 2. Ensure each form input has a name attr (already does per inspection — verify)
missing = [m for m in re.finditer(r'<(input|select|textarea)\b([^>]*)>', btxt)
           if 'type="hidden"' not in m.group(0)
           and 'name=' not in m.group(2)
           and 'bot-field' not in m.group(0)]
if missing:
    print(f"  WARNING: {len(missing)} form fields missing name= attr")

# 3. Ensure submit button is a real submit, not the converted <a> CTA.
# Our convert_cta_buttons skipped type=submit, so the form's submit button is intact.
# Sanity-check: form must contain a submit element.
form_block = re.search(r'<form\b[^>]*>(.*?)</form>', btxt, re.DOTALL)
if form_block and 'type="submit"' not in form_block.group(1):
    print("  WARNING: form has no submit button after polish")

book.write_text(btxt, encoding="utf-8")

# === Generate thank-you.html ===
ty_path = ROOT / "thank-you.html"
# Reuse 404.html's chrome as the basis to match brand styling.
ty_html = (ROOT / "404.html").read_text(encoding="utf-8")
ty_html = ty_html.replace("Page Not Found | Aqua Estate",
                          "Thank You | Aqua Estate")
ty_html = re.sub(
    r'<meta name="description"[^>]*/?>',
    '<meta name="description" content="Your consultation request has been received. An Aqua Estate concierge will respond within one business day."/>',
    ty_html, count=1)
# Replace the 404 main message. The 404 file uses brand-styled headlines.
# Heuristic: replace "404" / "slipped beneath the surface" copy with thank-you copy.
ty_html = re.sub(
    r'(<h1[^>]*>)(.*?)(</h1>)',
    r'\1Your request is in safe hands.\3',
    ty_html, count=1, flags=re.DOTALL)
ty_html = re.sub(
    r'(<p[^>]*class="[^"]*body-lg[^"]*"[^>]*>)(.*?)(</p>)',
    r'\1Thank you for reaching out to Aqua Estate. A member of our concierge team will be in touch within one business day to arrange your private consultation.\3',
    ty_html, count=1, flags=re.DOTALL)
# Make the "Return Home" button text reflect this page
ty_html = re.sub(r'Return\s*to\s*homepage', 'Return to homepage',
                 ty_html, flags=re.IGNORECASE)

ty_path.write_text(ty_html, encoding="utf-8")
print(f"  wrote thank-you.html ({len(ty_html)} bytes)")

print()
print(f"TOTAL extra anchor fixes: {totals['anchors']}")
print(f"TOTAL CTA buttons converted: {totals['buttons']}")
print("Polish complete.")
