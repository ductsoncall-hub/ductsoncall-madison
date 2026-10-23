#!/usr/bin/env python3
"""Static site generator for the Ducts On Call local-SEO site. Run: python3 build.py"""
import json, datetime, os, re
BASE = "https://ductsoncall-hub.github.io/ductsoncall-madison/"
PHONE = "(608) 906-1008"; TEL = "+16089061008"
TODAY = datetime.date.today().isoformat()
OUT = os.path.dirname(os.path.abspath(__file__))

CITIES = [
 # slug, name, county, blurb (factual/geographic only), neighbors
 ("madison","Madison","Dane","Wisconsin's capital and the center of our service area, from the Isthmus to the east and west sides.", ["Fitchburg","Middleton","Sun Prairie","Verona"]),
 ("sun-prairie","Sun Prairie","Dane","A fast-growing city northeast of Madison with many homes built in the last twenty years.", ["Madison","DeForest","Waunakee","Columbus"]),
 ("waunakee","Waunakee","Dane","A village north of Madison along WI-19 with a mix of newer subdivisions and older homes.", ["Madison","DeForest","Middleton","Lodi"]),
 ("middleton","Middleton","Dane","Directly west of Madison, with established neighborhoods and plenty of finished basements.", ["Madison","Waunakee","Verona","Lodi"]),
 ("verona","Verona","Dane","Southwest of Madison, home to many newer two-story homes with long duct runs.", ["Madison","Fitchburg","Middleton","Stoughton"]),
 ("fitchburg","Fitchburg","Dane","Just south of Madison, with a wide range of housing from the 1960s to today.", ["Madison","Verona","Stoughton","Sun Prairie"]),
 ("deforest","DeForest","Dane","North of Madison off I-39/90, with many homes built since 2000.", ["Sun Prairie","Waunakee","Poynette","Madison"]),
 ("stoughton","Stoughton","Dane","Southeast of Madison on the Yahara River, with a historic downtown and older housing stock.", ["Fitchburg","Verona","Madison","Sun Prairie"]),
 ("poynette","Poynette","Columbia","Our home base in Columbia County, between Madison and Portage.", ["Lodi","Portage","DeForest","Columbus"]),
 ("portage","Portage","Columbia","The Columbia County seat on the Wisconsin River, about 35 miles north of Madison.", ["Poynette","Lodi","Columbus","DeForest"]),
 ("lodi","Lodi","Columbia","A small city northwest of Madison near Lake Wisconsin.", ["Poynette","Waunakee","Middleton","Portage"]),
 ("columbus","Columbus","Columbia","East of Sun Prairie along US-151, with many older homes and farmsteads.", ["Sun Prairie","Poynette","Portage","DeForest"]),
]

FAQ = [
 ("Do my air ducts actually need cleaning?",
  "Not always, and we will tell you if they don't. The EPA says duct cleaning is reasonable when there is visible mold growth inside ducts or on HVAC components, when ducts are infested with vermin, or when they are clogged with excessive dust and debris that is released into the home. Every job starts with a free inspection so you can see what is in the system before deciding."),
 ("How is Ducts On Call different from other duct cleaners in Madison?",
  "Nick Bellino, the owner, is a NADCA-certified Air Systems Cleaning Specialist (ASCS) and the author of five books on mold, mycotoxins and indoor air quality. He answers the phone, performs the inspection and does the work himself. There is no call center and no sales team."),
 ("What does the cleaning process involve?",
  "The system is placed under negative pressure with a portable HEPA-filtered vacuum drawing 5,000 CFM (two 2,500 CFM motors), so dislodged debris is pulled out of the home rather than into it. Each vent, register, grill and diffuser is removed and washed by hand with an environmentally safe degreaser. For odor elimination the openings are blocked to maximize suction, the system is brushed, then air-washed with 180 PSI of fresh outside air."),
 ("How often should ducts be cleaned?",
  "The EPA recommends cleaning as needed rather than on a fixed schedule. NADCA's ACR standard suggests inspecting air handling units yearly and ductwork about every two years, more often with pets, smokers, recent renovation, water damage or occupants with respiratory sensitivities."),
 ("How much does it cost?",
  "Dryer vent cleaning is a flat $175. Air duct cleaning is quoted per system after the free inspection, so the price reflects your actual home: number of vents, furnace and air conditioner, and what the inspection finds. No surprises on the day."),
 ("Will it make a mess in my house?",
  "No. Technicians wear shoe coverings, floors are protected with coverings, and corner guards protect your drywall and trim. The home's air is HEPA-filtered to 0.3 microns during the job."),
 ("Do you serve my town?",
  "We serve Madison and the surrounding Dane and Columbia County communities including Sun Prairie, Waunakee, Middleton, Verona, Fitchburg, DeForest, Stoughton, Poynette, Portage, Lodi and Columbus. Call or text " + PHONE + " if you are nearby but not listed."),
 ("Can you test for mold or mycotoxins before cleaning?",
  "Yes. Indoor air quality services include pollutant assessment, mycotoxin testing, humidity assessment and environmental testing. Nick tests and reports what the results show; he does not diagnose or treat health conditions."),
]

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}assets/hero-living-room.jpg">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="US-WI"><meta name="geo.placename" content="{place}">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@500,700,800&f[]=general-sans@400,500,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{rel}index.html"><img src="{rel}assets/ductsoncall-logo.png" alt="Ducts On Call" width="200" height="48"></a>
    <nav class="primary" aria-label="Primary">
      <a href="{rel}air-duct-cleaning.html"{c_adc}>Air duct cleaning</a>
      <a href="{rel}dryer-vent-cleaning.html"{c_dvc}>Dryer vents</a>
      <a href="{rel}indoor-air-quality.html"{c_iaq}>Indoor air quality</a>
      <a href="{rel}service-area.html"{c_area}>Service area</a>
      <a href="{rel}faq.html"{c_faq}>FAQ</a>
    </nav>
    <a class="btn phone" href="tel:{tel}">Call or text {phone}</a>
  </div>
</header>
<main id="main">
'''

FOOT = '''
</main>
<section class="cta-band" id="contact">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Free inspection</p>
      <h2>Talk to Nick. He answers.</h2>
      <p>Call or text 7 AM to 7 PM. By appointment and referral across Madison and the surrounding Dane and Columbia County communities.</p>
    </div>
    <div class="cta-actions">
      <a class="btn big" href="tel:{tel}">{phone}</a>
      <a class="btn ghost" href="https://ductsoncall.com/get-in-touch" target="_blank" rel="noopener noreferrer">Request an appointment online</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap cols">
    <div>
      <img src="{rel}assets/ductsoncall-logo.png" alt="Ducts On Call" width="160" height="38" loading="lazy">
      <p class="small">Ducts On Call Inc. · N3303 County Highway J, Poynette, WI 53955 · <a href="tel:{tel}">{phone}</a></p>
      <p class="small">NADCA member since 2022 · ASCS-certified · Licensed &amp; insured · BBB A+ rated</p>
    </div>
    <div>
      <p class="small"><strong>Services</strong></p>
      <p class="small"><a href="{rel}air-duct-cleaning.html">Air duct cleaning</a><br><a href="{rel}dryer-vent-cleaning.html">Dryer vent cleaning</a><br><a href="{rel}indoor-air-quality.html">Indoor air quality &amp; mycotoxin testing</a></p>
    </div>
    <div>
      <p class="small"><strong>Service area</strong></p>
      <p class="small">{citylinks}</p>
    </div>
    <div>
      <p class="small"><strong>Elsewhere</strong></p>
      <p class="small"><a href="https://ductsoncall.com/" target="_blank" rel="noopener noreferrer">ductsoncall.com</a><br><a href="https://ductsoncall-hub.github.io/nick-bellino/" target="_blank" rel="noopener noreferrer">About Nick Bellino</a><br><a href="https://www.youtube.com/channel/UCAnxNY8XmPkzigamDoIeTow" target="_blank" rel="noopener noreferrer">YouTube (140+ videos)</a><br><a href="https://ductsoncall-hub.github.io/ductsoncall-videos/" target="_blank" rel="noopener noreferrer">Video archive</a><br><a href="https://nadca.com/find-a-professional/ducts-call" target="_blank" rel="noopener noreferrer">NADCA listing</a><br><a href="https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177" target="_blank" rel="noopener noreferrer">BBB profile</a></p>
    </div>
  </div>
  <div class="wrap small muted" style="margin-top:1.5rem">© 2026 Ducts On Call Inc. Duct cleaning has not been shown by the EPA to prevent health problems; it is appropriate when there is visible mold, vermin, or excessive debris. Nick tests and reports but does not diagnose or treat health conditions.</div>
</footer>
</body>
</html>
'''

def business_ld(extra_area=None):
    return {
      "@type": "HomeAndConstructionBusiness",
      "@id": BASE + "#business",
      "name": "Ducts On Call Inc.",
      "alternateName": "Ducts On Call",
      "image": BASE + "assets/hero-living-room.jpg",
      "logo": BASE + "assets/ductsoncall-logo.png",
      "url": BASE,
      "sameAs": ["https://ductsoncall.com/", "https://nadca.com/find-a-professional/ducts-call",
                 "https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177",
                 "https://www.yelp.com/biz/ducts-on-call-sun-prairie-2", "https://www.youtube.com/channel/UCAnxNY8XmPkzigamDoIeTow",
                 "https://www.linkedin.com/company/ducts-on-call", "https://www.facebook.com/298866327432382", "https://www.instagram.com/ductsoncallinc"],
      "telephone": TEL, "email": "ductsoncall@gmail.com",
      "address": {"@type": "PostalAddress", "streetAddress": "N3303 County Highway J", "addressLocality": "Poynette", "addressRegion": "WI", "postalCode": "53955", "addressCountry": "US"},
      "geo": {"@type": "GeoCoordinates", "latitude": 43.39, "longitude": -89.40},
      "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "19:00"}],
      "priceRange": "$$",
      "founder": {"@type": "Person", "name": "Nick Bellino", "url": "https://ductsoncall-hub.github.io/nick-bellino/", "jobTitle": "Owner, NADCA ASCS"},
      "memberOf": {"@type": "Organization", "name": "National Air Duct Cleaners Association (NADCA)"},
      "areaServed": [{"@type": "City", "name": f"{n}, WI"} for _, n, *_ in CITIES],
      "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Air duct cleaning", "url": BASE + "air-duct-cleaning.html"}},
        {"@type": "Offer", "price": "175", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Dryer vent cleaning", "url": BASE + "dryer-vent-cleaning.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Indoor air quality and mycotoxin testing", "url": BASE + "indoor-air-quality.html"}},
      ]},
    }

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

def citylinks(rel):
    return " · ".join(f'<a href="{rel}areas/{s}.html">{n}</a>' for s, n, *_ in CITIES)

def render(fn, title, desc, body, ld, current="", place="Madison, Wisconsin", sub=False):
    rel = "../" if sub else "./"
    canon = BASE + fn
    cur = {k: (' aria-current="page"' if current == k else '') for k in ["adc","dvc","iaq","area","faq"]}
    html = HEAD.format(title=title, desc=desc, canon=canon, base=BASE, rel=rel, place=place, ld=json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False), tel=TEL, phone=PHONE,
                       c_adc=cur["adc"], c_dvc=cur["dvc"], c_iaq=cur["iaq"], c_area=cur["area"], c_faq=cur["faq"])
    html += body + FOOT.format(tel=TEL, phone=PHONE, rel=rel, citylinks=citylinks(rel))
    path = os.path.join(OUT, fn); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(html)
    return canon

urls = []

# ---------- Home ----------
home_body = f'''
<section class="hero">
  <div class="wrap grid">
    <div>
      <p class="eyebrow">Air duct cleaning · Madison, Wisconsin</p>
      <h1>Madison air duct cleaning, done by the person who answers the phone.</h1>
      <p class="lede">NADCA-certified, licensed and insured. Nick Bellino inspects first, tells you honestly whether your ducts need cleaning, then cleans the whole system under HEPA-filtered vacuum. Serving Madison and the surrounding Dane and Columbia County communities.</p>
      <div class="actions">
        <a class="btn big" href="tel:{TEL}">Call or text {PHONE}</a>
        <a class="btn ghost" href="#process">See how the work is done</a>
      </div>
      <ul class="trust">
        <li>NADCA member since 2022</li><li>ASCS-certified owner</li><li>BBB A+ rated</li><li>Free inspection</li>
      </ul>
    </div>
    <figure class="hero-img"><img src="./assets/hero-living-room.jpg" alt="Sunlit living room with a brass floor register in the foreground" width="1536" height="864" fetchpriority="high"></figure>
  </div>
</section>

<section class="block" id="services">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Services</p><h2>Three things, done thoroughly.</h2></div>
    <div class="cards three">
      <a class="card" href="./air-duct-cleaning.html">
        <h3>Air duct cleaning</h3>
        <p>Whole-system mechanical cleaning under 5,000 CFM negative pressure. Every vent, register, grill and diffuser hand-washed. Odor elimination and bio-growth treatment available.</p>
        <span class="more">Quoted per system →</span>
      </a>
      <a class="card" href="./dryer-vent-cleaning.html">
        <h3>Dryer vent cleaning</h3>
        <p>Lint removal from the dryer to the exterior hood. Shorter dry times, lower fire risk, and a look at the transition duct behind the machine.</p>
        <span class="more">$175 flat →</span>
      </a>
      <a class="card" href="./indoor-air-quality.html">
        <h3>Indoor air quality testing</h3>
        <p>Pollutant assessment, mycotoxin testing, humidity and environmental testing. Know what is in your air before you spend money cleaning it.</p>
        <span class="more">Test first →</span>
      </a>
    </div>
  </div>
</section>

<section class="block alt" id="process">
  <div class="wrap grid two">
    <figure><img src="./assets/process-vacuum.jpg" alt="Technician guiding a large vacuum hose into a floor duct opening over a protective runner mat" width="1024" height="768" loading="lazy"></figure>
    <div>
      <p class="eyebrow">How the work is done</p>
      <h2>Under vacuum, by hand, with your floors covered.</h2>
      <ol class="steps">
        <li><strong>Free inspection.</strong> Nick looks inside the system and shows you what he finds. If it doesn't need cleaning, he says so.</li>
        <li><strong>Protect the home.</strong> Shoe coverings, floor coverings and corner guards on drywall and trim.</li>
        <li><strong>Negative pressure.</strong> A portable vacuum with two 2,500 CFM motors pulls 5,000 CFM through the system while HEPA-filtering your indoor air to 0.3 µm.</li>
        <li><strong>Every opening.</strong> Each vent, register, grill and diffuser is removed and washed with an environmentally safe degreaser.</li>
        <li><strong>Brush and air-wash.</strong> For odor elimination, openings are blocked, the system is brushed, then air-washed with 180 PSI of fresh outside air.</li>
      </ol>
    </div>
  </div>
</section>

<section class="block" id="why">
  <div class="wrap grid two">
    <div>
      <p class="eyebrow">Who shows up</p>
      <h2>Nick Bellino, owner. NADCA-certified, and he wrote the book on it. Five, actually.</h2>
      <p>Nick holds NADCA's Air Systems Cleaning Specialist (ASCS) certification and an Indoor Air Quality Technician certification, and has written five books on mold, mycotoxins and indoor air quality. He answers the phone, performs the inspection and does the cleaning himself.</p>
      <p><a class="btn ghost" href="https://ductsoncall-hub.github.io/nick-bellino/" target="_blank" rel="noopener noreferrer">More about Nick and his books</a></p>
    </div>
    <div class="proof">
      <a href="https://nadca.com/find-a-professional/ducts-call" target="_blank" rel="noopener noreferrer"><strong>NADCA</strong><span>Certified personnel: Nick Bellino, ASCS · member since 02/11/2022</span></a>
      <a href="https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177" target="_blank" rel="noopener noreferrer"><strong>BBB A+</strong><span>Ducts On Call Inc., Poynette, WI</span></a>
      <a href="https://www.yelp.com/biz/ducts-on-call-sun-prairie-2" target="_blank" rel="noopener noreferrer"><strong>Yelp</strong><span>Claimed profile · 61 photos</span></a>
      <a href="https://www.youtube.com/channel/UCAnxNY8XmPkzigamDoIeTow" target="_blank" rel="noopener noreferrer"><strong>YouTube</strong><span>140+ homeowner guides and indoor-air Shorts</span></a>
    </div>
  </div>
</section>

<section class="block alt" id="area">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Service area</p><h2>Madison and the communities around it.</h2></div>
    <div class="citygrid">
      {"".join(f'<a href="./areas/{s}.html">{n}<span>{c} County</span></a>' for s,n,c,*_ in CITIES)}
    </div>
  </div>
</section>

<section class="block" id="faq">
  <div class="wrap narrow">
    <div class="section-head"><p class="eyebrow">Questions</p><h2>Straight answers.</h2></div>
    {faq_html(FAQ[:5])}
    <p style="margin-top:1.5rem"><a href="./faq.html">All questions →</a></p>
  </div>
</section>
'''
urls.append(render("index.html", "Air Duct Cleaning Madison WI | Ducts On Call – NADCA Certified, Owner-Operated",
  "NADCA-certified air duct cleaning, dryer vent cleaning and indoor air quality testing in Madison, WI and surrounding Dane & Columbia County. Owner Nick Bellino inspects first and answers the phone. Call or text (608) 906-1008.",
  home_body, [business_ld(), faq_ld(FAQ[:5]), {"@type":"WebSite","url":BASE,"name":"Ducts On Call – Madison Air Duct Cleaning","publisher":{"@id":BASE+"#business"}}]))

# ---------- Service pages ----------
def service_page(fn, cur, title, desc, h1, lede, img, alt, sections, faq, svc_name, price=None):
    body = f'''
<section class="page-head"><div class="wrap grid">
  <div><p class="eyebrow">Service · Madison, WI</p><h1>{h1}</h1><p class="lede">{lede}</p>
  <div class="actions"><a class="btn big" href="tel:{TEL}">Call or text {PHONE}</a></div></div>
  <figure class="hero-img"><img src="./assets/{img}" alt="{alt}" width="1024" height="768"></figure>
</div></section>
<section class="block"><div class="wrap narrow prose">{sections}</div></section>
<section class="block alt"><div class="wrap narrow"><div class="section-head"><p class="eyebrow">Questions</p><h2>About this service</h2></div>{faq_html(faq)}</div></section>
'''
    svc = {"@type":"Service","name":svc_name,"serviceType":svc_name,"provider":{"@id":BASE+"#business"},"areaServed":[{"@type":"City","name":f"{n}, WI"} for _,n,*_ in CITIES],"url":BASE+fn}
    if price: svc["offers"] = {"@type":"Offer","price":price,"priceCurrency":"USD"}
    urls.append(render(fn, title, desc, body, [business_ld(), svc, faq_ld(faq)], current=cur))

service_page("air-duct-cleaning.html","adc",
 "Air Duct Cleaning in Madison, WI – Whole-System, HEPA Vacuum | Ducts On Call",
 "Professional air duct cleaning in Madison, Wisconsin: 5,000 CFM negative-pressure vacuum, HEPA filtration to 0.3 µm, every register hand-washed. NADCA ASCS-certified. Free inspection, quoted per system.",
 "Air duct cleaning in Madison, the thorough way.",
 "Whole-system mechanical cleaning under negative pressure, every register washed by hand, and your indoor air HEPA-filtered while it happens. Quoted per system after a free inspection.",
 "process-vacuum.jpg","Technician guiding a vacuum hose into a floor duct opening",
 '''<h2>What is included</h2>
<p>Air duct cleaning at Ducts On Call is the physical and mechanical removal of contaminants from the network of ducting, plenums and stacks. The system is placed under negative pressure using a portable vacuum with two 2,500 CFM motors, pulling 5,000 CFM through the ductwork so dislodged debris leaves the house rather than settling back into your rooms. While the system is under vacuum, the air in your home is HEPA-filtered down to 0.3 microns.</p>
<p>Every vent, register, grill and diffuser is removed and washed in an environmentally safe degreaser. Supply and return runs, trunk lines, the plenum and the furnace cabinet are all part of the job.</p>
<h2>Odor elimination and bio-growth treatment</h2>
<p>If the complaint is a smell when the furnace kicks on, the approach changes: all duct openings are blocked to maximize suction, the whole system is brushed, then air-washed with 180 PSI of fresh outside air. Where inspection or testing shows biological growth, a bio-growth treatment can follow the mechanical cleaning. The EPA is clear that cleaning alone does not fix a moisture problem, so Nick will point out the source if he sees one.</p>
<h2>When it is worth doing</h2>
<p>The EPA recommends duct cleaning when there is substantial visible mold inside hard-surface ducts or on other HVAC components, when ducts are infested with vermin, or when they are clogged with excessive dust and debris that is actually released into the home. Other common reasons homeowners in Madison call: a renovation that produced a lot of drywall dust, a newly purchased home with an unknown history, pets, smokers, or dust visibly blowing from registers.</p>
<h2>Pricing</h2>
<p>Air duct cleaning is quoted per system after the free inspection. The quote depends on the number of vents, whether the furnace and air conditioner coil are included, and what the inspection shows. You see the price before any work starts.</p>
<h2>Commercial and residential</h2>
<p>Ducts On Call is listed with NADCA for both residential and commercial work: offices, rental turnovers, restaurants, daycares and property management portfolios across greater Madison.</p>''',
 [FAQ[0],FAQ[2],FAQ[3],FAQ[4],FAQ[5]], "Air duct cleaning")

service_page("dryer-vent-cleaning.html","dvc",
 "Dryer Vent Cleaning Madison WI – $175 Flat | Ducts On Call",
 "Dryer vent cleaning in Madison, Sun Prairie, Waunakee and surrounding Wisconsin communities for a flat $175. Lint removed from dryer to exterior hood by NADCA-certified Ducts On Call. Call or text (608) 906-1008.",
 "Dryer vent cleaning, $175 flat.",
 "Lint removed from the back of the dryer to the exterior hood. Shorter dry times, lower fire risk, and a look at the transition duct most people never see.",
 "dryer-vent.jpg","Exterior dryer vent on the side of a ranch house with lint caught in the louvers",
 '''<h2>Why it matters</h2>
<p>Lint is highly flammable, and a dryer vent slowly packs with it. The U.S. Fire Administration reports that failure to clean is the leading factor contributing to clothes-dryer fires in residential buildings. A clogged vent also makes the dryer run longer and hotter, which costs energy and shortens the life of the machine.</p>
<h2>What is included</h2>
<p>The full run is cleaned, from the transition duct behind the dryer to the exterior hood, including the louvered cover where lint and sometimes bird nests collect. Nick checks the transition duct for crushed or foil-type flexible duct that should be replaced, and confirms airflow at the exterior when the job is finished.</p>
<h2>Signs it is time</h2>
<ul><li>Clothes take two cycles to dry</li><li>The top of the dryer or the laundry room feels hot</li><li>A burning smell during a cycle</li><li>Lint collecting around the exterior hood or behind the dryer</li><li>You have never had it cleaned since moving in</li></ul>
<h2>Pricing</h2>
<p>Dryer vent cleaning is a flat $175. It is often combined with an air duct cleaning visit.</p>''',
 [("How often should a dryer vent be cleaned?","Most homes benefit from yearly cleaning; more often for large families, long vent runs, or vents with several bends. If drying times climb, don't wait for the schedule."),
  ("Can you clean a vent that exits through the roof?","Yes. Roof and long-run vents are cleaned from both ends where access allows, and airflow is checked at the exit."),
  FAQ[6]], "Dryer vent cleaning", price="175")

service_page("indoor-air-quality.html","iaq",
 "Indoor Air Quality & Mycotoxin Testing Madison WI | Ducts On Call",
 "Indoor air quality testing in Madison, Wisconsin: pollutant assessment, mycotoxin testing, humidity and environmental testing by NADCA-certified Nick Bellino, author of five books on mold and indoor air. Know what's in your air before you clean.",
 "Find out what is in your air first.",
 "Pollutant assessment, mycotoxin testing, humidity and environmental testing. Nick tests and reports what the results show, then recommends only what the results support.",
 "hero-living-room.jpg","Sunlit living room with dust motes visible in a sunbeam near a floor register",
 '''<h2>Why test before cleaning</h2>
<p>A growing body of evidence indicates the air inside buildings can be more polluted than outdoor air. But the right response depends on what is actually there: particulate from a renovation calls for a different fix than hidden moisture feeding mold in a return. Testing first means you spend money on the thing that is actually wrong.</p>
<h2>What can be assessed</h2>
<ul><li>Mold and mycotoxin presence in air and on surfaces</li><li>Particulate matter and dust load in the system</li><li>Volatile organic compounds (VOCs) from materials and products</li><li>Humidity and conditions that support bio-growth</li><li>Odor sources in ductwork and HVAC components</li></ul>
<h2>What you get</h2>
<p>A plain-English report of what was found and where, with recommendations limited to what the results support: sometimes a cleaning, sometimes a moisture fix, sometimes nothing at all. Nick is an indoor air specialist, not a medical provider; he does not diagnose or treat health conditions.</p>
<h2>Written by someone who studies this</h2>
<p>Nick Bellino is the author of five books on mold, mycotoxins and indoor air quality and of a doctoral-level literature review on the economics of residential mold contamination. <a href="https://ductsoncall-hub.github.io/nick-bellino/books.html" target="_blank" rel="noopener noreferrer">See the books</a>.</p>''',
 [FAQ[7],FAQ[0],("Does duct cleaning improve indoor air quality?","It can when the ducts themselves are a source: visible mold, vermin, or heavy debris being released into the home. The EPA has not found that routine duct cleaning prevents health problems, which is exactly why Ducts On Call inspects and tests before recommending it.")], "Indoor air quality testing")

# ---------- Service area index + city pages ----------
area_body = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">Service area</p><h1>Air duct cleaning across greater Madison.</h1>
<p class="lede">Ducts On Call is based in Poynette and works by appointment and referral throughout Dane and Columbia County. Pick your community for local details.</p></div></section>
<section class="block"><div class="wrap"><div class="citygrid">{"".join(f'<a href="./areas/{s}.html">{n}<span>{c} County</span></a>' for s,n,c,*_ in CITIES)}</div>
<p class="note" style="margin-top:2rem">Not listed? We regularly travel a little further. Call or text <a href="tel:{TEL}">{PHONE}</a>.</p></div></section>
'''
urls.append(render("service-area.html","Service Area – Air Duct Cleaning in Dane & Columbia County, WI | Ducts On Call",
  "Ducts On Call serves Madison, Sun Prairie, Waunakee, Middleton, Verona, Fitchburg, DeForest, Stoughton, Poynette, Portage, Lodi and Columbus, Wisconsin with NADCA-certified air duct and dryer vent cleaning.",
  area_body, [business_ld()], current="area"))

for slug, name, county, blurb, neigh in CITIES:
    body = f'''
<section class="page-head"><div class="wrap grid">
  <div><p class="eyebrow">Service area · {county} County, WI</p><h1>Air duct cleaning in {name}, Wisconsin</h1>
  <p class="lede">{blurb} Ducts On Call provides NADCA-certified air duct cleaning, dryer vent cleaning and indoor air quality testing to {name} homes and businesses, by appointment and referral.</p>
  <div class="actions"><a class="btn big" href="tel:{TEL}">Call or text {PHONE}</a></div></div>
  <figure class="hero-img"><img src="../assets/hero-living-room.jpg" alt="Sunlit living room with a brass floor register" width="1536" height="864"></figure>
</div></section>
<section class="block"><div class="wrap narrow prose">
<h2>What we do in {name}</h2>
<ul>
<li><a href="../air-duct-cleaning.html">Air duct cleaning</a>: whole-system cleaning under 5,000 CFM negative pressure with HEPA filtration to 0.3 µm; every register hand-washed. Quoted per system after a free inspection.</li>
<li><a href="../dryer-vent-cleaning.html">Dryer vent cleaning</a>: $175 flat, from the dryer to the exterior hood.</li>
<li><a href="../indoor-air-quality.html">Indoor air quality and mycotoxin testing</a>: know what is in the air before paying to clean it.</li>
</ul>
<h2>Who comes to your door</h2>
<p>Nick Bellino, the owner. He is a NADCA-certified Air Systems Cleaning Specialist, holds an Indoor Air Quality Technician certification, and has written five books on mold, mycotoxins and indoor air quality. He answers the phone, performs the inspection and does the cleaning himself. The business is licensed, insured and BBB A+ rated.</p>
<h2>An honest first step</h2>
<p>Every {name} job starts with a free inspection. If your ducts don't need cleaning, Nick will tell you. The EPA recommends duct cleaning when there is visible mold, vermin, or excessive debris being released into the home, and that is the standard he works to.</p>
<h2>Nearby</h2>
<p>We also serve {", ".join(f'<a href="./{[c[0] for c in CITIES if c[1]==x][0]}.html">{x}</a>' for x in neigh)} and the rest of greater Madison.</p>
</div></section>
<section class="block alt"><div class="wrap narrow"><div class="section-head"><p class="eyebrow">Questions</p><h2>{name} homeowners ask</h2></div>{faq_html([FAQ[0],FAQ[4],FAQ[5]])}</div></section>
'''
    ld = [business_ld(), {"@type":"Service","name":f"Air duct cleaning in {name}, WI","serviceType":"Air duct cleaning","provider":{"@id":BASE+"#business"},"areaServed":{"@type":"City","name":f"{name}, WI"},"url":BASE+f"areas/{slug}.html"}, faq_ld([FAQ[0],FAQ[4],FAQ[5]]),
          {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Service area","item":BASE+"service-area.html"},{"@type":"ListItem","position":3,"name":name,"item":BASE+f"areas/{slug}.html"}]}]
    urls.append(render(f"areas/{slug}.html", f"Air Duct Cleaning {name} WI | NADCA-Certified, Owner-Operated | Ducts On Call",
      f"Air duct cleaning, dryer vent cleaning ($175) and indoor air quality testing in {name}, Wisconsin by NADCA ASCS-certified Nick Bellino of Ducts On Call. Free inspection. Call or text (608) 906-1008.",
      body, ld, current="area", place=f"{name}, Wisconsin", sub=True))

# ---------- FAQ ----------
faq_body = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">FAQ</p><h1>Air duct cleaning questions, answered honestly.</h1>
<p class="lede">Based on EPA and NADCA guidance and on how Ducts On Call actually works. If your question isn't here, call or text {PHONE}.</p></div></section>
<section class="block"><div class="wrap narrow">{faq_html(FAQ)}</div></section>
'''
urls.append(render("faq.html","Air Duct Cleaning FAQ – Madison WI | Ducts On Call",
  "Do ducts need cleaning? How often? What does it cost? Honest answers from NADCA-certified Ducts On Call in Madison, Wisconsin, based on EPA and NADCA guidance.",
  faq_body, [business_ld(), faq_ld(FAQ)], current="faq"))

# ---------- sitemap / robots ----------
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
open(os.path.join(OUT,".nojekyll"),"w").write("")
print(f"built {len(urls)} pages")
