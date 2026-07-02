#!/usr/bin/env python3
"""Generator for the 9 industry product pages + wiring into the business overview
(new grid cards AND new definition blocks), sitemap, and llms.txt."""
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
VER="20260613"; REL="../../"
FORCE=(len(sys.argv)>2 and sys.argv[2]=="force")

CONFIG=[
{"section":"business","slug":"trucking-insurance","def_id":"trucking","grid_label":"Trucking & Transportation",
 "eyebrow":"Commercial / Trucking","svc":"Trucking Insurance","title":"Michigan Trucking & Commercial Truck Insurance",
 "meta":"Trucking insurance for Michigan — primary liability, physical damage, motor truck cargo, and the FMCSA filings owner-operators and fleets need. Multi-carrier shopping.",
 "hero":"photo-1601584115197-04ecc0da31d7","alt":"Semi truck on a Michigan highway — trucking insurance",
 "def_text":"Trucking and transportation businesses need primary liability, physical damage, motor truck cargo, and non-trucking liability — plus the FMCSA filings (such as the MCS-90) interstate carriers require. We write owner-operators, fleets, and for-hire and private carriers.",
 "lead":"Trucking carries some of the highest liability exposure on the road, and the wrong policy or a missed filing can park your business. We cover Michigan owner-operators and fleets with the liability, cargo, and physical-damage coverage carriers and shippers require.",
 "whatwedo":[("FMCSA filings handled","we file the MCS-90 and other federal forms interstate carriers need to stay legal and loaded."),
   ("The full trucking stack","primary liability, physical damage, motor truck cargo, and non-trucking (bobtail) liability, coordinated correctly."),
   ("Owner-operators and fleets","whether you run one truck or twenty, we shop carriers that want your operation and radius."),
   ("Multi-carrier shopping","trucking pricing swings hard between markets — we compare to keep you covered and competitive.")],
 "who_h":"Operations we cover","who":"Owner-operators and independent drivers, for-hire and private fleets, local and long-haul carriers, dump trucks and tow operators, hot shot and box-truck businesses, and motor carriers across Michigan and interstate.",
 "cov_h":"What trucking insurance covers","cov":[("Primary liability","bodily injury and property damage you cause — required to operate."),
   ("Physical damage","collision and comprehensive for your tractor and trailer."),
   ("Motor truck cargo","the freight you haul against damage, theft, and loss."),
   ("Non-trucking / bobtail","liability when driving without a load or off dispatch."),
   ("General liability","loading, unloading, and premises exposures off the road.")],
 "faqs":[("What insurance do truckers need in Michigan?","Most need primary auto liability, physical damage on the truck and trailer, motor truck cargo, and — for interstate carriers — federal filings like the MCS-90. Owner-operators leased to a carrier often add non-trucking (bobtail) liability. We build the right combination for your authority and operation."),
   ("What is an MCS-90 filing?","It's a federal endorsement proving an interstate motor carrier carries the minimum public liability the FMCSA requires. Without the right filings on record, you can't legally run interstate freight. We handle the filing as part of placing your coverage."),
   ("Does trucking insurance cover the cargo I haul?","Only if you carry motor truck cargo coverage — your liability policy doesn't pay for the freight itself. Cargo coverage protects the load against damage, theft, and loss, with limits and commodity terms matched to what you haul."),
   ("How much does trucking insurance cost in Michigan?","It varies widely by your authority, radius, driving records, cargo, and loss history — trucking is one of the most variable commercial lines. Because we're independent, we shop multiple trucking markets to find your best combination of price and coverage.")],
 "cta":"Get a trucking insurance quote"},

{"section":"business","slug":"manufacturing-insurance","def_id":"manufacturers","grid_label":"Manufacturing",
 "eyebrow":"Commercial / Manufacturing","svc":"Manufacturing Insurance","title":"Michigan Manufacturing Insurance",
 "meta":"Manufacturing insurance for Michigan — product liability, commercial property for equipment and stock, business interruption, equipment breakdown, and workers comp.",
 "hero":"photo-1567789884554-0b844b597180","alt":"Manufacturing line — Michigan manufacturing insurance",
 "def_text":"Manufacturers need product liability, commercial property for equipment and stock, business interruption, commercial auto, and workers comp. Product recall and equipment breakdown are common add-ons. We match coverage to your process and exposures.",
 "lead":"A manufacturer's risk runs from the shop floor to the product in a customer's hands. Michigan manufacturing insurance protects your equipment and inventory, the income that depends on them, and the liability that follows your product out the door.",
 "whatwedo":[("Product liability done right","coverage for claims that your product caused injury or damage — the exposure that outlasts the sale."),
   ("Protect the operation","property for your building, machinery, and stock, plus business interruption and equipment breakdown so a loss doesn't stop production."),
   ("Coverage matched to your process","fabrication, food and beverage, plastics, metal, and assembly each carry different exposures."),
   ("Multi-carrier shopping","we compare manufacturing markets for the right program at the right price.")],
 "who_h":"Manufacturers we cover","who":"Metal fabrication and machine shops, plastics and injection molders, food and beverage producers, furniture and wood products, electronics and assembly, contract manufacturers, and other Michigan producers.",
 "cov_h":"What manufacturing insurance covers","cov":[("Product liability","claims that your finished product caused injury or damage."),
   ("Commercial property","your building, machinery, equipment, and inventory."),
   ("Business interruption","income lost while a covered loss halts production."),
   ("Equipment breakdown","mechanical or electrical failure of critical machinery."),
   ("Workers compensation","required for nearly every Michigan employer.")],
 "faqs":[("What insurance does a manufacturer need in Michigan?","Typically product liability, commercial property for equipment and stock, general liability, business interruption, equipment breakdown, commercial auto, and workers comp. Recall coverage and inland marine for goods in transit are common additions. We build the program around your process."),
   ("Why is product liability important for manufacturers?","Because your exposure doesn't end when the product ships — if it injures someone or damages property later, the claim comes back to you, often years on. Product liability defends and pays those claims, and it's essential for anyone making a physical product."),
   ("Does manufacturing insurance cover equipment breakdown?","It can, as a coverage you add. Equipment breakdown pays to repair or replace machinery that fails mechanically or electrically — and often the business income lost while it's down. For a production business, it's one of the most valuable add-ons."),
   ("How much does manufacturing insurance cost in Michigan?","It depends on your product, revenue, payroll, equipment values, and loss history. A small machine shop pays far less than a food producer. Because we're independent, we shop manufacturing markets to find your best combination of coverage and price.")],
 "cta":"Get a manufacturing quote"},

{"section":"business","slug":"counselor-insurance","def_id":"counselor","grid_label":"Counselors & Therapists",
 "eyebrow":"Commercial / Counselors","svc":"Counselor & Therapist Insurance","title":"Michigan Counselor & Therapist Insurance",
 "meta":"Insurance for Michigan counselors, therapists, and social workers — professional liability (malpractice), general liability, and coverage for telehealth and group practices.",
 "hero":"photo-1573497019940-1c28c88b4f3e","alt":"Counseling professional — Michigan counselor and therapist insurance",
 "def_text":"Counselors, therapists, and social workers need professional liability (malpractice) plus general liability for their practice. Telehealth, group practices, and licensure exposures all factor in. We write solo practitioners and group practices.",
 "lead":"The work you do carries real professional risk — a single client complaint or board inquiry can threaten your license and livelihood. Michigan counselor and therapist insurance protects you with professional liability built for mental-health practitioners, plus the general liability your practice needs.",
 "whatwedo":[("Malpractice that fits your practice","professional liability for the counseling, therapy, and clinical work you actually do, including telehealth."),
   ("License-defense protection","coverage that helps defend you in a licensing board investigation, not just a lawsuit."),
   ("Solo and group practices","whether you practice alone or run a group, we structure coverage for your setup."),
   ("Multi-carrier shopping","we compare professional-liability markets built for mental-health providers.")],
 "who_h":"Professionals we cover","who":"Licensed professional counselors (LPCs), therapists and psychotherapists, marriage and family therapists, clinical social workers, psychologists, substance-abuse counselors, and group counseling practices across Michigan.",
 "cov_h":"What counselor insurance covers","cov":[("Professional liability","malpractice claims tied to your counseling and clinical work."),
   ("License defense","help defending a licensing board complaint or inquiry."),
   ("General liability","slips, falls, and other premises claims at your office."),
   ("Telehealth","claims arising from remote and virtual sessions."),
   ("Group / practice coverage","protection for a group practice and its providers.")],
 "faqs":[("Do counselors and therapists need malpractice insurance in Michigan?","It's strongly recommended and often required — by employers, group practices, insurance panels, and some licensing situations. Professional liability defends and pays claims that your counseling caused harm, including the cost of defending a board complaint even when you've done nothing wrong."),
   ("What's the difference between professional and general liability for a therapist?","Professional liability (malpractice) covers claims tied to your clinical work and advice. General liability covers physical risks at your office, like a client slipping in the waiting room. Most practitioners need both — one won't respond to the other's claims."),
   ("Does counselor insurance cover telehealth?","Yes, when written for it. As remote sessions have become standard, professional liability policies for counselors generally extend to telehealth — but the terms vary, so we confirm your virtual work is covered."),
   ("How much does counselor or therapist insurance cost in Michigan?","Professional liability for a solo counselor is often very affordable — frequently a few hundred dollars a year — with group practices priced on size and services. We shop carriers that specialize in mental-health providers to find your best rate.")],
 "cta":"Get a counselor insurance quote"},

{"section":"business","slug":"consulting-insurance","def_id":"consulting","grid_label":"Consultants",
 "eyebrow":"Commercial / Consulting","svc":"Consultant Insurance","title":"Michigan Consultant Insurance",
 "meta":"Insurance for Michigan consultants — professional liability (E&O) for the advice you give, plus general liability and cyber coverage. Management, IT, HR, and marketing consultants.",
 "hero":"photo-1562564055-71e051d33c19","alt":"Consultants meeting — Michigan consultant insurance",
 "def_text":"Consultants need professional liability (E&O) for the advice they give, plus general liability and often cyber coverage. Management, IT, marketing, HR, and engineering consultants each carry different exposures. We tailor coverage to your specialty.",
 "lead":"When clients pay for your expertise, a result they didn't expect can turn into a claim against you. Michigan consultant insurance protects you with errors & omissions coverage for the advice and services you deliver, plus the general and cyber coverage modern consulting needs.",
 "whatwedo":[("E&O for your advice","professional liability covering claims that your work, advice, or deliverables caused a client financial harm."),
   ("Contract-ready limits","clients increasingly require proof of E&O before they sign — we set limits to win the engagement."),
   ("Cyber where it matters","many consultants handle client data; we add cyber coverage to close that gap."),
   ("Multi-carrier shopping","we match the E&O form to your consulting specialty and shop it for the best rate.")],
 "who_h":"Consultants we cover","who":"Management and business consultants, IT and technology consultants, marketing and PR consultants, HR and recruiting consultants, financial and operations consultants, engineering and environmental consultants, and independent advisors across Michigan.",
 "cov_h":"What consultant insurance covers","cov":[("Professional liability (E&O)","claims of negligence, errors, or failure to deliver in your work."),
   ("General liability","third-party injury or property damage at meetings and offices."),
   ("Cyber liability","data breaches and the client data you handle."),
   ("Defense costs","attorney fees and settlements, even for unfounded claims."),
   ("Contract compliance","limits and endorsements your client contracts require.")],
 "faqs":[("Do consultants need professional liability insurance?","Yes — it's the core coverage for anyone paid for advice or expertise. If a client claims your work cost them money through an error, omission, or failure to deliver, E&O defends and pays the claim. Many clients now require proof of it before they'll sign a contract."),
   ("What's the difference between general and professional liability for a consultant?","General liability covers physical risks — someone injured at a meeting or property you damage. Professional liability (E&O) covers financial harm from your advice or deliverables. Most consultants need both, and many add cyber because they handle client data."),
   ("Do I need cyber insurance as a consultant?","If you store or handle client data — and most consultants do — yes. A breach can expose you to notification costs and client claims that E&O alone may not cover. We frequently package cyber with a consultant's E&O and general liability."),
   ("How much does consultant insurance cost in Michigan?","For a solo consultant, professional liability is often a modest annual premium, with pricing based on your revenue, specialty, and the limits your contracts require. We shop multiple markets to match the right coverage to your practice at the best price.")],
 "cta":"Get a consultant insurance quote"},

{"section":"business","slug":"water-well-insurance","def_id":"water-well","grid_label":"Water Well Contractors",
 "eyebrow":"Commercial / Water Well","svc":"Water Well Contractor Insurance","title":"Michigan Water Well Contractor Insurance",
 "meta":"Insurance for Michigan water well drilling and pump contractors — general liability, commercial auto for rigs, contractor's equipment, pollution liability, and workers comp.",
 "hero":"photo-1559825481-12a05cc00344","alt":"Clear water — Michigan water well contractor insurance",
 "def_text":"Water well drilling and pump contractors need general liability with the right classification, commercial auto for rigs, contractor's equipment (inland marine), pollution liability, and workers comp. We write drillers, pump installers, and geothermal contractors.",
 "lead":"Drilling and servicing wells carries exposures most contractors never face — from striking utilities to contaminating groundwater. Michigan water well contractor insurance covers your liability, your rigs and equipment, and the pollution risk that comes with working underground.",
 "whatwedo":[("Correct trade classification","misclassifying well work is a fast way to overpay or void a claim — we get the classification and forms right."),
   ("Cover the rigs and equipment","commercial auto for drilling rigs and contractor's equipment (inland marine) for your tools and gear."),
   ("Pollution liability","coverage for groundwater contamination and pollution claims standard policies exclude."),
   ("Multi-carrier shopping","we shop the markets that understand drilling and pump work.")],
 "who_h":"Contractors we cover","who":"Water well drilling contractors, pump installation and service companies, geothermal drilling contractors, well abandonment and rehabilitation specialists, and related groundwater trades across Michigan.",
 "cov_h":"What water well contractor insurance covers","cov":[("General liability","third-party injury and property damage from your operations."),
   ("Pollution liability","groundwater contamination and pollution claims."),
   ("Commercial auto","drilling rigs, service trucks, and equipment trailers."),
   ("Contractor's equipment","your rigs, pumps, and tools (inland marine)."),
   ("Workers compensation","required for nearly every Michigan employer.")],
 "faqs":[("What insurance does a water well contractor need in Michigan?","Typically general liability with the correct drilling classification, commercial auto for rigs and trucks, contractor's equipment (inland marine) coverage, pollution liability for groundwater exposure, and workers comp. Larger jobs may require a commercial umbrella. We assemble the right program for your operation."),
   ("Why do well contractors need pollution liability?","Because drilling and pump work can contaminate groundwater, and standard general liability excludes most pollution claims. Pollution liability covers contamination and cleanup exposures unique to working underground — a critical gap for any drilling contractor."),
   ("Does my equipment get covered when it's on a job site?","Yes — contractor's equipment (inland marine) coverage protects your rigs, pumps, and tools whether they're at your yard, in transit, or on a job site. General liability and property policies won't cover mobile equipment the way inland marine does."),
   ("How much does water well contractor insurance cost in Michigan?","It depends on your payroll, revenue, equipment values, and the pollution exposure of your work. Because well drilling is a specialized class, we shop the carriers that write it to find the right coverage at a fair price.")],
 "cta":"Get a water well insurance quote"},

{"section":"business","slug":"liquor-liability-insurance","def_id":"liquor-liability","grid_label":"Liquor Liability",
 "eyebrow":"Commercial / Liquor Liability","svc":"Liquor Liability Insurance","title":"Michigan Liquor Liability Insurance",
 "meta":"Liquor liability insurance for Michigan businesses that sell or serve alcohol — dram shop protection bars, restaurants, and events need beyond general liability.",
 "hero":"photo-1514362545857-3bc16c4c7d1b","alt":"Cocktail at a bar — Michigan liquor liability insurance",
 "def_text":"Any Michigan business that sells or serves alcohol can be held liable under the state's dram shop law for harm caused by a visibly intoxicated or underage patron. Liquor liability is separate from general liability and required by most liquor licenses and landlords. We write bars, restaurants, and special events.",
 "lead":"Under Michigan's dram shop law, a business that serves a visibly intoxicated or underage patron can be held liable for the harm that follows. General liability won't cover it — liquor liability is the separate coverage your license, your landlord, and your protection require.",
 "whatwedo":[("Dram shop protection","coverage for the liability Michigan's dram shop law creates when you sell or serve alcohol."),
   ("Meet license and lease requirements","we provide the proof of liquor liability your liquor license and landlord require."),
   ("Coverage for how you serve","bars, restaurants, breweries, caterers, and one-time special events each get the right form."),
   ("Multi-carrier shopping","we compare markets so your alcohol exposure is covered at a fair price.")],
 "who_h":"Who needs liquor liability","who":"Bars and taverns, restaurants that serve alcohol, breweries and tasting rooms, banquet and event venues, caterers, package and liquor stores, and hosts of special events serving alcohol across Michigan.",
 "cov_h":"What liquor liability covers","cov":[("Dram shop liability","claims that serving a patron led to injury or damage."),
   ("Assault and battery","alcohol-related altercation claims (where included)."),
   ("Defense costs","legal fees to defend a liquor-related claim."),
   ("Host liquor (events)","serving (not selling) alcohol at a private event."),
   ("Required proof of coverage","the certificate your license or landlord requires.")],
 "faqs":[("What is dram shop liability in Michigan?","Michigan's dram shop law allows an injured party to hold a business liable for serving alcohol to a visibly intoxicated or underage person who then causes harm. Liquor liability insurance is what responds to those claims — and general liability specifically excludes them."),
   ("Do I need liquor liability if I already have general liability?","Yes. General liability almost always excludes alcohol-related claims, so a business that sells or serves alcohol needs separate liquor liability coverage. Most Michigan liquor licenses and commercial landlords also require proof of it."),
   ("Who needs liquor liability insurance?","Any business that sells or serves alcohol — bars, restaurants, breweries, caterers, event venues, and liquor stores — plus hosts serving alcohol at private events (covered under host liquor liability). If alcohol changes hands at your business, you have the exposure."),
   ("How much does liquor liability insurance cost in Michigan?","It depends on your alcohol sales, the type of establishment, and your loss history — a tasting room costs far less than a late-night bar. Because we're independent, we shop multiple markets to find the right liquor liability coverage at a competitive price.")],
 "cta":"Get a liquor liability quote"},

{"section":"business","slug":"home-health-insurance","def_id":"home-health","grid_label":"Home Health Care",
 "eyebrow":"Commercial / Home Health","svc":"Home Health Care Insurance","title":"Michigan Home Health Care Insurance",
 "meta":"Insurance for Michigan home health and home care agencies — professional liability, general liability, abuse coverage, non-owned auto for caregivers, and workers comp.",
 "hero":"photo-1559839734-2b71ea197ec2","alt":"Home health caregiver — Michigan home health care insurance",
 "def_text":"Home health and home care agencies need professional liability, general liability, abuse and molestation coverage, non-owned auto for caregivers, and workers comp. Medical and non-medical agencies have different forms. We write both.",
 "lead":"Caring for clients in their homes carries exposures a clinic never faces — caregivers driving between visits, working unsupervised, and serving a vulnerable population. Michigan home health insurance covers the professional, liability, abuse, and auto risks your agency lives with every day.",
 "whatwedo":[("Professional and general liability","coverage for claims tied to care provided and for premises and operations exposures."),
   ("Abuse and molestation coverage","critical protection when caring for vulnerable clients, often excluded elsewhere."),
   ("Non-owned auto for caregivers","coverage when staff drive their own cars between client visits — a gap most agencies miss."),
   ("Medical and non-medical forms","skilled home health and non-medical home care get the right coverage for each.")],
 "who_h":"Agencies we cover","who":"Skilled home health agencies, non-medical home care and companion services, personal care and senior care providers, hospice support, and private-duty caregivers across Michigan.",
 "cov_h":"What home health insurance covers","cov":[("Professional liability","claims tied to the care your staff provides."),
   ("General liability","premises and operations injury and damage claims."),
   ("Abuse and molestation","claims involving vulnerable clients in their homes."),
   ("Non-owned / hired auto","caregivers driving personal vehicles for work."),
   ("Workers compensation","required for nearly every Michigan employer.")],
 "faqs":[("What insurance does a home health agency need in Michigan?","Typically professional liability, general liability, abuse and molestation coverage, non-owned and hired auto (for caregivers using their own cars), and workers comp. Skilled and non-medical agencies have different forms, and some payers and licenses require specific limits. We build the right program for your agency."),
   ("Why do home care agencies need abuse and molestation coverage?","Because caregivers work one-on-one with vulnerable clients, often unsupervised, abuse and molestation allegations are a serious exposure — and standard liability typically excludes or sublimits them. Dedicated coverage with proper limits is considered essential for home care."),
   ("Does it cover caregivers driving their own cars?","Only with non-owned and hired auto coverage, which most agencies need because staff drive personal vehicles between client visits. Without it, an at-fault accident on the way to a client can become the agency's uncovered liability. We make sure it's included."),
   ("How much does home health insurance cost in Michigan?","It depends on your services (skilled vs. non-medical), payroll, number of caregivers, and client volume. Because we're independent, we shop the carriers that specialize in home care to find the right coverage at the best price.")],
 "cta":"Get a home health quote"},

{"section":"business","slug":"educational-insurance","def_id":"educational","grid_label":"Schools & Educational",
 "eyebrow":"Commercial / Education","svc":"School & Educational Insurance","title":"Michigan School & Educational Insurance",
 "meta":"Insurance for Michigan schools, daycares, and educational programs — property, liability, abuse coverage, educators' professional liability, D&O, and student accident.",
 "hero":"photo-1503676260728-1c00da094a0b","alt":"Classroom books and supplies — Michigan school and educational insurance",
 "def_text":"Schools, daycares, preschools, tutoring centers, and educational nonprofits need property, general liability, abuse and molestation coverage, educators' professional liability, directors & officers (D&O), and student-accident coverage. We write private schools, childcare, and education programs.",
 "lead":"Educational organizations are responsible for children and the people who teach them — a combination of exposures few businesses face. Michigan school and educational insurance brings property, liability, abuse, professional, and board coverage into one program built for how schools and programs operate.",
 "whatwedo":[("Coverage built for education","property and liability plus the abuse, educators' professional, and D&O coverages a generic policy leaves out."),
   ("Protect students and staff","abuse and molestation coverage and student-accident options for the children in your care."),
   ("Right-sized for your program","private schools, daycares, preschools, and tutoring centers each get coverage that fits."),
   ("Multi-carrier shopping","we compare education and human-services markets for the best program.")],
 "who_h":"Organizations we cover","who":"Private and charter schools, daycares and childcare centers, preschools and Montessori programs, tutoring and enrichment centers, trade and vocational schools, and educational nonprofits across Michigan.",
 "cov_h":"What educational insurance covers","cov":[("Property","buildings, classrooms, equipment, and contents."),
   ("General / premises liability","injury and damage claims on school grounds."),
   ("Abuse and molestation","claims involving students — a critical coverage."),
   ("Educators' professional liability","claims tied to teaching and educational decisions."),
   ("Directors and officers (D&O)","claims against the board and administration.")],
 "faqs":[("What insurance does a school or daycare need in Michigan?","Typically property, general liability, abuse and molestation coverage, educators' professional liability, directors and officers (D&O), workers comp, and often student-accident coverage. Childcare and licensing requirements may add more. We build the program around your program.")
   ,("Why do schools and daycares need abuse and molestation coverage?","Because organizations responsible for children face serious abuse-allegation exposure, and standard liability often excludes or sublimits it. Dedicated abuse and molestation coverage — with proper limits and screening practices — is considered essential for any school or childcare program."),
   ("What is educators' professional liability?","It covers claims arising from educational duties and decisions — things general liability doesn't, like a claim over how a student was taught, disciplined, or accommodated. Schools and education programs carry this professional exposure alongside their physical-risk exposure."),
   ("How much does school or daycare insurance cost in Michigan?","It depends on enrollment, ages served, property values, activities, and your program type. Because we're independent, we shop the education and human-services markets to match the right coverage to your organization at a fair price.")],
 "cta":"Get an educational insurance quote"},

{"section":"business","slug":"technology-insurance","def_id":"technology","grid_label":"Technology & IT",
 "eyebrow":"Commercial / Technology","svc":"Technology & IT Insurance","title":"Michigan Technology & IT Insurance",
 "meta":"Insurance for Michigan technology and IT companies — technology E&O (professional liability plus cyber), general liability, and property for software, SaaS, and IT firms.",
 "hero":"photo-1614064641938-3bbee52942c7","alt":"Technology and code — Michigan technology and IT insurance",
 "def_text":"Technology companies need technology E&O (which blends professional liability and cyber), general liability, and property for equipment. Software, IT services, SaaS, and hardware firms each carry different exposures. We write startups through established tech businesses.",
 "lead":"Tech companies carry a blended risk standard policies handle poorly — a failure of your software or service can cause a client both financial loss and a data breach. Michigan technology insurance combines professional liability and cyber into technology E&O, plus the general liability and property a tech business needs.",
 "whatwedo":[("Technology E&O","blended professional liability and cyber for claims that your product or service failed a client."),
   ("Cyber and data protection","breach response, ransomware, and the data-handling exposure every tech firm carries."),
   ("Contract-ready coverage","clients and partners increasingly require E&O and cyber limits — we set yours to close deals."),
   ("Startups to scale-ups","coverage that fits a two-person startup and grows with an established firm.")],
 "who_h":"Companies we cover","who":"Software and SaaS companies, IT services and managed service providers (MSPs), web and app developers, hardware and electronics firms, data and analytics companies, and technology consultants and startups across Michigan.",
 "cov_h":"What technology insurance covers","cov":[("Technology E&O","claims that your software, service, or product failed to perform."),
   ("Cyber liability","data breaches, ransomware, and breach-response costs."),
   ("General liability","third-party injury and property damage exposures."),
   ("Property / equipment","your hardware, servers, and office equipment."),
   ("Contract compliance","the E&O and cyber limits clients require to sign.")],
 "faqs":[("What insurance does a technology company need in Michigan?","Most need technology E&O (which blends professional liability and cyber), general liability, and property for equipment. Software and SaaS firms lean heavily on E&O and cyber; hardware firms add product liability. We build the program around your tech business and the contracts you're signing."),
   ("What is technology E&O?","It's a combined policy that covers both professional liability (a claim your software or service failed to perform) and cyber (a data breach or security failure). Tech companies face both exposures from the same event, so a blended technology E&O policy is the standard way to cover them."),
   ("Do software and SaaS companies need cyber insurance?","Yes — handling client data and running services online creates direct breach exposure, and clients increasingly require proof of cyber coverage. Most tech firms carry it inside a technology E&O policy or alongside one. We make sure your data exposure is covered."),
   ("How much does technology insurance cost in Michigan?","It depends on your revenue, the services you provide, the data you handle, and the limits your contracts require. Because we're independent, we shop the technology markets to match the right E&O and cyber coverage to your firm at a competitive price.")],
 "cta":"Get a technology insurance quote"},
]

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def head(cfg):
    sec_name="Commercial Insurance"; sec_url=f"{SITE}/business/"; url=f"{SITE}/business/{cfg['slug']}/"
    title_tag=f"{cfg['title']} | J. Jacobs"; og_img=f"{SITE}/assets/img/og/business-{cfg['slug']}.jpg"
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
    return f"""<header class="site-header"><div class="container">
    <a class="brand" href="{r}" aria-label="J. Jacobs and Associates Insurance home"><img class="brand-logo-img" src="{r}assets/img/logo.jpeg" alt="J. Jacobs and Associates Insurance"></a>
    <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary"><ul>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Our Agency</summary><ul class="submenu">
            <li><a href="{r}about/">About Us</a></li><li><a href="{r}team/">Our Team</a></li><li><a href="{r}carriers/">Our Carriers</a></li><li><a href="{r}reviews/">Reviews</a></li>
          </ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Products</summary><ul class="submenu">
            <li><a href="{r}personal/">Personal Insurance</a></li><li><a href="{r}personal/auto-insurance/">Auto Insurance</a></li><li><a href="{r}personal/home-insurance/">Home Insurance</a></li><li><a href="{r}personal/life-insurance/">Life Insurance</a></li><li><a href="{r}business/">Commercial Insurance</a></li><li><a href="{r}business/workers-compensation/">Workers Compensation</a></li>
          </ul></details></li>
        <li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Service</summary><ul class="submenu">
            <li><a href="{r}service/">Service Center</a></li><li><a href="{r}billing-claims/">Billing &amp; Claims</a></li>
          </ul></details></li>
        <li><a href="{r}blog/">Blog</a></li><li><a href="{r}faq/">FAQ</a></li><li><a href="{r}contact/">Contact</a></li>
      </ul></nav>
    <div class="header-cta"><a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a><a class="btn btn-primary" href="{r}quotes/">Start a Quote</a></div>
  </div></header>"""
def footer():
    r=REL
    return f"""<footer class="site-footer"><div class="container"><div class="footer-grid">
      <div class="footer-brand"><div class="footer-logo"><img src="{r}assets/img/logo.jpeg" alt="J. Jacobs and Associates"></div>
        <h4>J. Jacobs &amp; Associates</h4>
        <p>Family-owned independent insurance agency serving Michigan since 1981. We shop 35+ carriers so you don&rsquo;t have to.</p>
        <p style="margin-top:1rem;"><strong style="color:#fff;">4301 S. Baldwin Rd</strong><br>Lake Orion, Michigan 48359<br><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div><h4>Insurance</h4><ul><li><a href="{r}personal/">Personal Insurance</a></li><li><a href="{r}personal/auto-insurance/">Auto Insurance</a></li><li><a href="{r}personal/home-insurance/">Home Insurance</a></li><li><a href="{r}personal/life-insurance/">Life Insurance</a></li><li><a href="{r}business/">Commercial Insurance</a></li><li><a href="{r}business/workers-compensation/">Workers Compensation</a></li></ul></div>
      <div><h4>Agency</h4><ul><li><a href="{r}about/">About Us</a></li><li><a href="{r}team/">Our Team</a></li><li><a href="{r}carriers/">Our Carriers</a></li><li><a href="{r}reviews/">Reviews</a></li><li><a href="{r}service/">Service Center</a></li><li><a href="{r}billing-claims/">Billing &amp; Claims</a></li><li><a href="{r}faq/">FAQ</a></li></ul></div>
      <div><h4>Follow Us</h4><div class="social-row"><a href="https://www.facebook.com/JacobsandAssociates/" aria-label="Facebook" rel="noopener" target="_blank">f</a><a href="https://www.instagram.com/jjacobs_and_associates/" aria-label="Instagram" rel="noopener" target="_blank">IG</a><a href="https://www.linkedin.com/in/joe-jacobs-7a354422/" aria-label="LinkedIn" rel="noopener" target="_blank">in</a></div>
        <ul style="margin-top:1.25rem;"><li><a href="{r}contact/">Contact Us</a></li><li><a href="{r}privacy-policy/">Privacy Policy</a></li><li><a href="{r}accessibility/">Accessibility</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span><span>Independent Insurance Agency · Lake Orion, Michigan</span></div>
  </div></footer>
<script src="{r}assets/js/site.v2.js?v={VER}" defer></script>
</body>
</html>
"""
def body(cfg):
    src=f"{REL}assets/img/blog/{cfg['hero']}.avif"
    whatwedo="".join(f"<li><strong>{esc(b)}</strong> — {esc(rest)}</li>" for b,rest in cfg["whatwedo"])
    cov="".join(f"<li><strong>{esc(t)}</strong> — {esc(d)}</li>" for t,d in cfg["cov"])
    faqs="".join(f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-body"><p>{esc(a)}</p></div></details>\n' for q,a in cfg["faqs"])
    return f"""<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="{REL}">Home</a></li><li><a href="{REL}business/">Commercial Insurance</a></li><li>{esc(cfg['title'])}</li></ol></div></nav><main id="main">

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
      <span class="trust-band-item">20+ commercial carriers</span>
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

    <div class="callout">
      <h2>{esc(cfg['cta'])}</h2>
      <p>Tell us what you need and we'll shop your coverage across our markets. Most quotes back within one business day.</p>
      <a class="btn btn-primary btn-lg" href="{REL}quotes/">{esc(cfg['cta'])}</a>
    </div>
  </div>
</section>

</main>
"""
def build(cfg): return head(cfg)+UTIL+"\n"+header()+"\n"+body(cfg)+footer()
def generate():
    n=0
    for cfg in CONFIG:
        d=f"business/{cfg['slug']}"; out=f"{d}/index.html"
        if os.path.exists(out) and not FORCE: continue
        os.makedirs(d,exist_ok=True)
        safe_write(out,build(cfg).rstrip("\x00")); n+=1
        print(f"  business/{cfg['slug']}/  <- {cfg['title']}")
    print(f"Generated {n} pages.")
def wire():
    ov="business/index.html"; t=open(ov,encoding="utf-8").read(); orig=t
    # grid cards
    cards="".join(f'<a class="product-card" href="../business/{c["slug"]}/"><span class="icon">✓</span>{c["grid_label"]}</a>' for c in CONFIG if f'/business/{c["slug"]}/' not in t)
    anchor_card='<span class="icon">✓</span>One-Day Special Event</a></div>'
    if cards and anchor_card in t:
        t=t.replace(anchor_card,'<span class="icon">✓</span>One-Day Special Event</a>'+cards+'</div>',1)
    # definition blocks
    defs=""
    for c in CONFIG:
        if f'id="{c["def_id"]}"' in t: continue
        defs+=(f'<div class="product-definition" id="{c["def_id"]}">\n'
               f'  <h3><a href="#{c["def_id"]}">{c["grid_label"]}</a></h3>\n'
               f'  <p>{c["def_text"]}</p>\n'
               f'  <div class="product-actions"><a class="btn btn-secondary btn-sm" href="../business/{c["slug"]}/">Full details →</a> '
               f'<a class="btn btn-primary btn-sm" href="../quotes/">Get a quote for {c["grid_label"]}</a> '
               f'<a class="back-to-top" href="#products-list">↑ Back to coverage list</a></div>\n</div>\n')
    anchor_def='Get a quote for One-Day Special Event</a> <a class="back-to-top" href="#products-list">↑ Back to coverage list</a></div>\n</div></div>'
    if defs and anchor_def in t:
        t=t.replace(anchor_def,'Get a quote for One-Day Special Event</a> <a class="back-to-top" href="#products-list">↑ Back to coverage list</a></div>\n</div>'+defs+'</div>',1)
    if t!=orig: safe_write(ov, t.rstrip("\x00")); print("  wired business/index.html")
    # sitemap
    sm="sitemap.xml"; t=open(sm,encoding="utf-8").read(); add=""
    for c in CONFIG:
        loc=f"{SITE}/business/{c['slug']}/"
        if loc in t: continue
        add+=f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    if add: safe_write(sm, t.replace("</urlset>",add+"</urlset>").rstrip("\x00")); print(f"  +{add.count('<url>')} sitemap")
    # llms
    lt="llms.txt"; t=open(lt,encoding="utf-8").read(); add=""
    for c in CONFIG:
        u=f"{SITE}/business/{c['slug']}/"
        if u in t: continue
        add+=f"- {c['title']}: {u}\n"
    if add and "## More product pages" in t:
        safe_write(lt, t.replace("## More product pages\n","## More product pages\n"+add,1).rstrip("\x00")); print("  +llms")
if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "generate"
    (generate if mode=="generate" else wire)()
