# JJA Insurance — Session Handoff Notes
**Date:** 2026-05-18  
**Prepared for:** Next Claude session (other computer)

---

## What This Project Is

JJA Insurance (jjainsurance.com) has a quote form on their website. When a visitor submits a **Full Quote** (Auto or Home), two things happen simultaneously:
1. The form data goes to **Formspree** (emails the agency a readable summary)
2. The form data goes to a **Cloudflare Worker** that generates an **ACORD AL3 file** and emails it to Support@jjainsurance.com so staff can import it directly into **PL Rater** (Vertafore) without re-keying data

---

## Folder Structure

| Folder | What it is |
|--------|-----------|
| `C:\Website` | The live website — working well, do not break the quote forms |
| `C:\worker` | The Cloudflare Worker code — this is what gets deployed |
| `C:\Worker 2` | Copy from the other computer — now synced with C:\worker |
| `C:\Website 2` | Copy of website from the other computer — needs comparison/merge |

---

## What Was Done Today (2026-05-18)

### 1. Contact Form — Spam Honeypot ✅ DONE
- Added `<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">` to `C:\Website\contact\index.html`
- This stops spam bots from submitting the contact form
- Already saved to the file — just needs to be deployed to the live site

### 2. AL3 Worker — Fixed and Deployed ✅ DONE
The worker was generating AL3 files that failed to import into PL Rater with error:
> `Failed to Import Transaction. Tag=2 Error='[instanceKey] cannot be an empty string'`

**Root cause found:** The previous Claude session on the other computer "fixed" segment sizes based on what it thought was a PL Rater export. But those sizes were wrong — they didn't match the Hawksoft working export that actually imports successfully. Also, the `?` character in the TRG segment was caused by **trailing null bytes in the file itself** (not the code), which were corrupting that position.

**What was fixed in `C:\worker\al3-worker.js`:**

| Segment | Old (broken) size | New (correct) size | Source |
|---------|------------------|--------------------|--------|
| MHG | 176 | 196 | Matched Hawksoft working export |
| TRG | 212 | 212 | Same size, but removed `?` / null corruption |
| ACI | 200 | 249 | Matched Hawksoft |
| BIS addr (9BIS) | 340 | 343 | Matched Hawksoft |
| ISI | 183 | 275 | Matched Hawksoft |
| BPI | 511 | 511 | Already correct (not changed) |
| LAG | 259 | 636 | Matched Hawksoft (restored dual address block) |

VEH and DRV segments (auto-specific) were **kept from the newer version** — they have better field definitions (OT vehicle type, MI92 state marker, 33-char license number).

**Deployed successfully** via `npx wrangler deploy` from `C:\worker`. Version ID: `5fa88fda-3a0e-400c-bdd0-f53feb839493`

---

## What Still Needs to Be Done

### 3. Test AL3 Import ⏳ NEEDS TESTING
- Submit a Full Quote on jjainsurance.com (Auto or Home)
- Wait for the email with the .al3 attachment
- Rename file to `PL.al3` if PL Rater can't find it otherwise
- Try importing in PL Rater: **File → Import → AL3**
- Confirm no `instanceKey` error

### 4. Website Folder Comparison ⏳ NOT STARTED
- Compare `C:\Website` vs `C:\Website 2` (copy from other computer)
- `C:\Website` is the working live site — **do not change the quote forms**
- Goal: make sure `C:\Website` has the most current version of everything
- `C:\Website 2` has duplicate `.docx` files everywhere (ignore those) and a `HOME_Regiec_FIXED_v2.al3` test file (ignore that too)
- Focus on `.html`, `.py`, `.js`, and `.css` files

---

## Key Technical Details

**Cloudflare Worker URL:** https://jja-al3-worker.jacobs31.workers.dev  
**Worker name:** jja-al3-worker  
**Deploy command:** `cd C:\worker && npx wrangler deploy`  
**Email service:** Resend (secrets set in Cloudflare dashboard)  
**Form email:** Formspree (form ID: xnjweggp)  
**AL3 recipient:** Support@jjainsurance.com  

**Important:** PL Rater requires the file to be named `PL.al3` to find it on import. The worker names files `AUTO_LastName_Date.al3` — staff need to rename to `PL.al3` before importing, or the import dialog won't find it.

**Reference file:** The Hawksoft export `PL.al3` (uploaded during this session) is the known-good working AL3 for a home quote. Use it as the reference for segment sizes if any further debugging is needed.

---

## Files the Other Claude Should Ask to Connect
- `C:\Website` — live website
- `C:\worker` — worker code  
- `C:\Worker 2` — other computer copy (for comparison)
- `C:\Website 2` — other computer website copy (for comparison)
