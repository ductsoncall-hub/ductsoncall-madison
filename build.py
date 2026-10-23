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
 ("cottage-grove","Cottage Grove","Dane","East of Madison off I-94, a growing village with many homes built since the 1990s.", ["Madison","Sun Prairie","Stoughton","McFarland"]),
 ("oregon","Oregon","Dane","South of Madison on US-14, a village of established and newer subdivisions.", ["Fitchburg","Verona","Stoughton","McFarland"]),
 ("mcfarland","McFarland","Dane","Southeast of Madison on Lake Waubesa, with lakeside homes and finished basements.", ["Madison","Stoughton","Oregon","Cottage Grove"]),
 ("monona","Monona","Dane","Surrounded by Madison on Lake Monona, with mostly mid-century ranch and split-level homes.", ["Madison","McFarland","Cottage Grove","Fitchburg"]),
 ("cross-plains","Cross Plains","Dane","West of Middleton on US-14 in the Driftless hills.", ["Middleton","Mount Horeb","Verona","Lodi"]),
 ("mount-horeb","Mount Horeb","Dane","Southwest of Madison on US-18/151, with older village homes and newer edge subdivisions.", ["Verona","Cross Plains","Middleton","Fitchburg"]),
 ("windsor","Windsor","Dane","North of Madison next to DeForest, with newer construction along the I-39/90 corridor.", ["DeForest","Sun Prairie","Waunakee","Poynette"]),
 ("marshall","Marshall","Dane","Northeast of Sun Prairie on WI-19, a village of older homes and surrounding farmsteads.", ["Sun Prairie","Columbus","Cottage Grove","Madison"]),
 ("wisconsin-dells","Wisconsin Dells","Columbia","North of Portage on the Wisconsin River, with year-round homes, rentals and hospitality properties.", ["Portage","Poynette","Lodi","Pardeeville"]),
 ("pardeeville","Pardeeville","Columbia","East of Portage on Park Lake, a small village in the middle of Columbia County.", ["Portage","Poynette","Columbus","Wisconsin Dells"]),
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
  "We serve Madison and the surrounding Dane and Columbia County communities including " + ", ".join(n for _, n, *_ in CITIES[1:-1]) + " and " + CITIES[-1][1] + ". Call or text " + PHONE + " if you are nearby but not listed."),
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
<meta property="og:image" content="{ogimg}">
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
      <a href="{rel}commercial.html"{c_com}>Commercial</a>
      <a href="{rel}service-area.html"{c_area}>Service area</a>
      <a href="{rel}guides/index.html"{c_guides}>Guides</a>
      <a href="{rel}reviews.html"{c_rev}>Reviews</a>
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
      <a class="btn ghost" href="sms:{tel}?&body=Hi%20Nick%2C%20I%27d%20like%20a%20free%20duct%20inspection.%20My%20town%20is%20">Text Nick instead</a>
    </div>
  </div>
  <div class="wrap">
    <form class="lead-form" action="https://formsubmit.co/ductsoncall@gmail.com" method="POST">
      <input type="hidden" name="_subject" value="New inspection request from ductsoncall-madison site">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="{base}thanks.html">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <input type="hidden" name="page" value="{canon}">
      <h3>Or request your free inspection here</h3>
      <div class="lead-grid">
        <label>Name<input type="text" name="name" required autocomplete="name"></label>
        <label>Phone<input type="tel" name="phone" required autocomplete="tel" placeholder="(608) 555-0100"></label>
        <label>Town<input type="text" name="town" required placeholder="Madison, Sun Prairie, Waunakee…"></label>
        <label>What do you need?<select name="service"><option>Air duct cleaning</option><option>Dryer vent cleaning ($175)</option><option>Indoor air quality / mold testing</option><option>Commercial</option><option>Not sure – inspection first</option></select></label>
        <label class="full"><span>Anything Nick should know? <span class="opt">(optional)</span></span><textarea name="notes" rows="2" placeholder="Dust from vents, musty smell when furnace runs, just moved in, pets…"></textarea></label>
      </div>
      <div class="lead-actions"><button class="btn big" type="submit">Request free inspection</button><span class="small">Nick replies personally, usually the same day. No call center, no spam.</span></div>
    </form>
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
      <p class="small"><a href="{rel}air-duct-cleaning.html">Air duct cleaning</a><br><a href="{rel}dryer-vent-cleaning.html">Dryer vent cleaning</a><br><a href="{rel}indoor-air-quality.html">Indoor air quality &amp; mycotoxin testing</a><br><a href="{rel}commercial.html">Commercial &amp; industrial</a><br><a href="{rel}gallery.html">Before &amp; after</a><br><a href="{rel}guides/index.html">Homeowner guides</a><br><a href="{rel}reviews.html">Reviews</a></p>
    </div>
    <div>
      <p class="small"><strong>Service area</strong></p>
      <p class="small">{citylinks}</p>
    </div>
    <div>
      <p class="small"><strong>Elsewhere</strong></p>
      <p class="small"><a href="https://ductsoncall.com/" target="_blank" rel="noopener noreferrer">ductsoncall.com</a><br><a href="https://ductsoncall-hub.github.io/nick-bellino/" target="_blank" rel="noopener noreferrer">About Nick Bellino</a><br><a href="https://nick-bellino.pplx.app/" target="_blank" rel="noopener noreferrer">Nick's credentials &amp; books</a><br><a href="https://www.youtube.com/channel/UCAnxNY8XmPkzigamDoIeTow" target="_blank" rel="noopener noreferrer">YouTube (140+ videos)</a><br><a href="https://ductsoncall-hub.github.io/ductsoncall-videos/" target="_blank" rel="noopener noreferrer">Video archive</a><br><a href="https://nadca.com/find-a-professional/ducts-call" target="_blank" rel="noopener noreferrer">NADCA listing</a><br><a href="https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177" target="_blank" rel="noopener noreferrer">BBB profile</a></p>
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

def render(fn, title, desc, body, ld, current="", place="Madison, Wisconsin", sub=False, ogimg=None):
    rel = "../" if sub else "./"
    canon = BASE + fn
    cur = {k: (' aria-current="page"' if current == k else '') for k in ["adc","dvc","iaq","area","faq","com","guides","rev"]}
    html = HEAD.format(title=title, desc=desc, canon=canon, base=BASE, rel=rel, place=place, ogimg=(ogimg or BASE+"assets/og-ductsoncall.jpg"), ld=json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False), tel=TEL, phone=PHONE,
                       c_adc=cur["adc"], c_dvc=cur["dvc"], c_iaq=cur["iaq"], c_area=cur["area"], c_faq=cur["faq"], c_com=cur["com"], c_guides=cur["guides"], c_rev=cur["rev"])
    html += body + FOOT.format(tel=TEL, phone=PHONE, rel=rel, citylinks=citylinks(rel), base=BASE, canon=canon)
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

<section class="block" id="proof">
  <div class="wrap grid two">
    <div>
      <p class="eyebrow">What customers say</p>
      <h2>5.0 stars, everywhere we're listed.</h2>
      <blockquote class="quote">“Very professional and courteous. Nick, Rocko, and Kim from Poynette came out to our house to clean our vents. They were very knowledgeable and took the time to explain everything to us. It was very apparent that they cared about the quality of their work, as well as the health and well-being of my family.”<footer>Houzz review, July 2021</footer></blockquote>
      <p><a class="btn ghost" href="./reviews.html">Read reviews and leave yours</a></p>
    </div>
    <div class="ba">
      <figure><img src="./assets/job-01-before.jpg" alt="Inside a return duct before cleaning: heavy grey dust and debris on every surface" width="600" height="400" loading="lazy"><figcaption>Before · Madison return duct</figcaption></figure>
      <figure><img src="./assets/job-01-after.jpg" alt="Inside the same return duct after cleaning: bare clean sheet metal" width="600" height="400" loading="lazy"><figcaption>After</figcaption></figure>
      <p class="small"><a href="./gallery.html">More before &amp; after →</a></p>
    </div>
  </div>
</section>

<section class="block alt" id="guides">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Homeowner guides</p><h2>Read before you book anyone.</h2></div>
    <div class="cards three">
      <a class="card" href="./guides/air-duct-cleaning-cost-madison.html"><h3>What air duct cleaning costs in Madison</h3><p>Realistic ranges, what drives the price, and the $99 “whole house special” trap.</p><span class="more">Read →</span></a>
      <a class="card" href="./guides/signs-air-ducts-need-cleaning.html"><h3>7 signs your air ducts need cleaning</h3><p>And three that are commonly misread. Based on EPA and NADCA guidance.</p><span class="more">Read →</span></a>
      <a class="card" href="./guides/dryer-vent-fire-safety.html"><h3>Dryer vent fire safety</h3><p>Why lint is the leading factor in dryer fires and the five-minute check.</p><span class="more">Read →</span></a>
    </div>
    <p style="margin-top:1.5rem"><a href="./guides/index.html">All guides →</a></p>
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
<section class="block alt"><div class="wrap"><div class="section-head"><p class="eyebrow">Based in Poynette</p><h2>Between Madison and Portage.</h2></div>
<iframe class="map" src="https://www.google.com/maps?q=N3303+County+Highway+J,+Poynette,+WI+53955&output=embed" title="Map of Ducts On Call, Poynette, Wisconsin" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
<p class="small muted" style="margin-top:.75rem">Ducts On Call Inc. · N3303 County Highway J, Poynette, WI 53955 · Service calls across Dane and Columbia County.</p></div></section>
'''
urls.append(render("service-area.html","Service Area – Air Duct Cleaning in Dane & Columbia County, WI | Ducts On Call",
  "Ducts On Call serves " + ", ".join(n for _, n, *_ in CITIES[:-1]) + " and " + CITIES[-1][1] + ", Wisconsin with NADCA-certified air duct and dryer vent cleaning.",
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


# ---------- Reviews ----------
rev_body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Reviews</p><h1>5.0 stars on every platform that lists us.</h1>
<p class="lede">Ducts On Call is reviewed on Google, Yelp, Houzz and the BBB. Every listing shows a 5.0 rating. Read them at the source, and if Nick has worked in your home, a review is the most useful thank-you there is.</p></div></section>
<section class="block"><div class="wrap">
<blockquote class="quote big">“Very professional and courteous. Nick, Rocko, and Kim from Poynette came out to our house to clean our vents. They were very knowledgeable and took the time to explain everything to us. It was very apparent that they cared about the quality of their work, as well as the health and well-being of my family.”<footer><a href="https://www.houzz.com/professionals/hvac-contractors/madison-wi-us-probr0-bo~t_11814~r_5261457" target="_blank" rel="noopener noreferrer">Houzz review</a>, July 27, 2021</footer></blockquote>
<div class="cards three" style="margin-top:2.5rem">
  <a class="card" href="https://www.google.com/maps/search/Ducts+On+Call+duct+cleaning+Wisconsin" target="_blank" rel="noopener noreferrer"><h3>Google</h3><p>5.0 rating across our Google Business listings (Sun Prairie, Waunakee and Poynette), 38 reviews combined as of October 2026.</p><span class="more">Read on Google Maps →</span></a>
  <a class="card" href="https://www.yelp.com/biz/ducts-on-call-sun-prairie-2" target="_blank" rel="noopener noreferrer"><h3>Yelp</h3><p>5.0 rating. Claimed profile with 61 job photos.</p><span class="more">Read on Yelp →</span></a>
  <a class="card" href="https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177" target="_blank" rel="noopener noreferrer"><h3>Better Business Bureau</h3><p>A+ rating. Ducts On Call Inc., Poynette, Wisconsin.</p><span class="more">View BBB profile →</span></a>
</div>
<div class="note" style="margin-top:2.5rem"><strong>Had Nick out to your home?</strong> Leave a review on <a href="https://www.google.com/maps/search/Ducts+On+Call+duct+cleaning+Wisconsin" target="_blank" rel="noopener noreferrer">Google</a>, <a href="https://www.yelp.com/biz/ducts-on-call-sun-prairie-2" target="_blank" rel="noopener noreferrer">Yelp</a> or <a href="https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177/customer-reviews" target="_blank" rel="noopener noreferrer">BBB</a>. Mention your town so neighbors can find us.</div>
</div></section>
"""
urls.append(render("reviews.html","Ducts On Call Reviews – 5.0 Stars on Google, Yelp, Houzz & BBB | Madison WI Duct Cleaning",
  "Read Ducts On Call reviews: 5.0 stars on Google, Yelp and Houzz, BBB A+ rated. NADCA-certified air duct cleaning in Madison, Sun Prairie, Waunakee and surrounding Wisconsin communities.",
  rev_body, [business_ld(), {"@type":"Review","itemReviewed":{"@id":BASE+"#business"},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"author":{"@type":"Person","name":"Houzz customer"},"datePublished":"2021-07-27","reviewBody":"Very professional and courteous. Nick, Rocko, and Kim from Poynette came out to our house to clean our vents. They were very knowledgeable and took the time to explain everything to us. It was very apparent that they cared about the quality of their work, as well as the health and well-being of my family.","url":"https://www.houzz.com/professionals/hvac-contractors/madison-wi-us-probr0-bo~t_11814~r_5261457"}], current="rev"))

# ---------- Gallery ----------
gal_body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Before &amp; after</p><h1>What's inside a return duct, and what it looks like afterward.</h1>
<p class="lede">Real photos from a Madison job. Return ducts pull air from every room back to the furnace, so they collect the most debris and are the most skipped by rushed cleaners.</p></div></section>
<section class="block"><div class="wrap">
<div class="ba large">
  <figure><img src="./assets/job-01-before.jpg" alt="Inside a return duct before cleaning: heavy grey dust, lint and debris coating every surface" width="1200" height="800"><figcaption>Before. Years of dust, pet hair and drywall debris on every surface of the return.</figcaption></figure>
  <figure><img src="./assets/job-01-after.jpg" alt="Inside the same return duct after cleaning: bare, clean sheet metal" width="1200" height="800"><figcaption>After. Bare sheet metal after brushing and air-washing under 5,000 CFM negative pressure.</figcaption></figure>
</div>
<div class="prose narrow" style="margin-top:2.5rem">
<h2>How a result like this happens</h2>
<p>The furnace is sealed and the system placed under negative pressure, so the vacuum is pulling the whole time. Each run is agitated with rotating brushes and compressed air to break debris loose, and the vacuum carries it out of the house. Every register and grill is removed and washed by hand. Nothing is sprayed over dirt to hide it.</p>
<p>Nick photographs the inside of the system before and after on request, so you can see the same view you see here, in your own home.</p>
<p><a class="btn" href="tel:{TEL}">Call or text {PHONE} for a free inspection</a></p>
</div>
</div></section>
"""
urls.append(render("gallery.html","Air Duct Cleaning Before & After Photos – Madison WI | Ducts On Call",
  "Real before and after photos from a Madison, Wisconsin air duct cleaning by NADCA-certified Ducts On Call: a return duct caked in dust, then bare clean metal after negative-pressure cleaning.",
  gal_body, [business_ld(), {"@type":"ImageGallery","name":"Air duct cleaning before and after, Madison WI","image":[BASE+"assets/job-01-before.jpg",BASE+"assets/job-01-after.jpg"]}]))

# ---------- Commercial ----------
com_body = f"""
<section class="page-head"><div class="wrap grid">
  <div><p class="eyebrow">Commercial &amp; industrial · Madison, WI</p><h1>Commercial duct cleaning for offices, rentals and facilities.</h1>
  <p class="lede">Ducts On Call is listed with NADCA for both residential and commercial work. Rental turnovers, offices, daycares, clinics, restaurants and light industrial, scheduled around your hours.</p>
  <div class="actions"><a class="btn big" href="tel:{TEL}">Call or text {PHONE}</a></div></div>
  <figure class="hero-img"><img src="./assets/process-vacuum.jpg" alt="Technician connecting a large vacuum hose to a duct opening" width="1024" height="768"></figure>
</div></section>
<section class="block"><div class="wrap narrow prose">
<h2>Who we work with</h2>
<ul><li><strong>Property managers and landlords:</strong> duct and dryer vent cleaning at turnover, portfolio scheduling, written documentation for files.</li>
<li><strong>Offices and clinics:</strong> after-hours cleaning of supply and return systems, HEPA filtration of occupied air, minimal disruption.</li>
<li><strong>Restaurants and commercial kitchens:</strong> kitchen exhaust hood and duct cleaning to reduce grease fire risk.</li>
<li><strong>Daycares, schools and churches:</strong> air quality assessments and cleaning where sensitive occupants are a concern.</li>
<li><strong>Light industrial:</strong> dust-laden systems in shops and warehouses.</li></ul>
<h2>Standards we work to</h2>
<p>NADCA's ACR Standard for Assessment, Cleaning and Restoration of HVAC systems defines what a proper cleaning includes: source removal under negative pressure, access to every component, and verification afterward. Nick is a NADCA-certified Air Systems Cleaning Specialist, and Ducts On Call has been a NADCA member since 2022.</p>
<h2>Documentation</h2>
<p>Before-and-after photos, a written scope of what was cleaned, and indoor air quality or mycotoxin test results where testing was performed. Useful for tenant files, insurance and compliance.</p>
<h2>Getting a quote</h2>
<p>Commercial work is quoted after a walkthrough. Send square footage, number of air handlers and any known issues to <a href="mailto:ductsoncall@gmail.com">ductsoncall@gmail.com</a>, or call or text <a href="tel:{TEL}">{PHONE}</a>.</p>
</div></section>
"""
urls.append(render("commercial.html","Commercial Duct Cleaning Madison WI – Offices, Rentals, Restaurants | Ducts On Call",
  "NADCA-listed commercial and industrial air duct cleaning in Madison, Wisconsin: offices, rental turnovers, daycares, clinics, restaurant hood cleaning. After-hours scheduling, HEPA filtration, documentation. Call (608) 906-1008.",
  com_body, [business_ld(), {"@type":"Service","name":"Commercial duct cleaning","serviceType":"Commercial HVAC duct cleaning","provider":{"@id":BASE+"#business"},"areaServed":{"@type":"AdministrativeArea","name":"Dane County and Columbia County, Wisconsin"},"url":BASE+"commercial.html"}], current="com"))

# ---------- Guides ----------
GUIDES = [
 dict(slug="air-duct-cleaning-cost-madison", title="What Does Air Duct Cleaning Cost in Madison, WI? (2026)", h1="What air duct cleaning costs in Madison, and what drives the price",
  desc="Air duct cleaning cost in Madison, Wisconsin explained: realistic ranges, what changes the price, why the $99 whole-house special is a bait-and-switch, and how Ducts On Call quotes.",
  body="""
<p class="lede">The honest answer is that a proper whole-system cleaning of an average Madison home is a several-hundred-dollar job, and anything advertised for $99 is not a whole-system cleaning.</p>
<h2>What a real cleaning involves</h2>
<p>A complete cleaning means the furnace and every supply and return run are placed under negative pressure, agitated, and vacuumed out; every register and grill is removed and washed; and the blower compartment and plenums are cleaned. That takes a properly equipped crew several hours. Per-vent pricing, add-ons for the furnace or AC coil, and a dryer vent are the usual components of a quote.</p>
<h2>What moves the price</h2>
<ul><li><strong>Number of vents and returns.</strong> A 1,200 sq ft ranch and a 3,000 sq ft two-story with two zones are different jobs.</li>
<li><strong>Furnace and coil.</strong> Cleaning the blower and the evaporator coil adds time but is where a lot of the dust actually sits.</li>
<li><strong>Condition.</strong> Post-renovation drywall dust, pet hair, or a previously uncleaned 40-year-old system take longer.</li>
<li><strong>Access.</strong> Finished basements and tight mechanical rooms slow the work.</li>
<li><strong>Add-ons.</strong> Odor elimination, bio-growth treatment, and dryer vent cleaning.</li></ul>
<h2>The $99 special</h2>
<p>Low advertised prices are a lead-generation tactic. The crew arrives, finds "mold" or "problems" and the price multiplies, or they vacuum at the registers for 30 minutes and leave the trunk lines untouched. The EPA warns homeowners about companies that make sweeping claims about health benefits or recommend duct cleaning as a routine part of maintenance, and NADCA explicitly advises against blow-and-go pricing.</p>
<h2>How Ducts On Call quotes</h2>
<p>Dryer vent cleaning is a flat $175. Air duct cleaning is quoted per system after a free inspection, so you see the number before anything starts, and if the ducts don't need cleaning, Nick says so and leaves. No per-vent surprises on the day.</p>
<p><a class="btn" href="tel:{TEL}">Call or text {PHONE} for a quote</a></p>
"""),
 dict(slug="signs-air-ducts-need-cleaning", title="7 Signs Your Air Ducts Need Cleaning (and 3 That Don't Mean What You Think)", h1="7 signs your air ducts need cleaning, and 3 that are commonly misread",
  desc="Do your air ducts need cleaning? Seven real indicators based on EPA and NADCA guidance, three false alarms, and what to do next. From NADCA-certified Ducts On Call, Madison WI.",
  body="""
<p class="lede">The EPA's position is simple: clean ducts when there is visible mold, vermin, or excessive debris being released into the home. Here is what that looks like in a real house.</p>
<h2>Seven real signs</h2>
<ol><li><strong>Visible dust blowing from registers</strong> when the system starts, or dust streaks on the wall or ceiling around supply vents.</li>
<li><strong>Visible mold growth</strong> on the inside of hard-surface ducts or on the furnace, coil or plenum. Confirm with a lab if unsure; many things look like mold.</li>
<li><strong>Evidence of rodents or insects</strong>: droppings, nesting material or odor from vents.</li>
<li><strong>A recent renovation</strong> that produced drywall or sawdust while the system was running.</li>
<li><strong>A musty or burning-dust smell</strong> every time the furnace runs, especially after summer.</li>
<li><strong>You just bought the home</strong> and have no record of the system ever being cleaned. Pull a register and look.</li>
<li><strong>Filters load up unusually fast</strong>, which points to a dirty return side feeding the filter.</li></ol>
<h2>Three false alarms</h2>
<ul><li><strong>"It's been X years."</strong> Time alone is not a reason. Inspect, then decide.</li>
<li><strong>Allergy symptoms.</strong> The EPA has not found that duct cleaning prevents health problems. Dirty ducts can be a factor, but so can humidity, carpet, pets and the filter you're using. Test before you clean.</li>
<li><strong>A phone or door-to-door offer.</strong> An unsolicited "special" is a sales tactic, not a sign your ducts are dirty.</li></ul>
<h2>What to do next</h2>
<p>Pull one supply register and one return grill and look with a flashlight. If what you see matches the list above, book an inspection. Ducts On Call inspects for free and will tell you if cleaning is not warranted.</p>
<p><a class="btn" href="tel:{TEL}">Call or text {PHONE}</a></p>
"""),
 dict(slug="dryer-vent-fire-safety", title="Dryer Vent Fire Safety: What Wisconsin Homeowners Should Check", h1="Dryer vent fire safety: the five-minute check every homeowner should do",
  desc="Lint is the leading factor in residential clothes dryer fires. A five-minute dryer vent check, warning signs, and when to get the vent professionally cleaned. Ducts On Call, Madison WI, $175 flat.",
  body="""
<p class="lede">The U.S. Fire Administration reports that failure to clean is the leading factor contributing to clothes dryer fires in residential buildings. The fix is cheap and fast.</p>
<h2>Why dryer vents catch fire</h2>
<p>Lint is fine, dry and highly flammable. The dryer's lint screen catches most of it, but a steady stream passes through into the vent. Over months it packs the duct, airflow drops, the dryer runs hotter and longer, and the heating element can ignite the lint. Long runs, multiple elbows, foil or plastic flexible duct, and vents that exit through the roof are the highest risk.</p>
<h2>The five-minute check</h2>
<ol><li><strong>Dry time.</strong> If a normal load needs more than one cycle, airflow is restricted.</li>
<li><strong>Heat.</strong> Is the top of the dryer or the laundry room noticeably hot during a cycle?</li>
<li><strong>Exterior hood.</strong> Run the dryer and go outside. You should feel strong airflow and the flap should open fully. Lint around the hood is a bad sign.</li>
<li><strong>Behind the dryer.</strong> Pull it out. Is the transition duct crushed, kinked, or made of white plastic or thin foil? Replace with rigid or semi-rigid metal.</li>
<li><strong>Smell.</strong> A burning smell during a cycle means stop and investigate.</li></ol>
<h2>When to call</h2>
<p>If any check fails, or if the vent has never been cleaned, book a professional cleaning. Ducts On Call cleans the full run from the dryer to the exterior hood for a flat $175, checks the transition duct, and confirms airflow at the exit. Yearly is the right interval for most Wisconsin homes.</p>
<p><a class="btn" href="../dryer-vent-cleaning.html">Dryer vent cleaning details</a> <a class="btn ghost" href="tel:{TEL}">Call or text {PHONE}</a></p>
"""),
 dict(slug="duct-cleaning-after-renovation-or-moving-in", title="Should You Clean the Ducts After a Renovation or When You Buy a Home?", h1="Duct cleaning after a renovation or when you move in: what to check",
  desc="Two situations where duct cleaning is usually worth it: after construction dust and when buying a home with an unknown history. What to inspect and when to skip it. Ducts On Call, Madison WI.",
  body="""
<p class="lede">Most of the time, a duct system does not need cleaning on a schedule. Two situations are the exception more often than not.</p>
<h2>After a renovation</h2>
<p>Drywall sanding, demolition and flooring work put a very fine mineral dust into the air. If the furnace or air conditioner was running during the work, that dust was pulled into the returns and distributed through every supply run. It settles slowly and keeps re-entering the air for months. The tell is a chalky film on the inside of registers and a dusty smell on the first cold day.</p>
<p>The cheapest protection is prevention: turn the system off during dusty work and seal the returns. If that didn't happen, a cleaning after the project closes is usually justified, and the furnace filter should be replaced immediately.</p>
<h2>When you buy a home</h2>
<p>You rarely know whether the previous owners had pets, smoked, renovated, or had water damage. Before you move furniture in is the easiest time to clean, because the house is empty and the registers are accessible. Pull two or three registers and a return grill and look with a flashlight. Debris, pet hair, or a musty odor from the returns is a reason to clean; bare metal is a reason not to.</p>
<h2>Water damage changes the question</h2>
<p>A finished basement that flooded, a slow leak near the furnace, or an air conditioner that drained poorly can seed growth in the return side and the coil. Here testing comes first: it is cheap to find out whether there is biological growth before deciding how to treat it. The EPA notes that cleaning alone does not fix a moisture problem; the source has to be corrected.</p>
<p><a class="btn" href="tel:{TEL}">Call or text {PHONE} for a free inspection</a></p>
"""),
 dict(slug="mold-in-air-ducts", title="Mold in Air Ducts: What It Means and What Actually Works", h1="Mold in air ducts: what it means, what testing shows, and what actually works",
  desc="Is there mold in your air ducts? How to tell, when to test, why spraying biocide over dirt doesn't work, and the EPA-backed approach. By Nick Bellino, author of Molds and Mycotoxins in Air Ducts.",
  body="""
<p class="lede">Mold in a duct system is a moisture story first. Finding it is a reason to look for water, not just a reason to clean.</p>
<h2>Where it grows</h2>
<p>Sheet metal ducts are a poor surface for mold unless they are dirty and damp. The usual locations are the air conditioner's evaporator coil and drain pan, the plenum directly after it, insulated or lined ducts that have gotten wet, and returns in damp basements. Dust is the food; condensation or a leak is the water.</p>
<h2>How to tell</h2>
<p>Discoloration alone proves little; many deposits look like mold. The EPA suggests having a sample analyzed by a laboratory if you are unsure. Indoor air and surface sampling can also tell you whether spore levels indoors differ from outdoors, and mycotoxin testing adds another layer where sensitive occupants are involved. Nick tests and reports what the results show; he does not diagnose health conditions.</p>
<h2>What does not work</h2>
<p>Spraying a biocide or sealant over dirty ductwork. The EPA notes that no chemical biocides are registered for use in bare sheet metal ducts, and sealants applied over debris trap it rather than remove it. If the moisture source is not fixed, growth comes back.</p>
<h2>What does</h2>
<ol><li>Fix the water: coil drainage, insulation, humidity, leaks.</li>
<li>Mechanically remove the debris under negative pressure, so the food source is gone.</li>
<li>Clean the coil, pan and blower.</li>
<li>Where growth was confirmed, a bio-growth treatment appropriate for the surface.</li>
<li>Re-test if the stakes warrant it.</li></ol>
<p>Nick Bellino wrote a book on exactly this: <a href="https://a.co/d/d6XJZ6S" target="_blank" rel="noopener noreferrer">Molds and Mycotoxins in Air Ducts: The Hidden Dangers</a> (2025).</p>
<p><a class="btn" href="../indoor-air-quality.html">Indoor air quality testing</a> <a class="btn ghost" href="tel:{TEL}">Call or text {PHONE}</a></p>
"""),
]
for g in GUIDES:
    body = f"""
<section class="page-head"><div class="wrap narrow"><p class="eyebrow">Homeowner guide</p><h1>{g['h1']}</h1>
<p class="small muted">By <a href="https://ductsoncall-hub.github.io/nick-bellino/" target="_blank" rel="noopener noreferrer">Nick Bellino</a>, NADCA ASCS · Ducts On Call, Madison WI · Updated {TODAY}</p></div></section>
<section class="block"><div class="wrap narrow prose">{g['body'].replace('{TEL}',TEL).replace('{PHONE}',PHONE)}
<hr style="border:0;border-top:1px solid var(--line);margin:2.5rem 0">
<p class="small muted">Sources: U.S. EPA, <a href="https://www.epa.gov/indoor-air-quality-iaq/should-you-have-air-ducts-your-home-cleaned" target="_blank" rel="noopener noreferrer">Should You Have the Air Ducts in Your Home Cleaned?</a> · NADCA, <a href="https://nadca.com/homeowners" target="_blank" rel="noopener noreferrer">Homeowner resources</a> · U.S. Fire Administration, <a href="https://www.usfa.fema.gov/prevention/home-fires/prevent-fires/appliances/clothes-dryers/" target="_blank" rel="noopener noreferrer">Clothes dryer fire safety</a>.</p>
<p class="small"><a href="./index.html">← All guides</a></p>
</div></section>
"""
    ld = [business_ld(), {"@type":"Article","headline":g['title'],"description":g['desc'],"author":{"@type":"Person","name":"Nick Bellino","url":"https://ductsoncall-hub.github.io/nick-bellino/"},"publisher":{"@id":BASE+"#business"},"datePublished":TODAY,"dateModified":TODAY,"image":BASE+"assets/og-ductsoncall.jpg","mainEntityOfPage":BASE+f"guides/{g['slug']}.html"},
          {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":"Guides","item":BASE+"guides/index.html"},{"@type":"ListItem","position":3,"name":g['title'],"item":BASE+f"guides/{g['slug']}.html"}]}]
    urls.append(render(f"guides/{g['slug']}.html", g['title']+" | Ducts On Call", g['desc'], body, ld, current="guides", sub=True))

gi_body = f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Homeowner guides</p><h1>Read before you book anyone, including us.</h1>
<p class="lede">Plain-English guides written by Nick Bellino, NADCA-certified Air Systems Cleaning Specialist and author of five books on indoor air. Sourced to the EPA, NADCA and the U.S. Fire Administration.</p></div></section>
<section class="block"><div class="wrap"><div class="cards three">
{"".join(f'<a class="card" href="./{g["slug"]}.html"><h3>{g["title"]}</h3><p>{g["desc"]}</p><span class="more">Read →</span></a>' for g in GUIDES)}
</div>
<p class="note" style="margin-top:2.5rem">Want the deeper science? Nick's blog, <a href="https://ductsoncall-hub.github.io/" target="_blank" rel="noopener noreferrer">Indoor Air Science Notes</a>, has cited articles on mold, mycotoxins, particulate matter and healthy homes.</p>
</div></section>
"""
urls.append(render("guides/index.html","Homeowner Guides – Air Duct & Dryer Vent Cleaning, Madison WI | Ducts On Call",
  "Honest homeowner guides from NADCA-certified Ducts On Call, Madison WI: duct cleaning cost, signs ducts need cleaning, dryer vent fire safety, post-renovation cleaning, mold in ducts.",
  gi_body, [business_ld(), {"@type":"CollectionPage","name":"Homeowner guides","url":BASE+"guides/index.html"}], current="guides", sub=True))

# ---------- llms.txt ----------
open(os.path.join(OUT,"llms.txt"),"w").write(f"""# Ducts On Call Inc.

> NADCA-certified air duct cleaning, dryer vent cleaning and indoor air quality testing in Madison, Wisconsin and surrounding Dane and Columbia County communities. Owner-operated by Nick Bellino, NADCA ASCS, author of five books on mold and indoor air. Free inspections. Dryer vent cleaning $175 flat; duct cleaning quoted per system.

Phone: (608) 906-1008 (call or text, 7 AM–7 PM) · Email: ductsoncall@gmail.com · Address: N3303 County Highway J, Poynette, WI 53955 · Main site: https://ductsoncall.com

## Services
- [Air duct cleaning]({BASE}air-duct-cleaning.html)
- [Dryer vent cleaning]({BASE}dryer-vent-cleaning.html)
- [Indoor air quality & mycotoxin testing]({BASE}indoor-air-quality.html)
- [Commercial & industrial]({BASE}commercial.html)

## Service area
{chr(10).join(f"- [{n}, WI]({BASE}areas/{s}.html)" for s,n,*_ in CITIES)}

## Guides
{chr(10).join(f"- [{g['title']}]({BASE}guides/{g['slug']}.html)" for g in GUIDES)}

## Proof
- [Reviews]({BASE}reviews.html) · [Before & after]({BASE}gallery.html) · [FAQ]({BASE}faq.html)
- NADCA listing: https://nadca.com/find-a-professional/ducts-call · BBB: https://www.bbb.org/us/wi/poynette/profile/duct-cleaning/ducts-on-call-inc-0694-1000030177
- About the owner: https://ductsoncall-hub.github.io/nick-bellino/
""")


# ---------- Thank you ----------
thanks_body = f"""
<section class="page-head"><div class="wrap narrow"><p class="eyebrow">Request received</p><h1>Thanks. Nick has your request.</h1>
<p class="lede">He answers personally, usually the same day during business hours (7 AM to 7 PM). If it is urgent, call or text <a href="tel:{TEL}">{PHONE}</a> now.</p>
<p>While you wait, two guides most homeowners find useful:</p>
<div class="cards two">
  <a class="card" href="./guides/signs-air-ducts-need-cleaning.html"><h3>7 signs your air ducts need cleaning</h3><p>And three that are commonly misread.</p><span class="more">Read →</span></a>
  <a class="card" href="./guides/air-duct-cleaning-cost-madison.html"><h3>What air duct cleaning costs in Madison</h3><p>Realistic ranges and the $99 special trap.</p><span class="more">Read →</span></a>
</div>
<p style="margin-top:2rem"><a class="btn ghost" href="./index.html">Back to home</a></p>
</div></section>
"""
render("thanks.html","Request received | Ducts On Call", "Your free inspection request has been received. Nick Bellino replies personally, usually the same day.", thanks_body, [business_ld()])

# ---------- sitemap / robots ----------
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
tp=os.path.join(OUT,'thanks.html'); t=open(tp).read().replace('<meta name="viewport"','<meta name="robots" content="noindex"><meta name="viewport"',1); open(tp,'w').write(t)
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
open(os.path.join(OUT,".nojekyll"),"w").write("")
print(f"built {len(urls)} pages")
