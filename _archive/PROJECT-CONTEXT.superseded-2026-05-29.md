# J. Jacobs & Associates Insurance — Website Project Context

This file captures everything established about this site so any new Cowork
conversation can pick up where we left off. Paste the body of this file into
the **Project Instructions** field when creating a Cowork project, or just
reference it ("read PROJECT-CONTEXT.md") at the start of any new chat.

---

## About the business

- **Agency**: J. Jacobs & Associates Insurance
- **Owner**: Joseph Jacobs (jacobs31@jjainsurance.com)
- **Office**: 4301 S. Baldwin Rd, Lake Orion, Michigan 48359
- **Phone**: (248) 693-6455
- **Email**: Support@jjainsurance.com
- **Founded**: 1981 (family-owned; Jeff Jacobs founded, Joseph took over in 2014)
- **Type**: 100% independent insurance agency
- **Carriers**: 50+ commercial, 15+ personal lines (Auto-Owners, Citizens, Cincinnati, Progressive, Frankenmuth, Foremost, Liberty Mutual, Wolverine Mutual, Michigan Millers, AAA of Michigan, The Hartford, Hastings, Hagerty, American Modern, and more)
- **Service area**: All of Michigan
- **Awards**: Lake Orion Review Readers' Choice "Best of the Best" — 1st Place — 8 consecutive years (2018-2025)
- **Existing legacy site** (for reference): https://www.jjainsurance.com (WordPress, built by Advisor Evolved — do NOT cancel until new site confirmed live on jjainsurance.com for at least 1 week)

## Tech stack

- **Site type**: Pure static HTML/CSS/JS (no framework, no WordPress)
- **Local working folder**: `C:\Website`
- **Hosting**: Cloudflare Pages
- **Current deploy method**: Drag-and-drop folder uploads (to be migrated to Git+GitHub later — see SETUP-GUIDE.md)
- **Domain registrar**: GoDaddy (registration stays at GoDaddy)
- **DNS**: Cloudflare — nameservers flipped to `darwin.ns.cloudflare.com` / `uma.ns.cloudflare.com` on 2026-05-17. DNS is now managed in Cloudflare dashboard, not GoDaddy. Domain pending activation/propagation as of 2026-05-17.
- **Email hosting**: Google Workspace (independent of website hosting)
- **Forms**: Formspree (free tier), form ID `xnjweggp` → emails leads to Support@jjainsurance.com. Formshield (Formspree's ML spam filter) is intentionally **OFF** — see Quote form section below for why.
- **Analytics**: Google Analytics 4. Measurement ID `G-QRLBD79S35`. Loaded automatically via `assets/js/site.v2.js` on every page (no per-page snippet needed). Joseph also has a Google Tag Manager container `GT-M3LBGVP` provisioned but **not yet installed** — Tag Manager is a separate tool that can layer on top of GA4 later if needed.
- **AMS**: Hawksoft
- **Rater**: PL Rater (Vertafore)
- **Lead integration**: Currently manual — form emails → staff types into Hawksoft + PL Rater. Future option: Canopy Connect for direct PL Rater bridging.
- **AL3 generator**: In progress. Goal is a Cloudflare Worker that receives the quote form submission, generates an ACORD AL3 file (auto + home), and emails it to Support@jjainsurance.com via **Resend** (resend.com) so staff can import directly into PL Rater. Sample AL3 file is at `C:\Users\jacob\AppData\Roaming\Claude\...\uploads\PL-370ed2a4.al3` — use this as the format reference. Resend account being set up 2026-05-17; domain verification easy since DNS is on Cloudflare.

## Brand & design

- **Colors**: Navy (`#14365e`) and grays. NO gold/yellow accents.
- **CTAs**: Use navy blue (`#1c4e8c`) — not gold
- **Typography**: Inter from Google Fonts
- **Style**: Clean, modern, professional. Lots of whitespace, soft shadows. No emoji on the site itself (use sparingly elsewhere).
- **Tone**: Trustworthy, plain-language, Michigan-specific. We educate clients, not sell to them.
- **Logo file**: `assets/img/logo.jpeg`

## Site structure

Top-level pages:
- `index.html` — Home (with hero, awards, products, reviews, FAQ)
- `about/` — About Us (with team office image)
- `team/` — Team page (currently 15 members, removed Aimee VeCasey, Jonah Webster, Melanie Cappell)
- `carriers/` — Carriers list
- `reviews/` — Client reviews + Google review CTA
- `personal/` — Personal Insurance overview with all 16 products + scroll-to-definition
- `personal/auto-insurance/` — Dedicated Auto Insurance page
- `personal/home-insurance/` — Dedicated Home Insurance page
- `personal/life-insurance/` — Dedicated Life Insurance page
- `business/` — Commercial Insurance overview with all 20 products + scroll-to-definition
- `business/workers-compensation/` — Dedicated Workers Comp page
- `service/` — Customer Service Center
- `billing-claims/` — Billing & Claims center
- `blog/` — Blog index + 10 individual posts
- `quotes/` — Quote request form (PL Rater fields, with partial-lead capture — see Quote form section below)
- `contact/` — Contact form
- `faq/` — FAQ page
- `privacy-policy/`, `accessibility/`, `404.html`

City landing pages (top-level, SEO targets for surrounding Michigan towns):
- `clarkston-insurance/`, `fenton-insurance/`, `ortonville-insurance/`, `oxford-insurance/`,
  `grand-blanc-insurance/`, `goodrich-insurance/`, `lapeer-insurance/`, `rochester-insurance/`,
  `oakland-township-insurance/`, `white-lake-insurance/`

Legacy URL preservation (Cloudflare-served shims for the old WordPress paths):
- `wp-content/uploads/sites/38/2026/03/` — Bryan-sig-file-2.jpg, Rons-email-sig.jpg, image-4.jpg, JJA-Google-Review-QR-Code.png
- `wp-content/uploads/sites/38/2026/04/` — Best-of-the-Best-all-7.png
- These are duplicate copies of files that also live in `assets/img/`. They exist solely so URLs printed in email signatures, on QR-code materials, etc. still resolve after the DNS cutover. Do NOT delete these copies or rename them. The picture-name → URL mapping is in `URL's.docx` at the site root.

Build script: `build.py` reads markdown files from `content/blog/` and generates blog HTML.

## Important design conventions

- **Hero gradient**: `.hero` (homepage two-column) and `.page-hero` (inner pages single-column) both use the navy-tinted gradient with radial accents
- **Cards**: All card elements (`.card`, `.team-card`, `.product-card`, `.review-card`, `.award-card`, `.step`, `.faq-item`, `.blog-card`, `.product-definition`) have a default soft shadow + slight off-white bg (`#fbfcfd`) so they stand out on white sections
- **Nav dropdowns**: Use native HTML `<details>`/`<summary>` (not JS) — this is intentional to avoid cache/JS issues. The submenus toggle via browser behavior, not a script.
- **Mobile**: Fully responsive. Mobile menu uses hamburger.
- **Cache-busting**: All CSS/JS references include `?v=YYYYMMDD#` query strings. Bump this version when updating styles or scripts.
- **Relative paths**: All asset/link URLs use relative paths (`./assets/...`, `../assets/...`) — never absolute (`/assets/...`) — so the site works both locally and on Cloudflare.

## Quote form & partial-lead capture

The `/quotes/` page posts to Formspree (form ID `xnjweggp`). In addition to normal full submissions, `assets/js/site.v2.js` captures **partial leads** — background POSTs that fire once the user has filled out the contact basics but hasn't clicked Submit. This is meant to recover prospects who abandon mid-form.

Partial-lead triggers (all of them require the same validation gate to pass first):
1. **15-second idle** — once contact fields are valid and the user stops typing
2. **`pagehide` / `beforeunload`** — user closes the tab or navigates away
3. **`visibilitychange` to hidden** — user backgrounds the tab (mostly mobile)

Validation gate: the partial lead only fires when all five of `first_name`, `last_name`, `email` (valid format), `phone` (10+ digits), `zip` (exactly 5 digits) are filled. This is a deliberate floor so we don't email half-finished junk.

The partial lead is sent as a Formspree POST with `_subject` of `[PARTIAL] Quote Lead — jjainsurance.com` and a `partial_lead` field indicating which trigger fired. The user-facing autoresponse is stripped from partial leads.

A debug helper is left in the script: open DevTools console on `/quotes/` and type `window.testPartialLead()` to force-fire the trigger without waiting.

**Formshield is OFF on Formspree.** We turned it off after diagnosing on 2026-05-16 that the ML spam filter was silently moving partial submissions (and even some full ones) to the spam folder, so no emails were being delivered. If partial leads ever stop arriving in your inbox again, the first thing to check is whether Formshield got re-enabled in the Formspree dashboard. Settings → Spam Protection → Formshield should be the gray/off toggle.

### Quote form cross-sells

The quote form supports per-product cross-sell prompts (e.g. "Would you like an umbrella quote too?" inside the Auto section). The behavior is driven by any `<select>` element with a `data-cross-sell="line_xxx"` attribute, where `line_xxx` is the ID of the master product checkbox in the product picker. When the user answers "Yes":

1. The corresponding product checkbox auto-checks
2. That product's question section auto-reveals
3. The page smooth-scrolls down to it so the user notices

**Current cross-sell coverage:**

| Section | Cross-sells offered |
|---|---|
| Auto | Home (existing relationship), Umbrella |
| Home | Auto, Umbrella |
| Condo | Umbrella |
| Renters | Umbrella |
| Rental Property | Umbrella (note: landlords often need umbrella for tenant lawsuits) |
| Life | Umbrella |
| Recreational (Boat/Moto/RV/ATV) | Umbrella (note: boats/motorcycles especially benefit) |
| Business / Commercial | Workers Comp, Commercial Auto (info-only — see below), Commercial Umbrella |
| Workers Compensation | Business/Commercial, Commercial Umbrella |

**Note on Commercial Auto:** It's not a separate product checkbox — it's bundled under "Business / Commercial" because most commercial policies are written through one carrier. The "Want a Commercial Auto quote too?" question therefore captures the answer for the agent to follow up on, but doesn't trigger any auto-checking (the user already checked Business).

Adding a new cross-sell is a one-line HTML change — add `data-cross-sell="line_xxx"` to any `<select>` with Yes/No options. No JS edit needed.

## SEO & AEO

The site is instrumented for both:
- **InsuranceAgency / LocalBusiness schema** on every page (NAP, geo, hours, social, areaServed: Michigan)
- **FAQPage schema** on home, FAQ, personal/, business/, and most product pages
- **BlogPosting schema** on each blog post
- **BreadcrumbList schema** on every interior page
- **Review schema** on home and reviews page
- **Open Graph + Twitter Cards** on every page
- **Sitemap.xml + robots.txt** at root, kept in sync via build script

Top SEO priorities: rank for "Michigan independent insurance agency," "Lake Orion insurance agency," and product+location combinations ("Michigan workers compensation insurance," "Michigan auto insurance," etc.).

### Key external IDs / URLs

- **Google Review direct link** (used by the "Review us on Google" button on `/reviews/`): `https://g.page/r/CZiBtTy1adZDEAE/review`. This goes straight to the review form for the JJA Google Business Profile.
- **Google Analytics 4 measurement ID**: `G-QRLBD79S35`
- **Google Tag Manager container ID** (provisioned but not yet installed): `GT-M3LBGVP`
- **Google Search Console verification TXT**: `google-site-verification=pq73qHkdQNbIUtqC4QwoG4RTrGgMWjtwB15JvfXsw30` (already in DNS at GoDaddy)
- **Formspree form ID**: `xnjweggp` (dashboard: https://formspree.io/forms/xnjweggp/overview)

### Recommended post-launch tasks

Once DNS is pointed at Cloudflare and the site is live on `jjainsurance.com`, also do these (in priority order):

1. **Update Google Business Profile** to point to the new site URL. Confirm name/address/phone match the site exactly (the schema we ship uses `4301 S. Baldwin Rd, Lake Orion, MI 48359` and `(248) 693-6455`). Consistent NAP signals across the web help local SEO a lot.
2. **Resubmit sitemap in Google Search Console** at the new domain. The verification TXT is already in place; just point Search Console at the new sitemap URL.
3. **Set up Bing Webmaster Tools** (free, takes ~5 minutes). Bing is ~10% of search traffic and is also where ChatGPT pulls some of its citations from, so it matters for AEO too.
4. **Run a Rich Results Test** at https://search.google.com/test/rich-results on the homepage to confirm all the LocalBusiness / FAQ / Review schema validates cleanly.

## Domains & DNS

### Owned domains and what they should do

Joseph owns a portfolio of domains at GoDaddy. Strategy is **consolidate, not fragment** — 301-redirect everything brand-related or location-related to either the homepage or a relevant landing page. Don't build separate sites on each domain (duplicate-content penalties; splits SEO authority).

**Tier 1 — 301 redirect to homepage** (Joseph indicated these forwards are set up; verify in GoDaddy if uncertain):
- `jjacobsandassociates.com`, `jjains.com`, `jjacobsinsurance.com`, `jacobsfamilyinsurance.com` (brand variants)
- `michiganinsuranceagency.com`, `independentinsurancenearme.com`, `independentinsuranceagencynearme.com`, `michiganinsurancenearme.com` (descriptive/keyword)

**Tier 2 — 301 redirect to specific landing pages:**
| Source | Destination |
|---|---|
| `clarkstoninsurancenearme.com` | `/clarkston-insurance/` |
| `fentoninsurancenearme.com` | `/fenton-insurance/` |

**Tier 3 — non-business / personal (leave alone):**
`thewhiskeylady.com`, `emyliajacobs.com`, `juliejacobs.net`, `brennanjacobs.net`, `josephjacobs.net`

**Tier 4 — niche / drop at renewal:** `insurecryptosnow.com` (no active crypto-insurance line of business).

**.eth domains:** Joseph owns several (e.g. `fentoninsurance.eth`). They don't help SEO or AEO because Google/Bing/AI engines don't crawl ENS-resolved IPFS content. Recommendation is to let most expire and optionally keep `jjainsurance.eth` for future option value only. No active work needed on these.

**How to set up a redirect at GoDaddy:** Products → Manage on the domain → Forwarding section → Add → forward to the destination URL → **Permanent (301)** → **Forward only** (NOT "Forward with masking" — masking is bad for SEO).

### Current DNS state on jjainsurance.com (at GoDaddy)

**Correctly configured — don't touch:**
- **MX records** point to Google Workspace (`aspmx.l.google.com` and friends) — this handles all @jjainsurance.com email.
- **TXT `google-site-verification=pq73qHkdQNbIUtqC4QwoG4RTrGgMWjtwB15JvfXsw30`** — Search Console verification.
- **Google DKIM** record — email authentication.
- **DMARC** policy — `v=DMARC1;p=quarantine;pct=100`.
- **Apple domain verification** TXT — Apple Business Connect / iCloud Mail.

**Pending cleanup** (Joseph to do these in GoDaddy DNS Management — they're safe but tidying):
- Remove the "Template Applied: Crypto Wallet" template at the top of the DNS page (removes two `ENS1 0x...` Ethereum TXT records that came with it).
- Delete the `TXT @ NETORGFT12116311.onmicrosoft.com` record (Microsoft 365 verification leftover — Joseph doesn't use Microsoft 365).
- Fix the SPF record: change `v=spf1 include:mailgun.org include:_spf.google.com include:secureserver.net include:mailgun.org1 ~all` to `v=spf1 include:mailgun.org include:_spf.google.com ~all` (the original has a typo `mailgun.org1` and an unused `secureserver.net`). Keep Mailgun — Joseph does still use it.
- After WordPress cutover, delete the stale cPanel/WordPress CNAMEs: `autoconfig`, `autoconfig.admin`, `autodiscover`, `autodiscover.admin`, `cpanel`, `webdisk`, `webdisk.admin`, `webmail`, `whm`, `ftp`, `email`, `www.admin`. Also `fuse` (CNAME → mailgun.org) only if Mailgun is also being dropped — otherwise keep it.

**At go-live:**
- Update the `A @ 45.55.98.228` record (currently points to old WordPress host) to point to Cloudflare. Cloudflare will give the exact value to use when the custom domain is connected in the Pages dashboard. Don't change this until ready to flip the switch.

## Standing instructions for Claude

When making changes to this site:

1. **Read existing structure first** — don't reinvent. Match the design conventions, color variables, and patterns already in styles.css.
2. **Never use gold/yellow accents.** Navy + gray only.
3. **Never add emoji to site files** unless the user explicitly asks.
4. **Preserve relative paths** — use `./` or `../` prefixes, not `/` absolute paths.
5. **Bump cache-bust version** (`?v=...`) on CSS/JS references after any change to those files.
6. **Use native `<details>`/`<summary>`** for new dropdown/collapse UI — not JS-driven toggles.
7. **Blog posts**: write as markdown files in `content/blog/{slug}.md` with frontmatter, then run `python3 build.py` to generate HTML.
8. **Maintain SEO/AEO instrumentation** when adding pages: schema, Open Graph, canonical, breadcrumbs.
9. **Defer to PL Rater field structure** when modifying the quote form — fields should map cleanly to what staff will enter into the rater.
10. **Never bypass user confirmation** for actions that change deployed content. Make local edits, show the diff, let the user re-deploy to Cloudflare themselves.
11. **Default model for this project is Claude Sonnet 4.6.** Joseph noticed Opus consumed his usage limit faster than he wanted, and most work in this project (content edits, cache-bust bumps, adding pages, simple debugging) is well within Sonnet's range. Only suggest a temporary switch to Opus for genuinely complex tasks like heavy architectural reasoning or subtle cross-file bugs.
12. **Bash sandbox can't see most subdirectories.** `C:\Website` appears to be OneDrive-synced (or otherwise virtualized), so most subdirectories show up as cloud placeholders to the Linux bash sandbox. Bash often can't see into `assets/`, `blog/`, `about/`, etc., even though the host file tools (Read/Write/Edit/Glob/Grep) can — those force materialization on access. For bulk text replacements across many HTML files, don't trust a single bash `find … sed -i` — verify with a grep after, and fall back to per-file Edits for whatever didn't get touched.

## Open items / future work

- [ ] Migrate to Git-based deploys (GitHub + Cloudflare Pages auto-deploy) — see `SETUP-GUIDE.md`
- [ ] Set up Pages CMS once on Git for friendly blog editing — config already in `.pages.yml`
- [ ] Point `jjainsurance.com` DNS at Cloudflare (currently still pointing at WordPress host). The five legacy WordPress image URLs are already preserved at matching paths under `wp-content/uploads/sites/38/2026/` so the cutover won't break email signatures, the printed QR code, or other external links to those images.
- [ ] DNS housekeeping in GoDaddy: remove Crypto Wallet template, delete Microsoft 365 TXT, fix SPF typo. See "Domains & DNS" section above for exact steps.
- [ ] Replace placeholder OG image (`assets/img/og-default.jpg`) with a branded share card
- [ ] Optional: integrate quote form leads with Hawksoft via Canopy Connect or custom webhook
- [ ] Consider adding photos to Auto Insurance, Home Insurance, Business, Workers Comp, Service Center pages
- [ ] Optional next-batch city landing pages if Joseph wants more reach: Auburn Hills, Rochester Hills, Troy, Davison, Burton, Holly, Davisburg, Waterford, Almont, Imlay City, Metamora.

## Completed (recent)

- ✅ Google Analytics 4 wired up (ID `G-QRLBD79S35`, loads via `site.v2.js`)
- ✅ Google Search Console verified via TXT record
- ✅ 10 city landing pages built and added to `sitemap.xml`: clarkston, fenton, ortonville, oxford, grand-blanc, goodrich, lapeer, rochester, oakland-township, white-lake
- ✅ Quote form cross-sell triggers across all product sections (data-cross-sell pattern)
- ✅ Partial-lead capture on `/quotes/` (pagehide / beforeunload only — idle/visibilitychange removed to preserve Formspree 50/month free quota)
- ✅ Formspree Formshield disabled (was silently dropping partials in spam)
- ✅ Legacy WordPress image URL preservation (`wp-content/uploads/sites/38/2026/` shims)
- ✅ Favicon (SVG) added to all pages (`assets/img/favicon.svg`)
- ✅ OG share image built (`assets/img/og-default.jpg`) — navy gradient left panel with white logo, right panel with all 8 Best of the Best awards. Also saved as `jja-brand-card.jpg` (high quality) and `jja-brand-card-2x.jpg` (2400×1260 print resolution).
- ✅ Hero photos added to Auto Insurance, Home Insurance, Business, Workers Comp, Service pages
- ✅ Home quote form rebuilt with conditional logic (pool/trampoline/dogs/stove show/hide, auto cross-sell suppressed if auto already checked, address pre-fill)
- ✅ Contact form Formspree ID fixed (`contact/index.html` had placeholder `YOUR_FORM_ID` — corrected to `xnjweggp`)
- ✅ DNS moved to Cloudflare — nameservers updated at GoDaddy on 2026-05-17. All junk WordPress/cPanel CNAMEs deleted from Cloudflare. Email records (MX, DKIM, DMARC, SPF) verified present.

## Files & their purpose

- `index.html` and all other `.html` files — site pages (edit directly for content changes)
- `assets/css/styles.css` — all site styles (single source)
- `assets/js/site.v2.js` — site script (mobile menu, form helpers, year auto-update, **partial-lead capture for the quote form**). Note: nav dropdowns are CSS/HTML native, not JS.
- `URL's.docx` (at the site root) — Source-of-truth mapping for the five legacy WordPress image URLs that must keep resolving after DNS cutover. Filename has a literal apostrophe.
- `copy-images.bat` (at the site root) — One-shot helper script that copies the five preserved images from `assets/img/` into the matching `wp-content/uploads/sites/38/2026/...` paths. Already run; rerun if the wp-content folder ever needs to be rebuilt.
- `wp-content/uploads/sites/38/2026/03/` and `/04/` — Legacy URL preservation shims; see Site structure section.
- `assets/img/logo.jpeg` — site logo
- `assets/img/award-{year}.png` — 2018-2025 Best of the Best award images
- `assets/img/hero-home.jpg`, `team-office.jpg`, `personal-family.jpg`, `life-kids.jpg` — section imagery
- `content/blog/*.md` — blog post source files (markdown with YAML frontmatter)
- `build.py` — converts blog markdown → HTML on each run / each Git push
- `.pages.yml` — Pages CMS configuration (for future GitHub migration)
- `sitemap.xml`, `robots.txt` — SEO essentials
- `SETUP-GUIDE.md` — instructions for migrating to Git + setting up CMS
- `_pages.py`, `_build.py`, `_build_blog.py` — legacy build scripts (kept for reference, not used in current flow)

## Common tasks reference

**Update a phone number across the site**: edit all HTML files, bump cache-bust, redeploy.

**Add a new team member**: insert a new `<div class="team-card">...</div>` block in `team/index.html` matching the existing structure (avatar with initials, h3 name, role, bio paragraph, email link).

**Add a new blog post**:
1. Create `content/blog/your-post-slug.md` with frontmatter (slug, title, date, date_display, category, read_minutes, summary, meta_description)
2. Write the body in markdown or HTML below the closing `---`
3. Run `python3 build.py` from the Website folder
4. New post HTML appears at `blog/your-post-slug/index.html`
5. Drag the Website folder to Cloudflare to deploy

**Add a new product to Personal or Commercial page**: edit `personal/index.html` or `business/index.html` — add a new product-card link to the grid AND a new `<div class="product-definition" id="slug">...</div>` block below.

**Change brand colors**: edit the `:root` block at the top of `assets/css/styles.css`. All other colors derive from those variables.

**Update awards page**: replace year images in `assets/img/award-{year}.png` or add new years to the awards grid in `index.html` and `about/index.html`.

**Add a new city landing page** (the 10 existing ones — clarkston through white-lake — follow this template):

1. Pick the town and gather: correct ZIP codes (verify, don't guess), county, neighboring townships, 3-5 named lakes / parks / landmarks / institutions that locals would recognize, and a sentence on the town's character (rural / affluent suburb / lake community / county seat / etc.).
2. Copy `clarkston-insurance/index.html` as a starting template — it has the cleanest structure to clone.
3. Replace every town-specific reference with the new town's details. Make the prose feel local — name actual lakes, name the county courthouse, name the high school if it fits.
4. Update the schema blocks:
   - `InsuranceAgency` schema with `areaServed` listing the township + neighboring townships and ZIPs
   - `FAQPage` schema with 3 town-specific Q&As (e.g. about a local lake, about commuting to a regional center, about hobby farms if relevant)
   - `BreadcrumbList` schema
5. Set unique `<title>`, `<meta description>`, OG tags, and a self-referencing `<link rel="canonical">`.
6. Add the new URL to `sitemap.xml`.
7. If a town-specific `.com` redirect domain exists at GoDaddy, set up a 301 forward to the new page.

The hero, products section, commercial section, and footer should match the existing town pages exactly — same navy gradient hero, same product cards, same CTA layout. Only the localized copy and schema change.
