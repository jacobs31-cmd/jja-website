#!/usr/bin/env python3
"""
JJA Insurance — Buffer Post Scheduler
Schedules all 114 social media posts via Buffer's GraphQL API.
Run: python3 schedule_to_buffer.py
When prompted, paste your Buffer API key.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# ── CONFIG ────────────────────────────────────────────────────────────────────
GRAPHQL_URL     = "https://api.buffer.com"
ORG_ID          = "6a14a87235f22ccc6a284ead"
TIMEZONE_OFFSET = -4  # EDT (Eastern Daylight Time, UTC-4, May–Aug)

# ── ALL 114 POSTS ─────────────────────────────────────────────────────────────
# Format: (date MM/DD/YYYY, time HH:MM, platform, message)
PHONE    = "(248) 693-6455"
QUOTE    = "https://jjainsurance.com/quotes/"
URLS = {
    "cyber":    "https://jjainsurance.com/blog/does-your-michigan-business-need-cyber-insurance/",
    "home":     "https://jjainsurance.com/blog/why-home-insurance-went-up-2026/",
    "moto":     "https://jjainsurance.com/blog/michigan-motorcycle-insurance-terminology/",
    "q25":      "https://jjainsurance.com/blog/michigan-insurance-questions-answered/",
    "autogl":   "https://jjainsurance.com/blog/michigan-auto-insurance-glossary/",
    "homegl":   "https://jjainsurance.com/blog/michigan-homeowners-insurance-glossary/",
    "nofault":  "https://jjainsurance.com/blog/michigan-no-fault-option-6/",
    "wcaudit":  "https://jjainsurance.com/blog/what-happens-if-you-skip-your-workers-comp-audit-in-michigan/",
    "wcguide":  "https://jjainsurance.com/blog/michigan-workers-compensation-do-you-need-it-guide-for-business-owners/",
    "autoterm": "https://jjainsurance.com/blog/common-auto-insurance-terms/",
    "event":    "https://jjainsurance.com/blog/special-event-insurance/",
    "scam":     "https://jjainsurance.com/blog/protect-yourself-from-auto-insurance-refund-scams/",
    "storm":    "https://jjainsurance.com/blog/does-your-michigan-homeowners-insurance-cover-storm-damage/",
}

# Branded social images (served live from the site). Every post gets one.
# Keep this map + pick_image() in sync with schedule_instagram.py.
IMAGES = {
    "home":       "https://jjainsurance.com/social-images/jja_home_insurance.png",
    "auto":       "https://jjainsurance.com/social-images/jja_auto_insurance.png",
    "commercial": "https://jjainsurance.com/social-images/jja_commercial.png",
    "workers":    "https://jjainsurance.com/social-images/jja_workers_comp.png",
    "life":       "https://jjainsurance.com/social-images/jja_life_insurance.png",
    "tips":       "https://jjainsurance.com/social-images/jja_insurance_tips.png",
}

def pick_image(text):
    """Pick a branded image by keyword. Mirrors schedule_instagram.py.pick_image."""
    t = text.lower()
    if any(k in t for k in ["home insurance", "homeowners", "flood", "roof", "deductible", "replacement cost", "storm"]):
        return IMAGES["home"]
    if any(k in t for k in ["workers", "wcaudit"]):
        return IMAGES["workers"]
    if any(k in t for k in ["commercial", "cyber", "ransomware", "business policy", "special event", "summer event", "event insurance"]):
        return IMAGES["commercial"]
    if any(k in t for k in ["life insurance", "10-12x", "financially okay"]):
        return IMAGES["life"]
    if any(k in t for k in ["auto", "vehicle", "car", "motorcycle", "no-fault", "driver", "scam", "refund", "collision", "comprehensive", "uninsured", "pip", "two wheels", "teen driver", "boat", "atv", "jet ski"]):
        return IMAGES["auto"]
    return IMAGES["tips"]

POSTS = [
("05/26/2026","10:00","Facebook",f"Your homeowners insurance didn't go up because your house got more valuable. It went up because construction costs, weather claims, and reinsurance rates all spiked at once — and carriers passed it down the line.\n\nWe've put together 7 ways Michigan homeowners can fight back and actually lower their premium. Worth a read before your next renewal.\n\n{URLS['home']}\n\nWant us to shop it for you? We work with 20+ personal lines carriers. Call {PHONE} or visit {QUOTE}"),
("05/26/2026","11:00","Instagram",f"Your home insurance went up — here's why, and what you can do about it.\n\nWe wrote a full breakdown for Michigan homeowners. Link in bio.\n\n#HomeInsurance #Michigan #InsuranceTips #LakeOrion #MichiganHomes #SaveMoney"),
("05/26/2026","12:00","X",f"Michigan homeowners: Your premium went up because of construction costs, weather claims, and reinsurance — not your house. Here are 7 ways to fight back. {URLS['home']}"),
("05/27/2026","09:00","LinkedIn",f"If your homeowners insurance renewal arrived and you felt blindsided by the increase, you're not alone.\n\nWe put together a plain-English breakdown of exactly why Michigan home insurance premiums jumped in 2026 — and 7 concrete steps you can take before your next renewal to bring that number down.\n\nAs an independent agency, we shop 20+ personal lines carriers simultaneously. That means we find the best rate across the market, not just one company's offering.\n\nRead the full breakdown here: {URLS['home']}\n\nOr call us directly at {PHONE} — we're happy to do a no-cost policy review."),
("05/27/2026","12:00","X",f"The average Michigan homeowner saw a 15–20% rate hike last renewal cycle. Here's what's driving it — and how to push back. {URLS['home']} | {PHONE}"),
("05/28/2026","10:00","Facebook",f"Quick tip: One of the fastest ways to lower your home insurance premium is to raise your deductible — but only if you have that amount sitting in savings.\n\nGoing from a $500 to a $2,500 deductible can cut your premium by 15–25%. It's not the right move for everyone, but it's worth the conversation.\n\nWe can run through the numbers with you in 10 minutes. Call {PHONE} or get a quote at {QUOTE}"),
("05/28/2026","11:00","Instagram",f"Deductible too low? Raising it could save you hundreds a year — if the timing is right.\n\nWe'll help you figure out if it makes sense for your situation. Call us or click the link in bio.\n#InsuranceTip #HomeInsurance #Michigan #SaveMoney #LakeOrion"),
("05/28/2026","12:00","X",f"Raising your home insurance deductible from $500 to $2,500 can cut your premium by 15-25%. Only smart if you have the savings. Worth discussing. {PHONE}"),
("05/29/2026","09:00","LinkedIn",f"Three things most Michigan homeowners don't know are dragging their home insurance premium up:\n\n1. Claims history — even claims you didn't file but only inquired about\n2. Credit score — carriers in Michigan are still allowed to factor it in\n3. Outdated coverage amounts — if your home's rebuild value hasn't been updated in 3+ years, your rate may be inflated\n\nWe wrote a full guide on this. More importantly, we can do a no-cost policy review and tell you exactly where you stand.\n\n{URLS['home']} | Call {PHONE}"),
("06/01/2026","10:00","Facebook",f"Did you know bundling your home and auto with the same carrier can save you up to 20%? It sounds simple, but most people never ask because they got their policies at different times from different agents.\n\nAs an independent agency, we can bundle across carriers to find your best combined rate. Sometimes staying separate is smarter — we'll tell you honestly either way.\n\nCall {PHONE} or start a quote at {QUOTE}"),
("06/01/2026","11:00","Instagram",f"Bundling home + auto can save you up to 20%. Most people just never ask.\n\nWe shop 20+ carriers to find your best combined rate. Link in bio to get started.\n#BundleAndSave #Michigan #Insurance #HomeInsurance #AutoInsurance #LakeOrion"),
("06/01/2026","12:00","X",f"Bundling home + auto insurance can save you 10-20%. Most people don't ask because their policies came from different places at different times. We fix that. {QUOTE}"),
("06/02/2026","09:00","LinkedIn",f"A client came to us paying $4,200/year across two separate carriers — one for home, one for auto.\n\nAfter shopping both together across our 20+ personal lines carriers, we placed them with one carrier for $3,100 combined. Same coverage. $1,100 saved.\n\nWe don't earn more by bundling — we just find the best fit. That's what an independent agent does.\n\nWorth a 10-minute conversation? Call {PHONE} or visit {QUOTE}"),
("06/02/2026","12:00","X",f"Captive agents (State Farm, Allstate) show you one rate. We shop 20+ carriers at once. The math tends to favor choice. {QUOTE} | {PHONE}"),
("06/03/2026","10:00","Facebook",f"Michigan drivers: do you actually understand your no-fault coverage?\n\nMost people pick a PIP level at renewal and never think about it again. But the option you chose determines what gets paid if you're in a serious accident — including whether Medicare steps in or not.\n\nWe wrote a guide specifically on Option 6 (the Medicare coordination option): {URLS['nofault']}\n\nQuestions? Call {PHONE} — our agents know Michigan no-fault law cold."),
("06/03/2026","11:00","Instagram",f"Michigan auto insurance has 6 PIP options. Most people have no idea which one they picked.\n\nRead the breakdown — link in bio.\n#MichiganNoFault #AutoInsurance #Michigan #InsuranceTips #LakeOrion"),
("06/03/2026","12:00","X",f"Michigan drivers: Do you know which PIP option you selected? It determines how your medical bills get paid if you're in a crash. Quick read: {URLS['nofault']}"),
("06/04/2026","09:00","LinkedIn",f"Michigan's no-fault reform gave drivers 6 PIP coverage levels to choose from. Most made that choice quickly at renewal and moved on.\n\nBut that choice has real consequences — especially for drivers on Medicare. Option 6 lets Medicare serve as your primary medical coverage, which lowers your premium but leaves gaps most people don't discover until they need it.\n\nWe wrote a detailed breakdown of what Medicare covers (and doesn't) under Option 6: {URLS['nofault']}\n\nIf you want a plain-English review of your own coverage, call us at {PHONE}."),
("06/08/2026","10:00","Facebook",f"Michigan law requires most employers to carry workers' comp — but the rules have exceptions that confuse a lot of small business owners.\n\nSole proprietors. LLCs. Family members. Seasonal workers. The rules are different for each.\n\nWe wrote a guide that breaks it all down without the legalese: {URLS['wcguide']}\n\nNot sure if your business is covered the right way? Call {PHONE} — we work with 20+ commercial carriers."),
("06/08/2026","11:00","Instagram",f"Michigan business owners — do you actually need workers' comp insurance? The answer depends on more than just how many employees you have.\n\nFull guide at the link in bio.\n#WorkersComp #MichiganBusiness #SmallBusiness #BusinessInsurance #LakeOrion"),
("06/08/2026","12:00","X",f"Michigan business owners: sole proprietors, LLCs, and family-member employees all have different workers' comp rules. Don't assume you're covered. {URLS['wcguide']}"),
("06/09/2026","09:00","LinkedIn",f"Michigan workers' comp law catches a lot of small business owners off guard.\n\nCommon misconceptions:\n• 'I only have 1099 contractors, so I don't need it' — not always true\n• 'My LLC protects me' — workers' comp is separate from liability protection\n• 'I'm a sole proprietor so I'm exempt' — correct, but your employees aren't\n\nWe wrote a plain-English guide specifically for Michigan small business owners: {URLS['wcguide']}\n\nWe work with 20+ commercial carriers. Call {PHONE}."),
("06/09/2026","12:00","X",f"'I only have 1099 contractors, so I don't need workers comp.' This is wrong more often than people think in Michigan. Read why: {URLS['wcguide']}"),
("06/10/2026","10:00","Facebook",f"Skipping a workers' comp audit in Michigan isn't just inconvenient — it can trigger a policy cancellation, a significant premium penalty, and in some cases, a fine from the state.\n\nHere's exactly what happens when you skip: {URLS['wcaudit']}\n\nWe make the audit process simple. Call {PHONE}."),
("06/10/2026","11:00","Instagram",f"Skipping your workers' comp audit in Michigan can cost you way more than completing it.\n\nHere's what happens — link in bio.\n#WorkersComp #MichiganBusiness #BusinessInsurance #Insurance #LakeOrion"),
("06/10/2026","12:00","X",f"Skipping a workers' comp audit in Michigan: policy cancellation, premium penalties, and potential state fines. It's not worth it. {URLS['wcaudit']}"),
("06/11/2026","09:00","LinkedIn",f"Workers' comp audits aren't optional — and skipping one in Michigan has consequences that go beyond just an awkward phone call from your carrier.\n\nThe short version: your insurer estimated your payroll at the start of the policy year. The audit reconciles that estimate against reality. Skip it, and they assume the worst-case number — plus tack on penalties.\n\nDetailed breakdown here: {URLS['wcaudit']}\n\nWe handle workers' comp for Michigan businesses of all sizes. Call us at {PHONE}."),
("06/12/2026","10:00","Facebook",f"Michigan storm season is here. When a summer thunderstorm tears shingles off your roof or drops a tree limb through the garage, will your homeowners insurance pay for it?\n\nFor most Michigan homeowners, yes — wind, hail, and fallen trees are core covered perils. But a few things catch people off guard:\n\n- Flooding and basement backups are NOT covered by a standard policy\n- Many policies now carry a separate wind/hail deductible that's a percentage of your home's value\n- Old roofs are increasingly paid out at depreciated value, not full replacement\n\nWe broke it all down — what's covered, what isn't, and what to do before the next storm: {URLS['storm']}\n\nWant a no-cost policy review before storm season peaks? Call {PHONE} or visit {QUOTE}"),
("06/12/2026","12:00","X",f"Michigan storm season reminder: your homeowners policy covers wind, hail, and fallen trees — but NOT flooding or sewer backup. And watch for a percentage-based wind/hail deductible. What's covered and what isn't: {URLS['storm']}"),
("06/13/2026","09:00","LinkedIn",f"Michigan summers bring powerful storms — and a lot of confusion about what homeowners insurance actually covers.\n\nThe short version for Michigan homeowners:\n• Covered: wind and hail damage to roof and siding, fallen trees, detached structures, interior water damage from a storm-breached roof, power surge\n• Not covered: flooding (needs a separate flood policy), sewer/drain backup and sump-pump failure (need an endorsement)\n• Watch your deductible: many policies now apply a separate wind/hail deductible calculated as 1–2% of your home's insured value — on a $300K home, that's far more out of pocket than a flat deductible\n\nNearly half of all home insurance claims nationwide come from wind and hail, and Michigan has been hit by at least one billion-dollar storm every year since 2011. This is worth a five-minute policy check.\n\nFull breakdown: {URLS['storm']}\n\nWant us to review your coverage before peak season? Call {PHONE} or visit {QUOTE}"),
("06/15/2026","10:00","Facebook",f"Cyberattacks aren't just a big-company problem. The average ransom demand for a small business attack is now over $100,000 — and your standard business policy doesn't cover it.\n\nDoes your Michigan business have cyber insurance? Read our guide: {URLS['cyber']}\n\nOr call {PHONE} — we work with 20+ commercial carriers and can get you quoted today."),
("06/15/2026","11:00","Instagram",f"Small businesses are the #1 target for ransomware attacks. And your standard business policy? Doesn't cover it.\n\nCyber insurance guide for Michigan businesses — link in bio.\n#CyberInsurance #SmallBusiness #Michigan #BusinessInsurance #LakeOrion"),
("06/15/2026","12:00","X",f"60% of small businesses close within 6 months of a cyberattack. Most standard business policies don't cover it. Michigan businesses — here's what you need to know: {URLS['cyber']}"),
("06/16/2026","09:00","LinkedIn",f"Cyber insurance has gone from a niche add-on to a standard business necessity in about three years.\n\nMost general liability and BOP policies exclude cyber events entirely.\n\nWe put together a plain-English guide for Michigan business owners on what cyber coverage actually includes: {URLS['cyber']}\n\nIf you're not sure whether your current policy covers a data breach, call {PHONE}."),
("06/16/2026","12:00","X",f"Your BOP covers slip-and-falls. It does not cover a phishing email that locks your systems and demands $80,000. Those are different policies. {URLS['cyber']} | {PHONE}"),
("06/17/2026","10:00","Facebook",f"Planning a graduation party, outdoor wedding, festival, or fundraiser in Michigan this summer?\n\nSpecial event insurance is a one-time policy that covers liability if someone gets hurt, property damage, and sometimes vendor cancellations. It's affordable, fast to get, and most venues require it now.\n\nRead more about when you need it: {URLS['event']}\n\nGet a quote at {QUOTE} or call {PHONE}."),
("06/17/2026","11:00","Instagram",f"Summer event coming up? Most Michigan venues now require special event insurance — and it's more affordable than you'd think.\n\nFind out if you need it — link in bio.\n#EventInsurance #Michigan #WeddingInsurance #SummerEvents #LakeOrion"),
("06/17/2026","12:00","X",f"Hosting an outdoor event in Michigan this summer? Most venues now require event liability insurance. Here's what it covers and what it costs: {URLS['event']} | {PHONE}"),
("06/18/2026","09:00","LinkedIn",f"If your company is hosting a summer event — a client appreciation dinner, a golf outing, a fundraiser — you may need special event insurance.\n\nGeneral liability typically doesn't extend to off-site events, and venues are increasingly requiring their own certificate.\n\nThis is straightforward coverage, fast to place, and usually very affordable. Our team can turn it around same-day in most cases.\n\nMore info: {URLS['event']} | Call {PHONE}"),
("06/22/2026","10:00","Facebook",f"Do you know the difference between collision and comprehensive coverage?\n\nCollision: covers damage from hitting another car or object.\nComprehensive: covers everything else — theft, deer hits, hail, flooding, falling trees.\n\nMichigan weather makes comprehensive especially important. A lot of people drop it to save money and then get hit with an uncovered deer claim in November.\n\nFull glossary of Michigan auto insurance terms: {URLS['autoterm']}\n\nWant to make sure your coverage is right? Call {PHONE}."),
("06/22/2026","11:00","Instagram",f"Collision vs. comprehensive — do you know the difference? One covers deer hits. One doesn't.\n\nMichigan auto insurance glossary — link in bio.\n#AutoInsurance #Michigan #InsuranceTips #CarInsurance #LakeOrion"),
("06/22/2026","12:00","X",f"Collision covers hitting things. Comprehensive covers deer, hail, flooding, theft. Michigan drivers — know the difference before November. {URLS['autoterm']}"),
("06/23/2026","09:00","LinkedIn",f"Michigan's auto insurance market is genuinely more complex than most states — between no-fault PIP tiers, mini-tort rules, and the uninsured motorist landscape, there's a lot of terminology that matters.\n\nWe put together a complete Michigan auto insurance glossary: {URLS['autoterm']}\n\nThe agents at JJA have been working in Michigan insurance for 45 years. Call {PHONE}."),
("06/23/2026","12:00","X",f"Michigan auto insurance has more moving parts than most states. PIP tiers, mini-tort, no-fault rules. Know what you're buying. Full glossary: {URLS['autogl']}"),
("06/24/2026","10:00","Facebook",f"About 1 in 5 Michigan drivers is uninsured. If one of them hits you, your own collision coverage pays for the car — but without uninsured motorist (UM) coverage, your options for other damages get complicated fast.\n\nWe can walk you through whether your current limits make sense. Call {PHONE} or visit {QUOTE}."),
("06/24/2026","11:00","Instagram",f"1 in 5 Michigan drivers is uninsured. Do you have uninsured motorist coverage?\n\nLet us check your policy — link in bio or call us.\n#AutoInsurance #Michigan #UninsuredMotorist #InsuranceTips #LakeOrion"),
("06/24/2026","12:00","X",f"~20% of Michigan drivers are uninsured. Uninsured motorist coverage exists for exactly this reason. Do you have it? {PHONE} | {QUOTE}"),
("06/25/2026","09:00","LinkedIn",f"A question worth asking your insurance agent: what happens if an uninsured driver hits me?\n\nIn Michigan, about 1 in 5 drivers on the road doesn't have coverage. Uninsured motorist coverage is your backstop — but the limits matter, and most people set them at the minimum and forget about them.\n\nWe review UM limits as part of every policy review. Call {PHONE} or get started at {QUOTE}."),
("06/29/2026","10:00","Facebook",f"Michigan motorcyclists: summer's here and if you're back on the road, it's worth a quick check on your coverage.\n\nA few things most riders don't think about:\n• Lay-up policies — you may be paying for coverage you suspended\n• CPE (Carried Personal Effects) — covers your gear, not just the bike\n• Liability limits — same as auto but different risks\n\nFull terminology guide: {URLS['moto']}\n\nQuestions? Call {PHONE}."),
("06/29/2026","11:00","Instagram",f"Back on two wheels? Make sure your motorcycle insurance is keeping up.\n\nMichigan motorcycle insurance guide — link in bio.\n#MotorcycleInsurance #Michigan #Motorcycle #BikerLife #SummerRiding #LakeOrion"),
("06/29/2026","12:00","X",f"Michigan riders: summer coverage check. Lay-up policy reinstated? Gear covered under CPE? Liability limits still right? Full guide: {URLS['moto']} | {PHONE}"),
("06/30/2026","09:00","LinkedIn",f"Michigan motorcycle insurance has terminology that's specific to riders — lay-up coverage, CPE, agreed value vs. actual cash value — and most riders never fully understand their policy until they have a claim.\n\nWe put together a complete terminology guide: {URLS['moto']}\n\nIf you want your current policy reviewed, call {PHONE}."),
("06/30/2026","12:00","X",f"Do you know what a lay-up policy is? If you ride a motorcycle in Michigan you should. Quick read: {URLS['moto']}"),
("07/01/2026","10:00","Facebook",f"Summer in Michigan means boats, RVs, ATVs, and jet skis — and most people assume their home or auto policy covers those.\n\nUsually it doesn't. Or it covers them in very limited situations.\n\nWe can put together a specialty vehicle policy that actually fits how you use your equipment. Call {PHONE} or start a quote at {QUOTE}."),
("07/01/2026","11:00","Instagram",f"Boat, RV, ATV, jet ski — don't assume your home or auto policy covers them. Most don't.\n\nGet the right coverage before you hit the water. Link in bio.\n#BoatInsurance #Michigan #SummerFun #RVLife #LakeOrion #Insurance"),
("07/01/2026","12:00","X",f"Summer Michigan reminder: home and auto policies usually don't cover boats, ATVs, or RVs beyond very limited situations. Specialty vehicle policies exist for this. {QUOTE}"),
("07/06/2026","10:00","Facebook",f"We pulled together the 25 insurance questions Michigan residents ask most — and gave straight answers to all of them.\n\nFrom 'how much coverage do I actually need' to 'what happens if I let my policy lapse,' it's all in there.\n\n{URLS['q25']}\n\nStill have questions? Our agents have been answering them for 45 years. Call {PHONE}."),
("07/06/2026","11:00","Instagram",f"25 insurance questions Michigan residents ask most — answered. No jargon, no fluff.\n\nLink in bio.\n#Insurance #Michigan #InsuranceTips #FAQ #LakeOrion"),
("07/06/2026","12:00","X",f"25 insurance questions Michigan residents ask most — answered plainly. Bookmark this one: {URLS['q25']}"),
("07/07/2026","09:00","LinkedIn",f"We put together a roundup of the 25 most common insurance questions Michigan residents bring to us — and answered each one directly.\n\nUseful for clients, family members, or anyone who's ever felt confused at renewal time.\n\n{URLS['q25']}\n\nFor anything more complex, our agents are a call away: {PHONE}"),
("07/07/2026","12:00","X",f"'Does filing a claim raise my rates?' 'Do I need umbrella insurance?' 'What's the difference between ACV and replacement cost?' All answered: {URLS['q25']}"),
("07/08/2026","10:00","Facebook",f"One of the questions we get a lot: 'Should I file this claim or just pay out of pocket?'\n\nHonest answer: it depends on the amount and your claims history. Small claims can follow you for years and push up your premium more than the claim was worth.\n\nWe can help you think through it before you call your carrier. That's the value of having an independent agent. Call {PHONE}."),
("07/08/2026","11:00","Instagram",f"Should you file that claim — or just pay out of pocket? It's not always obvious.\n\nCall us before you call your carrier. We'll help you think it through.\n{PHONE}\n#InsuranceTip #Michigan #Insurance #LakeOrion"),
("07/08/2026","12:00","X",f"Before you file that insurance claim — call your independent agent first. Small claims can raise your rate more than they're worth. {PHONE} | jjainsurance.com"),
("07/09/2026","09:00","LinkedIn",f"A question agents get asked more than almost any other: 'Should I file this claim or just handle it myself?'\n\nThe honest answer is that it depends on three things:\n1. The dollar amount relative to your deductible\n2. Your current claims history with that carrier\n3. How long ago your last claim was\n\nWe walk clients through this analysis all the time — at no cost, with no pressure. Call {PHONE} before you file."),
("07/13/2026","10:00","Facebook",f"Do you know what 'replacement cost' vs. 'actual cash value' means on your homeowners policy?\n\nReplacement cost pays what it costs to rebuild. Actual cash value pays what the damaged item is worth today — accounting for depreciation.\n\nOn a roof, that difference can be $15,000.\n\nFull Michigan homeowners insurance glossary: {URLS['homegl']}\n\nNot sure what your policy says? Call {PHONE}."),
("07/13/2026","11:00","Instagram",f"Replacement cost vs. actual cash value — on a roof claim, this difference can be $15,000.\n\nKnow what your policy actually says. Link in bio.\n#HomeInsurance #Michigan #InsuranceTip #Homeowners #LakeOrion"),
("07/13/2026","12:00","X",f"Replacement cost vs. actual cash value. On a roof, that gap is often $10-20K. Most homeowners don't know which one they have. Do you? {URLS['homegl']}"),
("07/14/2026","09:00","LinkedIn",f"Most homeowners have either replacement cost (RC) or actual cash value (ACV) coverage — and most don't know which.\n\nRC pays to rebuild or replace at current prices. ACV subtracts depreciation, which on older materials can mean getting 40 cents on the dollar.\n\nFor most Michigan homeowners, RC coverage is worth the modest premium difference. Call {PHONE} or visit {QUOTE}."),
("07/14/2026","12:00","X",f"Your homeowners policy has a deductible, a coverage limit, and either RC or ACV payout terms. If you don't know all three, call your agent. {PHONE}"),
("07/15/2026","10:00","Facebook",f"Michigan homeowners: flood damage is almost never covered by a standard homeowners policy.\n\nIf your basement floods from heavy rain, a backed-up storm drain, or a creek overflowing — your homeowners policy likely doesn't pay.\n\nFlood insurance through the NFIP or private carriers is separate and worth talking about if you're in a low-lying area.\n\nQuestions? Call {PHONE} — we'll give you a straight answer."),
("07/15/2026","11:00","Instagram",f"Michigan homeowners: your home insurance almost certainly does NOT cover flood damage.\n\nFlood insurance is a separate policy — and it matters here.\n\nCall us to find out if you need it: {PHONE}\n#FloodInsurance #HomeInsurance #Michigan #Insurance #LakeOrion"),
("07/15/2026","12:00","X",f"Michigan reality: standard homeowners insurance doesn't cover flood damage. Basement flooding from heavy rain? Likely not covered. Flood insurance is a separate policy. {PHONE}"),
("07/16/2026","09:00","LinkedIn",f"A misconception that costs Michigan homeowners real money: 'My homeowners policy covers flooding.'\n\nIt doesn't. Standard homeowners policies explicitly exclude flood damage — water that enters from outside the structure, storm drains, or overflowing bodies of water.\n\nWith Michigan's weather patterns, this matters. Call {PHONE} or visit {QUOTE}."),
("07/20/2026","10:00","Facebook",f"Warning for Michigan drivers: auto insurance refund scams are still circulating.\n\nThe setup: someone calls or texts claiming you're owed a refund from your carrier. They ask for your policy number, bank info, or a small 'processing fee.' It's a scam.\n\nWe wrote a guide on how to spot and avoid these: {URLS['scam']}\n\nWhen in doubt, call your agent directly. Our number is {PHONE}."),
("07/20/2026","11:00","Instagram",f"Michigan drivers: auto insurance refund scams are still making the rounds.\n\nHow to spot them — link in bio.\n#InsuranceScam #Michigan #ConsumerProtection #AutoInsurance #LakeOrion"),
("07/20/2026","12:00","X",f"Michigan auto insurance scam still circulating: fake 'refund' calls asking for your policy number and bank info. It's fraud. Read how to spot it: {URLS['scam']}"),
("07/21/2026","09:00","LinkedIn",f"A heads-up for Michigan business owners and employees: auto insurance refund scams have been circulating for years and still catch people off guard.\n\nThe script is consistent: caller claims your insurance company owes you money and needs to verify your info. It sounds official. It's not.\n\nWe wrote a guide on the red flags: {URLS['scam']}\n\nIf you ever get a call like this about a JJA policy, hang up and call us directly at {PHONE}."),
("07/21/2026","12:00","X",f"If someone calls claiming you're owed an auto insurance refund and asks for your bank info — hang up. It's a scam. {URLS['scam']} | Your real agent: {PHONE}"),
("07/22/2026","10:00","Facebook",f"Three signs an insurance call is a scam:\n\n1. They contacted you — not the other way around\n2. They need your banking info to 'process' a refund\n3. There's urgency pressure: 'You have to claim this today'\n\nLegitimate insurance refunds don't work this way. When in doubt, hang up and call your agent directly.\n\nWe're at {PHONE} — always happy to verify anything you've received."),
("07/22/2026","11:00","Instagram",f"3 signs that insurance call is actually a scam.\n\n1 They called you\n2 They want your bank info\n3 There's pressure to act now\n\nHang up. Call your real agent.\n{PHONE}\n#InsuranceScam #Michigan #ConsumerProtection #LakeOrion"),
("07/22/2026","12:00","X",f"Red flag: they called you. Red flag: they need bank info. Red flag: act now or lose it. That's a scam, not an insurance refund. Your agent's number: {PHONE}"),
("07/27/2026","10:00","Facebook",f"45 years in Michigan insurance.\n\nJJA was founded in 1981 and we've been in Lake Orion ever since. Three decades of market shifts, no-fault reforms, carrier changes, and Michigan weather — we've seen it all.\n\nThe reason clients stay: we work for you, not for a carrier. We shop 20+ personal lines and 20+ commercial carriers to find your best rate. Every time.\n\nGet a quote at {QUOTE} or call {PHONE}."),
("07/27/2026","11:00","Instagram",f"45 years in Michigan. Lake Orion's Best of the Best 8 years running.\n\nWe shop 20+ carriers so you don't have to. Get a quote — link in bio.\n#JJAInsurance #LakeOrion #Michigan #Insurance #IndependentAgent"),
("07/27/2026","12:00","X",f"45 years in Michigan. Independent. Working for clients, not carriers. We shop 20+ personal and 20+ commercial carriers. {QUOTE} | {PHONE}"),
("07/28/2026","09:00","LinkedIn",f"What does it actually mean to work with an independent insurance agency?\n\nIt means your agent isn't tied to one carrier's products or pricing. We shop across the market — 20+ personal lines carriers and 20+ commercial — and place your coverage where it fits best.\n\nCaptive agents (State Farm, Allstate, Farmers, etc.) can only offer you their employer's products. Nothing wrong with those products — but you're seeing one option.\n\nWe've been doing this in Michigan since 1981. If you're up for renewal or want a second opinion, call {PHONE}."),
("07/28/2026","12:00","X",f"Captive agent: one carrier, one rate. Independent agent: 20+ carriers, best rate. We've been the latter in Michigan since 1981. {PHONE}"),
("07/29/2026","10:00","Facebook",f"Lake Orion Readers' Choice Best of the Best — 8 years in a row.\n\nWe don't take that lightly. It means people in our community trust us with something that matters — their home, their car, their business, their family.\n\nThank you to everyone who's voted and every client who's stuck with us. We'll keep earning it.\n\nNew to JJA? Start here: {QUOTE} or call {PHONE}."),
("07/29/2026","11:00","Instagram",f"Best of the Best — 8 years straight. Thank you, Lake Orion.\n\nNew here? Get a quote — link in bio.\n#LakeOrion #BestOfTheBest #JJAInsurance #Michigan #Community #Insurance"),
("07/29/2026","12:00","X",f"Lake Orion Readers' Choice Best of the Best — 8 consecutive years. Thank you to our community. New clients welcome: {QUOTE} | {PHONE}"),
("08/03/2026","10:00","Facebook",f"Sending a teen driver off to college or just to a new school year?\n\nAdding a teen to your auto policy is one of the biggest premium jumps most families experience. But there are ways to manage it — good student discounts, driver training credits, and getting the right vehicle on the right coverage tier.\n\nWe've been navigating this with Michigan families for 45 years. Call {PHONE} before the school year starts."),
("08/03/2026","11:00","Instagram",f"Teen driver in your house? Adding them to your policy doesn't have to wreck your budget.\n\nCall us — we'll find the right fit.\n{PHONE}\n#TeenDriver #AutoInsurance #Michigan #BackToSchool #Insurance #LakeOrion"),
("08/03/2026","12:00","X",f"Adding a teen driver to your Michigan auto policy? Good student discount, driver training credit, and right vehicle selection all matter. Call us before you add them: {PHONE}"),
("08/04/2026","09:00","LinkedIn",f"Back-to-school season is also when Michigan families discover how expensive adding a teen driver is.\n\nA few things that can help:\n• Good student discount (usually requires B average or better)\n• Driver training completion credit\n• Putting the teen on an older, safer vehicle\n• Checking whether a separate named-driver policy makes sense\n\nWe work with 20+ personal lines carriers. Call {PHONE}."),
("08/04/2026","12:00","X",f"Michigan parents: good student discount can offset a chunk of the teen driver premium increase. Ask about it before you add them to your policy. {PHONE}"),
("08/05/2026","10:00","Facebook",f"College student taking the family car? Living in the dorms without a car?\n\nYour coverage situation changes when your kid goes to school — and the answer isn't always 'add them to your policy at full rate.'\n\nCall {PHONE} and we'll sort out the right structure. It's a 10-minute conversation that can save you real money."),
("08/05/2026","11:00","Instagram",f"Kid heading to college? Your auto insurance situation just changed — maybe in your favor.\n\nCall us and we'll figure out the right coverage. {PHONE}\n#AutoInsurance #Michigan #CollegeStudent #Insurance #LakeOrion"),
("08/05/2026","12:00","X",f"Teen going to college without a car? You may be able to drop them from your policy or get a significant discount. Call before you pay the full rate: {PHONE}"),
("08/06/2026","09:00","LinkedIn",f"For Michigan business owners hiring summer help that's now heading back to school: if any of your seasonal employees drove company vehicles, make sure they're removed from your commercial auto policy before school starts.\n\nLeaving unlicensed or no-longer-employed drivers on a commercial policy is a liability exposure most carriers won't cover if there's a claim.\n\nQuestions about your commercial auto setup? Call {PHONE}."),
("08/10/2026","10:00","Facebook",f"Quick question: if something happened to you tomorrow, would your family be financially okay?\n\nLife insurance is the answer to that question — but most people either don't have enough of it, or they're paying too much for the wrong kind.\n\nTerm life is straightforward and affordable. Whole life has its place but it's not the right fit for everyone.\n\nWe can run through the options with you in one conversation. Call {PHONE} or start at {QUOTE}."),
("08/10/2026","11:00","Instagram",f"Would your family be financially okay if something happened to you? Life insurance is the answer — but the right kind matters.\n\nLet's talk it through. Link in bio or call {PHONE}.\n#LifeInsurance #Michigan #Insurance #Family #Protection #LakeOrion"),
("08/10/2026","12:00","X",f"Term life insurance for a healthy 40-year-old in Michigan is more affordable than most people think. The longer you wait, the more it costs. {PHONE} | {QUOTE}"),
("08/11/2026","09:00","LinkedIn",f"A conversation worth having: does your business have key person life insurance?\n\nIf your business depends on one or two people — owners, partners, rainmakers — key person coverage protects the company if that person dies unexpectedly. It can fund a buyout, keep operations running while you find a replacement, or satisfy lender requirements.\n\nMost small business owners know they need it. Most haven't gotten around to setting it up.\n\nCall {PHONE} and we'll put together a quote."),
("08/11/2026","12:00","X",f"Key person life insurance: if your business depends on one or two people and one of them dies, what happens? This is what protects the company. {PHONE}"),
("08/12/2026","10:00","Facebook",f"A rule of thumb: most financial advisors say you need 10-12x your annual income in life insurance coverage.\n\nIf you're carrying a $500K policy and making $100K a year, you're likely underinsured.\n\nWe're not financial advisors — we'll say that plainly. But we can show you what the right coverage level costs so you can make an informed decision.\n\nCall {PHONE} or visit {QUOTE}."),
("08/12/2026","11:00","Instagram",f"Life insurance rule of thumb: 10-12x your annual income in coverage. Most people fall short.\n\nLet's find out where you stand. Link in bio.\n#LifeInsurance #Michigan #Insurance #FinancialTips #LakeOrion"),
("08/12/2026","12:00","X",f"You need roughly 10-12x your annual income in life insurance. Quick math: are you there? If not, it's worth a conversation. {PHONE} | {QUOTE}"),
("08/13/2026","09:00","LinkedIn",f"Life insurance is one of those products people buy and then forget about — which is a problem when your income, debt, and family situation have all changed since you bought it.\n\nHad kids? Got a mortgage? Income went up? Business grew? Your coverage probably needs to be revisited.\n\nWe do policy reviews at no cost. Call {PHONE} and we'll tell you honestly whether what you have is still right."),
("08/17/2026","10:00","Facebook",f"What's the difference between an independent agent and a captive agent?\n\nCaptive agents (State Farm, Allstate, Farmers) work for one company. They can only quote you that company's products.\n\nIndependent agents like JJA work for you. We shop 20+ personal lines carriers and 20+ commercial carriers to find the best fit for your specific situation.\n\nSame coverage, better rates — because we have options.\n\nGet a quote: {QUOTE} | Call: {PHONE}"),
("08/17/2026","11:00","Instagram",f"Captive agent = one carrier's rates. Independent agent = 20+ carriers, best rate.\n\nJJA has been independent in Michigan since 1981. Get a quote — link in bio.\n#IndependentAgent #Insurance #Michigan #LakeOrion #BestRate"),
("08/17/2026","12:00","X",f"Captive agent shows you one price. Independent agent shows you the market. We've been the latter in Michigan since 1981. {QUOTE}"),
("08/18/2026","09:00","LinkedIn",f"End-of-summer is a good time to do a quick insurance audit before Q4 gets busy.\n\nThings worth checking:\n• Have your business revenues changed significantly?\n• Added vehicles to your fleet?\n• Major home improvement that increased your home's value?\n• Life events — marriage, kids, divorce — that change coverage needs?\n\nPolicy reviews are free. We do them all day. Call {PHONE}."),
("08/18/2026","12:00","X",f"End of summer checklist: Did your income, family, home, or business change this year? Your insurance may need to catch up. Free review: {PHONE}"),
("08/19/2026","10:00","Facebook",f"If your insurance company drops you — whether that's after a claim, a credit change, or a carrier pulling out of the market — you have options.\n\nCarriers drop clients more often than people realize, especially in high-claim areas. But being non-renewed doesn't mean you can't get good coverage.\n\nWe work with 20+ personal and 20+ commercial carriers. If you've been dropped or are worried about it, call {PHONE}. We'll find a solution."),
("08/19/2026","11:00","Instagram",f"Got a non-renewal notice from your insurance company? Don't panic — you have options.\n\nCall us and we'll find you coverage. {PHONE}\n#Insurance #Michigan #NonRenewal #Insurance #LakeOrion"),
("08/19/2026","12:00","X",f"Getting non-renewed by your Michigan insurer? We work with 20+ personal and 20+ commercial carriers. There are options. Call {PHONE}."),
("08/20/2026","09:00","LinkedIn",f"Carrier non-renewals are up across Michigan — particularly for homeowners in areas with high storm or water claims.\n\nIf a client, colleague, or family member gets a non-renewal notice, the clock is ticking (typically 30-60 days). The best time to start shopping is immediately.\n\nWe work with 20+ personal lines carriers and can usually find solid options even for high-risk properties.\n\nReach out at {PHONE} — we'll give an honest assessment of what's available and what it'll cost."),
]

# Platform name → Buffer service mapping
PLATFORM_SERVICE = {
    "Facebook": "facebook",
    "LinkedIn":  "linkedin",
    "Instagram": "instagram",
    "X":         "twitter",
}

def graphql(query, variables, api_key):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()}

def get_channels(api_key):
    q = """
    query GetChannels($input: ChannelsInput!) {
      channels(input: $input) {
        id name service
      }
    }
    """
    result = graphql(q, {"input": {"organizationId": ORG_ID}}, api_key)
    if "error" in result:
        print(f"  ERROR fetching channels: {result['error']}")
        return []
    return result.get("data", {}).get("channels", [])

def to_iso(date_str, time_str):
    """Convert MM/DD/YYYY HH:MM + EDT offset to ISO 8601."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
    tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    return dt.replace(tzinfo=tz).isoformat()

def create_post(api_key, channel_id, text, scheduled_at, platform):
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        __typename
        ... on PostActionSuccess {
          post { id }
        }
        ... on InvalidInputError { message }
        ... on LimitReachedError { message }
        ... on UnauthorizedError { message }
        ... on UnexpectedError   { message }
        ... on NotFoundError     { message }
        ... on RestProxyError    { message }
      }
    }
    """
    # Instagram requires images — save as drafts so Joseph can add
    # a photo to each one in Buffer before scheduling.
    if platform == "Instagram":
        inp = {
            "channelId": channel_id,
            "text": text,
            "mode": "addToQueue",
            "schedulingType": "automatic",
            "assets": [],
            "saveToDraft": True,
        }
    elif platform == "Facebook":
        inp = {
            "channelId": channel_id,
            "text": text,
            "dueAt": scheduled_at,
            "mode": "customScheduled",
            "schedulingType": "automatic",
            "assets": [{"image": {"url": pick_image(text)}}],
            "metadata": {"facebook": {"type": "post"}},
        }
    else:  # LinkedIn, X — no type metadata needed
        inp = {
            "channelId": channel_id,
            "text": text,
            "dueAt": scheduled_at,
            "mode": "customScheduled",
            "schedulingType": "automatic",
            "assets": [{"image": {"url": pick_image(text)}}],
        }
    variables = {"input": inp}
    return graphql(mutation, variables, api_key)

def main():
    print("\n" + "="*60)
    print("  JJA Insurance — Buffer Post Scheduler")
    print("="*60)
    print(f"\nReady to schedule {len(POSTS)} posts across 4 platforms.")

    # Use the BUFFER_API_KEY environment variable if set, otherwise prompt.
    # (Never hard-code the key here: this file lives in C:\Website, which deploys
    #  wholesale to the public site via `wrangler deploy`.)
    api_key = os.environ.get("BUFFER_API_KEY", "").strip()
    if api_key:
        print("Using Buffer API key from the BUFFER_API_KEY environment variable.\n")
    else:
        print("Tip: set a BUFFER_API_KEY environment variable to skip this prompt next time.\n")
        api_key = input("Paste your Buffer API key here: ").strip()

    if not api_key:
        print("No key entered. Exiting.")
        sys.exit(1)

    if not api_key.isascii() or " " in api_key:
        print("\nThat doesn't look like just an API key — it contains spaces or special")
        print("characters, which usually means extra text got pasted in by accident.")
        print("Paste ONLY your Buffer API key (or set the BUFFER_API_KEY variable). Exiting.")
        sys.exit(1)

    print("\nFetching your connected channels...")
    channels = get_channels(api_key)

    if not channels:
        print("Could not retrieve channels. Check your API key and try again.")
        sys.exit(1)

    print(f"Found {len(channels)} channels:")
    for ch in channels:
        print(f"  {ch['service']:12} | {ch['name']:30} | ID: {ch['id']}")

    # Map service name → channel ID
    channel_map = {}
    for ch in channels:
        svc = ch["service"].lower()
        if svc == "facebook":    channel_map["Facebook"]  = ch["id"]
        elif svc == "linkedin":  channel_map["LinkedIn"]  = ch["id"]
        elif svc == "instagram": channel_map["Instagram"] = ch["id"]
        elif svc in ("twitter", "x"): channel_map["X"]   = ch["id"]

    print(f"\nChannel map: {channel_map}")

    missing = [p for p in ["Facebook","LinkedIn","Instagram","X"] if p not in channel_map]
    if missing:
        print(f"\nWARNING: No channel found for: {missing}")
        print("Posts for those platforms will be skipped.")

    only_platform = input("\nOnly schedule one platform? (leave blank for all, or type: Facebook/LinkedIn/Instagram/X): ").strip()

    print(f"\nStarting to schedule {len(POSTS)} posts...\n")
    ok = 0
    skipped = 0
    errors = 0

    now = datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))

    for i, (date, time_str, platform, text) in enumerate(POSTS, 1):
        if only_platform and platform.lower() != only_platform.lower():
            skipped += 1
            continue

        # Instagram is scheduled separately (with branded images) by schedule_instagram.py.
        # Skip it here so it never posts image-less and never double-posts.
        if platform == "Instagram":
            print(f"  [{i:3}/{len(POSTS)}] SKIP  {date} {time_str} Instagram (run schedule_instagram.py)")
            skipped += 1
            continue

        channel_id = channel_map.get(platform)
        if not channel_id:
            print(f"  [{i:3}/{len(POSTS)}] SKIP  {date} {time_str} {platform} (no channel)")
            skipped += 1
            continue

        # Skip posts already in the past
        dt = datetime.strptime(f"{date} {time_str}", "%m/%d/%Y %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=TIMEZONE_OFFSET)))
        if dt <= now:
            print(f"  [{i:3}/{len(POSTS)}] SKIP  {date} {time_str} {platform} (past)")
            skipped += 1
            continue

        scheduled_at = to_iso(date, time_str)
        result = create_post(api_key, channel_id, text, scheduled_at, platform)

        gql_errors = result.get("errors")
        api_error  = result.get("error")
        cp = (result.get("data") or {}).get("createPost") or {}
        typename   = cp.get("__typename", "")
        if api_error or gql_errors:
            msg = api_error or gql_errors[0].get("message", "unknown")
            print(f"  [{i:3}/{len(POSTS)}] ERROR {date} {time_str} {platform}: {str(msg)[:80]}")
            errors += 1
        elif typename == "PostActionSuccess":
            post = cp.get("post") or {}
            print(f"  [{i:3}/{len(POSTS)}] OK    {date} {time_str} {platform} → {post.get('id','?')}")
            ok += 1
        elif typename:
            msg = cp.get("message", typename)
            print(f"  [{i:3}/{len(POSTS)}] ERROR {date} {time_str} {platform}: {msg}")
            errors += 1
        else:
            print(f"  [{i:3}/{len(POSTS)}] OK?   {date} {time_str} {platform} (no confirmation)")
            ok += 1

        # Respect Buffer's write rate limit (~100 per 15 min = ~1 per 9 sec).
        # 2 sec was too aggressive and triggered "Too many requests" errors.
        time.sleep(10)

    print(f"\n{'='*60}")
    print(f"  Done! Scheduled: {ok} | Skipped: {skipped} | Errors: {errors}")
    print(f"{'='*60}")
    print("\nView your scheduled posts at: https://publish.buffer.com")

if __name__ == "__main__":
    main()
