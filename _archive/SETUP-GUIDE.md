# J. Jacobs Insurance — Site Setup & Maintenance Guide

This guide walks you through:
1. Moving your site to a Git-based deployment (one-time setup)
2. Setting up Pages CMS so you can edit blog posts in a friendly UI
3. Ongoing maintenance — what you can do yourself, what to ask for help with

Time required: about 60-90 minutes for the one-time setup.

---

## Part 1 — Move to Git-based deploys (one-time, ~30 min)

You're currently dragging-and-dropping the site folder into Cloudflare Pages. That works fine, but you can't use a CMS with that method. To use Pages CMS, the site needs to live in a Git repository (GitHub) and Cloudflare needs to deploy from that repo automatically.

### Step 1.1 — Create a GitHub account

1. Go to https://github.com/signup
2. Use your work email (jacobs31@jjainsurance.com)
3. Verify your email and pick a username (e.g., `jjacobs-insurance` or your name)

### Step 1.2 — Install GitHub Desktop

GitHub Desktop is the easy graphical app for using GitHub. No command line needed.

1. Download from https://desktop.github.com
2. Install and sign in with your new GitHub account

### Step 1.3 — Create the repo and push your site

1. Open GitHub Desktop → **File → New Repository**
2. Name: `jjainsurance-site`
3. Local Path: select your `Documents` folder (it'll create `Documents/jjainsurance-site/`)
4. ⚠️ Don't add a README — we already have one
5. Click **Create Repository**

Now copy your existing site files into the new repo folder:

6. Open File Explorer to `Documents/Website/`
7. Select all files (Ctrl+A) and copy
8. Paste into `Documents/jjainsurance-site/`
9. Back in GitHub Desktop, you'll see all the files listed as changes
10. Write a commit message: `Initial commit — site v1`
11. Click **Commit to main**
12. Click **Publish repository** (top right). Uncheck "Keep this code private" if you want it public, or keep it private if you prefer.

Your site is now on GitHub.

### Step 1.4 — Connect Cloudflare Pages to GitHub

1. Go to your Cloudflare dashboard → **Workers & Pages** → your `jjainsurance` project
2. Click **Settings → Builds & deployments → Configure production deployments**
3. Click **Connect to Git** (or similar)
4. Authorize Cloudflare to access your GitHub
5. Select the `jjainsurance-site` repo
6. **Branch**: `main`
7. **Build command**: `python3 build.py`
8. **Build output directory**: `/` (just a slash — the site files are at the root)
9. Save

From now on, every push to `main` on GitHub auto-deploys to your Cloudflare site within about 60 seconds.

⚠️ **From now on, do NOT drag-drop folders into Cloudflare.** Always edit via GitHub Desktop or Pages CMS.

---

## Part 2 — Set up Pages CMS (~15 min)

Pages CMS is a free, friendly browser-based editor for content in your GitHub repo. It lets you write blog posts in a Word-like editor without touching code.

### Step 2.1 — Sign in to Pages CMS

1. Go to https://pagescms.org
2. Click **Sign in with GitHub**
3. Authorize Pages CMS to access your repos

### Step 2.2 — Connect the repo

1. From the Pages CMS dashboard, click **+ Add repository**
2. Select `jjainsurance-site`
3. Branch: `main`
4. Pages CMS will detect the `.pages.yml` file we already set up — that's the configuration that tells it what fields each post has

That's it. You should now see **Blog Posts** in the Pages CMS sidebar with all 10 existing posts.

### Step 2.3 — Add a new blog post

1. In Pages CMS, click **Blog Posts** in the sidebar
2. Click **+ Add Entry**
3. Fill in the fields:
   - **URL slug**: lowercase letters, numbers, and hyphens only (e.g., `michigan-renters-insurance-guide`). This becomes the URL.
   - **Title**: The headline
   - **Publish date**: When it was/will be published
   - **Date display**: How you want the date shown (e.g., `January 15, 2026`)
   - **Category**: Pick from the dropdown
   - **Read minutes**: Estimated read time
   - **Summary**: 1-2 sentences for the blog index page
   - **Meta description**: 150-160 characters for Google
   - **Content**: Write your post in the rich-text editor
4. Click **Save**

Pages CMS commits your new post to GitHub. Cloudflare detects the commit and rebuilds the site within 60 seconds. Your new post is live.

### Step 2.4 — Edit an existing post

1. Click any post in the Blog Posts list
2. Edit any field
3. Click **Save**

Same thing — auto-deploys to your live site within a minute.

---

## Part 3 — What you can edit yourself vs. ask for help

### Self-service (anyone on your team)
- Add or edit blog posts via Pages CMS — easy
- Update office hours, phone number — edit the `.pages.yml` settings file
- Add team member photos — drop them in `assets/img/team/` and reference in `team/index.html`

### Easier to ask
- Adding a new team member with full bio
- Adding/removing carriers from the carriers page
- Adding a new product page (auto, home variants, etc.)
- Color/layout changes
- Adding new sections or pages

Anyone with GitHub Desktop and a text editor can do everything above by editing HTML directly, but it's faster to just ask.

---

## Part 4 — Other things you'll want to set up

Once your site is live on the real domain:

### Google Search Console (free, do this within first week)
- Go to https://search.google.com/search-console
- Add `jjainsurance.com` as a property
- Submit your sitemap: `https://www.jjainsurance.com/sitemap.xml`
- Google starts crawling and indexing within days

### Bing Webmaster Tools (free)
- https://www.bing.com/webmasters — same as Google. About 10% of searches still come from Bing/Yahoo/DuckDuckGo.

### Google Business Profile (free, critical for local SEO)
- You probably already have this. Make sure it's claimed, verified, and the website URL points to the new site.
- Ensure name/address/phone exactly match what's on the new site (NAP consistency is a huge local-SEO factor).

### Google Analytics 4 (free, optional)
- https://analytics.google.com
- Create a property for jjainsurance.com
- Copy the tracking snippet
- I'll add it to `build.py` so it appears on every page

### Schema validator check (free, one-time)
- Test your structured data: https://search.google.com/test/rich-results
- Paste your homepage URL. Should show valid InsuranceAgency, FAQPage, Review, and BreadcrumbList schemas.

### Backups
- GitHub is your backup. Every version of every file is stored forever. You can roll back to any prior commit if something breaks.

---

## Part 5 — Lead form integration with Hawksoft + PL Rater

Your quote forms currently submit via Formspree (free) and email leads to Support@jjainsurance.com in a structured format.

To get those leads INTO PL Rater for rating, you have three options ranked by ease:

### Option A — Manual entry (current setup, $0)
Forms email a structured lead → your team copies fields into PL Rater. Works today. Cost: just your time.

### Option B — Canopy Connect (~$80-150/month)
The most common solution for independent agencies. Replaces your custom form with a Canopy widget that prefills consumer data and bridges directly into PL Rater. Big time savings. https://canopyconnect.com

### Option C — Direct Hawksoft + PL Rater integration (custom dev)
Hawksoft has an API; PL Rater has a partner program. Building a custom webhook that takes Formspree submissions, posts them to Hawksoft as a new prospect, and triggers a PL Rater quote is doable but requires development work. Reasonable estimate: $1,500-$3,000 one-time for a dev to build it, or I can spec it for you.

**My recommendation**: Stay on Option A for the first few months. If lead volume grows to where the manual entry becomes painful, evaluate Canopy Connect. Most agencies your size find Canopy Connect pays for itself in saved staff time.

---

## Questions?

Anytime you want to make a change you're not sure how to do, just open Cowork and ask. I can edit anything in the site and push it to GitHub on your behalf.
