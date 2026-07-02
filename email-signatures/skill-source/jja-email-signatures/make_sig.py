#!/usr/bin/env python3
"""
JJA email-signature generator (skill version).
Usage:  python3 make_sig.py "Full Name" "email@jjainsurance.com" "Title" [bryan]
Writes <First>-email-sig.jpg to the Website assets/img + wp-content shim, prints the URL.
Add the literal arg 'bryan' to use Bryan's football template + filename Bryan-sig-file-2.jpg.
"""
import sys, os, glob, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

def find_website():
    cands = [r"C:\Website"] + glob.glob("/sessions/*/mnt/Website") + ["/mnt/Website", os.path.expanduser("~/Website")]
    for c in cands:
        if os.path.isdir(os.path.join(c, "assets", "img")):
            return c
    raise SystemExit("Could not locate the Website folder (assets/img).")

WEB = find_website()
IMG = os.path.join(WEB, "assets", "img")
WP  = os.path.join(WEB, "wp-content", "uploads", "sites", "38", "2026", "03")

def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit("No suitable font found.")
NARROW = [r"C:\Windows\Fonts\ARIALN.TTF", "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf"]
REG    = [r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]

NAME_X, NAME_BASELINE, NAME_COLOR, NAME_MAXW, NAME_MAXSZ = 78, 270, (31,52,85), 775-78, 48
EMAIL_BASELINE, EMAIL_COLOR, EMAIL_SZ = 415, (40,44,52), 23
NAME_BOX, EMAIL_BOX = (76,230,790,285), (188,395,694,420)

def fit(paths, text, maxw, start):
    s = start
    while s > 18:
        f = font(paths, s)
        if f.getbbox(text)[2] <= maxw: return f
        s -= 1
    return font(paths, 18)

def build(base, name_line, email_line, out):
    im = Image.open(base).convert("RGB"); a = np.array(im)
    r,g,b = a[...,0].astype(int),a[...,1].astype(int),a[...,2].astype(int)
    dark = (r<120)&(g<120)&(b<178)&(r+g+b<440)
    ex0,ey0,ex1,ey1 = EMAIL_BOX
    cols = np.where(dark[ey0:ey1, ex0:ex1].any(axis=0))[0]
    ecx = (ex0+cols.min()+ex0+cols.max())//2 if len(cols) else 434
    mask = np.zeros(a.shape[:2], np.uint8)
    for (x0,y0,x1,y1) in (NAME_BOX, EMAIL_BOX):
        sub = np.zeros_like(dark); sub[y0:y1,x0:x1] = dark[y0:y1,x0:x1]; mask[sub]=255
    mask = cv2.dilate(mask, np.ones((5,5),np.uint8), iterations=2)
    bgr = cv2.inpaint(a[:,:,::-1].copy(), mask, 4, cv2.INPAINT_TELEA)
    im2 = Image.fromarray(bgr[:,:,::-1]); d = ImageDraw.Draw(im2)
    d.text((NAME_X,NAME_BASELINE), name_line, font=fit(NARROW,name_line,NAME_MAXW,NAME_MAXSZ),
           fill=NAME_COLOR, anchor="ls")
    d.text((ecx,EMAIL_BASELINE), email_line, font=font(REG,EMAIL_SZ), fill=EMAIL_COLOR, anchor="ms")
    im2.save(out, quality=95)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit('Usage: python3 make_sig.py "Full Name" "email" "Title" [bryan]')
    name, email, title = sys.argv[1], sys.argv[2], sys.argv[3]
    is_bryan = len(sys.argv) > 4 and sys.argv[4].lower() == "bryan"
    base = os.path.join(IMG, "Bryan-sig-file-2.jpg" if is_bryan else "Rons-email-sig.jpg")
    fn = "Bryan-sig-file-2.jpg" if is_bryan else name.split()[0] + "-email-sig.jpg"
    for d in (IMG, WP):
        os.makedirs(d, exist_ok=True)
        build(base, f"{name} - {title}", f"Email: {email}", os.path.join(d, fn))
    print("Saved:", fn)
    print("URL:  https://www.jjainsurance.com/assets/img/" + fn)
