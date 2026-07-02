# JJA Growth — Next Steps (off-site action items)

Companion to `GROWTH-ROADMAP.md`. Covers the work that can't be done in the site files:
the Google Business Profile build-out (Initiative 2) and the GoDaddy domain/DNS items (§9).
Created 2026-06-12.

---

## 1. Google Business Profile (Initiative 2 — highest ROI on the roadmap)

For a local agency, the Google map pack drives more calls than the website. The on-site
pieces are done (reviews page, schema, 4.9/808 badge). The rest is in the GBP dashboard.

> **STATUS 2026-06-12: GBP build-out completed by Joseph.** The checklist below is kept as a
> reference / maintenance list. The one part that's never "done" is the ongoing review-ask
> process (Part B) — keep that running on every happy client.

**A. Get the profile complete and consistent**
- [ ] Claim/verify ownership of the J. Jacobs & Associates profile.
- [ ] **NAP must match the site EXACTLY:** J. Jacobs & Associates Insurance · 4301 S. Baldwin Rd, Lake Orion, MI 48359 · (248) 693-6455 · jjainsurance.com. (Mismatches hurt ranking — handoff §8.)
- [ ] **Primary category:** Insurance agency. **Secondary** as applicable: Auto insurance agency, Home insurance agency, Life insurance agency, Commercial agent.
- [ ] Hours: Mon–Fri 9:00 AM – 5:00 PM.
- [ ] **Services:** mirror your product pages — Auto, Home, Life, Umbrella, Renters/Condo, Boat/RV/Motorcycle, Business/Commercial, Workers' Comp, General Liability, BOP, Commercial Auto, Cannabis, etc.
- [ ] **Description:** plain-language, Michigan-specific — independent agency since 1981, 50+ carriers, Lake Orion Review "Best of the Best" 8 years running (2018–2025).
- [ ] **Photos:** logo, storefront/exterior, office interior, team. (Real photos beat stock for conversion.)

**B. Systematic review-ask process** (this is the engine — most agencies skip it)
- [ ] Use the existing Google review link on every ask: `https://g.page/r/CZiBtTy1adZDEAE/review`
- [ ] Put the existing review QR code (`JJA-Google-Review-QR-Code.png`) at the front desk, on quote follow-ups, and in email signatures.
- [ ] Ask **every** happy client right after a bind, a claim handled well, or a save at renewal — a quick text/email with the link converts best.
- [ ] Respond to **every** review (thank positives by name; answer negatives calmly and factually).
- [ ] As the real Google count grows past 808, bump the number in the site (homepage hero + reviews section + schema `aggregateRating`) so all three stay identical.

**C. Ongoing GBP activity**
- [ ] Weekly Google Post (a tip, an offer, or a link to a blog post / product page).
- [ ] Seed the Q&A with 5–8 common questions and answer them yourself.

---

## 2. GoDaddy 301 redirects (consolidate domains → one site)

**How (per domain):** GoDaddy → Products → **Manage** the domain → **Forwarding** → **Add** →
enter the destination URL → choose **Permanent (301)** → **Forward only** (NEVER "Forward
with masking"). Masking splits SEO authority — don't use it.

**Tier 1 — forward to the homepage** `https://www.jjainsurance.com/`:
- [ ] jjacobsandassociates.com
- [ ] jjains.com
- [ ] jjacobsinsurance.com
- [ ] jacobsfamilyinsurance.com
- [ ] michiganinsuranceagency.com
- [ ] independentinsurancenearme.com
- [ ] independentinsuranceagencynearme.com
- [ ] michiganinsurancenearme.com

**Tier 2 — forward to the matching landing page:**
- [ ] clarkstoninsurancenearme.com → `https://www.jjainsurance.com/clarkston-insurance/`
- [ ] fentoninsurancenearme.com → `https://www.jjainsurance.com/fenton-insurance/`

**New-city domains: none to redirect.** Confirmed 2026-06-12 — Joseph owns no additional
`.com` domains beyond the Tier-1/2 list above, so there are no town `.com`s to point at the
new city pages. The Tier-1/2 redirects above are the complete list.

**Leave alone:** personal domains (thewhiskeylady.com, emyliajacobs.com, juliejacobs.net,
brennanjacobs.net, josephjacobs.net). **Drop at renewal:** insurecryptosnow.com.

---

## 3. GoDaddy DNS cleanup (safe tidying — §9)

In the `jjainsurance.com` DNS zone:
- [ ] Remove the **"Template Applied: Crypto Wallet"** template (drops two `ENS1 0x...` TXT records).
- [ ] Delete the **`TXT @ NETORGFT12116311.onmicrosoft.com`** record (unused Microsoft 365 leftover).
- [ ] **Fix SPF** — change:
  `v=spf1 include:mailgun.org include:_spf.google.com include:secureserver.net include:mailgun.org1 ~all`
  to:
  `v=spf1 include:mailgun.org include:_spf.google.com ~all`
  (removes the typo `mailgun.org1` and the unused `secureserver.net`; **keep Mailgun** — still in use).
- [ ] **After the WordPress cutover only:** delete stale cPanel/WordPress CNAMEs — `autoconfig`,
  `autoconfig.admin`, `autodiscover`, `autodiscover.admin`, `cpanel`, `webdisk`, `webdisk.admin`,
  `webmail`, `whm`, `ftp`, `email`, `www.admin`. Keep `fuse` (→ mailgun.org) unless Mailgun is also dropped.

**DO NOT TOUCH:** Google Workspace MX records, the Search Console verification TXT, Google
DKIM, DMARC (`v=DMARC1;p=quarantine;pct=100`), and the Apple domain-verification TXT.

---

## 4. ✅ FIXED 2026-06-12 — broken internal links in the intent posts

The 5 intent posts published 2026-06-12 (`how-much-does-business-insurance-cost-in-michigan`,
`how-to-switch-insurance-agents-in-michigan`, `got-a-non-renewal-notice-michigan`,
`buying-a-home-in-michigan-insurance-checklist`, `starting-a-business-in-michigan-insurance`)
link to product pages with `../<slug>/`, which from `/blog/<slug>/` resolves to
`/blog/<slug>/` — a **broken** path. They should be `../../business/<slug>/` or
`../../personal/<slug>/`. (The 3 new cost posts use the correct paths.)

**Done:** only two posts actually had the broken pattern — `how-much-does-business-insurance-cost-in-michigan`
and `starting-a-business-in-michigan-insurance`. All their product-page links were corrected to
`../../business/<slug>/` (and the "See all commercial coverages" link → `../../business/`). The
other intent posts were already fine. Re-run `python build.py` + deploy to publish the fix.

---

## Deploy reminder
The 3 new blog posts are staged as markdown + wired into `build.py`/`sitemap.xml`. To publish:
`python build.py` then `npx wrangler deploy` from `C:\Website` (real Windows terminal). The
homepage badge + roadmap updates ride along on that same site deploy.
