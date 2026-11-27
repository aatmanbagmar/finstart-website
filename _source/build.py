#!/usr/bin/env python3
"""Builds the FinStart Advisory static site into ./site"""
import json, math, html, os

SITE = "https://finstartadvisory.com"
OUT = os.environ.get("OUT", "site")
PREVIEW = os.environ.get("PREVIEW") == "1"
PHONE_DISPLAY = "+91 90496 38800"
PHONE_TEL = "+919049638800"
EMAIL = "finstartadvisory@gmail.com"
WA = "https://wa.me/919049638800"
MAP = "https://maps.app.goo.gl/oQsKYhWPvsD8TWks8"
ADDRESS_HTML = ("Sakshi, Plot 13, S.No. 31/2/1<br>North Main Road, between Lane 5 &amp; 6<br>"
                "Koregaon Park, next to OMA &amp; Ramesh Medical<br>Pune, Maharashtra 411001")

# ---------------------------------------------------------------- icons
I_CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.15a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 4.54 0 8.24 3.7 8.24 8.24 0 4.54-3.7 8.24-8.24 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.17.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28z"/></svg>')

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- services data
GROUPS = [
  ("run", "Run your finance", "Leadership, reporting and decisions, month after month.", ["vcfo", "mis", "strategy"]),
  ("raise", "Raise and transact", "Capital, valuation and the terms of every deal.", ["fundraise", "valuation", "deal-structuring"]),
  ("tax", "Tax and structure", "Compliance done right, and advice before you act.", ["tax-compliance", "tax-advisory", "restructuring"]),
]
SVC = {
  "vcfo": dict(
    name="Virtual CFO", short="Senior finance leadership for your business, without a full-time hire.",
    best="startups and businesses that need senior finance leadership without a full-time CFO.",
    intro="We act as your finance head. Each month we close the numbers with your accountant, explain what they mean, and help you make the next decision with confidence. The engagement is open-ended, with no lock-in.",
    incl=["Monthly MIS and management review", "Budgets, forecasts and variance analysis", "Cash flow and runway management", "Unit economics and margin analysis", "Investor updates and board packs", "Compliance calendar oversight", "Finance processes, controls and tools", "Banking and lender relationships"]),
  "mis": dict(
    name="MIS & reporting", short="A clear monthly view of profit, cash and performance.",
    best="owners and founders who want a reliable monthly view of profit, cash and performance.",
    intro="We design a reporting pack around how you actually run the business: the KPIs that matter, in a format you will read. It's built on your existing accounting system, with a monthly routine so it arrives without chasing.",
    incl=["KPI framework for your business model", "Monthly MIS pack and dashboard", "P&L by product, branch or channel", "Cash flow and working capital reports", "Month-end closing checklist", "Accounting clean-up and chart of accounts"]),
  "strategy": dict(
    name="Strategic consulting", short="Numbers behind your biggest decisions.",
    best="decisions with real money attached: a new market, a pricing change, a new venture.",
    intro="We bring numbers to big decisions. Each project starts with the question you need answered and ends with a model and a recommendation you can act on.",
    incl=["Business plans and projections", "Pricing and margin strategy", "Cost review and optimisation", "Expansion and new venture feasibility", "Capex and make-or-buy decisions", "Bank finance readiness, including CMA data"]),
  "fundraise": dict(
    name="Fundraise support", short="Deck, model, valuation and data room, delivered as a focused sprint.",
    badge="4-week or 6-week sprint",
    best="founders preparing for pre-seed, seed or Series A, and businesses raising growth capital.",
    intro="A focused sprint that gets your story, numbers and documents investor-ready. It runs over 4 or 6 weeks, depending on how much is already in place.",
    incl=["Pitch deck narrative and design", "Investor-grade financial model", "Valuation and round sizing", "Cap table and dilution planning", "Data room setup", "Investor Q&A and diligence preparation", "Term sheet review support", "Investor outreach support"]),
  "valuation": dict(
    name="Business valuation", short="What the business is worth, explained so you can negotiate.",
    best="fundraises, ESOP grants, share transfers, transactions and internal planning.",
    intro="We value businesses using the methods investors and acquirers recognise, including discounted cash flow, comparable companies and recent transactions, and explain the result in plain terms. Where a regulation requires a report signed by a registered valuer or merchant banker, we coordinate it.",
    incl=["DCF and market-based valuations", "Valuation for fundraising and negotiation", "ESOP and share-based valuations", "Valuation for share transfers and exits", "Scenario and sensitivity analysis", "Independent review of third-party valuations"]),
  "deal-structuring": dict(
    name="Deal structuring", short="The right structure for investors, partners, acquisitions and exits.",
    best="bringing in investors or partners, acquisitions, joint ventures and exits.",
    intro="The structure of a deal decides who pays what tax, who controls what, and what happens when things change. We design it with the commercial, tax and regulatory sides considered together.",
    incl=["Choice of instrument: equity, CCPS, CCDs, convertible notes", "Term sheet structuring and negotiation support", "Acquisition and joint venture structuring", "Shareholder and partner exit settlements", "Financial due diligence", "Tax impact analysis of each option"]),
  "tax-compliance": dict(
    name="Tax compliance", nav="Tax compliance", short="Direct and indirect tax, filed correctly and on time.",
    full="Tax compliance (direct & indirect)",
    badge="Year-round compliance",
    best="businesses that want every return filed correctly and on time, without last-minute follow-ups.",
    intro="Direct and indirect tax compliance on a fixed annual calendar. We prepare, reconcile and file, and tell you in advance what's due and what we need from you.",
    incl=["Income tax returns for companies, LLPs, firms and individuals", "TDS and TCS returns and reconciliations", "Advance tax computation", "GST registration and periodic returns", "GST annual returns and reconciliations", "Responses to income tax and GST notices"]),
  "tax-advisory": dict(
    name="Tax advisory", short="Advice before you act, while there's still time to change course.",
    best="transactions, new structures and questions where the tax answer isn't obvious.",
    intro="We look at the tax consequences of a decision while there is still time to change it, and give you a clear answer with the reasoning behind it.",
    incl=["Tax-efficient business and holding structures", "Startup tax benefits and DPIIT recognition", "ESOP and founder taxation", "Cross-border and FEMA-linked tax questions", "GST structuring for new business lines", "Opinions on specific tax positions"]),
  "restructuring": dict(
    name="Restructuring", short="Conversions, mergers, holding structures and group reorganisations.",
    best="changing ownership, entity type or group structure.",
    intro="From converting a partnership into a company to reorganising a family business between generations, we plan the route, model the tax and work through it step by step, alongside your lawyers and company secretary where needed.",
    incl=["Proprietorship, firm or LLP to company conversions", "Mergers, demergers and slump sales", "Holding company and group restructuring", "Family business separation and succession", "Shareholder and partner exits", "Capital restructuring and buybacks"]),
}

SVC["succession"] = dict(
    name="Succession planning & business transition", nav="Succession",
    short="Plan what happens to your business next, and find the right next owner, partner or operator.")
# Homepage "What we do": succession shown as its own group, placed before Tax and structure
HOME_GROUPS = GROUPS[:2] + [
  ("succession", "Succession and transition", "For owners planning who takes the business forward.", ["succession"]),
] + GROUPS[2:]
ROUTES = [
    ("A full sale", "To a buyer from your industry, an investor or a family office."),
    ("A partner or investor", "Someone takes a stake, you take some value out and stay involved."),
    ("A new operator", "A capable person or company takes over the day-to-day running."),
    ("A management buyout", "The people who already run the business take it over, often in stages."),
    ("A planned family handover", "Where a relative is willing, a structured transfer with clear ownership."),
]
SUCC_STEPS = [
    ("Readiness review", "What a buyer will look at, and what needs work first."),
    ("Valuation", "What the business is worth, and what you can realistically expect."),
    ("Getting buyer-ready", "Books, compliance and documents in order; personal and business assets separated."),
    ("Choosing the route", "Sale, partner, operator, buyout or family handover, weighed against your goals."),
    ("Finding the right party", "Suitable buyers and partners identified and approached confidentially."),
    ("Negotiation and structure", "Price, terms, staged payments and how control passes over."),
    ("Tax on the transfer", "Share sale or business sale, capital gains and the most efficient route."),
    ("Through the transition", "Due diligence support and a handover plan that keeps the business running."),
]

def svc_full(k): return SVC[k].get("full", SVC[k]["name"])

PAGES = {"vcfo": "virtual-cfo", "mis": "mis-reporting", "strategy": "strategic-consulting",
         "fundraise": "fundraise-support", "valuation": "business-valuation", "deal-structuring": "deal-structuring",
         "tax-compliance": "tax-compliance", "tax-advisory": "tax-advisory", "restructuring": "restructuring",
         "succession": "succession-planning"}
def url(k): return PAGES[k] + ".html"
RELATED = {
    "vcfo": ["mis", "fundraise", "tax-compliance"], "mis": ["vcfo", "strategy", "tax-compliance"],
    "strategy": ["vcfo", "valuation", "fundraise"], "fundraise": ["valuation", "deal-structuring", "vcfo"],
    "valuation": ["fundraise", "deal-structuring", "succession"], "deal-structuring": ["valuation", "tax-advisory", "succession"],
    "tax-compliance": ["tax-advisory", "vcfo", "mis"], "tax-advisory": ["restructuring", "deal-structuring", "tax-compliance"],
    "restructuring": ["tax-advisory", "succession", "deal-structuring"], "succession": ["valuation", "restructuring", "deal-structuring"],
}
SEO = {
    "vcfo": ("Virtual CFO Services in Pune & Across India", "Virtual CFO services for startups and established businesses: monthly MIS, cash flow, forecasting, investor reporting and finance leadership, with no lock-in."),
    "mis": ("MIS & Financial Reporting Services", "Custom MIS reports, KPI dashboards and monthly reporting packs for business owners and founders who want a clear view of profit, cash and performance."),
    "strategy": ("Strategic Financial Consulting", "Business plans, projections, pricing, cost reviews, feasibility studies and bank finance readiness for growing businesses."),
    "fundraise": ("Fundraising Support: Pitch Deck, Financial Model & Valuation", "A 4-week or 6-week fundraise sprint covering pitch deck, investor-grade financial model, valuation, data room and investor Q&A preparation."),
    "valuation": ("Business Valuation Services", "DCF and market-based business valuations for fundraising, ESOPs, share transfers, transactions and planning, explained in plain terms."),
    "deal-structuring": ("Deal Structuring & Transaction Advisory", "Structuring investments, acquisitions, joint ventures, partner exits and term sheets, with tax and regulatory impact considered together."),
    "tax-compliance": ("Income Tax & GST Compliance Services", "Income tax, TDS, advance tax and GST compliance on a fixed annual calendar, with reconciliations and responses to notices."),
    "tax-advisory": ("Tax Advisory for Businesses & Startups", "Tax advice before you act: business and holding structures, startup tax benefits, ESOP taxation and opinions on tax positions."),
    "restructuring": ("Business Restructuring: Conversions, Mergers & Holding Structures", "Conversions to company or LLP, mergers, demergers, slump sales, holding structures and family business reorganisation."),
    "succession": ("Succession Planning & Business Transition", "Succession planning for business owners: valuation, finding the right buyer, partner or operator, and a confidential, tax-efficient handover."),
}

# ---------------------------------------------------------------- shared chrome
NAV = [("services.html", "Services"), ("startups.html", "Startups"), ("businesses.html", "Businesses"),
       ("about.html", "About"), ("service-finder.html", "Service finder")]

def header(active):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="FinStart Advisory home"><img src="assets/logo@web.png" alt="FinStart Advisory" width="131" height="44"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"><span></span><span></span><span></span></span><span class="label">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {links}
      <a class="btn btn--primary" href="contact.html"{" aria-current=\"page\"" if active == "contact.html" else ""}>Book a discovery call</a>
    </nav>
  </div>
</header>'''

def footer():
    svc_links = "".join(f'<li><a href="{url(k)}">{SVC[k]["name"]}</a></li>' for k in ["vcfo", "fundraise", "mis", "tax-compliance", "restructuring", "succession"])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/logo-reversed@web.png" alt="FinStart Advisory" width="137" height="46">
        <p>Financial advisory and virtual CFO services for startups and growing businesses, backed by more than 60 years of practice.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>{svc_links}<li><a href="services.html">All services</a></li></ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="startups.html">For startups</a></li>
          <li><a href="businesses.html">For businesses</a></li>
          <li><a href="service-finder.html">Service finder</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li>Aatman Bagmar, Managing Partner</li>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><address>{ADDRESS_HTML}</address></li>
          <li><a href="{MAP}" target="_blank" rel="noopener">Get directions</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> FinStart Advisory. All rights reserved.</span>
      <a href="privacy.html">Privacy notice</a>
    </div>
  </div>
</footer>
<a class="wa-float" href="{WA}?text={esc('Hello FinStart Advisory, I found you through your website and would like to talk.').replace(' ', '%20')}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{I_WA}<span>Chat with us</span></a>'''

ORG = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": SITE + "/#organization",
  "name": "FinStart Advisory",
  "url": SITE + "/",
  "logo": SITE + "/assets/logo.png",
  "image": SITE + "/assets/og-image.png",
  "description": "Virtual CFO, fundraising, MIS, valuation, tax and restructuring advisory for startups and growing businesses in Pune and across India.",
  "telephone": PHONE_TEL,
  "email": EMAIL,
  "address": {"@type": "PostalAddress",
              "streetAddress": "Sakshi, Plot 13, S.No. 31/2/1, North Main Road, between Lane 5 & 6, Koregaon Park",
              "addressLocality": "Pune", "addressRegion": "Maharashtra", "postalCode": "411001", "addressCountry": "IN"},
  "hasMap": MAP,
  "areaServed": {"@type": "Country", "name": "India"},
  "employee": {"@type": "Person", "name": "Aatman Bagmar", "jobTitle": "Managing Partner"},
  "knowsAbout": ["Virtual CFO", "Fundraising", "Financial modelling", "Business valuation", "MIS reporting",
                 "Income tax", "GST", "Tax advisory", "Deal structuring", "Corporate restructuring"],
}

def page(slug, title, desc, active, body, extra_ld=None, scripts=("site.js",), noindex=False):
    canon = SITE + "/" if slug == "index" else f"{SITE}/{slug}"
    ld = [ORG] + (extra_ld or [])
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    js = "\n".join(f'<script src="assets/js/{s}" defer></script>' for s in scripts)
    PREVIEW_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400..700&display=swap">' if PREVIEW else ""
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow">'
    doc = f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#072B52">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FinStart Advisory">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.png">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/hanken-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
{PREVIEW_FONT}
{ld_html}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{js}
</body>
</html>
'''
    with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
        f.write(doc)

# ---------------------------------------------------------------- reusable blocks
def ledger_group(gid, title, sub, keys):
    rows = "".join(
        f'<li><a href="{url(k)}"><span class="name">{SVC[k]["name"]}</span><span class="desc">{SVC[k]["short"]}</span>{I_CHEV}</a></li>'
        for k in keys)
    return f'''<div class="ledger-group">
  <div class="ledger-group-head"><h3>{title}</h3><p>{sub}</p></div>
  <ul class="ledger">{rows}</ul>
</div>'''

def cta_band(title="Let's look at your numbers together.",
             text="Book a discovery call with Aatman Bagmar, Managing Partner. Bring your questions; there's nothing to prepare."):
    return f'''<section class="cta-band" aria-labelledby="cta-title">
  <div class="grid-paper" aria-hidden="true"></div>
  <div class="wrap">
    <div>
      <h2 id="cta-title">{title}</h2>
      <p>{text}</p>
      <div class="contact-lines">
        <span>Call or WhatsApp <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></span>
        <span>Email <a href="mailto:{EMAIL}">{EMAIL}</a></span>
      </div>
    </div>
    <div class="cta-actions">
      <a class="btn btn--primary" href="contact.html">Book a discovery call</a>
      <a class="btn btn--ghost-light" href="{WA}" target="_blank" rel="noopener">{I_WA} Message on WhatsApp</a>
    </div>
  </div>
</section>'''

def spark():
    return ('<svg class="spark" viewBox="0 0 560 300" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="M0 280 C 60 270, 90 276, 130 250 S 210 236, 250 200 S 320 196, 350 160"/>'
            '<path class="f" d="M350 160 C 420 120, 480 80, 560 40"/></svg>')

def page_head(title, text, crumb, parent=None):
    mid = f'<a href="{parent[0]}">{parent[1]}</a> / ' if parent else ""
    return f'''<section class="page-head">
  <div class="grid-paper" aria-hidden="true"></div>
  {spark()}
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / {mid}<span aria-current="page">{crumb}</span></nav>
    <h1>{title}</h1>
    <p>{text}</p>
  </div>
</section>'''

def breadcrumb_ld(name, slug, parent=None):
    items = [("Home", SITE + "/")] + ([(parent[1], f"{SITE}/{parent[0]}")] if parent else []) + [(name, f"{SITE}/{slug}")]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

# ---------------------------------------------------------------- hero chart
def catmull(points):
    d = f"M{points[0][0]} {points[0][1]}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {p2[0]} {p2[1]}"
    return d

def hero_chart():
    base = 470
    pts = [(40, 440), (100, 432), (150, 438), (215, 392), (270, 376), (320, 384), (380, 318), (430, 300), (470, 306), (530, 214)]
    actual = catmull(pts)
    end = pts[-1]
    area = actual + f" L{end[0]} {base} L{pts[0][0]} {base} Z"
    fpts = [end, (600, 168), (660, 128), (730, 80)]
    forecast = catmull(fpts)
    upper = [(530, 214), (600, 150), (660, 98), (730, 40)]
    lower = [(530, 214), (600, 186), (660, 160), (730, 124)]
    band = "M" + " L".join(f"{x} {y}" for x, y in upper) + " L" + " L".join(f"{x} {y}" for x, y in reversed(lower)) + " Z"

    # milestones: (x, y, title, sub, label anchor/offsets)
    milestones = [
        (40, 440, "Day one", "Structure and setup", "start", 10, -58),
        (215, 392, "Clean books", "Compliance on track", "middle", 0, -64),
        (380, 318, "Monthly MIS", "Decisions on data", "middle", 0, -64),
        (530, 214, "Funds raised", "Capital in place", "middle", 0, -64),
    ]
    ms_svg = ""
    for x, y, t, s, anchor, dx, dy in milestones:
        tx = x + dx
        ms_svg += (f'<g class="chart-ms" data-x="{x}">'
                   f'<line x1="{x}" y1="{y-12}" x2="{x}" y2="{y+dy+22}"/>'
                   f'<circle class="dot" cx="{x}" cy="{y}" r="7"/>'
                   f'<text x="{tx}" y="{y+dy}" text-anchor="{anchor}">{t}</text>'
                   f'<text class="sub" x="{tx}" y="{y+dy+18}" text-anchor="{anchor}">{s}</text></g>')
    ms_svg += ('<g class="chart-ms chart-ms--forecast">'
               '<circle cx="730" cy="80" r="9" fill="none" stroke="#7FB6EE" stroke-width="2" stroke-dasharray="3 4"/>'
               '<text x="718" y="24" text-anchor="end">Your next milestone</text>'
               '<text class="sub" x="718" y="42" text-anchor="end">Planned ahead</text></g>')
    ticks = "".join(f'<text class="chart-tick" x="{x}" y="{base+28}" text-anchor="middle">{l}</text>'
                    for x, l in [(40, "Year 0"), (210, "Year 1"), (380, "Year 2"), (550, "Year 3"), (720, "Year 4")])
    return f'''<div class="hero-chart" role="img" aria-label="Illustration: a growth line rising from Day one through Clean books, Monthly MIS and Funds raised, continuing as a dashed forecast to your next milestone.">
  <svg viewBox="0 0 760 520" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">
    <defs>
      <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#80BE28" stop-opacity=".28"/>
        <stop offset="1" stop-color="#80BE28" stop-opacity="0"/>
      </linearGradient>
    </defs>
    <g class="chart-legend">
      <line x1="40" y1="30" x2="68" y2="30" stroke="#80BE28" stroke-width="3.5" stroke-linecap="round"/>
      <text x="78" y="35">Actuals</text>
      <line x1="160" y1="30" x2="188" y2="30" stroke="#7FB6EE" stroke-width="2.5" stroke-dasharray="2 7" stroke-linecap="round"/>
      <text x="198" y="35">Forecast</text>
    </g>
    <line class="chart-axis" x1="40" y1="{base}" x2="740" y2="{base}"/>
    {ticks}
    <path class="chart-band" d="{band}"/>
    <path class="chart-area" d="{area}"/>
    <path class="chart-forecast" d="{forecast}"/>
    <path class="chart-actual" d="{actual}"/>
    <circle class="chart-pulse" cx="{end[0]}" cy="{end[1]}" r="6"/>
    {ms_svg}
  </svg>
</div>'''

# ================================================================ PAGES
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- HOME
home = f'''<section class="hero" aria-labelledby="hero-title">
  <div class="grid-paper" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero-copy">
      <h1 id="hero-title">Virtual CFO and financial advice for founders and business owners.</h1>
      <p class="hero-sub">FinStart Advisory runs the finance function for startups and established businesses: monthly MIS, fundraising, tax and structuring, handled by one team that knows your numbers.</p>
      <div class="btn-row">
        <a class="btn btn--green" href="contact.html">Book a discovery call</a>
        <a class="btn btn--ghost-light" href="service-finder.html">Find the right service</a>
      </div>
      <p class="hero-note"><span>Backed by 60+ years of practice</span><span>Pune-based, working across India</span><span>Retainers with no lock-in</span></p>
    </div>
    {hero_chart()}
  </div>
</section>

<section class="section" aria-labelledby="paths-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <h2 id="paths-title">Where is your business right now?</h2>
      <p class="lede">Founders and business owners need different things from finance. Start with the path that fits you.</p>
    </div>
    <div class="split">
      <a class="path path--startup" href="startups.html">
        <h3>I'm building a startup</h3>
        <p>From incorporation to your next round, we set up the finance function investors expect to see.</p>
        <ul><li>Financial model and pitch deck</li><li>Monthly MIS and runway tracking</li><li>Valuation, cap table and deal terms</li></ul>
        <span class="go">Finance for startups {I_ARROW}</span>
      </a>
      <a class="path path--business" href="businesses.html">
        <h3>I run an established business</h3>
        <p>For owner-run and family businesses that want sharper numbers, cleaner compliance and room to grow.</p>
        <ul><li>Owner-ready monthly reporting</li><li>Cash flow and working capital</li><li>Tax, restructuring and succession</li></ul>
        <span class="go">Finance for businesses {I_ARROW}</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <h2 id="services-title">What we do</h2>
      <p class="lede">Use any service on its own, or bring several together under a single virtual CFO engagement.</p>
    </div>
    {"".join(ledger_group(*g) for g in HOME_GROUPS)}
    <p style="margin-top:2.5rem"><a class="text-link" href="services.html">See everything included in each service</a></p>
  </div>
</section>

<section class="section section--navy" aria-labelledby="how-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="how-title">How an engagement starts</h2>
      <p class="lede">Four steps from first conversation to a working finance function.</p>
    </div>
    <ol class="steps">
      <li><h3>A conversation</h3><p>A discovery call about your business, your numbers and what you want to change.</p></li>
      <li><h3>A diagnostic</h3><p>We review your books, compliance position and reporting to find the gaps that matter most.</p></li>
      <li><h3>A clear scope</h3><p>You get a written proposal built from our service packages, matched to what you need now.</p></li>
      <li><h3>A working rhythm</h3><p>We set up the systems, agree a reporting cadence and become part of how you run the business.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="models-title">
  <div class="wrap">
    <div class="section-head section-head--split">
      <h2 id="models-title">Ways to work with us</h2>
      <p class="lede">Packaged so you know exactly what you're getting. Scoped to your business after a discovery call.</p>
    </div>
    <div class="models">
      <div class="model"><h3>Virtual CFO retainer</h3><span class="term">Ongoing, with no lock-in</span>
        <p>A senior finance lead for your business, month after month.</p>
        <ul><li>Monthly MIS and reviews</li><li>Cash, budgets and forecasts</li><li>Investor and board reporting</li></ul></div>
      <div class="model"><h3>Fundraise sprint</h3><span class="term">4-week or 6-week sprint</span>
        <p>A focused push to get you investor-ready and through investor conversations.</p>
        <ul><li>Pitch deck and financial model</li><li>Valuation and data room</li><li>Investor Q&amp;A preparation</li></ul></div>
      <div class="model"><h3>Compliance retainer</h3><span class="term">Year-round</span>
        <p>Direct and indirect tax on a fixed calendar, so deadlines stop being emergencies.</p>
        <ul><li>Income tax, TDS and advance tax</li><li>GST returns and reconciliations</li><li>Notice and assessment support</li></ul></div>
      <div class="model"><h3>Project mandate</h3><span class="term">Scoped to the outcome</span>
        <p>One-off work with a clear finish line and a defined deliverable.</p>
        <ul><li>Valuations</li><li>Restructuring and conversions</li><li>Deal structuring and due diligence</li></ul></div>
    </div>
  </div>
</section>

<section class="section section--navy" aria-labelledby="legacy-title">
  <div class="wrap legacy">
    <div class="legacy-figure num" aria-hidden="true">60+<small>years of practice behind FinStart, through Abhay Bagmar &amp; Associates, Pune.</small></div>
    <div>
      <h2 id="legacy-title">New-age advisory, held to an old-school standard.</h2>
      <p class="lede" style="margin:1.25rem 0 2rem">FinStart Advisory is backed by Abhay Bagmar &amp; Associates, a Pune practice that has advised businesses for more than six decades. We bring that depth of judgement to founders and growing companies, at the pace they work.</p>
      <ul class="facts">
        <li><strong>Pune-based, working across India</strong><span>In person in Pune, and remotely everywhere else.</span></li>
        <li><strong>Sector-agnostic</strong><span>From traditional trading and manufacturing businesses to new-age startups.</span></li>
        <li><strong>One team for the whole picture</strong><span>Reporting, fundraising, tax and structure handled together, not handed off.</span></li>
      </ul>
      <p style="margin-top:2rem"><a class="text-link" href="about.html">Read our story</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="finder-title">
  <div class="wrap">
    <div class="teaser">
      <div>
        <h2 id="finder-title">Not sure where to start?</h2>
        <p>Answer four quick questions and we'll point you to the service that fits, with a summary you can send us directly.</p>
        <p style="margin-top:1.5rem"><a class="btn btn--primary" href="service-finder.html">Start the service finder</a></p>
      </div>
      <ol class="teaser-qs" aria-label="The four questions">
        <li><span class="q">1</span><span><b>Your stage:</b> idea, startup or established business</span></li>
        <li><span class="q">2</span><span><b>Your priorities:</b> funding, numbers, tax, structure</span></li>
        <li><span class="q">3</span><span><b>Your setup:</b> who handles finance today</span></li>
        <li><span class="q">4</span><span><b>Your timing:</b> now, soon, or exploring</span></li>
      </ol>
    </div>
  </div>
</section>

{cta_band()}'''
page("index", "FinStart Advisory | Virtual CFO & Financial Advisory in Pune",
     "Virtual CFO, fundraising, MIS, valuation, tax and restructuring for startups and growing businesses. Pune-based, working across India, backed by 60+ years of practice.",
     "index.html", home)

# ---------------------------------------------------------------- SERVICES
def svc_card(k, cls="svc-card"):
    return (f'<a class="{cls}" href="{url(k)}"><h3>{svc_full(k)}</h3><p>{SVC[k]["short"]}</p>'
            f'<span class="more">View service {I_CHEV}</span></a>')

grid_html = ""
for gid, gt, gs, keys in HOME_GROUPS:
    grid_html += f'''<div class="svc-row">
  <div class="svc-row-head"><h2>{gt}</h2><p>{gs}</p></div>
  <div class="svc-cards">{"".join(svc_card(k) for k in keys)}</div>
</div>'''

FAQS = [
  ("What does a virtual CFO actually do?",
   "The same things a full-time CFO would: owning your numbers, planning cash, reporting to investors or lenders, and advising on decisions. The difference is that you get senior experience for the time you actually need, without a full-time salary."),
  ("Is there a minimum commitment?",
   "No. Our virtual CFO retainers are open-ended, with no lock-in. Fundraise sprints and projects have a defined scope that we agree with you before we start."),
  ("Why don't you publish fees?",
   "Every business starts from a different place, so we scope the work after a discovery call and share a written proposal. You'll know exactly what's included before you commit."),
  ("Do you work with businesses outside Pune?",
   "Yes. We work with clients across India. Clients in Pune can meet us in person; everyone else works with us remotely through scheduled calls and shared reporting."),
  ("Can you work alongside our existing accountant or CA?",
   "Yes. Many clients keep their accountant for bookkeeping and their CA for statutory audit. We work with them, not around them."),
  ("Which sectors do you work with?",
   "We are sector-agnostic. Our clients range from traditional trading and manufacturing businesses to new-age startups."),
  ("Do you carry out statutory audits?",
   "No. FinStart Advisory is a financial advisory firm. We focus on finance leadership, reporting, fundraising, tax and structuring, and we coordinate with your auditor where needed."),
]
faq_html = "".join(
    f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div><p>{a}</p></div></details>' for q, a in FAQS)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
svc_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "FinStart Advisory services",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
              "@type": "Service", "name": svc_full(k), "description": SVC[k]["short"],
              "provider": {"@id": SITE + "/#organization"}, "areaServed": "India",
              "url": f"{SITE}/{PAGES[k]}"}} for i, k in enumerate([k for g in GROUPS for k in g[3]] + ["succession"])]}

I_LOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 10.5V7.5a3.5 3.5 0 0 1 7 0v3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
routes_html = "".join(f'<li><strong>{t}</strong><span>{d}</span></li>' for t, d in ROUTES)
succ_steps_html = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in SUCC_STEPS)
open_to = [("takeover", "A full takeover"), ("stake", "A partnership or stake"), ("operate", "Running a business as operator"), ("any", "Any of the above"), ("unsure", "Not sure yet")]
open_to_html = "".join(f'<label class="tick"><input type="checkbox" name="open_to" value="{t}"><span>{t}</span></label>' for v, t in open_to)
interest_html = f'''<section class="section interest" id="interest" aria-labelledby="interest-t">
  <div class="wrap contact-grid">
    <div>
      <h2 id="interest-t" style="font-size:var(--fs-lg)">Interested in taking over or partnering with an established business?</h2>
      <p class="lede" style="margin-top:1rem">Register your interest. We'll get in touch only when an opportunity matches what you're looking for, and only after a confidentiality agreement.</p>
    </div>
    <form class="form" id="interest-form" action="https://formsubmit.co/ajax/{EMAIL}" method="post" novalidate>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="row">
        <div class="field"><label for="i-name">Your name</label><input id="i-name" name="name" autocomplete="name" required aria-describedby="err-i-name"><span class="err" id="err-i-name"></span></div>
        <div class="field"><label for="i-role">I am</label><select id="i-role" name="role"><option>An individual</option><option>A business owner</option><option>An investor or family office</option><option>Other</option></select></div>
      </div>
      <div class="row">
        <div class="field"><label for="i-email">Email</label><input id="i-email" name="email" type="email" autocomplete="email" required aria-describedby="err-i-email"><span class="err" id="err-i-email"></span></div>
        <div class="field"><label for="i-phone">Phone <span class="opt">(optional)</span></label><input id="i-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      </div>
      <fieldset class="field"><legend>What are you open to?</legend><div class="ticks">{open_to_html}</div><span class="err" id="err-i-open"></span></fieldset>
      <div class="field"><label for="i-sectors">Sectors and locations of interest</label><input id="i-sectors" name="sectors" placeholder="For example: retail, in Pune"></div>
      <div class="field"><label for="i-note">Anything else we should know <span class="opt">(optional)</span></label><textarea id="i-note" name="note" style="min-height:96px"></textarea></div>
      <div id="interest-status" class="form-status" role="status" tabindex="-1"></div>
      <div><button type="submit" class="btn btn--primary">Register interest</button></div>
      <p class="small">We use your details only to contact you about suitable opportunities. See our <a href="privacy.html">privacy notice</a>.</p>
    </form>
  </div>
</section>'''

def related_html(k):
    return f'''<section class="section section--paper" aria-labelledby="rel-t">
  <div class="wrap">
    <div class="section-head"><h2 id="rel-t" style="font-size:var(--fs-lg)">Related services</h2></div>
    <div class="svc-cards">{"".join(svc_card(r) for r in RELATED[k])}</div>
    <p style="margin-top:2rem"><a class="text-link" href="services.html">See all services</a></p>
  </div>
</section>'''

def service_ld(k):
    return {"@context": "https://schema.org", "@type": "Service", "name": svc_full(k), "description": SEO[k][1],
            "serviceType": svc_full(k), "provider": {"@id": SITE + "/#organization"}, "areaServed": "India",
            "url": f"{SITE}/{PAGES[k]}"}

for gid, gt, gs, keys in GROUPS:
    for k in keys:
        sv = SVC[k]
        badge = f'<span class="badge">{sv["badge"]}</span>' if sv.get("badge") else ""
        incl = "".join(f"<li>{I_CHECK}<span>{esc(x)}</span></li>" for x in sv["incl"])
        body = f'''{page_head(svc_full(k), sv["short"], sv["name"], parent=("services.html", "Services"))}
<section class="section">
  <div class="wrap svc-detail">
    <div>
      {badge}
      <p class="for"><b>Best for:</b> {sv["best"]}</p>
      <p class="intro">{sv["intro"]}</p>
      <div class="btn-row" style="margin-top:2rem">
        <a class="btn btn--primary" href="contact.html">Discuss this service</a>
        <a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">{I_WA} WhatsApp us</a>
      </div>
    </div>
    <div>
      <h2 class="incl-title">What's included</h2>
      <ul class="checks checks--one">{incl}</ul>
    </div>
  </div>
</section>
{related_html(k)}
{cta_band()}'''
        page(PAGES[k], f"{SEO[k][0]} | FinStart Advisory", SEO[k][1], "services.html", body,
             extra_ld=[service_ld(k), breadcrumb_ld(sv["name"], PAGES[k], ("services", "Services"))])

succ_body = f'''{page_head("Succession planning &amp; business transition",
  "For owners planning what happens to their business next: when there's no successor, the next generation has chosen a different path, or it's simply time to step back.",
  "Succession planning", parent=("services.html", "Services"))}
<section class="section">
  <div class="wrap succ-top">
    <div>
      <p class="succ-lede">Your business doesn't have to close when you step away. We help you plan the handover, value the business, and find the right next owner, partner or operator, so the business keeps running and you realise the value you've built.</p>
      <div class="btn-row"><a class="btn btn--primary" href="contact.html">Start a confidential conversation</a><a class="btn btn--ghost" href="#interest">Looking to take over a business?</a></div>
    </div>
    <div>
      <h2 class="succ-sub succ-sub--light">Ways your business can carry on</h2>
      <ul class="routes routes--light">{routes_html}</ul>
    </div>
  </div>
</section>
<section class="section section--navy" aria-labelledby="succ-steps-t">
  <div class="wrap">
    <div class="section-head"><h2 id="succ-steps-t">How we take you through it</h2></div>
    <ol class="steps steps--8">{succ_steps_html}</ol>
  </div>
</section>
{interest_html}
{related_html("succession")}
{cta_band("Plan what comes next, on your terms.", "Start a confidential conversation with Aatman Bagmar, Managing Partner. Nothing is shared without your approval.")}'''
page(PAGES["succession"], f"{SEO['succession'][0]} | FinStart Advisory", SEO["succession"][1], "services.html", succ_body,
     extra_ld=[service_ld("succession"), breadcrumb_ld("Succession planning", PAGES["succession"], ("services", "Services"))])

services = f'''{page_head("Everything your finance function needs, in one place.",
  "Services across running your finance, raising and transacting, tax and structure, and succession planning. Each one can stand alone or sit inside a virtual CFO engagement.", "Services")}
<section class="section svc-grid-section" aria-label="All services">
  <div class="wrap">{grid_html}</div>
</section>
<section class="section section--paper" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head"><h2 id="faq-title">Common questions</h2></div>
    <div class="faq">{faq_html}</div>
    <p style="margin-top:2.5rem">Still deciding? <a class="text-link" href="service-finder.html">Try the service finder</a></p>
  </div>
</section>
{cta_band()}'''
page("services", "Services: Virtual CFO, Fundraising, MIS, Tax & Restructuring | FinStart Advisory",
     "Virtual CFO, MIS & reporting, strategic consulting, fundraise support, valuation, deal structuring, tax compliance, tax advisory and restructuring for Indian startups and businesses.",
     "services.html", services, extra_ld=[svc_ld, faq_ld, breadcrumb_ld("Services", "services")])

# ---------------------------------------------------------------- STARTUPS
def pairs(items):
    return '<div class="pairs">' + "".join(
        f'<div class="pair"><p class="q">“{q}”</p><p class="a">{a} <a href="{url(k)}"><b>{SVC[k]["name"]}</b></a></p></div>'
        for q, a, k in items) + "</div>"

def stages(items):
    return '<div class="stages">' + "".join(
        f'<div class="stage"><h3>{t}<span class="when">{w}</span></h3><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>'
        for t, w, li in items) + "</div>"

startups = f'''{page_head("Finance for startups, from incorporation to your next round.",
  "Founders should spend their time on product and customers. We handle the numbers, the investor materials and the compliance, and grow the finance function with you.", "Startups")}
<section class="section section--paper" aria-labelledby="s1">
  <div class="wrap">
    <div class="section-head"><h2 id="s1">What founders usually come to us with</h2></div>
    {pairs([
      ("We're raising, and investors want a financial model.", "We build a model you can defend line by line, and a deck that tells the same story.", "fundraise"),
      ("We don't know our real burn or runway.", "A monthly MIS with cash and runway front and centre, reviewed with you every month.", "vcfo"),
      ("We have a term sheet. Is it fair?", "We review the terms, the dilution and the structure before you sign.", "deal-structuring"),
      ("Investors are asking for a valuation.", "A valuation built on methods investors recognise, explained so you can negotiate.", "valuation"),
      ("Compliance keeps slipping.", "Tax and GST on a fixed calendar, with reminders well before each deadline.", "tax-compliance"),
      ("We're setting up and want the structure right.", "Entity choice, founder shareholding and tax benefits planned from day one.", "tax-advisory"),
    ])}
  </div>
</section>
<section class="section" aria-labelledby="s2">
  <div class="wrap">
    <div class="section-head"><h2 id="s2">What we do at each stage</h2><p class="lede">The finance function a startup needs changes as it grows. Here's how ours changes with it.</p></div>
    {stages([
      ("Idea and incorporation", "Before the first rupee of revenue", ["Entity choice and founder structure", "Cap table and founder vesting", "DPIIT recognition and tax benefits", "Accounting and compliance setup", "First business plan and projections", "Banking and payments setup"]),
      ("Pre-seed and seed", "Building product, first customers", ["Pitch deck and financial model", "Valuation and round sizing", "Data room and diligence preparation", "Monthly MIS and runway tracking", "GST and TDS compliance", "Investor reporting setup"]),
      ("Series A and beyond", "Scaling team and revenue", ["Virtual CFO leadership", "Board packs and investor updates", "Unit economics and cohort analysis", "Budgets and rolling forecasts", "ESOP planning and valuation", "Series A readiness and diligence"]),
    ])}
  </div>
</section>
<section class="section section--paper" aria-labelledby="s3">
  <div class="wrap">
    <div class="teaser" style="background:#fff">
      <div><h2 id="s3">Raising in the next few months?</h2>
        <p>Our fundraise sprint runs over 4 or 6 weeks and covers your deck, model, valuation and data room, with support through investor conversations.</p></div>
      <div class="btn-row"><a class="btn btn--primary" href="fundraise-support.html">See the fundraise sprint</a><a class="btn btn--ghost" href="service-finder.html">Use the service finder</a></div>
    </div>
  </div>
</section>
{cta_band("Build the finance function investors expect.", "Book a discovery call with Aatman Bagmar, Managing Partner, and tell us where your startup is today.")}'''
page("startups", "Finance for Startups: Virtual CFO, Fundraising & Valuation | FinStart Advisory",
     "Startup finance from incorporation to Series A: financial models, pitch decks, valuation, monthly MIS, runway tracking, compliance and virtual CFO support.",
     "startups.html", startups, extra_ld=[breadcrumb_ld("Startups", "startups")])

# ---------------------------------------------------------------- BUSINESSES
biz_keys = ["mis", "vcfo", "tax-compliance", "tax-advisory", "restructuring", "succession", "strategy", "valuation"]
biz_rows = "".join(f'<li><a href="{url(k)}"><span class="name">{SVC[k]["name"]}</span><span class="desc">{SVC[k]["short"]}</span>{I_CHEV}</a></li>' for k in biz_keys)
businesses = f'''{page_head("Sharper numbers for established businesses.",
  "For owner-run, family and mid-sized businesses that have outgrown basic bookkeeping but don't need a full in-house finance team.", "Businesses")}
<section class="section section--paper" aria-labelledby="b1">
  <div class="wrap">
    <div class="section-head"><h2 id="b1">What business owners usually come to us with</h2></div>
    {pairs([
      ("I only see the real profit when the year closes.", "A monthly MIS that shows profit, margins and cash every month, by product, branch or channel.", "mis"),
      ("Money is stuck in debtors and stock.", "Working capital reviews and cash forecasts, so you see a crunch coming.", "vcfo"),
      ("I do not have a business succession plan.", "We plan the handover, value the business and find the right next owner, partner or operator.", "succession"),
      ("A partner wants to exit.", "A fair valuation and a tax-efficient settlement that works for everyone.", "deal-structuring"),
      ("We want bank finance for expansion.", "Projections, CMA data and a business plan lenders take seriously.", "strategy"),
      ("Tax and GST notices keep arriving.", "Clean, reconciled compliance and considered responses to every notice.", "tax-compliance"),
    ])}
  </div>
</section>
<section class="section" aria-labelledby="b2">
  <div class="wrap two-col">
    <div><h2 id="b2">Modernising without disruption</h2></div>
    <div class="prose">
      <p class="big">We work with the accountant, software and people you already have.</p>
      <p>Change happens in steps. First, a clear monthly report you can trust. Then better processes and controls. Then the tools that save your team time. At every step, you decide how far to go.</p>
      <p>And because we've worked with established businesses for decades, we understand how they really run: the relationships, the family dynamics and the decisions that never appear in the books.</p>
    </div>
  </div>
</section>
<section class="section section--paper" aria-labelledby="b3">
  <div class="wrap">
    <div class="section-head"><h2 id="b3">Services business owners use most</h2></div>
    <div class="ledger-group"><ul class="ledger" style="border-top:2px solid var(--navy)">{biz_rows}</ul></div>
  </div>
</section>
{cta_band("Know your numbers every month, not every March.", "Book a discovery call with Aatman Bagmar, Managing Partner, and we'll show you what a monthly MIS for your business could look like.")}'''
page("businesses", "Finance for SMEs & Family Businesses: MIS, Tax & Restructuring | FinStart Advisory",
     "Monthly MIS, cash flow and working capital, tax compliance, restructuring, succession planning and bank finance readiness for established and family-run businesses.",
     "businesses.html", businesses, extra_ld=[breadcrumb_ld("Businesses", "businesses")])

# ---------------------------------------------------------------- ABOUT
about = f'''{page_head("Six decades of practice. A new way to deliver it.",
  "FinStart Advisory is a financial advisory firm based in Pune, backed by the 60-year legacy of Abhay Bagmar &amp; Associates.", "About")}
<section class="section" aria-labelledby="a1">
  <div class="wrap two-col">
    <div><h2 id="a1">Our story</h2></div>
    <div class="prose">
      <p class="big">For more than sixty years, Abhay Bagmar &amp; Associates has advised businesses in and around Pune on accounts, tax and the decisions behind them. Many of those relationships now span generations.</p>
      <p>FinStart Advisory was set up to bring that experience to a new kind of client: founders building startups, and established businesses that want the kind of finance function usually found only in large companies.</p>
      <p>We help businesses understand their numbers, raise capital, stay compliant and structure themselves well. We grow with our clients, not off them.</p>
    </div>
  </div>
</section>
<section class="section section--paper" aria-labelledby="a2">
  <div class="wrap two-col">
    <div><h2 id="a2">What we believe</h2></div>
    <ul class="principles">
      <li><strong>Numbers should lead to decisions</strong><span>A report nobody acts on is a cost. Everything we produce is built to answer a question you actually have.</span></li>
      <li><strong>Advice before action</strong><span>Tax and structure are cheapest to get right before a decision is made, not after.</span></li>
      <li><strong>One team, whole picture</strong><span>Reporting, fundraising, tax and structure affect each other, so we handle them together.</span></li>
      <li><strong>No lock-ins</strong><span>Our retainers are open-ended. Clients stay for the value we add.</span></li>
      <li><strong>Plain language</strong><span>If we can't explain it simply, we haven't understood it well enough.</span></li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="a3">
  <div class="wrap two-col">
    <div><h2 id="a3">Where we work</h2></div>
    <div class="prose">
      <p class="big">Our office is in Koregaon Park, Pune. Our clients are across India.</p>
      <p>Clients in Pune can meet us in person. Everyone else works with us remotely, through scheduled reviews, shared reporting and a direct line to the person handling their work.</p>
      <p><a class="text-link" href="{MAP}" target="_blank" rel="noopener">Get directions to our office</a></p>
    </div>
  </div>
</section>
{cta_band()}'''
page("about", "About FinStart Advisory | 60+ Years of Practice, Pune",
     "FinStart Advisory is a Pune financial advisory firm backed by the 60-year legacy of Abhay Bagmar & Associates, serving startups and established businesses across India.",
     "about.html", about, extra_ld=[breadcrumb_ld("About", "about")])

# ---------------------------------------------------------------- SERVICE FINDER
def opts(name, kind, items):
    out = ""
    for v, b, s in items:
        iid = f"{name}-{v}"
        out += (f'<div class="option"><input type="{kind}" id="{iid}" name="{name}" value="{v}">'
                f'<label for="{iid}"><b>{b}</b><span>{s}</span></label></div>')
    return f'<div class="options">{out}</div>'

finder = f'''{page_head("Find the right service in four questions.",
  "Tell us where you are and what's on your mind. We'll recommend where to start, and you can send the summary straight to us.", "Service finder")}
<section class="section">
  <div class="wrap">
    <div class="finder">
      <div id="finder">
        <div class="finder-progress" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <div class="finder-step"><fieldset>
          <legend>Which best describes your business?</legend>
          <p class="hint">Pick the closest match.</p>
          {opts("stage", "radio", [
            ("idea", "Planning to start", "About to incorporate, or just incorporated"),
            ("early", "Early-stage startup", "Building the product, first customers or revenue"),
            ("scaling", "Funded or scaling startup", "Raised, or about to raise; team and revenue growing"),
            ("established", "Established business", "Steady revenue; owner-run, family or mid-sized"),
          ])}
        </fieldset></div>
        <div class="finder-step"><fieldset>
          <legend>What do you want help with?</legend>
          <p class="hint">Choose everything that applies.</p>
          {opts("needs", "checkbox", [
            ("raise", "Raising funds", "Equity, from angels, VCs or strategic investors"),
            ("numbers", "Clear monthly numbers", "A reliable view of profit, margins and cash"),
            ("cash", "Cash and runway", "Knowing how long the money lasts, and planning ahead"),
            ("compliance", "Tax and GST compliance", "Returns, TDS and GST filed right and on time"),
            ("taxplan", "Tax planning", "Reducing tax risk and planning before decisions"),
            ("structure", "Changing the structure", "Conversion, merger, holding company or succession"),
            ("deal", "A deal or partnership", "Buying, selling, a partner joining or exiting"),
            ("value", "A valuation", "Knowing what the business or a stake is worth"),
            ("growth", "Growth plans", "A new market, product line or venture"),
            ("succession", "Succession or a change of ownership", "Planning who takes the business forward"),
          ])}
        </fieldset></div>
        <div class="finder-step"><fieldset>
          <legend>Who handles finance today?</legend>
          <p class="hint">This tells us how much support you're likely to need.</p>
          {opts("team", "radio", [
            ("founder", "The founder or owner", "No one else looks after finance"),
            ("accountant", "An accountant", "Bookkeeping is done, but not much more"),
            ("team", "An in-house finance team", "We have people, but need senior input"),
            ("ca", "An external CA firm", "Compliance is handled by an outside firm"),
          ])}
        </fieldset></div>
        <div class="finder-step"><fieldset>
          <legend>How soon do you need help?</legend>
          <p class="hint">No commitment, this just helps us prepare.</p>
          {opts("when", "radio", [
            ("now", "Right away", "Something needs attention in the next few weeks"),
            ("soon", "In the next quarter", "Planning ahead for the coming months"),
            ("exploring", "Just exploring", "Understanding the options for now"),
          ])}
        </fieldset></div>
        <p class="finder-msg" role="alert"></p>
        <div class="finder-nav" hidden>
          <button type="button" class="btn btn--ghost" data-back hidden>Back</button>
          <span class="count" aria-live="polite"></span>
          <button type="button" class="btn btn--primary" data-next>Next question</button>
        </div>
        <noscript><p>The service finder needs JavaScript. You can <a href="services.html">browse all services</a> or <a href="contact.html">contact us</a> instead.</p></noscript>
      </div>
      <div class="result" id="finder-result" aria-live="polite"></div>
    </div>
  </div>
</section>'''
page("service-finder", "Which Finance Service Do I Need? Service Finder | FinStart Advisory",
     "Answer four quick questions to find the right finance service for your startup or business: virtual CFO, fundraising, MIS, valuation, tax or restructuring.",
     "service-finder.html", finder, scripts=("site.js", "finder.js"), extra_ld=[breadcrumb_ld("Service finder", "service-finder")])

# ---------------------------------------------------------------- CONTACT
svc_options = '<option>Not sure yet</option>' + "".join(f"<option>{SVC[k]['name']}</option>" for g in GROUPS for k in g[3]) + f"<option>{SVC['succession']['name']}</option>"
contact = f'''{page_head("Let's talk about your business.",
  "Tell us a little about where you are and what you need. We'll get back to you to set up a discovery call.", "Contact")}
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2 style="font-size:var(--fs-lg);margin-bottom:1.5rem">Reach us directly</h2>
      <div class="contact-card">
        <div><span class="k">Managing Partner</span><span class="v">Aatman Bagmar</span></div>
        <div><span class="k">Phone and WhatsApp</span><span class="v"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></span></div>
        <div><span class="k">Email</span><span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        <div><span class="k">Office</span><address>{ADDRESS_HTML}</address>
          <span style="margin-top:.5rem"><a class="text-link" href="{MAP}" target="_blank" rel="noopener">Get directions in Google Maps</a></span></div>
      </div>
      <p style="margin-top:1.75rem"><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">{I_WA} Message us on WhatsApp</a></p>
    </div>
    <form class="form" id="enquiry-form" action="https://formsubmit.co/ajax/{EMAIL}" method="post" novalidate>
      <h2>Send an enquiry</h2>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="err-name"><span class="err" id="err-name"></span></div>
        <div class="field"><label for="f-company">Company <span class="opt">(optional)</span></label><input id="f-company" name="company" autocomplete="organization"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="err-email"><span class="err" id="err-email"></span></div>
        <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      </div>
      <div class="row">
        <div class="field"><label for="f-role">I am a</label><select id="f-role" name="role"><option>Startup founder</option><option>Business owner</option><option>Finance professional</option><option>Other</option></select></div>
        <div class="field"><label for="f-service">Interested in</label><select id="f-service" name="service">{svc_options}</select></div>
      </div>
      <div class="field"><label for="f-message">How can we help?</label><textarea id="f-message" name="message" required aria-describedby="err-message" placeholder="A few lines about your business and what you'd like help with"></textarea><span class="err" id="err-message"></span></div>
      <div id="form-status" class="form-status" role="status" tabindex="-1"></div>
      <div><button type="submit" class="btn btn--primary">Send enquiry</button></div>
      <p class="small">We use your details only to reply to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
    </form>
  </div>
</section>'''
page("contact", "Contact FinStart Advisory | Book a Discovery Call, Pune",
     "Book a discovery call with FinStart Advisory. Call or WhatsApp +91 90496 38800, email finstartadvisory@gmail.com, or visit us in Koregaon Park, Pune.",
     "contact.html", contact, extra_ld=[breadcrumb_ld("Contact", "contact")])

# ---------------------------------------------------------------- PRIVACY
privacy = f'''{page_head("Privacy notice", "How FinStart Advisory handles the information you share through this website.", "Privacy notice")}
<section class="section"><div class="wrap"><div class="prose">
  <h2 style="font-size:var(--fs-lg);margin-bottom:1rem">What we collect</h2>
  <p>When you send an enquiry, we receive the details you enter: your name, email address, and optionally your company, phone number and message. If you use the service finder, your answers stay in your browser unless you choose to send them to us.</p>
  <h2 style="font-size:var(--fs-lg);margin:2rem 0 1rem">How we use it</h2>
  <p>We use your details only to respond to your enquiry and, if you become a client, to provide our services. We do not sell or share your information for marketing.</p>
  <h2 style="font-size:var(--fs-lg);margin:2rem 0 1rem">How it reaches us</h2>
  <p>Enquiries are delivered to our email inbox through a form delivery service. WhatsApp messages are handled under WhatsApp's own terms.</p>
  <h2 style="font-size:var(--fs-lg);margin:2rem 0 1rem">Your choices</h2>
  <p>To see, correct or delete the information we hold about you, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div></section>'''
page("privacy", "Privacy Notice | FinStart Advisory", "How FinStart Advisory handles information shared through this website.",
     "", privacy, extra_ld=[breadcrumb_ld("Privacy notice", "privacy")])

# ---------------------------------------------------------------- 404
nf = '''<section class="section notfound"><div class="wrap">
  <h1 style="font-size:var(--fs-xl);max-width:20ch">This page isn't on the books.</h1>
  <p class="lede" style="margin:1.25rem 0 2rem">The link may be out of date, or the address mistyped. Try one of these instead.</p>
  <div class="btn-row"><a class="btn btn--primary" href="index.html">Go to the home page</a><a class="btn btn--ghost" href="services.html">Browse services</a><a class="btn btn--ghost" href="contact.html">Contact us</a></div>
</div></section>'''
page("404", "Page not found | FinStart Advisory", "The page you were looking for could not be found.", "", nf, noindex=True)

# ---------------------------------------------------------------- SEO files
urls = [("", "1.0"), ("services", "0.9"), ("startups", "0.8"), ("businesses", "0.8"), ("about", "0.7"),
        ("service-finder", "0.7"), ("contact", "0.8"), ("privacy", "0.2")] + [(v, "0.8") for v in PAGES.values()]
with open(f"{OUT}/sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, p in urls:
        f.write(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-11-14</lastmod><priority>{p}</priority></url>\n")
    f.write("</urlset>\n")
with open(f"{OUT}/robots.txt", "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(f"{OUT}/site.webmanifest", "w") as f:
    json.dump({"name": "FinStart Advisory", "short_name": "FinStart", "start_url": "/", "display": "browser",
               "background_color": "#FFFFFF", "theme_color": "#072B52",
               "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                         {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, f, indent=2)
print("built")
