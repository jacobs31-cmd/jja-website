# JJA Website — Growth Roadmap (lead generation)

**Purpose:** turn the site from a traffic/education asset into a lead-generation engine.
Prioritized by *revenue impact* (leads → quotes → policies), not vanity traffic.
Created June 2026. Companion to `PROJECT-HANDOFF.md` (the technical source of truth).

Status keys: ☐ not started · ◐ in progress · ☑ done

---

## Now → Next → Later (at a glance)

- **DONE & LIVE (verified 2026-06-12):** Initiative 1 (45 product pages), 1.5 (113 OG cards),
  3 (20 city pages), 4 (10 intent posts incl. the 5 cost/switch/trigger ones), 5 (GA4
  `generate_lead`). Most "pending deploy" notes below are stale — this is all deployed.
- **ALSO DONE 2026-06-12:** Initiative 2 — Google Business Profile built out; on-site reviews
  page, schema, and 4.9/808 badge live. Ongoing: keep the systematic review-ask process running.
- **NOW:** deploy the staged changes (`python build.py` + `wrangler deploy`) — 3 new cost posts,
  homepage badge, fixed intent-post links. Then GoDaddy 301s (Tier-1/2) + DNS cleanup (§9) —
  steps in `GROWTH-NEXT-STEPS.md`. (No town `.com`s to redirect — confirmed none owned.)
- **LATER:** Git-based deploys (get off Drive-synced editing); local+product combos; stagger
  future blog posts ~weekly.

---

## Initiative 1 — Build real pages for high-value products we already advertise ☐
**Why:** The homepage lists Cannabis, Restaurant, Contractors, Professional Liability,
Collector Car, Pet, Bonds, Builders Risk — but most are just list items with no dedicated
page. Nothing to rank in Google, nothing to convert on. Commercial lines carry bigger
premiums and commissions, so these are worth more than another personal-lines glossary.

Priority order (highest-value / lowest-competition first):
- ☑ **Michigan cannabis / dispensary insurance** — built `/business/cannabis-insurance/` (June 2026)
- ☑ Michigan restaurant insurance — built `/business/restaurant-insurance/` (June 2026)
- ☑ Michigan contractor insurance — built `/business/contractor-insurance/`; links to/from the
  GL-for-contractors blog (June 2026)
- ☑ Michigan professional liability (E&O) — built `/business/professional-liability-insurance/` (June 2026)
- ☑ **Commercial core (8):** general-liability, commercial-property, commercial-auto,
  business-owners-policy (BOP), cyber-liability, commercial-umbrella, builders-risk,
  surety-bonds — built `2026-06-12`.
- ☑ **Personal lines (9):** umbrella, flood, boat, rv, motorcycle, renters, condo,
  collector-car, pet — built `2026-06-12`.
- ☑ **Niche pages (11)** built `2026-06-12`: commercial — fitness/gym, garage, property
  management, condo association, church, business interruption, special event; personal —
  ATV, mobile-home, specialty dwelling, high-net-worth. Every advertised product now has a
  dedicated page (36 product pages total). NOTE: ATV and mobile-home reuse on-brand stand-in
  hero photos — swap for true ATV / manufactured-home images when available.

- ☑ **Industry pages (9)** built `2026-06-12` from Joseph's list: trucking, manufacturing,
  counselor/therapist, consulting, water well, liquor liability, home health, educational,
  technology. Skipped: urgent care (per Joseph), garage keepers (covered by existing garage
  page). Each added to the business product grid + a NEW definition block, sitemap, llms, OG.
  NOTE: water-well uses a clean-water stand-in hero; swap for a drilling/well image when handy.
  **45 product pages total.**

> 25 product pages now live in `C:\Website` (8 earlier + 17 on 2026-06-12). All built with
> the **`gen_product_pages.py`** generator (config-driven, identical template + Breadcrumb/
> FAQPage/Service schema), wired into the overview pages ("Full details" links), homepage
> chips, `sitemap.xml`, `llms.txt`, and each given a branded OG card. Staged, pending deploy.

Each page must include: dedicated URL, unique title/meta/OG/canonical, InsuranceAgency +
FAQPage schema, BreadcrumbList, quote CTA, internal links to/from related pages, a sitemap
entry, and an `llms.txt` update. Model on `business/workers-compensation/` (cleanest
commercial product template).

## Initiative 1.5 — OG images (was on the SEO punch list) ☑
Built branded 1200×630 JPG OG cards for all ~60 pages/posts via `make_og_images.py`
(photo cards from each hero + navy branded cards for city/legal/infographic pages).
Rewired `og:image`/`twitter:image` sitewide; patched `build.py` so blog rebuilds keep the
cards. Replaces the generic `og-default.jpg` and the broken `.svg`/`.avif` blog OG images.
Staged, pending deploy.

## Initiative 2 — Reviews + Google Business Profile ☑ (on-site + GBP built out 2026-06-12; keep review-asks ongoing)
**Why:** For a local agency, the Google map pack drives more calls than the website. Likely
the single highest ROI on this list — and most of it is off the website.
- ☐ Systematic review-ask process for every happy client (use existing Google review QR/link)
- ☐ Fully build out the Google Business Profile: categories, services, products, photos,
  weekly posts, Q&A
- ☐ Keep visible rating and schema `aggregateRating` identical (handoff §8)
- ☑ Surface review count / recency on site — homepage hero + reviews-section badge now show
  "4.9 stars from 808 Google reviews" (2026-06-12; kept identical to schema aggregateRating)

## Initiative 3 — Expand local landing pages ◐
**Why:** Local intent converts. Was 10 city pages; added 10 on 2026-06-12 → 20 total.
- ☑ **Added 10 (2026-06-12):** Rochester Hills, Auburn Hills, Waterford, Orion Township,
  Troy, Bloomfield, Pontiac, Holly, Shelby Township, Washington Township. Each built from
  the Clarkston template via `gen_cities.py` with verified local detail (ZIPs, county,
  neighboring townships, lakes, landmarks), InsuranceAgency + FAQPage schema, OG card,
  sitemap + llms. Staged, pending deploy.
- ☐ 301-redirect any owned town `.com` domains to the matching new landing page (check
  GoDaddy for troy/rochesterhills/etc. domains).
- ☐ Optional later: local + product combos ("Troy business insurance"), Tier-3 towns.
- Generator: `gen_cities.py` (config-driven; add a city + run generate/wire to extend).

## Initiative 4 — Shift blog from education to intent ☐
**Why:** Current blog is mostly top-of-funnel glossaries. Weight new posts toward content
where the next click is naturally "get a quote." Publish staggered (~weekly) so we learn
from each post and get multiple social waves.
- ☐ Cost pages: "Business insurance cost in Michigan", "Average workers' comp cost in
  Michigan", "Cannabis insurance cost"
- ☐ Switch / trigger pages: "How to switch insurance agents in Michigan", "Got a non-renewal
  notice — what to do", "Buying a home in Michigan: insurance checklist", "Starting a
  Michigan business: what coverage you need"
- Process: markdown in `content/blog/`, `python build.py`, sitemap, deploy (handoff §6)

## Initiative 4 — Shift blog from education to intent ◐
- ☑ **5 intent posts published 2026-06-12:** "How Much Does Business Insurance Cost in
  Michigan?", "How to Switch Insurance Agents in Michigan", "Got a Non-Renewal Notice in
  Michigan?", "Buying a Home in Michigan: Insurance Checklist", "Starting a Business in
  Michigan: The Insurance You Actually Need." Cost + switch + trigger angles that convert,
  each cross-linked to the relevant product pages. Built via markdown + `build.py`, OG
  cards + sitemap done. Staged, pending deploy.
- ☑ **Built 2026-06-12 (markdown staged — run `python build.py` + deploy):** "How Much Does
  Workers' Comp Cost in Michigan?", "How Much Does Cannabis Insurance Cost in Michigan?",
  "Adding a Teen Driver in Michigan: What It Costs and How to Save." Researched figures,
  cross-linked to product pages (with correct `../../business|personal/` paths).
- ☐ Further ideas: more switch/trigger angles; stagger future posts ~weekly.
- Cadence note: consider staggering future posts ~weekly (learn from Search Console
  between posts) rather than publishing all at once.

## Initiative 5 — Measurement & conversion ◐ (GA4 done; one Ads import left)
- ☑ GA4 `generate_lead` conversion event live on quote + contact forms (2026-06-12),
  confirmed firing in Realtime. Now a **Key Event** and **imported into Google Ads**
  ("Submit lead form", Primary).
- ☑ GA4 `phone_call` event on `tel:` clicks — **LIVE on site, verified 2026-06-15**
  (`site.v2.js?v=20260614`); marked a **Key Event** in GA4.
- ☐ **Import `phone_call` into Google Ads** (set Primary) — the remaining pre-spend gate.
  Not available in the Ads UI yet (wizard, classic import, and Data Manager all checked
  2026-06-15); likely needs ~24–48h to propagate now that it's a Key Event. Retry later;
  don't create a manual conversion. See `PROJECT-HANDOFF.md` §12.
**Why:** Without attribution we're guessing which pages produce leads.
- ☐ GA4: fire a tracked event on quote-form submit, tied to landing page
- ☐ Mine Search Console for queries already near page 1 → prioritize those pages/posts
- ☐ Quote-form friction review; prominent click-to-call on mobile; consider a lead magnet
  (e.g., "Michigan insurance review checklist")

---

## Decision log
- June 2026: Roadmap created from site review. Agreed to start with Initiative 1
  (high-value commercial product pages), cannabis page first pending confirmation.
