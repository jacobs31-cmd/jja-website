/**
 * J. Jacobs & Associates — Contact Form Worker
 *
 * Flow: Turnstile spam check → Resend email → redirect
 *
 * Required secrets (set via wrangler secret put or Cloudflare dashboard):
 *   TURNSTILE_SECRET   — Cloudflare Turnstile secret key
 *   RESEND_API_KEY     — Resend API key (same one used by jja-al3-worker)
 */

const TO_EMAIL   = 'Support@jjainsurance.com';
const FROM_EMAIL = 'contact@jjainsurance.com';

export default {
  async fetch(request, env) {

    if (request.method !== 'POST') {
      return Response.redirect('https://jjainsurance.com/contact/', 302);
    }

    // ── Parse form data ────────────────────────────────────────────────────
    let formData;
    try {
      formData = await request.formData();
    } catch (e) {
      console.log('ERROR: Could not parse form data:', e.message);
      return Response.redirect('https://jjainsurance.com/contact/?error=parse', 302);
    }

    // ── Honeypot ───────────────────────────────────────────────────────────
    // The hidden _gotcha field is invisible to real users. If a bot filled it,
    // silently "succeed" (redirect as if sent) so the bot learns nothing.
    if (formData.get('_gotcha')) {
      console.log('Honeypot tripped — dropping submission silently.');
      return Response.redirect('https://jjainsurance.com/contact/?sent=1', 302);
    }

    // ── Verify Turnstile ───────────────────────────────────────────────────
    const token = formData.get('cf-turnstile-response') || '';
    console.log('Turnstile token present:', token.length > 0);

    const verifyBody = new URLSearchParams({
      secret:   env.TURNSTILE_SECRET || '',
      response: token,
      remoteip: request.headers.get('CF-Connecting-IP') || '',
    });

    let verify;
    try {
      const verifyRes = await fetch(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        {
          method:  'POST',
          body:    verifyBody,
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
      );
      verify = await verifyRes.json();
      console.log('Turnstile verify result:', JSON.stringify(verify));
    } catch (e) {
      console.log('ERROR: Turnstile siteverify call failed:', e.message);
      return Response.redirect('https://jjainsurance.com/contact/?error=verify', 302);
    }

    if (!verify.success) {
      console.log('Turnstile FAILED. Error codes:', verify['error-codes']);
      return Response.redirect('https://jjainsurance.com/contact/?error=turnstile', 302);
    }

    // ── Extract fields ─────────────────────────────────────────────────────
    const firstName     = formData.get('first_name')    || '';
    const lastName      = formData.get('last_name')     || '';
    const email         = formData.get('email')         || '';
    const phone         = formData.get('phone')         || '';
    const topic         = formData.get('topic')         || '';
    const currentClient = formData.get('current_client') || '';
    const policyNumber  = formData.get('policy_number') || '';
    const message       = formData.get('message')       || '';

    // ── Opt-out → record in the Communications Hub (single source of truth) ──────
    // Honor an explicit opt-out topic or clear opt-out language in the message.
    // Marketing scope (stops promotional email/text; transactional service still
    // allowed). Best-effort + fail-safe: a hub hiccup never breaks the contact form,
    // and Support is still emailed below so a human can follow up.
    const optOutRe = /\b(unsubscribe|opt[\s-]?out|remove me|stop (all )?(marketing|emails?|texts?|messages))\b|do not (contact|market)/i;
    const isOptOut = optOutRe.test(`${topic}\n${message}`);
    if (isOptOut && env.WEBSITE_HUB_KEY) {
      const hubBase = env.HUB_BASE || 'https://jja-marketing-send.jacobs31.workers.dev';
      const hubHeaders = { 'x-hub-key': env.WEBSITE_HUB_KEY, 'Content-Type': 'application/json' };
      try {
        if (email) await fetch(`${hubBase}/hub/v1/suppress`, { method: 'POST', headers: hubHeaders, body: JSON.stringify({ channel: 'email', email, scope: 'marketing', reason: 'website opt-out', source: 'website-contact-form' }) });
        if (phone) await fetch(`${hubBase}/hub/v1/suppress`, { method: 'POST', headers: hubHeaders, body: JSON.stringify({ channel: 'sms', phone, scope: 'marketing', reason: 'website opt-out', source: 'website-contact-form' }) });
        console.log('Hub opt-out recorded for', email || phone);
      } catch (e) { console.log('ERROR: hub opt-out forward failed:', e.message); }
    }

    const fullName = `${firstName} ${lastName}`.trim();
    const subject  = `New Contact Form — ${topic || 'General'} (${fullName})`;

    // ── Build HTML email ───────────────────────────────────────────────────
    const esc = (s) => String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');

    const row = (label, value) => value
      ? `<tr><td style="padding:6px 12px 6px 0;font-weight:600;white-space:nowrap;vertical-align:top;color:#555;">${label}</td><td style="padding:6px 0;">${esc(value)}</td></tr>`
      : '';

    const emailHtml = `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:600px;margin:0 auto;padding:24px;">
  <div style="background:#14365e;color:#fff;padding:16px 24px;border-radius:8px 8px 0 0;">
    <strong style="font-size:16px;">New Contact Form Submission</strong><br>
    <span style="font-size:13px;opacity:.85;">jjainsurance.com</span>
  </div>
  <div style="border:1px solid #ddd;border-top:none;border-radius:0 0 8px 8px;padding:24px;">
    <table style="border-collapse:collapse;width:100%;">
      ${row('Topic',          topic)}
      ${row('Current client', currentClient)}
      ${row('Name',           fullName)}
      ${row('Email',          email)}
      ${row('Phone',          phone)}
      ${row('Policy #',       policyNumber)}
    </table>
    <hr style="border:none;border-top:1px solid #eee;margin:16px 0;">
    <p style="margin:0 0 6px;font-weight:600;color:#555;">Message</p>
    <p style="margin:0;white-space:pre-wrap;">${esc(message)}</p>
    <hr style="border:none;border-top:1px solid #eee;margin:16px 0;">
    <p style="margin:0;font-size:12px;color:#888;">
      Reply directly to this email to respond to ${esc(fullName)}.
    </p>
  </div>
</body>
</html>`;

    // ── Send via Resend ────────────────────────────────────────────────────
    const emailPayload = {
      from:     FROM_EMAIL,
      to:       [TO_EMAIL],
      reply_to: email ? [email] : undefined,
      subject,
      html:     emailHtml,
    };

    let resendRes;
    try {
      resendRes = await fetch('https://api.resend.com/emails', {
        method:  'POST',
        headers: {
          'Authorization': `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type':  'application/json',
        },
        body: JSON.stringify(emailPayload),
      });
      const resendBody = await resendRes.text();
      console.log('Resend status:', resendRes.status, 'body:', resendBody);
    } catch (e) {
      console.log('ERROR: Resend fetch failed:', e.message);
      return Response.redirect('https://jjainsurance.com/contact/?error=send', 302);
    }

    if (resendRes.ok) {
      return Response.redirect('https://jjainsurance.com/contact/?sent=1', 302);
    }

    console.log('Resend returned non-OK status:', resendRes.status);
    return Response.redirect('https://jjainsurance.com/contact/?error=send', 302);
  },
};
