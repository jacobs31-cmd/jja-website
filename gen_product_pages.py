#!/usr/bin/env python3
"""
JJA — product/landing page generator.
Generates dedicated product pages (business/<slug>/ and personal/<slug>/) from a
config list, using the exact site template (utility bar, header, footer, breadcrumb +
FAQPage + Service schema, hero, trust band, CTA). Then wires each into the overview
page's matching definition block, sitemap.xml, and llms.txt.

  python gen_product_pages.py generate   # write the HTML pages (skips existing unless 'force')
  python gen_product_pages.py wire        # add "Full details" links + sitemap + llms entries
  python gen_product_pages.py generate force
"""
import os, re, sys, json

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

SITE="https://jjainsurance.com"
PHONE_TEL="+12486936455"; PHONE="(248) 693-6455"; EMAIL="Support@jjainsurance.com"
VER="20260702"
FORCE = (len(sys.argv)>2 and sys.argv[2]=="force")

# ---- per-product content -------------------------------------------------------
# section: business|personal ; def_id matches the scroll-to block on the overview page
CONFIG=[
# ===================== COMMERCIAL =====================
{"section":"business","slug":"general-liability-insurance","def_id":"general-liability",
 "eyebrow":"Commercial / General Liability","svc":"General Liability Insurance",
 "title":"Michigan General Liability Insurance",
 "meta":"General liability insurance for Michigan businesses. Covers third-party injury, property damage, and the lawsuits that come with them. Fast certificates, multi-carrier shopping.",
 "hero":"photo-1521791136064-7986c2920216","alt":"Michigan business owners shaking hands — general liability insurance",
 "lead":"General liability is the foundation policy nearly every Michigan business needs — and the one your clients, landlords, and contracts ask for first. It protects you when someone outside your business is injured or their property is damaged, and it pays to defend you even when the claim is groundless.",
 "whatwedo":[("Right-sized limits","most contracts and landlords require $1M per occurrence / $2M aggregate — we match your limits to what you actually need to sign."),
   ("Fast certificates of insurance","we turn around COIs and additional-insured endorsements quickly so a job or lease is never held up. Same-day is common."),
   ("Multi-carrier shopping","we shop your GL across our commercial markets to find the right price and form for your industry, not a single quote."),
   ("Coverage that fits your work","a consultant, a retailer, and a contractor face different exposures — we make sure your policy matches how you actually operate.")],
 "who_h":"Businesses we cover","who":"Retailers and shops, offices and professional services, contractors and trades, restaurants, manufacturers, wholesalers, fitness and personal care, nonprofits, and most other Michigan businesses. Many are eligible to bundle GL into a lower-cost Business Owners Policy (BOP).",
 "cov_h":"What general liability covers","cov":[("Third-party bodily injury","a customer slips and falls in your store or office."),
   ("Third-party property damage","you or an employee damage a client's property while working."),
   ("Personal & advertising injury","claims like libel, slander, or copyright in your advertising."),
   ("Legal defense costs","attorney fees and settlements — even for a claim that turns out to be groundless."),
   ("Products & completed operations","injury or damage caused by your product or finished work.")],
 "faqs":[("Is general liability insurance required in Michigan?","The state doesn't mandate general liability for most businesses, but in practice you'll need it the moment you sign a commercial lease, bid a job, or take on a client — landlords, general contractors, and customers almost always require proof of coverage before they'll work with you."),
   ("How much general liability coverage do I need?","Most Michigan contracts and leases require $1 million per occurrence and $2 million aggregate, often with the other party named as an additional insured. Higher-risk work or larger contracts may also require a commercial umbrella on top. We set your limits to match the contracts you're chasing."),
   ("What's the difference between general liability and professional liability?","General liability covers physical risks — bodily injury and property damage. Professional liability (E&O) covers financial harm from your advice or services. Many businesses need both; one won't respond to the other's claims."),
   ("How much does general liability cost for a Michigan business?","It depends on your industry, revenue, and claims history. A small office or consultant might pay $400–$900 a year; contractors and higher-risk trades pay more. Because we're independent, we shop your risk across carriers to find the best combination of price and coverage.")],
 "cta":"Get a general liability quote"},

{"section":"business","slug":"commercial-property-insurance","def_id":"commercial-property",
 "eyebrow":"Commercial / Property","svc":"Commercial Property Insurance",
 "title":"Michigan Commercial Property Insurance",
 "meta":"Commercial property insurance for Michigan businesses — buildings, equipment, inventory, and lost income after a covered loss. Multi-carrier shopping from an independent agency.",
 "hero":"photo-1486406146926-c627a92ad1ab","alt":"Commercial buildings — Michigan commercial property insurance",
 "lead":"Commercial property insurance protects the physical things your Michigan business depends on — your building, equipment, inventory, and furnishings — against fire, storms, theft, and more. The right policy also replaces the income you lose while you recover.",
 "whatwedo":[("Replacement-cost coverage","we push for replacement-cost over actual-cash-value where it makes sense, so a claim rebuilds your business instead of paying depreciated pennies."),
   ("Business income protection","we add business interruption coverage so a covered loss doesn't also cost you your revenue and payroll."),
   ("Accurate valuations","under-insuring triggers coinsurance penalties at claim time — we value your building and contents correctly up front."),
   ("Multi-carrier shopping","we compare property markets to fit your building type, occupancy, and location.")],
 "who_h":"Businesses we cover","who":"Owners and tenants of retail spaces, offices, restaurants, warehouses, light manufacturing, mixed-use buildings, and more. Property coverage is often bundled with general liability in a cost-effective Business Owners Policy (BOP).",
 "cov_h":"What commercial property covers","cov":[("Buildings","your structure, including permanently installed fixtures and systems."),
   ("Business personal property","equipment, inventory, furniture, and supplies."),
   ("Business income & extra expense","lost revenue and added costs while you recover from a covered loss."),
   ("Outdoor signs & fixtures","exterior signage and property in the open."),
   ("Equipment breakdown","mechanical or electrical breakdown of critical systems (added).")],
 "faqs":[("What does commercial property insurance cover?","Your building, business personal property (equipment, inventory, furniture), and often business income lost while you recover. Coverage forms range from basic named-peril to special (open-peril). It typically does not cover flood or earthquake, which are separate."),
   ("Do I need commercial property insurance if I rent my space?","Yes. Your landlord's policy covers the building shell, not your equipment, inventory, improvements, or lost income. A tenant's property/BOP policy covers what's yours — and most commercial leases require it."),
   ("What is actual cash value vs. replacement cost?","Replacement cost pays to repair or replace at today's prices. Actual cash value subtracts depreciation, which can mean a fraction of what you need. We help you choose and price the right valuation."),
   ("Does commercial property insurance cover floods?","No — flood is excluded from standard commercial property policies and is written separately. If your business is in a low-lying or flood-prone area, we can quote commercial flood coverage.")],
 "cta":"Get a commercial property quote"},

{"section":"business","slug":"commercial-auto-insurance","def_id":"commercial-auto",
 "eyebrow":"Commercial / Auto","svc":"Commercial Auto Insurance",
 "title":"Michigan Commercial Auto Insurance",
 "meta":"Commercial auto insurance for Michigan businesses — trucks, vans, and fleets. Liability, physical damage, hired and non-owned auto, and Michigan No-Fault handled right.",
 "hero":"photo-1574023240744-64c47c8c0676","alt":"Work vehicle — Michigan commercial auto insurance",
 "lead":"If your business owns vehicles — or employees drive for work — your personal auto policy won't cover a claim. Michigan commercial auto insurance covers your trucks, vans, and fleet, and handles the state's No-Fault rules the way a business needs.",
 "whatwedo":[("The right vehicle classification","we rate your vehicles correctly by use and weight so you're covered without overpaying."),
   ("Hired & non-owned auto","coverage for rented vehicles and for employees who run errands in their own cars — a gap most owners don't know they have."),
   ("Michigan No-Fault done right","we set PIP and residual liability correctly for business-titled vehicles."),
   ("Fleet and single-vehicle markets","whether you have one van or twenty trucks, we shop carriers that want your class of business.")],
 "who_h":"Businesses we cover","who":"Contractors and tradespeople, delivery and courier services, landscapers, food trucks, sales and service fleets, nonprofits with vehicles, and any Michigan business with vehicles titled to the company or used for work.",
 "cov_h":"What commercial auto covers","cov":[("Liability","bodily injury and property damage you cause with a business vehicle."),
   ("Michigan No-Fault / PIP","medical and wage benefits under Michigan's No-Fault system."),
   ("Physical damage","collision and comprehensive for your own vehicles."),
   ("Hired auto","vehicles you rent or borrow for business."),
   ("Non-owned auto","employees' personal vehicles used for business errands.")],
 "faqs":[("Do I need commercial auto insurance in Michigan?","If a vehicle is titled to your business, or employees drive for work beyond commuting, yes — a personal auto policy can deny a claim that happens during business use. Even if you drive your personal truck for the business, you may need commercial coverage."),
   ("Does my personal auto policy cover business use?","Usually not for true business use. Personal policies exclude or limit business activities like deliveries, hauling, or hired driving. Using a personal vehicle for work is one of the most common uncovered claims we see."),
   ("What is hired and non-owned auto coverage?","Hired auto covers vehicles your business rents or leases; non-owned covers employees using their own cars for business. Together they close a gap that catches many small businesses by surprise."),
   ("How is commercial auto rated in Michigan?","By vehicle type and weight, how it's used, radius of operation, driving records, and your No-Fault elections. We shop multiple carriers to match your fleet to the right market and price.")],
 "cta":"Get a commercial auto quote"},

{"section":"business","slug":"business-owners-policy","def_id":"bop",
 "eyebrow":"Commercial / BOP","svc":"Business Owners Policy",
 "title":"Michigan Business Owner's Policy (BOP)",
 "meta":"A Business Owner's Policy bundles general liability and commercial property into one cost-effective policy for Michigan small businesses — often 10–20% less than buying separately.",
 "hero":"photo-1551836022-aadb801c60ae","alt":"Michigan small business owner — business owner's policy",
 "lead":"A Business Owner's Policy (BOP) bundles the two coverages most Michigan small businesses need — general liability and commercial property — into one policy, usually for 10–20% less than buying them separately. It's the simplest, most cost-effective place for most small businesses to start.",
 "whatwedo":[("Bundle and save","we package GL, property, and business income together for a lower combined premium."),
   ("Add what you need","workers comp, commercial auto, cyber, and professional liability layer on cleanly around the BOP."),
   ("Eligibility review","not every business qualifies for a BOP — we check, and find the right alternative if not."),
   ("Multi-carrier shopping","we compare BOP markets so you get the best bundle for your industry.")],
 "who_h":"Businesses a BOP fits","who":"Office-based businesses, retailers and shops, restaurants, light contractors, professional services, and many other small-to-midsize Michigan businesses that meet underwriting criteria. Higher-risk operations may need standalone policies instead — we'll tell you which.",
 "cov_h":"What a BOP bundles","cov":[("General liability","third-party bodily injury, property damage, and advertising injury."),
   ("Commercial property","your building, equipment, inventory, and furnishings."),
   ("Business income","lost revenue and expenses while you recover from a covered loss."),
   ("Often added","equipment breakdown, data/cyber, hired & non-owned auto."),
   ("Bought separately","workers comp, commercial auto, and professional liability.")],
 "faqs":[("What is a Business Owner's Policy?","A BOP bundles general liability, commercial property, and business income coverage into a single, lower-cost policy for eligible small and midsize businesses — typically 10–20% cheaper than buying each coverage on its own."),
   ("What does a BOP not cover?","A BOP doesn't include workers compensation, commercial auto, or professional liability — those are added separately. It also excludes flood and, usually, cyber unless you add it. We build the full stack around your BOP."),
   ("Is my business eligible for a BOP?","Many office, retail, restaurant, and light-contracting businesses qualify based on size, industry, and risk. Higher-hazard operations often need monoline policies instead. We check eligibility across carriers for you."),
   ("How much does a BOP cost in Michigan?","It depends on your industry, revenue, property values, and location — but bundling typically runs 10–20% less than separate policies. We shop multiple BOP markets to find your best price.")],
 "cta":"Get a BOP quote"},

{"section":"business","slug":"cyber-liability-insurance","def_id":"cyber-liability",
 "eyebrow":"Commercial / Cyber","svc":"Cyber Liability Insurance",
 "title":"Michigan Cyber Liability Insurance",
 "meta":"Cyber liability insurance for Michigan businesses — data breaches, ransomware, and the response costs your standard business policy won't cover.",
 "hero":"photo-1614064641938-3bbee52942c7","alt":"Cybersecurity — Michigan cyber liability insurance",
 "lead":"A single phishing email can lock your systems and demand a five- or six-figure ransom — and your general liability or BOP won't cover a dime of it. Cyber liability insurance covers the breach response, extortion, and liability that come with running a business on computers.",
 "whatwedo":[("Cover the real costs","forensic investigation, customer notification, credit monitoring, legal, and PR — the expensive parts of a breach."),
   ("Ransomware & extortion","coverage and expert response for the attack small businesses are most likely to face."),
   ("Right-sized for small business","you don't need an enterprise policy — we match coverage to your actual data and revenue."),
   ("Multi-carrier shopping","cyber pricing and terms vary widely — we compare markets so you don't overpay.")],
 "who_h":"Businesses that need cyber","who":"Any Michigan business that stores customer data, takes card payments, sends invoices by email, or relies on computers to operate — which is nearly all of them. Healthcare, professional services, retail, and contractors are frequent targets.",
 "cov_h":"What cyber liability covers","cov":[("Breach response","forensics, notification, credit monitoring, and legal costs."),
   ("Ransomware & cyber extortion","ransom payments and expert negotiation/recovery."),
   ("Business interruption","income lost while systems are down."),
   ("Liability","claims from customers or partners whose data was exposed."),
   ("Funds-transfer fraud","losses from social-engineering and wire-fraud scams.")],
 "faqs":[("Does my business policy cover a cyberattack?","Almost never. Standard general liability and BOP policies exclude cyber events. A data breach or ransomware attack needs a dedicated cyber liability policy — the gap surprises many owners only after an incident."),
   ("How much does cyber insurance cost in Michigan?","For most small businesses, far less than a single breach — the average small-business attack costs well into six figures. Premiums depend on your revenue, data, and security controls. We shop carriers to find the right coverage at the right price."),
   ("What is ransomware coverage?","It covers the ransom demand plus the expert negotiation, recovery, and business income loss that follow — the costs that can otherwise sink a small business after an attack."),
   ("Do I need cyber insurance if I'm a small business?","Yes — small businesses are the most common ransomware targets precisely because they're less defended. If you hold customer data or run on computers, you have the exposure cyber insurance is built for.")],
 "cta":"Get a cyber liability quote"},

{"section":"business","slug":"commercial-umbrella-insurance","def_id":"commercial-umbrella",
 "eyebrow":"Commercial / Umbrella","svc":"Commercial Umbrella Insurance",
 "title":"Michigan Commercial Umbrella Insurance",
 "meta":"Commercial umbrella insurance adds $1M–$25M+ of liability protection over your Michigan business's general liability, auto, and employer's liability policies — often required by larger contracts.",
 "hero":"photo-1562564055-71e051d33c19","alt":"Michigan business protection — commercial umbrella insurance",
 "lead":"A commercial umbrella sits on top of your other liability policies and adds millions in extra protection for a relatively small premium. It's the coverage that keeps one catastrophic claim from wiping out the business — and it's increasingly required by large contracts, landlords, and municipalities.",
 "whatwedo":[("Extra limits where you need them","$1M to $25M+ over your general liability, commercial auto, and employer's liability."),
   ("Meet contract requirements","many big jobs, leases, and government work require umbrella limits — we set yours to win the contract."),
   ("Affordable protection","umbrella limits cost far less per dollar than raising each underlying policy."),
   ("Multi-carrier shopping","we match your umbrella to your underlying coverage and shop it for the best rate.")],
 "who_h":"Businesses that need umbrella","who":"Contractors and tradespeople, businesses with vehicles or fleets, companies with foot traffic, landlords and property owners, and any Michigan business required by contract to carry higher liability limits.",
 "cov_h":"How a commercial umbrella works","cov":[("Sits above your policies","extends your general liability, auto, and employer's liability limits."),
   ("Adds $1M–$25M+","large additional limits for a comparatively low premium."),
   ("Catastrophic claims","covers the big judgments that exceed your base policy limits."),
   ("Contract compliance","satisfies higher-limit requirements from clients and municipalities."),
   ("Broadens some coverage","can fill certain gaps in the underlying policies.")],
 "faqs":[("What does a commercial umbrella cover?","It adds liability limits on top of your general liability, commercial auto, and employer's liability policies. If a covered claim exceeds the underlying limit, the umbrella pays the rest — up to your umbrella limit."),
   ("How much does a commercial umbrella cost?","Far less per dollar of coverage than raising each underlying policy. A $1M umbrella is often a few hundred to a couple thousand dollars a year depending on your business. We shop it across carriers."),
   ("Do I need a commercial umbrella?","If you have meaningful liability exposure — vehicles, employees, foot traffic, or contracts that require high limits — an umbrella is usually the most cost-effective way to protect the business from a catastrophic claim."),
   ("Why do contracts require umbrella coverage?","Larger clients, landlords, and government entities want assurance you can cover a serious claim. An umbrella lets you meet $5M–$10M+ requirements affordably without overhauling your base policies.")],
 "cta":"Get a commercial umbrella quote"},

{"section":"business","slug":"builders-risk-insurance","def_id":"builders-risk",
 "eyebrow":"Commercial / Builders Risk","svc":"Builders Risk Insurance",
 "title":"Michigan Builders Risk Insurance",
 "meta":"Builders risk (course-of-construction) insurance for Michigan projects — covers buildings under construction or renovation against fire, theft, and weather. Required by most lenders.",
 "hero":"photo-1589939705384-5185137a7f0f","alt":"Michigan construction project — builders risk insurance",
 "lead":"Builders risk — also called course-of-construction — covers a building while it's being built or renovated, when a standard property policy doesn't apply yet. It protects the structure, materials, and work against fire, theft, vandalism, and weather from groundbreaking to completion.",
 "whatwedo":[("Project-matched terms","we set coverage to your project value and timeline so there are no gaps before the permanent policy starts."),
   ("Lender and GC compliance","most construction loans and general contractors require builders risk — we provide the documentation fast."),
   ("Materials on and off site","coverage for materials at the job site, in transit, and in storage."),
   ("Multi-carrier shopping","we shop the builders risk markets for new construction and renovations alike.")],
 "who_h":"Projects we cover","who":"Owners, builders, and general contractors on new homes and commercial buildings, ground-up construction, additions, and major renovations across Michigan — residential and commercial.",
 "cov_h":"What builders risk covers","cov":[("The structure under construction","the building and permanent fixtures while being built."),
   ("Building materials","on site, in transit, and in temporary storage."),
   ("Fire, theft & vandalism","common losses on active job sites."),
   ("Weather damage","wind, hail, and storm losses during construction."),
   ("Soft costs (added)","extra interest, fees, and rent from a covered delay.")],
 "faqs":[("What is builders risk insurance?","A temporary policy that covers a building while it's under construction or renovation — the structure, materials, and certain costs — against fire, theft, vandalism, and weather. It runs from the start of work through completion, when a permanent property policy takes over."),
   ("Who needs to buy builders risk — owner or contractor?","Either can, but it should be clearly assigned in the contract. Lenders usually require it on construction loans, and many general contractors require it on commercial projects. We help structure it so the right party carries it."),
   ("How long does builders risk coverage last?","For the construction period — typically 3, 6, or 12 months — with extensions available if the project runs long. Once the building is complete and occupied, you switch to a standard property or homeowners policy."),
   ("Does builders risk cover tools and equipment?","Generally no — contractor tools and equipment are covered under a separate inland marine (contractor's equipment) policy. Builders risk covers the project itself and its materials. We can write both.")],
 "cta":"Get a builders risk quote"},

{"section":"business","slug":"surety-bonds","def_id":"bonds",
 "eyebrow":"Commercial / Bonds","svc":"Surety Bonds",
 "title":"Michigan Surety Bonds",
 "meta":"Surety and license bonds for Michigan businesses and contractors — license & permit bonds, contract and performance bonds, and more. Fast issuance, competitive rates.",
 "hero":"photo-1450101499163-c8848c66ca85","alt":"Signing a surety bond — Michigan surety bonds",
 "lead":"A surety bond isn't insurance for you — it's a three-party guarantee that you'll meet an obligation, backing your promise to a customer, a government agency, or a project owner. Michigan contractors and licensed businesses need them to pull permits, win bids, and stay compliant.",
 "whatwedo":[("Fast issuance","we know which bonds Michigan agencies and projects require and turn most around quickly."),
   ("Competitive rates","bond pricing is based on the bond type and your credit — we shop surety markets for your best rate."),
   ("The right bond","license, permit, contract, performance, payment, and court bonds each work differently — we get you the correct one."),
   ("Growing bonding capacity","as your business grows, we help build the surety relationships that raise your bonding limits.")],
 "who_h":"Bonds we write","who":"Contractors (bid, performance, and payment bonds), licensed trades and professionals (license and permit bonds), auto dealers, freight brokers, notaries, and businesses that need court or fiduciary bonds across Michigan.",
 "cov_h":"Common Michigan bond types","cov":[("License & permit bonds","required to hold a license or pull permits in many trades."),
   ("Bid bonds","guarantee you'll honor a bid if awarded the job."),
   ("Performance bonds","guarantee you'll complete a contract as agreed."),
   ("Payment bonds","guarantee your subs and suppliers get paid."),
   ("Court & fiduciary bonds","required in certain legal and estate matters.")],
 "faqs":[("What is a surety bond?","A three-party agreement: you (the principal), the party requiring the bond (the obligee), and the surety that backs your promise. If you fail to meet the bonded obligation, the surety pays the obligee — and you repay the surety. It guarantees your performance, it doesn't insure your losses."),
   ("How much does a surety bond cost in Michigan?","Usually a small percentage of the bond amount — often 1–15% depending on the bond type and your credit. A $10,000 license bond might cost $100–$500 a year. We shop surety markets to find your best rate."),
   ("What bonds do Michigan contractors need?","It varies by trade and municipality — commonly license/permit bonds to operate, plus bid, performance, and payment bonds on larger or public projects. We confirm exactly what your work and jurisdiction require."),
   ("Can I get bonded with bad credit?","Often yes. Many license and permit bonds are available across credit ranges, sometimes at a higher rate, and specialty markets exist for tougher credit. Tell us the bond you need and we'll find a market for it.")],
 "cta":"Get a surety bond"},

# ===================== PERSONAL =====================
{"section":"personal","slug":"umbrella-insurance","def_id":"umbrella-insurance",
 "eyebrow":"Personal / Umbrella","svc":"Personal Umbrella Insurance",
 "title":"Michigan Umbrella Insurance","blog":"michigan-umbrella-insurance-who-needs-it",
 "meta":"Personal umbrella insurance adds $1M+ of liability protection over your Michigan auto and home policies for around $150–$300 a year. Find out who needs it and what it covers.",
 "hero":"photo-1562564055-71e051d33c19","alt":"Michigan family protection — personal umbrella insurance",
 "lead":"A personal umbrella adds a million dollars or more of liability protection on top of your auto and home policies — usually for a couple hundred dollars a year. It's the coverage that protects your savings, home, and future income if you're ever sued for more than your base policies cover.",
 "whatwedo":[("Extra liability where it counts","$1M–$5M over your auto, home, boat, and rental-property liability."),
   ("Protects your assets","a serious at-fault accident can exceed your auto limits fast — the umbrella covers the gap so your assets aren't exposed."),
   ("Surprisingly affordable","often $150–$300/year for $1M — one of the best value coverages in insurance."),
   ("Bundled and shopped","we coordinate it with your underlying policies and shop it for the best rate.")],
 "who_h":"Who needs an umbrella","who":"Homeowners with savings or equity, families with teen drivers, boat and recreational-vehicle owners, landlords, anyone with a pool or dog, and anyone whose net worth exceeds their current liability limits. If a lawsuit could reach your assets, you need one.",
 "cov_h":"What a personal umbrella covers","cov":[("Auto liability above your policy","the big at-fault claim that exceeds your auto limits."),
   ("Home & premises liability","injuries on your property, including pools and dogs."),
   ("Landlord/rental liability","claims tied to rental property you own."),
   ("Personal injury","libel, slander, and certain personal-injury claims."),
   ("Legal defense","defense costs for covered claims, on top of the limit.")],
 "faqs":[("What does umbrella insurance cover?","It adds liability limits over your auto, home, and other personal policies. If an at-fault accident or lawsuit exceeds your underlying limits, the umbrella pays the rest — up to $1M or more — plus legal defense. It doesn't cover your own property or injuries."),
   ("How much does umbrella insurance cost in Michigan?","Typically $150–$300 a year for $1 million in coverage, with each additional million costing less. It's one of the highest-value coverages available because it protects everything you own for a small premium."),
   ("Who really needs umbrella insurance?","Anyone whose assets or future income exceed their current liability limits — homeowners, families with teen drivers, boat owners, landlords, and pool or dog owners. If you could be sued for more than your auto/home limits, an umbrella protects the difference."),
   ("Do I need to have my home and auto with you to get an umbrella?","Usually your umbrella carrier requires certain minimum liability limits on the underlying auto and home policies, and it's cleanest to coordinate them. We can shop the umbrella alongside your other coverage to make it all line up.")],
 "cta":"Get an umbrella quote"},

{"section":"personal","slug":"flood-insurance","def_id":"flood-insurance",
 "eyebrow":"Personal / Flood","svc":"Flood Insurance","blog":"michigan-flood-insurance",
 "title":"Michigan Flood Insurance",
 "meta":"Flood insurance for Michigan homeowners — because your homeowners policy doesn't cover flood damage. NFIP and private flood options, even outside high-risk zones.",
 "hero":"photo-1657069342866-2d11c2509b02","alt":"Flooded street — Michigan flood insurance",
 "lead":"Your homeowners policy does not cover flood damage — and in Michigan, you don't have to live on a river to flood. Heavy rain, rapid snowmelt, and overwhelmed storm drains put basements and homes under water every year. Flood insurance is a separate policy that fills that gap.",
 "whatwedo":[("NFIP and private options","we quote both the federal program and private flood markets — private is often cheaper and broader."),
   ("Coverage outside high-risk zones","most Michigan flooding happens outside mapped flood zones, where coverage is least expensive — we make sure you're not assuming you're safe."),
   ("Right building and contents limits","we set structure and contents coverage to actually rebuild and replace."),
   ("Plain-English risk review","we explain your flood zone and options without the jargon.")],
 "who_h":"Who needs flood insurance","who":"Homeowners with finished basements, homes near lakes, rivers, or low-lying areas, anyone in a mapped flood zone (where lenders require it), and — frankly — most Michigan homeowners, since the majority of flood claims come from outside high-risk zones.",
 "cov_h":"What flood insurance covers","cov":[("Building coverage","foundation, walls, electrical, plumbing, HVAC, and built-ins."),
   ("Contents coverage","furniture, appliances, and personal belongings."),
   ("Debris removal","cleanup after a flood event."),
   ("Outside floodwater","rising water that a homeowners policy excludes."),
   ("Not covered by home insurance","exactly the gap a homeowners policy leaves open.")],
 "faqs":[("Does homeowners insurance cover flood damage?","No. Damage from rising or surface water — an overflowing creek, storm surge, or several inches of water across your yard and into the basement — is excluded from every standard homeowners policy. Flood requires a separate policy."),
   ("Do I need flood insurance if I'm not in a flood zone?","Often yes. The majority of Michigan flood claims come from outside high-risk zones, where coverage is also cheapest. If you have a finished basement or are anywhere water collects, it's worth quoting."),
   ("How much does flood insurance cost in Michigan?","Outside high-risk zones it's frequently a few hundred dollars a year; in mapped zones it costs more. Private flood markets are often cheaper and broader than the NFIP — we quote both so you can compare."),
   ("What's the difference between flood and water backup coverage?","Flood insurance covers outside water entering the home. Sewer/drain backup — water coming up through your drains — is a separate endorsement on your homeowners policy. Many Michigan homes need both. We make sure you're covered for each.")],
 "cta":"Get a flood insurance quote"},

{"section":"personal","slug":"boat-insurance","def_id":"boat-insurance",
 "eyebrow":"Personal / Boat","svc":"Boat & Watercraft Insurance","blog":"michigan-boat-rv-insurance",
 "title":"Michigan Boat & Watercraft Insurance",
 "meta":"Boat and watercraft insurance for Michigan — pontoons, powerboats, jet skis, and sailboats. Real hull and liability limits your homeowners policy won't give you.",
 "hero":"photo-1779078063955-8fbf934c358c","alt":"Boat on a Michigan lake — boat insurance",
 "lead":"Michigan has more registered boats than almost any state — and the small boat rider on your homeowners policy isn't enough to protect them. A real watercraft policy covers your boat, your liability on the water, and the gear that goes with it.",
 "whatwedo":[("Real hull and liability limits","standalone coverage that actually replaces the boat and protects you on the water — unlike the token limits on a home policy."),
   ("Coverage for how you boat","pontoons, powerboats, fishing boats, jet skis, and sailboats, on inland lakes and the Great Lakes."),
   ("Lay-up savings","we set seasonal lay-up so you're not overpaying through a Michigan winter."),
   ("Multi-carrier shopping","we compare marine markets for the best mix of coverage and price.")],
 "who_h":"Watercraft we cover","who":"Pontoons, runabouts and powerboats, fishing boats, personal watercraft and jet skis, sailboats, and the trailers that haul them — across Michigan's inland lakes and the Great Lakes.",
 "cov_h":"What boat insurance covers","cov":[("Hull / physical damage","your boat, motor, and trailer against collision, theft, and more."),
   ("Liability","injury or damage you cause to others on the water."),
   ("Medical payments","injuries to you and your passengers."),
   ("Uninsured boater","when another boater at fault has no coverage."),
   ("Personal effects & gear","fishing equipment and belongings aboard.")],
 "faqs":[("Does my homeowners policy cover my boat?","Only in a very limited way. Most homeowners policies include a small watercraft liability sublimit and little or no hull coverage — not enough for a real boat. A standalone marine policy gives you actual hull, liability, and medical limits."),
   ("How much does boat insurance cost in Michigan?","Often a few hundred dollars a year, depending on the boat's value, type, horsepower, and how you use it. Seasonal lay-up keeps the cost down. We shop marine carriers to find your best rate."),
   ("Do I need insurance for a jet ski or pontoon?","Michigan doesn't mandate it, but marinas, lakes, and lenders often require liability coverage, and the risk of an on-water injury claim makes it well worth carrying. We write jet skis, pontoons, and all personal watercraft."),
   ("What is lay-up coverage?","Lay-up reflects the months your boat is out of the water for the Michigan winter. Coverage and cost adjust for the off-season so you're not paying full freight year-round while still protecting the boat in storage.")],
 "cta":"Get a boat insurance quote"},

{"section":"personal","slug":"rv-insurance","def_id":"rv-insurance",
 "eyebrow":"Personal / RV","svc":"RV Insurance","blog":"michigan-boat-rv-insurance",
 "title":"Michigan RV Insurance",
 "meta":"RV insurance for Michigan — motorhomes, travel trailers, and campers. Coverage for the road and for full-timers that auto and home policies don't provide.",
 "hero":"photo-1779078063955-8fbf934c358c","alt":"RV on a Michigan road — RV insurance",
 "lead":"Your RV is part vehicle, part home — and neither your auto nor your homeowners policy fully covers it. RV insurance protects the motorhome or trailer, your liability on the road, and the belongings and attachments that make it yours.",
 "whatwedo":[("Coverage for your RV type","motorhomes (Class A, B, C) and towables — travel trailers, fifth wheels, and campers."),
   ("Full-timer coverage","if you live in your RV, we add the liability and contents coverage a part-time policy leaves out."),
   ("Attachments and belongings","awnings, satellite gear, and the contents inside."),
   ("Lay-up and multi-carrier shopping","seasonal savings plus comparison across RV markets.")],
 "who_h":"RVs we cover","who":"Class A, B, and C motorhomes, travel trailers, fifth wheels, pop-ups, and truck campers — for weekend trips, seasonal use, and full-time living across Michigan and beyond.",
 "cov_h":"What RV insurance covers","cov":[("Physical damage","collision and comprehensive for your motorhome or trailer."),
   ("Liability","injury or damage you cause while driving a motorhome."),
   ("Contents & attachments","belongings, awnings, and installed equipment."),
   ("Full-timer liability","home-style liability if you live in the RV."),
   ("Roadside & emergency expense","towing and lodging after a covered breakdown or loss.")],
 "faqs":[("Does my auto insurance cover my RV?","A drivable motorhome needs its own RV policy — auto insurance isn't built for it. Towable trailers get limited liability from the tow vehicle's policy, but their contents and physical damage need a separate RV policy."),
   ("Do I need RV insurance in Michigan?","Motorhomes you drive must be insured like any vehicle. Towables aren't required by the state, but lenders require coverage on financed units and it's well worth protecting the trailer and its contents. We write both."),
   ("What is full-timer RV coverage?","If your RV is your primary residence, full-timer coverage adds the personal liability and contents protection a standard RV policy doesn't include — closer to what a homeowners policy would provide. We set it up if you live on the road."),
   ("How much does RV insurance cost in Michigan?","It depends on the RV's type and value, how you use it, and whether you full-time. Seasonal lay-up lowers the cost for weekend and summer users. We shop RV carriers to find your best combination of coverage and price.")],
 "cta":"Get an RV insurance quote"},

{"section":"personal","slug":"motorcycle-insurance","def_id":"motorcycle-insurance",
 "eyebrow":"Personal / Motorcycle","svc":"Motorcycle Insurance","blog":"michigan-motorcycle-insurance-terminology",
 "title":"Michigan Motorcycle Insurance",
 "meta":"Motorcycle insurance for Michigan riders — liability, physical damage, gear coverage (CPE), and the No-Fault rules that make Michigan motorcycle coverage unique.",
 "hero":"photo-1676631284522-8007dd380171","alt":"Motorcycle on a Michigan road — motorcycle insurance",
 "lead":"Michigan's motorcycle insurance rules are genuinely different — No-Fault doesn't treat bikes like cars, and the wrong setup can leave you exposed after a crash. We make sure your coverage, gear protection, and limits actually fit how and what you ride.",
 "whatwedo":[("Michigan-specific coverage","we set liability and medical coverage correctly for the way Michigan No-Fault treats motorcycles — a common gap for riders."),
   ("Gear coverage (CPE)","carried personal effects protects your helmet, jacket, and gear, not just the bike."),
   ("Coverage for what you ride","cruisers, sport bikes, touring, off-road, and trikes, with agreed-value options for custom bikes."),
   ("Lay-up and multi-carrier shopping","seasonal savings for the Michigan off-season plus comparison across carriers.")],
 "who_h":"Bikes we cover","who":"Cruisers, sport bikes, touring and adventure bikes, trikes, off-road and dual-sport, and custom builds — for new riders and lifelong ones across Michigan.",
 "cov_h":"What motorcycle insurance covers","cov":[("Liability","injury or damage you cause to others."),
   ("Physical damage","collision and comprehensive for your bike."),
   ("Carried personal effects (CPE)","your helmet, jacket, and riding gear."),
   ("Accessories / custom parts","aftermarket and custom equipment, by agreed value."),
   ("Uninsured/underinsured motorist","when an at-fault driver has too little coverage.")],
 "faqs":[("Is motorcycle insurance required in Michigan?","Yes — Michigan requires liability coverage to register and ride. But the way No-Fault applies to motorcycles is different from cars, which affects how your medical benefits work after a crash. We set your coverage up correctly for it."),
   ("How does Michigan No-Fault affect motorcycle coverage?","Motorcycles aren't 'motor vehicles' under Michigan No-Fault the same way cars are, so medical benefits after a motorcycle crash often depend on the auto policy of a vehicle involved — or on coverage you add. It's the single most misunderstood part of riding insured here, and we walk you through it."),
   ("What is CPE coverage?","Carried Personal Effects covers your gear — helmet, jacket, boots, gloves — which a basic policy leaves out. For riders with serious gear, it's an inexpensive add that pays off after a loss."),
   ("Can I save with lay-up coverage over the Michigan winter?","Yes. Many riders adjust coverage during the months the bike is stored, keeping comprehensive (for theft/fire) while reducing on-road coverage. We set lay-up so you're protected in storage without paying full freight year-round.")],
 "cta":"Get a motorcycle quote"},

{"section":"personal","slug":"renters-insurance","def_id":"renters-insurance",
 "eyebrow":"Personal / Renters","svc":"Renters Insurance","blog":"michigan-renters-insurance",
 "title":"Michigan Renters Insurance",
 "meta":"Renters insurance for Michigan tenants — around $15–$20 a month to cover your belongings, liability, and living expenses if your unit becomes unlivable.",
 "hero":"photo-1768941124460-6fa7161715ff","alt":"Apartment interior — Michigan renters insurance",
 "lead":"Your landlord's policy covers the building — not a thing you own inside it. For about the price of a couple lunches a month, renters insurance covers your belongings, protects you if someone's hurt in your unit, and pays for a place to stay if you're displaced.",
 "whatwedo":[("Cover your stuff for real value","we set personal-property limits and add replacement cost so a loss actually replaces your things."),
   ("Liability that travels with you","protection if you accidentally injure someone or damage their property, at home or away."),
   ("Loss-of-use coverage","hotel and extra living costs if a fire or covered loss makes your unit unlivable."),
   ("Bundle to save","pairing renters with your auto often lowers both — we check.")],
 "who_h":"Who needs renters insurance","who":"Apartment and house renters, college students living off-campus, roommates, and anyone whose landlord requires proof of coverage on the lease. If you'd have to repay to replace everything you own, you need it.",
 "cov_h":"What renters insurance covers","cov":[("Personal property","furniture, electronics, clothing, and belongings — even away from home."),
   ("Personal liability","if you injure someone or damage their property."),
   ("Loss of use","temporary housing and costs if your unit is unlivable."),
   ("Medical payments","minor injuries to guests in your unit."),
   ("Theft","your belongings, including some items stolen outside the home.")],
 "faqs":[("What does renters insurance cover?","Your personal belongings (against fire, theft, and more), your personal liability if you injure someone or damage their property, and your living expenses if a covered loss makes your unit unlivable. It does not cover the building itself — that's your landlord's policy."),
   ("How much does renters insurance cost in Michigan?","Usually about $15–$20 a month for solid coverage. Bundling it with your auto policy often reduces the auto premium enough to offset much of the cost. It's one of the best value-for-money policies available."),
   ("Does my landlord's insurance cover my belongings?","No. Your landlord's policy covers the building structure, not your furniture, electronics, or clothes — and not your liability. If a fire or theft hits, only your own renters policy replaces your things."),
   ("Is renters insurance required in Michigan?","The state doesn't require it, but many Michigan landlords now require proof of renters insurance in the lease. Even when it's optional, the low cost and real protection make it worth carrying.")],
 "cta":"Get a renters quote"},

{"section":"personal","slug":"condo-insurance","def_id":"condo-insurance",
 "eyebrow":"Personal / Condo","svc":"Condo Insurance",
 "title":"Michigan Condo Insurance (HO-6)",
 "meta":"Condo insurance (HO-6) for Michigan owners — covers what your association's master policy doesn't: your interior, belongings, liability, and assessments.",
 "hero":"photo-1545324418-cc1a3fa10c00","alt":"Condominium building — Michigan condo insurance",
 "lead":"Your condo association's master policy stops at the walls — everything inside is on you. A condo (HO-6) policy covers your interior, your belongings, your liability, and the special assessments an association can pass along after a big loss.",
 "whatwedo":[("Fill the master-policy gap","we read how your association's master policy is written and cover exactly what it leaves to you — walls-in, fixtures, and improvements."),
   ("Loss-assessment coverage","protection when the association bills owners for a shortfall after a covered loss."),
   ("Belongings and liability","your personal property and personal liability, at home and away."),
   ("Bundle and shop","we pair condo with auto where it saves and compare carriers for the best rate.")],
 "who_h":"Who needs condo insurance","who":"Condominium and co-op owners, and many townhouse owners in associations. If you own your unit and an association maintains the building exterior, you need an HO-6 policy for everything the master policy doesn't cover.",
 "cov_h":"What condo (HO-6) covers","cov":[("Interior / walls-in","drywall, flooring, cabinets, fixtures, and your improvements."),
   ("Personal property","furniture, electronics, and belongings."),
   ("Personal liability","injuries to others or damage you cause."),
   ("Loss assessment","your share of an association assessment after a covered loss."),
   ("Loss of use","living costs if your unit becomes uninhabitable.")],
 "faqs":[("What does condo insurance (HO-6) cover?","It covers the parts of your condo the association's master policy doesn't: your interior finishes and improvements, your personal belongings, your personal liability, loss assessments, and living expenses if your unit is uninhabitable after a covered loss."),
   ("What's the difference between the master policy and my condo policy?","The association's master policy typically covers the building structure and common areas — often only up to the unfinished walls. Your HO-6 policy covers everything from the walls in: finishes, fixtures, belongings, and your liability. We coordinate the two so there's no gap."),
   ("What is loss-assessment coverage?","If a covered loss exceeds the association's master policy, the association can assess every owner for the shortfall. Loss-assessment coverage on your HO-6 pays your share — an important protection that's inexpensive to add."),
   ("How much does condo insurance cost in Michigan?","Often less than a homeowners policy since you're not insuring the whole building — commonly a few hundred dollars a year depending on your unit, belongings, and limits. We shop carriers to find your best rate.")],
 "cta":"Get a condo insurance quote"},

{"section":"personal","slug":"collector-car-insurance","def_id":"collector-car-insurance",
 "eyebrow":"Personal / Collector Car","svc":"Classic & Collector Car Insurance",
 "title":"Michigan Classic & Collector Car Insurance",
 "meta":"Classic and collector car insurance for Michigan — agreed-value coverage, low-mileage rates, and specialist carriers like Hagerty for the cars you actually cherish.",
 "hero":"photo-1503376780353-7e6692767b70","alt":"Collector car — Michigan classic car insurance",
 "lead":"A standard auto policy pays the depreciated value of your classic — which is the opposite of what a collector car does. Collector car insurance covers your vehicle at an agreed value you set up front, at a fraction of regular auto rates, through specialists who understand these cars.",
 "whatwedo":[("Agreed-value coverage","you and the carrier agree on the car's value now, so a total loss pays that amount — not a depreciated book value."),
   ("Low collector rates","because these cars are driven less and cared for more, premiums are often far below a daily driver."),
   ("Specialist markets","we place coverage through collector-car specialists like Hagerty and others built for these vehicles."),
   ("Flexible usage & storage","coverage for shows, tours, and limited pleasure driving, with proper storage terms.")],
 "who_h":"Vehicles we cover","who":"Classic and antique cars, muscle cars, exotics, restored trucks, hot rods and street rods, modified and kit cars, and collector motorcycles — driven for shows, tours, and weekend enjoyment, not daily commuting.",
 "cov_h":"What collector car insurance covers","cov":[("Agreed value","a guaranteed payout amount you set, no depreciation."),
   ("Physical damage","collision and comprehensive for your collector vehicle."),
   ("Liability","injury or damage you cause while driving it."),
   ("Spare parts","coverage for parts and tools (varies by carrier)."),
   ("Show & tour use","driving to and from car shows, club events, and tours.")],
 "faqs":[("What qualifies as a collector or classic car?","It varies by carrier, but generally a vehicle that's maintained as a collectible, driven on a limited basis, and stored properly — antiques, classics, muscle cars, exotics, restored vehicles, and certain modified cars. Daily drivers don't qualify; we'll confirm your car's eligibility."),
   ("What is agreed-value coverage?","You and the insurer agree on your car's value when the policy is written. If it's totaled, you're paid that agreed amount — not a depreciated 'actual cash value.' It's the core reason collector policies exist and why a standard auto policy is the wrong fit."),
   ("Why is collector car insurance cheaper than regular auto?","Because these cars are driven far fewer miles, stored carefully, and rarely the owner's only vehicle, they're lower risk — so premiums are often a fraction of a daily-driver policy despite higher agreed values."),
   ("Can I drive my classic car on a collector policy?","Yes, within the policy's usage terms — typically pleasure driving, car shows, club events, and tours rather than daily commuting. Many policies offer generous mileage. We match the policy to how you actually enjoy the car.")],
 "cta":"Get a collector car quote"},

{"section":"personal","slug":"pet-insurance","def_id":"pet-insurance",
 "eyebrow":"Personal / Pet","svc":"Pet Insurance",
 "title":"Michigan Pet Insurance",
 "meta":"Pet insurance for Michigan dogs and cats — help with unexpected vet bills for accidents and illness, so care decisions aren't driven by cost.",
 "hero":"photo-1450778869180-41d0601e046e","alt":"Dog and cat — Michigan pet insurance",
 "lead":"One emergency vet visit can run into the thousands. Pet insurance reimburses a large share of the cost of accidents and illness, so a tough diagnosis is a medical decision — not a financial one. We help Michigan pet owners find a plan that fits their pet and budget.",
 "whatwedo":[("Plans that fit your pet","accident-only or accident-and-illness, with deductible and reimbursement levels you choose."),
   ("Use any licensed vet","these plans reimburse you — there's no network, so you keep your veterinarian and emergency hospital."),
   ("Coverage that grows with them","we explain how pre-existing conditions, waiting periods, and age affect coverage so there are no surprises."),
   ("Straight answers","we'll tell you honestly when a plan is and isn't worth it for your situation.")],
 "who_h":"Pets we help cover","who":"Dogs and cats of all ages — puppies and kittens (the best time to start, before conditions become pre-existing), adult pets, and breeds prone to hereditary conditions. Michigan families who'd never want cost to limit their pet's care.",
 "cov_h":"What pet insurance typically covers","cov":[("Accidents","injuries, swallowed objects, and emergencies."),
   ("Illness","infections, cancer, digestive and chronic conditions."),
   ("Diagnostics","exams, bloodwork, X-rays, and imaging."),
   ("Surgery & hospitalization","procedures and overnight care."),
   ("Optional wellness","routine care add-ons on some plans.")],
 "faqs":[("How does pet insurance work?","You pay the vet, then submit the bill and get reimbursed a set percentage (often 70–90%) after your deductible. There's no network — you can use any licensed veterinarian or emergency hospital in Michigan or anywhere."),
   ("Does pet insurance cover pre-existing conditions?","Generally no — conditions your pet shows signs of before coverage starts are excluded, which is why enrolling while your pet is young and healthy matters. Some conditions considered cured may be covered later; we explain each plan's rules."),
   ("How much does pet insurance cost in Michigan?","Typically $20–$50+ a month for a dog and a bit less for a cat, depending on age, breed, and the coverage level and deductible you choose. We help you weigh the premium against the protection for your specific pet."),
   ("Is pet insurance worth it?","If an unexpected $3,000–$8,000 vet bill would force a hard financial decision, it usually is — especially for younger pets enrolled before any conditions develop. For some owners, a dedicated savings fund works instead. We'll give you an honest read for your situation.")],
 "cta":"Get a pet insurance quote"},

# ===================== NICHE COMMERCIAL =====================
{"section":"business","slug":"fitness-gym-insurance","def_id":"fitness-gym",
 "eyebrow":"Commercial / Fitness & Gym","svc":"Fitness & Gym Insurance","title":"Michigan Fitness & Gym Insurance",
 "meta":"Insurance for Michigan gyms, fitness studios, and personal trainers — general liability, professional liability, member-injury, and equipment coverage from an independent agency.",
 "hero":"photo-1534438327276-14e5300c3a48","alt":"Michigan gym floor — fitness and gym insurance",
 "lead":"Fitness businesses live with injury risk every day — a dropped weight, a slip on the floor, a member who pushes too hard. Michigan gym and studio insurance covers the liability, your equipment, and the professional exposure your trainers carry.",
 "whatwedo":[("Liability built for fitness","general liability plus professional liability for trainers and instructors — the member-injury claims a generic policy misses."),
   ("Coverage for your discipline","CrossFit, hot yoga, martial arts, and personal training each carry different exposures; we price yours correctly."),
   ("Protect your equipment and space","property coverage for machines, free weights, and your buildout."),
   ("Multi-carrier shopping","we compare fitness markets so you're covered without overpaying.")],
 "who_h":"Facilities we cover","who":"Gyms and health clubs, boutique and CrossFit studios, yoga and Pilates studios, martial arts and boxing gyms, dance studios, and independent personal trainers across Michigan.",
 "cov_h":"What fitness insurance covers","cov":[("General liability","slips, falls, and member injuries on your premises."),
   ("Professional liability","claims that a trainer's instruction caused injury."),
   ("Equipment and property","machines, weights, and your studio buildout."),
   ("Assault and battery","an often-required coverage for facilities open to the public."),
   ("Participant / member injury","injury claims tied to classes and training.")],
 "faqs":[("What insurance does a gym or fitness studio need in Michigan?","At minimum general liability and professional liability (for trainer and instructor claims), plus property coverage for equipment and your buildout. Many landlords and franchisors also require assault and battery coverage and specific limits. We build the package around your facility."),
   ("Do personal trainers need their own insurance?","Yes — even independent trainers and those working in someone else's gym carry professional liability exposure for injury claims tied to their instruction. Coverage is inexpensive and often required by the facilities you work in."),
   ("Why do fitness businesses need professional liability?","General liability covers a slip-and-fall, but not a claim that your trainer's program or advice injured a member. Professional liability fills that gap — essential for any business giving fitness instruction."),
   ("How much does gym insurance cost in Michigan?","It depends on your size, services, membership, and class types — higher-intensity formats cost more. Because we're independent, we shop fitness markets to find the right coverage at the right price.")],
 "cta":"Get a fitness insurance quote"},

{"section":"business","slug":"garage-insurance","def_id":"garage",
 "eyebrow":"Commercial / Garage","svc":"Garage & Auto Repair Insurance","title":"Michigan Garage & Auto Repair Insurance",
 "meta":"Garage insurance for Michigan auto repair shops, body shops, and dealers — garagekeepers, garage liability, and commercial auto for the vehicles in your care.",
 "hero":"photo-1530046339160-ce3e530c7d2f","alt":"Auto repair shop — Michigan garage insurance",
 "lead":"When customers' vehicles are in your care, a standard business policy won't cover them. Michigan garage insurance combines garagekeepers, garage liability, and commercial auto so a fire, theft, or test-drive accident doesn't come out of your pocket.",
 "whatwedo":[("Garagekeepers coverage","covers customer vehicles in your care, custody, and control — the core exposure standard policies leave out."),
   ("Garage liability","premises and operations liability for the shop floor and the work you do."),
   ("Coverage for your operation","body shops, mechanical repair, tire and lube, towing, and dealerships each get the right form."),
   ("Multi-carrier shopping","we shop garage markets for the right mix of price and protection.")],
 "who_h":"Operations we cover","who":"Auto repair and mechanical shops, body and collision shops, tire and quick-lube shops, towing and recovery operators, used-car and franchised dealers, and detailers across Michigan.",
 "cov_h":"What garage insurance covers","cov":[("Garagekeepers","customer vehicles in your care against fire, theft, and damage."),
   ("Garage liability","third-party injury and property damage from operations."),
   ("Commercial auto","your service trucks, loaners, and tow vehicles."),
   ("Property and tools","your building, equipment, and shop tools."),
   ("Faulty work / completed operations","claims tied to repairs after the car leaves.")],
 "faqs":[("What is garagekeepers insurance?","It covers customers' vehicles while they're in your care, custody, and control — parked on your lot, in the shop, or on a test drive. A standard general liability or property policy won't pay for damage to a vehicle you don't own; garagekeepers is built for exactly that."),
   ("What insurance does an auto repair shop need in Michigan?","Typically garage liability, garagekeepers, commercial auto for service and tow vehicles, and property coverage for your building, equipment, and tools. Body shops and dealers add specific coverages. We assemble the right package for your operation."),
   ("Does garage insurance cover test drives?","Yes — garagekeepers and garage liability respond to incidents during legitimate test drives and while moving customer vehicles, subject to your policy terms. It's one of the gaps that makes garage-specific coverage essential."),
   ("How much does garage insurance cost in Michigan?","It depends on your services, payroll, location, and the value of vehicles in your care. Towing and dealerships are rated differently than a small repair shop. We shop multiple garage markets to find your best rate.")],
 "cta":"Get a garage insurance quote"},

{"section":"business","slug":"property-management-insurance","def_id":"property-management",
 "eyebrow":"Commercial / Property Management","svc":"Property Management Insurance","title":"Michigan Property Management & Landlord Insurance",
 "meta":"Insurance for Michigan property managers and rental-property owners — landlord (dwelling fire) policies, commercial property, premises liability, and management E&O.",
 "hero":"photo-1486406146926-c627a92ad1ab","alt":"Apartment buildings — Michigan property management insurance",
 "lead":"Whether you own a few rentals or manage hundreds of units, the right coverage protects the buildings, your liability as a landlord, and the management work itself. Michigan property-management insurance brings landlord, liability, and professional coverage together.",
 "whatwedo":[("Landlord / dwelling-fire policies","DP-1 or DP-3 coverage for single rentals and portfolios — built for tenant-occupied property, unlike a homeowners policy."),
   ("Multi-unit and commercial property","coverage for apartment buildings, mixed-use, and commercial space."),
   ("Premises and management liability","protection for tenant and visitor injury claims and for your management activities (E&O)."),
   ("Portfolio shopping","we shop carriers across your whole portfolio for the best combined program.")],
 "who_h":"Who we cover","who":"Rental-property owners, landlords, real-estate investors, and professional property-management companies handling residential, multi-unit, and commercial property across Michigan.",
 "cov_h":"What property-management insurance covers","cov":[("Landlord / dwelling property","the rental structure on a DP-1 or DP-3 form."),
   ("Loss of rents","lost rental income while a unit is uninhabitable after a covered loss."),
   ("Premises liability","tenant and visitor injury claims on the property."),
   ("Management E&O","professional liability for your management activities."),
   ("Commercial umbrella","extra liability limits across the portfolio.")],
 "faqs":[("Do I need landlord insurance for a rental property in Michigan?","Yes. A homeowners policy is for owner-occupied homes and can deny a claim on a tenant-occupied property. Landlord (dwelling fire) coverage is built for rentals — covering the building, loss of rents, and your liability as a landlord."),
   ("What's the difference between landlord and homeowners insurance?","Homeowners covers an owner-occupied home and the owner's belongings. Landlord insurance covers a rental's structure, lost rental income, and landlord liability — and excludes the tenant's personal property, which the tenant covers with renters insurance."),
   ("What insurance does a property-management company need?","Beyond the property coverage on the buildings, a management company needs general liability, management errors and omissions (E&O), and often a commercial umbrella. We coordinate coverage between owners and managers so nothing falls through the gap."),
   ("Can you insure a portfolio of rental properties?","Yes — we shop carriers that handle scheduled portfolios and can package multiple properties for better pricing and simpler management than insuring each separately.")],
 "cta":"Get a property management quote"},

{"section":"business","slug":"condo-association-insurance","def_id":"condo-association",
 "eyebrow":"Commercial / Condo Association","svc":"Condo Association Insurance","title":"Michigan Condo Association Insurance",
 "meta":"Master insurance for Michigan condo and homeowner associations — building and common-area property, association liability, and directors & officers (D&O) for the board.",
 "hero":"photo-1545324418-cc1a3fa10c00","alt":"Condominium building — Michigan condo association insurance",
 "lead":"A condo or homeowner association's master policy protects the buildings, the common areas, and the board itself — and how it's written determines what unit owners must cover. We help Michigan associations get the master policy right and keep it affordable.",
 "whatwedo":[("The right master form","all-in, bare-walls, or single-entity — we make sure the master policy matches your bylaws so there are no gaps with owners' HO-6 policies."),
   ("Association liability and D&O","premises liability plus directors and officers coverage protecting your board."),
   ("Accurate building valuations","correct replacement values to avoid coinsurance penalties at claim time."),
   ("Multi-carrier shopping","we compare association markets to control assessments and premium.")],
 "who_h":"Associations we cover","who":"Condominium associations, homeowner associations (HOAs), townhome and co-op associations, and their boards across Michigan.",
 "cov_h":"What an association master policy covers","cov":[("Building and common-area property","the structure and shared areas per your governing form."),
   ("General / premises liability","injury and damage claims in common areas."),
   ("Directors and officers (D&O)","claims against board members for their decisions."),
   ("Fidelity / crime","theft of association funds."),
   ("Umbrella","higher liability limits for the association.")],
 "faqs":[("What does a condo association master policy cover?","It covers the building structure and common areas, plus association liability and the board's D&O exposure. How it's written — all-in, bare-walls, or single-entity — determines whether it covers fixtures inside units or stops at the walls, which is what each owner's HO-6 policy then picks up."),
   ("What's the difference between all-in and bare-walls coverage?","An all-in master policy covers fixtures and improvements inside units; a bare-walls policy covers only the structure to the unfinished walls, leaving more for owners' HO-6 policies. We match the master form to your bylaws so coverage lines up."),
   ("Does the association need D&O insurance?","Yes — board members can be personally named in claims over their decisions (assessments, rules, vendor disputes). Directors and officers coverage defends and protects them, and it's considered essential for any association board."),
   ("How are association assessments affected by insurance?","If a covered loss exceeds the master policy, owners can be assessed for the shortfall. Getting the master limits and valuations right — and owners carrying loss-assessment coverage on their HO-6 — keeps surprise assessments down. We help on both sides.")],
 "cta":"Get a condo association quote"},

{"section":"business","slug":"church-insurance","def_id":"church",
 "eyebrow":"Commercial / Church","svc":"Church Insurance","title":"Michigan Church & Religious Organization Insurance",
 "meta":"Insurance for Michigan churches and religious organizations — property, liability, sexual misconduct, directors & officers, and clergy professional coverage.",
 "hero":"photo-1438032005730-c779502df39b","alt":"Church interior — Michigan church insurance",
 "lead":"Churches and religious organizations carry exposures most businesses never face — from the building and volunteers to abuse liability and the board's decisions. Michigan church insurance brings property, liability, and the specialized coverages a congregation needs into one program.",
 "whatwedo":[("Specialized church coverage","property and liability plus the sexual-misconduct, D&O, and clergy coverages a generic policy leaves out."),
   ("Volunteer and event protection","coverage for volunteers and the events your congregation hosts."),
   ("Right-sized for your congregation","whether you're a small church or a large ministry, we match coverage to your activities."),
   ("Multi-carrier shopping","we compare faith-based markets built for religious organizations.")],
 "who_h":"Organizations we cover","who":"Churches, temples, mosques, and synagogues, ministries and missions, religious schools and daycares, and faith-based nonprofits across Michigan.",
 "cov_h":"What church insurance covers","cov":[("Property","the building, contents, and religious property."),
   ("General / premises liability","injury and damage claims on church grounds and at events."),
   ("Sexual misconduct liability","abuse and molestation claims — a critical coverage."),
   ("Directors and officers (D&O)","claims against the board and leadership."),
   ("Clergy professional and volunteers","pastoral counseling exposure and volunteer coverage.")],
 "faqs":[("What insurance does a church need in Michigan?","A church typically needs property coverage for the building and contents, general liability, sexual misconduct/abuse liability, directors and officers (D&O) for the board, and coverage for volunteers and special events. Larger ministries add clergy professional liability and more. We build the program around your congregation."),
   ("Why do churches need sexual misconduct coverage?","Abuse and molestation claims are among the most serious a religious organization can face, and standard liability often excludes or sublimits them. Dedicated sexual-misconduct liability — with proper limits and risk-management support — is considered essential for any church."),
   ("Does church insurance cover volunteers and events?","Yes, when written correctly. Faith-based policies extend liability to volunteers acting on the church's behalf and to events the church hosts, and host liquor liability can be added for events that serve alcohol. We make sure these are included."),
   ("Do small congregations still need full coverage?","Yes — the exposures (injury, abuse, board liability) don't scale away with size, and a single uncovered claim can threaten a small church's existence. Coverage is sized and priced to the congregation, so it stays affordable.")],
 "cta":"Get a church insurance quote"},

{"section":"business","slug":"business-interruption-insurance","def_id":"business-interruption",
 "eyebrow":"Commercial / Business Interruption","svc":"Business Interruption Insurance","title":"Michigan Business Interruption Insurance",
 "meta":"Business interruption (business income) insurance for Michigan businesses — replaces lost revenue and pays ongoing expenses when a covered loss shuts you down.",
 "hero":"photo-1551836022-aadb801c60ae","alt":"Michigan business owner — business interruption insurance",
 "lead":"Insurance can rebuild your building after a fire — but what pays your staff, rent, and bills while you're closed for months? Business interruption coverage replaces the income and covers the expenses that keep a covered loss from ending your business for good.",
 "whatwedo":[("Replace lost income","coverage for the revenue you lose while operations are suspended after a covered property loss."),
   ("Cover ongoing expenses","payroll, rent, and fixed costs that don't stop just because you're closed."),
   ("Right restoration period","we set the coverage period to how long your business would actually take to recover."),
   ("Add extra expense","funds to operate from a temporary location and reopen faster.")],
 "who_h":"Who needs it","who":"Any Michigan business that depends on a physical location, equipment, or inventory to earn revenue — restaurants, retailers, manufacturers, offices, and service businesses. If a fire or storm would force you to close, you need it.",
 "cov_h":"What business interruption covers","cov":[("Lost net income","the profit you would have earned while shut down."),
   ("Continuing expenses","payroll, rent, loan payments, and fixed costs."),
   ("Extra expense","costs to operate temporarily and speed your reopening."),
   ("Civil authority","income loss when authorities block access after a nearby covered loss."),
   ("Restoration period","coverage through the time it takes to rebuild and reopen.")],
 "faqs":[("What is business interruption insurance?","Also called business income coverage, it replaces the revenue you lose and pays the expenses that continue — payroll, rent, fixed costs — when a covered property loss (like a fire) forces your business to suspend operations. It's what keeps a covered loss from becoming a permanent closure."),
   ("Is business interruption included in my property policy?","It's usually an add-on to commercial property or a BOP, not automatic — and it's one of the most overlooked coverages. We make sure it's included and that the limits and restoration period actually match how your business would recover."),
   ("Does business interruption cover pandemic shutdowns?","Generally no — most policies require direct physical loss or damage to trigger coverage, and many now specifically exclude viruses and pandemics. It's built for events like fire, storm, or equipment loss. We'll explain exactly what your policy does and doesn't respond to."),
   ("How much business interruption coverage do I need?","Enough to cover your lost profit plus continuing expenses for the realistic time it would take to rebuild and reopen — often longer than owners expect. We help you calculate it so you're not underinsured when it matters most.")],
 "cta":"Get a business interruption quote"},

{"section":"business","slug":"special-event-insurance","def_id":"special-event","blog":"special-event-insurance",
 "eyebrow":"Commercial / Special Event","svc":"Special Event Insurance","title":"Michigan Special Event Insurance",
 "meta":"One-day and short-term special event insurance for Michigan — weddings, festivals, fundraisers, and gatherings. Liability and host liquor coverage most venues require.",
 "hero":"photo-1505944357431-27579db47558","alt":"Event venue — Michigan special event insurance",
 "lead":"Most Michigan venues won't let you host without it, and it's more affordable than people expect. Special event insurance provides one-day or short-term liability coverage for weddings, festivals, fundraisers, and gatherings — including host liquor liability when you're serving alcohol.",
 "whatwedo":[("Fast, affordable coverage","one-day and short-term policies, often $100 to $200, usually issued same day."),
   ("Meet venue requirements","we provide the certificate of insurance your venue requires, listing them as additional insured."),
   ("Host liquor liability","protection when alcohol is served at your event."),
   ("Coverage for the event type","weddings, graduations, festivals, conferences, and fundraisers.")],
 "who_h":"Events we cover","who":"Weddings and receptions, graduation and milestone parties, festivals and community events, conferences and meetings, fundraisers and galas, and corporate events across Michigan.",
 "cov_h":"What special event insurance covers","cov":[("General liability","third-party injury or property damage at your event."),
   ("Host liquor liability","alcohol-related claims when you serve (not sell) alcohol."),
   ("Venue additional insured","satisfies the certificate your venue requires."),
   ("Property damage to the venue","damage to the rented space during your event."),
   ("Optional cancellation","add-on for non-refundable costs if the event is called off (varies).")],
 "faqs":[("Do I need event insurance for a wedding in Michigan?","Most Michigan venues now require it before they'll let you host, typically $1 million in liability with the venue named as additional insured. Even when it's optional, it protects you from liability for injuries or damage during the event. We issue it quickly with the certificate your venue needs."),
   ("What does special event insurance cost?","For most events, around $100 to $200 for general liability, with host liquor liability adding a modest amount when alcohol is served. Larger events with more guests or higher risk cost more. We can usually turn a quote and certificate around the same day."),
   ("What is host liquor liability?","If you're serving (not selling) alcohol at a private event, host liquor liability covers alcohol-related claims — such as a guest who's overserved and causes harm. It's a common add-on to event coverage and sometimes required by the venue."),
   ("How quickly can I get event insurance?","Usually the same day during business hours. Tell us the date, venue, guest count, and whether alcohol is served, and we'll get you a quote and the certificate your venue requires.")],
 "cta":"Get a special event quote"},

# ===================== NICHE PERSONAL =====================
{"section":"personal","slug":"atv-insurance","def_id":"atv-insurance",
 "eyebrow":"Personal / ATV & Powersport","svc":"ATV & Powersport Insurance","title":"Michigan ATV & Powersport Insurance",
 "meta":"ATV, side-by-side, and snowmobile insurance for Michigan — liability, physical damage, and theft coverage for the trails and private property your registration doesn't cover.",
 "hero":"photo-1676631284522-8007dd380171","alt":"Off-road riding — Michigan ATV and powersport insurance",
 "lead":"Michigan ATV registration includes only minimal coverage on state land — and none on private property or many trails. A real powersport policy covers your ATV, side-by-side, or snowmobile against accidents, theft, and the liability you carry off-road.",
 "whatwedo":[("Cover the gap registration leaves","registration's minimal coverage doesn't follow you to private property or every trail — a policy does."),
   ("Coverage for what you ride","ATVs, side-by-sides and UTVs, and snowmobiles, including accessories and custom parts."),
   ("Liability off-road","protection if you injure someone or damage property while riding."),
   ("Lay-up and multi-carrier shopping","seasonal savings plus comparison across powersport carriers.")],
 "who_h":"Vehicles we cover","who":"ATVs and quads, side-by-sides and UTVs, snowmobiles, and dual-sport off-road machines — for trail riding, hunting, and recreation across Michigan.",
 "cov_h":"What ATV & powersport insurance covers","cov":[("Liability","injury or property damage you cause while riding."),
   ("Physical damage","collision and comprehensive for your machine."),
   ("Theft","a leading cause of ATV and snowmobile loss."),
   ("Accessories and custom parts","plows, winches, and aftermarket equipment."),
   ("Medical payments","injuries to you and your riders.")],
 "faqs":[("Does Michigan ATV registration include insurance?","Only minimal coverage, and only on state-operated land — it doesn't extend to private property or many trails, and it won't replace your machine if it's stolen or wrecked. A separate ATV policy is strongly recommended for real protection."),
   ("Do I need insurance for a snowmobile or side-by-side in Michigan?","The state doesn't broadly mandate it, but lenders require coverage on financed machines, many trails and clubs expect liability coverage, and theft and injury risk make it well worth carrying. We write ATVs, side-by-sides, and snowmobiles."),
   ("Does my home or auto policy cover my ATV?","Generally not for off-premises use. Homeowners policies exclude most motorized off-road vehicles once they leave your property, and auto policies don't apply. A dedicated powersport policy is how you actually cover trail and off-property riding."),
   ("How much does ATV insurance cost in Michigan?","Often a modest annual premium depending on the machine's value, type, and how you use it — with seasonal lay-up lowering the cost for snowmobiles and summer-only riders. We shop powersport carriers to find your best rate.")],
 "cta":"Get an ATV insurance quote"},

{"section":"personal","slug":"mobile-home-insurance","def_id":"mobile-home-insurance",
 "eyebrow":"Personal / Mobile & Manufactured Home","svc":"Mobile & Manufactured Home Insurance","title":"Michigan Mobile & Manufactured Home Insurance",
 "meta":"Insurance for Michigan mobile and manufactured homes — single-wide, double-wide, and modular. Covers the structure, additions, and personal property at the right value.",
 "hero":"photo-1554774853-719586f82d77","alt":"Manufactured home — Michigan mobile home insurance",
 "lead":"Manufactured and mobile homes are built and rated differently than site-built houses — and a standard homeowners policy isn't the right fit. We write coverage designed for single-wides, double-wides, modular, and park-model homes across Michigan.",
 "whatwedo":[("Coverage built for your home","policies designed for manufactured housing, not a forced fit of a standard HO-3."),
   ("Cover the structure and additions","the home plus attached decks, carports, skirting, and add-ons."),
   ("Right replacement value","we set coverage so a total loss actually replaces the home."),
   ("Multi-carrier shopping","we compare manufactured-home markets for the best rate.")],
 "who_h":"Homes we cover","who":"Single-wide and double-wide mobile homes, manufactured and modular homes, and park-model and tiny homes — owner-occupied or in a community, across Michigan.",
 "cov_h":"What mobile home insurance covers","cov":[("Dwelling / structure","the home and attached structures like decks and carports."),
   ("Personal property","your furniture, electronics, and belongings."),
   ("Personal liability","injuries to others or damage you cause."),
   ("Loss of use","living costs if your home is uninhabitable after a covered loss."),
   ("Transit / setup (varies)","coverage options when a home is moved or sited.")],
 "faqs":[("Can I insure a mobile or manufactured home with a regular homeowners policy?","Usually not well — manufactured homes are constructed and rated differently and need a policy designed for them. We write coverage built specifically for single-wides, double-wides, modular, and park-model homes so the structure is valued and covered correctly."),
   ("What does mobile home insurance cover?","The home's structure and attached additions (decks, carports, skirting), your personal property, personal liability, and loss of use if the home becomes uninhabitable after a covered loss. Coverage options also exist for moving and setting up a home."),
   ("Does it matter if my manufactured home is single-wide or double-wide?","Yes — size, age, construction, and whether it's in a community all affect rating and available coverage. We match the policy and value to your specific home so you're neither under- nor over-insured."),
   ("How much does mobile home insurance cost in Michigan?","It depends on the home's value, age, location, and construction. Manufactured-home policies are often affordable relative to site-built homes. We shop multiple carriers to find your best combination of coverage and price.")],
 "cta":"Get a mobile home quote"},

{"section":"personal","slug":"specialty-dwelling-insurance","def_id":"specialty-dwelling",
 "eyebrow":"Personal / Specialty Dwelling","svc":"Specialty Dwelling Insurance","title":"Michigan Specialty Dwelling Insurance",
 "meta":"Specialty dwelling insurance for Michigan — vacation homes, seasonal cabins, rentals, and homes under renovation that don't fit a standard homeowners policy.",
 "hero":"photo-1720065609938-ec0e33ffd9ad","alt":"Michigan home — specialty dwelling insurance",
 "lead":"Not every property fits a standard HO-3. Vacation homes, seasonal cabins, rentals, and homes under renovation each carry exposures a regular homeowners policy won't cover. We match the right specialty form to your situation across Michigan.",
 "whatwedo":[("The right form for the property","vacation, seasonal, rental (DP-1/DP-3), or renovation — we place the form that actually fits."),
   ("Coverage for vacancy and seasonal use","handling the vacancy and occupancy issues that void standard policies."),
   ("Landlord and rental options","dwelling-fire coverage with loss of rents for rental property."),
   ("Multi-carrier shopping","we compare specialty markets for hard-to-place dwellings.")],
 "who_h":"Properties we cover","who":"Vacation and second homes, seasonal cabins and cottages, rental and tenant-occupied dwellings, homes under renovation or vacant, and other properties that don't fit a standard homeowners policy across Michigan.",
 "cov_h":"What specialty dwelling insurance covers","cov":[("Dwelling","the structure on the form that fits its use (HO-3, DP-1, or DP-3)."),
   ("Loss of rents","rental income lost while a rental is uninhabitable."),
   ("Liability","injury and damage claims tied to the property."),
   ("Vacancy / seasonal handling","coverage written for homes not occupied year-round."),
   ("Renovation / under-construction options","coverage during major work.")],
 "faqs":[("Why can't I use a regular homeowners policy for a vacation or rental home?","Standard homeowners policies assume an owner-occupied primary residence. A second home, seasonal cabin, rental, or vacant property carries different occupancy and vacancy risks that a standard HO-3 may exclude — which is why a specialty dwelling form is the right fit."),
   ("How do I insure a rental property in Michigan?","Tenant-occupied property is written on a dwelling-fire form (DP-1 or DP-3) that covers the structure, loss of rents, and landlord liability — not the tenant's belongings, which they cover with renters insurance. We place the right landlord coverage for your rental."),
   ("Can you insure a vacant home or one under renovation?","Yes — vacant and under-renovation homes need specialized coverage because standard policies often limit or exclude vacancy. We have markets for vacant dwellings and for homes undergoing major renovation, including builders risk where appropriate."),
   ("What about a seasonal cabin or cottage?","Seasonal and second homes are commonly written on specialty forms that account for the months they're unoccupied. We match coverage to how and when you use the property so a winter vacancy doesn't leave you exposed.")],
 "cta":"Get a specialty dwelling quote"},

{"section":"personal","slug":"high-net-worth-insurance","def_id":"high-net-worth",
 "eyebrow":"Personal / High Net Worth","svc":"High Net Worth Insurance","title":"Michigan High Net Worth Insurance",
 "meta":"High net worth insurance for Michigan — broader coverage, higher limits, agreed value, and concierge claims through carriers like Chubb, PURE, and Cincinnati Private Client.",
 "hero":"photo-1613490493576-7fde63acd811","alt":"Luxury home — Michigan high net worth insurance",
 "lead":"Significant assets need more than a standard policy. High net worth insurance brings broader coverage forms, much higher liability limits, agreed value on homes and valuables, and concierge claim service — through specialist carriers built for affluent Michigan families.",
 "whatwedo":[("Broader, higher-limit coverage","richer forms and liability limits than standard carriers offer, sized to your assets."),
   ("Agreed value and cash-out","guaranteed valuations on homes, art, jewelry, and collections — no depreciation surprises."),
   ("One coordinated program","home, auto, valuables, umbrella, and more under a single high-net-worth carrier with concierge service."),
   ("Specialist markets","we place coverage with Chubb, PURE, Cincinnati Private Client, and other HNW carriers.")],
 "who_h":"Who high net worth coverage fits","who":"Families with $1M+ in insurable assets, homes valued $750K and up, owners of significant jewelry, art, or wine collections, and anyone whose liability exposure exceeds what standard policies comfortably cover.",
 "cov_h":"What high net worth insurance covers","cov":[("High-value home","broader coverage with extended or guaranteed replacement cost."),
   ("Valuable articles","agreed-value coverage for jewelry, art, wine, and collectibles."),
   ("High-limit liability and umbrella","$5M to $100M+ in personal liability protection."),
   ("Auto and collector vehicles","richer coverage for premium and collector cars."),
   ("Concierge claims and risk service","white-glove claims handling and risk consulting.")],
 "faqs":[("What is high net worth insurance?","A coordinated program through specialist carriers (Chubb, PURE, Cincinnati Private Client, and others) built for affluent families. It offers broader coverage forms, much higher limits, agreed value on homes and valuables, generous liability and umbrella options, and concierge claim service that standard carriers don't provide."),
   ("When should I switch to a high net worth carrier?","Generally when your home is valued around $750K+, you have $1M+ in insurable assets, you own significant jewelry, art, or collections, or your liability exposure outgrows standard limits. The richer coverage and higher limits usually justify the move. We'll tell you honestly when it makes sense."),
   ("How is high net worth coverage different from a standard policy?","Beyond higher limits, HNW policies typically include guaranteed or extended replacement cost on the home, agreed value (no depreciation) on valuables, much broader liability and umbrella options, and personalized claim and risk service — features standard carriers can't match."),
   ("Can you bundle all my coverage with one HNW carrier?","Yes — that's the point. We place home, auto, valuable articles, umbrella, and collector vehicles together with a single high-net-worth carrier, giving you one coordinated program, simpler service, and a single concierge claims contact.")],
 "cta":"Get a high net worth quote"},
]

# ---- template ------------------------------------------------------------------
REL="../../"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def head(cfg):
    sec_name="Commercial Insurance" if cfg["section"]=="business" else "Personal Insurance"
    sec_url=f"{SITE}/{cfg['section']}/"
    url=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
    title_tag=f"{cfg['title']} | J. Jacobs"
    og_img=f"{SITE}/assets/img/og/{cfg['section']}-{cfg['slug']}.jpg"
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE}/"},
        {"@type":"ListItem","position":2,"name":sec_name,"item":sec_url},
        {"@type":"ListItem","position":3,"name":cfg["title"],"item":url}]}
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in cfg["faqs"]]}
    svc={"@context":"https://schema.org","@type":"Service","serviceType":cfg["svc"],"name":cfg["title"],
        "description":cfg["meta"],"provider":{"@type":"InsuranceAgency","name":"J. Jacobs & Associates Insurance",
        "telephone":"+1-248-693-6455","url":f"{SITE}/","address":{"@type":"PostalAddress","streetAddress":"4301 S. Baldwin Rd",
        "addressLocality":"Lake Orion","addressRegion":"MI","postalCode":"48359","addressCountry":"US"}},
        "areaServed":{"@type":"State","name":"Michigan"},"url":url}
    j=lambda o:json.dumps(o,ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title_tag)}</title>
<meta name="description" content="{esc(cfg['meta'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#1a3a5c">
<link rel="icon" type="image/svg+xml" href="{REL}assets/img/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title_tag)}">
<meta property="og:description" content="{esc(cfg['meta'])}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="J. Jacobs & Associates">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(cfg['title'])} | J. Jacobs">
<meta name="twitter:description" content="{esc(cfg['meta'])}">
<meta name="twitter:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{REL}assets/css/styles.css?v={VER}">
<script type="application/ld+json">
{j(bc)}
</script>
<script type="application/ld+json">
{j(faq)}
</script>
<script type="application/ld+json">
{j(svc)}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

UTIL=f"""<div class="utility-bar">
  <div class="container">
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg> 4301 S. Baldwin Rd, Lake Orion, MI 48359</span>
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z"/></svg> <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg> <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div>"""

def header():
    r=REL
    return f"""<header class="site-header">
  <div class="container">
    <a class="brand" href="{r}" aria-label="J. Jacobs and Associates Insurance home">
      <img class="brand-logo-img" src="{r}assets/img/logo.jpeg" alt="J. Jacobs and Associates Insurance">
    </a>
    <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary">
      <ul>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Our Agency</summary>
          <ul class="submenu">
            <li><a href="{r}about/">About Us</a></li>
            <li><a href="{r}team/">Our Team</a></li>
            <li><a href="{r}carriers/">Our Carriers</a></li>
            <li><a href="{r}reviews/">Reviews</a></li>
          </ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Products</summary>
          <ul class="submenu">
            <li><a href="{r}personal/">Personal Insurance</a></li>
            <li><a href="{r}personal/auto-insurance/">Auto Insurance</a></li>
            <li><a href="{r}personal/home-insurance/">Home Insurance</a></li>
            <li><a href="{r}personal/life-insurance/">Life Insurance</a></li>
            <li><a href="{r}business/">Commercial Insurance</a></li>
            <li><a href="{r}business/workers-compensation/">Workers Compensation</a></li>
          </ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Service</summary>
          <ul class="submenu">
            <li><a href="{r}service/">Service Center</a></li>
            <li><a href="{r}billing-claims/">Billing &amp; Claims</a></li>
          </ul></details></li>
        <li><a href="{r}blog/">Blog</a></li>
        <li><a href="{r}faq/">FAQ</a></li>
        <li><a href="{r}contact/">Contact</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a>
      <a class="btn btn-primary" href="{r}quotes/">Start a Quote</a>
    </div>
  </div>
</header>"""

def footer():
    r=REL
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-logo"><img src="{r}assets/img/logo.jpeg" alt="J. Jacobs and Associates"></div>
        <h4>J. Jacobs &amp; Associates</h4>
        <p>Family-owned independent insurance agency serving Michigan since 1981. We shop 20+ carriers so you don&rsquo;t have to.</p>
        <p style="margin-top:1rem;"><strong style="color:#fff;">4301 S. Baldwin Rd</strong><br>
          Lake Orion, Michigan 48359<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Insurance</h4><ul>
        <li><a href="{r}personal/">Personal Insurance</a></li>
        <li><a href="{r}personal/auto-insurance/">Auto Insurance</a></li>
        <li><a href="{r}personal/home-insurance/">Home Insurance</a></li>
        <li><a href="{r}personal/life-insurance/">Life Insurance</a></li>
        <li><a href="{r}business/">Commercial Insurance</a></li>
        <li><a href="{r}business/workers-compensation/">Workers Compensation</a></li>
      </ul></div>
      <div><h4>Agency</h4><ul>
        <li><a href="{r}about/">About Us</a></li>
        <li><a href="{r}team/">Our Team</a></li>
        <li><a href="{r}carriers/">Our Carriers</a></li>
        <li><a href="{r}reviews/">Reviews</a></li>
        <li><a href="{r}service/">Service Center</a></li>
        <li><a href="{r}billing-claims/">Billing &amp; Claims</a></li>
        <li><a href="{r}faq/">FAQ</a></li>
      </ul></div>
      <div><h4>Follow Us</h4>
        <div class="social-row">
          <a href="https://www.facebook.com/JacobsandAssociates/" aria-label="Facebook" rel="noopener" target="_blank">f</a>
          <a href="https://www.instagram.com/jjacobs_and_associates/" aria-label="Instagram" rel="noopener" target="_blank">IG</a>
          <a href="https://www.linkedin.com/in/joe-jacobs-7a354422/" aria-label="LinkedIn" rel="noopener" target="_blank">in</a>
        </div>
        <ul style="margin-top:1.25rem;">
          <li><a href="{r}contact/">Contact Us</a></li>
          <li><a href="{r}privacy-policy/">Privacy Policy</a></li>
          <li><a href="{r}accessibility/">Accessibility</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span>
      <span>Independent Insurance Agency · Lake Orion, Michigan</span>
    </div>
  </div>
</footer>
<script src="{r}assets/js/site.v2.js?v={VER}" defer></script>
</body>
</html>
"""

def body(cfg):
    sec_name="Commercial Insurance" if cfg["section"]=="business" else "Personal Insurance"
    trust = "20+ commercial carriers" if cfg["section"]=="business" else "20+ personal lines carriers"
    img=cfg["hero"]; src=f"{REL}assets/img/blog/{img}.avif"
    whatwedo="".join(f"<li><strong>{esc(b)}</strong> — {esc(rest)}</li>" for b,rest in cfg["whatwedo"])
    cov="".join(f"<li><strong>{esc(t)}</strong> — {esc(d)}</li>" for t,d in cfg["cov"])
    faqs="".join(f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-body"><p>{esc(a)}</p></div></details>\n' for q,a in cfg["faqs"])
    bloglink=""
    if cfg.get("blog"):
        bloglink=f'<p style="margin-top:1.25rem;">Related reading: <a href="{REL}blog/{cfg["blog"]}/">our Michigan {cfg["svc"].lower()} guide</a>.</p>'
    return f"""<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="{REL}">Home</a></li><li><a href="{REL}{cfg['section']}/">{sec_name}</a></li><li>{esc(cfg['title'])}</li></ol></div></nav><main id="main">

<section class="section page-hero">
  <div class="container" style="max-width:1000px;">
  <div class="page-hero-banner">
    <picture>
    <source srcset="{src}" type="image/avif">
    <img src="{src}" alt="{esc(cfg['alt'])}" loading="eager" fetchpriority="high" style="width:100%;height:100%;object-fit:cover;display:block;">
  </picture>
  </div>

    <span class="eyebrow">{esc(cfg['eyebrow'])}</span>
    <h1>{esc(cfg['title'])}</h1>
    <p class="lead">{esc(cfg['lead'])}</p>

    <div class="trust-band">
      <span class="trust-band-item"><span class="stars">★★★★★</span> 4.9 on Google</span>
      <span class="trust-band-item">Best of the Best &mdash; 8 years running <span class="sub">(2018&ndash;2025)</span></span>
      <span class="trust-band-item">{trust}</span>
      <span class="trust-band-item">Family-owned since 1981</span>
    </div>

    <h2>What we do for {esc(cfg['svc'].lower())} clients</h2>
    <ul>{whatwedo}</ul>

    <h2>{esc(cfg['who_h'])}</h2>
    <p>{esc(cfg['who'])}</p>

    <h2>{esc(cfg['cov_h'])}</h2>
    <ul>{cov}</ul>

    <h2>Common questions</h2>
    {faqs}
    {bloglink}

    <div class="callout">
      <h2>{esc(cfg['cta'])}</h2>
      <p>Tell us what you need and we'll shop your coverage across our markets. Most quotes back within one business day.</p>
      <a class="btn btn-primary btn-lg" href="{REL}quotes/">{esc(cfg['cta'])}</a>
    </div>
  </div>
</section>

</main>
"""

def build(cfg):
    return head(cfg)+UTIL+"\n"+header()+"\n"+body(cfg)+footer()

def generate():
    n=0
    for cfg in CONFIG:
        d=f"{cfg['section']}/{cfg['slug']}"
        out=f"{d}/index.html"
        if os.path.exists(out) and not FORCE: continue
        os.makedirs(d,exist_ok=True)
        html=build(cfg).rstrip("\x00")
        safe_write(out,html)
        n+=1; print(f"  {cfg['section']}/{cfg['slug']}/  <- {cfg['title']}")
    print(f"\nGenerated {n} product pages.")

def wire():
    # 1) Full-details link in overview definition blocks
    for section,ov in (("business","business/index.html"),("personal","personal/index.html")):
        t=open(ov,encoding="utf-8").read(); orig=t
        for cfg in CONFIG:
            if cfg["section"]!=section: continue
            page=f"../{section}/{cfg['slug']}/"
            did=cfg["def_id"]
            # find the product-definition block by id, add a Full details link if not present
            pat=re.compile(r'(<div class="product-definition" id="'+re.escape(did)+r'">.*?<div class="product-actions">)(.*?)(</div>)',re.S)
            m=pat.search(t)
            if m and "/"+section+"/"+cfg["slug"]+"/" not in m.group(2):
                newactions=f'<a class="btn btn-secondary btn-sm" href="{page}">Full details →</a> '+m.group(2)
                t=t[:m.start(2)]+newactions+t[m.end(2):]
        if t!=orig:
            safe_write(ov,t.rstrip("\x00")); print(f"  wired {ov}")
    # 2) sitemap
    sm="sitemap.xml"; t=open(sm,encoding="utf-8").read()
    add=""
    for cfg in CONFIG:
        loc=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
        if loc in t: continue
        add+=f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    if add:
        t=t.replace("</urlset>",add+"</urlset>"); safe_write(sm, t.rstrip("\x00")); print(f"  added {add.count('<url>')} sitemap entries")
    # 3) llms.txt
    lt="llms.txt"; t=open(lt,encoding="utf-8").read()
    add=""
    for cfg in CONFIG:
        u=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
        if u in t: continue
        add+=f"- {cfg['title']}: {u}\n"
    if add and "## Sitemap" in t:
        t=t.replace("## Sitemap","## More product pages\n"+add+"\n## Sitemap",1)
        safe_write(lt, t.rstrip("\x00")); print("  added llms.txt entries")

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "generate"
    (generate if mode=="generate" else wire)()
