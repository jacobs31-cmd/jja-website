---
name: jja-email-signatures
description: Create, update, and publish J. Jacobs & Associates email-signature banners for employees, and draft the Gmail setup email. Use whenever Joseph wants a NEW employee email signature, wants to CHANGE someone's title on their signature, wants to UPDATE the award year across the signatures, or asks for an employee's signature image URL. Trigger on phrases like "make an email signature for [name]", "new employee signature", "add a sig for [name]", "update [name] signature title", "swap the award badge to [year]", or "give me the URL for [name] signature". JJA-specific (the wide J.Jacobs banner with awards and carriers that staff use in Gmail).
---

# JJA Email Signature Banners

Produces a per-employee version of the JJA banner: the navy **INSURANCE** band is
replaced with "**[Full Name] - [Title]**" and the email line becomes their address.
Everything else (logo, awards, carriers, address, phone, disclaimer) is preserved.

## Inputs to collect (ask only if missing)
- **Full name**, **email address**, **title** (e.g. "Licensed Insurance agent",
  "Senior Account Manager", "Commercial Director", "Licensed Commercial Producer").
- Confirm the title wording — it is NOT always "Licensed Insurance agent".
- Verify the email address spelling (a past one was given as `.con` instead of `.com`).

## Files (in the user's Website folder)
- Templates: `assets/img/Rons-email-sig.jpg` (office-building bg — default for everyone)
  and `assets/img/Bryan-sig-file-2.jpg` (football bg — Bryan only). Both already carry the
  current **2025** award badge.
- Generator: `make_sig.py` (bundled in this skill; resolves the Website folder automatically).
- Small print: `signature-smallprint.txt` (bundled) — the 3 disclaimer blocks.
- Award art per year: `assets/img/award-YEAR.png` (e.g. `award-2026.png`, 750x1445, white bg).

## A. Make / update a signature
1. Run the bundled generator in the Cowork bash sandbox. Per person (quote each argument):
   `python3 SKILL_DIR/make_sig.py "Full Name" "email@jjainsurance.com" "Title"`
   - Add the literal word `bryan` as a 4th argument ONLY for Bryan Newman (uses his football
     template and writes `Bryan-sig-file-2.jpg`).
   - It writes `First-email-sig.jpg` to BOTH `assets/img/` and
     `wp-content/uploads/sites/38/2026/03/`, and prints the public URL.
   - To **update** an existing person (e.g. title change), pass the same name so the same
     filename/URL is reused.
2. Show the result image to the user to confirm it looks right (name fits, email centered,
   no leftover text). Names auto-shrink to clear the award badges — that is expected.

## B. Update the award year (yearly)
1. Make sure `assets/img/award-YEAR.png` for the new year exists (same shield+ribbon+medal
   layout, white background). If not, ask the user to drop it in.
2. Composite it over the old badge on every signature with the bundled helper:
   `python3 SKILL_DIR/swap_award.py award-2026.png`  (use the actual new filename)
   It cuts the white background and composites the new badge onto every `*-email-sig.jpg`,
   `image-4.jpg`, `Rons-email-sig.jpg`, and `Bryan-sig-file-2.jpg` in `assets/img/`, and
   mirrors to `wp-content`. The six small history badges are left as-is.
3. Show a couple of results to confirm a clean swap.

## C. Publish (make URLs live)
The site is the assets-only Cloudflare Worker `jjainsurance`. Tell the user to run, in
**Command Prompt**:
`cd C:\Website`  then  `npx wrangler deploy`
(or drag-and-drop the `C:\Website` folder in the Cloudflare dashboard). Do NOT run deploy
from the sandbox. Existing URLs update in place; Gmail caches images so a changed one may
need re-inserting.

## D. Draft the setup email (optional, if asked)
Use the Gmail `create_draft` connector. One draft per person, **cc `jacobs31@jjainsurance.com`**.
Subject: "Your new email signature — 2-minute setup". Body = the template in
`EMAIL-TEMPLATE.md` with the FIRST name and URL filled in, plus the small print from
`signature-smallprint.txt`. Create as DRAFTS for the user to review/send (do not auto-send
unless told). Remind the user to publish (step C) before the emails go out.

## Notes
- Calibration lives in `make_sig.py` (Arial Narrow navy name, left x78/baseline 270,
  auto-shrink; Arial 23 centered email; old text removed by OpenCV inpaint). Don't change it.
- Keep saving to BOTH `assets/img/` and `wp-content/uploads/sites/38/2026/03/` so existing
  links never break.
- Full background/handoff: `C:\Website\email-signatures\NEW-EMPLOYEE-SIGNATURE-HANDOFF.md`.
