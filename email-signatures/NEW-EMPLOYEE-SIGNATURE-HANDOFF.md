# New-Employee Email Signature — Complete Handoff

Everything needed to add (or update) a JJA email-signature banner and get it onto
someone's Gmail. Built to be repeated easily for years. _Last updated: 2026-06-16._

---

## ⭐ The easy way (do this)

You don't have to touch any code. Open this project in **Cowork** and just say what
you need in plain language. Examples that work:

- **New employee:**
  > "Make an email signature for **Jane Smith**, **Jane@jjainsurance.com**, title **Account Manager**. Then publish and draft her setup email."
- **Change someone's title:**
  > "Update **Bryan Newman**'s signature title to **Commercial Director**."
- **New award year:**
  > "Update the award badge on all signatures to **2026**." (drop the new `award-2026.png` into `assets/img` first — see §4)
- **Just need the link:**
  > "Give me the URL for **David**'s signature."

Cowork will: generate the banner, drop in the current award badge, save it to the
site, give you the public URL, and (if asked) draft the Gmail setup email cc'd to you.
Everything below is the manual version of those same steps, in case you want it.

---

## 1. What you get & where it lives

- One JPG per person, 1440×720, e.g. `Rachel-email-sig.jpg`.
- Saved in **two** places (both are part of the live site):
  - `C:\Website\assets\img\`
  - `C:\Website\wp-content\uploads\sites\38\2026\03\`
- Public URL after publishing: `https://www.jjainsurance.com/assets/img/<First>-email-sig.jpg`
- The kit (this folder, `C:\Website\email-signatures\`): `make_sig.py` (generator),
  `signature-smallprint.txt` (the disclaimer), the template files, and this handoff.

---

## 2. Make the signature

**Easiest:** ask Cowork (see top). **Manual:**

1. Edit the `PEOPLE` list in `make_sig.py` — add `(Full Name, email, title, template, output_filename)`.
   - `template` = `TEMPLATE_STD` (office-building background, used for everyone) or
     `TEMPLATE_BRYAN` (football background — Bryan only).
   - To **update** an existing person, keep their existing `output_filename` so the URL stays the same.
2. Run `python make_sig.py` (needs Pillow + opencv-python; uses Arial Narrow + Arial on
   Windows). Output JPG lands in this folder.
3. Copy the JPG into BOTH `..\assets\img\` and `..\wp-content\uploads\sites\38\2026\03\`.

Calibration baked into `make_sig.py` (so it matches the original art): name = Arial
Narrow navy, left-aligned at x78 / baseline 270, auto-shrinks to clear the badges;
email = Arial 23, centered; old text removed by inpainting.

---

## 3. Publish (make the URL live)

The site is the Cloudflare **Worker** `jjainsurance` (assets-only). In **Command Prompt**
(not PowerShell):

```
cd C:\Website
npx wrangler deploy
```

Everything in `C:\Website` goes live; `.assetsignore` keeps scripts/docs/this kit out of
the public site. (Drag-and-drop upload in the Cloudflare dashboard also works.)

> URLs that already existed (e.g. a retitled person) update **in place** — same link.
> Gmail caches images, so a changed image may need a re-insert or a little time to refresh.

---

## 4. Update the award year (once a year)

The badge is the real award artwork, swapped in cleanly — no risky pixel editing.

1. Save the new year's badge art into `assets/img` as **`award-<YEAR>.png`**
   (same shield+ribbon+medal layout as `award-2025.png`, white background, 750×1445 is ideal).
2. Ask Cowork: *"Swap the award badge on all signatures to `award-<YEAR>.png`."*
   It template-matches the old badge's spot (~x857,y66, scaled) and composites the new one
   over it on every sig, leaving the six small history badges alone.
3. Publish (§3).

(Optional, fiddlier: bump the six small history badges up a year too — ask for it as a
separate step.)

---

## 5. Send the setup email

Ask Cowork: *"Draft the signature setup emails for [names], cc me."* It creates Gmail
**drafts** (cc `jacobs31@jjainsurance.com`) you review and send. Manual template below —
replace **[FIRST]** and **[URL]**; the small print is in `signature-smallprint.txt`.

---
**Subject:** Your new email signature — 2-minute setup

Hi **[FIRST]**,

Here's your new email signature and how to add it in Gmail. It takes about two minutes.

**Your signature image:** **[URL]**

Steps:
1. In Gmail, click the gear icon → See all settings → General tab.
2. Scroll to Signature → Create new (name it "JJA"), or edit your existing one.
3. Click the Insert image icon → choose Web address (URL) → paste the link above → Select.
4. Click the image once, then choose **Medium** from the size options (Small / Medium / Large / Original) so it fits the email width correctly.
5. Click below the image, press Enter, and paste the small print (below). Select it and set the font size to **Small**.
6. Under Signature defaults, set this signature for new emails and replies/forwards.
7. Click Save changes.

Small print — paste under the image: *(from `signature-smallprint.txt` — the three blocks:
CONFIDENTIALITY NOTICE / NO BINDING AUTHORITY / SECURITY & PRIVACY)*

Thanks,
Joseph

---

## 6. Roster (done so far)

| Name | Title | Email | File | Background |
|---|---|---|---|---|
| Ron Waters | Licensed Insurance agent | Ron@jjainsurance.com | Rons-email-sig.jpg | building |
| Bryan Newman | Commercial Director | BNewman@jjainsurance.com | Bryan-sig-file-2.jpg | football |
| Celia Brayman | Licensed Insurance agent | Celia@jjainsurance.com | Celia-email-sig.jpg | building |
| Carrie Austin | Licensed Insurance agent | Carrie@jjainsurance.com | Carrie-email-sig.jpg | building |
| Patti Davis | Licensed Insurance agent | Patti@jjainsurance.com | Patti-email-sig.jpg | building |
| Michele Stanifer | Licensed Insurance agent | MStanifer@jjainsurance.com | Michele-email-sig.jpg | building |
| Rachel Glover | Senior Account Manager | Rachel@jjainsurance.com | Rachel-email-sig.jpg | building |
| David Schmidlin | Licensed Commercial Producer | David@jjainsurance.com | David-email-sig.jpg | building |
| Jill | (existing) | — | Jill-email-sig.jpg | building |

All currently show the **2025** Best of the Best award. Generic banner: `image-4.jpg`.

---

## 7. Gotchas

- Verify each email address before the person pastes the URL into Gmail (one was given
  once as `.con` instead of `.com`).
- Publish (§3) **before** sending setup emails, so the image URLs resolve.
- Names auto-shrink to fit; very long name+title combos get a slightly smaller font — normal.
- Keep using `assets/img` + the `wp-content` shim path so existing links never break.
