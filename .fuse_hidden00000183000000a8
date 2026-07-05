#!/usr/bin/env python3
"""
predeploy_check.py - J. Jacobs & Associates website pre-deploy gauntlet.

Run from C:\\Website on the real Windows machine BEFORE every
`npx wrangler deploy`:

    python predeploy_check.py

Exit code 0 = safe to deploy. Exit code 1 = DO NOT DEPLOY (failures listed).

Checks (each one exists because it caught or would have caught a real
incident on this site):
  1. Every HTML page ends in </html>            (truncation bug, 2026-06-14)
  2. No NUL bytes in any HTML file              (write-corruption band-aids)
  3. Exactly ONE cache-bust version sitewide
     for styles.css and for site.v2.js         (24-page drift, 2026-07-02)
  4. sitemap.xml matches the folder structure   (missing/ghost pages)
  5. All internal href/src links resolve        (blog cross-link 404s, June)
  6. Quote form: consent checkbox fingerprint   (A2P campaign verification)
     + worker action + honeypot + Turnstile
  7. Contact form: worker action + honeypot + Turnstile
  8. SEO/AEO files present (sitemap, robots, llms.txt, _headers, 404.html)
     and robots.txt points at the sitemap
  9. site.v2.js still contains the GA4 loader + phone_call event

NOTE: run this on the real machine, not the Cowork bash sandbox - the
sandbox mount can serve stale/truncated copies of recently edited files
and will produce false failures.
"""

import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"_archive", "node_modules", ".git", ".wrangler", "__pycache__"}
# Directories that contain no crawlable index pages (for the sitemap check)
NON_PAGE_DIRS = {"assets", "content", "social-images", "brand", "wp-content"}

failures = []
warnings = []


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


def html_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(root, fn)


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# ---- 1 + 2: endings and NUL bytes -----------------------------------------
def check_endings_and_nuls():
    n = 0
    for p in html_files():
        n += 1
        raw = open(p, "rb").read()
        if b"\x00" in raw:
            fail("NUL byte(s) in " + rel(p))
        if not raw.rstrip().endswith(b"</html>"):
            fail("Does not end in </html>: " + rel(p))
    print("  pages scanned: %d" % n)


# ---- 3: cache-bust census ---------------------------------------------------
def check_versions():
    census = {"styles.css": {}, "site.v2.js": {}}
    pat = re.compile(r'(styles\.css|site\.v2\.js)\?v=([0-9A-Za-z]+)')
    for p in html_files():
        text = open(p, encoding="utf-8", errors="replace").read()
        for name, ver in pat.findall(text):
            census[name].setdefault(ver, []).append(rel(p))
    for name, vers in census.items():
        if len(vers) == 0:
            fail("No %s?v= references found at all" % name)
        elif len(vers) > 1:
            detail = "; ".join(
                "%s on %d page(s) e.g. %s" % (v, len(ps), ps[0])
                for v, ps in sorted(vers.items())
            )
            fail("MULTIPLE %s versions: %s" % (name, detail))
        else:
            v = next(iter(vers))
            print("  %s?v=%s on %d page(s) - uniform" % (name, v, len(vers[v])))


# ---- 4: sitemap sync --------------------------------------------------------
def check_sitemap():
    sm_path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm_path):
        fail("sitemap.xml missing")
        return
    sm = open(sm_path, encoding="utf-8").read()
    urls = set(re.findall(
        r"<loc>https?://(?:www\.)?jjainsurance\.com(/[^<]*)</loc>", sm))
    pages = set()
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs
                   if d not in SKIP_DIRS and d not in NON_PAGE_DIRS]
        if "index.html" in files:
            r = os.path.relpath(root, ROOT).replace("\\", "/")
            pages.add("/" if r == "." else "/%s/" % r)
    missing = sorted(pages - urls)
    ghosts = sorted(urls - pages)
    for m in missing:
        fail("Page not in sitemap.xml: " + m)
    for g in ghosts:
        fail("sitemap.xml entry has no page: " + g)
    if not missing and not ghosts:
        print("  sitemap in sync: %d URLs" % len(urls))


# ---- 5: internal links ------------------------------------------------------
def check_links():
    checked = 0
    bad = set()
    skip_schemes = ("http://", "https://", "mailto:", "tel:", "sms:",
                    "data:", "javascript:", "//", "#")
    pat = re.compile(r'(?:href|src)="([^"#?]+)(?:[#?][^"]*)?"')
    for p in html_files():
        text = open(p, encoding="utf-8", errors="replace").read()
        base = os.path.dirname(p)
        for m in pat.finditer(text):
            u = m.group(1)
            if not u or u.startswith(skip_schemes):
                continue
            checked += 1
            u = urllib.parse.unquote(u)
            if u.startswith("/"):
                target = os.path.join(ROOT, u.lstrip("/"))
            else:
                target = os.path.normpath(os.path.join(base, u))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                bad.add("%s -> %s" % (rel(p), m.group(1)))
    for b in sorted(bad):
        fail("Broken internal link: " + b)
    print("  internal refs checked: %d" % checked)


# ---- 6 + 7: form fingerprints ----------------------------------------------
def _must_contain(path, needles, label):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        fail("%s missing (%s)" % (path, label))
        return
    text = open(p, encoding="utf-8", errors="replace").read()
    for needle, why in needles:
        if needle not in text:
            fail("%s: missing %s (%s)" % (path, why, label))


def check_forms():
    _must_contain("quotes/index.html", [
        ('action="https://jja-al3-worker.jacobs31.workers.dev"',
         "form action -> jja-al3-worker"),
        ('data-worker="https://jja-al3-worker.jacobs31.workers.dev"',
         "data-worker attribute (partial-lead capture)"),
        ('name="_gotcha"', "honeypot field"),
        ('cf-turnstile', "Turnstile widget"),
        ('id="consent"', "A2P consent checkbox"),
        ('Reply STOP', "A2P consent text: Reply STOP"),
        ('sms-terms', "A2P consent link to /sms-terms/"),
        ('privacy-policy', "A2P consent link to /privacy-policy/"),
        ('frequency varies',
         "A2P consent text: frequency disclosure"),
    ], "quote form / A2P verification - DO NOT DEPLOY if failing")
    _must_contain("contact/index.html", [
        ('action="https://jja-contact.jacobs31.workers.dev"',
         "form action -> jja-contact"),
        ('name="_gotcha"', "honeypot field"),
        ('cf-turnstile', "Turnstile widget"),
    ], "contact form")
    print("  form fingerprints checked")


# ---- 8: SEO/AEO files -------------------------------------------------------
def check_seo_files():
    for f in ("sitemap.xml", "robots.txt", "llms.txt", "_headers",
              "404.html"):
        if not os.path.exists(os.path.join(ROOT, f)):
            fail("Missing root file: " + f)
    rb = os.path.join(ROOT, "robots.txt")
    if os.path.exists(rb):
        if "sitemap" not in open(rb, encoding="utf-8",
                                 errors="replace").read().lower():
            fail("robots.txt has no Sitemap: line")
    print("  SEO/AEO root files present")


# ---- 9: site.v2.js critical content ----------------------------------------
def check_sitejs():
    p = os.path.join(ROOT, "assets", "js", "site.v2.js")
    if not os.path.exists(p):
        fail("assets/js/site.v2.js missing")
        return
    text = open(p, encoding="utf-8", errors="replace").read()
    if "G-QRLBD79S35" not in text:
        fail("site.v2.js: GA4 measurement ID G-QRLBD79S35 missing")
    if "phone_call" not in text:
        fail("site.v2.js: phone_call event missing (Ads conversion source)")
    if "partial_lead" not in text:
        fail("site.v2.js: partial-lead capture missing")
    print("  site.v2.js critical content present")


CHECKS = [
    ("1+2. Page endings and NUL bytes", check_endings_and_nuls),
    ("3. Cache-bust version census", check_versions),
    ("4. Sitemap sync", check_sitemap),
    ("5. Internal links", check_links),
    ("6+7. Form fingerprints", check_forms),
    ("8. SEO/AEO files", check_seo_files),
    ("9. site.v2.js content", check_sitejs),
]


def main():
    print("Pre-deploy check - %s" % ROOT)
    print("-" * 60)
    for label, fn in CHECKS:
        print(label)
        try:
            fn()
        except Exception as e:  # a crashed check must block deploy too
            fail("%s crashed: %r" % (label, e))
    print("-" * 60)
    for w in warnings:
        print("WARN: %s" % w)
    if failures:
        print("RESULT: FAIL - DO NOT DEPLOY (%d problem(s)):" % len(failures))
        for f in failures:
            print("  X %s" % f)
        sys.exit(1)
    print("RESULT: PASS - safe to deploy (npx wrangler deploy)")
    sys.exit(0)


if __name__ == "__main__":
    main()
