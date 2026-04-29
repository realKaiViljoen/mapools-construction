#!/usr/bin/env python3
"""Final pass: fix grammatical stragglers from earlier bulk replacements
('Gauteng's across pools' etc.) and any remaining luxury phrases."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAIRS = [
    # Grammatically broken stragglers from earlier "most prestigious"→"across"
    ("Gauteng's across pools",       "Gauteng pools"),
    ("Gauteng's across estates",     "Gauteng homes and estates"),
    ("Gauteng's across homes",       "Gauteng homes"),
    ("Gauteng&#x27;s across pools",   "Gauteng pools"),
    ("Gauteng&#x27;s across estates", "Gauteng homes and estates"),
    ("Gauteng&#x27;s across homes",   "Gauteng homes"),
    ("Gauteng's across aquatic environments", "pools across Gauteng"),
    ("Gauteng's across",             "Gauteng"),    # final fallback
    ("Gauteng&#x27;s across",         "Gauteng"),
    ("across pools",                 "pools across Gauteng"),
    ("across estates",               "homes and estates"),
    ("across the most",              "across"),
    ("its across",                   "its"),

    # Grammar fix: "An Ma" → "A Ma"
    ("An Ma Pools",  "A Ma Pools"),
    ("an Ma Pools",  "a Ma Pools"),

    # Twitter / OG / meta description residuals
    ("A decade of surgical precision and uncompromising care for Gauteng pools.",
     "Director-led pool construction, renovation, and care across Gauteng."),
    ("A decade of surgical precision and uncompromising care for Gauteng&#x27;s across pools.",
     "Director-led pool construction, renovation, and care across Gauteng."),
    ("A decade of precision pool care for Gauteng's prestige estates.",
     "Director-led pool construction and care across Gauteng."),
    ("A decade of precision pool care for Gauteng&#x27;s prestige estates.",
     "Director-led pool construction and care across Gauteng."),
    ("A decade of",                  "Director-led"),
    ("a decade",                     "experience"),
    ("for over a decade,",           ""),
    ("for over a decade",            ""),
    ("Voices of pristine luxury — why Gauteng pools trust Ma Pools Construction.",
     "Customer feedback and reviews of Ma Pools Construction — being collected as customers leave them."),
    ("Voices of pristine luxury — why Gauteng homes and estates trust Ma Pools Construction.",
     "Customer feedback and reviews of Ma Pools Construction."),
    ("Voices of pristine luxury",    "Customer reviews"),
    ("Why Gauteng pools trust Ma Pools Construction.",
     "Customer reviews of Ma Pools Construction."),
    ("Why Gauteng homes and estates trust Ma Pools Construction.",
     "Customer reviews of Ma Pools Construction."),

    # Page-level descriptions
    ("This page slipped beneath the surface. Return to Ma Pools Construction's homepage to continue your tour of premium pool care for Gauteng estates.",
     "This page slipped beneath the surface. Head back to Ma Pools Construction's homepage."),
    ("Your consultation request has been received. An Ma Pools Construction concierge will respond within one business day.",
     "Your request has been received. The director will respond within one business day."),
    ("Your consultation request has been received. A Ma Pools Construction concierge will respond within one business day.",
     "Your request has been received. The director will respond within one business day."),

    # Other luxury residuals
    ("Premium pool maintenance and care for Gauteng pools.",
     "Pool construction, renovation and care across Gauteng."),
    ("Premium pool maintenance and care for Gauteng homes and estates.",
     "Pool construction, renovation and care across Gauteng."),
    ("premium pool care for Gauteng",
     "pool construction and care across Gauteng"),
    ("Premium pool care for Gauteng pools.",
     "Pool construction and care across Gauteng."),
    ("Premium pool care for",        "Pool construction and care for"),
    (" premium pool ",               " pool "),
    ("our exclusive circle of clients who demand nothing less than perfection for their estates",
     "our growing list of customers"),
    ("an exclusive circle",          "our customer list"),
    ("Limited availability. Our lead technician will contact you to arrange a comprehensive audit of your estate's pool system.",
     "We'll be in touch within one business day to discuss your project."),
    ("Schedule a Consultation",      "Get a Free Quote"),
    ("Limited service availability for new Gauteng registrations.",
     ""),
    ("Join our exclusive circle of clients who demand nothing less than perfection for their estates. Limited service availability for new Gauteng registrations.",
     "Got a project? WhatsApp us on 065 643 0603 or fill in the form."),

    # Stragglers
    ("Aqua ", "Ma Pools "),
    ("aquatic architectural maintenance", "pool care"),
    ("aquatic architectural", "pool"),
    ("aquatic luxury", "pool work"),
    ("aquatic environments", "pools"),
    ("aquatic preservation", "pool care"),
    ("aquatic excellence", "pool work"),
    ("Aquatic ", "Pool "),
    ("aquatic ", "pool "),
    ("Sanctuary of serenity", "well-built pool"),
    ("sanctuary of serenity", "well-built pool"),
    ("the art of stillness", "selected work"),
    ("The Art of Stillness", "Selected Work"),
    ("Surgical precision", "Real precision"),
    ("surgical precision", "real precision"),
    ("Architectural elegance", "well-built pool"),
    ("architectural elegance", "well-built pool"),
    ("&quot;set-and-forget&quot;", "hands-off"),
    ('"set-and-forget"', "hands-off"),
    ("set-and-forget", "hands-off"),

    # Common adjective scrubs
    ("White-glove ", ""),
    ("white-glove ", ""),
    ("Bespoke ",     ""),
    ("bespoke ",     ""),
    (" bespoke ",    " "),
    (" Bespoke ",    " "),
    ("clockwork precision", "fixed schedule"),

    # Title/header residuals on pages
    ("Voices of <br/>Pristine Luxury.", "Building a track record."),
    ("Voices of Pristine Luxury",       "Customer reviews"),
    ("Pristine Luxury",                  "Real Work"),
    ("Pristine ",                       ""),
    ("pristine ",                       ""),
]

def apply(text):
    n = 0
    for old, new in PAIRS:
        if old in text:
            n += text.count(old)
            text = text.replace(old, new)
    return text, n

TARGETS = list(ROOT.glob("*.html")) + [
    ROOT / "llms.txt",
    ROOT / "llms-full.txt",
    ROOT / "assets" / "site-config.json",
    ROOT / "assets" / "meta-tags.json",
    ROOT / "assets" / "schema-templates.json",
]

total = 0
for p in TARGETS:
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    new, n = apply(txt)
    if n:
        p.write_text(new, encoding="utf-8")
        print(f"  {str(p.relative_to(ROOT)):45s}  {n:>4d}")
        total += n

print(f"\nTotal final-cleanup replacements: {total}")
