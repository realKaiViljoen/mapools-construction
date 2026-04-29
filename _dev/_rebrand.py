#!/usr/bin/env python3
"""Rebrand: swap Aqua Estate placeholders → Ma Pools Construction real data
across all HTML, JSON, and txt files. Idempotent.

Real data source (provided by client):
  Director:  Mkhacani Amos Chauke
  Address:   331B Utekwane Street, Zone 7, Meadowlands, 1852
  Email:     mapoolsconstruction@gmail.com
  WhatsApp:  065 643 0603     (no calls — message only)
  Call:      078 712 2157     (no WhatsApp — voice only)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# 1) Bulk string replacements (specific → general)
# ---------------------------------------------------------------------------
# Order matters: longer matches first.
REPLACEMENTS = [
    # Domain (most specific first)
    ("https://www.aquaestate.co.za", "https://www.mapoolsconstruction.co.za"),
    ("www.aquaestate.co.za", "www.mapoolsconstruction.co.za"),
    ("aquaestate.co.za",     "mapoolsconstruction.co.za"),

    # Social-handle URLs
    ("https://www.instagram.com/aquaestate.za",     "https://www.instagram.com/mapoolsconstruction"),
    ("https://www.facebook.com/aquaestate.za",      "https://www.facebook.com/mapoolsconstruction"),
    ("https://www.linkedin.com/company/aqua-estate", "https://www.linkedin.com/company/ma-pools-construction"),

    # Email
    ("concierge@aquaestate.co.za", "mapoolsconstruction@gmail.com"),
    ("privacy@aquaestate.co.za",   "mapoolsconstruction@gmail.com"),
    ("legal@aquaestate.co.za",     "mapoolsconstruction@gmail.com"),

    # Phone (placeholder → call line)
    ("+27110000000",       "+27787122157"),
    ("+27 11 000 0000",    "+27 78 712 2157"),

    # Address (whole-string forms appearing in JSON-LD strings)
    ("1 Sandton Drive",                "331B Utekwane Street, Zone 7"),
    ('"streetAddress": "1 Sandton Drive"', '"streetAddress": "331B Utekwane Street, Zone 7"'),
    ('"addressLocality": "Sandhurst"',     '"addressLocality": "Meadowlands"'),
    ('"postalCode": "2196"',               '"postalCode": "1852"'),
    ("Sandton, Gauteng",                "Meadowlands, Soweto"),  # footer text

    # Geo coordinates: Sandhurst → Meadowlands Zone 7
    ('"latitude": -26.10760',   '"latitude": -26.23080'),
    ('"longitude": 28.05680',   '"longitude": 27.91520'),
    ('"latitude": "-26.10760"', '"latitude": "-26.23080"'),
    ('"longitude": "28.05680"', '"longitude": "27.91520"'),

    # Twitter handle (placeholder → site name; real handle TBD)
    ('"@aquaestate"', '"@mapoolspools"'),
    ('content="@aquaestate"', 'content="@mapoolspools"'),

    # Brand name forms (longest first)
    ("Aqua Estate (Pty) Ltd", "Ma Pools Construction"),
    ("AQUA ESTATE",            "MA POOLS CONSTRUCTION"),
    ("Aqua Estate",            "Ma Pools Construction"),
    ("aqua-estate",            "ma-pools-construction"),  # ids/slugs

    # Slogan placeholder — keep brand-relevant but accurate to construction biz
    ("Pristine pools. Effortless luxury.",
     "New builds, renovations, and dependable pool care across Gauteng."),

    # Copyright year
    ("© 2024", "© 2026"),
    ("&copy; 2024", "&copy; 2026"),

    # Founder placeholder name in About → director
    # (covers any literal mention; team strip handled separately)
    ("Adrian Thorne",  "Mkhacani Amos Chauke"),
]

# Files we touch — exclude assets we don't want to mutate
TARGET_GLOBS = [
    "*.html",
    "*.txt",
    "*.toml",
    "_redirects",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "llms-full.txt",
    "DEPLOY.md",
    "tasks/todo.md",
    "vercel.json",
    "assets/site-config.json",
    "assets/meta-tags.json",
    "assets/schema-templates.json",
    "assets/images/_url-mapping.json",
]

def apply_replacements(text: str) -> tuple[str, int]:
    n = 0
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            n += count
    return text, n

# ---------------------------------------------------------------------------
# 2) Strip placeholder aggregateRating + foundingDate from JSON-LD
# ---------------------------------------------------------------------------
def strip_jsonld_blocks(text: str) -> tuple[str, int]:
    """Remove fake aggregateRating and foundingDate fields. They violate Google
    policy until real data exists."""
    n = 0
    # aggregateRating: { ... } including the trailing comma if present
    pattern_agg = re.compile(
        r',\s*"aggregateRating"\s*:\s*\{[^{}]*\}',
        flags=re.DOTALL,
    )
    new_text, c = pattern_agg.subn("", text)
    text = new_text; n += c
    # Same pattern but at object START (no leading comma) followed by comma
    pattern_agg2 = re.compile(
        r'"aggregateRating"\s*:\s*\{[^{}]*\}\s*,',
        flags=re.DOTALL,
    )
    new_text, c = pattern_agg2.subn("", text)
    text = new_text; n += c
    # foundingDate: "2014"
    pattern_fd = re.compile(r',\s*"foundingDate"\s*:\s*"[^"]*"')
    new_text, c = pattern_fd.subn("", text)
    text = new_text; n += c
    pattern_fd2 = re.compile(r'"foundingDate"\s*:\s*"[^"]*"\s*,')
    new_text, c = pattern_fd2.subn("", text)
    text = new_text; n += c
    return text, n

# ---------------------------------------------------------------------------
# 3) Replace areaServed list in JSON-LD with Soweto-aligned suburbs
# ---------------------------------------------------------------------------
NEW_AREA_SERVED_BLOCK = """  "areaServed": [
    { "@type": "AdministrativeArea", "name": "Gauteng" },
    { "@type": "City", "name": "Johannesburg" },
    { "@type": "City", "name": "Soweto" },
    { "@type": "City", "name": "Roodepoort" },
    { "@type": "City", "name": "Krugersdorp" },
    { "@type": "Place", "name": "Meadowlands" },
    { "@type": "Place", "name": "Diepkloof" },
    { "@type": "Place", "name": "Orlando" },
    { "@type": "Place", "name": "Pimville" },
    { "@type": "Place", "name": "Dobsonville" },
    { "@type": "Place", "name": "Naledi" },
    { "@type": "Place", "name": "Protea Glen" },
    { "@type": "Place", "name": "Lenasia" },
    { "@type": "Place", "name": "Eldorado Park" },
    { "@type": "Place", "name": "Florida" }
  ]"""

def replace_area_served(text: str) -> tuple[str, int]:
    """Replace the multi-line areaServed array in any LocalBusiness JSON-LD."""
    pattern = re.compile(
        r'"areaServed"\s*:\s*\[[^\]]*\]',
        flags=re.DOTALL,
    )
    new_text, c = pattern.subn(NEW_AREA_SERVED_BLOCK, text)
    return new_text, c

# ---------------------------------------------------------------------------
# 4) Run across files
# ---------------------------------------------------------------------------
totals = {"strings": 0, "stripped": 0, "areas": 0}
files_touched = []
for glob in TARGET_GLOBS:
    for p in ROOT.glob(glob):
        if not p.is_file():
            continue
        original = p.read_text(encoding="utf-8")
        text = original
        text, n1 = apply_replacements(text)
        if p.suffix in (".html", ".json"):
            text, n2 = strip_jsonld_blocks(text)
            text, n3 = replace_area_served(text)
        else:
            n2 = n3 = 0
        if text != original:
            p.write_text(text, encoding="utf-8")
            files_touched.append((str(p.relative_to(ROOT)), n1, n2, n3))
            totals["strings"]  += n1
            totals["stripped"] += n2
            totals["areas"]    += n3

print(f"{'FILE':45s}  STRINGS  STRIPPED  AREAS")
for path, n1, n2, n3 in files_touched:
    print(f"{path:45s}  {n1:>7d}  {n2:>8d}  {n3:>5d}")
print()
print(f"  TOTAL string replacements:  {totals['strings']}")
print(f"  TOTAL JSON-LD blocks stripped: {totals['stripped']}")
print(f"  TOTAL areaServed arrays replaced: {totals['areas']}")
print(f"  Files touched: {len(files_touched)}")
