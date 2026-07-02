#!/usr/bin/env python3
"""
Build script for J. Jacobs & Associates Insurance site.
Generates static HTML files from page content + shared header/footer templates.
Run from the site directory: python3 _build.py
"""
import os
import sys
from pathlib import Path

SITE_URL = "https://www.jjainsurance.com"
SITE_NAME = "J. Jacobs & Associates"
PHONE = "(248) 693-6455"
PHONE_TEL = "+12486936455"
EMAIL = "Support@jjainsurance.com"
ADDRESS_STREET = "4301 S. Baldwin Rd"
ADDRESS_FULL = "4301 S. Baldwin Rd, Lake Orion, MI 48359"

# ---------- HEAD TEMPLATE ----------
def head(title, description, path, og_image=None, extra_schema=""):
    """Build the <head> for a page."""
    canonical = f"{SITE_URL}{path}"
    og_image_url = og_image or f"{SITE_URL}/assets/img/og-default.jpg"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#1a3a5c">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/styles.css">
{extra_schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

# ---------- UTILITY BAR ----------
UTILITY_BAR = f"""
<div class="utility-bar">
  <div class="container">
    <span class="utility-item">📍 {ADDRESS_FULL}</span>
    <span class="utility-item">📞 <a href="tel:{PHONE_TEL}">{PHONE}</a></span>
    <span class="utility-item">✉️ <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div>
"""

# ---------- HEADER / NAV ----------
HEADER = f"""
<header class="site-header">
  <div class="container">
    <a class="brand" href="/">
      <span class="brand-logo" aria-hidden="true">JJ</span>
      <span>
        <span class="brand-name">J. Jacobs &amp; Associates</span>
        <p class="brand-tag">Independent Insurance · Since 1981</p>
      </span>
    </a>

    <button class="menu-toggle" aria-controls="primary-nav" aria-expanded="false">☰ Menu</button>

    <nav class="main-nav" id="primary-nav" aria-label="Primary">
      <ul>
        <li class="has-submenu">
          <a href="/about/">Our Agency</a>
          <ul class="submenu">
            <li><a href="/about/">About Us</a></li>
            <li><a href="/team/">Our Team</a></li>
            <li><a href="/carriers/">Our Carriers</a></li>
            <li><a href="/reviews/">Reviews</a></li>
          </ul>
        </li>
        <li class="has-submenu">
          <a href="/personal/">Products</a>
          <ul class="submenu">
            <li><a href="/personal/">Personal Insurance</a></li>
            <li><a href="/personal/auto-insurance/">Auto Insurance</a></li>
            <li><a href="/personal/home-insurance/">Home Insurance</a></li>
            <li><a href="/personal/life-insurance/">Life Insurance</a></li>
            <li><a href="/business/">Commercial Insurance</a></li>
            <li><a href="/business/workers-compensation/">Workers Compensation</a></li>
          </ul>
        </li>
        <li><a href="/service/">Service Center</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </nav>

    <div class="header-cta">
      <a class="btn btn-outline" href="tel:{PHONE_TEL}">Call</a>
      <a class="btn btn-primary" href="/quotes/">Start a Quote</a>
    </div>
  </div>
</header>
"""

# ---------- FOOTER ----------
FOOTER = f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h4>J. Jacobs &amp; Associates</h4>
        <p>Family-owned independent insurance agency serving Michigan since 1981. We shop 50+ carriers so you don&rsquo;t have to.</p>
        <p style="margin-top:1rem;">
          <strong style="color:#fff;">{ADDRESS_STREET}</strong><br>
          Lake Orion, Michigan 48359<br>
          <a href="tel:{PHONE_TEL}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
      <div>
        <h4>Insurance</h4>
        <ul>
          <li><a href="/personal/">Personal Insurance</a></li>
          <li><a href="/personal/auto-insurance/">Auto Insurance</a></li>
          <li><a href="/personal/home-insurance/">Home Insurance</a></li>
          <li><a href="/personal/life-insurance/">Life Insurance</a></li>
          <li><a href="/business/">Commercial Insurance</a></li>
          <li><a href="/business/workers-compensation/">Workers Compensation</a></li>
        </ul>
      </div>
      <div>
        <h4>Agency</h4>
        <ul>
          <li><a href="/about/">About Us</a></li>
          <li><a href="/team/">Our Team</a></li>
          <li><a href="/carriers/">Our Carriers</a></li>
          <li><a href="/reviews/">Reviews</a></li>
          <li><a href="/service/">Service Center</a></li>
          <li><a href="/faq/">FAQ</a></li>
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
          <li><a href="/contact/">Contact Us</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/accessibility/">Accessibility</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-current-year>2026</span> J. Jacobs &amp; Associates Insurance. All rights reserved.</span>
      <span>Independent Insurance Agency · Lake Orion, Michigan</span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

def breadcrumbs(items):
    """items = [(label, url), ...]; last item is current page."""
    crumbs_html = '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
    schema_items = []
    for i, (label, url) in enumerate(items):
        if i == len(items) - 1:
            crumbs_html += f'<li>{label}</li>'
        else:
            crumbs_html += f'<li><a href="{url}">{label}</a></li>'
        schema_items.append(f'{{"@type": "ListItem", "position": {i+1}, "name": "{label}", "item": "{SITE_URL}{url}"}}')
    crumbs_html += '</ol></div></nav>'
    schema = (
        '<script type="application/ld+json">\n'
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [' +
        ', '.join(schema_items) + ']}\n</script>'
    )
    return crumbs_html, schema

def page(path, title, description, body, extra_schema="", breadcrumb_items=None):
    """Build a full page and write it to disk."""
    schema = extra_schema
    bc_html = ""
    if breadcrumb_items:
        bc_html, bc_schema = breadcrumbs(breadcrumb_items)
        schema = bc_schema + "\n" + extra_schema
    html = head(title, description, path, extra_schema=schema)
    html += UTILITY_BAR + HEADER + bc_html + '<main id="main">\n' + body + '\n</main>\n' + FOOTER
    out = Path(__file__).parent / (path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f"  wrote {out.relative_to(Path(__file__).parent)}")

# ---------- IMPORT PAGE CONTENT ----------
from _pages import PAGES, EXTRAS

def build():
    print("Building site...")
    for p in PAGES:
        page(**p)
    for fname, content in EXTRAS.items():
        out = Path(__file__).parent / fname
        out.write_text(content, encoding='utf-8')
        print(f"  wrote {fname}")
    print("Done.")

if __name__ == '__main__':
    build()
