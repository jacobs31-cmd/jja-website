#!/usr/bin/env python3
"""Generates blog index + 10 individual blog post pages.

Posts are stored as Python data; HTML body content is preserved verbatim
from the original site (cleaned up). Each page gets the standard
J. Jacobs site shell (header/footer/breadcrumbs/SEO).

Run: python3 _build_blog.py
"""
from pathlib import Path
import re

SITE_URL = "https://www.jjainsurance.com"
PHONE_TEL = "+12486936455"
PHONE = "(248) 693-6455"
EMAIL = "Support@jjainsurance.com"
VERSION = "20260515e"

# ------------------------------------------------------------------
# Each post: slug, title, date (ISO), category, reading_time, summary, body_html
# ------------------------------------------------------------------
POSTS = [
    {
        "slug": "michigan-motorcycle-insurance-terminology",
        "title": "Michigan Motorcycle Insurance: The Complete Terminology Guide",
        "date": "2026-05-15", "date_display": "May 15, 2026",
        "category": "Insurance Education", "read_minutes": 5,
        "summary": "Michigan motorcycle insurance terms explained — lay-up policies, agreed value, CPE coverage, guest passenger liability, and no-fault rules. Updated for 2025 Michigan law.",
        "meta_description": "Michigan motorcycle insurance terms explained: lay-up policies, agreed value, CPE coverage, guest passenger liability & no-fault rules. Updated for 2025 Michigan law.",
        "body_html": """
<p class="lead">From lay-up policies to custom parts coverage, understanding the language of motorcycle insurance helps Michigan riders get the right protection for every mile of the season.</p>

<p>Michigan's riding season is short and sweet — and every week of it matters. Whether you're cruising M-22 along Lake Michigan or heading north for a long weekend, the right motorcycle policy keeps you protected from the moment your lay-up ends to the day you park it for winter.</p>

<p>Motorcycle insurance isn't just a modified auto policy. It has its own structure: seasonal lay-up provisions, custom parts endorsements, and a unique relationship with Michigan's no-fault system that every rider should understand. This guide explains every key term — in plain language — so you can choose coverage with confidence.</p>

<div class="callout-box">
<p><strong>Michigan Note:</strong> Motorcycle insurance under Michigan no-fault law works differently than standard auto coverage. The motorcycle itself does not provide Personal Injury Protection (PIP). Motorcyclists injured by a motor vehicle are covered under the motorist's PIP or through the Michigan Assigned Insurance Placement Facility (MAIPF). Michigan also requires helmets for riders under 21, or those without qualifying insurance and training documentation.</p>
</div>

<h3>🛡 3 Things to Check Before Your First Spring Ride</h3>
<ul>
  <li><strong>Confirm your lay-up period has ended.</strong> If your seasonal policy suspends collision and liability coverage during winter months, riding before reinstating those coverages leaves you unprotected. Verify your policy's exact reinstatement date — not just a rough estimate.</li>
  <li><strong>Review your Custom Parts &amp; Equipment (CPE) limit.</strong> Standard policies typically cap CPE coverage at $3,000. If you've added chrome, a custom exhaust, saddlebags, or a sound system over the winter, that limit may no longer be enough.</li>
  <li><strong>Check your guest passenger liability.</strong> Not all motorcycle policies automatically include coverage for a passenger's injury claims against you. If you plan to carry a passenger this season, verify this coverage is active.</li>
</ul>

<h2>Policy Basics</h2>
<dl class="term-list">
  <dt>Motorcycle Policy</dt><dd>A specialized insurance policy for motorcycles, motor scooters, and mopeds. Unlike standard auto policies, motorcycle policies include coverage specific to the riding season, custom parts, and passenger liability.</dd>
  <dt>Year-Round Policy</dt><dd>Provides full coverage including collision and liability throughout all 12 months, regardless of season.</dd>
  <dt>Lay-Up / Seasonal Policy</dt><dd>Michigan riders can suspend physical damage and liability coverage during non-riding months (typically November-March), retaining only comprehensive for fire and theft. Reduces annual premiums.</dd>
  <dt>Agreed Value</dt><dd>Insurer and insured agree upfront on the bike's value. If totaled, that full amount is paid without depreciation — the preferred valuation for custom and vintage bikes.</dd>
  <dt>Actual Cash Value (ACV)</dt><dd>Pays the depreciated market value at the time of loss. Standard settlement basis if agreed value is not selected.</dd>
</dl>

<h2>Liability &amp; Michigan No-Fault</h2>
<dl class="term-list">
  <dt>Bodily Injury Liability</dt><dd>Covers injuries the insured motorcyclist causes to others in an at-fault accident. Michigan minimums mirror auto: 50/100 ($50,000 per person / $100,000 per accident).</dd>
  <dt>Property Damage Liability</dt><dd>Covers damage the insured causes to others' property. Michigan minimum is $10,000.</dd>
  <dt>PIP &amp; Motorcycles</dt><dd>Michigan no-fault PIP applies differently to motorcycles. The motorcycle itself does not provide PIP; motorcyclists injured by a motor vehicle are covered under the motorist's PIP or the MAIPF. Motorcyclists must carry a valid endorsement.</dd>
  <dt>Guest Passenger Liability</dt><dd>Covers bodily injury claims made by a passenger against the operator. Verify this is included in the policy — some forms limit or exclude passenger claims.</dd>
</dl>

<h2>Physical Damage</h2>
<dl class="term-list">
  <dt>Collision Coverage</dt><dd>Pays for damage to the motorcycle from a collision with another vehicle or object. Subject to a deductible.</dd>
  <dt>Comprehensive Coverage</dt><dd>Covers non-collision losses including theft (a major concern for motorcycles), fire, vandalism, and weather events. Subject to a deductible.</dd>
  <dt>Total Loss Threshold</dt><dd>When repair cost exceeds a percentage (typically 75-80%) of the ACV or agreed value, the insurer declares a total loss and pays the insured value.</dd>
</dl>

<h2>Custom Parts &amp; Equipment</h2>
<dl class="term-list">
  <dt>Custom Parts &amp; Equipment (CPE)</dt><dd>Covers aftermarket add-ons such as custom chrome, saddlebags, non-standard exhausts, sound systems, and custom paint. Standard policies provide limited CPE coverage (typically $3,000); higher limits require an endorsement.</dd>
  <dt>OEM vs. Aftermarket Parts</dt><dd>OEM (Original Equipment Manufacturer) parts are factory-standard. CPE coverage addresses non-OEM modifications that increase the bike's value above its stock configuration.</dd>
  <dt>Accessories Coverage</dt><dd>Covers gear transported with the motorcycle such as additional helmets and luggage. Sublimits vary by carrier.</dd>
</dl>

<h2>Additional Coverages &amp; Endorsements</h2>
<dl class="term-list">
  <dt>Uninsured / Underinsured Motorist (UM/UIM)</dt><dd>Protects the motorcyclist against at-fault drivers with no or insufficient liability insurance. Strongly recommended given the severe injury exposure of motorcyclists.</dd>
  <dt>Roadside Assistance</dt><dd>Covers towing, battery jump, flat tire service, and fuel delivery for the motorcycle.</dd>
  <dt>Trip Interruption</dt><dd>Pays lodging and meal expenses if the motorcycle breaks down or is damaged more than a specified distance from home during a trip.</dd>
  <dt>Helmet &amp; Safety Apparel Coverage</dt><dd>Optional coverage for riding gear (helmets, jackets, gloves, boots) damaged in an accident.</dd>
  <dt>Track Day / Racing Exclusion</dt><dd>Most motorcycle policies exclude coverage for competitive racing or use on closed tracks. Separate track day insurance is required.</dd>
</dl>
"""
    },
    {
        "slug": "michigan-insurance-questions-answered",
        "title": "The 25 Insurance Questions Michigan Residents Ask Most",
        "date": "2026-05-15", "date_display": "May 15, 2026",
        "category": "Insurance Education", "read_minutes": 14,
        "summary": "Real answers from Michigan-licensed agents — on no-fault PIP, flood coverage, deer strikes, gap insurance, umbrella policies, and more.",
        "meta_description": "Michigan insurance experts answer the 25 most common coverage questions: no-fault PIP, flood, gap insurance, umbrella policies, deer strikes, and more.",
        "body_html": """
<p class="lead">Whether you're buying insurance for the first time or reviewing your existing coverage, the same questions come up again and again. Michigan's unique no-fault auto system, brutal winters, and abundance of lakes create coverage situations you won't find in many other states. Below, our Michigan-licensed agents answer the 25 questions customers ask us every single day — in plain language, without the jargon.</p>

<h2>Homeowners Insurance</h2>

<h3>1. Does my homeowners policy cover flood damage?</h3>
<p><strong>No — and this is one of the most costly misconceptions in insurance.</strong> Standard homeowners policies (HO-3 and all other HO forms) specifically exclude flooding, surface water, storm surge, and overflow from lakes and rivers. To be covered for flood, Michigan homeowners must purchase a separate flood policy through the National Flood Insurance Program (NFIP) or a private flood insurer. Even if you don't live in a designated flood zone, flooding can happen.</p>

<h3>2. Am I covered if a tree falls on my house?</h3>
<p><strong>Yes, in most cases.</strong> If a tree falls and damages your home due to a covered peril like windstorm, your homeowners policy will pay to repair the structure under Coverage A — subject to your deductible. Most policies also include a sublimit (typically $500-$1,000) for debris removal. If a neighbor's tree falls on your home, your own policy still pays first. You'd only have a claim against your neighbor if they were negligent (e.g., the tree was visibly dead and previously reported).</p>

<h3>3. Does homeowners insurance cover mold?</h3>
<p><strong>It depends on how the mold got there.</strong> Mold resulting from a sudden and accidental covered peril — like a burst pipe — is generally covered. But mold caused by long-term moisture problems, poor maintenance, or a slow undetected leak is considered a maintenance issue and is excluded. Some policies offer a limited mold remediation endorsement (typically $5,000-$10,000).</p>

<h3>4. Does homeowners insurance cover sewer backup?</h3>
<p><strong>Not automatically — and this is a major coverage gap in Michigan.</strong> Standard policies exclude damage from water or sewage that backs up through drains and sewers. This is one of the most commonly purchased endorsements in Michigan, where aging combined sewer systems cause frequent backup events. Coverage typically runs $50-$150 per year — a small cost compared to a $15,000 basement cleanup.</p>

<h3>5. Is my home-based business covered under my homeowners policy?</h3>
<p><strong>Generally, no.</strong> Standard homeowners policies either exclude or severely limit coverage for business activities at the home. Business equipment may be subject to a small sublimit (often $2,500) and business liability is typically excluded entirely. If you run a home-based business — day care, photography, consulting, online retail — you need either a home business endorsement or a separate businessowners policy (BOP).</p>

<h3>6. Is my jewelry covered under my homeowners policy?</h3>
<p><strong>Only to a limited extent.</strong> Standard policies include sublimits — typically $1,500 for theft. An engagement ring worth $8,000 would be dramatically underinsured. Schedule valuable items individually with a jewelry floater for full appraised value coverage with no deductible.</p>

<h3>7. How much homeowners insurance do I actually need?</h3>
<p><strong>Insure for replacement cost — not market value or assessed value.</strong> An older Michigan home with a market value of $150,000 may cost $220,000 or more to rebuild at current construction prices. Insure to at least 80% of replacement cost to avoid a coinsurance penalty.</p>

<h2>Auto Insurance &amp; No-Fault</h2>

<h3>8. Michigan is no-fault — do I still need liability insurance?</h3>
<p><strong>Yes, absolutely.</strong> Michigan minimums are $50,000/$100,000 BI and $10,000 PD. Without liability insurance, you're personally responsible for damages you cause to others, and driving without required insurance in Michigan is a misdemeanor.</p>

<h3>9. What PIP level should I choose in Michigan?</h3>
<p><strong>Your health insurance situation determines the right answer.</strong> Unlimited PIP is best for those without strong health coverage. $500,000 or $250,000 work if you have comprehensive employer group health. $50,000 is only available if you're on Medicaid. PIP Opt-Out requires Medicare Parts A and B. A serious auto injury can generate millions in lifetime medical costs — never choose a lower PIP limit without confirming the client has qualifying health coverage to fill the gap.</p>

<h3>10. Does my auto insurance cover hitting a deer?</h3>
<p><strong>Yes — but only if you carry comprehensive coverage.</strong> Deer strikes are covered under comprehensive, not collision. Michigan is consistently in the top 10 states for deer-vehicle collisions. If you swerve to avoid a deer and hit a guardrail or tree, that's a collision claim, not comprehensive.</p>

<h3>11. What is gap insurance and do I need it?</h3>
<p><strong>Gap insurance covers the difference between what your insurer pays for a totaled vehicle and what you still owe on the loan or lease.</strong> New vehicles depreciate 15-25% in the first year. Recommended for clients who financed with a small down payment, have a long loan term, leased, or purchased a model that depreciates quickly.</p>

<h3>12. Does my auto policy cover me if someone else drives my car?</h3>
<p><strong>In Michigan, auto insurance generally follows the vehicle, not the driver.</strong> If you give someone permission to drive your car, your policy is primary. Household members must be listed on the policy or explicitly excluded. Lending to someone with a suspended license or intoxicated person could give the insurer grounds to deny the claim.</p>

<h3>13. Will a traffic ticket raise my insurance rates?</h3>
<p><strong>It depends on the type of violation, the carrier, and your prior record.</strong> Minor violations may have no impact after a first offense. Serious violations — excessive speeding, reckless driving, DUI — typically result in surcharges of 20-50% or more.</p>

<h3>14. Am I covered if I drive for Uber or Lyft?</h3>
<p><strong>Your personal auto policy will NOT cover you while actively working as a rideshare driver.</strong> Add a rideshare endorsement to close the Period 1 gap (app on, waiting for ride). The TNC's commercial policy covers Periods 2-3 (ride accepted through drop-off).</p>

<h3>15. Does my auto insurance cover a rental car?</h3>
<p><strong>Generally yes — but only to the extent of your existing coverages.</strong> If you carry only liability, physical damage to the rental would not be covered. The rental company's Collision Damage Waiver (CDW) is not insurance — it's a contract waiving their claim against you.</p>

<h2>Renters &amp; Landlord Insurance</h2>

<h3>16. Does renters insurance cover my roommate's belongings?</h3>
<p><strong>No.</strong> A renters insurance policy (HO-4) covers only the named insured and resident household members related to them. An unrelated roommate — even one on the lease — needs their own separate policy.</p>

<h3>17. Does renters or homeowners insurance cover my laptop if stolen outside my home?</h3>
<p><strong>Yes, with limitations.</strong> Personal property coverage extends to belongings stolen away from home. Standard policies pay actual cash value (depreciated). Electronics from a vehicle may be subject to sublimits.</p>

<h3>18. Does my landlord policy cover my tenant's belongings?</h3>
<p><strong>Absolutely not.</strong> A landlord policy covers the building, the landlord's furnishings, the landlord's liability, and lost rental income — never tenants' personal property. This is why many landlords require renters insurance as a lease condition.</p>

<h3>19. Am I covered if my dog bites someone?</h3>
<p><strong>Yes, in most cases — but breed restrictions apply.</strong> Homeowners liability includes dog bite coverage. The average claim exceeds $50,000. Many Michigan insurers have breed exclusions (pit bulls, Rottweilers, Dobermans, German Shepherds, and others).</p>

<h2>Umbrella Insurance</h2>

<h3>20. Do I really need an umbrella policy if I already have high liability limits?</h3>
<p><strong>Yes — and it costs far less than most people expect.</strong> A personal umbrella provides $1 million or more in additional liability above your auto and home limits for $150-$300 per year. In today's litigation environment, a serious auto accident, pool injury, or significant dog bite can easily exceed $300,000.</p>

<h2>Seasonal &amp; Specialty Vehicles</h2>

<h3>21. Am I covered year-round even if I only use my boat, motorcycle, or RV seasonally?</h3>
<p><strong>It depends on how the policy is structured.</strong> Many seasonal vehicle policies offer a lay-up provision that suspends collision and liability during the off-season. Physical damage coverage must be active when the vehicle is being used.</p>

<h2>Insurance Policy Basics</h2>

<h3>22. What is the difference between ACV and replacement cost?</h3>
<p><strong>The most important valuation concept in insurance.</strong> ACV pays the depreciated value. RCV pays what it costs to replace the property with a new equivalent at today's prices, with no depreciation deduction. A 10-year-old roof damaged by hail: ACV might pay $4,000 after depreciation; RCV would pay $14,000 to install a new roof.</p>

<h3>23. What happens to my claim if my damage doesn't exceed my deductible?</h3>
<p><strong>If total damage is at or below your deductible, the insurer pays nothing.</strong> Filing a claim — even with no payment — creates a record in the CLUE database that can affect your renewal premium. Self-insure small losses whenever possible.</p>

<h3>24. What is subrogation and how does it affect my claim?</h3>
<p><strong>Subrogation is your insurer's right to recover claim payments from a responsible third party.</strong> If a negligent contractor causes a fire at your home, your insurer pays your claim then pursues the contractor. Do not independently settle with a responsible third party and release them from liability — it can eliminate your insurer's subrogation rights.</p>

<h3>25. What is the difference between cancellation and non-renewal?</h3>
<p><strong>Cancellation terminates the policy before its expiration date. Non-renewal means the insurer declines to offer coverage for the next term.</strong> In Michigan, mid-term cancellation is permitted only for nonpayment (10 days written notice), fraud, or statutory grounds. Non-renewal requires at least 30 days advance written notice under MCL 500.3220.</p>
"""
    },
    {
        "slug": "michigan-auto-insurance-glossary",
        "title": "Michigan Auto Insurance Terminology Guide",
        "date": "2026-05-15", "date_display": "May 15, 2026",
        "category": "Insurance Education", "read_minutes": 6,
        "summary": "Every key auto insurance term defined — from Michigan's unique no-fault PIP tiers and liability minimums to physical damage coverage, endorsements, and underwriting concepts.",
        "meta_description": "Confused by the no-fault system? J. Jacobs and Associates explains Michigan auto insurance terms, PIP choices, and liability limits in plain language.",
        "body_html": """
<p class="lead">Michigan has one of the most complex auto insurance systems in the country. Our unique no-fault law — significantly overhauled in July 2020 — means Michigan drivers face choices and coverage rules that don't exist anywhere else. Understanding the terminology is the first step to making smart coverage decisions.</p>

<div class="callout-box">
<p><strong>Michigan-Specific Note:</strong> Michigan's No-Fault Insurance Act (MCL 500.3101 et seq.) was substantially reformed in 2019, with the most significant changes taking effect July 2, 2020. PIP coverage tiers, minimum liability limits, and the MCCA surcharge structure all changed. All definitions below reflect current Michigan law as of 2025.</p>
</div>

<h2>Michigan No-Fault System</h2>
<dl class="term-list">
  <dt>No-Fault Insurance</dt><dd>Michigan's auto system (MCL 500.3101 et seq.) under which each driver's own insurer pays their medical and wage-loss benefits after an accident regardless of fault. Overhauled in 2019; major changes effective July 2, 2020.</dd>
  <dt>Personal Injury Protection (PIP)</dt><dd>No-fault benefit covering medical expenses, wage loss (up to 85% of net income), replacement services, and funeral expenses for the insured and household members injured in an auto accident. Michigan now offers tiered PIP options.</dd>
  <dt>PIP — Unlimited</dt><dd>Provides lifetime, unlimited medical coverage. Previously mandatory for all Michigan drivers; now optional but remains the most comprehensive protection available.</dd>
  <dt>PIP — $500,000 Limit</dt><dd>Caps PIP medical at $500,000 per person per accident. A lower-cost option for insureds with comprehensive employer health insurance.</dd>
  <dt>PIP — $250,000 Limit</dt><dd>Caps PIP medical at $250,000. Can be selected with a PIP medical exclusion if the insured has qualifying health coverage that will act as primary.</dd>
  <dt>PIP — $50,000 Limit</dt><dd>Available only to Medicaid-eligible insureds. Medicaid becomes the primary payer after the PIP limit is exhausted.</dd>
  <dt>PIP Opt-Out (Medicare)</dt><dd>Drivers covered under both Medicare Parts A and B may opt out of PIP medical coverage entirely, eliminating that portion of the premium.</dd>
  <dt>MCCA (Michigan Catastrophic Claims Association)</dt><dd>State-mandated association that reimburses insurers for PIP medical claims exceeding a set threshold (currently $600,000). Every Michigan insurer must be a member.</dd>
  <dt>Tort Threshold / Residual Liability</dt><dd>Under Michigan no-fault, an injured party may sue the at-fault driver for non-economic damages only if the injury meets the serious impairment threshold under MCL 500.3135.</dd>
  <dt>Mini-Tort</dt><dd>Allows a Michigan driver to recover up to $3,000 from an at-fault driver for vehicle damage not covered by the driver's own collision insurance.</dd>
</dl>

<h2>Liability Coverage</h2>
<dl class="term-list">
  <dt>Bodily Injury Liability (BI)</dt><dd>Pays for injuries caused to others when the insured is at fault. Michigan minimums (as of 2020) are 50/100 — $50,000 per person and $100,000 per accident.</dd>
  <dt>Property Damage Liability (PD)</dt><dd>Pays for damage the insured causes to another person's property. Michigan minimum is $10,000.</dd>
  <dt>Split Limits</dt><dd>Liability expressed as three numbers: bodily injury per person / bodily injury per accident / property damage per accident (e.g., 100/300/100).</dd>
  <dt>Combined Single Limit (CSL)</dt><dd>A single liability limit that applies to both bodily injury and property damage combined.</dd>
</dl>

<h2>Physical Damage Coverage</h2>
<dl class="term-list">
  <dt>Collision Coverage</dt><dd>Pays for damage to the insured's vehicle caused by a collision with another vehicle or object, or by the vehicle overturning. Subject to a deductible.</dd>
  <dt>Comprehensive Coverage</dt><dd>Pays for non-collision losses including theft, fire, vandalism, hail, falling objects, and animal strikes. Subject to a deductible.</dd>
  <dt>Gap Coverage</dt><dd>Pays the difference between a totaled vehicle's ACV and the outstanding loan or lease balance. Especially important for new vehicles.</dd>
  <dt>Total Loss</dt><dd>When repair cost plus salvage value exceeds the vehicle's ACV, it is declared a total loss. Michigan insurers typically apply a 75-80% damage-to-value threshold.</dd>
  <dt>New Car Replacement</dt><dd>If a new vehicle is totaled within the first one to two model years, pays for a brand-new replacement rather than the depreciated ACV.</dd>
</dl>

<h2>Additional Coverages &amp; Endorsements</h2>
<dl class="term-list">
  <dt>Uninsured Motorist (UM)</dt><dd>Pays for the insured's injuries caused by a driver with no liability insurance. In Michigan, UM applies to bodily injury since PIP covers most medical expenses.</dd>
  <dt>Underinsured Motorist (UIM)</dt><dd>Pays when the at-fault driver's liability limits are insufficient to cover all of the insured's damages.</dd>
  <dt>Rental Reimbursement</dt><dd>Covers rental vehicle costs while the insured's car is being repaired after a covered loss. Typical limits are $30-$50 per day for up to 30 days.</dd>
  <dt>Towing &amp; Labor</dt><dd>Pays for emergency roadside assistance including towing, flat tire changes, lockout service, and fuel delivery.</dd>
  <dt>Rideshare Endorsement</dt><dd>Fills the coverage gap when a driver is logged into a TNC app (Uber, Lyft) but has not yet accepted a ride.</dd>
  <dt>Named Driver Exclusion</dt><dd>Excludes a specific household driver from all policy coverage.</dd>
</dl>

<h2>Rating &amp; Underwriting</h2>
<dl class="term-list">
  <dt>Named Insured</dt><dd>The person or entity listed on the declarations page as the primary policyholder.</dd>
  <dt>Motor Vehicle Record (MVR)</dt><dd>A driver's license history showing violations and accidents. Pulled by insurers during underwriting and at renewal.</dd>
  <dt>Credit-Based Insurance Score</dt><dd>Michigan allows insurers to use credit information as a rating factor.</dd>
  <dt>Rating Territory</dt><dd>The geographic area where the vehicle is principally garaged.</dd>
  <dt>SR-22</dt><dd>A certificate of financial responsibility required by Michigan DLSOS for high-risk drivers.</dd>
  <dt>Policy Period</dt><dd>The dates during which coverage is in force, typically six months or one year for personal auto policies.</dd>
</dl>
"""
    },
    {
        "slug": "michigan-homeowners-insurance-glossary",
        "title": "Michigan Homeowners Insurance Terminology Guide",
        "date": "2026-05-15", "date_display": "May 15, 2026",
        "category": "Insurance Education", "read_minutes": 6,
        "summary": "Every homeowners insurance term explained — policy forms HO-1 through HO-8, Coverage A through F, valuation methods, exclusions, endorsements, and Michigan-specific policy conditions.",
        "meta_description": "Michigan homeowners insurance terms explained: HO-1 through HO-8, Coverage A-F, replacement cost vs. ACV, flood exclusions, sewer backup, and more.",
        "body_html": """
<p class="lead">Your homeowners policy is likely the most important insurance policy you own — and also one of the most misunderstood. Many Michigan homeowners don't know what their policy actually covers until they have a claim, and by then it's too late to change it. This glossary defines every key term in a Michigan homeowners insurance policy.</p>

<div class="callout-box">
<p><strong>Michigan Homeowners Note:</strong> Michigan's climate creates unique exposures — sewer backup from aging combined sewers, ice dam damage, and flooding near the Great Lakes and inland waterways. Review your endorsements carefully and ask your agent about coverage gaps specific to your area.</p>
</div>

<h3>The 3 Most Common Michigan Homeowners Coverage Gaps</h3>
<ul>
  <li><strong>Flood damage</strong> — excluded on all standard HO policies; requires a separate NFIP or private flood policy</li>
  <li><strong>Sewer &amp; drain backup</strong> — excluded by default; add the endorsement for ~$50-$150/year</li>
  <li><strong>Underinsurance</strong> — insuring to market value instead of full replacement cost leaves you short at claim time</li>
</ul>

<h2>Core Policy Forms</h2>
<dl class="term-list">
  <dt>Homeowners Policy (HO)</dt><dd>A package insurance policy combining property and liability coverage. Michigan homeowners most commonly carry HO-3 policies.</dd>
  <dt>HO-1 — Basic Form</dt><dd>A limited named-perils policy covering only 10 specific perils. Rarely written today.</dd>
  <dt>HO-2 — Broad Form</dt><dd>A named-perils policy covering the dwelling and personal property against 16 specified perils.</dd>
  <dt>HO-3 — Special Form</dt><dd>The most common homeowners form. Covers the dwelling on an open-perils basis and personal property on a named-perils basis. The Michigan market standard.</dd>
  <dt>HO-4 — Renters Form</dt><dd>Designed for tenants; covers personal property and liability but not the structure.</dd>
  <dt>HO-5 — Comprehensive Form</dt><dd>Provides open-perils coverage for both the dwelling and personal property. The broadest protection available.</dd>
  <dt>HO-6 — Condo Unit Owner</dt><dd>Covers the interior of a condominium unit, personal property, and personal liability.</dd>
  <dt>HO-8 — Modified Coverage</dt><dd>Used for older homes where replacement cost exceeds market value. Pays the lesser of repair cost or ACV.</dd>
</dl>

<h2>Coverage Components (A-F)</h2>
<dl class="term-list">
  <dt>Coverage A — Dwelling</dt><dd>Covers the physical structure including walls, roof, floors, built-in appliances, and attached structures. Insure to at least 80% of replacement cost.</dd>
  <dt>Coverage B — Other Structures</dt><dd>Covers detached structures such as fences, sheds, and detached garages. Typically 10% of Coverage A.</dd>
  <dt>Coverage C — Personal Property</dt><dd>Covers the insured's belongings both on and away from the premises. Special sublimits apply to jewelry, cash, firearms, and collectibles.</dd>
  <dt>Coverage D — Loss of Use</dt><dd>Pays additional living expenses when a covered loss makes the home uninhabitable during repairs.</dd>
  <dt>Coverage E — Personal Liability</dt><dd>Protects the insured against bodily injury or property damage claims by third parties, including legal defense costs.</dd>
  <dt>Coverage F — Medical Payments</dt><dd>Pays reasonable medical expenses for guests injured on the premises regardless of fault. Typical limits are $1,000-$5,000.</dd>
</dl>

<h2>Valuation &amp; Settlement</h2>
<dl class="term-list">
  <dt>Replacement Cost Value (RCV)</dt><dd>The cost to repair or replace damaged property with new materials of like kind and quality at current prices, without deducting depreciation.</dd>
  <dt>Actual Cash Value (ACV)</dt><dd>Replacement cost minus depreciation. Produces lower claim payments than RCV.</dd>
  <dt>Agreed Value</dt><dd>Insurer and insured agree upfront on the insured value; no coinsurance penalty applies.</dd>
  <dt>Extended Replacement Cost</dt><dd>Provides coverage above the policy limit (typically 20-50%) if rebuilding costs spike after a major disaster.</dd>
  <dt>Guaranteed Replacement Cost</dt><dd>Pays the full cost to rebuild regardless of the policy limit.</dd>
  <dt>Coinsurance — 80% Rule</dt><dd>Requires the homeowner to insure the dwelling to at least 80% of replacement cost.</dd>
  <dt>Depreciation</dt><dd>Decrease in value due to age, wear, and obsolescence. Withheld from ACV payments; may be recoverable after repairs.</dd>
  <dt>Recoverable Depreciation</dt><dd>The withheld depreciation amount the insured can recover by completing repairs and submitting documentation.</dd>
</dl>

<h2>Perils, Exclusions &amp; Endorsements</h2>
<dl class="term-list">
  <dt>Open Perils (All-Risk)</dt><dd>Covers all causes of loss except those specifically excluded.</dd>
  <dt>Named Perils</dt><dd>Covers only the specific causes of loss listed in the policy.</dd>
  <dt>Flood Exclusion</dt><dd>Standard homeowners policies exclude flooding from external sources.</dd>
  <dt>Sewer Backup Endorsement</dt><dd>Optional coverage for water or sewage backing up through drains.</dd>
  <dt>Service Line Coverage</dt><dd>Covers repair of utility service lines running from the street to the home.</dd>
  <dt>Scheduled Personal Property (Floater)</dt><dd>Separately insuring high-value items beyond standard sublimits, often with broader perils and no deductible.</dd>
  <dt>Home Business Endorsement</dt><dd>Provides limited coverage for business equipment and liability for home-based businesses.</dd>
  <dt>Equipment Breakdown</dt><dd>Covers mechanical or electrical failure of home systems (HVAC, water heater, appliances).</dd>
</dl>

<h2>Policy Conditions &amp; Michigan Law</h2>
<dl class="term-list">
  <dt>Deductible</dt><dd>The insured's out-of-pocket share before the insurer pays. Higher deductibles reduce premiums.</dd>
  <dt>Wind / Hail Deductible</dt><dd>A separate deductible — often a percentage of Coverage A — applying specifically to wind or hail damage.</dd>
  <dt>Mortgagee Clause</dt><dd>Protects the lender's interest in the property.</dd>
  <dt>Subrogation</dt><dd>The insurer's right to pursue a responsible third party after paying a claim.</dd>
  <dt>Cancellation (MCL 500.3220)</dt><dd>Michigan law requires written notice — typically 10 days for nonpayment and 30 days for other reasons.</dd>
  <dt>Non-renewal</dt><dd>Insurer's decision not to continue the policy at expiration. Michigan requires at least 30 days advance written notice.</dd>
  <dt>Proof of Loss</dt><dd>A formal, sworn statement by the insured detailing the nature, date, and amount of a loss.</dd>
</dl>
"""
    },
    {
        "slug": "michigan-no-fault-option-6",
        "title": "Michigan No-Fault Option 6: What Medicare Covers and What It Doesn't",
        "date": "2025-09-18", "date_display": "September 18, 2025",
        "category": "Auto Insurance", "read_minutes": 3,
        "summary": "Choosing Option 6 to use Medicare instead of PIP in Michigan? Explore the risks, coverage gaps, and potential out-of-pocket costs before you decide.",
        "meta_description": "Choosing Option 6 to use Medicare instead of PIP in Michigan? Explore the risks, coverage gaps, and potential out-of-pocket costs before you opt out of no-fault medical benefits.",
        "body_html": """
<p class="lead">Michigan's auto insurance reforms allow drivers with Medicare to opt out of their Personal Injury Protection (PIP) medical coverage, known as Option 6. This can lower your car insurance premium, but it is critical to understand the serious limitations and risks involved before choosing this option.</p>

<h2>What Option 6 means for your coverage</h2>
<p>By selecting Option 6, you are essentially telling your auto insurance company that <strong>Medicare Parts A and B will be your primary and sole medical coverage</strong> for any injuries sustained in a car accident. Your auto policy will pay nothing toward your medical care, regardless of who was at fault.</p>

<h2>Requirements to qualify for Option 6</h2>
<p>This is not a straightforward choice. To be eligible for Option 6, strict conditions apply to you and everyone in your household:</p>
<ul>
  <li><strong>Named Insured:</strong> You, as the named insured on the policy, must be enrolled in both Medicare Parts A and B.</li>
  <li><strong>Household Members:</strong> Your spouse and any resident relatives must also have "qualified health coverage." This can include another auto policy with PIP medical coverage, their own Medicare coverage, or a private health insurance plan that covers auto accident injuries.</li>
</ul>

<h2>What Medicare covers after a car accident</h2>
<p>While Medicare does cover medically necessary treatment for car accident injuries, it is not a complete replacement for robust PIP coverage:</p>
<ul>
  <li><strong>Medicare Part A (Hospital):</strong> Covers inpatient hospital stays, skilled nursing facility care, and hospice care related to your injuries.</li>
  <li><strong>Medicare Part B (Medical):</strong> Covers medically necessary services like doctor visits, emergency room treatment, diagnostic tests, ambulance transportation, and durable medical equipment.</li>
</ul>

<h2>Gaps and financial risks of choosing Option 6</h2>
<p>Relying solely on Medicare for an auto accident can leave you with significant out-of-pocket costs and no coverage for vital long-term care services.</p>
<ul>
  <li><strong>Out-of-Pocket Expenses:</strong> You will be responsible for Medicare's standard deductibles, copayments, and other cost-sharing expenses.</li>
  <li><strong>Missing Services:</strong> Medicare does not cover many essential services that are often required for serious car accident injuries:
    <ul>
      <li>Long-term or in-home attendant care</li>
      <li>Residential treatment facilities</li>
      <li>Home and vehicle modifications for accessibility</li>
      <li>Long-term rehabilitation or physical therapy that exceeds Medicare limits</li>
      <li>Dental coverage</li>
    </ul>
  </li>
  <li><strong>Medicare's Right to Reimbursement:</strong> If you receive a personal injury settlement, Medicare has a right to be reimbursed for any payments it made on your behalf.</li>
</ul>

<h2>What your auto policy still covers</h2>
<p>Even with Option 6, your auto policy still provides important benefits:</p>
<ul>
  <li><strong>Bodily Injury Liability:</strong> Protects you from lawsuits if you cause an accident and are found liable.</li>
  <li><strong>Property Protection (PPI):</strong> Covers damage your car does to other people's property.</li>
  <li><strong>Lost Wages and Replacement Services:</strong> Provides compensation for lost income and help with household chores, typically capped at three years.</li>
</ul>
"""
    },
    {
        "slug": "what-happens-if-you-skip-your-workers-comp-audit-in-michigan",
        "title": "What Happens If You Skip Your Workers' Comp Audit in Michigan?",
        "date": "2025-09-18", "date_display": "September 18, 2025",
        "category": "Workers Comp", "read_minutes": 3,
        "summary": "Avoid severe penalties for a missed workers' comp audit in Michigan. Learn about the financial, legal, and insurance consequences for Michigan business owners.",
        "meta_description": "Avoid severe penalties for a missed workers' comp audit in Michigan. Learn about the financial, legal, and insurance consequences for Michigan business owners.",
        "body_html": """
<p class="lead">Avoiding your workers' compensation audit can lead to serious consequences for your Michigan business. Learn how to prevent significant financial penalties, coverage cancellation, and legal liability by staying compliant.</p>

<h2>Understanding the Workers' Comp Audit</h2>
<p>An insurance audit verifies that you paid the correct premium for your workers' compensation coverage. By law, Michigan business owners must carry this insurance for their employees. The audit process involves checking your actual payroll and employee classification codes against the estimates used to calculate your premium.</p>

<h2>Risks of skipping your Michigan workers' comp audit</h2>
<p>Refusing or ignoring a workers' compensation audit is a violation of your policy and Michigan state law. The consequences can be severe and escalate quickly.</p>
<ul>
  <li><strong>Higher estimated premiums.</strong> Your insurer will likely assign you a much higher premium, estimating your payroll using the highest possible rates and the riskiest classification codes.</li>
  <li><strong>Mandatory surcharges.</strong> If you get coverage through Michigan's assigned risk pool, you may face a mandatory non-compliance charge — possibly double your estimated annual premium.</li>
  <li><strong>Collection action.</strong> If you do not pay, your insurer can send your account to collections, harming your business's credit.</li>
  <li><strong>Policy cancellation.</strong> Failing to cooperate with an audit is grounds for your insurer to cancel your policy mid-term — leaving your business illegally uninsured.</li>
  <li><strong>Difficulty finding new coverage.</strong> With a non-compliant cancellation on your record, you may be flagged as high-risk.</li>
  <li><strong>State-imposed fines.</strong> Operating without workers' compensation coverage is illegal in Michigan and can result in significant fines and penalties.</li>
  <li><strong>Personal liability for injuries.</strong> If your coverage is canceled and an employee gets injured on the job, you could be personally liable.</li>
</ul>

<h2>What to do if you missed your audit deadline</h2>
<ol>
  <li><strong>Contact your insurer immediately.</strong> Get in touch with your insurance carrier or agent to explain the situation and reschedule the audit.</li>
  <li><strong>Gather all necessary documents.</strong> Have your payroll records, tax forms (like 941s), and employee information ready to demonstrate a good-faith effort to comply.</li>
  <li><strong>Address the issue promptly.</strong> Your insurer prefers to complete the audit and determine an accurate premium rather than resort to drastic measures.</li>
</ol>

<h2>Conclusion</h2>
<p>Ignoring a workers' compensation audit in Michigan is not a viable option for any business. The potential financial, insurance, and legal risks far outweigh the inconvenience of completing the process. By communicating proactively with your insurance provider, you can ensure your business remains protected and compliant with state law.</p>
"""
    },
    {
        "slug": "michigan-workers-compensation-do-you-need-it-guide-for-business-owners",
        "title": "Do I Need Workers' Compensation Insurance in Michigan? A Guide for Small Businesses",
        "date": "2025-09-17", "date_display": "September 17, 2025",
        "category": "Workers Comp", "read_minutes": 2,
        "summary": "Is workers' comp required for your small business in Michigan? Learn the criteria for mandatory coverage, exemptions, and the risks of non-compliance.",
        "meta_description": "Is workers' comp required for your small business in Michigan? Learn the criteria for mandatory coverage, exemptions for sole proprietors and family members, and the risks of non-compliance.",
        "body_html": """
<p class="lead">For most Michigan employers, having workers' compensation insurance is a legal requirement. Understanding the rules is crucial for protecting your business and your employees. This guide covers the key criteria for Michigan workers' comp and outlines the potential risks of going without it.</p>

<h2>When is workers' comp mandatory in Michigan?</h2>
<p>Your business must carry workers' compensation coverage if you meet any of the following conditions:</p>
<ul>
  <li><strong>Three or more employees</strong> at any single time. This includes part-time staff.</li>
  <li><strong>One or more employees</strong> who work 35 hours or more per week for 13 weeks or longer during a year.</li>
  <li>You are a <strong>public employer</strong>, such as a government agency or a school district.</li>
</ul>

<h2>Are there exemptions for small businesses?</h2>
<p>Yes, some employers are not required to carry workers' comp insurance. However, if you do hire employees, the requirements listed above will apply.</p>
<ul>
  <li><strong>Sole proprietors and partners</strong> are not considered employees of their own business and are not required to cover themselves.</li>
  <li><strong>Family members</strong> may be exempt in specific situations, though it's important to check the details.</li>
  <li><strong>Agricultural and domestic workers</strong> have special rules that depend on the number of hours they work.</li>
</ul>

<h2>What are the risks of skipping workers' comp?</h2>
<p>Operating without the proper insurance is a serious offense in Michigan:</p>
<ul>
  <li><strong>Hefty fines:</strong> You could face fines of up to $1,000 for each day you are uninsured.</li>
  <li><strong>Employee lawsuits:</strong> If an employee is injured on the job, they can sue you directly. You would be personally liable for their medical bills and lost wages.</li>
  <li><strong>Business shutdown:</strong> The state can issue a stop-work order, forcing your business to shut down until you obtain the required insurance.</li>
</ul>

<h2>Is workers' comp a smart choice even if you're exempt?</h2>
<p>Even if your business falls under an exemption, carrying workers' compensation insurance is often a wise decision. It provides essential protection from financial devastation in the event of a workplace injury — an investment in your company's security and your employees' well-being.</p>
"""
    },
    {
        "slug": "common-auto-insurance-terms",
        "title": "Common Michigan Auto Insurance Terms Explained for Drivers",
        "date": "2025-09-15", "date_display": "September 15, 2025",
        "category": "Auto Insurance", "read_minutes": 4,
        "summary": "Navigating your auto insurance policy can be confusing — especially with Michigan's no-fault system. This guide explains deductibles, liability, and PIP coverage in plain language.",
        "meta_description": "Confused by Michigan's no-fault auto insurance? This guide breaks down deductibles, liability, and PIP coverage options in plain language.",
        "body_html": """
<p class="lead">Navigating your auto insurance policy can be confusing, especially with unique requirements like Michigan's no-fault system. This guide explains common car insurance terms in plain language, helping you understand your coverage options, including deductibles, liability, and Personal Injury Protection (PIP) in Michigan.</p>

<h2>Deductible: Your Share of the Cost</h2>
<p>A <strong>deductible</strong> is the amount you pay out-of-pocket on a claim before your insurance company starts to pay. For example, if you have a $1,000 deductible for collision repairs and the total damage is $2,500, you pay the first $1,000, and your insurance covers the remaining $1,500.</p>

<h2>Bodily Injury Liability Coverage in Michigan</h2>
<p>In Michigan, <strong>Bodily Injury (BI) liability</strong> insurance is also known as "residual liability" coverage. It covers the costs of injuries you cause to other people in an accident. While Michigan is a no-fault state, this coverage is essential because you can still be sued in certain situations.</p>

<h3>Michigan's No-Fault System and BI Liability</h3>
<ul>
  <li><strong>No-Fault vs. At-Fault:</strong> Under Michigan's no-fault law, your own insurance's PIP typically pays for your medical bills and lost wages, regardless of who caused the accident.</li>
  <li><strong>When You Can Be Sued:</strong> Your BI liability coverage kicks in when someone files a lawsuit against you after an accident involving serious injuries.</li>
  <li><strong>BI Coverage Pays For:</strong>
    <ul>
      <li>Pain and suffering compensation</li>
      <li>Excess medical bills exceeding the at-fault driver's PIP coverage</li>
      <li>Excess lost wages for the injured party</li>
    </ul>
  </li>
</ul>

<h3>Understanding BI Coverage Limits</h3>
<p>Your policy will show BI limits as two numbers, such as <strong>$250,000/$500,000</strong>:</p>
<ul>
  <li><strong>$250,000 per person:</strong> The maximum amount your insurance will pay for one person's injuries.</li>
  <li><strong>$500,000 per accident:</strong> The maximum total amount your insurance will pay for all injuries in a single accident.</li>
  <li><strong>Michigan Law Changes (2020):</strong> Drivers can select their BI limits, with $250,000/$500,000 being the default. We recommend higher coverage for better financial protection.</li>
</ul>

<h2>Uninsured/Underinsured Motorist (UM/UIM) Coverage</h2>
<p>This vital coverage protects you and your passengers if you're in an accident with a driver who is either uninsured or underinsured. Your <strong>UM/UIM coverage</strong> can help pay for medical expenses, lost wages, and pain and suffering.</p>

<h2>Personal Injury Protection (PIP) in Michigan</h2>
<p>As part of Michigan's no-fault system, <strong>PIP coverage</strong> pays for your medical expenses and lost wages if you are injured in a car accident, regardless of who was at fault.</p>
<ul>
  <li><strong>PIP Covers:</strong>
    <ul>
      <li>Medical care (doctor visits, hospital stays, physical therapy)</li>
      <li>Lost wages (up to 85% of your income for up to three years)</li>
      <li>Household replacement services</li>
      <li>Funeral expenses</li>
    </ul>
  </li>
  <li><strong>PIP Medical Coverage Options (since 2020):</strong>
    <ul>
      <li>Unlimited coverage</li>
      <li>$500,000 per person</li>
      <li>$250,000 per person</li>
      <li>$50,000 per person (Medicaid)</li>
      <li>Opt-out (if you have qualifying health insurance)</li>
    </ul>
  </li>
</ul>

<h2>Comprehensive Coverage</h2>
<p><strong>Comprehensive coverage</strong> protects your vehicle from damage caused by events other than collisions — theft, vandalism, hail or weather damage, hitting an animal (like a deer), damage from falling objects, and glass damage.</p>

<h2>Collision Coverage Types</h2>
<ul>
  <li><strong>Broadform Collision:</strong> Your deductible is waived if you are not at fault. If at fault, you pay the deductible.</li>
  <li><strong>Standard Collision:</strong> You pay your deductible regardless of who is at fault.</li>
  <li><strong>Liability Only:</strong> Minimum required insurance. No coverage for damage to your own vehicle.</li>
</ul>
"""
    },
    {
        "slug": "special-event-insurance",
        "title": "Special Event Insurance: Do You Need It?",
        "date": "2024-05-15", "date_display": "May 15, 2024",
        "category": "Commercial Insurance", "read_minutes": 2,
        "summary": "Most venues require proof of event insurance to use their space. Even at home, your Homeowners may not cover certain events. Here's why you need event coverage.",
        "meta_description": "Most venues will require proof of event insurance. Event coverage protects you from third-party injury, property damage, and liquor liability for weddings, graduations, and more.",
        "body_html": """
<h2>Who needs event insurance?</h2>
<p>Anyone who likes to have a good time! But actually, event insurance is a necessity for any group of people coming together, especially if there is alcohol involved. Common events that need coverage include:</p>
<ul>
  <li>Graduations and open houses</li>
  <li>Weddings and bridal showers</li>
  <li>Baptisms and baby showers</li>
  <li>Funerals</li>
  <li>Conferences and banquets</li>
  <li>Quinceañeras and Sweet Sixteen parties</li>
  <li>Bar and Bat Mitzvahs</li>
  <li>Proms and school dances</li>
  <li>Concerts and festivals</li>
  <li>Farmers markets</li>
  <li>Math tournaments and tournaments</li>
  <li>Private events of all kinds</li>
</ul>

<h2>Why do I need event insurance?</h2>
<p>For starters, <strong>most venues will require you to show proof of event insurance to use their space</strong>. Even if you have it at your home, your Homeowners may not cover you for certain events. Beyond that basic requirement, large groups, alcohol, and rented spaces put your assets on the line.</p>

<p>If you chose the menu and a guest has a serious allergy to fish, you could be on the hook (pun intended) if they end up in the hospital. If someone busts a move which in turn busts a window, you can expect the venue to pursue some money from you for the repair.</p>

<p>Say a wedding guest is "overserved" and winds up injuring themselves or others once they've left the party. As the host, you could be hit with a mountain of problems way worse than any hangover. Wedding insurance will provide your legal defense.</p>

<p><strong>Events mean risk, and risk means you need special event liability insurance.</strong></p>

<h2>What is event insurance?</h2>
<p>Special events insurance is a specific type of liability insurance that protects you against the risks associated with organizing or participating in a special event. Event coverage includes third-party bodily injury, property damage, and liquor liability.</p>

<h3>Event Liability</h3>
<p>Coverage for bodily injury and property damage to third parties — attendees, vendors, or the venue itself. Covered claims also provide for legal fees and damage payments.</p>

<h3>Liquor Liability</h3>
<p>Provides coverage for legal expenses and damage payouts if alcohol service at your event causes a covered peril (bodily injury or property damage). This is included in your event policy if you're not selling alcohol, as in BYOB or open bar events. If you own a business that sells, serves, or distributes alcohol at events, you can easily add retail liquor liability coverage to your policy.</p>
"""
    },
    {
        "slug": "protect-yourself-from-auto-insurance-refund-scams",
        "title": "Protect Yourself From Auto Insurance Refund Scams",
        "date": "2022-04-19", "date_display": "April 19, 2022",
        "category": "Auto Insurance", "read_minutes": 1,
        "summary": "Michigan's auto insurance refunds are on their way. Watch out for scammers trying to steal your personal information by impersonating your insurance company.",
        "meta_description": "Michigan auto insurance refunds are coming. Watch out for scammers trying to steal your personal information by impersonating insurance companies. Stay safe with these tips.",
        "body_html": """
<p class="lead">Auto insurance refunds are on their way, and you should be alert for bad actors using the current news to attempt to steal your personal information.</p>

<p>Thanks to cost savings under Michigan's historic, bipartisan auto insurance reform passed by the Legislature and signed by Governor Whitmer in 2019, Michiganders are receiving $400 per-vehicle refunds from their auto insurance companies this spring.</p>

<p><strong>It's important to know that you do not have to do anything in order to receive your refund.</strong> Your insurer will issue it to you automatically via check or ACH deposit by May 9.</p>

<p>If someone calls claiming to need your personal information in order to give you your refund, <strong>hang up</strong>. Never give out personal information including address, birthdate, Social Security Number, account numbers, or passwords to unsolicited callers.</p>

<p>If you receive a call about your auto insurance refund, contact your insurance company directly to verify the request and inquire how you can provide information securely if necessary.</p>
"""
    },
]

# Sort by date desc
POSTS.sort(key=lambda p: p['date'], reverse=True)


# ------------------------------------------------------------------
# Shared shell
# ------------------------------------------------------------------
def utility_bar():
    return f'''<div class="utility-bar">
  <div class="container">
    <span class="utility-item">📍 4301 S. Baldwin Rd, Lake Orion, MI 48359</span>
    <span class="utility-item">📞 <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
    <span class="utility-item">✉️ <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div>'''

def header(rel):
    return f'''<header class="site-header">
  <div class="container">
    <a class="brand" href="{rel}" aria-label="J. Jacobs and Associates Insurance home">
      <img class="brand-logo-img" src="{rel}assets/img/logo.jpeg" alt="J. Jacobs and Associates Insurance">
    </a>
    <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>
    <nav class="main-nav" id="primary-nav" aria-label="Primary">
      <ul>
        <li class="has-submenu">
          <details class="submenu-wrap"><summary class="nav-toggle">Our Agency</summary>
          <ul class="submenu">
            <li><a href="{rel}about/">About Us</a></li>
            <li><a href="{rel}team/">Our Team</a></li>
            <li><a href="{rel}carriers/">Our Carriers</a></li>
            <li><a href="{rel}reviews/">Reviews</a></li>
          </ul></details>
        </li>
        <li class="has-submenu">
          <details class="submenu-wrap"><summary class="nav-toggle">Products</summary>
          <ul class="submenu">
            <li><a href="{rel}personal/">Personal Insurance</a></li>
            <li><a href="{rel}personal/auto-insurance/">Auto Insurance</a></li>
            <li><a href="{rel}personal/home-insurance/">Home Insurance</a></li>
            <li><a href="{rel}personal/life-insurance/">Life Insurance</a></li>
            <li><a href="{rel}business/">Commercial Insurance</a></li>
            <li><a href="{rel}business/workers-compensation/">Workers Compensation</a></li>
          </ul></details>
        </li>
        <li><a href="{rel}service/">Service Center</a></li>
        <li><a href="{rel}blog/">Blog</a></li>
        <li><a href="{rel}faq/">FAQ</a></li>
        <li><a href="{rel}contact/">Contact</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a>
      <a class="btn btn-primary" href="{rel}quotes/">Start a Quote</a>
    </div>
  </div>
</header>'''


def footer(rel):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-logo"><img src="{rel}assets/img/logo.jpeg" alt="J. Jacobs and Associates"></div>
        <h4>J. Jacobs &amp; Associates</h4>
        <p>Family-owned independent insurance agency serving Michigan since 1981.</p>
        <p style="margin-top:1rem;">
          <strong style="color:#fff;">4301 S. Baldwin Rd</strong><br>
          Lake Orion, Michigan 48359<br>
          <a href="tel:{PHONE_TEL}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
      <div>
        <h4>Insurance</h4>
        <ul>
          <li><a href="{rel}personal/">Personal Insurance</a></li>
          <li><a href="{rel}personal/auto-insurance/">Auto Insurance</a></li>
          <li><a href="{rel}personal/home-insurance/">Home Insurance</a></li>
          <li><a href="{rel}personal/life-insurance/">Life Insurance</a></li>
          <li><a href="{rel}business/">Commercial Insurance</a></li>
          <li><a href="{rel}business/workers-compensation/">Workers Compensation</a></li>
        </ul>
      </div>
      <div>
        <h4>Agency</h4>
        <ul>
          <li><a href="{rel}about/">About Us</a></li>
          <li><a href="{rel}team/">Our Team</a></li>
          <li><a href="{rel}carriers/">Our Carriers</a></li>
          <li><a href="{rel}reviews/">Reviews</a></li>
          <li><a href="{rel}blog/">Blog</a></li>
          <li><a href="{rel}faq/">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Follow Us</h4>
        <div class="social-row">
          <a href="https://www.facebook.com/JacobsandAssociates/" aria-label="Facebook" rel="noopener" target="_blank">f</a>
          <a href="https://www.instagram.com/jjacobs_and_associates/" aria-label="Instagram" rel="noopener" target="_blank">IG</a>
          <a href="https://www.linkedin.com/in/joe-jacobs-7a354422/" aria-label="LinkedIn" rel="noopener" target="_blank">in</a>
        </div>
        <ul style="margin-top:1.25rem;">
          <li><a href="{rel}contact/">Contact Us</a></li>
          <li><a href="{rel}privacy-policy/">Privacy Policy</a></li>
          <li><a href="{rel}accessibility/">Accessibility</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span>
      <span>Independent Insurance Agency · Lake Orion, Michigan</span>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/site.v2.js?v={VERSION}" defer></script>
</body>
</html>'''


def head(title, description, canonical_path, og_image=None, extra_schema=""):
    og_image_url = og_image or f"{SITE_URL}/assets/img/og-default.jpg"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE_URL}{canonical_path}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#14365e">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE_URL}{canonical_path}">
<meta property="og:site_name" content="J. Jacobs & Associates">
<meta property="og:image" content="{og_image_url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{extra_schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''


# ------------------------------------------------------------------
# Blog Index
# ------------------------------------------------------------------
def render_index():
    cards = []
    for p in POSTS:
        cards.append(f'''<article class="blog-card">
          <a href="./{p['slug']}/" class="blog-card-link">
            <div class="blog-card-meta">
              <span class="blog-card-cat">{p['category']}</span>
              <span class="blog-card-dot">·</span>
              <time datetime="{p['date']}">{p['date_display']}</time>
              <span class="blog-card-dot">·</span>
              <span>{p['read_minutes']} min read</span>
            </div>
            <h2>{p['title']}</h2>
            <p>{p['summary']}</p>
            <span class="blog-card-cta">Read article →</span>
          </a>
        </article>''')

    breadcrumbs_schema = (
        '<script type="application/ld+json">\n'
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
        f'{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}},'
        f'{{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE_URL}/blog/"}}'
        ']}\n</script>'
    )
    # Also add Blog schema
    blog_schema = (
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"Blog","name":"J. Jacobs & Associates Insurance Blog","url":"' + SITE_URL + '/blog/","publisher":{"@type":"Organization","name":"J. Jacobs & Associates"}}\n'
        '</script>'
    )

    h = head(
        title="Insurance Blog | Michigan Insurance News & Tips | J. Jacobs & Associates",
        description="Michigan insurance news, education, and tips from J. Jacobs & Associates — covering auto, home, life, business, workers comp, and more. Updated regularly.",
        canonical_path="/blog/",
        extra_schema=breadcrumbs_schema + "\n" + blog_schema
    )
    h += '<link rel="stylesheet" href="../assets/css/styles.css?v=' + VERSION + '">\n'

    body = (
        utility_bar() + '\n' +
        header('../') + '\n' +
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="../">Home</a></li><li>Blog</li></ol></div></nav>\n' +
        '<main id="main">\n' +
        '<section class="section">\n' +
        '<div class="container">\n' +
        '<span class="eyebrow">News &amp; Education</span>\n' +
        '<h1>Insurance Insights from J. Jacobs &amp; Associates</h1>\n' +
        '<p class="lead">Michigan-specific insurance education, news, and practical advice from our team of licensed agents. Updated regularly.</p>\n' +
        '<div class="blog-grid">' + ''.join(cards) + '</div>\n' +
        '<div class="callout"><h2>Want to talk to a real agent?</h2><p>Get a free comparison quote across our 50+ carriers — no obligation.</p>' +
        '<a class="btn btn-primary btn-lg" href="../quotes/">Start My Quote</a></div>\n' +
        '</div>\n</section>\n</main>\n' +
        footer('../')
    )

    out = Path('blog/index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h.replace('</head>', '<link rel="stylesheet" href="../assets/css/styles.css?v=' + VERSION + '">\n</head>', 1).replace('<link rel="stylesheet" href="../assets/css/styles.css?v=' + VERSION + '">\n<link rel="stylesheet" href="../assets/css/styles.css?v=' + VERSION + '">', '<link rel="stylesheet" href="../assets/css/styles.css?v=' + VERSION + '">') + body, encoding='utf-8')
    print(f"  blog/index.html")


# ------------------------------------------------------------------
# Individual post pages
# ------------------------------------------------------------------
def render_post(i, p):
    prev_post = POSTS[i-1] if i > 0 else None
    next_post = POSTS[i+1] if i < len(POSTS) - 1 else None

    # Article + Breadcrumb schema
    article_schema = (
        '<script type="application/ld+json">\n'
        '{'
        '"@context":"https://schema.org",'
        '"@type":"BlogPosting",'
        f'"headline":"{p["title"]}",'
        f'"datePublished":"{p["date"]}",'
        f'"dateModified":"{p["date"]}",'
        '"author":{"@type":"Person","name":"Joseph Jacobs","url":"' + SITE_URL + '/team/"},'
        '"publisher":{"@type":"Organization","name":"J. Jacobs & Associates","logo":{"@type":"ImageObject","url":"' + SITE_URL + '/assets/img/logo.jpeg"}},'
        f'"description":"{p["meta_description"]}",'
        f'"mainEntityOfPage":{{"@type":"WebPage","@id":"{SITE_URL}/blog/{p["slug"]}/"}}'
        '}\n</script>'
    )
    bc_schema = (
        '<script type="application/ld+json">\n'
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
        f'{{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}},'
        f'{{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE_URL}/blog/"}},'
        f'{{"@type": "ListItem", "position": 3, "name": "{p["title"][:80]}", "item": "{SITE_URL}/blog/{p["slug"]}/"}}'
        ']}\n</script>'
    )

    h = head(
        title=f'{p["title"]} | J. Jacobs & Associates',
        description=p["meta_description"],
        canonical_path=f"/blog/{p['slug']}/",
        extra_schema=article_schema + "\n" + bc_schema
    )
    h = h.replace('</head>', f'<link rel="stylesheet" href="../../assets/css/styles.css?v={VERSION}">\n</head>')

    nav_links = []
    if prev_post:
        nav_links.append(f'<a class="post-nav-link prev" href="../{prev_post["slug"]}/"><span class="post-nav-label">← Previous</span><span class="post-nav-title">{prev_post["title"]}</span></a>')
    if next_post:
        nav_links.append(f'<a class="post-nav-link next" href="../{next_post["slug"]}/"><span class="post-nav-label">Next →</span><span class="post-nav-title">{next_post["title"]}</span></a>')
    post_nav = '<nav class="post-nav">' + ''.join(nav_links) + '</nav>' if nav_links else ''

    article = f'''
<article class="blog-post">
  <header class="blog-post-header">
    <span class="eyebrow">{p['category']}</span>
    <h1>{p['title']}</h1>
    <div class="blog-post-meta">
      <span>By <strong>Joseph Jacobs</strong></span>
      <span>·</span>
      <time datetime="{p['date']}">{p['date_display']}</time>
      <span>·</span>
      <span>{p['read_minutes']} min read</span>
    </div>
  </header>

  <div class="blog-post-body">
    {p['body_html']}
  </div>

  <footer class="blog-post-footer">
    <div class="blog-post-cta">
      <h2>Have questions about your coverage?</h2>
      <p>Our Michigan-licensed agents are happy to review your policy and answer your questions — no cost, no obligation.</p>
      <p><a class="btn btn-primary btn-lg" href="../../quotes/">Get a Free Quote</a>&nbsp;<a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}">Call (248) 693-6455</a></p>
    </div>

    <div class="blog-disclaimer">
      <p><strong>Disclaimer:</strong> This blog post is intended for general educational purposes only and does not constitute insurance advice for any specific situation. Coverage availability, terms, and pricing vary by insurer, policy form, and individual risk characteristics. Michigan insurance laws and regulations are subject to change. Consult a licensed Michigan insurance agent for advice specific to your circumstances. J. Jacobs and Associates is licensed in the state of Michigan.</p>
    </div>

    {post_nav}
  </footer>
</article>
'''

    body = (
        utility_bar() + '\n' +
        header('../../') + '\n' +
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="../../">Home</a></li><li><a href="../">Blog</a></li><li>' + p['title'][:60] + '</li></ol></div></nav>\n' +
        '<main id="main">\n' +
        '<section class="section"><div class="container" style="max-width:820px;">' +
        article +
        '</div></section>\n</main>\n' +
        footer('../../')
    )

    out = Path(f'blog/{p["slug"]}/index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h + body, encoding='utf-8')
    print(f"  blog/{p['slug']}/index.html")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def build():
    print("Building blog...")
    render_index()
    for i, p in enumerate(POSTS):
        render_post(i, p)

    # Update sitemap
    sitemap_path = Path('sitemap.xml')
    sitemap = sitemap_path.read_text(encoding='utf-8')
    if '/blog/' not in sitemap:
        new_entries = '  <url>\n    <loc>https://www.jjainsurance.com/blog/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        for p in POSTS:
            new_entries += f'  <url>\n    <loc>https://www.jjainsurance.com/blog/{p["slug"]}/</loc>\n    <lastmod>{p["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
        sitemap = sitemap.replace('</urlset>', new_entries + '</urlset>')
        sitemap_path.write_text(sitemap, encoding='utf-8')
        print("  sitemap.xml updated")

    print("\nDone.")


if __name__ == '__main__':
    build()
