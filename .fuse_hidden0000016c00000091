#!/usr/bin/env python3
"""
JJA email-signature banner generator.
Recreated from README-SIGNATURES.md recipe.

Takes the Ron template (band already removed), removes the old name + email
text, and redraws each agent's name/email.

Edit PEOPLE, then run:  python make_sig.py
Outputs <Firstname>-email-sig.jpg next to this script.
"""
import os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "assets", "img", "Rons-email-sig.jpg")

# (Full Name, email, title)
PEOPLE = [
    ("Jill Stockwell", "Jstockwell@jjainsurance.com", "Director of Personal Lines"),
]

NAME_COLOR  = (31, 52, 85)    # navy, RGB
EMAIL_COLOR = (40, 44, 52)
NAME_X      = 78
NAME_BASE_Y = 273
NAME_X_MAX  = 773
NAME_SIZE   = 48
EMAIL_X      = 281
EMAIL_BASE_Y = 415
EMAIL_SIZE   = 23
EMAIL_RECT   = (273, 393, 603, 424)   # x0,y0,x1,y1 flat panel to clear


def find_font(candidates, size):
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise FileNotFoundError(str(candidates))

def narrow_font(size):
    return find_font([
        r"C:\Windows\Fonts\ARIALN.TTF",
        "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
    ], size)

def regular_font(size):
    return find_font([
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ], size)


def build_name_mask(img_bgr):
    b = img_bgr[:, :, 0].astype(int)
    g = img_bgr[:, :, 1].astype(int)
    r = img_bgr[:, :, 2].astype(int)
    navy = (r < 90) & (g < 90) & (b < 120) & (b >= r)
    mask = np.zeros(img_bgr.shape[:2], np.uint8)
    band = np.zeros_like(navy)
    band[230:290, 60:790] = True
    mask[navy & band] = 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    return mask

def clear_email_band(img_bgr):
    x0, y0, x1, y1 = EMAIL_RECT
    fill = np.median(img_bgr[426:432, x0:x1].reshape(-1, 3), axis=0)
    img_bgr[y0:y1, x0:x1] = fill
    return img_bgr

def fit_name_font(name_line):
    size = NAME_SIZE
    while size >= 30:
        f = narrow_font(size)
        if NAME_X + f.getbbox(name_line)[2] <= NAME_X_MAX:
            return f
        size -= 1
    return narrow_font(30)


def make_one(full_name, email, title):
    img = cv2.imread(TEMPLATE)
    if img is None:
        sys.exit("template not found: " + TEMPLATE)
    img = cv2.inpaint(img, build_name_mask(img), 3, cv2.INPAINT_TELEA)
    img = clear_email_band(img)

    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil)
    name_line = full_name + " - " + title
    draw.text((NAME_X, NAME_BASE_Y), name_line,
              font=fit_name_font(name_line), fill=NAME_COLOR, anchor="ls")
    draw.text((EMAIL_X, EMAIL_BASE_Y), "Email: " + email,
              font=regular_font(EMAIL_SIZE), fill=EMAIL_COLOR, anchor="ls")

    first = full_name.split()[0]
    out = os.path.join(HERE, first + "-email-sig.jpg")
    pil.save(out, "JPEG", quality=92)
    print("wrote", out)
    return out


if __name__ == "__main__":
    for person in PEOPLE:
        make_one(*person)
