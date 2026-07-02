#!/usr/bin/env python3
"""
linkcheck.py - J. Jacobs & Associates website health check.

Crawls the LIVE site (every URL in sitemap.xml) over HTTP and verifies:
  * every page returns HTTP 200 AND ends in </html>  (truncation guard - see
    PROJECT-HANDOFF.md sec.2 "pages can be truncated mid-footer")
  * every INTERNAL link, image, and CSS/JS/icon asset returns HTTP 200

External (off-site) links are listed but only status-checked when you pass
--external (off-site sites often rate-limit automated checks, so results are noisy).

Reads the live site over HTTP only - it does NOT read or write any local site
files, so it is safe to run anywhere (including the Cowork sandbox); the only
thing it writes locally is a timestamped report under ./link-reports/.

Usage:
    python3 linkcheck.py            # internal check, writes report, prints summary
    python3 linkcheck.py --external # also status-check outbound links
    python3 linkcheck.py --json     # also print a machine-readable JSON summary

Exit code: 0 = clean, 1 = problems found, 2 = could not reach the site.
Stdlib only - no pip install needed.
"""
import sys, re, os, json, datetime, urllib.request, urllib.error
from urllib.parse import urljoin
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

ORIGIN   = "https://jjainsurance.com"
SITEMAP  = ORIGIN + "/sitemap.xml"
UA       = "JJA-linkcheck/1.0 (+monthly site health check)"
TIMEOUT  = 25
WORKERS  = 8
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "link-reports")


def fetch(url, method="GET"):
    """Return (status, body_bytes, final_url). status is an int or 'ERR:...'."""
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read() if method == "GET" else b""
            return r.status, body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, b"", url
    except Exception as e:
        return "ERR:" + type(e).__name__, b"", url


class RefParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []  # list of (kind, raw_url)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.refs.append(("link", d["href"]))
        elif tag == "img":
            if d.get("src"):
                self.refs.append(("img", d["src"]))
            for attr in ("srcset",):
                if d.get(attr):
                    for part in d[attr].split(","):
                        u = part.strip().split(" ")[0]
                        if u:
                            self.refs.append(("img", u))
        elif tag == "source" and d.get("srcset"):
            for part in d["srcset"].split(","):
                u = part.strip().split(" ")[0]
                if u:
                    self.refs.append(("img", u))
        elif tag == "link" and d.get("href"):
            rel = (d.get("rel") or "").lower()
            if "stylesheet" in rel:
                self.refs.append(("css", d["href"]))
            elif "icon" in rel:
                self.refs.append(("icon", d["href"]))
        elif tag == "script" and d.get("src"):
            self.refs.append(("js", d["src"]))


def is_internal(u):
    return u == ORIGIN or u.startswith(ORIGIN + "/")


def normalize(href, base):
    if not href:
        return None
    h = href.strip()
    if h.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    try:
        return urljoin(base, h).split("#")[0]
    except Exception:
        return None


def get_pages():
    status, body, _ = fetch(SITEMAP)
    if status != 200:
        print("FATAL: could not fetch sitemap.xml (status %s)" % status)
        sys.exit(2)
    return re.findall(r"<loc>([^<]+)</loc>", body.decode("utf-8", "replace"))


def main():
    external = "--external" in sys.argv
    as_json  = "--json" in sys.argv

    pages = get_pages()
    page_results = {}   # page -> {status, ends_html, len}
    resources    = {}   # resource_url -> {type, internal, pages:set}

    def crawl(page):
        status, body, _ = fetch(page)
        html = body.decode("utf-8", "replace")
        page_results[page] = {
            "status": status,
            "ends_html": html.rstrip().lower().endswith("</html>"),
            "len": len(html),
        }
        p = RefParser()
        try:
            p.feed(html)
        except Exception:
            pass
        for kind, href in p.refs:
            a = normalize(href, page)
            if not a:
                continue
            r = resources.setdefault(a, {"type": kind, "internal": is_internal(a), "pages": set()})
            r["pages"].add(page)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(crawl, pages))

    targets = [u for u, m in resources.items() if m["internal"] or external]
    res_status = {}

    def chk(u):
        st, _, _ = fetch(u, method="GET")
        res_status[u] = st

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(chk, targets))

    # ---- compile ----
    bad_pages = [(u, d) for u, d in page_results.items()
                 if d["status"] != 200 or not d["ends_html"]]
    bad_res = []
    for u, m in resources.items():
        st = res_status.get(u)
        if st is not None and st != 200:
            bad_res.append((u, m["type"], st, sorted(m["pages"])))
    bad_res.sort(key=lambda x: (x[1], x[0]))

    n_internal = sum(1 for m in resources.values() if m["internal"])
    n_external = sum(1 for m in resources.values() if not m["internal"])
    clean = not bad_pages and not bad_res

    # ---- report ----
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("J. JACOBS & ASSOCIATES - WEBSITE HEALTH CHECK")
    lines.append("Run: %s   Site: %s" % (stamp, ORIGIN))
    lines.append("=" * 60)
    lines.append("Pages crawled (from sitemap): %d" % len(pages))
    lines.append("Internal links/images/assets checked: %d" % n_internal)
    lines.append("External links found%s: %d" % (
        " (checked)" if external else " (listed, not checked)", n_external))
    lines.append("")
    if clean:
        lines.append("RESULT: PASS - no broken pages, links, or images found.")
    else:
        lines.append("RESULT: ISSUES FOUND - %d page problem(s), %d broken resource(s)."
                     % (len(bad_pages), len(bad_res)))
    lines.append("=" * 60)

    if bad_pages:
        lines.append("")
        lines.append("PAGE PROBLEMS (bad status or truncated / missing </html>):")
        for u, d in sorted(bad_pages):
            why = "status %s" % d["status"] if d["status"] != 200 else "TRUNCATED (no closing </html>)"
            lines.append("  - %s  [%s]" % (u, why))

    if bad_res:
        lines.append("")
        lines.append("BROKEN LINKS / IMAGES / ASSETS:")
        for u, kind, st, on_pages in bad_res:
            rel = u.replace(ORIGIN, "")
            lines.append("  - [%s %s] %s" % (st, kind, rel))
            lines.append("        appears on %d page(s):" % len(on_pages))
            for pg in on_pages:
                lines.append("          %s" % pg.replace(ORIGIN, ""))

    if clean:
        lines.append("")
        lines.append("Everything resolves with HTTP 200 and every page ends in </html>.")

    report = "\n".join(lines)

    os.makedirs(REPORT_DIR, exist_ok=True)
    fname = os.path.join(REPORT_DIR, "linkcheck-%s.txt" % now.strftime("%Y-%m-%d"))
    with open(fname, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    print(report)
    print("\nReport saved to: %s" % fname)

    if as_json:
        summary = {
            "run": stamp,
            "site": ORIGIN,
            "pages_crawled": len(pages),
            "internal_checked": n_internal,
            "external_found": n_external,
            "external_checked": external,
            "result": "PASS" if clean else "ISSUES",
            "page_problems": [{"url": u, "status": d["status"], "ends_html": d["ends_html"]}
                              for u, d in bad_pages],
            "broken_resources": [{"url": u, "type": k, "status": st,
                                   "pages": [p.replace(ORIGIN, "") for p in pg]}
                                  for (u, k, st, pg) in bad_res],
            "report_file": fname,
        }
        print("\n===JSON===")
        print(json.dumps(summary, indent=2))

    sys.exit(0 if clean else 1)


if __name__ == "__main__":
    main()
