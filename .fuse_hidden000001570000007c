#!/usr/bin/env python3
r"""
JJA Insurance — Create Branded Social Media Images
Downloads real photos from Pexels and overlays JJA navy/gray branding.
Output: 1080x1080 PNG files saved to C:\Website\social-images\

Run: python create_social_images.py
Requires: pip install Pillow
"""

import os, sys, urllib.request, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── OUTPUT PATH ───────────────────────────────────────────────────────────────
OUTPUT_DIR = r"C:\Website\social-images"

# ── JJA BRAND COLORS — pulled directly from jjainsurance.com CSS ─────────────
NAVY       = (20,  54,  94)    # --navy:       #14365e  (primary)
NAVY_DARK  = (10,  35,  66)    # --navy-dark:  #0a2342  (darkest, for gradient)
NAVY_LIGHT = (30,  74, 122)    # --navy-light: #1e4a7a  (accent line)
WHITE      = (255, 255, 255)   # --white
GRAY_TEXT  = (196, 203, 214)   # #c4cbd6  (light text used on dark sections)
GRAY_URL   = (183, 192, 207)   # #b7c0cf  (secondary text on dark)
BLACK      = (0,   0,   0)

# ── REAL PEXELS PHOTOS — one per category ─────────────────────────────────────
# Direct Pexels image URLs (free to use under Pexels license)
IMAGES = [
    {
        "filename": "jja_home_insurance.png",
        "label":    "HOME INSURANCE",
        "tagline":  "Protecting Michigan Homeowners",
        # Beautiful suburban home exterior — white house, green lawn
        "url": "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
    {
        "filename": "jja_auto_insurance.png",
        "label":    "AUTO INSURANCE",
        "tagline":  "Michigan's #1 Independent Agency",
        # Family with car, parked in driveway
        "url": "https://images.pexels.com/photos/36833508/pexels-photo-36833508/free-photo-of-family-driving-in-white-sedan-on-urban-street.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
    {
        "filename": "jja_commercial.png",
        "label":    "COMMERCIAL INSURANCE",
        "tagline":  "Protecting Michigan Businesses",
        # Small business owner smiling in their shop
        "url": "https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
    {
        "filename": "jja_workers_comp.png",
        "label":    "WORKERS' COMPENSATION",
        "tagline":  "Coverage for Your Team",
        # Construction worker with hard hat on job site
        "url": "https://images.pexels.com/photos/1216589/pexels-photo-1216589.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
    {
        "filename": "jja_life_insurance.png",
        "label":    "LIFE INSURANCE",
        "tagline":  "Securing Your Family's Future",
        # Happy family outdoors together
        "url": "https://images.pexels.com/photos/1128318/pexels-photo-1128318.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
    {
        "filename": "jja_insurance_tips.png",
        "label":    "INSURANCE TIPS",
        "tagline":  "45 Years of Michigan Expertise",
        # Professional agent/advisor sitting across desk from client
        "url": "https://images.pexels.com/photos/3760263/pexels-photo-3760263.jpeg?auto=compress&cs=tinysrgb&w=1280&h=1280&fit=crop",
    },
]

SIZE = 1080

def download_image(url):
    """Download a photo from Pexels and return a PIL Image."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")

def smart_crop(img, size=SIZE):
    """Resize and center-crop to a square."""
    w, h = img.size
    scale = size / min(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - size) // 2
    top  = (new_h - size) // 2
    return img.crop((left, top, left + size, top + size))

def get_font(size, bold=False):
    """Try to load a system font, fall back to PIL default."""
    font_paths = [
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\arialbd.ttf"  if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\verdanab.ttf" if bold else r"C:\Windows\Fonts\verdana.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def add_branding(img, label, tagline):
    """Overlay JJA navy/gray branded bar. Colors from jjainsurance.com CSS."""
    draw = ImageDraw.Draw(img, "RGBA")

    # Dark gradient fade into navy (bottom 420px → 195px solid bar)
    grad_top    = SIZE - 420
    grad_bottom = SIZE - 195
    for y in range(grad_top, grad_bottom):
        progress = (y - grad_top) / (grad_bottom - grad_top)
        alpha = int(210 * (progress ** 1.5))
        draw.line([(0, y), (SIZE, y)], fill=(*NAVY_DARK, alpha))

    # Solid navy bar (bottom 195px)
    bar_top = SIZE - 195
    draw.rectangle([(0, bar_top), (SIZE, SIZE)], fill=(*NAVY, 255))

    # Navy-light accent line at top of bar
    draw.rectangle([(0, bar_top), (SIZE, bar_top + 4)], fill=(*NAVY_LIGHT, 255))

    y_base = bar_top + 18

    # Agency name — light gray, regular
    font_jja = get_font(19, bold=False)
    draw.text((44, y_base), "J. JACOBS & ASSOCIATES INSURANCE", font=font_jja, fill=GRAY_TEXT)

    # Category label — white, bold, large
    font_cat = get_font(36, bold=True)
    draw.text((44, y_base + 32), label, font=font_cat, fill=WHITE)

    # Tagline — light gray
    font_tag = get_font(21, bold=False)
    draw.text((44, y_base + 80), tagline, font=font_tag, fill=GRAY_TEXT)

    # Website + phone — gray, right-aligned
    font_url = get_font(17, bold=False)
    url_text = "jjainsurance.com  |  (248) 693-6455"
    bbox = draw.textbbox((0, 0), url_text, font=font_url)
    url_w = bbox[2] - bbox[0]
    draw.text((SIZE - url_w - 44, y_base + 84), url_text, font=font_url, fill=GRAY_URL)

    # Thin navy-light strip at very bottom
    draw.rectangle([(0, SIZE - 5), (SIZE, SIZE)], fill=(*NAVY_LIGHT, 255))

    return img

def build_image(cfg):
    filename = cfg["filename"]
    label    = cfg["label"]
    tagline  = cfg["tagline"]
    url      = cfg["url"]

    print(f"\n  Downloading photo for {filename}...")
    try:
        raw = download_image(url)
    except Exception as e:
        print(f"  ERROR downloading: {e}")
        return False

    print(f"  Processing ({raw.size[0]}x{raw.size[1]}) → 1080x1080...")
    img = smart_crop(raw)
    img = add_branding(img, label, tagline)

    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, "PNG", optimize=True)
    print(f"  Saved → {out_path}")
    return True

def main():
    print("\n" + "="*60)
    print("  JJA Insurance — Social Media Image Creator")
    print("  Real Pexels photos + JJA navy/gray branded overlay")
    print("="*60)

    if not os.path.isdir(OUTPUT_DIR):
        print(f"\nERROR: Output folder not found: {OUTPUT_DIR}")
        sys.exit(1)

    ok = fail = 0
    for cfg in IMAGES:
        if build_image(cfg):
            ok += 1
        else:
            fail += 1

    print(f"\n{'='*60}")
    print(f"  Done! Created: {ok}  |  Failed: {fail}")
    print(f"  Files saved to: {OUTPUT_DIR}")
    if ok > 0:
        print(f"\n  Next: Deploy Cloudflare Pages — Buffer picks up new")
        print(f"  images automatically, no changes to Buffer needed.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
