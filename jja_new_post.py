#!/usr/bin/env python3
"""
JJA blog post helper — the deterministic backend for the `jja-blog-post` skill.

Claude does the judgment (dedupe, topics, writing, picking the right photo).
This script does the brittle mechanical parts that used to cause slips, and it
SELF-VERIFIES and refuses to leave temp files behind.

Run from C:\\Website (ideally in a real Windows terminal — no sandbox cache issues).

Subcommands
-----------
  list
      Print every existing post slug (built + markdown) so you can dedupe.

  hero-sheet "photo-AAA photo-BBB ..."  [out.png]
      Download candidate Unsplash photo IDs and tile them into one contact-sheet
      PNG so you can SEE them and pick the right one (we once shipped a vegetable
      photo for a barn post — always eyeball first). 404s are skipped. Default
      out = ./_hero_candidates.png (a temp file `finish`/`clean` will remove).

  hero photo-XXXX
      Download that photo full-res and write assets/img/blog/photo-XXXX.avif
      (quality 58, ~50-330 KB). Refuses if the file already exists or the id is
      already referenced anywhere. Print the line to paste into frontmatter.

  finish
      One shot: run build.py, generate OG cards, sync sitemap.xml (idempotent),
      verify every post, and remove temp scratch files. Prints a report and the
      deploy command (does NOT deploy).

  verify [slug ...]
      NUL-safe content check (reads via Python, not bash grep) of the built
      pages: ends in </html>, loads site.v2.js, has BlogPosting + BreadcrumbList,
      canonical, og:image card. Defaults to all posts.

  clean
      Remove known temp/scratch files so nothing strays into a deploy.
"""
import sys, os, re, glob, subprocess, datetime, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(ROOT, "blog")
CONTENT = os.path.join(ROOT, "content", "blog")
IMGDIR = os.path.join(ROOT, "assets", "img", "blog")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
SITE = "https://jjainsurance.com"
TEMP_GLOBS = ["_hero_candidates*.png", "build_fresh.py", "*_sentinel*.*", "_sentinel*"]

def _read(p):
    """NUL-safe read (the sandbox mount sometimes injects stray NUL bytes)."""
    with open(p, "rb") as f:
        return f.read().replace(b"\x00", b"").decode("utf-8", "replace")

def _unsplash(token, w=1600):
    url = f"https://images.unsplash.com/{token}?w={w}&q=85&auto=format&fit=crop&fm=jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()

def cmd_list():
    built = sorted(d for d in os.listdir(BLOG) if os.path.isdir(os.path.join(BLOG, d)))
    md = sorted(os.path.splitext(f)[0] for f in os.listdir(CONTENT) if f.endswith(".md"))
    print(f"{len(built)} built posts:")
    for s in built: print("  ", s)
    print(f"\n{len(md)} markdown sources:")
    for s in md: print("  ", s)

def cmd_hero_sheet(ids, out=None):
    from PIL import Image
    out = out or os.path.join(ROOT, "_hero_candidates.png")
    tiles, labels = [], []
    for tok in ids.split():
        try:
            data = _unsplash(tok, 800)
        except Exception as e:
            print(f"  skip {tok} ({e})"); continue
        tmp = os.path.join(ROOT, f"_cand_{tok}.jpg")
        open(tmp, "wb").write(data)
        tiles.append(tmp); labels.append(tok)
    if not tiles:
        print("No candidates resolved."); return
    cell_w, cell_h, pad = 360, 240, 6
    cols = min(3, len(tiles)); rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*(cell_w+pad)+pad, rows*(cell_h+pad)+pad), (245, 247, 250))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, (t, lab) in enumerate(zip(tiles, labels)):
        im = Image.open(t).convert("RGB"); im.thumbnail((cell_w, cell_h))
        x = pad + (i % cols)*(cell_w+pad); y = pad + (i//cols)*(cell_h+pad)
        sheet.paste(im, (x, y)); d.text((x+4, y+4), lab, fill=(20, 54, 94))
        os.remove(t)
    sheet.save(out)
    print(f"Contact sheet -> {out}\n  Read it, then run:  python jja_new_post.py hero <chosen-id>")

def cmd_hero(token):
    if not (token.startswith("photo-") or token.startswith("premium_photo-")):
        print("Expected an Unsplash id like photo-1500076656116-558758c991c1"); return
    dest = os.path.join(IMGDIR, token + ".avif")
    if os.path.exists(dest):
        print(f"Already exists: {dest}"); return
    hits = subprocess.run(["grep", "-rl", token, ROOT], capture_output=True, text=True).stdout
    if hits.strip():
        print(f"WARNING: id already referenced:\n{hits}")
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(_unsplash(token))).convert("RGB")
    img.save(dest, "AVIF", quality=58)
    kb = os.path.getsize(dest)//1024
    print(f"Wrote {dest} ({kb} KB)\n  Add to the post's frontmatter:  image: {token}.avif")

def _slugs_from_content():
    out = []
    for f in sorted(glob.glob(os.path.join(CONTENT, "*.md"))):
        t = _read(f); slug = os.path.splitext(os.path.basename(f))[0]
        m = re.search(r'^slug:\s*(.+)$', t, re.M)
        if m: slug = m.group(1).strip().strip('"\'')
        out.append(slug)
    return out

def cmd_sitemap_sync():
    xml = _read(SITEMAP)
    today = datetime.date.today().isoformat()
    built = [d for d in os.listdir(BLOG) if os.path.isdir(os.path.join(BLOG, d))]
    added = []
    for slug in built:
        loc = f"{SITE}/blog/{slug}/"
        if loc in xml:
            continue
        block = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n")
        xml = xml.replace("</urlset>", block + "</urlset>")
        added.append(slug)
    if added:
        open(SITEMAP, "w", encoding="utf-8").write(xml)
    print(f"sitemap.xml: added {len(added)} new entr{'y' if len(added)==1 else 'ies'}" +
          (": " + ", ".join(added) if added else " (already in sync)"))

def cmd_verify(slugs=None):
    slugs = slugs or [d for d in os.listdir(BLOG) if os.path.isdir(os.path.join(BLOG, d))]
    ok = True
    for slug in slugs:
        f = os.path.join(BLOG, slug, "index.html")
        if not os.path.exists(f):
            print(f"  FAIL {slug}: no index.html"); ok = False; continue
        t = _read(f)
        checks = {
            "ends </html>": t.rstrip().endswith("</html>"),
            "site.v2.js": "site.v2.js?v=" in t,
            "BlogPosting": "BlogPosting" in t,
            "BreadcrumbList": "BreadcrumbList" in t,
            "canonical": 'rel="canonical"' in t,
            "og card": f"og/blog-{slug}.jpg" in t,
        }
        bad = [k for k, v in checks.items() if not v]
        print(("  OK   " if not bad else "  FAIL ") + slug + ("" if not bad else "  -> " + ", ".join(bad)))
        ok = ok and not bad
    print("ALL GOOD" if ok else "SOME CHECKS FAILED")
    return ok

def cmd_clean():
    removed = []
    for g in TEMP_GLOBS:
        for p in glob.glob(os.path.join(ROOT, g)):
            os.remove(p); removed.append(os.path.basename(p))
    print("Removed temp files: " + (", ".join(removed) if removed else "none"))

def cmd_finish():
    print("== build ==")
    subprocess.run([sys.executable, "build.py"], cwd=ROOT, check=True)
    print("\n== og cards ==")
    subprocess.run([sys.executable, "make_og_images.py", "generate"], cwd=ROOT, check=True)
    print("\n== sitemap ==")
    cmd_sitemap_sync()
    print("\n== verify ==")
    ok = cmd_verify()
    print("\n== clean ==")
    cmd_clean()
    print("\nReady. NOT deployed (Joseph deploys). From a Windows terminal:")
    print("  cd C:\\Website && npx wrangler deploy")
    print("Then: python checkpoint.py")
    sys.exit(0 if ok else 1)

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    c = a[0]
    if c == "list": cmd_list()
    elif c == "hero-sheet": cmd_hero_sheet(a[1], a[2] if len(a) > 2 else None)
    elif c == "hero": cmd_hero(a[1])
    elif c == "sitemap": cmd_sitemap_sync()
    elif c == "verify": cmd_verify(a[1:] or None)
    elif c == "clean": cmd_clean()
    elif c == "finish": cmd_finish()
    else: print(f"Unknown subcommand: {c}\n"); print(__doc__)

if __name__ == "__main__":
    main()
