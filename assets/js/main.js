// J. Jacobs & Associates — site script
(function () {
  'use strict';

  // -------- Helpers --------
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

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

  // -------- Submenu (dropdown) — event delegation pattern --------
  // Works reliably regardless of when DOM nodes are added/cached.
  document.addEventListener('click', (e) => {
    // Did the click land on a submenu trigger?
    const trigger = e.target.closest('.has-submenu > a, .has-submenu > button, .nav-toggle');
    if (trigger) {
      e.preventDefault();
      e.stopPropagation();
      const parent = trigger.closest('.has-submenu');
      if (!parent) return;
      const willOpen = !parent.classList.contains('is-open');
      // Close all other submenus
      $$('.has-submenu.is-open').forEach((p) => { if (p !== parent) p.classList.remove('is-open'); });
      // Toggle this one
      parent.classList.toggle('is-open', willOpen);
      trigger.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      return;
    }

    // Click was outside any has-submenu — close them all
    if (!e.target.closest('.has-submenu')) {
      $$('.has-submenu.is-open').forEach((p) => p.classList.remove('is-open'));
    }
    // Also close the mobile menu if clicking outside
    if (nav && nav.classList.contains('is-open') && !nav.contains(e.target) && toggle && !toggle.contains(e.target)) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Escape closes any open submenu
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      $$('.has-submenu.is-open').forEach((p) => p.classList.remove('is-open'));
    }
  });

  // -------- Quote form progressive disclosure --------
  const quoteForm = $('#quote-form');
  if (quoteForm) {
    const showHide = (selector, show) => {
      const el = $(selector);
      if (!el) return;
      el.style.display = show ? '' : 'none';
      el.querySelectorAll('input, select, textarea').forEach((i) => {
        if (!show) { i.removeAttribute('required'); } else if (i.dataset.required === 'true') { i.setAttribute('required', ''); }
      });
    };
    const updateSections = () => {
      const auto = $('input[name="line_auto"]')?.checked;
      const home = $('input[name="line_home"]')?.checked;
      const life = $('input[name="line_life"]')?.checked;
      const biz = $('input[name="line_business"]')?.checked;
      showHide('#section-auto', auto);
      showHide('#section-home', home);
      showHide('#section-life', life);
      showHide('#section-business', biz);
    };
    quoteForm.querySelectorAll('input[name^="line_"]').forEach((cb) => cb.addEventListener('change', updateSections));
    updateSections();
  }

  // -------- Phone formatting --------
  $$('input[type="tel"]').forEach((input) => {
    input.addEventListener('input', (e) => {
      const v = e.target.value.replace(/\D/g, '').slice(0, 10);
      if (v.length >= 7) e.target.value = `(${v.slice(0, 3)}) ${v.slice(3, 6)}-${v.slice(6)}`;
      else if (v.length >= 4) e.target.value = `(${v.slice(0, 3)}) ${v.slice(3)}`;
      else if (v.length > 0) e.target.value = `(${v}`;
      else e.target.value = '';
    });
  });

  // -------- Current year in footer --------
  const yr = $('[data-current-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
