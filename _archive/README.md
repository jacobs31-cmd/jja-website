# J. Jacobs & Associates Insurance — Static Site

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
