"""Page content for J. Jacobs & Associates site."""

# ----------------------------------------------------------------------
# Shared schema snippets
# ----------------------------------------------------------------------
AGENCY_SCHEMA = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"InsuranceAgency","@id":"https://www.jjainsurance.com/#agency","name":"J. Jacobs & Associates Insurance","url":"https://www.jjainsurance.com/","telephone":"+1-248-693-6455","email":"Support@jjainsurance.com","priceRange":"$$","foundingDate":"1981","address":{"@type":"PostalAddress","streetAddress":"4301 S. Baldwin Rd","addressLocality":"Lake Orion","addressRegion":"MI","postalCode":"48359","addressCountry":"US"},"areaServed":{"@type":"State","name":"Michigan"},"sameAs":["https://www.facebook.com/JacobsandAssociates/","https://www.instagram.com/jjacobs_and_associates/","https://www.linkedin.com/in/joe-jacobs-7a354422/"]}
</script>'''


def faq_schema(qas):
    """Build a FAQPage JSON-LD from a list of (question, answer) tuples."""
    items = []
    for q, a in qas:
        a_clean = a.replace('"', '\\"').replace('\n', ' ')
        items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a_clean}"}}}}')
    return ('<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ','.join(items) + ']}\n</script>')


def faq_html(qas):
    """Render FAQ items as <details> elements."""
    out = []
    for q, a in qas:
        out.append(f'<details class="faq-item"><summary>{q}</summary><div class="faq-body"><p>{a}</p></div></details>')
    return '\n'.join(out)


# ----------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------
ABOUT_BODY = '''
<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">About our agency</span>
    <h1>Family-owned, independent, and built around Michigan since 1981</h1>
    <p class="lead">J. Jacobs &amp; Associates is an independent insurance agency in Lake Orion, Michigan, serving families and business owners across the state for more than four decades.</p>

    <h2>Our story</h2>
    <p>Jeff Jacobs founded the agency in 1981, building it into one of the top five agents in Michigan through the company he represented. In 2005, he left captive agency life to become an independent agent — giving his clients access to multiple insurance carriers and a better experience. In 2014, Jeff retired and his son <strong>Joseph Jacobs</strong> took over.</p>
    <p>Joseph has been in the insurance business since 2000. He holds a degree in Finance (with a minor in Computer Science) from the University of Michigan, and is licensed in Property, Casualty, Commercial, Annuities, and Life Insurance. Today, he leads a team of more than a dozen licensed agents and account managers, with combined experience spanning hundreds of years across every line of insurance.</p>

    <h2>Why independent matters</h2>
    <p>Captive agents (think State Farm, Allstate, Farmers) and direct carriers (GEICO, Progressive direct) only sell one company's products. We sell <strong>more than 50</strong> commercial lines carriers and 20+ personal lines carriers — so we shop your coverage every renewal and switch you when another carrier offers better value. You never have to call around or start over.</p>

    <ul class="checklist mt-2">
      <li><strong>Access to 20+ carriers</strong> — including Michigan-based insurers like Citizens, Frankenmuth, Wolverine Mutual, Michigan Millers, and AAA of Michigan, plus national A-rated carriers.</li>
      <li><strong>We re-shop at renewal</strong> — if your premium goes up, we re-quote across our markets so you don't have to call around.</li>
      <li><strong>One stop, every line</strong> — bundle your business, auto, home, and life coverage in one place for the best pricing.</li>
      <li><strong>Local, family-owned</strong> — a real Michigan agency answering a real Michigan phone.</li>
    </ul>

    <h2>What sets us apart</h2>
    <p>What separates one agent from another isn't the company logo on the door — it's their <em>knowledge</em> of insurance products and their <em>ability to proactively service</em> their clients. Our team includes designations like CPIA (Certified Professional Insurance Agent) and ARM (Associate in Risk Management), and most of our staff have been with us for years. We focus on educating you so you can make confident decisions — not just selling a policy.</p>

    <div class="callout mt-2">
      <h2>Ready for a real comparison?</h2>
      <p>We'll shop your coverage and show you exactly what we find — no obligation, no pressure.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# TEAM
# ----------------------------------------------------------------------
TEAM_MEMBERS = [
    ("Joseph Jacobs", "JJ", "Owner / President · CPIA", "jacobs31@jjainsurance.com",
     "Joseph has been in insurance since 2000 and has run the agency since 2014. He's fully licensed in Property, Casualty, Commercial, Annuities, and Life. Finance degree from the University of Michigan with a minor in Computer Science."),
    ("Jill Stockwell", "JS", "Personal Lines Manager · ARM", "jstockwell@jjainsurance.com",
     "Office manager of Personal Lines, 9+ years with the agency, 8 years P&C licensed. Bachelor's from MSU, ARM designation from Lawrence Tech. Previously Assistant Director of Risk Management at Wayne State."),
    ("Rachel Glover", "RG", "Commercial Director · Licensed Agent", "Rachel@jjainsurance.com",
     "Director of our commercial department. P&C licensed and our go-to expert for workers' compensation and guiding new businesses through insurance audits."),
    ("Todd Randall", "TR", "Licensed Agent · Personal Lines", "Sales@jjainsurance.com",
     "28 years in sales, 19 of them as an insurance agent. Trenton High School and Ferris State University alumnus."),
    ("Jacqueline Paquette", "JP", "Licensed Account Manager", "Support@jjainsurance.com",
     "30+ years of customer service experience. Licensed P&C agent. Albion College graduate (Sociology, Women's Studies, Public Policy)."),
    ("Henry Socha", "HS", "Licensed Agent · Personal Lines", "Sales@jjainsurance.com",
     "BS in Finance from Oakland University. Background as a registered broker-dealer brings strong financial perspective to insurance advice."),
    ("Bryan Newman", "BN", "Licensed Agent · Personal Lines", "Sales@jjainsurance.com",
     "Decade-plus of insurance experience. Started with Allstate in 2015, moved to independent in 2017. Associate's Degree in Business Administration plus mortgage banking background."),
    ("Dagmar Winborn", "DW", "Senior Account Manager", "Support@jjainsurance.com",
     "26 years in the insurance industry. Truly eats, sleeps, and breathes insurance — and that shows in client service."),
    ("Janna Kolodziejczak", "JK", "Senior Customer Service Rep", "Support@jjainsurance.com",
     "Licensed P&C since 2019. 30+ years of customer service and office administration. Bachelor's in Business Administration from Baker College."),
    ("Ron Waters", "RW", "Licensed Agent · Personal Lines", "Sales@jjainsurance.com",
     "Sales career across multiple industries, now back home in Rochester, Michigan serving his community. Known for making complex deals feel simple."),
    ("Britton Collier", "BC", "Licensed Account Manager", "Support@jjainsurance.com",
     "Over a decade across restaurant management, financial services, and insurance. Licensed in life, home, and auto."),
    ("Aimee VeCasey", "AV", "Licensed Account Manager", "Support@jjainsurance.com",
     "Three years in insurance plus retail management and mortgage underwriting background. MSU graduate (Psychology)."),
    ("Olivia Debus", "OD", "Licensed Account Manager", "Support@jjainsurance.com",
     "Marketing degree from Oakland University. Brings high energy and a hands-on approach to client relationships."),
    ("Jonah Webster", "JW", "Commercial Account Manager", "Commercial@jjainsurance.com",
     "U.S. Air Force veteran with six years of service. MBA and P&C licensed. Commercial Lines Account Manager since 2025."),
    ("Jozett Reibel", "JR", "Licensed Account Manager", "Support@jjainsurance.com", "Licensed account manager on our service team."),
    ("Melanie Cappell", "MC", "Licensed Account Manager", "Support@jjainsurance.com", "Licensed account manager on our service team."),
    ("Michele Stanifer", "MS", "Licensed Account Manager", "Support@jjainsurance.com", "Licensed account manager on our service team."),
    ("Kenyata Williams", "KW", "Licensed Account Manager", "Support@jjainsurance.com", "Licensed account manager on our service team."),
]

team_cards = ''.join([
    f'''<div class="team-card">
  <div class="avatar" aria-hidden="true">{initials}</div>
  <h3>{name}</h3>
  <div class="role">{role}</div>
  <p>{bio}</p>
  <a class="email" href="mailto:{email}">{email}</a>
</div>'''
    for name, initials, role, email, bio in TEAM_MEMBERS
])

TEAM_BODY = f'''
<section class="section">
  <div class="container">
    <span class="eyebrow">Our team</span>
    <h1>Meet the people behind your coverage</h1>
    <p class="lead" style="max-width:760px;">Our licensed agents and account managers bring hundreds of years of combined experience to every conversation. When you call J. Jacobs &amp; Associates, you get a real Michigan person who knows your file.</p>

    <div class="team-grid" style="margin-top:2.5rem;">
      {team_cards}
    </div>

    <div class="callout mt-2">
      <h2>Want to work with us?</h2>
      <p>Start a quote online or call us — we'd love to hear from you.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# CARRIERS
# ----------------------------------------------------------------------
CARRIERS = [
    "Auto-Owners Insurance", "Citizens Insurance", "Cincinnati Insurance", "Progressive",
    "Frankenmuth Insurance", "Foremost Insurance", "Liberty Mutual", "Wolverine Mutual",
    "Michigan Millers Mutual", "Accident Fund", "Hagerty Insurance", "American Modern",
    "AAA of Michigan", "The Hartford", "Hastings Mutual", "Safeco Insurance",
    "Travelers", "Nationwide", "EMC Insurance", "Pioneer State Mutual",
]

carrier_items = ''.join([f'<li class="carrier-pill">{c}</li>' for c in CARRIERS])

CARRIERS_BODY = f'''
<section class="section">
  <div class="container">
    <span class="eyebrow">Our markets</span>
    <h1>The carriers we work with</h1>
    <p class="lead" style="max-width:760px;">As an independent agency, we have access to <strong>20+ commercial lines carriers</strong> and <strong>20+ personal lines carriers</strong>. That means real choice, real competition for your business, and real savings.</p>

    <h2 class="mt-2">Featured carriers</h2>
    <ul class="carriers-list">{carrier_items}</ul>
    <p class="text-center" style="margin-top:1.5rem; color: var(--text-muted); font-size:.9rem;">Don't see your current carrier? We likely have access — just call us at <a href="tel:+12486936455">(248) 693-6455</a>.</p>

    <h2 class="mt-2">Why so many carriers?</h2>
    <p>Insurance pricing is a moving target. Carriers tighten or loosen underwriting, raise or drop rates, and re-evaluate territory risk on different schedules. The carrier that was cheapest for you three years ago is rarely still the cheapest today. With 20+ markets, we can almost always find someone willing to compete for your business — and that's how we keep your premium in check year after year.</p>

    <h2>Michigan-based and national A-rated</h2>
    <p>Many of our markets are Michigan-based companies (Citizens, Frankenmuth, Wolverine Mutual, Michigan Millers, AAA of Michigan) — keeping premium dollars in the state. We also have access to top-rated national carriers like The Hartford, Liberty Mutual, Progressive, and Travelers. Every carrier we work with is A-rated or better for financial strength.</p>

    <div class="callout">
      <h2>Let us shop your coverage</h2>
      <p>Tell us about your current policy and we'll compare it across our carriers — no obligation.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# REVIEWS
# ----------------------------------------------------------------------
REVIEWS_BODY = '''
<section class="section">
  <div class="container">
    <span class="eyebrow">5.0 stars · Real Google reviews</span>
    <h1>What our clients say</h1>
    <p class="lead" style="max-width:760px;">Our clients are the reason we've been in business for over four decades. Here's what some of them have shared.</p>

    <div class="grid grid-2" style="margin-top:2rem;">

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"I received great service from Todd! Not only did he help me save money on my home and car insurance policies, but he took the time to help me understand my coverage and advise me."</blockquote>
        <cite>Verified Google review</cite>
      </article>

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"Jacqueline Paquette is new to J. Jacobs — and like every member of their team, she does not disappoint. I have been a customer for 10 years and have always been satisfied with the service. Very reachable, knowledgeable, and respond in amazing time."</blockquote>
        <cite>Verified Google review</cite>
      </article>

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"I always get top notch care with J. Jacobs — that's why I've been with them over 25 years. They always make sure I get the best rates. Kudos to Amanda, she's the best!"</blockquote>
        <cite>Verified Google review</cite>
      </article>

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"A friend gave me J. Jacobs' phone number after I complained about the cost of my homeowners insurance. I'm so glad she did. Todd Randall got me homeowners and auto, and saved me a substantial amount of money. Definitely worth a call at renewal."</blockquote>
        <cite>Verified Google review</cite>
      </article>

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"Megan was amazing at making sure everything went smoothly with coverage for my first home. Easy to get in touch with and always responsive. She took a lot of stress off an overwhelming process. I recommended her to my coworkers."</blockquote>
        <cite>Verified Google review</cite>
      </article>

      <article class="review-card">
        <div class="stars" aria-label="5 of 5">★★★★★</div>
        <blockquote>"Professional, friendly, and they actually return phone calls. After being shuffled around by a big-name carrier for years, finding J. Jacobs has been a relief."</blockquote>
        <cite>Verified Google review</cite>
      </article>

    </div>

    <div class="callout mt-2">
      <h2>Leave us a review</h2>
      <p>Are you a current client? We'd love to hear about your experience on Google or Facebook.</p>
      <a class="btn btn-primary btn-lg" href="https://www.facebook.com/JacobsandAssociates/reviews/" target="_blank" rel="noopener">Review us on Facebook</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# PERSONAL INSURANCE
# ----------------------------------------------------------------------
PERSONAL_LINES = [
    "Auto Insurance", "Home Insurance", "Condo Insurance", "Renters Insurance",
    "Life Insurance", "Umbrella Insurance", "Boat &amp; Jet Ski Insurance",
    "Motorcycle Insurance", "RV Insurance", "ATV &amp; Powersport Insurance",
    "Collector Car Insurance", "Flood Insurance", "Mobile &amp; Manufactured Home",
    "Specialty Dwelling", "Pet Health Insurance", "High Net Worth Insurance",
]
personal_cards = ''.join([f'<a class="product-card" href="#"><span class="icon">✓</span>{p}</a>' for p in PERSONAL_LINES])

PERSONAL_FAQS = [
    ("How much auto insurance do I need in Michigan?",
     "Michigan requires minimum bodily injury limits of $50,000 per person / $100,000 per accident, $10,000 property damage liability, and Personal Injury Protection (PIP). Most independent agents recommend at least $250,000 / $500,000 limits — and PIP coverage levels depending on your health insurance situation. We walk every client through their Michigan No-Fault PIP options."),
    ("Should I bundle home and auto insurance?",
     "Usually, yes. Most carriers offer 10-25% multi-policy discounts when you bundle home and auto with the same company. The exception is when one line of business is heavily discounted at a different carrier — which is exactly why we shop both with multiple companies before recommending a bundle."),
    ("How is my home insurance premium calculated?",
     "Premiums are based on your home's replacement cost (not market value), construction type, roof age, location, claims history, coverage limits, and deductibles. Other factors include credit-based insurance score (in most states), distance to a fire hydrant, and risk features like pools or wood-burning stoves."),
    ("Do I need umbrella insurance?",
     "If you have assets to protect, kids who drive, a pool, a dog with a bite history, or anything that could lead to a liability lawsuit larger than your underlying auto or home limits — yes. A $1 million umbrella usually costs $200-400/year for most families and is one of the highest-value coverages in personal insurance."),
]

PERSONAL_BODY = f'''
<section class="section">
  <div class="container">
    <span class="eyebrow">Personal insurance</span>
    <h1>Personal &amp; family insurance in Michigan</h1>
    <p class="lead" style="max-width:760px;">At J. Jacobs &amp; Associates, we help individuals and families worry less about their insurance protection — so they can spend more time on the things that matter most. Our 20+ personal lines carriers let us shop your coverage and find a real fit.</p>

    <h2 class="mt-2">Coverage options</h2>
    <div class="grid grid-3" style="margin-top:1rem;">{personal_cards}</div>

    <h2 class="mt-2">Why work with us for personal insurance?</h2>
    <div class="grid grid-3" style="margin-top:1rem;">
      <div class="card">
        <h3>Fast turnaround</h3>
        <p>Most personal lines quotes are back to you the same day, with bindable coverage often within 24 hours.</p>
      </div>
      <div class="card">
        <h3>Proactive service</h3>
        <p>Premium goes up at renewal? We re-shop it. Need to add a teen driver or a new vehicle? One call.</p>
      </div>
      <div class="card">
        <h3>Carrier selection</h3>
        <p>20+ A-rated personal lines carriers means we can almost always find a better fit than a single direct carrier.</p>
      </div>
    </div>

    <h2 class="mt-2">Common questions</h2>
    {faq_html(PERSONAL_FAQS)}

    <div class="callout">
      <h2>Get a personal insurance quote</h2>
      <p>Takes 2 minutes online. We'll shop it across our markets and show you what we find.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# AUTO INSURANCE (sub-page)
# ----------------------------------------------------------------------
AUTO_FAQS = [
    ("What are the minimum auto insurance requirements in Michigan?",
     "Michigan requires Bodily Injury Liability of $50,000 per person and $100,000 per accident, Property Damage Liability of $10,000, and Personal Injury Protection (PIP). Since the 2020 No-Fault reform, drivers can also choose their PIP medical limit (from $50,000 up to unlimited) instead of being required to carry unlimited medical coverage."),
    ("How does Michigan No-Fault insurance work?",
     "Under Michigan No-Fault, if you're injured in an auto accident, your own auto insurance pays your medical bills and lost wages — regardless of who caused the crash. The 2020 reform let drivers choose PIP medical limits ($50K, $250K, $500K, or unlimited) based on what their health insurance covers. We walk every Michigan driver through that decision."),
    ("What auto insurance discounts can I get?",
     "Common discounts include multi-policy (bundling home/auto), multi-vehicle, good driver, good student (3.0 GPA or above), paid-in-full, paperless, anti-theft devices, mature driver, and continuous coverage. Some carriers also offer discounts for alumni associations, professional memberships (AARP, MEA, CPA, SAE), and home ownership."),
    ("How much auto insurance do I really need?",
     "Michigan minimums are not enough for most drivers. We typically recommend $250,000/$500,000 bodily injury limits at a minimum, paired with property damage limits high enough to cover replacement of a luxury vehicle. If you own a home or have meaningful savings, an umbrella policy on top is usually well worth it."),
    ("Will my auto insurance go up after an accident?",
     "Most likely, yes — especially for an at-fault accident or claim that exceeds a few thousand dollars. Surcharges typically stay on your policy for 3-5 years depending on the carrier and the incident. That said, the size of the increase varies wildly between carriers, which is exactly why having an independent agent helps after a claim."),
    ("Do I need rental car coverage?",
     "Rental reimbursement is typically $5-$10/month and covers a rental car while your vehicle is in the shop after a covered claim. For most families, it's worth it. If you have access to a second vehicle that can fill in, you can skip it."),
]

AUTO_BODY = f'''
<section class="section">
  <div class="container" style="max-width:1000px;">
    <span class="eyebrow">Personal insurance / Auto</span>
    <h1>Michigan Auto Insurance — Done Right</h1>
    <p class="lead">Michigan auto insurance is different. No-Fault rules, PIP choices, and one of the highest-premium markets in the country mean you need an agent who actually understands the state. We do.</p>

    <h2>What we cover</h2>
    <p>Our auto insurance markets include Auto-Owners, Progressive, Citizens, Frankenmuth, Liberty Mutual, AAA of Michigan, The Hartford, Hastings Mutual, and more. We write coverage for:</p>
    <ul>
      <li>Standard auto (sedans, SUVs, trucks)</li>
      <li>High-performance and luxury vehicles</li>
      <li>Teen drivers and SR-22 filings</li>
      <li>Collector cars and classics (Hagerty and others)</li>
      <li>Motorcycles, ATVs, and powersports</li>
      <li>RVs and motorhomes</li>
      <li>Boats, jet skis, and watercraft</li>
    </ul>

    <h2>Michigan No-Fault explained</h2>
    <p>Since the 2020 No-Fault reform, Michigan drivers can choose their <strong>PIP (Personal Injury Protection) medical limit</strong>. The options:</p>
    <ul>
      <li><strong>Unlimited PIP</strong> — the historical Michigan default. Covers all reasonable medical costs from a covered auto accident, for life.</li>
      <li><strong>$500,000 PIP</strong> — high coverage for most situations.</li>
      <li><strong>$250,000 PIP</strong> — middle ground.</li>
      <li><strong>$50,000 PIP</strong> — only available if you're enrolled in Medicaid.</li>
      <li><strong>PIP Opt-Out</strong> — only available if you have qualified health insurance (typically Medicare).</li>
    </ul>
    <p>The right choice depends on your health insurance, your assets, and your risk tolerance. We&rsquo;ll walk you through it — and the difference between picking the wrong tier and the right one can be hundreds of dollars in premium and millions of dollars in protection.</p>

    <h2>Common questions</h2>
    {faq_html(AUTO_FAQS)}

    <div class="callout">
      <h2>Get an auto insurance quote</h2>
      <p>Tell us about your vehicles and we'll shop your coverage across our Michigan auto carriers.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Auto Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# HOME INSURANCE (sub-page)
# ----------------------------------------------------------------------
HOME_FAQS = [
    ("How much home insurance do I need?",
     "Your home should be insured for its full replacement cost — what it would actually cost to rebuild from the ground up at today's labor and material prices, not what you paid for it or what it would sell for. We use carrier estimators that pull from your home's square footage, construction type, and features to calculate this accurately."),
    ("What does home insurance actually cover?",
     "A standard Michigan homeowners policy includes: Dwelling (Coverage A) — the structure itself; Other Structures (Coverage B) — detached garages, sheds, fences; Personal Property (Coverage C) — your stuff; Loss of Use (Coverage D) — living expenses if your home is unlivable after a claim; Personal Liability (Coverage E); and Medical Payments (Coverage F). Flood and earthquake are NOT included and require separate coverage."),
    ("Should I raise my home insurance deductible?",
     "Often, yes. Going from a $500 to a $1,000 or $2,500 deductible typically saves 10-25% on premium. The math works out for most homeowners who can absorb the higher deductible — assuming you don't file small claims that would have been better paid out of pocket anyway."),
    ("Why did my home insurance go up so much?",
     "In recent years, replacement cost inflation, severe weather losses, and reinsurance market shifts have driven double-digit increases across Michigan. Your individual rate is also affected by your claims history, the carrier's territory rating, and your roof age. The good news: not all carriers have raised rates equally — which is where shopping with us pays off."),
    ("Do I need flood insurance in Michigan?",
     "If you're in a FEMA-designated Special Flood Hazard Area or near a lake/river, almost certainly yes — and your mortgage company will likely require it. Even if you're not in a flood zone, flooding is the most common natural disaster in the U.S. and standard homeowners policies do NOT cover it. We write flood through the NFIP and private flood markets."),
]

HOME_BODY = f'''
<section class="section">
  <div class="container" style="max-width:1000px;">
    <span class="eyebrow">Personal insurance / Home</span>
    <h1>Michigan Home Insurance That Actually Protects You</h1>
    <p class="lead">Whether you own a starter home in Lake Orion, a lakefront cottage in northern Michigan, or a multi-family in metro Detroit, we'll shop your homeowners coverage across 20+ carriers to find the right protection at the right price.</p>

    <h2>What our home insurance covers</h2>
    <p>A J. Jacobs &amp; Associates homeowners policy is built around six core coverages:</p>
    <ul>
      <li><strong>Dwelling (Coverage A):</strong> Replacement cost of your home itself</li>
      <li><strong>Other Structures (Coverage B):</strong> Detached garages, sheds, fences, gazebos</li>
      <li><strong>Personal Property (Coverage C):</strong> Furniture, electronics, clothing, valuables</li>
      <li><strong>Loss of Use (Coverage D):</strong> Hotel, rental, and meal costs if your home is unlivable</li>
      <li><strong>Personal Liability (Coverage E):</strong> If someone is injured on your property or you cause damage elsewhere</li>
      <li><strong>Medical Payments (Coverage F):</strong> Smaller medical bills for guests injured on your property</li>
    </ul>

    <h2>Optional coverages worth considering</h2>
    <ul>
      <li><strong>Flood insurance</strong> (always separate — required in flood zones)</li>
      <li><strong>Sewer backup &amp; sump pump failure</strong> (commonly excluded but inexpensive to add)</li>
      <li><strong>Service line coverage</strong> (buried water, sewer, and electric lines)</li>
      <li><strong>Scheduled personal property</strong> (jewelry, art, firearms — covered for full appraised value)</li>
      <li><strong>Identity theft restoration</strong></li>
      <li><strong>Umbrella liability</strong> (an extra $1M+ on top of home and auto)</li>
    </ul>

    <h2>Common questions</h2>
    {faq_html(HOME_FAQS)}

    <div class="callout">
      <h2>Get a home insurance quote</h2>
      <p>Tell us about your home and we'll shop it across our Michigan markets — most quotes back same-day.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Home Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# LIFE INSURANCE
# ----------------------------------------------------------------------
LIFE_FAQS = [
    ("What's the difference between term and whole life insurance?",
     "Term life insurance covers you for a fixed period (10, 20, or 30 years) at a fixed premium. If you die during that period, your beneficiaries receive the death benefit. If you outlive it, the policy ends. Whole life lasts your entire life and includes a cash value component that grows over time, but costs significantly more per dollar of death benefit. Most people are better served by term life."),
    ("How much life insurance do I need?",
     "A common rule of thumb is 10-12x your annual income, but that's just a starting point. The actual number depends on: your debts (mortgage, student loans, credit cards), how many years of income replacement your family needs, future college costs for kids, your spouse's earning ability, and any existing coverage. We do a comprehensive needs analysis for every life client."),
    ("How is life insurance priced?",
     "The two biggest factors are your age and your health. Other factors: tobacco use, family medical history, occupation, hobbies (private pilots and SCUBA divers pay more), and the death benefit amount you select. The cheapest time to buy life insurance is today — premiums only go up with age."),
    ("Is life insurance worth it if I'm single with no kids?",
     "Probably not if no one depends on you financially — unless you have meaningful debt that someone has co-signed for, or you want to lock in low rates now to protect against future health issues. Buying a smaller term policy at age 25 in good health can be valuable even if you don't have dependents yet."),
]

LIFE_BODY = f'''
<section class="section">
  <div class="container" style="max-width:1000px;">
    <span class="eyebrow">Personal insurance / Life</span>
    <h1>Michigan Life Insurance — Simple, Honest, Affordable</h1>
    <p class="lead">Life insurance is one of the most cost-effective ways to protect the people who depend on you financially. We'll help you find the right policy at the right price.</p>

    <h2>Why life insurance matters</h2>
    <p>If you have a child, are married, or carry any kind of debt, purchasing life insurance is a no-brainer. The question isn't <em>whether</em> you need it — it's <em>how much</em> and <em>what kind</em>.</p>
    <p>Without coverage, your loved ones could face:</p>
    <ul>
      <li>Loss of your income</li>
      <li>Mortgage they can't afford alone</li>
      <li>College costs out of reach</li>
      <li>Federal estate and death taxes</li>
      <li>Final expenses (funerals average $7,000-15,000)</li>
    </ul>

    <h2>Term vs. whole life</h2>
    <p><strong>Term life</strong> is the workhorse of personal life insurance. You pick a coverage period (10, 20, or 30 years) and a death benefit, and you pay a fixed premium. Most healthy people in their 30s and 40s can secure $500,000-$1,000,000 of term coverage for $25-$60 per month.</p>
    <p><strong>Whole life</strong> covers you for life and builds cash value, but costs 5-15x what term costs for the same death benefit. It has a place — estate planning, lifetime guarantees for special-needs dependents, etc. — but most families are better served by term plus retirement savings.</p>

    <h2>Common questions</h2>
    {faq_html(LIFE_FAQS)}

    <div class="callout">
      <h2>Get a life insurance quote</h2>
      <p>The process is simple. Tell us a bit about you, and we'll come back with options across multiple carriers.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Life Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# BUSINESS / COMMERCIAL
# ----------------------------------------------------------------------
COMMERCIAL_LINES = [
    "General Liability", "Commercial Property", "Commercial Auto", "Business Owners Policy (BOP)",
    "Workers Compensation", "Professional Liability (E&O)", "Cyber Liability",
    "Commercial Umbrella", "Builders Risk", "Contractors Insurance",
    "Restaurant Insurance", "Cannabis Insurance", "Fitness &amp; Gym Insurance",
    "Garage &amp; Auto Repair", "Property Management", "Condo Association",
    "Church Insurance", "Bonds &amp; Surety", "Business Interruption",
    "One-Day Special Event",
]
commercial_cards = ''.join([f'<a class="product-card" href="#"><span class="icon">✓</span>{p}</a>' for p in COMMERCIAL_LINES])

BIZ_FAQS = [
    ("What insurance does my Michigan business need?",
     "At minimum, most Michigan businesses need General Liability and Workers Compensation (required by Michigan law for most businesses with 1+ employees). Beyond that, you'll likely want Commercial Property if you own equipment or inventory, Commercial Auto if you have business vehicles, Professional Liability if you give professional advice, and an Umbrella policy for catastrophic claims. We help every business owner figure out the right stack."),
    ("Do I need workers compensation insurance in Michigan?",
     "Yes — Michigan law requires workers compensation coverage for almost every employer. Specifically: any private employer with 1+ employees working 35+ hours per week for 13+ weeks per year, or 3+ employees at any one time. Sole proprietors, partners, and certain corporate officers can opt out, but coverage is required for any other employees."),
    ("How much does business insurance cost?",
     "It depends entirely on your industry, revenue, payroll, claims history, and location. A typical small office-based business might pay $500-$1,500/year for general liability. A restaurant or contractor will pay more. Workers compensation is rated per $100 of payroll and varies by job classification. We give every business a detailed quote across multiple carriers."),
    ("What is a Business Owners Policy (BOP)?",
     "A BOP bundles general liability, commercial property, and business interruption coverage into one policy at a lower price than buying each separately. Available to businesses that meet underwriting criteria (typically office-based, retail, light contracting, restaurants, and similar — high-risk industries usually need separate policies)."),
]

BIZ_BODY = f'''
<section class="section">
  <div class="container">
    <span class="eyebrow">Commercial insurance</span>
    <h1>Michigan Business &amp; Commercial Insurance</h1>
    <p class="lead" style="max-width:780px;">From sole proprietors to multi-location operations, we protect Michigan businesses across every industry. With access to <strong>20+ commercial carriers</strong>, we find coverage other agencies can't.</p>

    <h2 class="mt-2">Lines of commercial coverage</h2>
    <div class="grid grid-3" style="margin-top:1rem;">{commercial_cards}</div>

    <h2 class="mt-2">Industries we specialize in</h2>
    <div class="grid grid-3">
      <div class="card"><h3>Restaurants &amp; Hospitality</h3><p>Liquor liability, food spoilage, slip-and-fall exposure, employee dishonesty.</p></div>
      <div class="card"><h3>Contractors &amp; Trades</h3><p>General liability, tools &amp; equipment, builders risk, workers comp, commercial auto.</p></div>
      <div class="card"><h3>Cannabis</h3><p>Specialized markets for cultivators, processors, dispensaries, and ancillary businesses.</p></div>
      <div class="card"><h3>Fitness &amp; Gyms</h3><p>Liability for instructors, members, equipment, and group classes.</p></div>
      <div class="card"><h3>Property Management</h3><p>Multi-location commercial property, condo associations, rental dwellings.</p></div>
      <div class="card"><h3>Churches &amp; Nonprofits</h3><p>D&amp;O, sexual misconduct liability, property, special events, volunteer coverage.</p></div>
    </div>

    <h2 class="mt-2">Common questions</h2>
    {faq_html(BIZ_FAQS)}

    <div class="callout">
      <h2>Get a commercial insurance quote</h2>
      <p>Tell us about your business and we'll shop your coverage across our 20+ commercial markets.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Business Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# WORKERS COMP (sub-page)
# ----------------------------------------------------------------------
WC_FAQS = [
    ("Is workers compensation insurance required in Michigan?",
     "Yes, for almost every employer. Michigan law requires workers comp coverage for any private employer with one or more employees working 35+ hours per week for 13+ weeks per year, or three or more employees at any one time, full-time or part-time. Sole proprietors and partners can opt out, but their employees still need coverage."),
    ("How is workers comp premium calculated?",
     "Premium is calculated as a rate per $100 of payroll, multiplied by your experience modifier (Mod). Rates vary by job classification (an office worker is rated much lower than a roofer). New businesses start with a 1.0 Mod. As your claims history develops, your Mod adjusts up or down — making safety and claims management critical to long-term cost."),
    ("What does workers compensation cover?",
     "Medical care for work-related injuries and illnesses, wage replacement (typically 80% of after-tax wages, subject to state maximums), vocational rehabilitation, and survivor benefits if an employee dies from a work-related cause. It also protects you (the employer) from being sued by injured employees in most cases — the 'exclusive remedy' principle."),
    ("Can I get workers comp for myself as a business owner?",
     "Sole proprietors and partners are typically excluded from workers comp by default in Michigan but can elect to include themselves. Corporate officers are usually included by default but can elect out. LLC member treatment depends on tax election. We help every business owner make the right choice for their situation."),
    ("What's an experience modifier (Mod) and why does it matter?",
     "Your experience modifier compares your claims history to similar businesses in your classification. A Mod above 1.0 means you have more claims than average (and pay more). Below 1.0 means fewer claims (and you pay less). The same business can pay double the premium of a competitor with the same payroll because of Mod differences — managing claims and safety actively pays off for years."),
]

WC_BODY = f'''
<section class="section">
  <div class="container" style="max-width:1000px;">
    <span class="eyebrow">Commercial / Workers Comp</span>
    <h1>Michigan Workers Compensation Insurance</h1>
    <p class="lead">Workers comp is required for almost every Michigan business — and one of the easiest places to overpay if you don't have the right agent. We help you navigate classifications, Mods, audits, and claims to keep your premium right-sized.</p>

    <h2>What we do for workers comp clients</h2>
    <ul>
      <li><strong>Classification review</strong> — we make sure your employees are in the right NCCI classifications. Misclassification is the #1 reason businesses overpay.</li>
      <li><strong>Audit support</strong> — we walk you through your annual workers comp audit and dispute incorrect findings on your behalf.</li>
      <li><strong>Experience Mod management</strong> — we monitor your Mod and identify opportunities to dispute or close reserves on open claims.</li>
      <li><strong>Multi-carrier shopping</strong> — we have access to Accident Fund, Travelers, Frankenmuth, Hastings Mutual, EMC, Pioneer State Mutual, and more — including specialty markets for high-risk classes.</li>
    </ul>

    <h2>Industries we write</h2>
    <p>Construction and contractors, restaurants and hospitality, manufacturing, healthcare, professional services, retail, transportation, landscaping, cannabis operations, fitness centers, religious organizations, and most other Michigan business types.</p>

    <h2>Common questions</h2>
    {faq_html(WC_FAQS)}

    <div class="callout">
      <h2>Get a workers comp quote</h2>
      <p>Send us your payroll and classifications and we'll shop your coverage. Most quotes back within one business day.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Workers Comp Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# SERVICE CENTER
# ----------------------------------------------------------------------
SERVICE_BODY = '''
<section class="section">
  <div class="container">
    <span class="eyebrow">Service center</span>
    <h1>Customer service for current clients</h1>
    <p class="lead">Whether you need an ID card, a certificate of insurance, to file a claim, or just want to talk through your coverage, we're here to help.</p>

    <div class="grid grid-3" style="margin-top:2rem;">
      <a class="card" href="/contact/?topic=id-card" style="text-decoration:none; color:inherit;">
        <h3>Proof of Insurance</h3>
        <p>Need an ID card for your auto, boat, or motorcycle policy? Request it and we'll send it right over.</p>
      </a>
      <a class="card" href="/contact/?topic=certificate" style="text-decoration:none; color:inherit;">
        <h3>Certificate of Insurance</h3>
        <p>Need a COI for a business contract, landlord, or vendor? Send us the details and we'll issue it the same day.</p>
      </a>
      <a class="card" href="/contact/?topic=claim" style="text-decoration:none; color:inherit;">
        <h3>File or Discuss a Claim</h3>
        <p>Need to report a new claim or check on an existing one? We'll point you to your carrier's claim center and walk you through the process.</p>
      </a>
      <a class="card" href="/contact/?topic=billing" style="text-decoration:none; color:inherit;">
        <h3>Billing &amp; Payments</h3>
        <p>Pay your bill, set up autopay, or update payment info. Each carrier has its own portal — we'll point you to yours.</p>
      </a>
      <a class="card" href="/contact/?topic=policy-change" style="text-decoration:none; color:inherit;">
        <h3>Policy Changes</h3>
        <p>Adding a vehicle, dropping a driver, increasing coverage? Send us the change request and effective date.</p>
      </a>
      <a class="card" href="/contact/?topic=review" style="text-decoration:none; color:inherit;">
        <h3>Annual Account Review</h3>
        <p>Premiums went up? Life situation changed? Let's review your coverage together — usually 20-30 minutes.</p>
      </a>
    </div>

    <h2 class="mt-2">Or just call us</h2>
    <p>Sometimes it's faster. Our office answers the phone Monday-Friday, 9am-5pm. Call <a href="tel:+12486936455"><strong>(248) 693-6455</strong></a> and a real person will pick up.</p>

    <div class="callout">
      <h2>Not a client yet?</h2>
      <p>Get a free comparison quote and see what we'd save you.</p>
      <a class="btn btn-primary btn-lg" href="/quotes/">Start My Quote</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# QUOTE FORM
# ----------------------------------------------------------------------
# ⚠⚠⚠ STALE — DO NOT REGENERATE /quotes/ FROM THIS. ⚠⚠⚠
# The LIVE quotes/index.html is a large, hand-maintained multi-product intake
# form that posts to the al3-worker. This QUOTE_BODY is an OLD, divergent
# Formspree placeholder (action=YOUR_FORM_ID). Running `python _pages.py` with
# /quotes/ still in PAGES will OVERWRITE the live compliant form with this
# broken one — including reverting the A2P-compliant SMS consent text.
# Before any site rebuild: remove the /quotes/ entry from PAGES (or sync this
# body to the live file). Consent text below kept compliant as defense-in-depth.
QUOTE_BODY = '''
<section class="section">
  <div class="container" style="max-width:880px;">
    <span class="eyebrow">Start a quote</span>
    <h1>Get Your Free Insurance Quote</h1>
    <p class="lead">Tell us about you and we'll shop your coverage across our markets. A licensed agent will follow up within one business day with your options.</p>

    <form id="quote-form" class="form-wrap" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">

      <input type="hidden" name="_subject" value="New Quote Request — jjainsurance.com">
      <input type="hidden" name="_format" value="plain">
      <input type="hidden" name="_next" value="https://www.jjainsurance.com/quotes/?submitted=1">

      <fieldset>
        <legend>What would you like a quote for?</legend>
        <div class="checkbox-row"><input type="checkbox" id="line_auto" name="line_auto" value="Auto"><label for="line_auto">Auto Insurance</label></div>
        <div class="checkbox-row"><input type="checkbox" id="line_home" name="line_home" value="Home"><label for="line_home">Home / Condo / Renters Insurance</label></div>
        <div class="checkbox-row"><input type="checkbox" id="line_life" name="line_life" value="Life"><label for="line_life">Life Insurance</label></div>
        <div class="checkbox-row"><input type="checkbox" id="line_umbrella" name="line_umbrella" value="Umbrella"><label for="line_umbrella">Umbrella Insurance</label></div>
        <div class="checkbox-row"><input type="checkbox" id="line_recreational" name="line_recreational" value="Recreational"><label for="line_recreational">Boat / Motorcycle / RV / ATV</label></div>
        <div class="checkbox-row"><input type="checkbox" id="line_business" name="line_business" value="Business"><label for="line_business">Business / Commercial Insurance</label></div>
      </fieldset>

      <h2 style="margin-top:2rem;">Your info</h2>

      <div class="field-group">
        <div class="field">
          <label for="first_name">First name <span class="req">*</span></label>
          <input type="text" id="first_name" name="first_name" required>
        </div>
        <div class="field">
          <label for="last_name">Last name <span class="req">*</span></label>
          <input type="text" id="last_name" name="last_name" required>
        </div>
      </div>

      <div class="field-group">
        <div class="field">
          <label for="email">Email <span class="req">*</span></label>
          <input type="email" id="email" name="email" required>
        </div>
        <div class="field">
          <label for="phone">Phone <span class="req">*</span></label>
          <input type="tel" id="phone" name="phone" required>
        </div>
      </div>

      <div class="field-group">
        <div class="field">
          <label for="dob">Date of birth</label>
          <input type="date" id="dob" name="dob">
        </div>
        <div class="field">
          <label for="zip">ZIP code <span class="req">*</span></label>
          <input type="text" id="zip" name="zip" pattern="[0-9]{5}" required>
        </div>
      </div>

      <div class="field">
        <label for="current_carrier">Current insurance carrier</label>
        <input type="text" id="current_carrier" name="current_carrier" placeholder="e.g., Auto-Owners, State Farm, none">
      </div>

      <div class="field">
        <label for="renewal_date">Current policy renewal date</label>
        <input type="date" id="renewal_date" name="renewal_date">
      </div>

      <!-- Auto -->
      <div id="section-auto" style="display:none;">
        <h2 style="margin-top:1.5rem;">Auto details</h2>
        <div class="field">
          <label for="vehicles">Vehicles (year, make, model)</label>
          <textarea id="vehicles" name="vehicles" placeholder="e.g.,&#10;2022 Ford F-150&#10;2019 Honda CR-V"></textarea>
        </div>
        <div class="field">
          <label for="drivers">Drivers (name, DOB, license status)</label>
          <textarea id="drivers" name="drivers" placeholder="e.g.,&#10;John Smith, 1/15/1980, valid&#10;Jane Smith, 4/12/1982, valid"></textarea>
        </div>
        <div class="field">
          <label for="auto_coverage">Coverage level preference</label>
          <select id="auto_coverage" name="auto_coverage">
            <option value="">Select…</option>
            <option>Best coverage</option>
            <option>Better coverage</option>
            <option>Good coverage</option>
            <option>Liability only (PLPD)</option>
            <option>Not sure — recommend</option>
          </select>
        </div>
      </div>

      <!-- Home -->
      <div id="section-home" style="display:none;">
        <h2 style="margin-top:1.5rem;">Home details</h2>
        <div class="field">
          <label for="home_address">Property address</label>
          <input type="text" id="home_address" name="home_address" placeholder="Street, City, State, ZIP">
        </div>
        <div class="field-group">
          <div class="field"><label for="year_built">Year built</label><input type="number" id="year_built" name="year_built"></div>
          <div class="field"><label for="square_feet">Square footage</label><input type="number" id="square_feet" name="square_feet"></div>
        </div>
        <div class="field-group">
          <div class="field">
            <label for="home_type">Home type</label>
            <select id="home_type" name="home_type">
              <option value="">Select…</option>
              <option>Ranch (1 story)</option>
              <option>Colonial (2 story)</option>
              <option>1.5 story</option>
              <option>Tri-level</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field">
            <label for="siding">Siding</label>
            <select id="siding" name="siding">
              <option value="">Select…</option>
              <option>Vinyl</option>
              <option>Brick</option>
              <option>50/50 Brick &amp; Vinyl</option>
              <option>Wood</option>
              <option>Other</option>
            </select>
          </div>
        </div>
        <div class="field">
          <label for="home_extras">Anything else we should know?</label>
          <textarea id="home_extras" name="home_extras" placeholder="e.g., recently replaced roof, finished basement, swimming pool, wood-burning stove, dogs, claims history"></textarea>
        </div>
      </div>

      <!-- Life -->
      <div id="section-life" style="display:none;">
        <h2 style="margin-top:1.5rem;">Life details</h2>
        <div class="field-group">
          <div class="field">
            <label for="life_type">Coverage type</label>
            <select id="life_type" name="life_type">
              <option value="">Select…</option>
              <option>Term (10 years)</option>
              <option>Term (20 years)</option>
              <option>Term (30 years)</option>
              <option>Whole Life</option>
              <option>Not sure — recommend</option>
            </select>
          </div>
          <div class="field">
            <label for="life_amount">Coverage amount</label>
            <select id="life_amount" name="life_amount">
              <option value="">Select…</option>
              <option>$100,000</option>
              <option>$250,000</option>
              <option>$500,000</option>
              <option>$1,000,000</option>
              <option>$2,000,000+</option>
              <option>Not sure — recommend</option>
            </select>
          </div>
        </div>
        <div class="field">
          <label for="health">General health</label>
          <select id="health" name="health">
            <option value="">Select…</option>
            <option>Excellent</option>
            <option>Very good</option>
            <option>Good</option>
            <option>Average</option>
            <option>Below average</option>
          </select>
        </div>
        <div class="field">
          <label for="tobacco">Tobacco use in past 12 months?</label>
          <select id="tobacco" name="tobacco">
            <option value="">Select…</option>
            <option>No</option>
            <option>Yes</option>
          </select>
        </div>
      </div>

      <!-- Business -->
      <div id="section-business" style="display:none;">
        <h2 style="margin-top:1.5rem;">Business details</h2>
        <div class="field"><label for="business_name">Business name</label><input type="text" id="business_name" name="business_name"></div>
        <div class="field"><label for="business_type">What does the business do?</label><textarea id="business_type" name="business_type" placeholder="e.g., HVAC contractor, restaurant, software consulting"></textarea></div>
        <div class="field-group">
          <div class="field"><label for="annual_revenue">Annual revenue</label><input type="text" id="annual_revenue" name="annual_revenue" placeholder="e.g., $500,000"></div>
          <div class="field"><label for="annual_payroll">Annual payroll</label><input type="text" id="annual_payroll" name="annual_payroll" placeholder="e.g., $200,000"></div>
        </div>
        <div class="field">
          <label for="business_lines">Coverages needed (check current policy)</label>
          <textarea id="business_lines" name="business_lines" placeholder="e.g., General Liability, Workers Comp, Commercial Property, Commercial Auto"></textarea>
        </div>
      </div>

      <h2 style="margin-top:1.5rem;">Anything else?</h2>
      <div class="field">
        <label for="comments">Comments or questions</label>
        <textarea id="comments" name="comments"></textarea>
      </div>

      <div class="field">
        <label for="referrer">How did you hear about us?</label>
        <select id="referrer" name="referrer">
          <option value="">Select…</option>
          <option>Customer referral</option>
          <option>Google search</option>
          <option>Google ad</option>
          <option>Facebook</option>
          <option>Instagram</option>
          <option>Mailer / flyer</option>
          <option>Newspaper</option>
          <option>Other</option>
        </select>
      </div>

      <div class="consent-notice">
        <label class="checkbox-row">
          <input type="checkbox" name="consent" required>
          <span><strong>Required:</strong> I agree to receive SMS text messages, calls, and emails from J. Jacobs &amp; Associates Insurance about my quote request and policies at the phone number and email I provide. Message frequency varies; message &amp; data rates may apply. Reply STOP to opt out or HELP for help. My mobile information will not be shared with or sold to third parties. See our <a href="/sms-terms/" target="_blank" rel="noopener">SMS Terms</a> and <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>.</span>
        </label>
      </div>

      <button class="btn btn-primary btn-lg btn-block" type="submit">Submit Quote Request</button>
    </form>

    <p class="text-center" style="margin-top:1rem; color:var(--text-muted); font-size:.9rem;">
      Prefer to call? Reach us at <a href="tel:+12486936455"><strong>(248) 693-6455</strong></a> Monday-Friday, 9am-5pm.
    </p>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------------
CONTACT_BODY = '''
<section class="section">
  <div class="container">
    <div class="grid grid-2">

      <div>
        <span class="eyebrow">Contact us</span>
        <h1>How can we help?</h1>
        <p class="lead">Have a question, need policy support, or want to leave a message? Send it our way.</p>

        <h2 class="mt-2">Office</h2>
        <p><strong>J. Jacobs &amp; Associates</strong><br>
        4301 S. Baldwin Rd<br>
        Lake Orion, Michigan 48359</p>

        <p><strong>Phone:</strong> <a href="tel:+12486936455">(248) 693-6455</a><br>
        <strong>Email:</strong> <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a><br>
        <strong>Hours:</strong> Monday-Friday, 9am-5pm</p>

        <p><a class="btn btn-outline" href="https://maps.google.com/maps?daddr=4301+S.+Baldwin+Rd+Lake+Orion+MI+48359" target="_blank" rel="noopener">Get Directions</a></p>

        <h2 class="mt-2">Looking for a quote?</h2>
        <p>If you're looking for new insurance, our quote form has all the right questions. <a href="/quotes/">Start a quote here →</a></p>
      </div>

      <div>
        <form class="form-wrap" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
          <input type="hidden" name="_subject" value="New Contact Form Submission — jjainsurance.com">

          <div class="field">
            <label for="c_topic">What's this about? <span class="req">*</span></label>
            <select id="c_topic" name="topic" required>
              <option value="">Select…</option>
              <option>General question</option>
              <option>ID card request</option>
              <option>Certificate of insurance</option>
              <option>Policy change</option>
              <option>File or discuss a claim</option>
              <option>Account review</option>
              <option>Billing question</option>
              <option>Other</option>
            </select>
          </div>

          <div class="field">
            <label for="c_client">Are you a current client?</label>
            <select id="c_client" name="current_client">
              <option>Yes</option>
              <option>No</option>
            </select>
          </div>

          <div class="field-group">
            <div class="field"><label for="c_first">First name <span class="req">*</span></label><input type="text" id="c_first" name="first_name" required></div>
            <div class="field"><label for="c_last">Last name <span class="req">*</span></label><input type="text" id="c_last" name="last_name" required></div>
          </div>

          <div class="field-group">
            <div class="field"><label for="c_email">Email <span class="req">*</span></label><input type="email" id="c_email" name="email" required></div>
            <div class="field"><label for="c_phone">Phone <span class="req">*</span></label><input type="tel" id="c_phone" name="phone" required></div>
          </div>

          <div class="field">
            <label for="c_policy">Policy number(s) — if applicable</label>
            <input type="text" id="c_policy" name="policy_number">
          </div>

          <div class="field">
            <label for="c_message">How can we help? <span class="req">*</span></label>
            <textarea id="c_message" name="message" required></textarea>
          </div>

          <div class="consent-notice">
            <label class="checkbox-row">
              <input type="checkbox" name="consent" required>
              <span><strong>Required:</strong> I agree to receive SMS text messages, calls, and emails from J. Jacobs &amp; Associates Insurance about my request and policies at the phone number and email I provide. Message frequency varies; message &amp; data rates may apply. Reply STOP to opt out or HELP for help. My mobile information will not be shared with or sold to third parties. See our <a href="/sms-terms/" target="_blank" rel="noopener">SMS Terms</a> and <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>.</span>
            </label>
          </div>

          <button class="btn btn-primary btn-block" type="submit">Send Message</button>
        </form>
      </div>

    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# FAQ
# ----------------------------------------------------------------------
MAIN_FAQS = [
    ("What is an independent insurance agency?",
     "An independent insurance agency represents many different insurance carriers rather than selling for just one. We can compare quotes from 20+ companies and choose the best fit for each client, whereas a captive agent (like State Farm or Allstate) can only sell their one company's products."),
    ("Where is J. Jacobs and Associates located?",
     "Our office is at 4301 S. Baldwin Rd, Lake Orion, Michigan 48359. We're licensed throughout the state of Michigan and serve clients from across the state."),
    ("How long has J. Jacobs and Associates been in business?",
     "We've been family-owned and operated since 1981. Founder Jeff Jacobs started the agency, and his son Joseph Jacobs has run it since 2014."),
    ("What types of insurance do you offer?",
     "We write Personal Lines: auto, home, condo, renters, life, umbrella, boat, motorcycle, RV, ATV, collector car, flood, mobile home, pet, high net worth. And Commercial Lines: general liability, commercial property, commercial auto, workers compensation, BOP, professional liability, restaurant, cannabis, fitness, contractors, builders risk, bonds, cyber liability, and more."),
    ("How does the quote process work?",
     "Step 1: Fill out our online quote form (takes 2-15 minutes depending on detail). Step 2: We shop your coverage across our markets — typically 4-20+ carriers for personal lines, more for commercial. Step 3: A licensed agent reviews the options with you, you pick what you like, and we bind coverage. The entire process can be same-day for simple personal lines and 1-2 weeks for complex commercial accounts."),
    ("Do you serve clients outside of Lake Orion?",
     "Yes, throughout the entire state of Michigan. While our office is in Lake Orion (Oakland County), most of our work is done by phone, email, and online. We have clients in metro Detroit, Grand Rapids, Lansing, Traverse City, the Upper Peninsula, and everywhere in between."),
    ("What carriers do you work with?",
     "Our personal lines carriers include Auto-Owners, Citizens, Cincinnati Insurance, Progressive, Frankenmuth, Foremost, Liberty Mutual, Wolverine Mutual, Michigan Millers Mutual, Hagerty, American Modern, AAA of Michigan, The Hartford, Hastings Mutual, and Safeco. Our commercial markets include Accident Fund, Travelers, EMC, Pioneer State Mutual, Cincinnati, Frankenmuth, Hastings, and 40+ others. See our full carrier list."),
    ("Why might my insurance be going up?",
     "In recent years, broad market increases have hit Michigan due to: rising replacement costs (labor and materials), severe weather losses, reinsurance market pressure, and tightened underwriting. Your individual rate is also affected by your claims history, credit-based insurance score, neighborhood loss trends, and roof age (for home). The good news: not all carriers raise rates at the same time — we'll re-shop yours."),
    ("How does Michigan No-Fault auto insurance work?",
     "Under Michigan No-Fault, if you're injured in an auto accident, your own auto insurance pays your medical bills and lost wages regardless of who caused the crash. Since the 2020 reform, drivers can choose their PIP medical coverage level — from $50,000 up to unlimited — based on what their health insurance covers."),
    ("Do I need flood insurance?",
     "If you're in a FEMA Special Flood Hazard Area, your mortgage lender will require it. Even if you're not in a designated flood zone, flooding is the most common natural disaster in the U.S. — and standard homeowners policies do not cover it. We write flood through the NFIP and through private flood markets."),
    ("Is workers compensation required for my business in Michigan?",
     "Yes, for almost every Michigan employer. Specifically: any private employer with one or more employees working 35+ hours per week for 13+ weeks per year, or three or more employees at any one time. Sole proprietors and partners can opt out, but employees still need coverage."),
    ("How do I file an insurance claim?",
     "Each carrier has its own claim center. The fastest way is usually their 1-800 claims line, listed in your policy documents. If you're a current J. Jacobs client and you're not sure where to start, call us at (248) 693-6455 — we'll walk you through it and stay involved through the claim."),
    ("Can I bundle home and auto for a discount?",
     "Almost always, yes. Multi-policy discounts range from 10-25% depending on carrier and state. We almost always quote both lines together and compare bundled vs. separate pricing across our markets."),
    ("How do I cancel my existing insurance policy?",
     "Once we bind your new coverage, we coordinate with your previous carrier to cancel — usually backdated to your new policy's effective date so you don't pay double. You don't need to do anything yourself; we handle it."),
    ("Do you offer payment plans?",
     "Yes. Most carriers offer monthly, quarterly, semi-annual, and annual payment options. Many also offer paid-in-full and autopay discounts (typically 5-10% off). We'll set up whatever billing frequency works for you."),
]

FAQ_BODY = f'''
<section class="section">
  <div class="container" style="max-width:900px;">
    <span class="eyebrow">FAQ</span>
    <h1>Insurance questions, answered</h1>
    <p class="lead">Common questions we hear from Michigan families and business owners. Have one we didn't answer? <a href="/contact/">Send us a note</a> or call <a href="tel:+12486936455">(248) 693-6455</a>.</p>

    <div class="mt-2">{faq_html(MAIN_FAQS)}</div>

    <div class="callout">
      <h2>Have a different question?</h2>
      <p>Real Michigan agents, real answers. Reach out and we'll help.</p>
      <a class="btn btn-primary" href="/contact/">Contact Us</a>
      <a class="btn btn-outline" href="tel:+12486936455" style="color:#fff;border-color:#fff;margin-left:.5rem;">Call (248) 693-6455</a>
    </div>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# PRIVACY POLICY
# ----------------------------------------------------------------------
PRIVACY_BODY = '''
<section class="section">
  <div class="container" style="max-width:820px;">
    <h1>Privacy Policy</h1>
    <p><em>Last updated: 2026</em></p>

    <p>J. Jacobs &amp; Associates ("we", "our", "us") respects your privacy. This policy describes how we collect, use, and protect information you provide through this website and through your insurance relationship with our agency.</p>

    <h2>Information we collect</h2>
    <p>We collect information you provide directly to us, including: name, contact information (address, phone, email), date of birth, vehicle and driver information, property information, business details, current insurance information, and any other information you provide on quote and contact forms or in correspondence with our team.</p>

    <p>We also receive insurance-related information from carriers and third-party data providers used to underwrite and price your coverage (motor vehicle reports, consumer credit-based insurance scores, claims history reports, and similar).</p>

    <h2>How we use information</h2>
    <p>We use your information to: provide insurance quotes and bind coverage on your behalf; service your existing policies; communicate with you about your account, claims, and renewals; and comply with applicable laws and regulations governing insurance.</p>

    <h2>Sharing of information</h2>
    <p>We share information with insurance carriers we're shopping or placing your business with, as needed for quoting, underwriting, and policy administration. We may also share information with service providers who help us operate (rating tools, agency management systems, email and form providers), and where required by law.</p>

    <p><strong>We do not sell your personal information.</strong></p>

    <h2>Cookies &amp; analytics</h2>
    <p>This website may use cookies for basic site functionality and anonymous traffic analytics. You can disable cookies in your browser settings.</p>

    <h2>SMS &amp; email communications</h2>
    <p>When you submit a form on this site, you may consent to receive SMS, phone, and email communications from our agency related to your request. You may unsubscribe at any time by replying STOP to SMS messages, clicking the unsubscribe link in emails, or contacting us at <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a>.</p>

    <h2>Your choices</h2>
    <p>You may request a copy of the information we have about you, ask us to correct inaccurate information, or request deletion (subject to legal and contractual record-retention requirements). Contact us at <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a> with any privacy-related request.</p>

    <h2>Contact us about privacy</h2>
    <p>J. Jacobs &amp; Associates<br>
    4301 S. Baldwin Rd<br>
    Lake Orion, Michigan 48359<br>
    <a href="tel:+12486936455">(248) 693-6455</a><br>
    <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a></p>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# ACCESSIBILITY
# ----------------------------------------------------------------------
ACCESSIBILITY_BODY = '''
<section class="section">
  <div class="container" style="max-width:820px;">
    <h1>Accessibility Statement</h1>
    <p>J. Jacobs &amp; Associates is committed to making our website accessible to all visitors, including those with disabilities.</p>

    <h2>Standards we aim to meet</h2>
    <p>We strive to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA. We use semantic HTML, ARIA attributes where appropriate, sufficient color contrast, keyboard-navigable navigation, alt text on images, and form labels.</p>

    <h2>Need help accessing our content?</h2>
    <p>If you encounter any accessibility barriers on this site or need information in an alternative format, please contact us:</p>
    <p>
      Phone: <a href="tel:+12486936455">(248) 693-6455</a><br>
      Email: <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a>
    </p>
    <p>We're happy to provide information by phone, mail, or in person at our Lake Orion office.</p>

    <h2>Ongoing improvement</h2>
    <p>Accessibility is an ongoing effort. We review our site periodically and welcome feedback to help us improve.</p>
  </div>
</section>
'''


# ----------------------------------------------------------------------
# PAGE LIST
# ----------------------------------------------------------------------
PAGES = [
    {
        "path": "/about/",
        "title": "About Us | J. Jacobs & Associates Insurance | Lake Orion, MI",
        "description": "Family-owned independent insurance agency in Lake Orion, Michigan since 1981. Learn about our story, our founders, and why being independent matters.",
        "body": ABOUT_BODY,
        "breadcrumb_items": [("Home", "/"), ("About", "/about/")],
        "extra_schema": AGENCY_SCHEMA,
    },
    {
        "path": "/team/",
        "title": "Our Team | J. Jacobs & Associates Insurance",
        "description": "Meet the licensed agents and account managers at J. Jacobs & Associates Insurance. Experienced Michigan insurance professionals serving you since 1981.",
        "body": TEAM_BODY,
        "breadcrumb_items": [("Home", "/"), ("Our Agency", "/about/"), ("Team", "/team/")],
    },
    {
        "path": "/carriers/",
        "title": "Our Insurance Carriers | J. Jacobs & Associates",
        "description": "We work with 50+ commercial and 20+ personal lines insurance carriers — including Citizens, Auto-Owners, Frankenmuth, Progressive, Liberty Mutual, AAA of Michigan, and more.",
        "body": CARRIERS_BODY,
        "breadcrumb_items": [("Home", "/"), ("Our Agency", "/about/"), ("Carriers", "/carriers/")],
    },
    {
        "path": "/reviews/",
        "title": "Client Reviews | J. Jacobs & Associates Insurance",
        "description": "Read 5-star reviews from J. Jacobs & Associates Insurance clients across Michigan. Real reviews from real Lake Orion families and business owners.",
        "body": REVIEWS_BODY,
        "breadcrumb_items": [("Home", "/"), ("Our Agency", "/about/"), ("Reviews", "/reviews/")],
    },
    {
        "path": "/personal/",
        "title": "Personal Insurance in Michigan | Auto, Home, Life | J. Jacobs",
        "description": "Personal insurance for Michigan families: auto, home, life, umbrella, boat, motorcycle, RV, condo, renters, and more. We shop 20+ personal lines carriers.",
        "body": PERSONAL_BODY,
        "breadcrumb_items": [("Home", "/"), ("Personal Insurance", "/personal/")],
        "extra_schema": faq_schema(PERSONAL_FAQS),
    },
    {
        "path": "/personal/auto-insurance/",
        "title": "Michigan Auto Insurance | J. Jacobs & Associates",
        "description": "Michigan auto insurance done right. We shop 20+ carriers, explain No-Fault PIP options, and find the best coverage for Michigan drivers. Call (248) 693-6455.",
        "body": AUTO_BODY,
        "breadcrumb_items": [("Home", "/"), ("Personal Insurance", "/personal/"), ("Auto Insurance", "/personal/auto-insurance/")],
        "extra_schema": faq_schema(AUTO_FAQS),
    },
    {
        "path": "/personal/home-insurance/",
        "title": "Michigan Home Insurance | J. Jacobs & Associates",
        "description": "Michigan home insurance from an independent agency that shops 20+ carriers. Real protection, real prices, real Michigan agents. Get a quote in minutes.",
        "body": HOME_BODY,
        "breadcrumb_items": [("Home", "/"), ("Personal Insurance", "/personal/"), ("Home Insurance", "/personal/home-insurance/")],
        "extra_schema": faq_schema(HOME_FAQS),
    },
    {
        "path": "/personal/life-insurance/",
        "title": "Michigan Life Insurance | Term & Whole Life | J. Jacobs",
        "description": "Term and whole life insurance for Michigan families. We shop multiple carriers to find the right coverage at the right price. Free quote in minutes.",
        "body": LIFE_BODY,
        "breadcrumb_items": [("Home", "/"), ("Personal Insurance", "/personal/"), ("Life Insurance", "/personal/life-insurance/")],
        "extra_schema": faq_schema(LIFE_FAQS),
    },
    {
        "path": "/business/",
        "title": "Michigan Business & Commercial Insurance | J. Jacobs",
        "description": "Commercial insurance for Michigan businesses. 20+ carriers for general liability, commercial property, workers comp, restaurants, contractors, cannabis, and more.",
        "body": BIZ_BODY,
        "breadcrumb_items": [("Home", "/"), ("Commercial Insurance", "/business/")],
        "extra_schema": faq_schema(BIZ_FAQS),
    },
    {
        "path": "/business/workers-compensation/",
        "title": "Michigan Workers Compensation Insurance | J. Jacobs",
        "description": "Michigan workers compensation insurance from an experienced independent agency. We handle classifications, audits, Mod management, and multi-carrier shopping.",
        "body": WC_BODY,
        "breadcrumb_items": [("Home", "/"), ("Commercial Insurance", "/business/"), ("Workers Compensation", "/business/workers-compensation/")],
        "extra_schema": faq_schema(WC_FAQS),
    },
    {
        "path": "/service/",
        "title": "Customer Service Center | J. Jacobs & Associates Insurance",
        "description": "ID cards, certificates of insurance, claims, billing, policy changes — everything you need as a J. Jacobs & Associates client. Call (248) 693-6455.",
        "body": SERVICE_BODY,
        "breadcrumb_items": [("Home", "/"), ("Service Center", "/service/")],
    },
    {
        "path": "/quotes/",
        "title": "Get an Insurance Quote | J. Jacobs & Associates",
        "description": "Get a free auto, home, life, or business insurance quote from J. Jacobs & Associates. We shop 20+ carriers and find the best Michigan coverage.",
        "body": QUOTE_BODY,
        "breadcrumb_items": [("Home", "/"), ("Start a Quote", "/quotes/")],
    },
    {
        "path": "/contact/",
        "title": "Contact Us | J. Jacobs & Associates Insurance",
        "description": "Contact J. Jacobs & Associates Insurance in Lake Orion, Michigan. Call (248) 693-6455, email Support@jjainsurance.com, or use our contact form.",
        "body": CONTACT_BODY,
        "breadcrumb_items": [("Home", "/"), ("Contact", "/contact/")],
        "extra_schema": AGENCY_SCHEMA,
    },
    {
        "path": "/faq/",
        "title": "Insurance FAQ | J. Jacobs & Associates",
        "description": "Common insurance questions answered: Michigan No-Fault, workers comp requirements, home insurance basics, life insurance options, and more.",
        "body": FAQ_BODY,
        "breadcrumb_items": [("Home", "/"), ("FAQ", "/faq/")],
        "extra_schema": faq_schema(MAIN_FAQS),
    },
    {
        "path": "/privacy-policy/",
        "title": "Privacy Policy | J. Jacobs & Associates Insurance",
        "description": "Privacy policy for J. Jacobs & Associates Insurance website and agency relationships.",
        "body": PRIVACY_BODY,
        "breadcrumb_items": [("Home", "/"), ("Privacy Policy", "/privacy-policy/")],
    },
    {
        "path": "/accessibility/",
        "title": "Accessibility Statement | J. Jacobs & Associates Insurance",
        "description": "J. Jacobs & Associates Insurance accessibility statement and contact information for accessibility support.",
        "body": ACCESSIBILITY_BODY,
        "breadcrumb_items": [("Home", "/"), ("Accessibility", "/accessibility/")],
    },
]


# ----------------------------------------------------------------------
# EXTRA FILES: robots.txt, sitemap.xml, 404.html, README.md
# ----------------------------------------------------------------------
SITEMAP_URLS = [
    ("/", "1.0", "weekly"),
    ("/about/", "0.8", "monthly"),
    ("/team/", "0.7", "monthly"),
    ("/carriers/", "0.7", "monthly"),
    ("/reviews/", "0.7", "weekly"),
    ("/personal/", "0.9", "monthly"),
    ("/personal/auto-insurance/", "0.9", "monthly"),
    ("/personal/home-insurance/", "0.9", "monthly"),
    ("/personal/life-insurance/", "0.9", "monthly"),
    ("/business/", "0.9", "monthly"),
    ("/business/workers-compensation/", "0.9", "monthly"),
    ("/service/", "0.6", "monthly"),
    ("/quotes/", "1.0", "monthly"),
    ("/contact/", "0.8", "monthly"),
    ("/faq/", "0.8", "weekly"),
    ("/privacy-policy/", "0.3", "yearly"),
    ("/accessibility/", "0.3", "yearly"),
]

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url, priority, change in SITEMAP_URLS:
    sitemap_xml += f'  <url>\n    <loc>https://www.jjainsurance.com{url}</loc>\n    <changefreq>{change}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
sitemap_xml += '</urlset>\n'

robots_txt = """User-agent: *
Allow: /
Disallow: /_*

Sitemap: https://www.jjainsurance.com/sitemap.xml
"""

# 404 page
NOT_FOUND_HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | J. Jacobs & Associates Insurance</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
<section class="section" style="text-align:center; min-height: 70vh; display:flex; align-items:center;">
  <div class="container" style="max-width:600px;">
    <span class="eyebrow">404</span>
    <h1>Page Not Found</h1>
    <p class="lead">The page you're looking for doesn't exist or has moved.</p>
    <p style="margin-top:1.5rem;">
      <a class="btn btn-primary btn-lg" href="/">Go to Homepage</a>
      <a class="btn btn-outline btn-lg" href="/contact/" style="margin-left:.5rem;">Contact Us</a>
    </p>
    <p style="margin-top:2rem; color:var(--text-muted);">Or call us at <a href="tel:+12486936455"><strong>(248) 693-6455</strong></a></p>
  </div>
</section>
</body>
</html>
'''

README_MD = '''# J. Jacobs & Associates Insurance — Static Site

Static website rebuild for jjainsurance.com.

## Stack

Pure static HTML, CSS, and a tiny bit of JavaScript. No frameworks, no build dependencies beyond Python 3 (used only to generate pages from shared templates).

## Files

- `index.html` — Homepage
- `<section>/index.html` — Each section page (about, team, personal, business, etc.)
- `assets/css/styles.css` — All site styles
- `assets/js/main.js` — Mobile menu, form helpers
- `robots.txt`, `sitemap.xml` — Search engine essentials
- `_build.py`, `_pages.py` — Build script (regenerates the HTML if you want to edit shared header/footer or content)

## Edit content

The fastest way is to edit `_pages.py` (page content) or the templates in `_build.py` (shared header/footer), then run:

```
python3 _build.py
```

That regenerates all the HTML files in place. You can also just edit the generated HTML files directly — they're plain HTML.

## Deploy

This is a pure static site. It works on any host:

### Cloudflare Pages (recommended — free, fast, includes form handling)
1. Create a Cloudflare account, then go to Workers & Pages → Create → Pages
2. Direct upload: drag the entire site folder into Cloudflare's upload UI
3. Or connect to a Git repo (recommended for ongoing updates)
4. Free SSL is automatic. Add jjainsurance.com as a custom domain.

### Netlify (free)
1. Drag the site folder onto netlify.com/drop
2. Done. Add custom domain in settings.

### Vercel (free)
1. Drop into the Vercel dashboard or connect to Git
2. Free SSL, custom domain in settings

### Your own server / VPS
Copy the folder to any web server. Configure to serve `index.html` for directory requests.

## Forms

The quote and contact forms POST to Formspree. Before deploying:

1. Create a free Formspree account at formspree.io
2. Create one form for "Quote Request" and one for "Contact"
3. Replace `YOUR_FORM_ID` in `_pages.py` (or in the generated HTML) with your actual form IDs
4. Run `python3 _build.py` to regenerate if you edited the Python file

Form submissions will email to whatever email you set in Formspree. From there:
- Quote leads come in formatted with all the PL Rater / Hawksoft fields ready to copy in
- Contact requests come in with the relevant policy info

If you want a more native Hawksoft integration later, look into Canopy Connect or a custom webhook from Formspree to your AMS.

## SEO & AEO

The site includes:
- LocalBusiness / InsuranceAgency schema (Google Knowledge Panel, AI engine grounding)
- FAQPage schema on relevant pages (gets pulled into Google's AI Overviews and answer engines like ChatGPT/Perplexity)
- BreadcrumbList schema
- Open Graph + Twitter Card meta tags
- Clean canonical URLs
- robots.txt + sitemap.xml
- Semantic HTML and accessible markup
- Fast loading (no framework overhead)

After launch:
- Submit `https://www.jjainsurance.com/sitemap.xml` in Google Search Console
- Verify Google Business Profile is connected
- Verify Bing Webmaster Tools
- Set up Google Analytics 4 if you want traffic data (add the snippet to `_build.py` head)

## To-do before launch

- [ ] Replace `YOUR_FORM_ID` placeholders with real Formspree IDs (or your form handler of choice)
- [ ] Add a real logo image at `assets/img/logo.png`
- [ ] Add real team photos (or remove avatars if you prefer initials)
- [ ] Add an Open Graph image (`assets/img/og-default.jpg`, 1200x630)
- [ ] Verify all carrier names match your current appointments
- [ ] Confirm the office hours in the schema match reality
- [ ] Add Google Analytics or Plausible if you want analytics
'''

EXTRAS = {
    "sitemap.xml": sitemap_xml,
    "robots.txt": robots_txt,
    "404.html": NOT_FOUND_HTML,
    "README.md": README_MD,
}
