#!/usr/bin/env python3
"""
JJA Blog Builder — Enhanced (2026-05-28)
Generates new posts and rebuilds index/sitemap.
Existing posts marked prebuilt=True are skipped for HTML generation.
"""

import json, re, os, html as html_lib
from pathlib import Path

SITE_URL   = "https://www.jjainsurance.com"
PHONE_TEL  = "+12486936455"
PHONE_DISP = "(248) 693-6455"
VERSION    = "20260528"

# ─────────────────────────────────────────────────────────────
# POSTS  (prebuilt=True → skip HTML, include in index/sitemap)
# ─────────────────────────────────────────────────────────────
POSTS = [

    # ── EXISTING (prebuilt stubs – metadata only) ─────────────
    {
        "slug": "commercial-auto-vs-personal-auto-michigan",
        "title": "Commercial Auto vs. Personal Auto Insurance in Michigan: Why the Difference Matters",
        "seo_title": "Commercial vs. Personal Auto in Michigan",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Auto Insurance", "read_minutes": 7,
        "summary": "Using your personal vehicle for work in Michigan? Your personal auto policy likely won't cover a business-related accident. Here's who needs commercial auto insurance and what happens if you don't have it.",
        "meta_description": "Using your personal vehicle for work in Michigan? Your personal policy may not cover you. Learn when you need commercial auto coverage.",
        "og_image": "/assets/img/blog/commercial-auto-vs-personal-auto-michigan.svg",
        "card_photo": "photo-1574023240744-64c47c8c0676",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "common-auto-insurance-terms",
        "title": "Common Michigan Auto Insurance Terms Explained for Drivers",
        "seo_title": "Michigan Auto Insurance Terms Explained",
        "date": "2025-09-15", "date_display": "September 15, 2025", "date_modified": "2026-05-25",
        "category": "Auto Insurance", "read_minutes": 4,
        "summary": "Confused by Michigan's no-fault system? Deductibles, PIP, liability, comprehensive — every key term explained in plain English.",
        "meta_description": "Confused by Michigan's no-fault auto insurance? Deductibles, PIP, liability, comprehensive — every key term explained in plain English.",
        "og_image": "/assets/img/blog/common-auto-insurance-terms.svg",
        "card_photo": "photo-1694380974280-ad353c6dc597",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "does-your-michigan-business-need-cyber-insurance",
        "title": "Does Your Michigan Business Need Cyber Insurance?",
        "seo_title": "Does Your MI Business Need Cyber Insurance?",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Commercial Insurance", "read_minutes": 7,
        "summary": "Only 17% of Michigan SMBs carry cyber insurance — yet the average breach costs $200,000. Find out who needs it and what it actually covers.",
        "meta_description": "Only 17% of Michigan SMBs carry cyber insurance — yet the average breach costs $200,000. Find out who needs it and what it covers.",
        "og_image": "/assets/img/blog/does-your-michigan-business-need-cyber-insurance.svg",
        "card_photo": "photo-1614064641938-3bbee52942c7",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "general-liability-insurance-michigan-contractors",
        "title": "General Liability Insurance for Michigan Contractors: What You Need to Know",
        "seo_title": "General Liability for MI Contractors",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Commercial Insurance", "read_minutes": 7,
        "summary": "Michigan contractors: most GCs require $1M–$2M liability before you step on a job site. Here's what GL covers, what it doesn't, and how much it costs.",
        "meta_description": "Michigan contractors: most GCs require $1M–$2M liability before you step on a job site. Learn what GL covers and what it costs.",
        "og_image": "/assets/img/blog/general-liability-insurance-michigan-contractors.svg",
        "card_photo": "photo-1589939705384-5185137a7f0f",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "how-much-life-insurance-do-i-need",
        "title": "How Much Life Insurance Do You Actually Need? A Michigan Family's Guide",
        "seo_title": "How Much Life Insurance Do You Need?",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Life Insurance", "read_minutes": 6,
        "summary": "Most Michigan families are either underinsured or guessing. Here's a straightforward way to calculate the right coverage amount.",
        "meta_description": "How much life insurance do you need in Michigan? Use the DIME method, 10x income rule, and other proven frameworks to find the right number.",
        "og_image": "/assets/img/blog/how-much-life-insurance-do-i-need.svg",
        "card_photo": "photo-1709216461598-018ae6307dc0",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-auto-insurance-glossary",
        "title": "Michigan Auto Insurance Terminology Guide",
        "seo_title": "Michigan Auto Insurance Terminology Guide",
        "date": "2026-05-15", "date_display": "May 15, 2026", "date_modified": "2026-05-25",
        "category": "Insurance Education", "read_minutes": 6,
        "summary": "Every key auto insurance term explained in plain English — PIP, PLPD, OTC, mini-tort, and more.",
        "meta_description": "Confused by Michigan's no-fault system? Every key auto insurance term explained — PIP, PLPD, mini-tort, OTC, and more.",
        "og_image": "/assets/img/blog/michigan-auto-insurance-glossary.svg",
        "card_photo": "photo-1574023240744-64c47c8c0676",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-business-owners-policy",
        "title": "What Is a Business Owner's Policy (BOP) — and Does Your Michigan Business Need One?",
        "seo_title": "Michigan Business Owner's Policy (BOP) Guide",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Commercial Insurance", "read_minutes": 6,
        "summary": "A BOP bundles general liability and commercial property into one policy — usually cheaper than buying them separately. Here's who qualifies and what it covers.",
        "meta_description": "A BOP bundles GL and property coverage for Michigan small businesses. Learn what's included, who qualifies, and what it costs.",
        "og_image": "/assets/img/blog/michigan-business-owners-policy.svg",
        "card_photo": "photo-1551836022-aadb801c60ae",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-flood-insurance",
        "title": "Flood Insurance in Michigan: What Your Homeowners Policy Doesn't Cover",
        "seo_title": "Michigan Flood Insurance: What HO Doesn't Cover",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Home Insurance", "read_minutes": 7,
        "summary": "Standard homeowners insurance doesn't cover flood damage — not a drop of it. Here's what Michigan homeowners need to know about flood insurance.",
        "meta_description": "Homeowners insurance doesn't cover flood damage in Michigan. Learn what NFIP and private flood insurance cost and who needs it.",
        "og_image": "/assets/img/blog/michigan-flood-insurance.svg",
        "card_photo": "photo-1657069342866-2d11c2509b02",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-gap-insurance",
        "title": "Gap Insurance in Michigan: What It Is and When You Actually Need It",
        "seo_title": "Michigan Gap Insurance: When You Need It",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Auto Insurance", "read_minutes": 6,
        "summary": "Gap insurance covers the difference between what you owe on your car loan and what your car is actually worth. Here's when it's worth it.",
        "meta_description": "Gap insurance in Michigan covers what's owed on your loan vs. your car's value after a total loss. Learn when it's worth buying.",
        "og_image": "/assets/img/blog/michigan-gap-insurance.svg",
        "card_photo": "photo-1585390062628-be8608aa7d83",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-homeowners-insurance-glossary",
        "title": "Michigan Homeowners Insurance Terminology Guide",
        "seo_title": "Michigan Homeowners Insurance Glossary",
        "date": "2026-05-15", "date_display": "May 15, 2026", "date_modified": "2026-05-25",
        "category": "Insurance Education", "read_minutes": 6,
        "summary": "Every homeowners insurance term explained — HO-1 through HO-8, Coverage A through F, replacement cost vs. ACV, and more.",
        "meta_description": "Every homeowners insurance term explained: HO-1 through HO-8, Coverage A–F, replacement cost vs ACV, and more. Michigan-specific notes throughout.",
        "og_image": "/assets/img/blog/michigan-homeowners-insurance-glossary.svg",
        "card_photo": "photo-1772313952254-dae19b91854b",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-insurance-questions-answered",
        "title": "The 25 Insurance Questions Michigan Residents Ask Most",
        "seo_title": "25 Michigan Insurance Questions Answered",
        "date": "2026-05-15", "date_display": "May 15, 2026", "date_modified": "2026-05-25",
        "category": "Insurance Education", "read_minutes": 14,
        "summary": "Michigan-licensed agents answer the 25 most common insurance questions — no-fault, homeowners, life, commercial, and more.",
        "meta_description": "Michigan-licensed agents answer the 25 most common insurance questions: no-fault, PIP, homeowners, claims, life insurance, and more.",
        "og_image": "/assets/img/blog/michigan-insurance-questions-answered.svg",
        "card_photo": "photo-1526948531399-320e7e40f0ca",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-motorcycle-insurance-terminology",
        "title": "Michigan Motorcycle Insurance: The Complete Terminology Guide",
        "seo_title": "Michigan Motorcycle Insurance: Terms Guide",
        "date": "2026-05-15", "date_display": "May 15, 2026", "date_modified": "2026-05-25",
        "category": "Insurance Education", "read_minutes": 5,
        "summary": "Michigan motorcycle insurance terms explained — lay-up policies, agreed value, CPE, and what Michigan no-fault means for riders.",
        "meta_description": "Michigan motorcycle insurance terms explained: lay-up policies, agreed value, CPE, OTC, and Michigan no-fault coverage for riders.",
        "og_image": "/assets/img/blog/michigan-motorcycle-insurance-terminology.svg",
        "card_photo": "photo-1676631284522-8007dd380171",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-no-fault-option-6",
        "title": "Michigan No-Fault Option 6: What Medicare Covers and What It Doesn't",
        "seo_title": "Michigan No-Fault Option 6 & Medicare",
        "date": "2025-09-18", "date_display": "September 18, 2025", "date_modified": "2026-05-25",
        "category": "Auto Insurance", "read_minutes": 3,
        "summary": "Thinking about choosing Option 6 PIP in Michigan and using Medicare instead? Here's what that decision actually means for your coverage.",
        "meta_description": "Choosing Option 6 to use Medicare instead of PIP in Michigan? Understand the serious coverage gaps before you make that call.",
        "og_image": "/assets/img/blog/michigan-no-fault-option-6.svg",
        "card_photo": "photo-1633157953349-75c66213ca2f",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-teen-driver-insurance",
        "title": "Adding a Teen Driver to Your Michigan Auto Policy: What Parents Need to Know",
        "seo_title": "Adding a Teen Driver in Michigan",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Auto Insurance", "read_minutes": 7,
        "summary": "Adding a teen driver in Michigan raises your auto insurance by $2,500+ per year. Here's how to manage the cost without cutting the coverage your teen actually needs.",
        "meta_description": "Adding a teen driver in Michigan raises your auto insurance by $2,500+ per year. Learn what affects the cost and how to keep it manageable.",
        "og_image": "/assets/img/blog/michigan-teen-driver-insurance.svg",
        "card_photo": "Teen",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-umbrella-insurance-who-needs-it",
        "title": "Michigan Umbrella Insurance: Who Needs It and What It Actually Costs",
        "seo_title": "Michigan Umbrella Insurance: Who Needs It",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Personal Insurance", "read_minutes": 6,
        "summary": "For about $40/month, you can add $1 million in liability protection on top of your home and auto coverage. Michigan umbrella insurance is one of the most underused policies out there.",
        "meta_description": "Michigan umbrella insurance costs $400–$600/year for $1M in coverage. Find out who needs it, what it covers, and what it doesn't.",
        "og_image": "/assets/img/blog/michigan-umbrella-insurance-who-needs-it.svg",
        "card_photo": "photo-1562564055-71e051d33c19",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "michigan-workers-compensation-do-you-need-it-guide-for-business-owners",
        "title": "Do I Need Workers' Compensation Insurance in Michigan? A Guide for Small Businesses",
        "seo_title": "Michigan Workers' Comp: Do You Need It?",
        "date": "2025-09-17", "date_display": "September 17, 2025", "date_modified": "2026-05-25",
        "category": "Workers Comp", "read_minutes": 2,
        "summary": "Is workers' comp required for your Michigan small business? The threshold is lower than most owners think.",
        "meta_description": "Is workers' comp required for your Michigan small business? Learn the employee count thresholds, penalties, and what coverage actually costs.",
        "og_image": "/assets/img/blog/michigan-workers-compensation-do-you-need-it-guide-for-business-owners.svg",
        "card_photo": "photo-1589939705384-5185137a7f0f",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "special-event-insurance",
        "title": "Special Event Insurance: Do You Need It?",
        "seo_title": "Michigan Special Event Insurance Guide",
        "date": "2024-05-15", "date_display": "May 15, 2024", "date_modified": "2026-05-25",
        "category": "Commercial Insurance", "read_minutes": 2,
        "summary": "Most Michigan venues require event insurance. Learn what it covers, how much it costs, and whether you need it for your next event.",
        "meta_description": "Most Michigan venues require event insurance. Learn what it covers, how much it costs, and whether you need it for your next event.",
        "og_image": "/assets/img/blog/special-event-insurance.svg",
        "card_photo": "photo-1677677403344-029c7fcd7300",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "term-vs-whole-life-insurance-michigan",
        "title": "Term vs. Whole Life Insurance: How to Actually Decide",
        "seo_title": "Term vs. Whole Life Insurance in Michigan",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Life Insurance", "read_minutes": 7,
        "summary": "Term vs. whole life insurance in Michigan — a clear breakdown of cost, coverage length, and which one actually fits your situation.",
        "meta_description": "Term vs. whole life insurance in Michigan: a clear breakdown of cost, coverage length, and which one fits your situation.",
        "og_image": "/assets/img/blog/term-vs-whole-life-insurance-michigan.svg",
        "card_photo": "photo-1628676348963-f88c671333f6",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "what-happens-if-you-skip-your-workers-comp-audit-in-michigan",
        "title": "What Happens If You Skip Your Workers' Comp Audit in Michigan?",
        "seo_title": "Skipping MI Workers' Comp Audit: Consequences",
        "date": "2025-09-18", "date_display": "September 18, 2025", "date_modified": "2026-05-25",
        "category": "Workers Comp", "read_minutes": 3,
        "summary": "Missing your Michigan workers' comp audit triggers penalty premiums, policy cancellation, and potential fines. Here's what actually happens.",
        "meta_description": "Missing your Michigan workers' comp audit triggers penalty premiums, policy cancellation, and potential fines. Here's what happens.",
        "og_image": "/assets/img/blog/what-happens-if-you-skip-your-workers-comp-audit-in-michigan.svg",
        "card_photo": "photo-1628147529780-36964fbb8d54",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "why-home-insurance-went-up-2026",
        "title": "Why Did My Homeowners Insurance Go Up in 2026? (And 7 Ways to Fight Back)",
        "seo_title": "Why Home Insurance Rates Went Up in 2026",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Home Insurance", "read_minutes": 8,
        "summary": "Michigan home insurance rates are up 21% over two years. Learn the real reasons why — and what you can actually do about it.",
        "meta_description": "Michigan home insurance rates are up 21% over two years. Learn the real reasons why — and 7 things you can do to push back.",
        "og_image": "/assets/img/blog/why-home-insurance-went-up-2026.svg",
        "card_photo": "home-infograph",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },
    {
        "slug": "why-independent-insurance-agents-get-better-rates",
        "title": "Why Independent Insurance Agents Get You Better Rates (And One Call Does It)",
        "seo_title": "Why Independent Agents Get You Better Rates",
        "date": "2026-05-25", "date_display": "May 25, 2026", "date_modified": "2026-05-25",
        "category": "Insurance Education", "read_minutes": 6,
        "summary": "One call to JJA Insurance compares 10+ Michigan carriers. See why independent agents consistently beat captive agents on price and coverage.",
        "meta_description": "One call to JJA Insurance compares 10+ Michigan carriers. See why independent agents consistently beat captive agents on price and coverage.",
        "og_image": "/assets/img/blog/why-independent-insurance-agents-get-better-rates.svg",
        "card_photo": "photo-1526948531399-320e7e40f0ca",
        "faqs": [], "related_posts": [], "prebuilt": True, "body_html": "",
    },

    # ── NEW POSTS ─────────────────────────────────────────────

    {
        "slug": "michigan-boat-rv-insurance",
        "title": "Michigan Boat & RV Insurance: What You Need Before Summer Hits",
        "seo_title": "Michigan Boat & RV Insurance Guide",
        "date": "2026-05-28", "date_display": "May 28, 2026", "date_modified": "2026-05-28",
        "category": "Personal Insurance", "read_minutes": 7,
        "summary": "Michigan has 11,000+ inland lakes — and the moment you're on the water or the road, your home and auto policies stop covering you. Here's what boat and RV insurance actually covers and what it costs.",
        "meta_description": "Michigan boat insurance starts at $200/year. RV insurance from $180/year. Learn what's required, what's covered, and when your home policy won't protect you.",
        "seo_title": "Michigan Boat & RV Insurance Guide",
        "og_image": "/assets/img/blog/michigan-boat-rv-insurance.svg",
        "card_photo": "photo-1779078063955-8fbf934c358c",
        "related_posts": ["michigan-flood-insurance", "michigan-umbrella-insurance-who-needs-it", "michigan-motorcycle-insurance-terminology"],
        "faqs": [
            {"q": "Is boat insurance required in Michigan?",
             "a": "Michigan doesn't legally require boat insurance the way it requires auto insurance. However, if your boat is financed, your lender will require coverage. Most marinas also require liability insurance as a condition of docking. And without coverage, any accident on the water leaves you personally on the hook."},
            {"q": "Does my homeowners insurance cover my boat?",
             "a": "Sometimes — but only for small boats. Most homeowners policies cover watercraft under 25 horsepower or 26 feet for liability, and even then, physical damage coverage is often excluded. Once you're over those thresholds, you're outside standard homeowners coverage and need a standalone boat policy."},
            {"q": "Do I need Michigan no-fault insurance on my RV?",
             "a": "Yes, if it's a self-propelled motorhome or camper van. Michigan treats motorhomes like motor vehicles — you need no-fault PIP coverage, bodily injury liability, and property damage liability. Travel trailers are different: they're towed, not driven, but if they have two or more axles, Michigan requires registration and insurance before they can legally be on the road."},
            {"q": "What is a lay-up period and how does it save money?",
             "a": "A lay-up period is a seasonal suspension of certain coverages — typically collision and liability — for the months your boat or RV sits in storage. You keep comprehensive coverage for fire, theft, and storm damage in storage, but you're not paying for on-water or on-road liability you're not using. In Michigan, where boats often sit from October through April, a lay-up endorsement can cut your premium meaningfully."},
            {"q": "How much does boat insurance cost in Michigan?",
             "a": "It depends on what you're insuring. Fishing boats and pontoons typically run $200–$500 per year. Runabouts and bass boats land in the $300–$600 range. Cabin cruisers and larger vessels can run $600–$1,200 or more. Personal watercraft (jet skis) usually cost $200–$400 per year. Navigating the Great Lakes rather than inland lakes pushes rates higher due to larger wave exposure and longer distances from shore."},
        ],
        "body_html": """
<p style="font-size:.9rem;background:var(--gray-50);border-left:4px solid var(--navy);padding:.75rem 1rem;border-radius:0 var(--r-sm) var(--r-sm) 0;margin-bottom:1.5rem;">
  Michigan boat and RV season is here. <a href="../../personal/" style="color:var(--navy);font-weight:600;">Get a watercraft or RV insurance quote from JJA →</a>
</p>

<p class="lead">Michigan gives you 11,000 inland lakes, hundreds of miles of Great Lakes shoreline, and some of the best camping in the Midwest. But the moment you pull out of the marina or hook that camper up to your truck, your standard homeowners and auto policies stop protecting you. Boat and RV insurance fills that gap — and in Michigan, there are rules that catch people off guard every single summer.</p>

<div class="callout-box">
  <p><strong>Michigan-specific rule:</strong> If your RV is a self-propelled motorhome or camper van, it's legally treated like a car. Michigan no-fault requirements apply — PIP, bodily injury liability, and property damage coverage are all mandatory. An uninsured motorhome cannot legally be driven on Michigan roads.</p>
</div>

<h2>Does Michigan Require Boat Insurance?</h2>

<p>Michigan doesn't legally require boat insurance the way it requires auto insurance. You can technically launch a boat without coverage. But that doesn't mean you should — and in practice, it often isn't optional.</p>

<p>If you financed your boat, your lender requires coverage. Full stop. Most marinas require liability insurance as a condition of docking. And if you cause an accident on the water — capsizing another boat, injuring a passenger, damaging a dock — you're personally liable for every dollar of damages.</p>

<p>There's also a coverage gap hiding in your homeowners policy. Most Michigan homeowners policies cover small watercraft — under 25 horsepower, under 26 feet — for basic liability. Once you're over those thresholds, that coverage disappears. And physical damage (the boat getting totaled) is almost never covered under homeowners regardless of size.</p>

<h2>What Boat Insurance Covers</h2>

<p>A standalone Michigan boat policy typically includes:</p>

<ul>
  <li><strong>Physical damage</strong> — collision, storm damage, sinking, fire, theft</li>
  <li><strong>Liability</strong> — bodily injury and property damage you cause to others on the water</li>
  <li><strong>Uninsured/underinsured boater coverage</strong> — if someone without coverage hits you</li>
  <li><strong>Medical payments</strong> — for injuries to you and your passengers</li>
  <li><strong>Towing and salvage</strong> — emergency assistance if you break down on the water</li>
  <li><strong>Fishing equipment</strong> — rods, reels, tackle boxes as optional add-on coverage</li>
</ul>

<p>What it doesn't cover: fuel spill cleanup (that's an add-on), racing, commercial use, or damage you cause intentionally.</p>

<h2>What Does Michigan Boat Insurance Cost?</h2>

<figure style="margin:1.5rem 0 2rem;">
  <img src="../../assets/img/blog/michigan-boat-rv-costs.svg"
       alt="Michigan boat and RV insurance costs by vessel type — bar chart"
       style="width:100%;height:auto;display:block;border-radius:8px;"
       loading="lazy" width="800" height="420">
  <figcaption style="font-size:.8rem;color:var(--text-muted);margin-top:.5rem;text-align:center;">Average annual insurance costs by vessel type in Michigan (2026)</figcaption>
</figure>

<p>Premiums depend on what you're insuring, where you navigate, and how much coverage you carry:</p>

<ul>
  <li><strong>Fishing boats / pontoons:</strong> $200–$500/year</li>
  <li><strong>Bass boats / runabouts:</strong> $300–$600/year</li>
  <li><strong>Cabin cruisers / larger vessels:</strong> $600–$1,200+/year</li>
  <li><strong>Personal watercraft (jet skis):</strong> $200–$400/year</li>
</ul>

<p>Boats used on the Great Lakes cost more than those on inland lakes — the exposure is higher, waves are bigger, and distances from shore are greater. High-performance boats and offshore racing models are in a separate category entirely.</p>

<p>One Michigan advantage: the short boating season. A lay-up endorsement (see below) can meaningfully reduce your premium by suspending coverage during winter storage.</p>

<h2>RV Insurance in Michigan: What's Required vs. What's Smart</h2>

<p>RV insurance in Michigan splits into two very different categories depending on what you're towing — or driving.</p>

<p><strong>Self-propelled motorhomes (Class A, B, C) and camper vans</strong> are treated like motor vehicles under Michigan law. They require the same no-fault coverage as your car: PIP medical coverage, bodily injury liability ($50,000/$100,000 minimum), and property damage liability ($10,000 minimum). You cannot register a motorhome or legally drive it without this coverage.</p>

<p><strong>Travel trailers, fifth wheels, and pop-up campers</strong> are towed — they don't move under their own power. However, if your trailer has two or more axles, Michigan requires registration and insurance before it can legally use Michigan roads. Your towing vehicle's auto policy may cover liability while towing, but physical damage to the trailer itself typically isn't covered under a standard auto policy.</p>

<p>Beyond the legal minimums, RV-specific policies add coverage your auto policy won't provide:</p>

<ul>
  <li><strong>Total loss replacement</strong> — new-for-old if your RV is totaled in the first few years</li>
  <li><strong>Full-timer coverage</strong> — if your RV is your primary residence, standard policies won't cover it properly</li>
  <li><strong>Campsite/vacation liability</strong> — covers accidents at your campsite, not just on the road</li>
  <li><strong>Attached accessories</strong> — awnings, satellite dishes, solar panels, slide-outs</li>
  <li><strong>Emergency expense coverage</strong> — hotel and meals if you break down far from home</li>
</ul>

<h2>What RV Insurance Costs in Michigan</h2>

<p>Michigan RV premiums are among the higher in the country due to no-fault requirements and seasonal storage costs, but the range is wide:</p>

<ul>
  <li><strong>Travel trailers and 5th wheels:</strong> $180–$600/year</li>
  <li><strong>Class B and C motorhomes:</strong> $600–$1,400/year</li>
  <li><strong>Class A motorhomes:</strong> $1,000–$3,000/year</li>
</ul>

<p>Progressive data for Michigan puts the average motorhome policy around $1,055 per year — less than most people expect for a vehicle worth $50,000–$200,000.</p>

<h2>The Lay-Up Period: Michigan's Best Boat and RV Discount</h2>

<p>Michigan boats and many RVs sit in storage from October through April — roughly half the year. A lay-up endorsement suspends your on-water or on-road liability and collision coverage during that window, while keeping comprehensive protection active for fire, theft, vandalism, and storm damage in storage.</p>

<p>The savings vary by insurer, but for a boat stored 5–6 months per year, a lay-up discount can reduce your annual premium by 20–40%. Ask about it specifically when shopping — not all agents bring it up automatically.</p>

<h2>When Your Home and Auto Policies Stop Covering You</h2>

<p>This is where Michigan boaters and RV owners get burned. Standard homeowners policies typically exclude:</p>

<ul>
  <li>Boats over 25–26 HP or over 26 feet in length</li>
  <li>Outboard motors above certain horsepower thresholds</li>
  <li>Any watercraft on the Great Lakes or open water</li>
  <li>Physical damage to any watercraft (most policies)</li>
</ul>

<p>And your standard auto policy covers your tow vehicle while it's driving — not the trailer it's pulling. The trailer's contents, physical structure, and any damage it causes while parked are outside auto policy territory.</p>

<p>The fix is straightforward: a standalone boat or RV policy that picks up where your other policies leave off. At JJA, we shop those across multiple carriers — pricing varies more than most people expect between insurers on recreational vehicles, so comparison shopping pays off here.</p>

<div class="callout-box">
  <p><strong>Quick tip:</strong> Bundle your boat or RV policy with your home and auto and you'll almost always get a multi-policy discount. One call to our office compares pricing across 10+ Michigan carriers simultaneously — you don't have to shop each one separately.</p>
</div>

<h2>Frequently Asked Questions</h2>

<details class="faq-item">
  <summary>Is boat insurance required in Michigan?</summary>
  <div class="faq-body">
    <p>Michigan doesn't legally require boat insurance the way it requires auto insurance. However, if your boat is financed, your lender will require coverage. Most marinas also require liability insurance as a condition of docking. And without coverage, any accident on the water leaves you personally liable for all damages.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Does my homeowners insurance cover my boat?</summary>
  <div class="faq-body">
    <p>Sometimes — for small boats only. Most Michigan homeowners policies cover watercraft under 25 horsepower for basic liability. Once you're over that threshold, you're outside standard homeowners coverage. Physical damage to the boat is almost never covered under homeowners, regardless of size. Check your dec page and call us if you're not sure where your coverage ends.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Do I need Michigan no-fault insurance on my RV?</summary>
  <div class="faq-body">
    <p>Yes, if it's a self-propelled motorhome or camper van. Michigan treats motorhomes like motor vehicles — PIP, bodily injury liability, and property damage are all required. Travel trailers are different: if they have two or more axles, Michigan requires registration and insurance, but the coverage requirements differ from a motor vehicle policy.</p>
  </div>
</details>

<details class="faq-item">
  <summary>What is a lay-up period and how does it save money?</summary>
  <div class="faq-body">
    <p>A lay-up period suspends certain coverages — collision and liability — for the months your boat or RV is in storage. You keep comprehensive for fire, theft, and storm damage. In Michigan, where boats often sit from October through April, a lay-up endorsement can cut your premium by 20–40%. It's worth asking about specifically when you're getting a quote.</p>
  </div>
</details>

<details class="faq-item">
  <summary>How much does boat insurance cost in Michigan?</summary>
  <div class="faq-body">
    <p>Fishing boats and pontoons typically run $200–$500 per year. Runabouts and bass boats land in the $300–$600 range. Cabin cruisers and larger vessels can exceed $1,000 per year. Personal watercraft usually costs $200–$400 per year. Great Lakes navigation pushes rates higher than inland lakes due to the exposure involved. Call our office and we'll compare across multiple carriers — the range between insurers on recreational boats is wider than most people expect.</p>
  </div>
</details>
""",
    },

    {
        "slug": "michigan-renters-insurance",
        "title": "Michigan Renters Insurance: What It Covers, What It Costs, and Why You Probably Need It",
        "seo_title": "Michigan Renters Insurance Guide",
        "date": "2026-05-28", "date_display": "May 28, 2026", "date_modified": "2026-05-28",
        "category": "Home Insurance", "read_minutes": 7,
        "summary": "Your landlord's insurance covers the building. It doesn't cover your stuff. Michigan renters insurance averages $18/month — here's everything you need to know.",
        "meta_description": "Michigan renters insurance averages $18/month and covers your belongings, liability, and hotel costs if your unit becomes uninhabitable. Here's what to know.",
        "og_image": "/assets/img/blog/michigan-renters-insurance.svg",
        "card_photo": "photo-1613575831056-0acd5da8f085",
        "related_posts": ["why-home-insurance-went-up-2026", "michigan-homeowners-insurance-glossary", "how-to-file-homeowners-insurance-claim-michigan"],
        "faqs": [
            {"q": "Does Michigan law require renters insurance?",
             "a": "No state law requires renters insurance in Michigan. But your lease might. Many Michigan landlords require it as a lease condition — if you let it lapse, you're technically in breach. Even when it's not required, it's worth carrying. Your landlord's policy covers the building. It does not cover your belongings, your liability, or the cost of staying somewhere else if your unit becomes uninhabitable."},
            {"q": "Does renters insurance cover theft from my car in Michigan?",
             "a": "Usually yes. Personal property stolen from your vehicle is typically covered under the personal property portion of a renters insurance policy, subject to your deductible. This surprises a lot of people — your laptop bag stolen from your car parked outside a Michigan grocery store is a renters insurance claim, not an auto claim."},
            {"q": "Does renters insurance cover flooding in Michigan?",
             "a": "No. Standard renters insurance does not cover flood damage — same as homeowners insurance. If your ground-floor apartment floods because a river overflowed or a storm surge came through, your renters policy won't pay for damaged belongings. Separate flood insurance through NFIP or a private carrier is needed for that."},
            {"q": "What's the difference between actual cash value and replacement cost renters insurance?",
             "a": "Actual cash value pays what your belongings are worth today — depreciated. A 3-year-old laptop worth $200 gets you $200. Replacement cost pays what it costs to buy a comparable new laptop today — maybe $1,200. The premium difference is small; the payout difference after a claim is enormous. Always choose replacement cost if you can."},
            {"q": "How much personal property coverage do I actually need?",
             "a": "More than most renters think. Walk through your apartment and add up replacement costs: furniture, electronics, kitchen equipment, clothing, tools, sports gear. A modest one-bedroom in Michigan can easily total $20,000–$35,000 in belongings. Most renters underestimate this and end up underinsured. We can help you run through a quick inventory to find the right number."},
        ],
        "body_html": """
<p style="font-size:.9rem;background:var(--gray-50);border-left:4px solid var(--navy);padding:.75rem 1rem;border-radius:0 var(--r-sm) var(--r-sm) 0;margin-bottom:1.5rem;">
  Michigan renters insurance starts at $15/month. <a href="../../personal/" style="color:var(--navy);font-weight:600;">Get a renters insurance quote from JJA →</a>
</p>

<p class="lead">If you rent in Michigan and don't have renters insurance, you're one burst pipe, break-in, or kitchen fire away from replacing everything you own out of pocket. Your landlord's insurance covers the building. It covers the landlord's appliances and fixtures. It does not cover your couch, your laptop, your TV, or the cost of a hotel while your unit gets repaired. That's on you — unless you have a renters policy.</p>

<div class="callout-box">
  <p><strong>The math:</strong> Michigan renters insurance averages <strong>$18/month ($216/year)</strong>. For that, you get coverage on your personal belongings, up to $100,000 in liability protection, and additional living expenses if your unit becomes uninhabitable. That's less than most people spend on streaming services.</p>
</div>

<h2>What Your Landlord's Policy Actually Covers</h2>

<p>This is the misconception that costs Michigan renters thousands of dollars every year. When a pipe bursts and floods your apartment, your landlord's insurance covers the building — the walls, floors, structure, the landlord's appliances. It does not cover your furniture, your electronics, your clothing, or any of your personal property.</p>

<p>Your landlord isn't being stingy. That's how property insurance works. Their policy is designed to protect their investment in the building. Your belongings are your investment, and protecting them is your responsibility.</p>

<p>Same thing applies to liability. If someone slips and falls in your apartment and sues, your landlord's policy doesn't protect you. If you accidentally cause a fire that damages neighboring units, your landlord's policy covers the landlord's damages — your liability exposure is separate.</p>

<h2>What Renters Insurance Covers</h2>

<figure style="margin:1.5rem 0 2rem;">
  <img src="../../assets/img/blog/renters-vs-landlord-coverage.svg"
       alt="What renters insurance covers vs. what your landlord's policy covers — comparison chart"
       style="width:100%;height:auto;display:block;border-radius:8px;"
       loading="lazy" width="800" height="400">
  <figcaption style="font-size:.8rem;color:var(--text-muted);margin-top:.5rem;text-align:center;">Renters insurance vs. landlord's policy — who covers what</figcaption>
</figure>

<p>A standard Michigan renters policy has three parts:</p>

<p><strong>Personal property coverage</strong> protects your belongings from fire, smoke, theft, vandalism, windstorm, burst pipes, ice dam damage, and several other named perils. That includes:</p>

<ul>
  <li>Furniture, electronics, appliances you own</li>
  <li>Clothing and jewelry (up to policy limits)</li>
  <li>Laptops, tablets, gaming systems</li>
  <li>Sports equipment and tools</li>
  <li>Property stolen from your <em>car</em> — yes, really (more on that below)</li>
</ul>

<p><strong>Personal liability coverage</strong> protects you if someone is injured in your unit or if you accidentally damage someone else's property. A guest trips on a rug and breaks their wrist — that's a liability claim. You're liable for your dog biting a neighbor — that's covered too. Standard policies include $100,000 in liability coverage; $300,000 is worth considering if you entertain regularly.</p>

<p><strong>Additional living expenses (ALE)</strong> pay your hotel, meals, and temporary housing costs if your unit becomes uninhabitable after a covered loss. A kitchen fire that displaces you for three weeks costs real money. ALE covers that gap.</p>

<h2>What Renters Insurance Doesn't Cover</h2>

<p>A few things Michigan renters often assume are covered but aren't:</p>

<ul>
  <li><strong>Flooding</strong> — water coming in from outside (heavy rain, overflowing river) is not a covered peril under standard renters insurance. You need separate flood coverage for that.</li>
  <li><strong>Earthquake</strong> — rare in Michigan but excluded nonetheless</li>
  <li><strong>Your roommate's stuff</strong> — unless they're listed on the policy, their belongings aren't covered</li>
  <li><strong>Business property above the policy sub-limit</strong> — if you run a business from home, coverage for business equipment is capped</li>
  <li><strong>High-value items above sub-limits</strong> — jewelry, art, and collectibles often have per-item limits; a scheduled endorsement covers the rest</li>
</ul>

<h2>How Much Does Renters Insurance Cost in Michigan?</h2>

<p>Michigan renters insurance is affordable — and getting more so relative to what it covers, even though rates have climbed:</p>

<ul>
  <li><strong>State average:</strong> $216/year ($18/month)</li>
  <li><strong>Detroit:</strong> approximately $342/year — highest in the state</li>
  <li><strong>Ann Arbor:</strong> approximately $173/year — lowest in the state</li>
  <li><strong>Grand Rapids, Lansing, Flint:</strong> typically $180–$240/year</li>
</ul>

<p>Rates increased 5.8% in 2024 and another 6.6% in 2025 — Michigan is tracking above the national average on renters insurance inflation. Even so, $18/month to protect $25,000 in belongings is still a strong value proposition.</p>

<h2>Actual Cash Value vs. Replacement Cost: This Decision Matters</h2>

<p>When you buy renters insurance, you'll choose between two types of personal property coverage:</p>

<p><strong>Actual cash value (ACV)</strong> pays what your belongings are worth <em>today</em>, factoring in depreciation. Your 3-year-old MacBook is worth maybe $400 on the used market. If it's stolen, ACV pays you $400.</p>

<p><strong>Replacement cost coverage</strong> pays what it costs to replace the item with something comparable and new. That same MacBook costs $1,300 new. Replacement cost pays $1,300.</p>

<p>The premium difference between ACV and replacement cost renters insurance is usually $5–$15 per month. The payout difference after a real claim can be thousands. Always choose replacement cost.</p>

<h2>Michigan-Specific Risks Worth Understanding</h2>

<p>A few perils hit Michigan renters harder than the national average:</p>

<p><strong>Burst pipes.</strong> Michigan winters push temperatures well below zero. If heat in your building fails while you're traveling — or if your unit is in a poorly insulated structure — pipes freeze and burst. Your renters policy covers the resulting water damage to your belongings. The building damage is the landlord's problem.</p>

<p><strong>Ice dams.</strong> Ice dams form when heat escapes through a roof, melts snow, and refreezes at the eaves. The backed-up water works its way under shingles and into the building. If you're on an upper floor, this can damage your belongings. Covered under renters insurance as a water damage peril.</p>

<p><strong>Tornadoes.</strong> Michigan averages 15–17 tornadoes per year. Most are weak EF0 or EF1 events, but they cause real damage. Windstorm is a covered peril under standard renters insurance — your belongings damaged in a tornado are covered.</p>

<p><strong>Theft from your car.</strong> This one surprises people. Personal property stolen from your vehicle is typically covered under your renters policy — not your auto policy. So your laptop bag taken from your car in a parking lot is a renters insurance claim.</p>

<h2>How Much Coverage Do You Actually Need?</h2>

<p>Walk through your apartment and add up what it would cost to replace everything — not what you paid, but what it costs new today. Most renters underestimate badly. A modest one-bedroom adds up fast:</p>

<ul>
  <li>Living room furniture + TV: $3,000–$5,000</li>
  <li>Bedroom furniture + bedding: $2,000–$4,000</li>
  <li>Laptop, tablet, phone: $2,500–$4,000</li>
  <li>Kitchen items + appliances: $1,000–$3,000</li>
  <li>Clothing: $3,000–$8,000</li>
  <li>Miscellaneous tools, sports gear, accessories: $1,000–$3,000</li>
</ul>

<p>That's $12,500–$27,000 on the conservative end. Most people think they have $10,000 in stuff and actually have $25,000. Insure what you'd actually need to replace.</p>

<div class="callout-box">
  <p><strong>Pro move:</strong> Take a video walkthrough of every room in your apartment and store it in cloud storage. If you ever file a claim, that footage is invaluable documentation of what you owned. Takes 10 minutes; worth thousands.</p>
</div>

<h2>Frequently Asked Questions</h2>

<details class="faq-item">
  <summary>Does Michigan law require renters insurance?</summary>
  <div class="faq-body">
    <p>No state law requires it. But your lease might — and many Michigan landlords make it a lease condition. Even when it's not required, going without it means your belongings, your liability exposure, and your temporary housing costs are entirely unprotected. For $18/month, the coverage is worth it.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Does renters insurance cover theft from my car?</summary>
  <div class="faq-body">
    <p>Usually yes. Personal property stolen from your vehicle is typically covered under your renters policy's personal property section, subject to your deductible. This surprises a lot of Michigan renters — your laptop stolen from a parking lot goes through renters insurance, not auto insurance.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Does renters insurance cover flooding?</summary>
  <div class="faq-body">
    <p>No. Standard renters insurance doesn't cover flood damage. Water coming in from outside — a storm surge, an overflowing river, heavy rainfall — is excluded. If you're in a flood-prone area of Michigan, you'd need a separate NFIP or private flood policy to cover your belongings against that specific risk.</p>
  </div>
</details>

<details class="faq-item">
  <summary>What's the difference between actual cash value and replacement cost?</summary>
  <div class="faq-body">
    <p>ACV pays what your items are worth today after depreciation. Replacement cost pays what it costs to buy comparable new items. The premium difference is usually $5–$15/month. The claim payout difference can be thousands of dollars. Choose replacement cost if it's available — it almost always is.</p>
  </div>
</details>

<details class="faq-item">
  <summary>How much personal property coverage do I need?</summary>
  <div class="faq-body">
    <p>More than most renters expect. Walk through your apartment and estimate replacement cost on everything — furniture, electronics, clothing, kitchen gear, sports equipment. A modest one-bedroom in Michigan can easily total $20,000–$35,000. Most renters pick $15,000 and find out after a fire or theft that they were underinsured. We can help you build a quick inventory to get to the right number.</p>
  </div>
</details>
""",
    },

    {
        "slug": "how-to-file-homeowners-insurance-claim-michigan",
        "title": "How to File a Homeowners Insurance Claim in Michigan: A Step-by-Step Guide",
        "seo_title": "Filing a Home Insurance Claim in Michigan",
        "date": "2026-05-28", "date_display": "May 28, 2026", "date_modified": "2026-05-28",
        "category": "Home Insurance", "read_minutes": 8,
        "summary": "What you do in the first 24 hours after home damage can make or break your claim. Here's exactly what to do — and what to avoid — when filing a homeowners insurance claim in Michigan.",
        "meta_description": "Michigan homeowners: here's exactly how to file a home insurance claim step by step, including your legal rights, key deadlines, and what to do if your claim is denied.",
        "og_image": "/assets/img/blog/how-to-file-homeowners-insurance-claim-michigan.svg",
        "card_photo": "photo-1736217044407-822311e9c226",
        "related_posts": ["why-home-insurance-went-up-2026", "michigan-flood-insurance", "michigan-renters-insurance"],
        "faqs": [
            {"q": "How long does a homeowners insurance claim take in Michigan?",
             "a": "Michigan law requires insurers to pay within 60 days of receiving your complete proof of loss. Simple claims — a broken window, minor theft — often resolve in 2–4 weeks. Complex losses involving structural damage, large theft claims, or disputes about coverage can run longer, especially if documentation is incomplete. Your agent can push for faster resolution if things stall."},
            {"q": "Does filing a homeowners insurance claim raise my rates in Michigan?",
             "a": "It can, especially if you file frequently. Frequency of claims affects your risk profile more than the dollar amount of any single claim. One claim rarely causes a dramatic rate increase. Two or three claims in a three-year window can trigger meaningful increases or, in some cases, non-renewal. Call your agent before deciding whether to file — for small claims close to your deductible, paying out of pocket is often the smarter move."},
            {"q": "Do I need a police report to file a homeowners insurance claim in Michigan?",
             "a": "Not for every claim. For theft, burglary, or vandalism, yes — file a police report before contacting your insurer and get the report number. For weather damage, fire, accidental damage, or pipe bursts, a police report isn't required. Your insurer may ask for it on theft claims if you don't have one."},
            {"q": "Can I choose my own contractor for home insurance repairs in Michigan?",
             "a": "In most cases, yes. Some policies have preferred contractor networks, but Michigan law generally gives homeowners the right to use a licensed contractor of their choosing. Be careful about signing anything with a contractor before the adjuster has assessed the damage — some contractors include assignment of benefits language that can complicate your claim."},
            {"q": "What is 'proof of loss' and when do I need to submit it in Michigan?",
             "a": "A proof of loss is a sworn statement you sign detailing what was damaged or lost and its estimated value. Your insurer provides the form. Under Michigan law, you typically have 60 days to submit it after the insurer requests it. Missing that deadline can jeopardize your claim. Don't wait — get the form submitted promptly once you receive it."},
        ],
        "body_html": """
<p style="font-size:.9rem;background:var(--gray-50);border-left:4px solid var(--navy);padding:.75rem 1rem;border-radius:0 var(--r-sm) var(--r-sm) 0;margin-bottom:1.5rem;">
  Dealing with home damage in Michigan? Your JJA agent can guide you through the claims process. <a href="../../home-insurance/" style="color:var(--navy);font-weight:600;">Contact a Michigan home insurance agent →</a>
</p>

<p class="lead">A tree falls on your roof. Pipes burst in January. Someone breaks into your garage. What you do in the first 24 hours can make a real difference in how your claim gets processed — and how much you get paid. Here's exactly what to do when you need to file a homeowners insurance claim in Michigan, including the legal rights most homeowners don't know they have.</p>

<div class="callout-box">
  <p><strong>Know your rights:</strong> Michigan law requires your insurer to pay your claim within <strong>60 days</strong> of receiving your proof of loss. If they're late, they owe you <strong>12% simple interest</strong> on the overdue amount. Knowing this matters if your claim drags on.</p>
</div>

<h2>Step 1: Secure the Property and Document Everything First</h2>

<p>Before you touch anything, document the damage. Take photos and video of every affected area — wide shots for context, close-ups of specific damage. Walk through every room that was impacted. If your phone timestamps or geotags photos, use it. More documentation is always better than less.</p>

<p>Do not throw anything away before the adjuster sees it. That water-logged carpet, the broken window frame, the furniture that got ruined — your insurer needs to see the damage to compensate you for it. Cleaning up before the adjuster visits is one of the most common mistakes Michigan homeowners make after a loss.</p>

<p>If the damage makes your home unsafe, take emergency steps to stabilize it. Cover a hole in the roof with a tarp. Board up a broken window. Call an emergency plumber to stop a burst pipe. This isn't just smart — your policy requires you to take reasonable steps to prevent additional damage after a covered loss. Document these emergency repairs too.</p>

<h2>Step 2: File a Police Report When Required</h2>

<p>If your claim involves theft, burglary, or vandalism, call the police before you call your insurance company. File a report and get the report number — you'll need it when you submit your claim. Without a police report, theft claims are significantly harder to process and easier for insurers to dispute.</p>

<p>For weather damage, fire, water damage from burst pipes, or accidental damage, a police report isn't necessary. Skip this step for those scenarios and go straight to your insurer.</p>

<h2>Step 3: Call Your Agent Before the Insurance Company's 800 Number</h2>

<figure style="margin:1.5rem 0 2rem;">
  <img src="../../assets/img/blog/michigan-claims-process.svg"
       alt="Michigan homeowners insurance claims process — 6 steps from damage to payment"
       style="width:100%;height:auto;display:block;border-radius:8px;"
       loading="lazy" width="800" height="380">
  <figcaption style="font-size:.8rem;color:var(--text-muted);margin-top:.5rem;text-align:center;">The Michigan homeowners insurance claims process, step by step</figcaption>
</figure>

<p>Your agent knows your policy, your insurer's internal processes, and how to get things moving. Calling your agent first — not the generic 1-800 number — gives you real advantages:</p>

<ul>
  <li>Your agent can review your policy and tell you upfront whether the claim is likely to be covered</li>
  <li>They can advise you on whether the claim is worth filing, or whether paying out of pocket makes more sense given your deductible and rate history</li>
  <li>They'll know what documentation the specific insurer needs and flag issues before they become disputes</li>
  <li>If your claim gets pushed back, your agent can advocate on your behalf in ways you can't easily do yourself</li>
</ul>

<p>Not every claim is worth filing. If the damage is $800 and your deductible is $1,000, you're paying out of pocket anyway — and filing the claim creates a record that can affect your renewal rate. A two-minute call to your agent can help you make that call intelligently.</p>

<h2>Step 4: Understand the Michigan Claims Timeline</h2>

<p>Michigan law sets specific deadlines that work in your favor:</p>

<ul>
  <li><strong>Proof of loss:</strong> You typically have 60 days to submit it after your insurer requests it. Don't miss this deadline.</li>
  <li><strong>Payment deadline:</strong> Your insurer must pay within 60 days of receiving your complete, signed proof of loss.</li>
  <li><strong>Late payment penalty:</strong> If the insurer pays late, they owe you 12% simple interest on the overdue amount. This is Michigan law.</li>
  <li><strong>Coverage decision:</strong> Insurers must affirm or deny coverage within a reasonable time after proof of loss is complete. "Reasonable" is vague — if you feel the process is stalling, document your communications and contact your agent.</li>
</ul>

<h2>Step 5: The Adjuster Inspection — What to Know</h2>

<p>The adjuster's job is to assess the damage and assign a dollar figure. They work for the insurance company. That doesn't mean they're your adversary, but it does mean their initial estimate may not fully account for everything.</p>

<p>Be present for the inspection. Walk through every damaged area with the adjuster and point out everything. If you've already gotten your own contractor's estimate, have it ready. If the adjuster's estimate comes back lower than your contractor's, you have options: provide the contractor's estimate as a counteroffer, request a re-inspection, or ask your insurer to explain the discrepancy in writing.</p>

<p>You're not obligated to accept the first offer. Negotiating a claim isn't combative — it's normal. Most adjusters have some flexibility, especially when you have documentation and a competing estimate to back you up.</p>

<h2>What Not to Do After a Home Insurance Loss</h2>

<p>A few things Michigan homeowners commonly do that hurt their claims:</p>

<ul>
  <li><strong>Starting major repairs before the adjuster visit.</strong> Emergency stabilization is fine and required. Full repairs before the adjuster sees the damage is a problem — you've destroyed the evidence they need to assess.</li>
  <li><strong>Throwing away damaged items.</strong> Hold everything until the adjuster clears it or you've photographed it thoroughly.</li>
  <li><strong>Assuming coverage without checking.</strong> A lot of homeowners assume flooding, sewer backup, and earthquake are covered. They're usually not under a standard policy. Call your agent first.</li>
  <li><strong>Accepting a settlement that doesn't cover the real cost.</strong> You're not required to accept the first offer. You can negotiate, get your own estimates, and push back.</li>
  <li><strong>Signing contractor assignments of benefits before the adjuster visits.</strong> Some contractors present paperwork that transfers your insurance rights to them. Read before you sign — this can remove your control over the claims process.</li>
</ul>

<h2>Should You File Every Claim? Not Necessarily.</h2>

<p>This is the question most homeowners don't think to ask. Filing a claim creates a record. Multiple claims in a short window — say, two or three claims in three years — can trigger rate increases or non-renewal in Michigan, even if each individual claim was small and legitimate.</p>

<p>The rule of thumb: if the damage is at or below your deductible, don't file — you're paying out of pocket anyway and generating a claims record. If the damage is meaningfully above your deductible, file. For damage in the middle zone — say, $500 over your deductible — call your agent and run through the math before deciding.</p>

<h2>What to Do If Your Claim Is Denied</h2>

<p>A denial isn't the end of the road. Michigan homeowners have several options:</p>

<ol>
  <li><strong>Request the denial in writing.</strong> Your insurer is required to explain why coverage was denied. Get it in writing.</li>
  <li><strong>Review your policy language.</strong> The denial letter will cite specific policy language. Pull your policy and read the relevant section yourself. Sometimes denials are based on a misreading of the policy.</li>
  <li><strong>File an appeal with your insurer.</strong> Most insurers have a formal appeal process. Use it.</li>
  <li><strong>File a complaint with Michigan DIFS.</strong> The Michigan Department of Insurance and Financial Services investigates insurer conduct. Filing a DIFS complaint at michigan.gov/difs is free and often prompts faster resolution.</li>
  <li><strong>Consult a public adjuster or insurance attorney.</strong> For large claims, this is worth it. Public adjusters work on contingency; they get paid a percentage of your settlement, so they're motivated to maximize it.</li>
</ol>

<div class="callout-box">
  <p><strong>Your JJA agent as advocate:</strong> If your claim runs into problems — slow payment, a disputed estimate, or a denial you believe is wrong — call us. We know how to work with carriers on your behalf. That's part of what you pay for when you work with an independent agent rather than calling a 1-800 number.</p>
</div>

<h2>Frequently Asked Questions</h2>

<details class="faq-item">
  <summary>How long does a homeowners insurance claim take in Michigan?</summary>
  <div class="faq-body">
    <p>Michigan law requires payment within 60 days of receiving your complete proof of loss. Simple claims often resolve in 2–4 weeks. Complex losses involving structural damage or coverage disputes take longer. Keep your documentation tight and your responses prompt — delays on your end push the timeline out.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Does filing a homeowners claim raise my rates in Michigan?</summary>
  <div class="faq-body">
    <p>It can. One claim rarely causes dramatic rate increases. Two or three claims in three years can trigger meaningful increases or non-renewal. Before filing, call your agent to assess whether the claim is worth it relative to your deductible and rate history. For small claims near your deductible, paying out of pocket is often the smarter long-term move.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Do I need a police report for a home insurance claim in Michigan?</summary>
  <div class="faq-body">
    <p>Yes for theft, burglary, and vandalism — file the police report before calling your insurer. No for weather damage, fire, accidental damage, or pipe bursts. Get the report number and keep a copy for your claim file.</p>
  </div>
</details>

<details class="faq-item">
  <summary>Can I use my own contractor for insurance repairs in Michigan?</summary>
  <div class="faq-body">
    <p>In most cases, yes. Michigan law gives homeowners the right to use a licensed contractor of their choosing. Some policies have preferred vendor programs, but they're generally not mandatory. Be cautious about signing contractor paperwork that includes assignment of benefits language before the adjuster has assessed the damage.</p>
  </div>
</details>

<details class="faq-item">
  <summary>What is a proof of loss and when is it due?</summary>
  <div class="faq-body">
    <p>A proof of loss is a sworn statement detailing what was damaged and its value. Your insurer provides the form. In Michigan, you typically have 60 days to submit it after the insurer requests it. Missing this deadline can jeopardize your claim — submit it promptly once you receive the form.</p>
  </div>
</details>
""",
    },

]  # end POSTS

POSTS.sort(key=lambda p: p['date'], reverse=True)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def utility_bar():
    return '''<div class="utility-bar">
  <div class="container">
    <span class="utility-item">📍 4301 S. Baldwin Rd, Lake Orion, MI 48359</span>
    <span class="utility-item">📞 <a href="tel:+12486936455">(248) 693-6455</a></span>
    <span class="utility-item">✉️ <a href="mailto:Support@jjainsurance.com">Support@jjainsurance.com</a></span>
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
        <li><a href="{rel}personal/">Personal</a></li>
        <li><a href="{rel}business/">Business</a></li>
        <li><a href="{rel}faq/">FAQ</a></li>
        <li><a href="{rel}blog/">Blog</a></li>
        <li><a href="{rel}reviews/">Reviews</a></li>
        <li><a href="{rel}about/">About</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a class="btn btn-outline" href="tel:+12486936455">Call</a>
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
      </div>
      <div class="footer-col">
        <h4>Personal Insurance</h4>
        <ul>
          <li><a href="{rel}personal/">Overview</a></li>
          <li><a href="{rel}auto-insurance/">Auto Insurance</a></li>
          <li><a href="{rel}home-insurance/">Homeowners Insurance</a></li>
          <li><a href="{rel}life-insurance/">Life Insurance</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Business Insurance</h4>
        <ul>
          <li><a href="{rel}business/">Overview</a></li>
          <li><a href="{rel}business-insurance/">General Liability</a></li>
          <li><a href="{rel}workers-comp/">Workers Comp</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="{rel}about/">About Us</a></li>
          <li><a href="{rel}team/">Our Team</a></li>
          <li><a href="{rel}reviews/">Reviews</a></li>
          <li><a href="{rel}contact/">Contact</a></li>
          <li><a href="{rel}blog/">Blog</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 J. Jacobs &amp; Associates Insurance. All rights reserved. | <a href="{rel}privacy-policy/">Privacy Policy</a></p>
      <p style="font-size:.8rem;margin-top:.5rem;">Licensed in Michigan. 4301 S. Baldwin Rd, Lake Orion, MI 48359 | (248) 693-6455</p>
    </div>
  </div>
</footer>'''

# ─────────────────────────────────────────────────────────────
# HEAD
# ─────────────────────────────────────────────────────────────
def head(title, description, canonical_path, og_image=None, extra_schema="",
         pub_date="", mod_date="", article_section=""):
    og_image_url = og_image or f"{SITE_URL}/assets/img/og-default.jpg"
    if not og_image_url.startswith("http"):
        og_image_url = SITE_URL + og_image_url

    article_tags = ""
    if pub_date:
        article_tags += f'\n<meta property="article:published_time" content="{pub_date}">'
        article_tags += f'\n<meta property="article:modified_time" content="{mod_date or pub_date}">'
        article_tags += f'\n<meta property="article:author" content="{SITE_URL}/team/">'
    if article_section:
        article_tags += f'\n<meta property="article:section" content="{article_section}">'

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
<meta property="og:site_name" content="JJA Insurance">
<meta property="og:image" content="{og_image_url}">
<meta property="og:locale" content="en_US">{article_tags}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:creator" content="@JJAInsurance">
<link rel="sitemap" type="application/xml" href="{SITE_URL}/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{extra_schema}
<link rel="stylesheet" href="../../assets/css/styles.css?v={VERSION}">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

# ─────────────────────────────────────────────────────────────
# RENDER POST
# ─────────────────────────────────────────────────────────────
def render_post(i, p, all_posts):
    if p.get("prebuilt"):
        return  # skip existing posts

    prev_post = all_posts[i-1] if i > 0 else None
    next_post = all_posts[i+1] if i < len(all_posts)-1 else None

    seo_title  = p.get("seo_title", p["title"])
    mod_date   = p.get("date_modified", p["date"])
    og_img_url = SITE_URL + p["og_image"] if p.get("og_image") else f"{SITE_URL}/assets/img/og-default.jpg"

    # ── Schemas ──────────────────────────────────────────────
    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "datePublished": p["date"],
        "dateModified": mod_date,
        "author": {"@type": "Person", "name": "Joseph Jacobs", "url": f"{SITE_URL}/team/"},
        "publisher": {"@type": "Organization", "name": "J. Jacobs & Associates",
                      "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/img/logo.jpeg"}},
        "description": p["meta_description"],
        "image": og_img_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE_URL}/blog/{p['slug']}/"}
    })

    bc_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"][:80], "item": f"{SITE_URL}/blog/{p['slug']}/"},
        ]
    })

    faq_schema = ""
    if p.get("faqs"):
        faq_schema = json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in p["faqs"]
            ]
        })

    speakable_schema = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "speakable": {"@type": "SpeakableSpecification",
                      "cssSelector": [".blog-post-header h1", ".blog-post-body .lead", ".blog-post-body h2:first-of-type"]},
        "url": f"{SITE_URL}/blog/{p['slug']}/"
    })

    all_schemas = (
        f'<script type="application/ld+json">\n{article_schema}\n</script>\n'
        f'<script type="application/ld+json">\n{bc_schema}\n</script>\n'
        + (f'<script type="application/ld+json">\n{faq_schema}\n</script>\n' if faq_schema else "")
        + f'<script type="application/ld+json">\n{speakable_schema}\n</script>'
    )

    h = head(
        title=f'{seo_title} | JJA Insurance',
        description=p["meta_description"],
        canonical_path=f"/blog/{p['slug']}/",
        og_image=p.get("og_image"),
        extra_schema=all_schemas,
        pub_date=p["date"],
        mod_date=mod_date,
        article_section=p.get("category", "Insurance Education"),
    )

    # ── Related posts ─────────────────────────────────────────
    slug_map = {post["slug"]: post for post in all_posts}
    related_section = ""
    if p.get("related_posts"):
        rel_cards = []
        for rel_slug in p["related_posts"][:3]:
            rp = slug_map.get(rel_slug)
            if rp:
                rel_cards.append(
                    f'<a href="../{rp["slug"]}/" style="display:block;padding:1rem;border:1px solid var(--border);border-radius:var(--r-md);text-decoration:none;color:inherit;transition:border-color .2s;">'
                    f'<span style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;">{rp["category"]}</span>'
                    f'<p style="margin:.25rem 0 0;font-weight:600;color:var(--ink);font-size:.95rem;">{rp["title"]}</p>'
                    f'</a>'
                )
        if rel_cards:
            related_section = (
                '<div style="margin:2.5rem 0;padding-top:2rem;border-top:1px solid var(--border);">'
                '<h3 style="font-size:1rem;text-transform:uppercase;letter-spacing:.06em;color:var(--text-muted);margin-bottom:1rem;">Related Articles</h3>'
                '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;">'
                + ''.join(rel_cards) + '</div></div>'
            )

    # ── Author bio ────────────────────────────────────────────
    author_bio = '''<div style="display:flex;align-items:flex-start;gap:1.25rem;background:var(--gray-50);border:1px solid var(--border);border-radius:var(--r-md);padding:1.5rem;margin:2rem 0;">
      <img src="../../assets/img/joseph-jacobs.jpg" alt="Joseph Jacobs, founder of JJA Insurance"
           style="width:72px;height:72px;border-radius:50%;object-fit:cover;flex-shrink:0;"
           onerror="this.style.display=\'none\'">
      <div>
        <strong style="display:block;font-size:1rem;color:var(--ink);">Joseph Jacobs</strong>
        <span style="font-size:0.85rem;color:var(--text-muted);">Licensed Michigan Insurance Agent &amp; Founder</span>
        <p style="margin:0.5rem 0 0;font-size:0.9rem;color:var(--text);">Joseph founded J. Jacobs &amp; Associates in 1981 and has spent 45 years helping Michigan families and businesses navigate insurance. He holds licenses across personal and commercial lines and has earned Lake Orion&#39;s Readers&#39; Choice Best Insurance Agency eight consecutive years (2018–2025). <a href="../../team/" style="color:var(--navy);">Meet our team →</a></p>
      </div>
    </div>'''

    # ── Nav ───────────────────────────────────────────────────
    nav_links = []
    if prev_post:
        nav_links.append(f'<a class="post-nav-link prev" href="../{prev_post["slug"]}/"><span class="post-nav-label">← Previous</span><span class="post-nav-title">{prev_post["title"]}</span></a>')
    if next_post:
        nav_links.append(f'<a class="post-nav-link next" href="../{next_post["slug"]}/"><span class="post-nav-label">Next →</span><span class="post-nav-title">{next_post["title"]}</span></a>')
    post_nav = '<nav class="post-nav">' + ''.join(nav_links) + '</nav>' if nav_links else ''

    # ── Hero figure ───────────────────────────────────────────
    hero_fig = f'<figure style="margin:0 0 2rem;border-radius:12px;overflow:hidden;"><img src="../../assets/img/blog/{p["slug"]}.svg" alt="{p["title"]}" style="width:100%;height:auto;display:block;" loading="eager" width="1200" height="630"></figure>'

    article = f'''
<article class="blog-post">
  <header class="blog-post-header">
    <span class="eyebrow">{p["category"]}</span>
    <h1>{p["title"]}</h1>
    <div class="blog-post-meta">
      <span>By <strong>Joseph Jacobs</strong></span>
      <span>·</span>
      <time datetime="{p["date"]}">{p["date_display"]}</time>
      <span>·</span>
      <span>{p["read_minutes"]} min read</span>
    </div>
  </header>

  <div class="blog-post-body">
    {hero_fig}
    {p["body_html"]}
  </div>

  {related_section}

  <footer class="blog-post-footer">
    {author_bio}

    <div class="blog-post-cta">
      <h2>Have questions about your coverage?</h2>
      <p>Our Michigan-licensed agents are happy to review your policy and answer your questions — no cost, no obligation.</p>
      <p><a class="btn btn-primary btn-lg" href="../../quotes/">Get a Free Quote</a>&nbsp;<a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a></p>
    </div>

    <div class="blog-disclaimer">
      <p><strong>Disclaimer:</strong> This blog post is intended for general educational purposes only and does not constitute insurance advice for any specific situation. Coverage availability, terms, and pricing vary by insurer, policy form, and individual risk characteristics. Michigan insurance laws and regulations are subject to change. Consult a licensed Michigan insurance agent for advice specific to your circumstances. J. Jacobs and Associates is licensed in the state of Michigan.</p>
    </div>

    {post_nav}
  </footer>
</article>'''

    body = (
        utility_bar() + '\n' +
        header('../../') + '\n' +
        f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol><li><a href="../../">Home</a></li><li><a href="../">Blog</a></li><li>{p["title"][:60]}</li></ol></div></nav>\n' +
        '<main id="main">\n<section class="section"><div class="container" style="max-width:820px;">' +
        article +
        '</div></section>\n</main>\n' +
        footer('../../')
    )

    out = Path(f'blog/{p["slug"]}/index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h + body, encoding='utf-8')
    print(f"  ✓ blog/{p['slug']}/index.html")


# ─────────────────────────────────────────────────────────────
# RENDER INDEX
# ─────────────────────────────────────────────────────────────
def render_index(all_posts):
    cards = ""
    for p in all_posts:
        og_url = SITE_URL + p["og_image"] if p.get("og_image") else f"{SITE_URL}/assets/img/og-default.jpg"
        if p.get("card_photo"):
            pid = p["card_photo"]
            # Local files (infographics) use a relative fallback; Unsplash photos use CDN JPEG
            if pid.startswith("photo-") or pid.startswith("premium_photo-"):
                fallback_src = f"https://images.unsplash.com/{pid}?w=800&q=85&auto=format&fit=crop&fm=jpg"
            else:
                fallback_src = f"../assets/img/blog/{pid}.avif"
            card_img = f'''<picture>
      <source srcset="../assets/img/blog/{pid}.avif" type="image/avif">
      <img src="{fallback_src}" alt="{p["title"]}" loading="lazy" width="400" height="210" style="width:100%;height:auto;display:block;object-fit:cover;">
    </picture>'''
        else:
            card_img = f'<img src="{og_url}" alt="{p["title"]}" loading="lazy" width="400" height="210">'
        cards += f'''  <a href="./{p["slug"]}/" class="post-card">
    <div class="post-card-img">
      {card_img}
    </div>
    <div class="post-card-body">
      <span class="eyebrow">{p["category"]}</span>
      <h2 class="post-card-title">{p["title"]}</h2>
      <p>{p["summary"]}</p>
      <div class="post-card-meta">
        <time datetime="{p["date"]}">{p["date_display"]}</time>
        <span>·</span>
        <span>{p["read_minutes"]} min read</span>
      </div>
    </div>
  </a>\n'''

    bc_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
        ]
    })
    blog_schema = json.dumps({
        "@context": "https://schema.org", "@type": "Blog",
        "name": "JJA Insurance Blog",
        "url": f"{SITE_URL}/blog/",
        "description": "Michigan insurance tips, coverage guides, and expert advice from J. Jacobs & Associates.",
        "publisher": {"@type": "Organization", "name": "J. Jacobs & Associates", "url": SITE_URL}
    })
    all_schemas = (
        f'<script type="application/ld+json">\n{bc_schema}\n</script>\n'
        f'<script type="application/ld+json">\n{blog_schema}\n</script>'
    )

    og_index = SITE_URL + "/assets/img/blog-index-og.svg"
    h = head(
        title="Insurance Blog | Michigan Insurance Tips | JJA Insurance",
        description="Michigan insurance tips, coverage guides, and expert advice from a family-owned independent agency serving Lake Orion and greater Michigan since 1981.",
        canonical_path="/blog/",
        og_image=og_index,
        extra_schema=all_schemas,
    )
    # Fix stylesheet path for index (one level deep)
    h = h.replace('href="../../assets', 'href="../assets')
    h = h.replace('src="../../assets', 'src="../assets')

    body = (
        utility_bar() + '\n' +
        header('../') + '\n' +
        '<main id="main">\n<section class="section">\n<div class="container">\n' +
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li>Blog</li></ol></nav>\n' +
        '<h1 class="section-title">Michigan Insurance Blog</h1>\n' +
        '<p class="section-subtitle">Practical insurance guides from Michigan-licensed agents with 45 years of experience.</p>\n' +
        '<div class="post-grid">\n' + cards + '</div>\n' +
        '</div>\n</section>\n</main>\n' +
        footer('../')
    )

    Path('blog/index.html').write_text(h + body, encoding='utf-8')
    print("  ✓ blog/index.html")

# ─────────────────────────────────────────────────────────────
# UPDATE SITEMAP
# ─────────────────────────────────────────────────────────────
def update_sitemap(all_posts):
    import re as _re
    sitemap_path = Path('sitemap.xml')
    sitemap = sitemap_path.read_text(encoding='utf-8')

    # Add image namespace if missing
    if 'xmlns:image' not in sitemap:
        sitemap = sitemap.replace(
            'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
        )

    # Remove all existing blog entries
    sitemap = _re.sub(r'\s*<url>\s*<loc>https://www\.jjainsurance\.com/blog[^<]*</loc>[\s\S]*?</url>', '', sitemap)

    # Build new entries
    today = "2026-05-28"
    new_entries = f'''
  <url>
    <loc>{SITE_URL}/blog/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>'''

    for p in all_posts:
        mod = p.get("date_modified", p["date"])
        img_url = SITE_URL + p["og_image"] if p.get("og_image") else ""
        img_entry = f'''
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>{p["title"]}</image:title>
    </image:image>''' if img_url else ""
        new_entries += f'''
  <url>
    <loc>{SITE_URL}/blog/{p["slug"]}/</loc>
    <lastmod>{mod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>{img_entry}
  </url>'''

    sitemap = sitemap.replace('</urlset>', new_entries + '\n</urlset>')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print(f"  ✓ sitemap.xml ({len(all_posts)} blog posts)")


# BUILD
# ------------------------------------------------------------------
def build():
    import os as _os
    _os.chdir(str(Path(__file__).parent))
    print("Building JJA blog...")
    all_posts = POSTS
    for i, p in enumerate(all_posts):
        render_post(i, p, all_posts)
    render_index(all_posts)
    update_sitemap(all_posts)
    print("\nDone.")

if __name__ == "__main__":
    build()
