#!/usr/bin/env python3
"""Builds the Interlake Construction static site into ../site.
Edit content here and re-run: python3 src/build.py  (writes the published site to docs/)"""
import json, os, datetime

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
LIVE_URL = "https://interlakenw.github.io"  # where the site is served now; change to SITE after domain switch
WEB3FORMS_KEY = "9a5e8652-03c0-4c27-9bf8-6eed6fa8b5c8"  # Web3Forms access key (public-safe). Submissions email office@interlakenw.com
SITE = "https://www.interlakenw.com"
BIZ = {
    "name": "Interlake Construction LLC",
    "short": "Interlake Construction",
    "phone": "(206) 659-5021",
    "tel": "+12066595021",
    "email": "office@interlakenw.com",
    "street": "4616 25th Ave NE #51",
    "city": "Seattle", "state": "WA", "zip": "98105",
    "license": "INTERCL764PA",
    "lat": 47.6625, "lng": -122.2995,
}
TODAY = datetime.date.today().isoformat()

REGIONS = {
    "Skagit & Snohomish County": ["Mount Vernon", "Burlington", "Stanwood", "Arlington", "Marysville", "Lake Stevens",
                                  "Everett", "Mukilteo", "Mill Creek", "Lynnwood", "Edmonds", "Bothell"],
    "Seattle & North King County": ["Seattle", "Shoreline", "Lake Forest Park", "Kenmore", "Woodinville", "Mercer Island"],
    "Eastside": ["Bellevue", "Redmond", "Kirkland", "Issaquah", "Sammamish", "Newcastle"],
    "South King & Pierce County": ["Renton", "Tukwila", "Burien", "SeaTac", "Des Moines", "Kent", "Auburn",
                                   "Federal Way", "Puyallup", "Fife", "University Place", "Tacoma"],
}
ALL_CITIES = [c for v in REGIONS.values() for c in v]

ICON = {
 "phone": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5zm-2 16-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9z"/></svg>',
}

def pic(name, alt, sizes="100vw", eager=False, cls="", w=1600, h=1200):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="img/{name}-1600.webp" srcset="img/{name}-800.webp 800w, img/{name}-1600.webp 1600w" '
            f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {load}{c}>')

NAV = [("index.html", "Home"), ("services.html", "Services"), ("projects.html", "Projects"),
       ("service-areas.html", "Service Areas"), ("about.html", "About")]
SUB = [("residential.html", "Residential Remodeling"), ("commercial.html", "Commercial & Tenant Improvements"),
       ("restoration.html", "Restoration & Reconstruction")]

def header(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current or (href == "services.html" and current in [s[0] for s in SUB]) else ""
        if href == "services.html":
            sub = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{l}</a></li>' for h, l in SUB)
            items.append(f'<li class="has-sub"><a href="{href}"{cur}>{label}</a><ul>{sub}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    items.append('<li><a class="btn btn--primary" href="contact.html">Free Estimate</a></li>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container">
  <span class="hide-sm">Licensed &amp; insured general contractor · WA Lic. {BIZ['license']}</span>
  <span>Serving Mount Vernon to Tacoma · <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></span>
</div></div>
<header class="site-header"><div class="container">
  <a class="brand" href="index.html" aria-label="{BIZ['short']} home"><img src="img/logo.webp" alt="{BIZ['short']}" width="480" height="377"></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
</div></header>"""

def footer():
    svc = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in SUB)
    return f"""<section class="cta-band"><div class="container">
  <div><h2>Ready to start your project?</h2><p>Free, no-pressure estimates anywhere from Mount Vernon to Tacoma.</p></div>
  <div class="btn-row" style="margin:0"><a class="btn btn--white" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a></div>
</div></section>
<footer class="site-footer"><div class="container">
  <div class="footer-grid">
    <div><a class="footer-logo" href="index.html"><img src="img/logo-white.webp" alt="{BIZ['short']}" width="480" height="377" loading="lazy"></a>
      <p>Remodeling, tenant improvements and restoration for homes and businesses across the Puget Sound.</p></div>
    <div><h3>Services</h3><ul>{svc}<li><a href="services.html">All Services</a></li></ul></div>
    <div><h3>Company</h3><ul><li><a href="about.html">About</a></li><li><a href="projects.html">Projects</a></li><li><a href="service-areas.html">Service Areas</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h3>Contact</h3><ul>
      <li><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></li>
      <li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
      <li>{BIZ['street']}<br>{BIZ['city']}, {BIZ['state']} {BIZ['zip']}</li>
      <li>WA Contractor Lic. {BIZ['license']}</li></ul></div>
  </div>
  <div class="footer-bottom"><span>© <span id="yr">{datetime.date.today().year}</span> {BIZ['name']}. All rights reserved.</span><span>Licensed, bonded &amp; insured in Washington State</span></div>
</div></footer>
<div class="call-bar"><a href="tel:{BIZ['tel']}">Call Now</a><a href="contact.html">Free Estimate</a></div>
<script src="js/main.js" defer></script>"""

def org_schema():
    return {
        "@context": "https://schema.org", "@type": "GeneralContractor", "@id": SITE + "/#business",
        "name": BIZ["name"], "url": SITE + "/", "telephone": BIZ["tel"], "email": BIZ["email"],
        "logo": SITE + "/img/logo.png", "image": SITE + "/img/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"],
                    "addressRegion": BIZ["state"], "postalCode": BIZ["zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "areaServed": [{"@type": "City", "name": f"{c}, WA"} for c in ALL_CITIES],
        "priceRange": "$$",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Construction services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
            ["Kitchen remodeling", "Bathroom remodeling", "Whole-home remodels", "ADU / DADU construction",
             "Commercial tenant improvements", "Office build-outs", "Water damage reconstruction",
             "Fire damage reconstruction", "Mold damage repair"]]},
        "identifier": {"@type": "PropertyValue", "name": "WA Contractor License", "value": BIZ["license"]},
    }

def page(file, title, desc, body, current=None, schema=None, crumbs=None, og_img="og-image.jpg", noindex=False):
    canonical = SITE + "/" + ("" if file == "index.html" else file.replace(".html", ""))
    blocks = [org_schema()]
    if crumbs:
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(crumbs)]})
    if schema: blocks += schema
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, separators=(",", ":"))}</script>' for b in blocks)
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/img/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#d7181f">
<link rel="icon" href="img/icon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="img/icon-180.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
{ld}
</head>
<body>
{header(current or file)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    with open(os.path.join(OUT, file), "w") as f:
        f.write(html)
    return canonical

def page_hero(h1, sub, img, crumbs):
    bc = " / ".join(f'<a href="{u or "index.html"}">{n}</a>' for n, u in crumbs[:-1]) + f" / {crumbs[-1][0]}"
    return f"""<section class="page-hero"><picture>{pic(img, "", eager=True)}</picture><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb">{bc}</nav><h1>{h1}</h1><p>{sub}</p>
<div class="btn-row"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a></div>
</div></section>"""

TESTIMONIALS = [
    ("I was impressed by the clear communication and timeliness throughout the project.", "Michael Jameson", "Burien, WA"),
    ("I couldn't be happier with the quality of work and their commitment to getting everything just right. Highly recommended!", "Jessica Harlow", "Redmond, WA"),
    ("Interlake Construction made the entire process stress-free, and the results were beyond our expectations.", "Sarah Mitchell", "SeaTac, WA"),
    ("The team was courteous, efficient, and incredibly skilled. They transformed my space and made it a dream come true.", "David Walters", "Renton, WA"),
]
def testimonials_html():
    q = "".join(f'<figure class="quote reveal"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>“{t}”</blockquote><figcaption>{n}<span>{c}</span></figcaption></figure>' for t, n, c in TESTIMONIALS)
    return f"""<section class="section section--alt"><div class="container">
<div class="center"><span class="eyebrow">Testimonials</span><h2>What our clients say</h2></div>
<div class="grid grid-3" style="grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:2.5rem">{q}</div></div></section>"""

def faq_html(items):
    d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<div class="faq">{d}</div>', schema

def service_schema(name, desc, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "provider": {"@id": SITE + "/#business"}, "url": SITE + "/" + url,
            "areaServed": {"@type": "AdministrativeArea", "name": "Puget Sound region, Washington"}}

# ---------------------------------------------------------------- HOME
def build_home():
    cards = [
        ("residential.html", "kitchen-remodel", "Modern kitchen remodel with island and gas range", "Residential Remodeling",
         "Kitchens, bathrooms, whole-home remodels, additions and ADU/DADU builds — done right the first time."),
        ("commercial.html", "fitness-studio-tenant-improvement", "Fitness studio tenant improvement with LED lighting", "Commercial & Tenant Improvements",
         "Tenant improvements, office build-outs, storefronts and ADA upgrades that keep your business on schedule."),
        ("restoration.html", "water-damage-demolition", "Water-damaged room opened up for reconstruction", "Restoration & Reconstruction",
         "Rebuilding after water, fire and mold damage — from drywall and flooring to full kitchen and bath rebuilds."),
    ]
    c = "".join(f'<article class="card reveal"><a href="{h}" tabindex="-1" aria-hidden="true">{pic(img, alt, "(max-width:900px) 100vw, 33vw", w=800, h=600)}</a><div class="card-body"><h3><a href="{h}" style="color:inherit;text-decoration:none">{t}</a></h3><p>{d}</p><a class="card-link" href="{h}">Learn more<span class="hidden"> about {t}</span></a></div></article>' for h, img, alt, t, d in cards)
    body = f"""<section class="hero"><picture>{pic("kitchen-remodel", "Finished open-concept kitchen remodel by Interlake Construction", eager=True)}</picture>
<div class="container">
  <span class="eyebrow">Puget Sound General Contractor</span>
  <h1>Transforming Spaces, Restoring Confidence</h1>
  <p>Your trusted partner for remodeling, tenant improvements and restoration — serving homes and businesses from Mount Vernon to Tacoma.</p>
  <div class="btn-row"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="projects.html">See Our Work</a></div>
  <div class="hero-badges"><span>Licensed &amp; insured</span><span>Residential &amp; commercial</span><span>Free estimates</span></div>
</div></section>

<section class="section"><div class="container">
<div class="center"><span class="eyebrow">What we do</span><h2>Construction services built around you</h2>
<p class="lead">At Interlake Construction LLC, we pride ourselves on delivering exceptional craftsmanship and unparalleled customer service — whether we're renovating your home, upgrading your commercial space or restoring a property after damage.</p></div>
<div class="grid grid-3" style="margin-top:2.5rem">{c}</div>
</div></section>

<section class="section section--dark"><div class="container grid grid-2">
<div>{pic("modern-staircase", "Custom open-riser staircase with cable railing", "(max-width:900px) 100vw, 50vw", cls="rounded-img")}</div>
<div><span class="eyebrow">Why Interlake</span><h2>Done right. On time. With respect for your space.</h2>
<div class="grid" style="gap:1rem;margin-top:1.5rem">
<div><h3>Quality</h3><p>The job will get done right the first time.</p></div>
<div><h3>Trust</h3><p>Professional, certified technicians you can trust in your home or business.</p></div>
<div><h3>Integrity</h3><p>We respect your time and keep our schedule — with clear communication from estimate to final walkthrough.</p></div>
</div></div></div></section>

<section class="section"><div class="container">
<div class="center"><span class="eyebrow">Recent work</span><h2>Projects across the Puget Sound</h2></div>
<div class="gallery" style="margin-top:2.5rem">
<figure class="reveal">{pic("commercial-storefront-buildout", "Commercial storefront shell build-out with glass entry", "(max-width:600px) 100vw, 33vw", w=800, h=600)}<figcaption>Storefront Build-Out<small>Commercial</small></figcaption></figure>
<figure class="reveal">{pic("home-addition-exterior", "Two-story home exterior after renovation", "(max-width:600px) 100vw, 33vw", w=800, h=600)}<figcaption>Home Renovation<small>Residential</small></figcaption></figure>
<figure class="reveal">{pic("office-stone-feature-wall", "Stacked stone feature wall installed in office lobby", "(max-width:600px) 100vw, 33vw", w=800, h=600)}<figcaption>Office Feature Wall<small>Commercial</small></figcaption></figure>
</div>
<div class="center"><a class="btn btn--outline" href="projects.html" style="margin-top:2rem">View all projects</a></div>
</div></section>

{testimonials_html()}

<section class="section"><div class="container grid grid-2">
<div><span class="eyebrow">Service area</span><h2>From Mount Vernon to Tacoma</h2>
<p class="lead">Based in Seattle, we work throughout Skagit, Snohomish, King and Pierce counties — including Everett, Lynnwood, Bellevue, Redmond, Renton, Kent and Tacoma.</p>
<a class="btn btn--outline" href="service-areas.html">See all service areas</a></div>
<div>{pic("multifamily-framing", "Multifamily building framing and sheathing in progress", "(max-width:900px) 100vw, 50vw", cls="rounded-img", w=1200, h=1600)}</div>
</div></section>"""
    page("index.html", "Interlake Construction | Remodeling & Restoration Contractor, Seattle WA",
         "Seattle general contractor for home remodeling, commercial tenant improvements and water/fire damage reconstruction. Serving Mount Vernon to Tacoma. Free estimates: (206) 659-5021.",
         body)

# ---------------------------------------------------------------- SERVICES HUB
def build_services():
    rows = [
        ("residential.html", "deck-home-renovation", "Home renovation with new deck", "Residential", "Remodeling for the way you live",
         ["Custom homes & whole-home remodels", "Kitchen & bathroom remodels", "ADU / DADU construction", "Framing, drywall & finishing", "Flooring & tile", "Plumbing, electrical, HVAC & roofing"]),
        ("commercial.html", "commercial-storefront-buildout", "Commercial storefront build-out", "Commercial", "Spaces that work as hard as you do",
         ["Tenant improvements & build-outs", "Office & storefront construction", "Mechanical & electrical installs", "Insulation, drywall & paint", "High-traffic commercial flooring", "ADA ramps & accessibility upgrades"]),
        ("restoration.html", "wall-reconstruction", "Wall opened to studs for reconstruction", "Reconstruction", "Rebuilding after water, fire & mold",
         ["Drywall, wall & ceiling rebuilds", "Flooring replacement", "Interior & exterior painting", "Custom cabinetry & trim", "Kitchen & bathroom rebuilds", "Full remodels after loss"]),
    ]
    sec = ""
    for i, (h, img, alt, eb, t, items) in enumerate(rows):
        li = "".join(f"<li>{x}</li>" for x in items)
        imgcol = f'<div>{pic(img, alt, "(max-width:900px) 100vw, 50vw", cls="rounded-img")}</div>'
        txt = f'<div><span class="eyebrow">{eb}</span><h2>{t}</h2><ul class="checklist cols-2">{li}</ul><div class="btn-row"><a class="btn btn--primary" href="{h}">{eb} services</a></div></div>'
        sec += f'<section class="section{" section--alt" if i % 2 else ""}" id="{eb.lower()}"><div class="container grid grid-2">{imgcol + txt if i % 2 == 0 else txt + imgcol}</div></section>'
    crumbs = [("Home", ""), ("Services", "services")]
    body = page_hero("Comprehensive Construction Services Tailored to Your Needs",
                     "Residential, commercial and reconstruction services — new builds, upgrades and repairs after damage.",
                     "multifamily-building", [("Home", "index.html"), ("Services", "")]) + sec
    page("services.html", "Construction Services | Residential, Commercial & Restoration | Interlake",
         "Full-service general contractor: home remodels, ADUs, commercial tenant improvements and water, fire & mold damage reconstruction across the Puget Sound.",
         body, crumbs=crumbs)

def service_page(file, h1, sub, hero, title, desc, intro, sections, faqs, gallery, name):
    s = ""
    for t, d, items in sections:
        li = "".join(f"<li>{x}</li>" for x in items)
        s += f'<div class="value reveal"><h3>{t}</h3><p>{d}</p><ul class="checklist">{li}</ul></div>'
    g = "".join(f'<figure class="reveal">{pic(i, a, "(max-width:600px) 100vw, 33vw", w=800, h=600)}<figcaption>{c}</figcaption></figure>' for i, a, c in gallery)
    fq, fschema = faq_html(faqs)
    body = page_hero(h1, sub, hero, [("Home", "index.html"), ("Services", "services.html"), (name, "")]) + f"""
<section class="section"><div class="container">
<div class="center"><p class="lead">{intro}</p></div>
<div class="grid grid-3" style="margin-top:2.5rem">{s}</div></div></section>
<section class="section section--alt"><div class="container">
<div class="center"><span class="eyebrow">Our work</span><h2>{name} projects</h2></div>
<div class="gallery" style="margin-top:2rem">{g}</div></div></section>
<section class="section"><div class="container" style="max-width:820px">
<div class="center"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>{fq}</div></section>
{testimonials_html()}"""
    crumbs = [("Home", ""), ("Services", "services"), (name, file.replace(".html", ""))]
    page(file, title, desc, body, crumbs=crumbs, schema=[service_schema(name, desc, file.replace(".html", "")), fschema])

def build_residential():
    service_page("residential.html", "Residential Remodeling & Home Renovation",
        "Kitchens, bathrooms, whole-home remodels and ADUs across Seattle and the Puget Sound.", "kitchen-remodel",
        "Home Remodeling Contractor Seattle | Kitchens, Baths & ADUs | Interlake",
        "Kitchen and bathroom remodels, whole-home renovations and ADU/DADU construction from Mount Vernon to Tacoma. Licensed WA contractor. Free estimates.",
        "Whether you're updating one room or reimagining your whole home, our team handles every trade under one roof — so you get one point of contact, a clear schedule and work that's done right the first time.",
        [("Kitchens & Baths", "Layouts, cabinetry, counters, tile and fixtures — designed around how you actually use the space.", ["Kitchen remodels", "Bathroom remodels", "Tile & flooring", "Custom cabinetry & trim"]),
         ("Whole-Home & Additions", "From custom homes to full gut renovations and additions that add space and value.", ["Custom homes", "Whole-home remodels", "Framing, drywall & finishing", "Roofing & exteriors"]),
         ("ADUs / DADUs & Systems", "Backyard cottages, in-law units and the systems behind every great home.", ["ADU / DADU builds", "Plumbing", "Electrical", "HVAC"])],
        [("How long does a kitchen remodel take?", "Most kitchen remodels take 6–12 weeks of construction depending on scope, permits and material lead times. We give you a written schedule before work starts."),
         ("Do you handle permits?", "Yes. We manage permitting and inspections with your city or county as part of the project."),
         ("Do you build ADUs and DADUs?", "Yes — we build attached and detached accessory dwelling units, from foundation and framing through finishes."),
         ("Are estimates free?", "Yes. Contact us for a free, no-obligation estimate.")],
        [("kitchen-remodel", "Kitchen remodel", "Open-concept kitchen"), ("modern-staircase", "Modern staircase", "Custom staircase"),
         ("home-addition-exterior", "Home exterior renovation", "Exterior renovation"), ("deck-home-renovation", "Deck and home renovation", "Deck & renovation"),
         ("exterior-siding-renovation", "Exterior re-siding project", "Re-siding in progress")], "Residential")

def build_commercial():
    service_page("commercial.html", "Commercial Construction & Tenant Improvements",
        "Office build-outs, storefronts and tenant improvements delivered on schedule so you can open sooner.", "fitness-studio-tenant-improvement",
        "Tenant Improvement Contractor Seattle | Commercial Build-Outs | Interlake",
        "Commercial tenant improvements, office build-outs, storefronts and ADA upgrades in Seattle, Bellevue, Everett, Tacoma and across the Puget Sound.",
        "We help business owners, landlords and property managers turn raw or outdated space into a finished, code-compliant space — with minimal downtime and clear communication throughout.",
        [("Tenant Improvements", "Shell and second-generation space built out to your layout and brand.", ["Office build-outs", "Retail & storefronts", "Fitness & studio spaces", "Demising walls"]),
         ("Interiors & Systems", "Every trade coordinated under one contractor.", ["Framing & drywall", "Mechanical & electrical", "Insulation & paint", "High-traffic flooring"]),
         ("Accessibility & Upgrades", "Keep your space safe, compliant and welcoming.", ["ADA ramps", "Accessible restrooms", "Code upgrades", "Facility repairs"])],
        [("What is a tenant improvement (TI)?", "A tenant improvement is the build-out or renovation of commercial space to fit a specific tenant — walls, finishes, lighting, restrooms and systems."),
         ("Can you work around our business hours?", "Yes. We can schedule phased or after-hours work to keep your business running."),
         ("Do you work with landlords and property managers?", "Yes — we regularly coordinate with owners, property managers and tenants on the same project."),
         ("Do you handle ADA upgrades?", "Yes, including ramps, accessible restrooms and other accessibility improvements.")],
        [("fitness-studio-tenant-improvement", "Fitness studio TI", "Fitness studio build-out"), ("commercial-storefront-buildout", "Storefront build-out", "Storefront build-out"),
         ("office-stone-feature-wall", "Office stone feature wall", "Office feature wall"), ("multifamily-building", "Multifamily building", "Multifamily"),
         ("multifamily-framing", "Multifamily framing", "Framing & sheathing")], "Commercial")

def build_restoration():
    service_page("restoration.html", "Water, Fire & Mold Damage Reconstruction",
        "When the cleanup crew leaves, we put your home or business back together — better than before.", "water-damage-demolition",
        "Water & Fire Damage Reconstruction Seattle | Restoration Contractor | Interlake",
        "Reconstruction after water, fire and mold damage: drywall, flooring, cabinetry, kitchens and baths. Serving Seattle, Everett, Bellevue, Tacoma and the Puget Sound.",
        "Property damage is stressful. We make the rebuild simple — scoping the repairs, working with your insurance documentation and restoring your property quickly and correctly.",
        [("Structure & Walls", "Rebuilding what was removed during mitigation.", ["Drywall repair", "Wall & ceiling rebuilds", "Framing repair", "Insulation"]),
         ("Finishes", "Matching or upgrading finishes so the repair disappears.", ["Flooring replacement", "Interior & exterior paint", "Custom cabinetry & trim", "Tile"]),
         ("Full Rebuilds", "When the damage is extensive, we rebuild entire rooms.", ["Kitchen rebuilds", "Bathroom rebuilds", "Full remodels", "Code upgrades"])],
        [("Do you work with insurance companies?", "Yes. We work from your insurance scope and documentation and communicate with your adjuster as needed."),
         ("Do you do the water extraction / drying?", "Our focus is reconstruction — rebuilding after mitigation is complete. We can coordinate with your mitigation company."),
         ("Can you upgrade finishes during the rebuild?", "Yes. Many clients use the rebuild as a chance to upgrade; we'll price any upgrades separately from the insurance scope."),
         ("How quickly can you start?", "Call us at (206) 659-5021 — we prioritize damage repairs to get you back in your space fast.")],
        [("water-damage-demolition", "Water damaged room", "Water damage tear-out"), ("wall-reconstruction", "Wall reconstruction", "Wall reconstruction"),
         ("exterior-siding-renovation", "Exterior siding rebuild", "Exterior rebuild")], "Restoration")

# ---------------------------------------------------------------- PROJECTS
def build_projects():
    items = [
        ("kitchen-remodel", "Open-concept kitchen remodel", "Kitchen Remodel", "residential"),
        ("modern-staircase", "Open-riser staircase with cable railing", "Custom Staircase", "residential"),
        ("home-addition-exterior", "Two-story home exterior", "Home Renovation", "residential"),
        ("deck-home-renovation", "New deck and home renovation", "Deck & Renovation", "residential"),
        ("exterior-siding-renovation", "House wrapped for new siding", "Exterior Re-Siding", "residential"),
        ("fitness-studio-tenant-improvement", "Fitness studio tenant improvement", "Fitness Studio TI", "commercial"),
        ("commercial-storefront-buildout", "Commercial storefront shell", "Storefront Build-Out", "commercial"),
        ("office-stone-feature-wall", "Stone feature wall in office", "Office Feature Wall", "commercial"),
        ("multifamily-building", "Completed multifamily building", "Multifamily Building", "commercial"),
        ("multifamily-framing", "Multifamily framing and sheathing", "Multifamily Framing", "commercial"),
        ("water-damage-demolition", "Water damage tear-out", "Water Damage Repair", "restoration"),
        ("wall-reconstruction", "Wall opened for reconstruction", "Wall Reconstruction", "restoration"),
    ]
    g = "".join(f'<figure data-cat="{cat}">{pic(i, a, "(max-width:600px) 100vw, 33vw", w=800, h=600)}<figcaption>{t}<small>{cat.title()}</small></figcaption></figure>' for i, a, t, cat in items)
    body = page_hero("Our Projects", "A look at recent residential, commercial and restoration work across the Puget Sound.",
                     "fitness-studio-tenant-improvement", [("Home", "index.html"), ("Projects", "")]) + f"""
<section class="section"><div class="container">
<div class="filters" role="group" aria-label="Filter projects">
<button aria-pressed="true" data-filter="all">All</button><button aria-pressed="false" data-filter="residential">Residential</button>
<button aria-pressed="false" data-filter="commercial">Commercial</button><button aria-pressed="false" data-filter="restoration">Restoration</button></div>
<div class="gallery" id="gallery">{g}</div></div></section>"""
    page("projects.html", "Project Gallery | Remodels, Tenant Improvements & Restoration | Interlake",
         "See recent kitchen remodels, home renovations, commercial tenant improvements and damage reconstruction by Interlake Construction in the Seattle area.",
         body, crumbs=[("Home", ""), ("Projects", "projects")])

# ---------------------------------------------------------------- AREAS
def build_areas():
    regions = "".join(f'<div class="region"><h3>{r}</h3><ul class="area-list">{"".join(f"<li>{c}</li>" for c in cs)}</ul></div>' for r, cs in REGIONS.items())
    body = page_hero("Service Areas: Mount Vernon to Tacoma",
                     "Remodeling, tenant improvements and reconstruction throughout Skagit, Snohomish, King and Pierce counties.",
                     "multifamily-framing", [("Home", "index.html"), ("Service Areas", "")]) + f"""
<section class="section"><div class="container">
<p class="lead">Interlake Construction is based in Seattle and serves homeowners, businesses and property managers along the I-5 corridor and Eastside — from Mount Vernon in the north to Tacoma in the south, and all the surrounding communities. Don't see your city? <a href="contact.html">Ask us</a> — if it's in the region, we likely serve it.</p>
{regions}
</div></section>
<section class="section section--alt"><div class="container grid grid-3">
<div class="value"><h3>Residential</h3><p>Kitchen, bath and whole-home remodels and ADUs in every community we serve.</p><a class="card-link" href="residential.html">Residential services</a></div>
<div class="value"><h3>Commercial</h3><p>Tenant improvements and build-outs from Everett to Bellevue to Tacoma.</p><a class="card-link" href="commercial.html">Commercial services</a></div>
<div class="value"><h3>Restoration</h3><p>Reconstruction after water, fire and mold damage across the Puget Sound.</p><a class="card-link" href="restoration.html">Restoration services</a></div>
</div></section>"""
    page("service-areas.html", "Service Areas | General Contractor Mount Vernon to Tacoma, WA | Interlake",
         "Interlake Construction serves Seattle, Everett, Bellevue, Redmond, Renton, Kent, Tacoma, Mount Vernon and surrounding Puget Sound communities.",
         body, crumbs=[("Home", ""), ("Service Areas", "service-areas")])

# ---------------------------------------------------------------- ABOUT
def build_about():
    body = page_hero("About Interlake Construction", "A Seattle-based general contractor built on quality, trust and integrity.",
                     "modern-staircase", [("Home", "index.html"), ("About", "")]) + f"""
<section class="section"><div class="container grid grid-2">
<div><span class="eyebrow">Who we are</span><h2>Craftsmanship and customer service, every time</h2>
<p>At Interlake Construction LLC, we pride ourselves on delivering exceptional craftsmanship and unparalleled customer service. Whether you're renovating your home, upgrading your commercial space or restoring a property after damage, our team is here to make the process simple.</p>
<p>We handle residential remodels, commercial tenant improvements and reconstruction from Mount Vernon to Tacoma — coordinating every trade so you have one point of contact and one clear schedule.</p>
<ul class="contact-info"><li>{ICON['shield']}<div><strong>Licensed, bonded &amp; insured</strong>Washington contractor license {BIZ['license']}</div></li></ul></div>
<div>{pic("office-stone-feature-wall", "Interlake technician installing a stone feature wall", "(max-width:900px) 100vw, 50vw", cls="rounded-img", w=1200, h=1600)}</div>
</div></section>
<section class="section section--alt"><div class="container">
<div class="center"><span class="eyebrow">Our values</span><h2>How we work</h2></div>
<div class="grid grid-3" style="margin-top:2rem">
<div class="value"><span class="num">01</span><h3>Quality</h3><p>The job will get done right the first time.</p></div>
<div class="value"><span class="num">02</span><h3>Trust</h3><p>Professional, certified technicians you can trust in your home.</p></div>
<div class="value"><span class="num">03</span><h3>Integrity</h3><p>We respect your time and keep our schedule.</p></div>
</div></div></section>
{testimonials_html()}"""
    page("about.html", "About Us | Interlake Construction LLC, Seattle WA",
         "Learn about Interlake Construction — a licensed Seattle general contractor focused on quality, trust and integrity in remodeling and restoration.",
         body, crumbs=[("Home", ""), ("About", "about")])

# ---------------------------------------------------------------- CONTACT
def build_contact():
    body = f"""<section class="page-hero"><div class="container">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / Contact</nav>
<h1>Get Your Free Estimate</h1><p>Tell us about your project and we'll get back to you within one business day. Prefer to talk? Call <a href="tel:{BIZ['tel']}" style="color:#fff;font-weight:700">{BIZ['phone']}</a>.</p></div></section>
<section class="section"><div class="container grid grid-2" style="align-items:start">
<form class="form" name="contact" method="POST" action="https://api.web3forms.com/submit">
  <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
  <input type="hidden" name="subject" value="New estimate request from the Interlake website">
  <input type="hidden" name="from_name" value="Interlake website">
  <input type="hidden" name="redirect" value="{LIVE_URL}/thank-you.html">
  <input type="checkbox" name="botcheck" class="hidden" style="display:none" tabindex="-1" autocomplete="off">
  <div class="form-row">
    <div><label for="name">Full name <span class="req">*</span></label><input id="name" name="name" autocomplete="name" required></div>
    <div><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
  </div>
  <div class="form-row">
    <div><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div><label for="city">Project city</label><input id="city" name="city" autocomplete="address-level2" placeholder="e.g. Bellevue"></div>
  </div>
  <div><label for="type">Project type</label><select id="type" name="project_type">
    <option value="">Select one…</option><option>Kitchen remodel</option><option>Bathroom remodel</option><option>Whole-home remodel / addition</option>
    <option>ADU / DADU</option><option>Commercial tenant improvement</option><option>Water / fire / mold damage repair</option><option>Other</option></select></div>
  <div><label for="details">Project details <span class="req">*</span></label><textarea id="details" name="details" required placeholder="What would you like done? Rough size, timeline, budget range, insurance claim, etc."></textarea></div>
  <div class="form-row">
    <div><label for="start">Desired start</label><input id="start" name="start_date" type="date"></div>
    <div><label for="finish">Needed by</label><input id="finish" name="completion_date" type="date"></div>
  </div>
  <button class="btn btn--primary" type="submit" style="justify-content:center">Request My Free Estimate</button>
  <p class="note">We never share your information.</p>
</form>
<div><span class="eyebrow">Contact info</span><h2>Let's talk about your project</h2>
<ul class="contact-info">
<li>{ICON['phone']}<div><strong>Phone</strong><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></div></li>
<li>{ICON['mail']}<div><strong>Email</strong><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
<li>{ICON['pin']}<div><strong>Office</strong>{BIZ['street']}, {BIZ['city']}, {BIZ['state']} {BIZ['zip']}</div></li>
<li>{ICON['shield']}<div><strong>License</strong>WA {BIZ['license']}</div></li></ul>
<iframe class="map" title="Map to Interlake Construction office" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
 src="https://maps.google.com/maps?q=4616+25th+Ave+NE,+Seattle,+WA+98105&amp;z=14&amp;output=embed"></iframe>
</div></div></section>"""
    page("contact.html", "Contact Interlake Construction | Free Estimate | (206) 659-5021",
         "Request a free estimate from Interlake Construction for remodeling, tenant improvements or damage reconstruction. Call (206) 659-5021.",
         body, crumbs=[("Home", ""), ("Contact", "contact")])

def build_misc():
    page("thank-you.html", "Thank You | Interlake Construction", "Thanks for contacting Interlake Construction.",
         f"""<section class="section"><div class="container center" style="max-width:700px"><span class="eyebrow">Message received</span>
<h1>Thank you!</h1><p class="lead">We've received your request and will reach out within one business day. Need us sooner? Call <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a>.</p>
<a class="btn btn--primary" href="index.html">Back to home</a></div></section>""", noindex=True, current="contact.html")
    page("404.html", "Page Not Found | Interlake Construction", "Page not found.",
         """<section class="section"><div class="container center" style="max-width:700px"><span class="eyebrow">404</span>
<h1>We couldn't find that page</h1><p class="lead">It may have moved when we updated our site.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn--primary" href="index.html">Home</a><a class="btn btn--outline" href="services.html">Services</a><a class="btn btn--outline" href="contact.html">Contact</a></div></div></section>""", noindex=True)

def build_meta(urls):
    sm = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": BIZ["name"], "short_name": "Interlake",
        "icons": [{"src": "/img/icon-180.png", "sizes": "180x180", "type": "image/png"}, {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#d7181f", "background_color": "#ffffff", "display": "standalone", "start_url": "/"}))

if __name__ == "__main__":
    for d in ("", "css", "js", "img"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    build_home(); build_services(); build_residential(); build_commercial(); build_restoration()
    build_projects(); build_areas(); build_about(); build_contact(); build_misc()
    build_meta([SITE + "/"] + [SITE + "/" + p for p in ["services", "residential", "commercial", "restoration", "projects", "service-areas", "about", "contact"]])
    print("built")
