#!/usr/bin/env python3
"""Strip phone numbers from WhatsApp button/link text. The wa.me href does
the work — visible text should just say 'Chat on WhatsApp' (or 'WhatsApp'
for shorter contexts)."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

PAIRS = [
    # Anchor/button visible text — most common form
    (">WhatsApp 065 643 0603<", ">Chat on WhatsApp<"),
    # Standalone label inside contact cards (used in about.html as a tel-style label)
    # Keep it readable but no number — but only if surrounded by a wa.me link
    # We'll handle that by-context: if ">065 643 0603<" is inside an <a href="https://wa.me/...">, replace with "WhatsApp"
]

# General pair-replace
def apply(txt):
    n = 0
    for old, new in PAIRS:
        if old in txt:
            n += txt.count(old)
            txt = txt.replace(old, new)
    return txt, n

# Special-case the about.html WhatsApp card row:
# <a class="..." href="https://wa.me/27656430603" ...>065 643 0603</a>
WA_LINK_NUMBER_RE = re.compile(
    r'(<a\b[^>]*?href="https://wa\.me/27656430603[^"]*"[^>]*>)\s*065\s*643\s*0603\s*(</a>)',
)

total = 0
for p in ROOT.glob("*.html"):
    txt = p.read_text(encoding="utf-8")
    txt, n = apply(txt)
    pre = txt
    txt = WA_LINK_NUMBER_RE.sub(r"\1WhatsApp\2", txt)
    if pre != txt:
        n += pre.count('>065 643 0603<') - txt.count('>065 643 0603<')
    if n:
        p.write_text(txt, encoding="utf-8")
        print(f"  {p.name:25s} {n} replacements")
        total += n
print(f"\nTotal: {total}")
