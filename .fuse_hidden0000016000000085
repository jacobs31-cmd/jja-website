#!/usr/bin/env python3
"""Generator for city/local landing pages (modeled on the Clarkston template).
Each page lives at /<slug>/ , relative path '../'. Writes the page, then wire() adds
sitemap entries and updates the llms.txt local-pages section.
  python gen_cities.py generate [force]
  python gen_cities.py wire
"""
import os, sys, json

def safe_write(path, text):
    """Flush-and-verify file write — guards against the silent mid-file truncation
    that left page footers cut off. Unlike open(path,'w').write(...), this always
    closes the handle, then re-reads the file and aborts loudly if the on-disk
    content does not match, so a truncated page can never be written or deployed again."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("ABORT: short/truncated write to " + path)
SITE="https://jjainsurance.com"; PHONE_TEL="+12486936455"; PHONE="(248) 693-6455"; EMAIL="Support@jjainsurance.com"
VER="20260702"; REL="../"
FORCE=(len(sys.argv)>2 and sys.argv[2]=="force")

CONFIG=[
{"slug":"rochester-hills-insurance","name":"Rochester Hills","county":"Oakland County","geo":[42.658,-83.150],
 "title":"Rochester Hills Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Rochester Hills, MI. We shop 35+ carriers for auto, home, life, and business coverage across Oakland County.",
 "ogdesc":"Independent insurance agent serving Rochester Hills, MI families and businesses. We shop 35+ carriers for the best auto, home, life, and commercial coverage.",
 "areas":[("City","Rochester Hills, Michigan"),("City","Rochester, Michigan"),("AdministrativeArea","Oakland Township, Michigan"),("City","Auburn Hills, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Rochester Hills since 1981",
 "h1":"Rochester Hills insurance — local, independent, and shopped across 35+ carriers",
 "lead":"We're a family-owned independent agency a short drive up the road in Lake Orion. For more than 40 years we've shopped 35+ carriers for Rochester Hills families and business owners — from the neighborhoods off Tienken and Adams to the homes near the Clinton River and Stony Creek — finding the best mix of price, coverage, and service.",
 "cover_intro":"Whether you're near Oakland University, along the Clinton River, or out toward Stony Creek Metropark, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"Stony Creek Lake, the Clinton River, Clear Spring Lake, and Emerald Lake — plus the boats, jet skis, and ATVs Rochester Hills families trailer up north",
 "biz_intro":"Rochester Hills has a deep base of professional offices, medical and dental practices, and contractors. We write commercial insurance through 20+ markets:",
 "serve":[("Rochester Hills","48306, 48307, 48309"),("Rochester",""),("Oakland Township",""),("Auburn Hills",""),("Troy",""),("Shelby Township","")],
 "faq_local_q":"Do you serve all of Rochester Hills and the surrounding area?",
 "faq_local_a":"Yes — from our Lake Orion office we cover all of Rochester Hills (48306, 48307, 48309) plus Rochester, Oakland Township, Auburn Hills, Troy, and Shelby Township just across the Macomb County line. Most of our work is done by phone, email, and online, so you never have to come in."},

{"slug":"auburn-hills-insurance","name":"Auburn Hills","county":"Oakland County","geo":[42.687,-83.234],
 "title":"Auburn Hills Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Auburn Hills, MI. Personal and commercial coverage shopped across 35+ carriers — homes, autos, and the businesses that power Oakland County.",
 "ogdesc":"Independent insurance agent serving Auburn Hills, MI families and businesses. We shop 35+ carriers for auto, home, life, and commercial coverage.",
 "areas":[("City","Auburn Hills, Michigan"),("City","Rochester Hills, Michigan"),("City","Pontiac, Michigan"),("AdministrativeArea","Orion Township, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Auburn Hills since 1981",
 "h1":"Auburn Hills insurance for families — and the businesses that power Oakland County",
 "lead":"Our office is about ten minutes north in Lake Orion, and we've insured Auburn Hills families and companies for over 40 years. From the neighborhoods near Oakland University to the corporate corridor along I-75, we shop 35+ carriers to find the right coverage at the right price.",
 "cover_intro":"Whether you live near Oakland University, off Squirrel Road, or along the Clinton River downtown, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"the Clinton River and the lakes around neighboring Lake Angelus and Pontiac, plus boats, motorcycles, and ATVs",
 "biz_intro":"Auburn Hills is one of Michigan's busiest commercial hubs — home to Stellantis North America, Oakland University, BorgWarner, Great Lakes Crossing, and 80+ international companies, plus the contractors, restaurants, and service firms that support them. We write commercial insurance through 20+ markets:",
 "serve":[("Auburn Hills","48326"),("Rochester Hills",""),("Pontiac",""),("Lake Orion / Orion Township",""),("Bloomfield",""),("Lake Angelus","")],
 "faq_local_q":"Do you write commercial insurance for Auburn Hills businesses?",
 "faq_local_a":"Absolutely — it's one of our specialties. Auburn Hills is a major business center, and we write general liability, commercial property, commercial auto, workers compensation, BOP, professional liability, cyber, and specialty programs through 20+ commercial carriers. From a startup near Oakland University to an established firm in the I-75 corridor, we shop the market to fit your operation."},

{"slug":"waterford-insurance","name":"Waterford","county":"Oakland County","geo":[42.660,-83.412],
 "title":"Waterford Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Waterford, MI. Lake-home, boat, auto, and business coverage shopped across 35+ carriers — built for Waterford's 30+ lakes.",
 "ogdesc":"Independent insurance agent serving Waterford, MI. Lake-home and boat specialists — we shop 35+ carriers for auto, home, watercraft, life, and commercial coverage.",
 "areas":[("AdministrativeArea","Waterford Township, Michigan"),("City","Pontiac, Michigan"),("City","Keego Harbor, Michigan"),("AdministrativeArea","White Lake, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Waterford since 1981",
 "h1":"Waterford insurance — lake homes, boats, and everything else, done locally",
 "lead":"With more than 30 lakes, Waterford is boat-and-lake-home country — and that's exactly the coverage most agencies underprice or miss. We're a family-owned independent agency that shops 35+ carriers for Waterford families and business owners, including the marine and lakefront markets your home and boat actually need.",
 "cover_intro":"Whether you're on Cass Lake, Elizabeth Lake, or anywhere across Waterford Township, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"Cass Lake, Elizabeth Lake, Sylvan Lake, Williams Lake, Loon Lake, Lotus Lake, and Pontiac Lake — with real hull and liability limits, not the token boat rider on a home policy",
 "biz_intro":"From marinas and lakeside restaurants to contractors and retail along Dixie and Highland, we write commercial insurance for Waterford businesses through 20+ markets:",
 "serve":[("Waterford","48327, 48328, 48329"),("Pontiac",""),("Keego Harbor",""),("Clarkston",""),("White Lake",""),("West Bloomfield","")],
 "faq_local_q":"Do you write boat and lake-home insurance for Waterford's lakes?",
 "faq_local_a":"Yes — it's a specialty here. We write boats, pontoons, and jet skis for Cass Lake, Elizabeth Lake, Sylvan Lake, Williams Lake, Loon Lake, Lotus Lake, Pontiac Lake, and the rest, with standalone marine policies that have real hull, liability, and medical limits. For lakefront homes we use carriers that properly value docks, seawalls, boathouses, and high replacement costs — coverage a standard policy often gets wrong."},

{"slug":"orion-township-insurance","name":"Orion Township","county":"Oakland County","geo":[42.784,-83.259],
 "title":"Orion Township & Lake Orion Insurance | J. Jacobs & Associates",
 "meta":"Your hometown independent insurance agency in Orion Township & Lake Orion, MI. We shop 35+ carriers for auto, home, lake-home, boat, life, and business coverage.",
 "ogdesc":"Hometown independent insurance agency in Orion Township and Lake Orion, MI. We shop 35+ carriers for auto, home, boat, life, and commercial coverage.",
 "areas":[("AdministrativeArea","Orion Township, Michigan"),("City","Lake Orion, Michigan"),("AdministrativeArea","Oakland Township, Michigan"),("City","Auburn Hills, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Right here at home since 1981",
 "h1":"Orion Township & Lake Orion insurance — from your hometown agency",
 "lead":"This is home. Our office sits on S. Baldwin Road in Orion Township, and we've insured our Lake Orion neighbors since 1981. When you call us, you're working with people who live here — who know Lake Orion, Bald Mountain, and the difference a 506-acre all-sports lake makes to your home and boat coverage.",
 "cover_intro":"Whether you're in the Village of Lake Orion, on the lake, or anywhere across Orion Township, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"Lake Orion (all-sports, 506 acres), Square Lake, and the surrounding waters — boats, pontoons, and jet skis with real hull and liability limits",
 "biz_intro":"From the shops in downtown Lake Orion to contractors and service businesses across Orion Township, we write commercial insurance through 20+ markets:",
 "serve":[("Lake Orion / Orion Township","48359, 48360, 48362"),("Oakland Township",""),("Auburn Hills",""),("Oxford",""),("Lake Angelus",""),("Independence Township","")],
 "faq_local_q":"You're actually located in Orion Township, right?",
 "faq_local_a":"Yes — our office is at 4301 S. Baldwin Rd, right here in Orion Township, and we've been family-owned and local since 1981. We're not a call center or a one-carrier branch office. When you call (248) 693-6455 you get a real person who lives and works in the community, knows Lake Orion's lakefront market, and can shop your coverage across 35+ carriers."},

{"slug":"troy-insurance","name":"Troy","county":"Oakland County","geo":[42.580,-83.143],
 "title":"Troy Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Troy, MI. We shop 35+ carriers for auto, home, life, and commercial coverage across one of Michigan's busiest suburbs.",
 "ogdesc":"Independent insurance agent serving Troy, MI families and businesses. We shop 35+ carriers for the best auto, home, life, and commercial coverage.",
 "areas":[("City","Troy, Michigan"),("City","Rochester Hills, Michigan"),("City","Birmingham, Michigan"),("City","Sterling Heights, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Troy since 1981",
 "h1":"Troy insurance — independent coverage for one of Michigan's busiest suburbs",
 "lead":"Troy is a corporate and retail powerhouse with some of Oakland County's most desirable neighborhoods — and plenty of competition for your insurance dollar. As a family-owned independent agency, we shop 35+ carriers so Troy families and businesses get the best combination of price and coverage, not one company's quote.",
 "cover_intro":"From the neighborhoods near Big Beaver and Long Lake to the homes by the Troy schools, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"the boats, motorcycles, and collector cars Troy households store and trailer to the lakes up north",
 "biz_intro":"Troy is home to Somerset Collection, countless corporate headquarters, medical and professional offices, tech and finance firms, and the contractors who serve them. We write commercial insurance through 20+ markets:",
 "serve":[("Troy","48083, 48084, 48085, 48098"),("Rochester Hills",""),("Birmingham",""),("Bloomfield",""),("Sterling Heights",""),("Clawson","")],
 "faq_local_q":"Why use an independent agent in a city with so many insurance offices?",
 "faq_local_a":"Because most of those offices are captive — they only sell one company's products (State Farm, Allstate, Farmers). We represent 35+ carriers, so instead of one quote you get the best of the whole market, and we re-shop your coverage every renewal. In a competitive market like Troy, that's how you actually keep your rate down year after year."},

{"slug":"bloomfield-insurance","name":"Bloomfield","county":"Oakland County","geo":[42.583,-83.245],
 "title":"Bloomfield Insurance Agent | High-Value Home & HNW | J. Jacobs",
 "meta":"Independent insurance agent for Bloomfield Hills & Bloomfield Township, MI. High-value home, valuables, auto, and high-net-worth coverage through Chubb, PURE, and 35+ carriers.",
 "ogdesc":"Independent insurance agent serving Bloomfield Hills and Bloomfield Township, MI. High-value home and high-net-worth specialists across 35+ carriers.",
 "areas":[("AdministrativeArea","Bloomfield Township, Michigan"),("City","Bloomfield Hills, Michigan"),("City","Birmingham, Michigan"),("AdministrativeArea","West Bloomfield, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Bloomfield since 1981",
 "h1":"Bloomfield insurance — high-value homes, valuables, and the coverage they deserve",
 "lead":"Bloomfield Hills and Bloomfield Township are among Michigan's most prestigious communities — and significant homes, collections, and assets need more than a standard policy. We place coverage through high-net-worth specialists like Chubb, PURE, and Cincinnati Private Client, plus 35+ standard carriers, so Bloomfield families get broader coverage, higher limits, and concierge claim service.",
 "cover_intro":"From the estates near Cranbrook to the lake homes off Lone Pine and Long Lake, we write personal coverage built for higher-value households:",
 "rec":"Wing Lake, Forest Lake, Island Lake, Gilbert Lake, and Lower Long Lake — with agreed-value coverage on boats and collector cars",
 "biz_intro":"For Bloomfield's professional practices, family offices, and business owners, we write commercial insurance through 20+ markets:",
 "serve":[("Bloomfield Hills & Township","48301, 48302, 48304"),("Birmingham",""),("West Bloomfield",""),("Troy",""),("Auburn Hills",""),("Pontiac","")],
 "faq_local_q":"Do you handle high-value and high-net-worth coverage in Bloomfield?",
 "faq_local_a":"Yes — it's a core part of what we do here. For homes valued at $750K and up, significant jewelry, art, or wine collections, and families with substantial assets, we place coverage through high-net-worth carriers (Chubb, PURE, Cincinnati Private Client) that offer guaranteed replacement cost, agreed value on valuables, very high liability and umbrella limits, and concierge claims. See our <a href=\"../business/\">commercial</a> and high-net-worth coverage, or just call and we'll review what you have."},

{"slug":"pontiac-insurance","name":"Pontiac","county":"Oakland County","geo":[42.638,-83.291],
 "title":"Pontiac Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Pontiac, MI. We shop 35+ carriers for auto, home, life, and business coverage in the heart of Oakland County.",
 "ogdesc":"Independent insurance agent serving Pontiac, MI families and businesses. We shop 35+ carriers for auto, home, life, and commercial coverage.",
 "areas":[("City","Pontiac, Michigan"),("City","Auburn Hills, Michigan"),("AdministrativeArea","Waterford, Michigan"),("AdministrativeArea","Bloomfield Township, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Pontiac since 1981",
 "h1":"Pontiac insurance — independent coverage for the heart of Oakland County",
 "lead":"As the Oakland County seat, Pontiac is a community on the rise — and whether you own a home, rent, drive for work, or run a business here, you deserve an agent who shops the whole market for you. We're a family-owned independent agency that compares 35+ carriers to find Pontiac residents the best combination of price and coverage.",
 "cover_intro":"From the historic neighborhoods downtown to the homes near Sylvan Lake and the Clinton River, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"the Clinton River, nearby Sylvan Lake, and the boats and motorcycles Pontiac-area riders enjoy",
 "biz_intro":"From small businesses and contractors to the firms revitalizing downtown and the M1 Concourse corridor, we write commercial insurance for Pontiac through 20+ markets:",
 "serve":[("Pontiac","48340, 48341, 48342"),("Auburn Hills",""),("Waterford",""),("Bloomfield",""),("Sylvan Lake",""),("Keego Harbor","")],
 "faq_local_q":"Do you write renters and affordable auto coverage for Pontiac?",
 "faq_local_a":"Yes. We write renters insurance (often $15–$20 a month) and shop Michigan No-Fault auto across many carriers to find Pontiac drivers the most competitive rate for the coverage they need. Because we're independent, we can compare standard and non-standard markets in one place — useful for finding affordable coverage that still protects you."},

{"slug":"holly-insurance","name":"Holly","county":"Oakland County","geo":[42.793,-83.625],
 "title":"Holly Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Holly, MI. We shop 35+ carriers for auto, home, boat, life, and business coverage — small-town service from a local agency.",
 "ogdesc":"Independent insurance agent serving Holly, MI families and businesses. We shop 35+ carriers for auto, home, boat, life, and commercial coverage.",
 "areas":[("Place","Holly, Michigan"),("AdministrativeArea","Holly Township, Michigan"),("City","Fenton, Michigan"),("AdministrativeArea","Springfield Township, Michigan"),("AdministrativeArea","Oakland County, Michigan")],
 "eyebrow":"Serving Holly since 1981",
 "h1":"Holly insurance — small-town service from a local independent agency",
 "lead":"Holly has the kind of historic, close-knit, small-town character that deserves an agent who treats you like a neighbor, not a policy number. We're a family-owned independent agency in nearby Lake Orion that shops 35+ carriers for Holly families and business owners — from the homes near Battle Alley to the lake properties in the Holly Recreation Area.",
 "cover_intro":"Whether you're in the Village of Holly, out toward Mt. Holly, or on one of the area lakes, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"Bush Lake, Bevins Lake, McGinnis Lake, and the Holly Recreation Area waters — plus boats, ATVs, and snowmobiles for the Mt. Holly crowd",
 "biz_intro":"From the shops and restaurants along Battle Alley to contractors and the businesses around the Michigan Renaissance Festival, we write commercial insurance for Holly through 20+ markets:",
 "serve":[("Holly","48442"),("Fenton",""),("Grand Blanc",""),("Davisburg",""),("Springfield Township",""),("Groveland Township","")],
 "faq_local_q":"Do you cover lake homes, boats, and recreational toys around Holly?",
 "faq_local_a":"Yes — Holly's recreation area and lakes mean lots of boats, ATVs, snowmobiles, and cabins, and we write all of it. We use marine and powersport specialists for watercraft and off-road vehicles, and we handle seasonal and specialty dwelling coverage for cabins and second homes. Whether it's a pontoon on Bush Lake or a sled headed to Mt. Holly, we'll get it covered."},

{"slug":"shelby-township-insurance","name":"Shelby Township","county":"Macomb County","geo":[42.670,-83.034],
 "title":"Shelby Township Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Shelby Township, MI (Macomb County). We shop 35+ carriers for auto, home, life, and business coverage.",
 "ogdesc":"Independent insurance agent serving Shelby Township, MI. We shop 35+ carriers for the best auto, home, life, and commercial coverage in Macomb County.",
 "areas":[("AdministrativeArea","Shelby Township, Michigan"),("City","Utica, Michigan"),("City","Rochester Hills, Michigan"),("AdministrativeArea","Washington Township, Michigan"),("AdministrativeArea","Macomb County, Michigan")],
 "eyebrow":"Serving Shelby Township since 1981",
 "h1":"Shelby Township insurance — independent coverage for western Macomb County",
 "lead":"Shelby Township is one of Macomb County's fastest-growing communities, and we've served Macomb-area clients for decades from our office just across the county line in Lake Orion. As a family-owned independent agency, we shop 35+ carriers so Shelby Township families and businesses get the best combination of price and coverage.",
 "cover_intro":"From the subdivisions near Stony Creek Metropark to the homes along the Clinton River, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"Stony Creek's waters and the Clinton River, plus the boats, ATVs, and motorcycles Shelby Township families enjoy",
 "biz_intro":"From retail and restaurants along Van Dyke and Hall Road to contractors and professional offices, we write commercial insurance for Shelby Township through 20+ markets:",
 "serve":[("Shelby Township","48315, 48316, 48317"),("Utica",""),("Rochester Hills",""),("Sterling Heights",""),("Washington Township",""),("Macomb Township","")],
 "faq_local_q":"Do you serve Macomb County and Shelby Township?",
 "faq_local_a":"Yes — we're licensed throughout Michigan and have served Macomb County clients for years. Shelby Township sits right across the Oakland–Macomb line from our service area, and most of our work is done by phone, email, and online, so being a few miles away makes no difference. You get the same 35+-carrier shopping and local service as our Oakland County clients."},

{"slug":"washington-township-insurance","name":"Washington Township","county":"Macomb County","geo":[42.738,-83.010],
 "title":"Washington Township Insurance Agent | J. Jacobs & Associates",
 "meta":"Independent insurance agent for Washington Township, MI (Macomb County). Home, acreage, auto, and business coverage shopped across 35+ carriers.",
 "ogdesc":"Independent insurance agent serving Washington Township and Romeo, MI. We shop 35+ carriers for auto, home, acreage, life, and commercial coverage.",
 "areas":[("AdministrativeArea","Washington Township, Michigan"),("Place","Romeo, Michigan"),("AdministrativeArea","Bruce Township, Michigan"),("AdministrativeArea","Shelby Township, Michigan"),("AdministrativeArea","Macomb County, Michigan")],
 "eyebrow":"Serving Washington Township since 1981",
 "h1":"Washington Township insurance — coverage for Macomb County's countryside",
 "lead":"With its rolling hills, vineyards, golf courses, and larger properties, Washington Township needs an agent who understands acreage, outbuildings, and semi-rural coverage — not a cookie-cutter city policy. We're a family-owned independent agency that shops 35+ carriers for Washington Township and Romeo-area families and businesses.",
 "cover_intro":"From the estates and acreage near Romeo to the newer subdivisions, we write the full lineup of personal insurance through 15+ personal-lines carriers:",
 "rec":"the boats, ATVs, and recreational vehicles common out here, plus coverage for barns, outbuildings, and hobby farms",
 "biz_intro":"From the wineries, orchards, and golf courses to contractors and Main Street businesses in Romeo, we write commercial insurance for Washington Township through 20+ markets:",
 "serve":[("Washington Township","48094, 48095"),("Romeo",""),("Bruce Township",""),("Shelby Township",""),("Ray Township",""),("Oakland Township","")],
 "faq_local_q":"Do you cover larger properties, acreage, and outbuildings out here?",
 "faq_local_a":"Yes — that's exactly where an independent agent helps. Washington Township has a lot of acreage, barns, pole buildings, and hobby farms that standard policies handle poorly. We use carriers that properly cover outbuildings, detached structures, and rural exposures, plus specialty dwelling coverage for second homes and seasonal properties. Tell us what's on the property and we'll match it to the right market."},
]

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def page(cfg):
    url=f"{SITE}/{cfg['slug']}/"; og=f"{SITE}/assets/img/og/{cfg['slug']}.jpg"; name=cfg['name']
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":f"{name} Insurance","item":url}]}
    biz={"@context":"https://schema.org","@type":"InsuranceAgency","@id":f"{url}#localbusiness",
        "parentOrganization":{"@id":f"{SITE}/#organization"},"name":f"J. Jacobs & Associates Insurance — {name}",
        "url":url,"telephone":"+1-248-693-6455","email":EMAIL,
        "address":{"@type":"PostalAddress","streetAddress":"4301 S. Baldwin Rd","addressLocality":"Lake Orion","addressRegion":"MI","postalCode":"48359","addressCountry":"US"},
        "areaServed":[{"@type":t,"name":n} for t,n in cfg['areas']],"priceRange":"$$",
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"}],
        "geo":{"@type":"GeoCoordinates","latitude":cfg['geo'][0],"longitude":cfg['geo'][1]}}
    faqs=[("Are you a local "+name+" insurance agent?","We're based in Lake Orion and have insured "+name+"-area families and businesses since 1981. We handle policies throughout "+cfg['county']+" and the surrounding communities — most of it by phone, email, and online, so you never have to come into an office."),
        ("What insurance do you write for "+name+" residents?","Personal lines: auto, home, condo, renters, life, umbrella, boat, motorcycle, RV, ATV, classic and collector car, flood, and pet. Commercial lines for "+name+"-area business owners: general liability, commercial property, commercial auto, workers compensation, BOP, professional liability, cyber, contractor coverage, and more."),
        (cfg['faq_local_q'],cfg['faq_local_a']),
        ("Can you bundle home and auto for a discount?","Almost always, yes. Multi-policy discounts typically range from 10% to 25% depending on the carrier. We compare bundled pricing across all 35+ of our markets and show you what each option looks like before you decide.")]
    faq_schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":esc_text(a)}} for q,a in faqs]}
    j=lambda o:json.dumps(o,ensure_ascii=False)
    serve_html="".join(f"<li>{esc(p)}{(' ('+z+')') if z else ''}</li>" for p,z in cfg['serve'])
    faq_html="".join(f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-body"><p>{a}</p></div></details>\n' for q,a in faqs)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(cfg['title'])}</title>
<meta name="description" content="{esc(cfg['meta'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#1a3a5c">
<link rel="icon" type="image/svg+xml" href="{REL}assets/img/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(cfg['title'])}">
<meta property="og:description" content="{esc(cfg['ogdesc'])}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="J. Jacobs & Associates">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(cfg['title'])}">
<meta name="twitter:description" content="{esc(cfg['ogdesc'])}">
<meta name="twitter:image" content="{og}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{REL}assets/css/styles.css?v={VER}">
<script type="application/ld+json">
{j(bc)}
</script>
<script type="application/ld+json">
{j(biz)}
</script>
<script type="application/ld+json">
{j(faq_schema)}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="utility-bar"><div class="container">
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg> 4301 S. Baldwin Rd, Lake Orion, MI 48359</span>
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z"/></svg> <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg> <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></div>
<header class="site-header"><div class="container">
    <a class="brand" href="{REL}" aria-label="J. Jacobs and Associates Insurance home"><img class="brand-logo-img" src="{REL}assets/img/logo.jpeg" alt="J. Jacobs and Associates Insurance"></a>
    <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary"><ul>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Our Agency</summary><ul class="submenu">
            <li><a href="{REL}about/">About Us</a></li><li><a href="{REL}team/">Our Team</a></li><li><a href="{REL}carriers/">Our Carriers</a></li><li><a href="{REL}reviews/">Reviews</a></li></ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Products</summary><ul class="submenu">
            <li><a href="{REL}personal/">Personal Insurance</a></li><li><a href="{REL}personal/auto-insurance/">Auto Insurance</a></li><li><a href="{REL}personal/home-insurance/">Home Insurance</a></li><li><a href="{REL}personal/life-insurance/">Life Insurance</a></li><li><a href="{REL}business/">Commercial Insurance</a></li><li><a href="{REL}business/workers-compensation/">Workers Compensation</a></li></ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Service</summary><ul class="submenu">
            <li><a href="{REL}service/">Service Center</a></li><li><a href="{REL}billing-claims/">Billing &amp; Claims</a></li></ul></details></li>
        <li><a href="{REL}blog/">Blog</a></li><li><a href="{REL}faq/">FAQ</a></li><li><a href="{REL}contact/">Contact</a></li>
      </ul></nav>
    <div class="header-cta"><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a><a class="btn btn-primary" href="{REL}quotes/">Start a Quote</a></div>
</div></header>
<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="{REL}">Home</a></li><li>{esc(name)} Insurance</li></ol></div></nav><main id="main">

<section class="section page-hero"><div class="container" style="max-width:880px;">
    <span class="eyebrow">{esc(cfg['eyebrow'])}</span>
    <h1>{esc(cfg['h1'])}</h1>
    <p class="lead">{esc(cfg['lead'])}</p>
    <div class="trust-band">
      <span class="trust-band-item"><span class="stars">★★★★★</span> 4.9 on Google</span>
      <span class="trust-band-item">Best of the Best &mdash; 8 years running <span class="sub">(2018&ndash;2025)</span></span>
      <span class="trust-band-item">35+ carriers shopped</span>
      <span class="trust-band-item">Family-owned since 1981</span>
    </div>
    <div style="margin-top:1.5rem; display:flex; gap:.75rem; flex-wrap:wrap;">
      <a class="btn btn-primary btn-lg" href="{REL}quotes/">Get a {esc(name)} Quote</a>
      <a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
</div></section>

<section class="section"><div class="container" style="max-width:880px;">
    <h2>What we cover for {esc(name)} families</h2>
    <p>{cfg['cover_intro']}</p>
    <ul>
      <li><strong><a href="{REL}personal/auto-insurance/">Auto insurance</a></strong> — Michigan No-Fault done right, with PIP options explained in plain language, multi-vehicle households, teen drivers, and the after-claim re-shop most agencies skip.</li>
      <li><strong><a href="{REL}personal/home-insurance/">Home insurance</a></strong> — we know local replacement-cost expectations and which carriers underwrite well in your ZIP code.</li>
      <li><strong>Boat, watercraft &amp; recreational</strong> — {cfg['rec']}.</li>
      <li><strong><a href="{REL}personal/life-insurance/">Life insurance</a></strong> — term, whole, and universal policies from $100K to $5M+.</li>
      <li><strong>Umbrella, condo, renters, flood, and pet</strong> — and anything else you need, shopped across our markets.</li>
    </ul>

    <h2 class="mt-2">For {esc(name)}-area business owners</h2>
    <p>{cfg['biz_intro']}</p>
    <ul>
      <li>General liability and commercial property</li>
      <li><a href="{REL}business/workers-compensation/">Workers compensation</a> — including audit support and Mod management</li>
      <li>Commercial auto for service vehicles and fleets</li>
      <li><a href="{REL}business/business-owners-policy/">Business owners policies (BOP)</a> for restaurants, retail, and professional offices</li>
      <li><a href="{REL}business/contractor-insurance/">Contractor coverage</a>, <a href="{REL}business/professional-liability-insurance/">professional liability</a>, and <a href="{REL}business/cyber-liability-insurance/">cyber</a></li>
      <li><a href="{REL}business/">See all 45+ commercial coverages →</a></li>
    </ul>

    <h2 class="mt-2">Why {esc(name)} residents choose an independent agent</h2>
    <p>Most local insurance offices represent only one carrier — State Farm, Allstate, Farmers. As an independent agency, we represent <strong>35+ carriers</strong> including Michigan-based companies like <a href="{REL}carriers/">Citizens, Frankenmuth, Wolverine Mutual, and Michigan Millers</a>, plus national A-rated names like The Hartford, Liberty Mutual, Hanover, Hagerty, and Hiscox.</p>
    <p>What that means for you: we shop your coverage every renewal. When a carrier raises rates or tightens underwriting, we have other markets to compare against — so most of our clients stay for decades because they don't have to call around themselves.</p>

    <h2>Areas we serve around {esc(name)}</h2>
    <p>From our office in Lake Orion we serve clients throughout {esc(name)} and the surrounding {esc(cfg['county'])} communities, including:</p>
    <ul>{serve_html}</ul>

    <h2>Common questions from {esc(name)} clients</h2>
    {faq_html}
    <div class="callout">
      <h2>Ready to compare {esc(name)} insurance quotes?</h2>
      <p>It takes 2 minutes for a quick quote. We'll shop your coverage across 35+ carriers and get back to you within one business day.</p>
      <a class="btn btn-primary btn-lg" href="{REL}quotes/">Start My Quote</a>
    </div>
    <p class="text-center" style="margin-top:1.5rem; color:var(--text-muted); font-size:.9rem;">Prefer to talk? Call us at <a href="tel:{PHONE_TEL}"><strong>{PHONE}</strong></a>, Monday-Friday 9am-5pm.</p>
</div></section>
</main>

<footer class="site-footer"><div class="container"><div class="footer-grid">
      <div class="footer-brand"><div class="footer-logo"><img src="{REL}assets/img/logo.jpeg" alt="J. Jacobs and Associates"></div>
        <h4>J. Jacobs &amp; Associates</h4>
        <p>Family-owned independent insurance agency serving Michigan since 1981. We shop 35+ carriers so you don&rsquo;t have to.</p>
        <p style="margin-top:1rem;"><strong style="color:#fff;">4301 S. Baldwin Rd</strong><br>Lake Orion, Michigan 48359<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div><h4>Insurance</h4><ul><li><a href="{REL}personal/">Personal Insurance</a></li><li><a href="{REL}personal/auto-insurance/">Auto Insurance</a></li><li><a href="{REL}personal/home-insurance/">Home Insurance</a></li><li><a href="{REL}personal/life-insurance/">Life Insurance</a></li><li><a href="{REL}business/">Commercial Insurance</a></li><li><a href="{REL}business/workers-compensation/">Workers Compensation</a></li></ul></div>
      <div><h4>Agency</h4><ul><li><a href="{REL}about/">About Us</a></li><li><a href="{REL}team/">Our Team</a></li><li><a href="{REL}carriers/">Our Carriers</a></li><li><a href="{REL}reviews/">Reviews</a></li><li><a href="{REL}service/">Service Center</a></li><li><a href="{REL}billing-claims/">Billing &amp; Claims</a></li><li><a href="{REL}faq/">FAQ</a></li></ul></div>
      <div><h4>Follow Us</h4><div class="social-row"><a href="https://www.facebook.com/JacobsandAssociates/" aria-label="Facebook" rel="noopener" target="_blank">f</a><a href="https://www.instagram.com/jjacobs_and_associates/" aria-label="Instagram" rel="noopener" target="_blank">IG</a><a href="https://www.linkedin.com/in/joe-jacobs-7a354422/" aria-label="LinkedIn" rel="noopener" target="_blank">in</a></div>
        <ul style="margin-top:1.25rem;"><li><a href="{REL}contact/">Contact Us</a></li><li><a href="{REL}privacy-policy/">Privacy Policy</a></li><li><a href="{REL}accessibility/">Accessibility</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span><span>Independent Insurance Agency · Lake Orion, Michigan</span></div>
</div></footer>
<script src="{REL}assets/js/site.v2.js?v={VER}" defer></script>
</body>
</html>
"""
def esc_text(s):
    # for JSON schema answer text: strip any HTML tags
    import re
    return re.sub('<[^>]+>','',s)
def generate():
    n=0
    for cfg in CONFIG:
        d=cfg['slug']; out=f"{d}/index.html"
        if os.path.exists(out) and not FORCE: continue
        os.makedirs(d,exist_ok=True)
        safe_write(out,page(cfg).rstrip("\x00")); n+=1
        print(f"  /{cfg['slug']}/  <- {cfg['name']}")
    print(f"Generated {n} city pages.")
def wire():
    sm="sitemap.xml"; t=open(sm,encoding="utf-8").read(); add=""
    for cfg in CONFIG:
        loc=f"{SITE}/{cfg['slug']}/"
        if loc in t: continue
        add+=f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    if add: safe_write(sm,t.replace("</urlset>",add+"</urlset>").rstrip("\x00")); print(f"  +{add.count('<url>')} sitemap")
    lt="llms.txt"; t=open(lt,encoding="utf-8").read()
    names=", ".join(c['name'] for c in CONFIG)
    old="Clarkston, Fenton, Ortonville, Oxford, Grand Blanc, Goodrich, Lapeer, Rochester, Oakland Township, and White Lake"
    if old in t and "Rochester Hills" not in t:
        t=t.replace(old, old+", "+names, 1); safe_write(lt,t.rstrip("\x00")); print("  +llms cities")
if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "generate"
    (generate if mode=="generate" else wire)()
