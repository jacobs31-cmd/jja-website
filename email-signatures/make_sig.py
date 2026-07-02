#!/usr/bin/env python3
"""
JJA agent email-signature banner generator.
-------------------------------------------
Creates a per-agent signature banner by replacing only the agent name line and
the email line on a template. Everything else (logo, awards, carriers, address,
phone) is preserved.

HOW TO USE
  1. Edit the PEOPLE list below.
  2. Run:  python make_sig.py
  3. Output JPGs land in this folder. Copy each to BOTH:
        ..\\assets\\img\\
        ..\\wp-content\\uploads\\sites\\38\\2026\\03\\
     then publish the site (see README-SIGNATURES.md).

Requires Pillow + opencv-python(-headless), and either Arial Narrow + Arial
(Windows) or Liberation Sans Narrow + Liberation Sans (Linux). Fonts auto-located.

Easiest path: ask Claude in Cowork to "make an email signature for <Name>, <email>,
<title>" and it runs this for you.
"""
import os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

def _first(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("None exist:\n  " + "\n  ".join(paths))

# Default template = Ron's sig (office-building bg). Bryan uses his own (football bg).
TEMPLATE_STD = _first([os.path.join(HERE, "Rons-email-sig.jpg"),
                       os.path.join(HERE, "..", "assets", "img", "Rons-email-sig.jpg")])
TEMPLATE_BRYAN = _first([os.path.join(HERE, "Bryan-sig-file-2.jpg"),
                         os.path.join(HERE, "..", "assets", "img", "Bryan-sig-file-2.jpg")])
NARROW = _first([r"C:\Windows\Fonts\ARIALN.TTF",
                 "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf"])
REG = _first([r"C:\Windows\Fonts\arial.ttf",
              "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"])

# --- Calibrated layout (measured from the original Ron/Bryan sigs) ---
NAME_X, NAME_BASELINE = 78, 270          # name is LEFT-aligned at x=78
NAME_COLOR  = (31, 52, 85)               # brand navy
NAME_MAXW   = 775 - 78                    # keep clear of the award badges
NAME_MAXSZ  = 48                          # auto-shrinks for long name+title
EMAIL_BASELINE = 415                      # email line is CENTER-aligned (see EMAIL_BOX)
EMAIL_COLOR = (40, 44, 52)
EMAIL_SZ    = 23
NAME_BOX  = (76, 230, 790, 285)           # inpaint region for the old name
EMAIL_BOX = (188, 395, 694, 420)          # wide enough to cover any centered email line

def _fit(fp, text, maxw, start):
    sz = start
    while sz > 18:
        f = ImageFont.truetype(fp, sz)
        if f.getbbox(text)[2] <= maxw:
            return f, sz
        sz -= 1
    return ImageFont.truetype(fp, 18), 18

def build(name_line, email_line, out, base=TEMPLATE_STD):
    im = Image.open(base).convert("RGB"); a = np.array(im)
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    dark = (r < 120) & (g < 120) & (b < 178) & (r + g + b < 440)
    # measure the original email's horizontal center so the new one matches it
    ex0, ey0, ex1, ey1 = EMAIL_BOX
    cols = np.where(dark[ey0:ey1, ex0:ex1].any(axis=0))[0]
    ecx = (ex0 + cols.min() + ex0 + cols.max()) // 2 if len(cols) else 434
    mask = np.zeros(a.shape[:2], np.uint8)
    for (x0, y0, x1, y1) in (NAME_BOX, EMAIL_BOX):
        sub = np.zeros_like(dark); sub[y0:y1, x0:x1] = dark[y0:y1, x0:x1]; mask[sub] = 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    bgr = cv2.inpaint(a[:, :, ::-1].copy(), mask, 4, cv2.INPAINT_TELEA)
    im2 = Image.fromarray(bgr[:, :, ::-1]); d = ImageDraw.Draw(im2)
    nf, nsz = _fit(NARROW, name_line, NAME_MAXW, NAME_MAXSZ)
    d.text((NAME_X, NAME_BASELINE), name_line, font=nf, fill=NAME_COLOR, anchor="ls")
    ef = ImageFont.truetype(REG, EMAIL_SZ)
    d.text((ecx, EMAIL_BASELINE), email_line, font=ef, fill=EMAIL_COLOR, anchor="ms")
    im2.save(out, quality=95)
    print(f"  wrote {os.path.basename(out)}  (name size {nsz})")

# ------- EDIT THIS LIST, then run -------------------------------------------
# (Full Name, email, title, base_template, output_filename)
#   base_template: TEMPLATE_STD (office building) or TEMPLATE_BRYAN (football)
#   output_filename: keep an existing name to update that same URL
PEOPLE = [
    ("Celia Brayman",    "Celia@jjainsurance.com",     "Licensed Insurance agent",    TEMPLATE_STD,   "Celia-email-sig.jpg"),
    ("Carrie Austin",    "Carrie@jjainsurance.com",    "Licensed Insurance agent",    TEMPLATE_STD,   "Carrie-email-sig.jpg"),
    ("Patti Davis",      "Patti@jjainsurance.com",     "Licensed Insurance agent",    TEMPLATE_STD,   "Patti-email-sig.jpg"),
    ("Michele Stanifer", "MStanifer@jjainsurance.com", "Licensed Insurance agent",    TEMPLATE_STD,   "Michele-email-sig.jpg"),
    ("Rachel Glover",    "Rachel@jjainsurance.com",    "Senior Account Manager",      TEMPLATE_STD,   "Rachel-email-sig.jpg"),
    ("David Schmidlin",  "David@jjainsurance.com",     "Licensed Commercial Producer",TEMPLATE_STD,   "David-email-sig.jpg"),
    ("Bryan Newman",     "BNewman@jjainsurance.com",   "Commercial Director",         TEMPLATE_BRYAN, "Bryan-sig-file-2.jpg"),
]
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating signature banners...")
    for name, email, title, base, fn in PEOPLE:
        build(f"{name} - {title}", f"Email: {email}", os.path.join(HERE, fn), base=base)
    print("Done. Copy each JPG into ..\\assets\\img\\ and "
          "..\\wp-content\\uploads\\sites\\38\\2026\\03\\, then publish.")
