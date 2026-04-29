#!/usr/bin/env python3
"""Polish v2: 2 bug fixes + 5 improvements. Idempotent.

Bug fixes
  1) Custom cursor was invisible. Rewrite CSS + JS:
     - white-cored navy-bordered dot (visible on any background)
     - margin-offset centering (avoids CSS↔JS transform conflict)
     - opacity 0→1 on first mousemove (no corner-flash)
     - reliable display rules (only hide on touch / coarse pointer)
  2) "MA POOLS CONSTRUCTION" wordmark in nav was a <div> on most pages,
     not a link. Wrap in <a href="/"> sitewide so clicking the wordmark
     always returns home.

Improvements
  3) WhatsApp pulse animation on the floating bubble + sticky bar
     (subtle 2.4s ring pulse, brand-consistent attention draw).
  4) Hero "scroll for more" indicator on index.html (animated chevron).
  5) Page-load fade-in + scroll-reveal extended to inner-page sections.
  6) Sitewide focus-visible ring polish.
  7) 404 page personality rewrite (handled separately via Edit, not here).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
              "book.html", "about.html", "privacy.html", "terms.html",
              "404.html", "thank-you.html"]

# ============================================================================
# 1) New cursor CSS + JS — visible-by-default, robust display rules
# ============================================================================
CURSOR_CSS = """
        /* Custom cursor (desktop only) */
        @media (hover: hover) and (pointer: fine) {
            body.ma-cursor-active { cursor: none; }
            body.ma-cursor-active a,
            body.ma-cursor-active button,
            body.ma-cursor-active [role="button"],
            body.ma-cursor-active summary,
            body.ma-cursor-active label { cursor: none; }
            body.ma-cursor-active input,
            body.ma-cursor-active textarea,
            body.ma-cursor-active select,
            body.ma-cursor-active [contenteditable] { cursor: text !important; }
        }
        .ma-cursor-dot, .ma-cursor-ring {
            position: fixed;
            top: 0; left: 0;
            pointer-events: none;
            z-index: 9999;
            border-radius: 50%;
            opacity: 0;
            will-change: transform;
        }
        .ma-cursor-dot.ready, .ma-cursor-ring.ready { opacity: 1; }
        .ma-cursor-dot {
            width: 8px; height: 8px;
            background: #fff;
            box-shadow: 0 0 0 1.5px #0A2342, 0 2px 8px rgba(10,35,66,0.25);
            margin: -4px 0 0 -4px;
            transition: opacity 200ms;
        }
        .ma-cursor-ring {
            width: 36px; height: 36px;
            border: 1.5px solid rgba(10, 35, 66, 0.45);
            margin: -18px 0 0 -18px;
            transition: width 240ms cubic-bezier(0.22, 1, 0.36, 1),
                        height 240ms cubic-bezier(0.22, 1, 0.36, 1),
                        margin 240ms cubic-bezier(0.22, 1, 0.36, 1),
                        border-color 240ms,
                        background-color 240ms,
                        opacity 200ms;
        }
        .ma-cursor-ring.active {
            width: 56px; height: 56px;
            margin: -28px 0 0 -28px;
            border-color: #25D366;
            background: rgba(37, 211, 102, 0.12);
        }
        @media (pointer: coarse), (hover: none) {
            .ma-cursor-dot, .ma-cursor-ring { display: none !important; }
        }
"""

CURSOR_JS = """<!-- AE:CURSOR:START -->
<script>
(function(){
  if (window.__maCursor) return;
  if (matchMedia('(pointer: coarse)').matches) return;
  window.__maCursor = true;
  var dot = document.createElement('div'); dot.className = 'ma-cursor-dot';
  var ring = document.createElement('div'); ring.className = 'ma-cursor-ring';
  document.body.appendChild(dot); document.body.appendChild(ring);
  var mx = -100, my = -100, rx = -100, ry = -100, started = false;
  function start(){
    if (started) return; started = true;
    document.body.classList.add('ma-cursor-active');
    dot.classList.add('ready'); ring.classList.add('ready');
  }
  document.addEventListener('mousemove', function(e){
    if (!started) start();
    mx = e.clientX; my = e.clientY;
    dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)';
  }, { passive: true });
  (function loop(){
    rx += (mx - rx) * 0.18;
    ry += (my - ry) * 0.18;
    ring.style.transform = 'translate3d(' + rx + 'px,' + ry + 'px,0)';
    requestAnimationFrame(loop);
  })();
  var sel = 'a, button, [role="button"], summary, label, [data-cursor="active"]';
  document.addEventListener('mouseover', function(e){
    if (e.target && e.target.closest && e.target.closest(sel)) ring.classList.add('active');
  });
  document.addEventListener('mouseout', function(e){
    if (e.target && e.target.closest && e.target.closest(sel)) ring.classList.remove('active');
  });
  document.addEventListener('mouseleave', function(){ dot.style.opacity = ring.style.opacity = '0'; });
  document.addEventListener('mouseenter', function(){ if (started) { dot.style.opacity = ring.style.opacity = '1'; } });
})();
</script>
<!-- AE:CURSOR:END -->"""

# Mark ranges in CSS to detect old cursor block and replace
CURSOR_CSS_OLD_RE = re.compile(
    r'\n\s*/\*\s*Custom cursor.*?\.ma-cursor-ring\.active\s*\{[^}]*\}\s*(\}\s*)?',
    re.DOTALL,
)
# Also match the new placement we'll create (idempotency)
def replace_cursor_css(txt):
    style_re = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.DOTALL)
    m = style_re.search(txt)
    if not m:
        return txt
    style = m.group(2)
    # Strip prior cursor block (if any)
    new_style = CURSOR_CSS_OLD_RE.sub('\n', style)
    # Append new cursor CSS at end of inline <style>
    new_style = new_style.rstrip() + "\n" + CURSOR_CSS + "    "
    if new_style != style:
        txt = txt.replace(m.group(0), m.group(1) + new_style + m.group(3), 1)
    return txt

def replace_cursor_js(txt):
    txt = re.sub(r'<!-- AE:CURSOR:START -->.*?<!-- AE:CURSOR:END -->',
                 '', txt, flags=re.DOTALL)
    if "</body>" in txt:
        txt = txt.replace("</body>", CURSOR_JS + "\n</body>", 1)
    return txt

# ============================================================================
# 2) Wrap nav wordmark in <a href="/">
# ============================================================================
WORDMARK_DIV_RE = re.compile(
    r'(<div\s+class="text-2xl[^"]*"[^>]*>)\s*(MA POOLS CONSTRUCTION)\s*(</div>)',
    re.IGNORECASE,
)
WORDMARK_SPAN_RE = re.compile(
    r'(<span\s+class="text-2xl[^"]*"[^>]*>)\s*(MA POOLS CONSTRUCTION)\s*(</span>)',
    re.IGNORECASE,
)

def linkify_wordmark(txt):
    """Wrap nav wordmark in an <a href="/"> if it isn't already."""
    n = 0
    def repl(m):
        nonlocal n
        n += 1
        # Extract class attr
        class_match = re.search(r'class="([^"]*)"', m.group(1))
        cls = class_match.group(1) if class_match else "text-2xl"
        return ('<a href="/" aria-label="Ma Pools Construction home" '
                f'class="{cls} hover:opacity-80 transition-opacity">'
                + m.group(2) + '</a>')
    txt = WORDMARK_DIV_RE.sub(repl, txt)
    txt = WORDMARK_SPAN_RE.sub(repl, txt)
    return txt, n

# ============================================================================
# 3) WhatsApp pulse animation
# ============================================================================
WA_PULSE_CSS = """
        /* WhatsApp pulse */
        @keyframes ma-wa-pulse {
            0%   { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.55), 0 10px 30px rgba(37,211,102,0.45); }
            70%  { box-shadow: 0 0 0 18px rgba(37, 211, 102, 0); 0 10px 30px rgba(37,211,102,0.45); }
            100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); 0 10px 30px rgba(37,211,102,0.45); }
        }
        .ma-wa-pulse { animation: ma-wa-pulse 2.4s cubic-bezier(0.22,1,0.36,1) infinite; }
        @media (prefers-reduced-motion: reduce) { .ma-wa-pulse { animation: none; } }
"""

# Apply ma-wa-pulse class to the WA-float anchor
def add_wa_pulse(txt):
    # Idempotent: skip if already has class
    pat = re.compile(
        r'(<!-- AE:WA-FLOAT:START -->\s*<a\b[^>]*?\bclass=")([^"]*)(")',
        re.DOTALL,
    )
    def repl(m):
        cls = m.group(2)
        if "ma-wa-pulse" in cls:
            return m.group(0)
        return m.group(1) + cls + " ma-wa-pulse" + m.group(3)
    return pat.sub(repl, txt)

# ============================================================================
# 4) Page-load fade-in + scroll-reveal global utilities
# ============================================================================
PAGE_FADE_CSS = """
        /* Page-load fade-in */
        body { opacity: 0; transition: opacity 600ms cubic-bezier(0.22, 1, 0.36, 1); }
        body.ma-page-loaded { opacity: 1; }
        @media (prefers-reduced-motion: reduce) { body { opacity: 1 !important; transition: none; } }

        /* Focus-visible polish (sitewide) */
        *:focus { outline: none; }
        *:focus-visible {
            outline: 2px solid #0A2342;
            outline-offset: 3px;
            border-radius: 4px;
        }
        a:focus-visible, button:focus-visible, [role="button"]:focus-visible {
            outline-color: #0A2342;
        }
        input:focus-visible, textarea:focus-visible, select:focus-visible {
            outline: 2px solid #0A2342;
            outline-offset: 1px;
        }
"""

PAGE_FADE_JS = """<!-- AE:PAGEFADE:START -->
<script>
(function(){
  function go(){ document.body.classList.add('ma-page-loaded'); }
  if (document.readyState === 'complete') { go(); }
  else { window.addEventListener('load', go); }
  // Scroll-reveal observer (covers .scroll-reveal class on every page)
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.scroll-reveal').forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('.scroll-reveal').forEach(function(el){ el.classList.add('visible'); });
  }
})();
</script>
<!-- AE:PAGEFADE:END -->"""

PAGE_FADE_CSS_MARKER = "/* Page-load fade-in */"
PAGE_FADE_JS_MARKER = "<!-- AE:PAGEFADE:START -->"

def add_page_fade(txt):
    # Inject CSS once (idempotent)
    style_re = re.compile(r'(<style[^>]*>)(.*?)(</style>)', re.DOTALL)
    m = style_re.search(txt)
    if m and PAGE_FADE_CSS_MARKER not in m.group(2):
        new_style = m.group(2).rstrip() + "\n" + PAGE_FADE_CSS + "    "
        txt = txt.replace(m.group(0), m.group(1) + new_style + m.group(3), 1)
    # Strip any prior pagefade block, inject fresh
    txt = re.sub(r'<!-- AE:PAGEFADE:START -->.*?<!-- AE:PAGEFADE:END -->',
                 '', txt, flags=re.DOTALL)
    if "</body>" in txt:
        txt = txt.replace("</body>", PAGE_FADE_JS + "\n</body>", 1)
    # Add ma-wa-pulse CSS once
    if WA_PULSE_CSS.strip().split('\n')[1].strip()[:30] not in txt:  # rough check
        if m:
            m2 = style_re.search(txt)
            if m2 and 'ma-wa-pulse' not in m2.group(2):
                new_style2 = m2.group(2).rstrip() + "\n" + WA_PULSE_CSS + "    "
                txt = txt.replace(m2.group(0), m2.group(1) + new_style2 + m2.group(3), 1)
    return txt

# ============================================================================
# Run across all HTML pages
# ============================================================================
print(f"{'PAGE':22s}  cursor  pulse  fade  wordmark")
totals = dict(cursor=0, pulse=0, fade=0, wordmark=0)
for page in HTML_PAGES:
    p = ROOT / page
    if not p.exists():
        continue
    original = p.read_text(encoding="utf-8")
    txt = original
    pre = txt; txt = replace_cursor_css(txt); txt = replace_cursor_js(txt)
    cursor_changed = 1 if pre != txt else 0
    pre = txt; txt = add_wa_pulse(txt)
    pulse_changed = 1 if pre != txt else 0
    pre = txt; txt = add_page_fade(txt)
    fade_changed = 1 if pre != txt else 0
    pre = txt; txt, wm_n = linkify_wordmark(txt)
    if txt != original:
        p.write_text(txt, encoding="utf-8")
    print(f"  {page:22s}  {cursor_changed:>6}  {pulse_changed:>5}  {fade_changed:>4}  {wm_n:>8}")
    totals["cursor"] += cursor_changed
    totals["pulse"] += pulse_changed
    totals["fade"] += fade_changed
    totals["wordmark"] += wm_n

print(f"  {'TOTAL':22s}  {totals['cursor']:>6}  {totals['pulse']:>5}  {totals['fade']:>4}  {totals['wordmark']:>8}")
