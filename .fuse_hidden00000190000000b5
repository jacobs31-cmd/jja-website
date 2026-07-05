#!/usr/bin/env python3
r"""
JJA Website — Handoff auto-updater.

What it does (all mechanical, no AI, safe to re-run):
  1. Reads the live site files and extracts the volatile facts that tend to drift
     (worker/form URLs, Turnstile sitekey, cache-bust versions, page list, blog &
     team counts, which social/build scripts exist, SEO files present).
  2. Scans for DEPRECATED strings (Formspree, OneDrive, etc.) outside _archive and
     warns if any reappear in live files.
  3. Rewrites ONLY the text between <!-- AUTO:STATE --> and <!-- /AUTO:STATE --> in
     PROJECT-HANDOFF.md. Your hand-written prose is never touched.
  4. Archives any file in STALE_DOCS that still sits at the site root (date-stamped).
  5. Mirrors PROJECT-HANDOFF.md -> PROJECT-CONTEXT.md (the Project-Instructions paste
     source) so the two never drift.

Run from the site folder:   python3 update_handoff.py
Preview without writing:    python3 update_handoff.py --dry-run

The script roots itself at its own folder, so it works on Windows (C:\Website) or in
any synced copy without editing paths.
"""

import re
import sys
import shutil
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
TODAY = date.today().isoformat()
DRY_RUN = "--dry-run" in sys.argv

HANDOFF = BASE / "PROJECT-HANDOFF.md"
CONTEXT = BASE / "PROJECT-CONTEXT.md"
ARCHIVE = BASE / "_archive"

# ── CONFIG ──────────────────────────────────────────────────────────────────
# Files considered superseded. If one is still at the root, it gets moved to
# _archive/ with a date suffix. Already-archived files are skipped automatically.
STALE_DOCS = [
    "HANDOFF-NOTES.md",
    "README.md",
    "SETUP-GUIDE.md",
]

# Strings that must NOT appear in live (non-archive) files. The script warns if they
# do — it never deletes code. "Live" deprecated refs usually mean a regression.
DEPRECATED_STRINGS = ["formspree", "xnjweggp", "onedrive"]

# Files the deprecated-scan should ignore: the handoff docs (which legitimately
# *mention* the deprecated terms in a "do not reintroduce" context), this script,
# and the legacy build scripts kept for reference only — their stale Formspree refs
# are expected and don't represent a live regression.
SCAN_IGNORE = {
    "PROJECT-HANDOFF.md", "PROJECT-CONTEXT.md", "update_handoff.py",
    "_pages.py", "_build.py", "_build_blog.py", "_build_blog_new.py",
}

# Top-level page sections to report (presence check).
KNOWN_SECTIONS = [
    "about", "team", "carriers", "reviews", "faq", "personal", "business",
    "service", "billing-claims", "blog", "quotes", "contact",
    "privacy-policy", "accessibility",
]
# ────────────────────────────────────────────────────────────────────────────


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def grep_first(pattern: str, text: str, default="(not found)"):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else default


def cache_bust_versions():
    """Tally ?v=... strings on styles.css across all HTML files."""
    counts = {}
    for html in BASE.rglob("*.html"):
        if "_archive" in html.parts:
            continue
        for m in re.finditer(r"styles\.css\?v=([0-9a-z]+)", read(html)):
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))


def count_blog_posts():
    bdir = BASE / "blog"
    if not bdir.is_dir():
        return 0, 0
    published = sum(1 for d in bdir.iterdir() if d.is_dir() and (d / "index.html").exists())
    md_sources = len(list((BASE / "content" / "blog").glob("*.md")))
    return published, md_sources


def count_team_cards():
    return read(BASE / "team" / "index.html").count("team-card")


def scan_deprecated():
    """Return list of (relpath, term) for deprecated strings found in live files."""
    hits = []
    exts = {".html", ".js", ".css", ".txt", ".py"}
    for p in BASE.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if "_archive" in p.parts or p.name in SCAN_IGNORE:
            continue
        low = read(p).lower()
        for term in DEPRECATED_STRINGS:
            if term in low:
                hits.append((p.relative_to(BASE).as_posix(), term))
    return hits


def present(*names):
    return [n for n in names if (BASE / n).exists()]


def signature_banners():
    """List agent email-signature banners in assets/img and check the generator
    + the mirror folder, so the handoff's signature roster stays current."""
    img = BASE / "assets" / "img"
    agents = []
    if img.is_dir():
        for p in sorted(img.glob("*-email-sig.jpg")):
            name = p.name[:-len("-email-sig.jpg")]
            if name.lower() != "rons":          # Rons-email-sig.jpg is the template
                agents.append(name)
    has_generator = (BASE / "make_sig.py").exists()
    mirror = BASE / "wp-content" / "uploads" / "sites" / "38" / "2026" / "03"
    mirrored = sorted(p.name for p in mirror.glob("*-email-sig.jpg")) if mirror.is_dir() else []
    return agents, has_generator, len(mirrored)


def build_state_block():
    quotes_html = read(BASE / "quotes" / "index.html")
    contact_html = read(BASE / "contact" / "index.html")

    quote_action = grep_first(r'action="(https://[^"]*workers\.dev[^"]*)"', quotes_html)
    contact_action = grep_first(r'action="(https://[^"]*workers\.dev[^"]*)"', contact_html)
    sitekey = grep_first(r'data-sitekey="([^"]+)"', contact_html or quotes_html)

    versions = cache_bust_versions()
    ver_line = ", ".join(f"`{v}` ({n})" for v, n in versions.items()) or "(none found)"

    published, md_sources = count_blog_posts()
    team_n = count_team_cards()
    sections_present = [s for s in KNOWN_SECTIONS if (BASE / s).is_dir()]
    sections_missing = [s for s in KNOWN_SECTIONS if not (BASE / s).is_dir()]

    cities = sorted(
        d.name for d in BASE.iterdir()
        if d.is_dir() and d.name.endswith("-insurance")
    )

    social_scripts = present(
        "schedule_to_buffer.py", "schedule_instagram.py", "check_instagram.py",
        "add_images_to_buffer.py", "create_social_images.py",
    )
    social_imgs = len(list((BASE / "social-images").glob("*.png"))) if (BASE / "social-images").is_dir() else 0
    seo_files = present("llms.txt", "sitemap.xml", "robots.txt", "_headers")
    build_canonical = "build.py" if (BASE / "build.py").exists() else "(missing!)"

    dep = scan_deprecated()
    if dep:
        dep_line = "**WARNING — deprecated strings found in live files:** " + "; ".join(
            f"`{term}` in `{rel}`" for rel, term in dep
        )
    else:
        dep_line = "No deprecated strings (Formspree / OneDrive / etc.) found in live files. Clean."

    lines = [
        f"_Generated {TODAY} by `update_handoff.py`._",
        "",
        f"- **Quote form posts to:** `{quote_action}`",
        f"- **Contact form posts to:** `{contact_action}`",
        f"- **Turnstile sitekey:** `{sitekey}`",
        f"- **Cache-bust versions in use (styles.css):** {ver_line}",
        f"- **Published blog posts:** {published}  ·  **markdown sources in content/blog:** {md_sources}",
        f"- **Team cards:** {team_n}",
        f"- **Canonical blog builder:** `{build_canonical}`",
        f"- **City landing pages ({len(cities)}):** {', '.join(cities) if cities else '(none)'}",
        f"- **Core sections present:** {', '.join(sections_present)}",
    ]
    if sections_missing:
        lines.append(f"- **Core sections MISSING:** {', '.join(sections_missing)}")
    sig_agents, sig_gen, sig_mirrored = signature_banners()
    sig_line = (
        f"- **Agent email-signature banners ({len(sig_agents)}):** "
        f"{', '.join(sig_agents) if sig_agents else '(none)'} "
        f"(generator `make_sig.py` {'present' if sig_gen else 'MISSING'}; "
        f"{sig_mirrored} mirrored to wp-content/.../2026/03)"
    )
    lines += [
        f"- **Social scripts present:** {', '.join(social_scripts) if social_scripts else '(none)'}",
        f"- **Branded social images:** {social_imgs} PNG(s) in social-images/",
        f"- **SEO/AEO files present:** {', '.join(seo_files) if seo_files else '(none)'}",
        sig_line,
        "",
        dep_line,
    ]
    return "\n".join(lines)


def update_markers(text: str, block: str) -> str:
    pattern = re.compile(r"(<!-- AUTO:STATE -->)(.*?)(<!-- /AUTO:STATE -->)", re.DOTALL)
    if not pattern.search(text):
        print("  ! AUTO:STATE markers not found in PROJECT-HANDOFF.md — skipping injection.")
        return text
    return pattern.sub(lambda m: f"{m.group(1)}\n{block}\n{m.group(3)}", text)


def archive_stale():
    moved = []
    if not any((BASE / n).exists() for n in STALE_DOCS):
        return moved
    if not DRY_RUN:
        ARCHIVE.mkdir(exist_ok=True)
    for name in STALE_DOCS:
        src = BASE / name
        if src.exists():
            stem, suf = src.stem, src.suffix
            dest = ARCHIVE / f"{stem}.archived-{TODAY}{suf}"
            print(f"  archive: {name} -> _archive/{dest.name}")
            if not DRY_RUN:
                shutil.move(str(src), str(dest))
            moved.append(name)
    return moved


def main():
    if not HANDOFF.exists():
        sys.exit("PROJECT-HANDOFF.md not found — run this from the site folder.")

    mode = " (DRY RUN — no files written)" if DRY_RUN else ""
    print(f"JJA handoff updater{mode}\n")

    print("1. Extracting live state...")
    block = build_state_block()
    print("\n--- state snapshot ---")
    print(block)
    print("--- end snapshot ---\n")

    print("2. Updating PROJECT-HANDOFF.md AUTO:STATE region...")
    new_text = update_markers(read(HANDOFF), block)
    if not DRY_RUN:
        HANDOFF.write_text(new_text, encoding="utf-8")
    print("   done.")

    print("3. Archiving stale docs...")
    moved = archive_stale()
    if not moved:
        print("   nothing to archive (root is already clean).")

    print("4. Mirroring -> PROJECT-CONTEXT.md...")
    if not DRY_RUN:
        CONTEXT.write_text(new_text, encoding="utf-8")
    print("   done.\n")

    print("Finished." + (" (dry run — re-run without --dry-run to apply)" if DRY_RUN else ""))


if __name__ == "__main__":
    main()
