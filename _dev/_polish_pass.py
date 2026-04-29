#!/usr/bin/env python3
"""Final polish pass:
  1) Fix gallery.html residue (broken JSON-LD contentUrls + portfolio language)
  2) Strip every em-dash (—) sitewide. Owner's call: "nothing uglier than an
     mdash". Replace " — " with ", " and bare "—" with "," and clean up
     " &mdash; " HTML entities.
  3) Add custom cursor (CSS + JS) to all production pages — small navy dot
     follows the mouse, soft ring grows on interactive elements, hidden
     on mobile/touch.
Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
              "book.html", "about.html", "privacy.html", "terms.html",
              "404.html", "thank-you.html"]
TEXT_FILES = ["llms.txt", "llms-full.txt"]

# ============================================================================
# 1) Gallery residue
# ============================================================================
GALLERY_PAIRS = [
    # ImageGallery JSON-LD: broken filenames → real existing files
    ("/assets/images/gallery-steyn-city.jpg",
     "/assets/images/gallery-steyn-city-residence-pool.png"),
    ("/assets/images/gallery-sandhurst.jpg",
     "/assets/images/gallery-sandhurst-courtyard-lap-pool.png"),
    ("/assets/images/gallery-meyersdal.jpg",
     "/assets/images/gallery-meyersdal-eco-estate-pool.png"),
    # Portfolio / curated-showcase residue in JSON-LD descriptions
    ('"Ma Pools Construction Portfolio Gallery"',
     '"Ma Pools Construction Project Gallery"'),
    ('"A curated showcase of pools across Gauteng under Ma Pools Construction care."',
     '"A selection of pools, renovations and installations completed by Ma Pools Construction across Gauteng."'),
]

def fix_gallery_residue():
    p = ROOT / "gallery.html"
    txt = p.read_text(encoding="utf-8")
    n = 0
    for old, new in GALLERY_PAIRS:
        if old in txt:
            n += txt.count(old)
            txt = txt.replace(old, new)
    if n:
        p.write_text(txt, encoding="utf-8")
    return n

# ============================================================================
# 2) Em-dash sweep
# ============================================================================
def strip_emdashes(txt):
    n = 0
    # Spaced em-dash → comma + space (most common, parenthetical use)
    pre = txt; txt = txt.replace(" — ", ", ");           n += pre.count(" — ")
    # Spaced &mdash; entity
    pre = txt; txt = txt.replace(" &mdash; ", ", ");     n += pre.count(" &mdash; ")
    # Em-dash at start of line (—Mkhacani style attribution)
    pre = txt; txt = re.sub(r'^—\s*', '— ', txt, flags=re.MULTILINE)  # placeholder
    # Em-dash at end-of-line (rare): drop to comma
    pre = txt; txt = re.sub(r' —\s*$', ',', txt, flags=re.MULTILINE)
    # Bare em-dash (no spaces, e.g. word—word) → comma
    pre = txt; txt = txt.replace("—", ",");              n += pre.count("—")
    pre = txt; txt = txt.replace("&mdash;", ",");        n += pre.count("&mdash;")
    # Cleanup: ", ," → "," ; "  ," → " ,"; double commas → single
    txt = re.sub(r',\s*,', ',', txt)
    txt = re.sub(r' {2,}', ' ', txt)
    return txt, n

# ============================================================================
# 3) Custom cursor (CSS + JS)
# ============================================================================
CURSOR_CSS = """
        /* Custom cursor (desktop only) */
        .ma-cursor-dot, .ma-cursor-ring {
            position: fixed;
            top: 0; left: 0;
            pointer-events: none;
            z-index: 9999;
            border-radius: 50%;
            transform: translate3d(-50%, -50%, 0);
            display: none;
        }
        @media (hover: hover) and (pointer: fine) {
            body.ma-cursor-on { cursor: none; }
            body.ma-cursor-on a,
            body.ma-cursor-on button,
            body.ma-cursor-on [role="button"],
            body.ma-cursor-on summary,
            body.ma-cursor-on label { cursor: none; }
            body.ma-cursor-on input,
            body.ma-cursor-on textarea,
            body.ma-cursor-on select { cursor: text; }
            .ma-cursor-dot, .ma-cursor-ring { display: block; }
        }
        .ma-cursor-dot {
            width: 6px; height: 6px;
            background: #0A2342;
        }
        .ma-cursor-ring {
            width: 32px; height: 32px;
            border: 1.5px solid rgba(10, 35, 66, 0.35);
            transition: width 240ms cubic-bezier(0.22, 1, 0.36, 1),
                        height 240ms cubic-bezier(0.22, 1, 0.36, 1),
                        border-color 240ms,
                        background-color 240ms;
        }
        .ma-cursor-ring.active {
            width: 52px; height: 52px;
            border-color: #25D366;
            background: rgba(37, 211, 102, 0.10);
        }
"""

CURSOR_JS = """<!-- AE:CURSOR:START -->
<script>
(function(){
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (window.maCursorOn) return; window.maCursorOn = true;
  document.body.classList.add('ma-cursor-on');
  var dot = document.createElement('div'); dot.className = 'ma-cursor-dot';
  var ring = document.createElement('div'); ring.className = 'ma-cursor-ring';
  document.body.appendChild(dot); document.body.appendChild(ring);
  var mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', function(e){
    mx = e.clientX; my = e.clientY;
    dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0) translate(-50%,-50%)';
  }, { passive: true });
  (function loop(){
    rx += (mx - rx) * 0.18;
    ry += (my - ry) * 0.18;
    ring.style.transform = 'translate3d(' + rx + 'px,' + ry + 'px,0) translate(-50%,-50%)';
    requestAnimationFrame(loop);
  })();
  var sel = 'a, button, [role="button"], summary, label, [data-cursor="active"]';
  document.addEventListener('mouseover', function(e){
    if (e.target && e.target.closest && e.target.closest(sel)) ring.classList.add('active');
  });
  document.addEventListener('mouseout', function(e){
    if (e.target && e.target.closest && e.target.closest(sel)) ring.classList.remove('active');
  });
  document.addEventListener('mouseleave', function(){
    dot.style.opacity = ring.style.opacity = '0';
  });
  document.addEventListener('mouseenter', function(){
    dot.style.opacity = ring.style.opacity = '1';
  });
})();
</script>
<!-- AE:CURSOR:END -->"""

CURSOR_CSS_MARKER_START = "/* Custom cursor (desktop only) */"
CURSOR_JS_MARKER = "<!-- AE:CURSOR:START -->"

def add_custom_cursor(txt):
    # Skip if already added
    if CURSOR_CSS_MARKER_START in txt and CURSOR_JS_MARKER in txt:
        return txt, False
    # Strip prior versions (idempotency)
    txt = re.sub(re.escape(CURSOR_JS_MARKER) + r".*?<!-- AE:CURSOR:END -->",
                 "", txt, flags=re.DOTALL)
    # Inject CSS into inline <style>
    style_re = re.compile(r'(<style>)(.*?)(</style>)', re.DOTALL)
    m = style_re.search(txt)
    if m:
        new_style = m.group(2)
        if CURSOR_CSS_MARKER_START not in new_style:
            new_style = new_style.rstrip() + "\n" + CURSOR_CSS + "    "
        txt = txt.replace(m.group(0), m.group(1) + new_style + m.group(3), 1)
    # Inject JS just before </body>
    if "</body>" in txt:
        txt = txt.replace("</body>", CURSOR_JS + "\n</body>", 1)
    return txt, True

# ============================================================================
# Run
# ============================================================================
gallery_n = fix_gallery_residue()
print(f"Gallery residue fixed: {gallery_n} replacements\n")

print(f"{'FILE':25s}  emdash  cursor")
total_em = 0
for page in HTML_PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    original = p.read_text(encoding="utf-8")
    txt = original
    txt, n_em = strip_emdashes(txt)
    txt, added_cursor = add_custom_cursor(txt)
    if txt != original:
        p.write_text(txt, encoding="utf-8")
    print(f"  {page:25s}  {n_em:>5d}  {'✓' if added_cursor else '-'}")
    total_em += n_em

# Em-dash also from .txt llms files
for tf in TEXT_FILES:
    p = ROOT / tf
    if not p.exists():
        continue
    original = p.read_text(encoding="utf-8")
    txt, n_em = strip_emdashes(original)
    if txt != original:
        p.write_text(txt, encoding="utf-8")
    print(f"  {tf:25s}  {n_em:>5d}")
    total_em += n_em

print(f"\nTotal em-dashes removed: {total_em}")
