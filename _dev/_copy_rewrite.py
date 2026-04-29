#!/usr/bin/env python3
"""Comprehensive copy rewrite: replace luxury-Sandton fictional copy with
accurate Ma Pools Construction copy across every page. Voice: plain, direct,
director-led, comprehensive scope (build → renovate → equip → repair → service
+ paving/tiles/plumbing/garden). Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAGES = ["index.html", "services.html", "gallery.html", "testimonials.html",
         "book.html", "about.html", "privacy.html", "terms.html",
         "404.html", "thank-you.html"]

# ---------------------------------------------------------------------------
# Phrase replacements — order matters: longest match first to avoid clobbers
# ---------------------------------------------------------------------------
# Each pair: (old_string, new_string).
PAIRS = [
    # ---- Brand stub email (rebrand step left this; switch to real Gmail) ----
    ("concierge@mapoolsconstruction.co.za", "mapoolsconstruction@gmail.com"),

    # ---- Residual address fragments missed by rebrand ----
    ("42 Sandton Drive, Sandhurst, Gauteng, 2196",
     "331B Utekwane Street, Zone 7, Meadowlands, 1852"),
    ("Waterfall City, Midrand", "Meadowlands, Soweto"),
    ("Sandton, Gauteng", "Meadowlands, Soweto"),
    ("e.g. Waterfall Estate, Midrand", "e.g. Diepkloof, Soweto / Roodepoort"),
    ("j.smith@luxuryestate.co.za", "you@example.com"),

    # =====================================================================
    # INDEX (landing page) — hero, sections, footer, trust copy
    # =====================================================================
    ("Gauteng's Premier Certification", "MEADOWLANDS · GAUTENG"),
    ("Curating Pristine Serenity for Elite Estates",
     "Pool builds, repairs, and care across Gauteng."),
    ("Uncompromising pool maintenance for the architectural gems of Gauteng. Precision engineering meets aesthetic perfection.",
     "Director-led pool construction, renovation, equipment installation, and ongoing care — plus paving, tiling, plumbing, and garden services. Servicing all of Gauteng from our base in Meadowlands, Soweto."),
    ("Request Exclusive Consult", "Get a Free Quote"),
    ("Our Portfolio", "See Our Work"),
    (">PREMIUM SERVICES<", ">WHAT WE DO<"),
    ("Architectural Care Solutions",
     "From the first dig to the last filter sand change."),
    ("We provide a bespoke maintenance ecosystem designed specifically for high-capacity, luxury residential pools.",
     "We handle the whole pool lifecycle: new builds, renovations, equipment, plumbing, repairs, and regular service. Plus paving, tiling, ceiling, and garden work — one contractor, one director, one accountable quote."),
    ("VIEW ALL PACKAGES", "SEE ALL SERVICES"),
    ("VIEW ALL SERVICES", "SEE ALL SERVICES"),
    ("A luxury pool is more than a recreational space; it is a significant architectural asset. Our technicians are trained in the specific requirements of Gauteng’s climate, ensuring your investment remains in immaculate condition year-round.",
     "Whether you're building a new pool, renovating an old one, fixing a leaking pump, or just need the filter sand changed — we handle it. One contractor for your pool, your paving, and your plumbing. Direct line to the director."),
    ("A luxury pool is more than a recreational space; it is a significant architectural asset. Our technicians are trained in the specific requirements of Gauteng's climate, ensuring your investment remains in immaculate condition year-round.",
     "Whether you're building a new pool, renovating an old one, fixing a leaking pump, or just need the filter sand changed — we handle it. One contractor for your pool, your paving, and your plumbing. Direct line to the director."),
    ("Schedule Your Exclusive Water Quality Consultation",
     "Send Us a Quick Message"),
    ("Premier pool maintenance services for Gauteng's most exclusive private residences.",
     "Pool construction, renovation, repairs, and care across Gauteng."),
    ("Precision in Tranquility.", "Pool builds, repairs, and care across Gauteng."),
    ("Precision in Tranquility", "Pool builds, repairs, and care across Gauteng"),

    # =====================================================================
    # SERVICES — hero + footer + signature stamp + booking CTA
    # =====================================================================
    ("Premier Gauteng Pool Care", "POOL & CONSTRUCTION SERVICES"),
    ("Service Excellence for <br/>Pristine Estate Living",
     "Pool builds, renovations, repairs, and care."),
    ("Service Excellence for Pristine Estate Living",
     "Pool builds, renovations, repairs, and care."),
    ("Ma Pools Construction provides bespoke maintenance solutions for luxury properties across Gauteng. From precision chemistry to eco-efficient upgrades, we ensure your aquatic sanctuary remains flawless.",
     "From new construction through to filter changes and pump repairs — Ma Pools Construction handles every stage of pool ownership across Gauteng. Plus paving, tiling, ceiling, plumbing, and garden services. Director-led, fixed quotes, accountable timelines."),
    ("Every service is backed by our signature stamp of quality. We don't just maintain pools; we preserve your lifestyle assets in Gauteng's most exclusive estates.",
     "Every job is led by our founding director, Mkhacani Amos Chauke — and quoted upfront. No call centres, no middlemen, no surprise add-ons."),
    ("Ready for <br/>Crystal Clarity?", "Ready to <br/>start?"),
    ("Ready for Crystal Clarity?", "Ready to start?"),
    ("Premier pool maintenance services tailored for Gauteng's most prestigious homes and private estates.",
     "Pool builds, renovations, repairs, and care across Gauteng — director-led."),

    # ---- Bento card #2 (Technical Repairs) inline copy ----
    ("Specialized troubleshooting for complex hydraulic and electrical systems. We fix what others cannot.",
     "Pump repairs, leak detection, jacuzzi leak repair, motor pump installation, filter sand changes, timer install — we fix what others walk away from."),
    (">Pump Repair<", ">Pump Repair<"),  # keep
    (">Leak Detection<", ">Jacuzzi Leaks<"),
    (">Chlorinators<", ">Filter Sand<"),

    # ---- Bento card #3 (Acid Washes → Equipment & Plumbing) ----
    (">Professional Acid Washes<", ">Equipment & Plumbing<"),
    ("Revitalize aging plaster and remove deep stains with our controlled chemical treatment. Restores that &quot;new pool&quot; brilliance in 48 hours.",
     "Pool heating systems, plumbing installation, motor pumps, timers, and pool covers — supplied, installed, and serviced. We also build fish ponds and install jacuzzis."),
    ("Revitalize aging plaster and remove deep stains with our controlled chemical treatment. Restores that \"new pool\" brilliance in 48 hours.",
     "Pool heating systems, plumbing installation, motor pumps, timers, and pool covers — supplied, installed, and serviced. We also build fish ponds and install jacuzzis."),
    ("Stain removal &amp; algae deep-clean", "Heating · Plumbing · Pumps · Timers · Covers"),
    ("Stain removal & algae deep-clean", "Heating · Plumbing · Pumps · Timers · Covers"),
    (">RESULT ORIENTED<", ">EVERY SYSTEM<"),

    # ---- Bento card #4 (Eco-Friendly Equipment → Beyond the Pool) ----
    (">Eco-Friendly Equipment<", ">Beyond the Pool<"),
    ("Upgrade to sustainable pool management. Reduce electricity costs by up to 70% and minimize chemical dependency.",
     "We don't just do pools. Paving, floor tiles, ceilings, house and office plumbing, garden services — one contractor, one quote."),
    (">LATEST TECH<", ">FULL CONTRACTOR<"),
    (">Variable Speed<", ">Paving<"),
    ("Intelligent pump flow", "Driveway, patio, pool deck"),
    (">UV Sterilizers<", ">Plumbing<"),
    ("Chemical-free sanitation", "House & office, full install"),

    # ---- Bento card #1 (Weekly Maintenance → Pool Construction) ----
    (">Weekly Maintenance<", ">Pool Construction & Renovation<"),
    ("Our flagship white-glove service. Comprehensive cleaning, chemical balancing, and equipment health checks conducted with clockwork precision.",
     "New pool construction, complete renovations, marblite finishing, fiberglass installation, and fish pond builds. Quoted upfront, built by our own team."),
    ("Precision pH and Chlorine balancing", "New pool construction, full project management"),
    ("Multi-point pump and filter inspection", "Renovations, marblite, fiberglass"),
    ("Surface skimming and robotic sweep optimization", "Fish ponds, pool covers, pool services"),

    # ---- Schema service entries ----
    ('"name": "Weekly Maintenance"', '"name": "Pool Construction & Renovation"'),
    ('"name": "Professional Acid Washes"', '"name": "Pool Equipment & Plumbing"'),
    ('"name": "Eco-Friendly Equipment Upgrades"', '"name": "Paving, Tiling & General Construction"'),
    ('"name": "Estate Concierge"', '"name": "Pool Services & Maintenance"'),
    ('"serviceType": "Pool Acid Wash and Restoration"',
     '"serviceType": "Pool Equipment & Plumbing Installation"'),
    ('"serviceType": "Eco-Friendly Pool Equipment Installation"',
     '"serviceType": "Paving, Tiling, Ceiling & Plumbing"'),
    ('"serviceType": "Pool Concierge Service"',
     '"serviceType": "Pool Services and Maintenance"'),
    ('"serviceType": "Premium Pool Maintenance"',
     '"serviceType": "Pool Construction and Renovation"'),
    ("White-glove weekly cleaning, precision pH and chlorine balancing, multi-point pump and filter inspection, surface skimming and robotic sweep optimisation.",
     "New pool construction, full renovations, marblite finishing, fiberglass installation, fish pond construction, and pool cover supply & installation."),
    ("White-glove weekly cleaning, precision pH and chlorine balancing, multi-point pump and filter inspection, surface skimming and robotic sweep optimisation",
     "New pool construction, full renovations, marblite finishing, fiberglass installation, fish pond construction, and pool cover supply & installation"),
    ("Specialist troubleshooting for hydraulic and electrical pool systems, including pump repair, leak detection, and chlorinator service.",
     "Pump repair, leak detection, motor pump installation, filter sand changes, timer installation, jacuzzi installation and leak repair."),
    ("Controlled chemical treatment that revitalises aging plaster, removes deep stains and algae, and restores new-pool brilliance in approximately 48 hours.",
     "Pool heating systems, pool plumbing installation, motor pumps, timers, and pool covers supplied and installed."),
    ("Installation of variable-speed pumps, UV sterilisers and saline systems that reduce electricity consumption by up to 70% and minimise chemical dependency.",
     "Paving (driveways, patios, pool decks), floor tiles, ceiling installation, house and office plumbing, and garden services."),
    ("Fully managed monthly pool service with 24/7 priority emergency support, performance audits, and Gold Certification.",
     "Regular pool services, water testing, equipment checks, and ad-hoc cleaning — flexible plans matched to your pool and budget."),

    # =====================================================================
    # GALLERY — hero, captions, descriptions, footer
    # =====================================================================
    ("A curated showcase of Gauteng's most prestigious aquatic environments, maintained with surgical precision and aesthetic care.",
     "A selection of pool builds, renovations, and installations completed by Ma Pools Construction. Project photography is being added as we publish each completed job."),
    ("Defining the standard of aquatic excellence for Gauteng's most exclusive residential addresses.",
     "Pool construction and care across Gauteng — director-led, all the trades you need."),

    # ---- Gallery card titles & descriptions ----
    (">Steyn City Residence<", ">New Pool Build<"),
    (">Sandhurst Courtyard<", ">Lap Pool Project<"),
    (">Meyersdal Eco Estate<", ">Family Pool & Deck<"),
    (">Mansion Pool<", ">Modern Pool Build<"),
    (">Modern Patio<", ">Pool Deck Project<"),
    (">Pool Detail<", ">Tile & Finish Detail<"),
    (">Tropical Garden Pool<", ">Garden Pool Build<"),

    # ---- Schema gallery entries ----
    ('"name": "Steyn City Residence"', '"name": "New Pool Build"'),
    ('"description": "Precision chemical balance and weekly tile detailing at a Steyn City estate pool."',
     '"description": "New pool construction project — full build, finish, and equipment install."'),
    ('"name": "Sandhurst Courtyard"', '"name": "Lap Pool Project"'),
    ('"description": "Filtration system optimisation for a narrow architectural lap pool in a Sandhurst courtyard."',
     '"description": "Narrow lap-pool installation with filtration and timer setup."'),
    ('"name": "Meyersdal Eco Estate"', '"name": "Family Pool & Deck"'),
    ('"description": "Eco-friendly saline systems delivering five-star clarity at Meyersdal Eco Estate."',
     '"description": "Family-home pool with surrounding paving and pool cover."'),

    # =====================================================================
    # BOOK — hero, form, footer, trust line
    # =====================================================================
    ("Exclusive Gauteng Service", "FREE QUOTE"),
    ("Secure your position in our elite maintenance circle. We provide precision chemistry and architectural care for Gauteng's most prestigious private estates.",
     "Tell us about your project — pool, paving, plumbing, jacuzzi, anything. We'll come back with a quote within one business day. WhatsApp is fastest."),
    ("Secure your position in our elite maintenance circle.",
     "Tell us about your project — we'll quote within one business day."),
    ("The standard in aquatic luxury for Gauteng's premier estates. Professionalism defined by silence and clarity.",
     "Pool construction and care across Gauteng — director-led, accountable, accessible."),

    # ---- Book form select options ----
    (">Infinity / Rim Flow<", ">Infinity / Rim Flow<"),  # keep
    (">Indoor Lap Pool<",     ">Lap Pool<"),
    (">Natural Bio-Pool<",    ">Fibreglass Pool<"),
    (">Classic Geometric<",   ">Concrete / Marblite Pool<"),
    (">Weekly Premier Care<", ">New Pool Construction<"),
    (">Water Revival System<", ">Renovation / Resurface<"),
    (">Smart Automation Install<", ">Pump / Equipment / Plumbing<"),
    (">Special Event Preparation<", ">Regular Pool Service<"),
    ('value="weekly">',  'value="new_build">'),
    ('value="revival">', 'value="renovation">'),
    ('value="automation">', 'value="equipment">'),
    ('value="once_off">', 'value="service">'),
    ('value="rim_flow">', 'value="infinity">'),
    ('value="indoor">',  'value="lap">'),
    ('value="natural">', 'value="fibreglass">'),
    ('value="standard">', 'value="concrete">'),

    # =====================================================================
    # ABOUT — hero, sections, contact, copy
    # =====================================================================
    (">SINCE 2014<", ">MEADOWLANDS · GAUTENG<"),
    ("Excellence in every drop.", "Built by hand. Run by the director."),
    ("Maintaining Gauteng's most prestigious pool estates with surgical precision and uncompromising care.",
     "Ma Pools Construction is a Soweto-based pool and construction business led by founding director Mkhacani Amos Chauke. We service homes and businesses across Gauteng — from new pool builds and renovations to plumbing, paving, and ongoing pool care."),
    ("Premier Standard Certified", "DIRECTOR-LED · ACCOUNTABLE"),
    (">Commitment to Serenity<", ">How we work.<"),
    ('At Ma Pools Construction, we believe a swimming pool is more than a recreational asset—it is a sanctuary of serenity and a statement of architectural elegance. we have provided discerning Gauteng homeowners with a seamless, "set-and-forget" pool maintenance experience.',
     "Ma Pools Construction is built around one idea: one contractor handles the whole job. New build, renovation, equipment, repair, regular service — plus paving, tiling, ceiling, plumbing, and garden work. Everything stays under one roof, accountable to the director. We say what we'll charge, we say when we'll arrive, and we don't hand off your job to anyone you didn't meet."),
    ('At Ma Pools Construction, we believe a swimming pool is more than a recreational asset—it is a sanctuary of serenity and a statement of architectural elegance. we have provided discerning Gauteng homeowners with a seamless, &quot;set-and-forget&quot; pool maintenance experience.',
     "Ma Pools Construction is built around one idea: one contractor handles the whole job. New build, renovation, equipment, repair, regular service — plus paving, tiling, ceiling, plumbing, and garden work. Everything stays under one roof, accountable to the director. We say what we'll charge, we say when we'll arrive, and we don't hand off your job to anyone you didn't meet."),
    (">Precision Chemical Balancing<", ">New builds & renovations<"),
    (">Structural Integrity Inspections<", ">Equipment, plumbing & repairs<"),
    (">Sustainable Filtration Solutions<", ">Paving, tiling & garden services<"),
    ("A decade of surgical precision and uncompromising care for Gauteng's most prestigious estate pools.",
     "Director-led pool construction, renovation, and care for homes and businesses across Gauteng."),
    ("A decade of precision pool care for Gauteng's prestige estates.",
     "Director-led pool construction, renovation, and care across Gauteng."),
    ("About Ma Pools Construction — Gauteng's Premier Pool Care Firm",
     "About Ma Pools Construction — Director-led pool builds & care, Gauteng"),
    ("About Ma Pools Construction — Gauteng&#x27;s Premier Pool Care Firm",
     "About Ma Pools Construction — Director-led pool builds & care, Gauteng"),

    # =====================================================================
    # METATAG / SOCIAL DESCRIPTIONS (HTML-encoded variants)
    # =====================================================================
    ("Discreet, expert pool maintenance for luxury estates across Sandton, Bryanston, Hyde Park &amp; Pretoria. Precision water chemistry. Book a private consultation.",
     "Pool construction, renovations, repairs, equipment, plumbing &amp; care across Gauteng. Director-led from Meadowlands. WhatsApp 065 643 0603 for a free quote."),
    ("Discreet, expert pool maintenance for luxury estates across Sandton, Bryanston, Hyde Park & Pretoria. Precision water chemistry. Book a private consultation.",
     "Pool construction, renovations, repairs, equipment, plumbing & care across Gauteng. Director-led from Meadowlands. WhatsApp 065 643 0603 for a free quote."),
    ("Discreet, expert pool maintenance for luxury estates across Sandton, Bryanston, Hyde Park &amp; Pretoria. Book a private consultation.",
     "Pool construction, renovations, repairs &amp; care across Gauteng. WhatsApp 065 643 0603 for a free quote."),
    ("Discreet, expert pool maintenance for Gauteng&#x27;s most prestigious estates. Book a private consultation.",
     "Pool construction, renovations, repairs &amp; care across Gauteng. Free quote in 24 hours."),
    ("Ma Pools Construction | Premium Pool Care for Gauteng&#x27;s Finest Homes",
     "Ma Pools Construction | Pool builds, renovations &amp; care across Gauteng"),
    ("Ma Pools Construction | Premium Pool Care for Gauteng's Finest Homes",
     "Ma Pools Construction | Pool builds, renovations & care across Gauteng"),
    ("Ma Pools Construction | Premium Pool Care for Gauteng",
     "Ma Pools Construction | Pool builds & care across Gauteng"),
    ("Premium pool maintenance and care for Gauteng's most prestigious private estates.",
     "Pool construction, renovations, repairs and care across Gauteng — director-led."),
    ("Premium pool care for Gauteng's most prestigious estates.",
     "Pool construction, renovation, repairs and care across Gauteng."),
    ("Bespoke pool care for Gauteng estates: white-glove weekly maintenance, technical repairs, acid washes, eco-equipment upgrades. Precision chemistry, 24h response.",
     "Pool construction, renovations, equipment installs, repairs and care across Gauteng. Plus paving, tiling, plumbing &amp; garden services. WhatsApp 065 643 0603."),
    ("Weekly maintenance, technical repairs, acid washes &amp; eco-equipment upgrades for Gauteng&#x27;s most prestigious estates.",
     "Pool builds, renovations, equipment, repairs &amp; service across Gauteng. WhatsApp 065 643 0603 for a free quote."),
    ("Curated portfolio of Gauteng&#x27;s most prestigious pools under Ma Pools Construction care — Steyn City, Sandhurst, Meyersdal Eco Estate and more.",
     "A selection of pool builds, renovations and installations completed by Ma Pools Construction across Gauteng."),
    ("A curated showcase of Gauteng&#x27;s most prestigious aquatic environments, maintained with surgical precision.",
     "Pool builds, renovations and installations completed across Gauteng."),
    ("A curated showcase of Gauteng&#x27;s most prestigious pools.",
     "Selected work from Ma Pools Construction."),
    ("Architectural infinity pool at Steyn City under Ma Pools Construction care",
     "Pool installation completed by Ma Pools Construction"),

    # OG image alt residuals
    ("Ma Pools Construction — pristine infinity pool at a Sandton luxury estate at golden hour",
     "Ma Pools Construction — pool construction and care across Gauteng"),
    ("Ma Pools Construction technician calibrating water chemistry at a luxury Gauteng pool",
     "Ma Pools Construction — pool construction and care services across Gauteng"),

    # =====================================================================
    # GENERIC LUXURY-PHRASE CLEANUP — these often slip through
    # =====================================================================
    # alt-text and inline copy stragglers
    ("luxury Gauteng pool",       "Gauteng pool"),
    ("luxury Gauteng estate",     "Gauteng property"),
    ("luxury estate",             "property"),
    ("luxury swimming pool",      "swimming pool"),
    ("luxury pool",               "pool"),
    ("luxury residential",        "residential"),
    ("Sandhurst luxury estate",   "Gauteng property"),
    ("most prestigious",          "across"),
    ("most exclusive",            "across"),
    ("prestigious estate",        "Gauteng project"),
    ("exclusive estates",         "homes and estates"),
    ("exclusive private estates", "homes and estates"),
    ("private estates",           "homes and estates"),
    ("estate pool",               "pool"),
    ("Modern architectural infinity pool at sunset overlooking a Gauteng valley with warm glowing lights",
     "Modern infinity pool at sunset overlooking a Gauteng valley"),
    ("Pristine luxury swimming pool in a modern Gauteng garden with clear turquoise water and minimalist architecture",
     "Modern swimming pool in a Gauteng garden with clear turquoise water"),
    ("Stunning aerial view of a geometric modern pool integrated into a minimalist luxury estate with travertine tiling",
     "Aerial view of a geometric modern pool with travertine tiling"),
    ("Aerial view of a geometric modern pool integrated into a minimalist Sandhurst luxury estate with travertine decking",
     "Aerial view of a geometric modern pool with travertine decking"),
    ("Luxury poolside lounge area with modern white furniture and a clean blue pool under bright sunlight",
     "Poolside lounge area with white furniture and a clean blue pool"),
    ("Luxury poolside lounge area with modern white furniture beside a clean blue Gauteng estate pool",
     "Poolside lounge area with white furniture beside a clean blue Gauteng pool"),
    ("Luxury infinity pool at a Steyn City residence overlooking a Gauteng sunset with crystal clear blue water",
     "Infinity pool overlooking a Gauteng sunset with crystal-clear blue water"),
    ("Narrow lap pool in a minimalist Sandhurst courtyard with clean architectural lines and morning shadows",
     "Narrow lap pool in a minimalist courtyard with clean lines and morning shadows"),
    ("Geometric swimming pool reflecting a high-end architectural villa under Gauteng's blue skies",
     "Geometric swimming pool reflecting a modern villa under Gauteng's blue skies"),
    ("Luxury pool deck with designer lounge chairs beside shimmering azure estate water on a clear Gauteng day",
     "Pool deck with lounge chairs beside shimmering blue water on a clear Gauteng day"),
    ("Panoramic Meyersdal estate pool with glass railings and limestone flooring overlooking a valley",
     "Family pool with glass railings and limestone deck overlooking a valley"),
    ("Architectural infinity pool at The Obsidian Residence overlooking a Gauteng sunset with concrete edges and crystal clear water",
     "Modern infinity pool overlooking a Gauteng sunset with concrete edges and clear water"),
    ("Modern minimalist Gauteng estate with floor-to-ceiling glass windows reflecting a sunset over the pool deck",
     "Modern minimalist Gauteng home with glass windows reflecting a sunset over the pool deck"),
    ("Stylised map of Johannesburg Northern Suburbs marking the Ma Pools Construction office in Sandhurst, Gauteng",
     "Map of Gauteng marking the Ma Pools Construction office in Meadowlands, Soweto"),
    ("Modern architectural infinity pool at sunset overlooking a lush Gauteng valley with warm glowing lights and deep blue water",
     "Modern infinity pool at sunset over a Gauteng valley with deep blue water"),
    ("Pool installation completed by Ma Pools Construction — pristine infinity pool at a Sandton luxury estate at golden hour",
     "Pool installation completed by Ma Pools Construction — Gauteng project at golden hour"),
    ("Ma Pools Construction technician in uniform testing pool water quality at a luxury Gauteng estate with professional tools",
     "Ma Pools Construction technician testing pool water quality on a Gauteng project"),
    ("Pool installation completed by Ma Pools Construction — pristine infinity pool at a Sandton at golden hour",
     "Pool installation completed by Ma Pools Construction at golden hour"),
    ("at a Sandton luxury", "in Gauteng"),

    # Address/locality stragglers in alt text & body copy
    ("at a Sandton",   "in Gauteng"),
    ("Sandhurst Estate",  "Gauteng property"),
    ("Bryanston Country Club", "Gauteng property"),
    ("Waterfall Equestrian", "Gauteng property"),
    ("Hyde Park Resident", "Gauteng customer"),
    ("Hyde Park",            "Gauteng"),
    ("Bryanston",            "Gauteng"),
    ("Sandhurst",            "Meadowlands"),  # last — narrative use only
    ("Steyn City",           "Gauteng project"),
    ("Meyersdal Eco Estate", "Gauteng project"),
    ("Waterfall Estate",     "Gauteng project"),
    ("Sandton",              "Gauteng"),  # final fallback for narrative
]

def apply(text: str) -> tuple[str, int]:
    n = 0
    for old, new in PAIRS:
        if old in text:
            n += text.count(old)
            text = text.replace(old, new)
    return text, n

# Run across HTML + key txt/json reference files
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
        rel = p.relative_to(ROOT)
        print(f"  {str(rel):45s}  {n:>4d} replacements")
        total += n

print(f"\nTotal copy replacements: {total}")
