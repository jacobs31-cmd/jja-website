#!/usr/bin/env python3
"""
Swap the featured award badge on every JJA signature.
Usage:  python3 swap_award.py award-2026.png
Composites assets/img/<new badge> over the old center shield+medal on all banners
(in assets/img + wp-content). Leaves the six small history badges as-is.
"""
import sys, os, glob, numpy as np, cv2
from PIL import Image

def find_website():
    for c in [r"C:\Website"] + glob.glob("/sessions/*/mnt/Website") + ["/mnt/Website"]:
        if os.path.isdir(os.path.join(c, "assets", "img")): return c
    raise SystemExit("Could not locate the Website folder.")
WEB = find_website()
IMG = os.path.join(WEB, "assets", "img")
WP  = os.path.join(WEB, "wp-content", "uploads", "sites", "38", "2026", "03")

if len(sys.argv) < 2:
    raise SystemExit("Usage: python3 swap_award.py award-<YEAR>.png")
new_badge = os.path.join(IMG, sys.argv[1])
# locate the old badge box by matching the previous year's art if present, else fixed box
X, Y, TW, TH = 857, 66, 229, 441   # known location/scale for this layout
prev = sorted(glob.glob(os.path.join(IMG, "award-*.png")))
arr = np.array(Image.open(new_badge).convert("RGB").resize((TW, TH)))
white = (arr[:,:,0]>236)&(arr[:,:,1]>236)&(arr[:,:,2]>236)
n, lab = cv2.connectedComponents(white.astype(np.uint8))
bl = set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1])
bg = np.isin(lab, list(bl)) & white
alpha = cv2.erode(np.where(bg,0,255).astype(np.uint8), np.ones((2,2),np.uint8))
a = (alpha/255.0)[...,None]

targets = [f for f in os.listdir(IMG)
           if (f.endswith("-email-sig.jpg") or f in ("image-4.jpg","Rons-email-sig.jpg","Bryan-sig-file-2.jpg"))]
for f in targets:
    out = cv2.cvtColor(cv2.imread(os.path.join(IMG,f)), cv2.COLOR_BGR2RGB).copy()
    roi = out[Y:Y+TH, X:X+TW].astype(float)
    out[Y:Y+TH, X:X+TW] = (arr*a + roi*(1-a)).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(IMG,f), quality=95)
    if os.path.isdir(WP): Image.fromarray(out).save(os.path.join(WP,f), quality=95)
    print("updated", f)
print("Done. Publish the site to go live.")
