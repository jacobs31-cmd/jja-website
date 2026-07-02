# Website dec-page options — APPLIED (deploy + test checklist)

Website quote requests now offer customers **three ways** to send their declarations
pages instead of only "reply to this email":
1. **Reply** to the acknowledgment email with a photo/scan.
2. **Text photos to (248) 241-9549** — include your name.
3. **Secure upload link** (private, 30-day expiry) in the email + SMS.

And **support@jjainsurance.com** is now CC'd when a website customer's dec pages arrive.

All code changes below are **already applied to source** and pass `node --check`. They
are **not deployed yet** — deploy commands are at the bottom (your call, per usual).

---

## ✅ Resolved: shared KV confirmed
Both `jja-al3-worker` and `jja-intake-worker` bind `QUOTE_HISTORY` to the **same**
namespace id `8c16859f8c8141fb923dcd83df10674d`. So the upload token the website worker
mints is readable by the upload page at `quotesheet.jjainsurance.com/upload`. The secure
link will work. No binding change needed.

## Phone-number map (corrected 2026-06-12)
| Number | What it is | Inbound texts go to |
|---|---|---|
| **(248) 241-9549** | **Twilio — Personal** (MMS) | `quotesheet.jjainsurance.com/sms-inbound` (personal intake worker) |
| (248) 927-2013 | Twilio — Commercial (MMS) | `commquote.jjainsurance.com/sms-inbound` (commercial worker) |
| (248) 690-5320 | Hawksoft text-in | Hawksoft directly — **uncategorized if no client match** (bad for brand-new web leads) |
| (248) 693-6455 | Office line | Forwards as SMS-to-email to the support inbox (manual) |

**Website text number = (248) 241-9549.** Website quote leads are written into the
**personal** pipeline (`q:…:WEB` in the shared `QUOTE_HISTORY` KV), so a photo texted to
241-9549 hits the personal `/sms-inbound`, matches the web lead **by phone in the
pipeline** (works for brand-new prospects — it's not matching against Hawksoft), saves to
the lead's 📥 docs, files to Hawksoft, notifies the owner, and **CCs support@** for web
leads. Commercial's 927-2013 would NOT match a website lead (different pipeline), so do
not use it here.

### Config prerequisites for the text channel (verify these)
1. **`jja-intake-worker` must have `TWILIO_SID` + `TWILIO_TOKEN` secrets set.** Without
   them, `/sms-inbound` silently no-ops (returns empty TwiML, no email) — the most likely
   reason an earlier test text produced nothing.
2. **`jja-al3-worker` `TWILIO_FROM` = `+12482419549`** so the outbound text-back comes
   from the same number customers reply to.
3. **A2P 10DLC registration.** The Twilio inventory shows messaging still flagged
   *"Complete registration"* on both numbers — finish that or carrier filtering can drop
   messages. (Inbound person→app texts usually still arrive, but don't assume.)
4. **Test before relying on it:** from a phone that just submitted a test quote, text a
   photo to 241-9549 → you should get a 📱 email to jacobs31@ (CC support@) and see the
   photo on that lead. No email = check #1 and #3.

---

## What changed (files)

**`C:\worker\al3-worker\al3-worker.js`** (the website quote worker)
- Added `dqToken()` helper.
- Mints a one-time `up:<token>` record in `QUOTE_HISTORY` for each web lead (keyed to the
  lead, `source:"web"`, 30-day TTL) → builds the secure upload link.
- `buildCustomerAckEmail()` now shows the "Three easy ways to send them" block with the
  text number and the **Upload Documents Securely** button (instead of the old
  reply-only paragraph + "how to find your dec pages" box).
- The instant SMS now includes the upload link + "text photos to (248) 241-9549, or reply."

**`C:\worker\intake-worker\intake-worker.js`** (Personal Lines intake)
- Upload "📥 documents received" alert now CCs `support@jjainsurance.com` for web leads
  (`rec.source === 'web'`).
- Inbound-text "📱 Customer text" alert now CCs `support@jjainsurance.com` for web leads
  (lead key contains `:WEB:`).
- Replies to the ack email already land in Support@jjainsurance.com (it's the From
  address), so the "email" channel needed no change.

**`C:\Website\quotes\index.html`** (the public site)
- Post-submit "Quote Request Received!" panel now lists the three options (emoji-free,
  per the site brand rules). The secure link is referenced as "in your email" since the
  page can't show a per-customer token.

> Not touched: `jja-commercial-worker`. Website quotes are personal-lines and flow through
> the personal intake worker. If you ever want commercial dec uploads to CC support@ too,
> the same one-line `cc:` edits apply there.

---

## Deploy (from a real Windows terminal — not the Drive-synced sandbox)

```
cd C:\worker\al3-worker      && npx wrangler deploy      # website quote worker
cd C:\worker\intake-worker   && npx wrangler deploy      # personal intake (support@ CC)
cd C:\Website                && npx wrangler deploy      # the site (confirmation panel)
```

## Test checklist
1. Submit a test quote on the site → confirmation panel shows the 3 options. ✅ (built)
2. Acknowledgment **email** → shows "Three easy ways," with a working **Upload Documents
   Securely** button.
3. Click the upload link → upload page loads (NOT "link expired").
4. Upload a test file → files to the lead **and support@ is CC'd** on the 📥 alert.
5. Text a photo to (248) 241-9549 (from a phone that submitted a test quote) → confirm it
   files to the lead and the 📱 alert CCs support@.
6. Reply to the ack email with an attachment → lands in Support@jjainsurance.com.
