// J. Jacobs & Associates — site script
(function () {
  'use strict';

  // -------- Helpers --------
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  // -------- Auto year update --------
  $$('[data-current-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

  // -------- Google Analytics 4 --------
  // Load gtag.js asynchronously and configure with the GA4 measurement ID.
  // GT-M3LBGVP (Google Tag Manager) is a separate tool — not installed here.
  (function loadGA4() {
    if (window.gtag || document.getElementById('ga4-loader')) return;
    var s = document.createElement('script');
    s.id = 'ga4-loader';
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-QRLBD79S35';
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', 'G-QRLBD79S35', { anonymize_ip: true });
  })();

  // -------- Microsoft Clarity --------
  // Heatmaps + session recordings. Project ID: xfosckzgap.
  // Clarity masks form inputs/sensitive content by default.
  (function loadClarity() {
    if (window.clarity) return;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', 'xfosckzgap');
  })();

  // -------- Phone-call click tracking (GA4) --------
  // Fires a GA4 "phone_call" event whenever a visitor taps a tel: link.
  // Mark this as a Key Event in GA4 and import it into Google Ads so that
  // click-to-call from ads is counted as a conversion. Mirrors the form's
  // existing generate_lead event. Uses event delegation so it also catches
  // tel: links added to the page after load.
  (function trackPhoneClicks() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest && e.target.closest('a[href^="tel:"]');
      if (!link || !window.gtag) return;
      window.gtag('event', 'phone_call', {
        event_category: 'engagement',
        event_label: link.getAttribute('href').replace('tel:', ''),
        transport_type: 'beacon'
      });
    }, true);
  })();

  // -------- Accessibility toolbar widget (UserWay) --------
  // Adds an on-page accessibility menu (font size, contrast, dark mode,
  // readable font, larger cursor, stop animations, etc.) so users can
  // adjust the site to their needs without changing browser settings.
  // Loaded on every page via this site script.
  (function loadAccessibilityWidget() {
    if (document.getElementById('userway-widget-loader')) return;
    var s = document.createElement('script');
    s.id = 'userway-widget-loader';
    s.src = 'https://cdn.userway.org/widget.js';
    s.async = true;
    s.setAttribute('data-account', '');
    (document.body || document.head).appendChild(s);
  })();

  // -------- Mobile menu toggle --------
  const toggle = $('.menu-toggle');
  const nav = $('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // -------- Submenu (dropdown) --------
  // The nav dropdowns use native <details>/<summary> elements — the browser
  // handles the open/close toggle for free. We do NOT preventDefault on the
  // summary click; doing so would block the native behavior.
  // We just add three small UX enhancements:
  //   1. Clicking outside an open dropdown closes it.
  //   2. Pressing Escape closes any open dropdowns.
  //   3. Opening one dropdown closes any others (single-open behavior).
  const allSubmenus = () => $$('details.submenu-wrap');

  // Single-open behavior: when one opens, close the others.
  allSubmenus().forEach((d) => {
    d.addEventListener('toggle', () => {
      if (d.open) {
        allSubmenus().forEach((other) => { if (other !== d) other.open = false; });
      }
    });
  });

  document.addEventListener('click', (e) => {
    // Close mobile menu if user clicks outside it
    if (nav && nav.classList.contains('is-open') && !nav.contains(e.target) && toggle && !toggle.contains(e.target)) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
    // Close any open dropdown if the click was outside it
    allSubmenus().forEach((d) => {
      if (d.open && !d.contains(e.target)) d.open = false;
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      allSubmenus().forEach((d) => { d.open = false; });
    }
  });

  // -------- Quote form: mode toggle + conditional sections --------
  const quoteForm = $('#quote-form');
  if (quoteForm) {

    // Show/hide a region. When hidden, strip 'required' from its inputs so
    // the browser doesn't block submit on fields the user can't see. We
    // remember original required state via data-required.
    const setRegionVisible = (el, visible) => {
      if (!el) return;
      el.hidden = !visible;
      $$('input, select, textarea', el).forEach((input) => {
        if (visible) {
          if (input.dataset.required === 'true') input.setAttribute('required', '');
          input.disabled = false;
        } else {
          if (input.hasAttribute('required')) input.dataset.required = 'true';
          input.removeAttribute('required');
          // Disable so the field is excluded from FormData on submit.
          // This prevents hidden product sections from cluttering the email.
          input.disabled = true;
        }
      });
    };

    // -------- Quote mode toggle (Quick vs Full) --------
    const quoteTypeInput = $('#quote_type');
    const modeToggleWrap = $('.quote-mode-toggle');

    const applyMode = (mode) => {
      quoteForm.setAttribute('data-mode', mode);
      // Re-query buttons each time so we don't hold a stale reference.
      $$('.quote-mode-btn').forEach((b) => {
        const isActive = b.dataset.mode === mode;
        b.classList.toggle('is-active', isActive);
        b.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      if (quoteTypeInput) {
        quoteTypeInput.value = mode === 'full' ? 'Full Quote' : 'Quick Quote';
      }
      // Show/hide all data-mode-only="full" regions
      $$('[data-mode-only="full"]', quoteForm).forEach((el) => {
        setRegionVisible(el, mode === 'full');
      });
      // Re-sync all product sections: Quick hides them all; Full shows
      // the ones whose checkbox is checked (and applies data-mode-only rules).
      productCheckboxes.forEach((cb) => {
        const section = document.getElementById(cb.dataset.section);
        if (!section) return;
        const showSection = cb.checked && mode === 'full';
        setRegionVisible(section, showSection);
        if (showSection) {
          $$('[data-mode-only="full"]', section).forEach((el) => {
            setRegionVisible(el, true);
          });
        }
      });
    };

    // Event delegation: catch any click that lands inside the mode-toggle
    // wrapper, even if it lands on a nested <span>. This is more reliable
    // than attaching listeners to each button.
    if (modeToggleWrap) {
      modeToggleWrap.addEventListener('click', (e) => {
        const btn = e.target.closest('.quote-mode-btn');
        if (!btn || !modeToggleWrap.contains(btn)) return;
        e.preventDefault();
        const mode = btn.dataset.mode || 'quick';
        applyMode(mode);
      });
      // Keyboard support: Space/Enter activate, arrow keys move focus
      modeToggleWrap.addEventListener('keydown', (e) => {
        const btn = e.target.closest('.quote-mode-btn');
        if (!btn) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'ArrowDown' || e.key === 'ArrowUp') {
          e.preventDefault();
          const buttons = $$('.quote-mode-btn', modeToggleWrap);
          const idx = buttons.indexOf(btn);
          const next = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? (idx + 1) % buttons.length : (idx - 1 + buttons.length) % buttons.length;
          buttons[next].focus();
          applyMode(buttons[next].dataset.mode);
        }
      });
    }

    // -------- Product checkbox -> section visibility --------
    const productCheckboxes = $$('input[type="checkbox"][data-section]', quoteForm);
    const selectedCountEl = document.getElementById('productSelectedCount');
    const continueWrap = document.getElementById('productContinue');
    const continueBtn = document.getElementById('productContinueBtn');

    const updateSelectedCount = () => {
      const selected = productCheckboxes.filter((cb) => cb.checked);
      if (selectedCountEl) {
        if (!selected.length) {
          selectedCountEl.innerHTML = 'No products selected yet. Check one or more above.';
        } else {
          const names = selected.map((cb) => {
            const lbl = cb.closest('label.product-pick');
            const name = lbl ? lbl.querySelector('.pick-name') : null;
            return name ? name.textContent.trim() : cb.value;
          });
          const word = selected.length === 1 ? 'product' : 'products';
          selectedCountEl.innerHTML = `<strong>${selected.length} ${word} selected:</strong> ${names.join(', ')}`;
        }
      }
      // Show the Continue button only when at least one product is selected.
      if (continueWrap) continueWrap.hidden = selected.length === 0;
    };

    // Show/hide a product's question section.
    // In Quick Quote mode the sections are never shown — the user only
    // picks which products they want and fills in contact info. The agent
    // calls to gather details. In Full Quote mode the section appears as
    // soon as the checkbox is checked.
    const syncSection = (checkbox) => {
      const section = document.getElementById(checkbox.dataset.section);
      if (!section) return;
      const mode = quoteForm.getAttribute('data-mode');
      const showSection = checkbox.checked && mode === 'full';
      setRegionVisible(section, showSection);
      if (showSection) {
        $$('[data-mode-only="full"]', section).forEach((el) => {
          setRegionVisible(el, true);
        });
      }
      updateSelectedCount();
    };
    productCheckboxes.forEach((cb) => {
      cb.addEventListener('change', () => syncSection(cb));
      // initial state
      syncSection(cb);
    });
    updateSelectedCount();

    // -------- Generic cross-sell trigger --------
    // Any <select> with a data-cross-sell="line_xxx" attribute will, when
    // set to "Yes", check the corresponding product checkbox (auto-revealing
    // its question section) and smooth-scroll to it. Used for upsell
    // questions like "Would you like a home quote too?" across every product.
    $$('[data-cross-sell]', quoteForm).forEach((trigger) => {
      trigger.addEventListener('change', () => {
        if (trigger.value !== 'Yes') return;
        const targetId = trigger.dataset.crossSell;
        const cb = document.getElementById(targetId);
        if (!cb || cb.checked) return;
        cb.checked = true;
        syncSection(cb);
        // Smooth-scroll to the newly revealed section so the user notices.
        setTimeout(() => {
          const sectionId = cb.dataset.section;
          const section = sectionId ? document.getElementById(sectionId) : null;
          if (section) {
            const head = section.querySelector('.quote-section-head') || section;
            head.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      });
    });

    // -------- Continue button: scroll to "Your information" so the user
    // fills the required contact fields first, then naturally scrolls down
    // into the product-specific questions below.
    if (continueBtn) {
      continueBtn.addEventListener('click', () => {
        const target = document.getElementById('your-information');
        if (!target) return;
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // After scrolling, put keyboard focus on the first name field so the
        // user can start typing immediately.
        setTimeout(() => {
          const firstNameField = document.getElementById('first_name');
          if (firstNameField) firstNameField.focus({ preventScroll: true });
        }, 450);
      });
    }

    // -------- Require at least one product selected before submit --------
    quoteForm.addEventListener('submit', (e) => {
      const anyChecked = productCheckboxes.some((cb) => cb.checked);
      if (!anyChecked) {
        e.preventDefault();
        const firstCb = productCheckboxes[0];
        if (firstCb) {
          firstCb.focus();
          // Mild visual cue without adding new CSS
          firstCb.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        alert('Please check at least one product you would like a quote for.');
      }
    });

    // -------- Partial lead capture --------
    // Sends a background POST to the quote Worker when the user has filled out
    // the key contact fields but hasn't submitted yet, so the agency still gets
    // the lead. Fires only when the user actually closes or navigates away
    // from the tab (pagehide / beforeunload) — one submission per person max.
    // Idle and visibilitychange triggers were removed because they fired too
    // frequently during normal form-filling and sent duplicate/premature leads
    // before users even clicked Submit.
    let partialSent = false;

    const isValidEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
    const isValidPhone = (v) => v.replace(/\D/g, '').length >= 10;
    const isValidZip = (v) => /^\d{5}$/.test(v.trim());

    const partialFieldVal = (name) => {
      const el = quoteForm.querySelector(`[name="${name}"]`);
      return el ? el.value.trim() : '';
    };

    const allPartialFieldsValid = () => {
      if (!partialFieldVal('first_name')) return false;
      if (!partialFieldVal('last_name')) return false;
      if (!isValidEmail(partialFieldVal('email'))) return false;
      if (!isValidPhone(partialFieldVal('phone'))) return false;
      if (!isValidZip(partialFieldVal('zip'))) return false;
      return true;
    };

    const sendPartialLead = (trigger) => {
      if (partialSent) return;
      if (!allPartialFieldsValid()) return;
      // Read the worker URL from the form's data-worker attribute.
      const workerUrl = quoteForm.dataset && quoteForm.dataset.worker;
      if (!workerUrl) return;
      partialSent = true;
      try {
        // Build a plain object from the current form state
        const fd = new FormData(quoteForm);
        const formObj = {};
        fd.forEach((val, key) => {
          if (formObj[key] !== undefined) {
            formObj[key] = formObj[key] + ',' + val;
          } else {
            formObj[key] = val;
          }
        });
        // Mark as partial lead so the Worker sends a lightweight partial email
        formObj.partial_lead      = trigger || 'yes';
        formObj.partial_lead_note = 'User filled out contact info but had not yet clicked Submit at the time this was captured.';

        // Use fetch with keepalive (survives page unload).
        // JSON body is well under the 64 KB keepalive limit.
        fetch(workerUrl, {
          method:   'POST',
          body:     JSON.stringify({ formData: formObj }),
          headers:  { 'Content-Type': 'application/json' },
          keepalive: true,
        }).then((r) => {
          if (r.status < 200 || r.status >= 300) {
            // Non-2xx — allow a retry on the next trigger.
            partialSent = false;
          }
        }).catch(() => {
          // Network error — allow a retry on the next trigger.
          partialSent = false;
        });
      } catch (e) {
        partialSent = false;
      }
    };

    // Unload triggers only — fires when the user closes or navigates away.
    // This ensures at most one partial per visitor.
    window.addEventListener('pagehide', () => sendPartialLead('pagehide'));
    window.addEventListener('beforeunload', () => sendPartialLead('beforeunload'));

    // If the user actually submits the full form, mark partial as sent so we
    // don't also fire a partial right before the real one.
    quoteForm.addEventListener('submit', () => { partialSent = true; });

    // Manual test helper retained for future debugging. Open DevTools console
    // and type window.testPartialLead() to force-fire the trigger without
    // waiting 15 seconds or closing the tab.
    window.testPartialLead = function () {
      partialSent = false;
      sendPartialLead('manual-test');
    };

    // Initialize default mode
    applyMode(quoteForm.getAttribute('data-mode') || 'quick');
  }

})();
