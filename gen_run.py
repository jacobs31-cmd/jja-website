#!/usr/bin/env python3
"""One-off runner: builds the 11 niche product pages (same engine as gen_product_pages.py)."""
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
VER="20260613"
FORCE = (len(sys.argv)>2 and sys.argv[2]=="force")

CONFIG=[
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

REL="../../"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def head(cfg):
    sec_name="Commercial Insurance" if cfg["section"]=="business" else "Personal Insurance"
    sec_url=f"{SITE}/{cfg['section']}/"; url=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
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
        <p>Family-owned independent insurance agency serving Michigan since 1981. We shop 35+ carriers so you don&rsquo;t have to.</p>
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
    trust = "20+ commercial carriers" if cfg["section"]=="business" else "15+ personal lines carriers"
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
def build(cfg): return head(cfg)+UTIL+"\n"+header()+"\n"+body(cfg)+footer()
def generate():
    n=0
    for cfg in CONFIG:
        d=f"{cfg['section']}/{cfg['slug']}"; out=f"{d}/index.html"
        if os.path.exists(out) and not FORCE: continue
        os.makedirs(d,exist_ok=True)
        safe_write(out,build(cfg).rstrip("\x00")); n+=1
        print(f"  {cfg['section']}/{cfg['slug']}/  <- {cfg['title']}")
    print(f"Generated {n} pages.")
def wire():
    for section,ov in (("business","business/index.html"),("personal","personal/index.html")):
        t=open(ov,encoding="utf-8").read(); orig=t
        for cfg in CONFIG:
            if cfg["section"]!=section: continue
            page=f"../{section}/{cfg['slug']}/"; did=cfg["def_id"]
            pat=re.compile(r'(<div class="product-definition" id="'+re.escape(did)+r'">.*?<div class="product-actions">)(.*?)(</div>)',re.S)
            m=pat.search(t)
            if m and "/"+section+"/"+cfg["slug"]+"/" not in m.group(2):
                t=t[:m.start(2)]+f'<a class="btn btn-secondary btn-sm" href="{page}">Full details →</a> '+m.group(2)+t[m.end(2):]
        if t!=orig: safe_write(ov,t.rstrip("\x00")); print(f"  wired {ov}")
    sm="sitemap.xml"; t=open(sm,encoding="utf-8").read(); add=""
    for cfg in CONFIG:
        loc=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
        if loc in t: continue
        add+=f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-06-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    if add: safe_write(sm,t.replace("</urlset>",add+"</urlset>").rstrip("\x00")); print(f"  +{add.count('<url>')} sitemap")
    lt="llms.txt"; t=open(lt,encoding="utf-8").read(); add=""
    for cfg in CONFIG:
        u=f"{SITE}/{cfg['section']}/{cfg['slug']}/"
        if u in t: continue
        add+=f"- {cfg['title']}: {u}\n"
    if add and "## More product pages" in t:
        t=t.replace("## More product pages\n","## More product pages\n"+add,1)
        safe_write(lt,t.rstrip("\x00")); print("  +llms")
if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "generate"
    (generate if mode=="generate" else wire)()
