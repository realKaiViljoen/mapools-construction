#!/usr/bin/env python3
"""One-shot migration: applies image paths, alt text, meta tags, schemas, nav fixes
to the 6 production HTML pages. Run once; safe to re-run (idempotent on rewrites).

Usage: python3 _migrate.py
"""
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ["index.html", "services.html", "gallery.html",
         "testimonials.html", "book.html", "about.html"]

with open(ROOT / "assets" / "images" / "_url-mapping.json") as f:
    URL_MAP = json.load(f)
with open(ROOT / "assets" / "meta-tags.json") as f:
    META = json.load(f)
with open(ROOT / "assets" / "schema-templates.json") as f:
    SCHEMA = json.load(f)

# Nav anchor → page mapping
ANCHOR_MAP = {
    "#pools": "/gallery.html",
    "#services": "/services.html",
    "#gallery": "/gallery.html",
    "#testimonials": "/testimonials.html",
    "#booking": "/book.html",
    "#book": "/book.html",
    "#about": "/about.html",
    "#contact": "/about.html",
    "#home": "/index.html",
}

# Heuristic mapping of link text → destination, for footer/inline `href="#"` links
TEXT_MAP = {
    "philosophy": "/about.html",
    "sustainability": "/about.html",
    "press": "/about.html",
    "careers": "/about.html",
    "team": "/about.html",
    "legal": "/terms.html",
    "privacy": "/privacy.html",
    "privacy policy": "/privacy.html",
    "terms": "/terms.html",
    "terms of service": "/terms.html",
    "contact": "/about.html",
    "contact us": "/about.html",
    "book": "/book.html",
    "book a consult": "/book.html",
    "book a consultation": "/book.html",
    "request a consultation": "/book.html",
    "request exclusive consult": "/book.html",
    "schedule a consultation": "/book.html",
    "services": "/services.html",
    "all services": "/services.html",
    "view all packages": "/services.html",
    "gallery": "/gallery.html",
    "estates": "/gallery.html",
    "our portfolio": "/gallery.html",
    "portfolio": "/gallery.html",
    "testimonials": "/testimonials.html",
    "client testimonials": "/testimonials.html",
    "about": "/about.html",
    "about us": "/about.html",
    "home": "/index.html",
    "aqua estate": "/index.html",
}

def build_meta_block(page: str) -> str:
    """Return the head meta+OG+Twitter+canonical block for a page."""
    m = META[page]
    out = []
    out.append(f'<title>{html.escape(m["title"])}</title>')
    out.append(f'<meta name="description" content="{html.escape(m["description"])}"/>')
    out.append(f'<meta name="robots" content="{html.escape(m.get("robots","index, follow, max-image-preview:large"))}"/>')
    out.append(f'<link rel="canonical" href="{html.escape(m["canonical"])}"/>')
    out.append('<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>')
    og = m["og"]
    out.append(f'<meta property="og:type" content="{html.escape(og["type"])}"/>')
    out.append(f'<meta property="og:site_name" content="{html.escape(og["site_name"])}"/>')
    out.append(f'<meta property="og:title" content="{html.escape(og["title"])}"/>')
    out.append(f'<meta property="og:description" content="{html.escape(og["description"])}"/>')
    out.append(f'<meta property="og:url" content="{html.escape(og["url"])}"/>')
    out.append(f'<meta property="og:image" content="{html.escape(og["image"])}"/>')
    out.append(f'<meta property="og:image:alt" content="{html.escape(og["image_alt"])}"/>')
    out.append(f'<meta property="og:locale" content="{html.escape(og["locale"])}"/>')
    tw = m["twitter"]
    out.append(f'<meta name="twitter:card" content="{html.escape(tw["card"])}"/>')
    out.append(f'<meta name="twitter:site" content="{html.escape(tw["site"])}"/>')
    out.append(f'<meta name="twitter:title" content="{html.escape(tw["title"])}"/>')
    out.append(f'<meta name="twitter:description" content="{html.escape(tw["description"])}"/>')
    out.append(f'<meta name="twitter:image" content="{html.escape(tw["image"])}"/>')
    return "\n".join(out)

def build_schema_block(page: str) -> str:
    """Return all JSON-LD scripts whose place_on includes this page."""
    blocks = []
    for key, val in SCHEMA.items():
        if not isinstance(val, dict):
            continue
        if "script" not in val or "place_on" not in val:
            continue
        # Skip the FAQ template (marked do-not-publish, no FAQ content exists)
        if key == "faq_page_template":
            continue
        # Breadcrumb is per-page; only include on pages other than home
        if key == "breadcrumb_template":
            if page == "index.html":
                continue
            # Customise breadcrumb for this page later — for now skip generic template
            continue
        if page in val["place_on"]:
            blocks.append(val["script"])
    return "\n".join(blocks)

# Migration markers so re-runs are safe
START = "<!-- AE:META:START -->"
END   = "<!-- AE:META:END -->"

def strip_existing_managed_block(html_text: str) -> str:
    return re.sub(re.escape(START) + r".*?" + re.escape(END), "",
                  html_text, flags=re.DOTALL)

def strip_existing_basics(html_text: str) -> str:
    """Remove <title>, <meta name=description>, <link rel=canonical> outside
    the managed block to avoid duplicates."""
    html_text = re.sub(r"<title>.*?</title>", "", html_text, flags=re.DOTALL|re.IGNORECASE)
    html_text = re.sub(r'<meta[^>]+name=["\']description["\'][^>]*/?>', "",
                       html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*/?>', "",
                       html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'<link[^>]+rel=["\']icon["\'][^>]*/?>', "",
                       html_text, flags=re.IGNORECASE)
    html_text = re.sub(r'<meta[^>]+name=["\']robots["\'][^>]*/?>', "",
                       html_text, flags=re.IGNORECASE)
    return html_text

def replace_image_urls(html_text: str) -> tuple[str, int]:
    """For each lh3 URL → local_path, replace the src AND update alt on the same <img>."""
    count = 0
    for url, info in URL_MAP.items():
        local = info["local_path"].lstrip("/")  # use relative path
        alt = info["alt"]
        # Pattern: <img ... src="<url>" ... /> — replace src and overwrite alt
        # Find every <img> tag containing this URL and rewrite its alt + src.
        url_escaped = re.escape(url)
        img_pattern = re.compile(
            r'(<img\b[^>]*?\bsrc=)(["\'])' + url_escaped + r'(\2)([^>]*/?>)',
            re.IGNORECASE | re.DOTALL,
        )
        def img_repl(m):
            nonlocal count
            count += 1
            prefix, q, _q2, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
            # Rebuild the WHOLE tag from scratch to ensure clean alt
            full = m.group(0)
            # Strip data-alt
            full = re.sub(r'\sdata-alt=(["\']).*?\1', "", full, flags=re.DOTALL)
            # Replace existing alt value
            new_alt = alt.replace('"', "&quot;")
            if re.search(r'\salt=', full, flags=re.IGNORECASE):
                full = re.sub(r'\salt=(["\']).*?\1',
                              f' alt="{new_alt}"', full, count=1,
                              flags=re.DOTALL|re.IGNORECASE)
            else:
                # Insert alt after <img
                full = re.sub(r'<img', f'<img alt="{new_alt}"', full, count=1, flags=re.IGNORECASE)
            # Replace src URL
            full = full.replace(url, "/" + local)
            # Add loading="lazy" to non-hero images (don't flag hero on index)
            if "loading=" not in full.lower() and "hero" not in local.lower():
                full = re.sub(r'<img', '<img loading="lazy" decoding="async"', full, count=1, flags=re.IGNORECASE)
            elif "loading=" not in full.lower():
                full = re.sub(r'<img', '<img loading="eager" fetchpriority="high" decoding="async"', full, count=1, flags=re.IGNORECASE)
            return full
        new_html, n = img_pattern.subn(img_repl, html_text)
        html_text = new_html
        # Also handle background-image url(<url>) and any non-img usage:
        if url in html_text:
            html_text = html_text.replace(url, "/" + local)
            count += 1  # counted but no alt to worry about
    return html_text, count

def fix_anchor_links(html_text: str) -> tuple[str, int]:
    """Replace href="#xyz" with cross-page links where appropriate."""
    count = 0
    # 1. Named anchors (like #services, #booking)
    for anchor, dest in ANCHOR_MAP.items():
        pattern = re.compile(r'href=(["\'])' + re.escape(anchor) + r'\1', re.IGNORECASE)
        new, n = pattern.subn(f'href="{dest}"', html_text)
        html_text = new
        count += n

    # 2. <a href="#">TEXT</a> — heuristic by inner text
    def a_repl(m):
        nonlocal count
        inner = m.group(2).strip()
        # Strip surrounding tags, get visible text
        text = re.sub(r"<[^>]+>", "", inner).strip().lower()
        text = re.sub(r"\s+", " ", text)
        if text in TEXT_MAP:
            count += 1
            return f'<a{m.group(1)}href="{TEXT_MAP[text]}"{m.group(3)}>{m.group(2)}</a>'
        return m.group(0)

    a_pattern = re.compile(
        r'<a((?:\s+[^>]*?)?)\s*href=["\']#["\']([^>]*)>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    # Above regex doesn't keep groups consistent; use simpler approach:
    a_pattern = re.compile(
        r'<a([^>]*?)\shref=["\']#["\']([^>]*?)>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    def repl2(m):
        nonlocal count
        before, after, inner = m.group(1), m.group(2), m.group(3)
        text = re.sub(r"<[^>]+>", "", inner).strip().lower()
        text = re.sub(r"\s+", " ", text)
        if text in TEXT_MAP:
            count += 1
            return f'<a{before} href="{TEXT_MAP[text]}"{after}>{inner}</a>'
        return m.group(0)
    html_text = a_pattern.sub(repl2, html_text)
    return html_text, count

def inject_head(html_text: str, page: str) -> str:
    """Insert managed meta+schema block right before </head>."""
    # 1. Strip prior managed block (re-run safety)
    html_text = strip_existing_managed_block(html_text)
    # 2. Strip pre-existing basics that would duplicate
    html_text = strip_existing_basics(html_text)
    meta_block = build_meta_block(page)
    schema_block = build_schema_block(page)
    block = f"{START}\n{meta_block}\n{schema_block}\n{END}\n"
    if "</head>" not in html_text:
        raise RuntimeError(f"{page}: missing </head>")
    return html_text.replace("</head>", block + "</head>", 1)

# Per-page main
report = []
for page in PAGES:
    p = ROOT / page
    txt = p.read_text(encoding="utf-8")
    txt, img_count = replace_image_urls(txt)
    txt, anchor_count = fix_anchor_links(txt)
    txt = inject_head(txt, page)
    p.write_text(txt, encoding="utf-8")
    report.append(f"  {page:25s} images={img_count:3d}  anchors_fixed={anchor_count:3d}")

# ALSO process the standalone pages (404, privacy, terms) for nav fixes only.
for page in ["404.html", "privacy.html", "terms.html"]:
    p = ROOT / page
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    txt, anchor_count = fix_anchor_links(txt)
    p.write_text(txt, encoding="utf-8")
    report.append(f"  {page:25s} (nav-only)        anchors_fixed={anchor_count:3d}")

print("Migration complete:")
for line in report:
    print(line)
