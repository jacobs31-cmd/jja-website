#!/usr/bin/env python3
"""Build script for J. Jacobs Insurance site.

Reads markdown files from /content/blog/, generates the blog index and
individual post HTML pages. This runs on every Git push via Cloudflare Pages
build command.

Usage:
  python3 build.py
"""
import re
import json
from pathlib import Path

SITE_URL = "https://jjainsurance.com"
PHONE = "(248) 693-6455"
PHONE_TEL = "+12486936455"
EMAIL = "Support@jjainsurance.com"
# Cache-bust versions — keep in sync with the sitewide canonical values
# (styles.css and site.v2.js are versioned independently; bump only the one whose file changed).
CSS_VERSION = "20260529"
JS_VERSION = "20260702"  # bumped 2026-07-02 to match the sitewide bump done by the marketing project

CONTENT_DIR = Path('content/blog')
BLOG_DIR = Path('blog')

# ---- Hero image map for build.py-generated posts ----
# Value = filename relative to assets/img/blog/
# .svg  -> rendered as plain <img>
# .avif -> rendered as <picture> with Unsplash JPEG fallback
PHOTO_MAP = {
    'michigan-auto-insurance-glossary':                            'photo-1516862523118-a3724eb136d7.avif',
    'michigan-homeowners-insurance-glossary':                      'photo-1554774853-719586f82d77.avif',
    'michigan-insurance-questions-answered':                       'photo-1559982240-f760db87b822.avif',
    'michigan-motorcycle-insurance-terminology':                   'photo-1676631284522-8007dd380171.avif',
    'michigan-no-fault-option-6':                                  'photo-1578041262130-633307b3bfd6.avif',
    'michigan-workers-compensation-do-you-need-it-guide-for-business-owners': 'photo-1628147529780-36964fbb8d54.avif',
    'common-auto-insurance-terms':                                 'photo-1683743637041-a1215e8e3052.avif',
    'special-event-insurance':                                     'photo-1505944357431-27579db47558.avif',
    'what-happens-if-you-skip-your-workers-comp-audit-in-michigan': 'photo-1454165804606-c3d57bc86b40.avif',
    'does-your-michigan-homeowners-insurance-cover-storm-damage':   'photo-1605727216801-e27ce1d0cc28.avif',
    'how-much-does-business-insurance-cost-in-michigan':            'photo-1486406146926-c627a92ad1ab.avif',
    'how-to-switch-insurance-agents-in-michigan':                   'photo-1521791136064-7986c2920216.avif',
    'got-a-non-renewal-notice-michigan':                           'photo-1450101499163-c8848c66ca85.avif',
    'buying-a-home-in-michigan-insurance-checklist':               'photo-1554774853-719586f82d77.avif',
    'starting-a-business-in-michigan-insurance':                   'photo-1551836022-aadb801c60ae.avif',
    'michigan-workers-comp-cost':                                  'photo-1628147529780-36964fbb8d54.avif',
    'michigan-cannabis-insurance-cost':                            'photo-1486406146926-c627a92ad1ab.avif',
    'adding-a-teen-driver-michigan-cost':                          'photo-1516862523118-a3724eb136d7.avif',
    'bundling-home-auto-insurance-michigan':                       'photo-1570129477492-45c003edd2be.avif',
    'michigan-pole-barn-detached-garage-insurance':               'photo-1500076656116-558758c991c1.avif',
    'do-i-need-business-insurance-llc-michigan':                  'photo-1556742049-0cfed4f6a45d.avif',
}

# ---- Manually-written blog posts (DORMANT since 2026-07-02) ----
# All 15 posts below were back-filled with markdown sources in content/blog/
# (verified byte/text-faithful vs the live pages). Because each slug now has a
# .md file, build.py SKIPS these entries — they are kept only as a fallback in
# case a markdown source is ever accidentally deleted. To change one of these
# posts, edit its content/blog/<slug>.md — editing this list does nothing.
MANUAL_POSTS = [
    {'slug': 'commercial-auto-vs-personal-auto-michigan',
     'title': 'Commercial Auto vs. Personal Auto Insurance in Michigan: Why the Difference Matters',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Auto Insurance',
     'read_minutes': 7, 'image': 'photo-1574023240744-64c47c8c0676.avif',
     'summary': 'Using your personal vehicle for work in Michigan? Your personal policy may not cover you. Learn when you need commercial auto coverage.'},
    {'slug': 'does-your-michigan-business-need-cyber-insurance',
     'title': 'Does Your Michigan Business Need Cyber Insurance?',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Commercial Insurance',
     'read_minutes': 7, 'image': 'photo-1614064641938-3bbee52942c7.avif',
     'summary': 'Only 17% of Michigan SMBs carry cyber insurance -- yet the average breach costs $200K+. Learn what cyber coverage includes and whether your business needs it.'},
    {'slug': 'general-liability-insurance-michigan-contractors',
     'title': 'General Liability Insurance for Michigan Contractors',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Commercial Insurance',
     'read_minutes': 7, 'image': 'photo-1589939705384-5185137a7f0f.avif',
     'summary': "Michigan contractors: most GCs require $1M-$2M liability before you step on a job site. Here's what you need, what it costs, and how to get it fast."},
    {'slug': 'how-much-life-insurance-do-i-need',
     'title': 'How Much Life Insurance Do You Need?',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Life Insurance',
     'read_minutes': 6, 'image': 'photo-1709216461598-018ae6307dc0.avif',
     'summary': 'How much life insurance do you need in Michigan? Use the DIME method, 10x income rule, and our agent-tested checklist to find the right coverage amount.'},
    {'slug': 'how-to-file-homeowners-insurance-claim-michigan',
     'title': 'How to File a Homeowners Insurance Claim in Michigan: A Step-by-Step Guide',
     'date': '2026-05-28', 'date_display': 'May 28, 2026', 'category': 'Home Insurance',
     'read_minutes': 8, 'image': 'photo-1720065609938-ec0e33ffd9ad.avif',
     'summary': "Michigan homeowners: here's exactly how to file a home insurance claim step by step -- from documenting damage to getting your check."},
    {'slug': 'michigan-boat-rv-insurance',
     'title': 'Michigan Boat & RV Insurance: What You Need Before Summer Hits',
     'date': '2026-05-28', 'date_display': 'May 28, 2026', 'category': 'Personal Insurance',
     'read_minutes': 7, 'image': 'photo-1779078063955-8fbf934c358c.avif',
     'summary': "Michigan boat insurance starts at $200/year. RV insurance from $180/year. Learn what's required, what's covered, and when your home policy won't protect you."},
    {'slug': 'michigan-business-owners-policy',
     'title': "Michigan Business Owner's Policy (BOP) Guide",
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Commercial Insurance',
     'read_minutes': 6, 'image': 'photo-1551836022-aadb801c60ae.avif',
     'summary': "A BOP bundles GL and property coverage for Michigan small businesses. Learn what it covers, what it doesn't, and what a policy costs in Michigan."},
    {'slug': 'michigan-flood-insurance',
     'title': "Michigan Flood Insurance: What Homeowners Insurance Doesn't Cover",
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Home Insurance',
     'read_minutes': 7, 'image': 'photo-1657069342866-2d11c2509b02.avif',
     'summary': "Homeowners insurance doesn't cover flood damage in Michigan. Learn what NFIP and private flood policies cover, what they cost, and who really needs one."},
    {'slug': 'michigan-gap-insurance',
     'title': 'Michigan Gap Insurance: When You Need It',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Auto Insurance',
     'read_minutes': 6, 'image': 'photo-1585390062628-be8608aa7d83.avif',
     'summary': "Gap insurance in Michigan covers what's owed on your loan vs. your car's value after a total loss. Learn when you need it and what it costs."},
    {'slug': 'michigan-renters-insurance',
     'title': 'Michigan Renters Insurance Guide',
     'date': '2026-05-28', 'date_display': 'May 28, 2026', 'category': 'Home Insurance',
     'read_minutes': 7, 'image': 'photo-1768941124460-6fa7161715ff.avif',
     'summary': 'Michigan renters insurance averages $18/month and covers your belongings, liability, and hotel costs if your unit becomes uninhabitable.'},
    {'slug': 'michigan-teen-driver-insurance',
     'title': 'Adding a Teen Driver to Your Michigan Auto Policy: What Parents Need to Know',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Auto Insurance',
     'read_minutes': 7, 'image': 'Teen.avif',
     'summary': "Adding a teen driver in Michigan raises your auto insurance by $2,500+ per year. Here's how to minimize the cost without cutting essential coverage."},
    {'slug': 'michigan-umbrella-insurance-who-needs-it',
     'title': 'Michigan Umbrella Insurance: Who Needs It?',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Personal Insurance',
     'read_minutes': 6, 'image': 'photo-1562564055-71e051d33c19.avif',
     'summary': "Michigan umbrella insurance costs $400-$600/year for $1M in coverage. Find out who needs it, what it covers, and what it doesn't."},
    {'slug': 'term-vs-whole-life-insurance-michigan',
     'title': 'Term vs. Whole Life Insurance in Michigan',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Life Insurance',
     'read_minutes': 7, 'image': 'photo-1628676348963-f88c671333f6.avif',
     'summary': "Term vs. whole life insurance in Michigan: a clear breakdown of cost, coverage length, cash value, and which one fits your family's needs."},
    {'slug': 'why-home-insurance-went-up-2026',
     'title': 'Why Your Home Insurance Went Up in 2026',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Home Insurance',
     'read_minutes': 8, 'image': 'home-infograph.avif',
     'summary': 'Michigan home insurance rates are up 21% over two years. Learn the real reasons your premium rose in 2026 and 7 proven ways to lower it.'},
    {'slug': 'why-independent-insurance-agents-get-better-rates',
     'title': 'Why Independent Insurance Agents Get You Better Rates',
     'date': '2026-05-25', 'date_display': 'May 25, 2026', 'category': 'Insurance Education',
     'read_minutes': 6, 'image': 'photo-1526948531399-320e7e40f0ca.avif',
     'summary': 'One call to JJA Insurance compares 10+ Michigan carriers. See why independent agents consistently beat captive agents on price and coverage options.'},
]


# ---------------------- Frontmatter parser ----------------------
def parse_md(text):
    """Split a markdown file into (frontmatter dict, body string)."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 4)
    if end == -1:
        return {}, text
    fm_block = text[4:end].strip()
    body = text[end + 4:].lstrip('\n')
    fm = {}
    for line in fm_block.split('\n'):
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        if val.isdigit():
            val = int(val)
        fm[key.strip()] = val
    return fm, body


def md_to_html(text):
    """If text looks like raw HTML, pass through. Otherwise basic md -> html."""
    if '<p>' in text or '<h2>' in text or '<dl' in text or '<div class=' in text:
        return text
    lines = text.split('\n')
    out = []
    in_list = False
    for line in lines:
        h = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h:
            level = len(h.group(1))
            out.append(f'<h{level}>{h.group(2)}</h{level}>')
            continue
        if re.match(r'^[-*]\s+', line):
            if not in_list:
                out.append('<ul>')
                in_list = True
            item = re.sub(r'^[-*]\s+', '', line)
            out.append(f'<li>{item}</li>')
            continue
        if in_list and line.strip() == '':
            out.append('</ul>')
            in_list = False
        if line.strip() == '':
            out.append('')
        else:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            out.append(f'<p>{line}</p>')
    if in_list:
        out.append('</ul>')
    return '\n'.join(out)


# ---------------------- Shared HTML chunks ----------------------
def utility_bar():
    # SVG-icon version — matches the sitewide standard (homepage, about, manual posts).
    return (
        '<div class="utility-bar">\n  <div class="container">\n'
        '    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg> 4301 S. Baldwin Rd, Lake Orion, MI 48359</span>\n'
        f'    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z"/></svg> <a href="tel:{PHONE_TEL}">{PHONE}</a></span>\n'
        f'    <span class="utility-item"><svg class="ico" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg> <a href="mailto:{EMAIL}">{EMAIL}</a></span>\n'
        '  </div>\n</div>'
    )


def header(rel):
    return (
        '<header class="site-header"><div class="container">'
        f'<a class="brand" href="{rel}" aria-label="J. Jacobs and Associates Insurance home">'
        f'<img class="brand-logo-img" src="{rel}assets/img/logo.jpeg" alt="J. Jacobs and Associates Insurance">'
        '</a>'
        '<button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>'
        '<nav class="main-nav" id="primary-nav" aria-label="Primary"><ul>'
        '<li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Our Agency</summary>'
        '<ul class="submenu">'
        f'<li><a href="{rel}about/">About Us</a></li>'
        f'<li><a href="{rel}team/">Our Team</a></li>'
        f'<li><a href="{rel}carriers/">Our Carriers</a></li>'
        f'<li><a href="{rel}reviews/">Reviews</a></li>'
        '</ul></details></li>'
        '<li class="has-submenu"><details class="submenu-wrap"><summary class="nav-toggle">Products</summary>'
        '<ul class="submenu">'
        f'<li><a href="{rel}personal/">Personal Insurance</a></li>'
        f'<li><a href="{rel}personal/auto-insurance/">Auto Insurance</a></li>'
        f'<li><a href="{rel}personal/home-insurance/">Home Insurance</a></li>'
        f'<li><a href="{rel}personal/life-insurance/">Life Insurance</a></li>'
        f'<li><a href="{rel}business/">Commercial Insurance</a></li>'
        f'<li><a href="{rel}business/workers-compensation/">Workers Compensation</a></li>'
        '</ul></details></li>'
        f'<li><a href="{rel}service/">Service Center</a></li>'
        f'<li><a href="{rel}blog/">Blog</a></li>'
        f'<li><a href="{rel}faq/">FAQ</a></li>'
        f'<li><a href="{rel}contact/">Contact</a></li>'
        '</ul></nav>'
        '<div class="header-cta">'
        f'<a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a>'
        f'<a class="btn btn-primary" href="{rel}quotes/">Start a Quote</a>'
        '</div></div></header>'
    )


def footer(rel):
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        '<div class="footer-brand">'
        f'<div class="footer-logo"><img src="{rel}assets/img/logo.jpeg" alt="J. Jacobs and Associates"></div>'
        '<h4>J. Jacobs &amp; Associates</h4>'
        '<p>Family-owned independent insurance agency serving Michigan since 1981.</p>'
        f'<p style="margin-top:1rem;"><strong style="color:#fff;">4301 S. Baldwin Rd</strong><br>'
        f'Lake Orion, Michigan 48359<br>'
        f'<a href="tel:{PHONE_TEL}">{PHONE}</a><br>'
        f'<a href="mailto:{EMAIL}">{EMAIL}</a></p>'
        '</div>'
        '<div><h4>Insurance</h4><ul>'
        f'<li><a href="{rel}personal/">Personal Insurance</a></li>'
        f'<li><a href="{rel}personal/auto-insurance/">Auto Insurance</a></li>'
        f'<li><a href="{rel}personal/home-insurance/">Home Insurance</a></li>'
        f'<li><a href="{rel}personal/life-insurance/">Life Insurance</a></li>'
        f'<li><a href="{rel}business/">Commercial Insurance</a></li>'
        f'<li><a href="{rel}business/workers-compensation/">Workers Compensation</a></li>'
        '</ul></div>'
        '<div><h4>Agency</h4><ul>'
        f'<li><a href="{rel}about/">About Us</a></li>'
        f'<li><a href="{rel}team/">Our Team</a></li>'
        f'<li><a href="{rel}carriers/">Our Carriers</a></li>'
        f'<li><a href="{rel}reviews/">Reviews</a></li>'
        f'<li><a href="{rel}blog/">Blog</a></li>'
        f'<li><a href="{rel}faq/">FAQ</a></li>'
        '</ul></div>'
        '<div><h4>Follow Us</h4>'
        '<div class="social-row">'
        '<a href="https://www.facebook.com/JacobsandAssociates/" aria-label="Facebook" rel="noopener" target="_blank">f</a>'
        '<a href="https://www.instagram.com/jjacobs_and_associates/" aria-label="Instagram" rel="noopener" target="_blank">IG</a>'
        '<a href="https://www.linkedin.com/in/joe-jacobs-7a354422/" aria-label="LinkedIn" rel="noopener" target="_blank">in</a>'
        '</div>'
        '<ul style="margin-top:1.25rem;">'
        f'<li><a href="{rel}contact/">Contact Us</a></li>'
        f'<li><a href="{rel}privacy-policy/">Privacy Policy</a></li>'
        f'<li><a href="{rel}accessibility/">Accessibility</a></li>'
        '</ul></div>'
        '</div>'
        '<div class="footer-bottom">'
        '<span>&copy; <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span>'
        '<span>Independent Insurance Agency &middot; Lake Orion, Michigan</span>'
        '</div></div></footer>'
        f'\n<script src="{rel}assets/js/site.v2.js?v={JS_VERSION}" defer></script>\n</body>\n</html>'
    )


def head(title, description, canonical_path, extra_schema="", css_rel="../", og_image=None, extra_meta=""):
    og_img = og_image or f"{SITE_URL}/assets/img/og-default.jpg"
    gf = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{title}</title>\n"
        f"<meta name=\"description\" content=\"{description}\">\n"
        f"<link rel=\"canonical\" href=\"{SITE_URL}{canonical_path}\">\n"
        "<meta name=\"robots\" content=\"index, follow, max-image-preview:large, max-snippet:-1\">\n"
        "<meta name=\"theme-color\" content=\"#14365e\">\n"
        "<meta property=\"og:type\" content=\"article\">\n"
        f"<meta property=\"og:title\" content=\"{title}\">\n"
        f"<meta property=\"og:description\" content=\"{description}\">\n"
        f"<meta property=\"og:url\" content=\"{SITE_URL}{canonical_path}\">\n"
        "<meta property=\"og:site_name\" content=\"J. Jacobs &amp; Associates\">\n"
        f"<meta property=\"og:image\" content=\"{og_img}\">\n"
        "<meta property=\"og:image:width\" content=\"1200\">\n"
        "<meta property=\"og:image:height\" content=\"630\">\n"
        "<meta property=\"og:locale\" content=\"en_US\">\n"
        "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
        f"<meta name=\"twitter:title\" content=\"{title}\">\n"
        f"<meta name=\"twitter:description\" content=\"{description}\">\n"
        f"<meta name=\"twitter:image\" content=\"{og_img}\">\n"
        f"{extra_meta}"
        "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        f"<link href=\"{gf}\" rel=\"stylesheet\">\n"
        f"<link rel=\"stylesheet\" href=\"{css_rel}assets/css/styles.css?v={CSS_VERSION}\">\n"
        f"{extra_schema}\n"
        "</head>\n<body>\n"
        "<a class=\"skip-link\" href=\"#main\">Skip to content</a>\n"
    )


def hero_fig(img, title, rel='../../'):
    """Full-width hero figure for individual blog posts."""
    if not img:
        return ''
    src = f'{rel}assets/img/blog/{img}'
    is_unsplash = img.endswith('.avif') and (img.startswith('photo-') or img.startswith('premium_photo-'))
    if is_unsplash:
        photo_id = img.replace('.avif', '')
        fallback = f'https://images.unsplash.com/{photo_id}?w=1200&q=85&auto=format&fit=crop&fm=jpg'
        return (
            '<figure style="margin:0 0 2rem;border-radius:12px;overflow:hidden;">'
            f'<picture><source srcset="{src}" type="image/avif">'
            f'<img src="{fallback}" alt="{title}" style="width:100%;height:auto;display:block;" loading="eager" width="1200" height="630">'
            '</picture></figure>\n'
        )
    else:
        return (
            '<figure style="margin:0 0 2rem;border-radius:12px;overflow:hidden;">'
            f'<img src="{src}" alt="{title}" style="width:100%;height:auto;display:block;" loading="eager" width="1200" height="630">'
            '</figure>\n'
        )


def card_thumb(img, title):
    """Thumbnail image for the blog index card (bleeds to card edges)."""
    if not img:
        return ''
    src = f'../assets/img/blog/{img}'
    is_unsplash = img.endswith('.avif') and (img.startswith('photo-') or img.startswith('premium_photo-'))
    if is_unsplash:
        photo_id = img.replace('.avif', '')
        fallback = f'https://images.unsplash.com/{photo_id}?w=600&q=70&auto=format&fit=crop&fm=jpg'
        return (
            '<div class="blog-card-thumb"><picture>'
            f'<source srcset="{src}" type="image/avif">'
            f'<img src="{fallback}" alt="{title}" loading="lazy" width="600" height="315">'
            '</picture></div>'
        )
    else:
        return f'<div class="blog-card-thumb"><img src="{src}" alt="{title}" loading="lazy" width="600" height="315"></div>'


def build_faq_schema(body_html):
    """If the post body has an FAQ section (an <h2> containing 'Frequently Asked
    Questions' / 'FAQ' followed by <h3> questions), emit FAQPage JSON-LD so the post
    can win 'People Also Ask' results and AI-engine citations. Returns '' if none.
    The schema is generated FROM the visible Q&A, so it always matches the page."""
    m = re.search(r'<h2[^>]*>\s*(?:Frequently Asked Questions|FAQs?)\b.*?</h2>(.*?)(?=<h2|\Z)',
                  body_html, re.S | re.I)
    if not m:
        return ''
    qas = []
    for q, a in re.findall(r'<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|\Z)', m.group(1), re.S):
        q = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', q)).strip()
        a = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', a)).strip()
        if q and a:
            qas.append({"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}})
    # Also support the site-standard <details class="faq-item"> markup
    for q, a in re.findall(
            r'<details class="faq-item">\s*<summary>(.*?)</summary>(.*?)</details>',
            m.group(1), re.S):
        q = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', q)).strip()
        a = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', a)).strip()
        if q and a:
            qas.append({"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}})
    if not qas:
        return ''
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qas}
    return '\n<script type="application/ld+json">\n' + json.dumps(data) + '\n</script>'


# ---------------------- Build blog ----------------------
def build_blog():
    print("Building blog from markdown files...")
    posts = []
    if not CONTENT_DIR.exists():
        print("  No content/blog/ found -- skipping.")
        return

    # sorted() = deterministic build on every OS (matches Windows glob order,
    # which is what the live site was generated with)
    for md_file in sorted(CONTENT_DIR.glob('*.md')):
        text = md_file.read_text(encoding='utf-8')
        fm, body = parse_md(text)
        if not fm.get('slug'):
            fm['slug'] = md_file.stem
        fm['body_html'] = md_to_html(body)
        posts.append(fm)

    if not posts:
        print("  No posts found.")
        return

    for p in posts:
        p.setdefault('image', PHOTO_MAP.get(p['slug'], ''))

    md_slugs = {p['slug'] for p in posts}
    all_posts = list(posts)
    for mp in MANUAL_POSTS:
        if mp['slug'] not in md_slugs:
            entry = dict(mp)
            entry['_manual'] = True
            all_posts.append(entry)

    all_posts.sort(key=lambda p: str(p.get('date', '')), reverse=True)

    cards = []
    for p in all_posts:
        thumb = card_thumb(p.get('image', ''), p['title'])
        cards.append(
            '<article class="blog-card">'
            f'<a href="./{p["slug"]}/" class="blog-card-link">'
            f'{thumb}'
            '<div class="blog-card-meta">'
            f'<span class="blog-card-cat">{p.get("category", "Insurance")}</span>'
            '<span class="blog-card-dot">&middot;</span>'
            f'<time datetime="{p.get("date", "")}">{p.get("date_display", "")}</time>'
            '<span class="blog-card-dot">&middot;</span>'
            f'<span>{p.get("read_minutes", "")} min read</span>'
            '</div>'
            f'<h2>{p.get("card_title") or p["title"]}</h2>'
            f'<p>{p.get("summary", "")}</p>'
            '<span class="blog-card-cta">Read article &rarr;</span>'
            '</a></article>'
        )

    bc_schema = (
        '<script type="application/ld+json">\n'
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
        f'{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE_URL}/"}},'
        f'{{"@type":"ListItem","position":2,"name":"Blog","item":"{SITE_URL}/blog/"}}'
        ']}\n</script>'
    )
    blog_schema = (
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"Blog","name":"J. Jacobs & Associates Insurance Blog","url":"'
        + SITE_URL + '/blog/","publisher":{"@type":"Organization","name":"J. Jacobs & Associates"}}\n</script>'
    )

    idx_html = head(
        title="Michigan Insurance Blog | Tips & News | JJA Insurance",
        description="Michigan insurance news, education, and tips from J. Jacobs & Associates -- covering auto, home, life, business, workers comp, and more. Updated regularly.",
        canonical_path="/blog/",
        extra_schema=bc_schema + "\n" + blog_schema,
        css_rel="../",
        og_image=f"{SITE_URL}/assets/img/og/blog.jpg",
    )
    idx_html += (
        utility_bar() + '\n' +
        header('../') + '\n' +
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
        '<li><a href="../">Home</a></li><li>Blog</li></ol></div></nav>\n'
        '<main id="main">\n<section class="section page-hero">\n<div class="container">\n'
        '<span class="eyebrow">News &amp; Education</span>\n'
        '<h1>Insurance Insights from J. Jacobs &amp; Associates</h1>\n'
        '<p class="lead">Michigan-specific insurance education, news, and practical advice from our team of licensed agents. Updated regularly.</p>\n'
        '<div class="blog-grid">' + ''.join(cards) + '</div>\n'
        '<div class="callout"><h2>Want to talk to a real agent?</h2>'
        '<p>Get a free comparison quote across our 50+ carriers -- no obligation.</p>'
        '<a class="btn btn-primary btn-lg" href="../quotes/">Start My Quote</a></div>\n'
        '</div>\n</section>\n</main>\n' +
        footer('../')
    )
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    (BLOG_DIR / 'index.html').write_text(idx_html, encoding='utf-8')
    print("  blog/index.html")

    for i, p in enumerate(posts):
        prev_p = posts[i-1] if i > 0 else None
        next_p = posts[i+1] if i < len(posts) - 1 else None

        post_img = p.get('image', '')
        og_img_url = f"{SITE_URL}/assets/img/og/blog-{p['slug']}.jpg"
        word_count = len(re.sub(r'<[^>]+>', ' ', p['body_html']).split())
        faq_schema = build_faq_schema(p['body_html'])

        article_schema = (
            '<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"BlogPosting",'
            f'"headline":"{p["title"]}","image":"{og_img_url}","datePublished":"{p.get("date","")}",'
            f'"dateModified":"{p.get("date","")}","author":{{"@type":"Person","name":"Joseph Jacobs","url":"{SITE_URL}/team/"}},'
            f'"publisher":{{"@type":"Organization","name":"J. Jacobs & Associates","logo":{{"@type":"ImageObject","url":"{SITE_URL}/assets/img/logo.jpeg"}}}},'
            f'"inLanguage":"en-US","articleSection":"{p.get("category","Insurance")}","wordCount":{word_count},'
            f'"description":"{p.get("meta_description","")}","mainEntityOfPage":{{"@type":"WebPage","@id":"{SITE_URL}/blog/{p["slug"]}/"}}}}' +
            ('\n</script>' if True else '')
        )
        bc = (
            '<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            f'{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE_URL}/"}},'
            f'{{"@type":"ListItem","position":2,"name":"Blog","item":"{SITE_URL}/blog/"}},'
            f'{{"@type":"ListItem","position":3,"name":"{p["title"][:80]}","item":"{SITE_URL}/blog/{p["slug"]}/"}}' +
            ']}\n</script>'
        )

        article_meta = (
            f'<meta property="article:published_time" content="{p.get("date","")}">\n'
            f'<meta property="article:modified_time" content="{p.get("date","")}">\n'
            f'<meta property="article:author" content="{SITE_URL}/team/">\n'
            f'<meta property="article:section" content="{p.get("category","Insurance")}">\n'
            '<meta name="twitter:creator" content="@JJAInsurance">\n'
            f'<link rel="sitemap" type="application/xml" href="{SITE_URL}/sitemap.xml">\n'
        )
        speakable = (
            '\n<script type="application/ld+json">\n'
            '{"@context": "https://schema.org", "@type": "WebPage", "speakable": '
            '{"@type": "SpeakableSpecification", "cssSelector": '
            '[".blog-post-header h1", ".blog-post-body .lead", ".blog-post-body h2:first-of-type"]}, '
            f'"url": "{SITE_URL}/blog/{p["slug"]}/"}}\n</script>'
        )

        # seo_title (optional frontmatter) = short <title>/og:title variant;
        # falls back to the full H1 title. Lets back-filled posts keep the exact
        # title tag they already rank with.
        h = head(
            title=f'{p.get("seo_title") or p["title"]} | JJA Insurance',
            description=p.get('meta_description', ''),
            canonical_path=f'/blog/{p["slug"]}/',
            extra_schema=article_schema + '\n' + bc + faq_schema + speakable,
            css_rel='../../',
            og_image=og_img_url,
            extra_meta=article_meta,
        )

        nav_links = []
        if prev_p:
            nav_links.append(
                f'<a class="post-nav-link prev" href="../{prev_p["slug"]}/">'
                f'<span class="post-nav-label">&larr; Previous</span>'
                f'<span class="post-nav-title">{prev_p.get("card_title") or prev_p["title"]}</span></a>'
            )
        if next_p:
            nav_links.append(
                f'<a class="post-nav-link next" href="../{next_p["slug"]}/">'
                f'<span class="post-nav-label">Next &rarr;</span>'
                f'<span class="post-nav-title">{next_p.get("card_title") or next_p["title"]}</span></a>'
            )
        post_nav = '<nav class="post-nav">' + ''.join(nav_links) + '</nav>' if nav_links else ''

        article = (
            '<article class="blog-post">'
            '<header class="blog-post-header">'
            f'<span class="eyebrow">{p.get("category", "Insurance")}</span>'
            f'<h1>{p["title"]}</h1>'
            '<div class="blog-post-meta">'
            '<span>By <strong>Joseph Jacobs</strong></span>'
            '<span>&middot;</span>'
            f'<time datetime="{p.get("date","")}">{p.get("date_display","")}</time>'
            '<span>&middot;</span>'
            f'<span>{p.get("read_minutes","")} min read</span>'
            '</div>'
            '</header>\n'
            + hero_fig(post_img, p['title']) +
            f'<div class="blog-post-body">\n{p["body_html"]}\n</div>'
            '<footer class="blog-post-footer">'
            # Author bio (E-E-A-T). NOTE: wording corrected 2026-07-02 — the agency was
            # founded by Jeff Jacobs in 1981; Joseph took over in 2014 (handoff §1).
            '<div style="display:flex;align-items:flex-start;gap:1.25rem;background:var(--gray-50);border:1px solid var(--border);border-radius:var(--r-md);padding:1.5rem;margin:2rem 0;">'
            '<div>'
            '<strong style="display:block;font-size:1rem;color:var(--ink);">Joseph Jacobs</strong>'
            '<span style="font-size:0.85rem;color:var(--text-muted);">Licensed Michigan Insurance Agent &amp; Agency Principal</span>'
            '<p style="margin:0.5rem 0 0;font-size:0.9rem;color:var(--text);">Joseph leads J. Jacobs &amp; Associates, his family\'s independent agency founded in 1981, and has spent his career helping Michigan families and businesses navigate insurance. He holds licenses across personal and commercial lines, and under his leadership the agency has earned Lake Orion&#39;s Readers&#39; Choice Best Insurance Agency award eight consecutive years (2018&ndash;2025). '
            '<a href="../../team/" style="color:var(--navy);">Meet our team &rarr;</a></p>'
            '</div>'
            '</div>'
            '<div class="blog-post-cta">'
            '<h2>Have questions about your coverage?</h2>'
            '<p>Our Michigan-licensed agents are happy to review your policy and answer your questions — no cost, no obligation.</p>'
            f'<p><a class="btn btn-primary btn-lg" href="../../quotes/">Get a Free Quote</a>&nbsp;'
            f'<a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a></p>'
            '</div>'
            '<div class="blog-disclaimer">'
            '<p><strong>Disclaimer:</strong> This blog post is intended for general educational purposes only and does not constitute insurance advice for any specific situation. Coverage availability, terms, and pricing vary by insurer, policy form, and individual risk characteristics. Michigan insurance laws and regulations are subject to change. Consult a licensed Michigan insurance agent for advice specific to your circumstances. J. Jacobs and Associates is licensed in the state of Michigan.</p>'
            '</div>'
            + post_nav +
            '</footer></article>'
        )

        body_full = (
            utility_bar() + '\n' +
            header('../../') + '\n' +
            f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
            f'<li><a href="../../">Home</a></li><li><a href="../">Blog</a></li><li>{p["title"][:60]}</li>'
            f'</ol></div></nav>\n'
            '<main id="main">\n<section class="section"><div class="container" style="max-width:820px;">' +
            article +
            '</div></section>\n</main>\n' +
            footer('../../')
        )

        out = BLOG_DIR / p['slug'] / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(h + body_full, encoding='utf-8')
        print(f"  blog/{p['slug']}/index.html")

    print(f"\n  Built {len(posts)} posts from markdown + {len(all_posts)-len(posts)} manual = {len(all_posts)} total in index.")


if __name__ == '__main__':
    build_blog()
    print("\nDone.")
