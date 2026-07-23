#!/usr/bin/env python3
"""
bump_version.py - unify the cache-bust ?v= version across the whole site.

Run from C:\\Website on the real Windows machine BEFORE predeploy_check:

    python bump_version.py

It rewrites every  styles.css?v=...  , site.v2.js?v=...  and  home.css?v=...
reference in every .html page to ONE new version, so returning visitors
fetch the refreshed CSS/JS (they're served with a 7-day cache) and so
predeploy_check.py's "exactly one version sitewide" test passes.

Safe: only the ?v= query changes; nothing else in the files is touched.
Edit NEW_VERSION below if you want a different stamp.
"""
import os
import re

NEW_VERSION = "20260719"
ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"_archive", "node_modules", ".git", ".wrangler", "__pycache__", "wp-content"}
PAT = re.compile(r'(styles\.css|site\.v2\.js|home\.css)\?v=[0-9A-Za-z]+')

def html_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(root, fn)

def main():
    before = {}
    changed = 0
    total = 0
    for p in html_files():
        total += 1
        # newline="" preserves the file's exact line endings (CRLF/LF) so we
        # only ever change the ?v= query, nothing else.
        text = open(p, encoding="utf-8", errors="replace", newline="").read()
        for name, ver in [(m.group(1), m.group(0).split("=")[-1]) for m in PAT.finditer(text)]:
            before.setdefault(name, {}).setdefault(ver, 0)
            before[name][ver] += 1
        new = PAT.sub(lambda m: "%s?v=%s" % (m.group(1), NEW_VERSION), text)
        if new != text:
            # safe write: full content, flush+close, then verify it landed
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            if open(p, encoding="utf-8", errors="replace", newline="").read() != new:
                raise SystemExit("WRITE VERIFY FAILED: " + p)
            changed += 1

    print("Scanned %d HTML files; rewrote %d." % (total, changed))
    print("Was (before):")
    for name, vers in before.items():
        print("  %s -> %s" % (name, ", ".join("%s(%d)" % (v, c) for v, c in sorted(vers.items()))))
    print("Now: everything -> ?v=%s" % NEW_VERSION)

if __name__ == "__main__":
    main()
