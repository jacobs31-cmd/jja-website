/**
 * JJA Quote Form — Worker Submission & PDF Download
 *
 * What this does:
 *  1. Intercepts the quote form submit.
 *  2. Generates a branded PDF summary of the quote (jsPDF).
 *  3. Converts the form data to JSON and POSTs it — along with the PDF as a
 *     base64 string — to the JJA Cloudflare Worker, which sends a Resend email
 *     with the PDF and any AL3 files attached.
 *  4. On success: hides the form and shows an in-page confirmation with a
 *     "Download Your Quote Summary (PDF)" button so the customer can save a copy.
 *
 * The Worker URL is read from the form's data-worker attribute.
 *
 * Dependencies: jsPDF UMD build loaded on the quotes page via CDN.
 * Gracefully degrades if jsPDF fails to load — form still submits, PDF omitted.
 *
 * v20260524a
 */
(function () {
  'use strict';

  // ── Helpers ────────────────────────────────────────────────────────────────

  /** Walk ancestors; return true if any ancestor (or self) is hidden. */
  function isHidden(el) {
    var node = el;
    while (node && node !== document.body) {
      if (node.hidden) return true;
      if (node.style && (node.style.display === 'none' || node.style.visibility === 'hidden')) return true;
      node = node.parentElement;
    }
    return false;
  }

  /** Get the display value of a form element. Returns '' if empty/unchecked. */
  function fieldVal(el) {
    if (!el || el.disabled || isHidden(el)) return '';
    if (el.type === 'checkbox') return el.checked ? (el.value || 'Yes') : '';
    if (el.type === 'date') {
      if (!el.value) return '';
      var p = el.value.split('-');
      return p[1] + '/' + p[2] + '/' + p[0]; // MM/DD/YYYY
    }
    return (el.value || '').trim();
  }

  /** Shorthand: get value by element ID. */
  function byId(id) {
    var el = document.getElementById(id);
    return el ? fieldVal(el) : '';
  }

  // ── Data Collection ────────────────────────────────────────────────────────

  function collectFormData() {
    var form = document.getElementById('quote-form');
    if (!form) return null;

    var mode = form.getAttribute('data-mode') || 'quick';

    // Products selected
    var productKeys = ['auto','home','condo','renters','rental','life','umbrella','recreational','business','workcomp'];
    var products = [];
    productKeys.forEach(function (p) {
      var cb = document.getElementById('line_' + p);
      if (!cb || !cb.checked) return;
      var lbl = cb.closest('label');
      var name = lbl ? (lbl.querySelector('.pick-name') || lbl).textContent.trim() : p;
      products.push(name);
    });

    // Contact — hardcoded known IDs for the always-present fields
    var c = {
      name:            [byId('first_name'), byId('last_name')].filter(Boolean).join(' '),
      email:           byId('email'),
      phone:           byId('phone'),
      zip:             byId('zip'),
      dob:             byId('dob'),
      occupation:      byId('occupation'),
      referrer:        byId('referrer'),
      referrer_name:   byId('referrer_name'),
      spouse:          [byId('spouse_first_name'), byId('spouse_last_name')].filter(Boolean).join(' '),
      spouse_dob:      byId('spouse_dob'),
      address:         [byId('street_address'), byId('address_line_2')].filter(Boolean).join(', '),
      city:            byId('city'),
      current_carrier: byId('current_carrier'),
      renewal_date:    byId('renewal_date'),
      current_premium: byId('current_premium')
    };

    // Product sections — DOM-walk each visible .quote-section
    var sectionIds = [
      'section-auto', 'section-home', 'section-condo', 'section-renters',
      'section-rental', 'section-life', 'section-umbrella', 'section-recreational',
      'section-business', 'section-workcomp'
    ];
    var sections = [];

    sectionIds.forEach(function (sid) {
      var sec = document.getElementById(sid);
      if (!sec || isHidden(sec)) return;

      var heading = sec.querySelector('h2');
      var title = heading ? heading.textContent.trim() : sid;
      var rows = [];
      var seen = {};

      // label[for] → input/select/textarea pairs
      sec.querySelectorAll('label[for]').forEach(function (lbl) {
        var id = lbl.htmlFor;
        if (seen[id]) return;
        var el = document.getElementById(id);
        if (!el || el.disabled || isHidden(el)) return;
        var v = fieldVal(el);
        if (!v) return;
        seen[id] = true;
        var labelText = lbl.textContent.replace(/\s+/g, ' ').trim()
          .replace(/\s*[•\*]\s*$/, '').replace(/\s*\(required\)\s*/i, '').trim();
        rows.push([labelText, v]);
      });

      // Checked checkboxes whose label[for] wasn't already seen
      sec.querySelectorAll('input[type=checkbox]:checked').forEach(function (cb) {
        if (!cb.id || seen[cb.id] || cb.disabled || isHidden(cb)) return;
        var lbl = sec.querySelector('label[for="' + cb.id + '"]');
        if (!lbl) return;
        seen[cb.id] = true;
        rows.push([lbl.textContent.trim(), '✓']);
      });

      if (rows.length) sections.push({ title: title, rows: rows });
    });

    return {
      mode:     mode,
      products: products,
      contact:  c,
      sections: sections,
      comments: byId('comments')
    };
  }

  // ── Formatted Text Summary (injected into the lead email sent by the Worker) ──

  function buildFormattedSummary(data) {
    if (!data) return '';
    var lines = [];
    var date = new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    var modeLabel = data.mode === 'full' ? 'Full Quote (15-min)' : 'Quick Quote (2-min)';

    lines.push('================================================================');
    lines.push('  QUOTE REQUEST — J. JACOBS & ASSOCIATES INSURANCE');
    lines.push('================================================================');
    lines.push('  ' + date + '   |   ' + modeLabel);
    lines.push('');

    if (data.products.length) {
      lines.push('PRODUCTS REQUESTED');
      data.products.forEach(function (p) { lines.push('  • ' + p); });
      lines.push('');
    }

    var c = data.contact;
    lines.push('CONTACT INFORMATION');
    if (c.name)            lines.push('  Name:              ' + c.name);
    if (c.email)           lines.push('  Email:             ' + c.email);
    if (c.phone)           lines.push('  Phone:             ' + c.phone);
    if (c.zip)             lines.push('  ZIP Code:          ' + c.zip);
    if (c.dob)             lines.push('  Date of Birth:     ' + c.dob);
    if (c.occupation)      lines.push('  Occupation:        ' + c.occupation);
    if (c.spouse)          lines.push('  Spouse:            ' + c.spouse + (c.spouse_dob ? '  (DOB: ' + c.spouse_dob + ')' : ''));
    if (c.address)         lines.push('  Address:           ' + c.address + (c.city ? ', ' + c.city + ', MI' : ''));
    if (c.current_carrier) lines.push('  Current Carrier:   ' + c.current_carrier);
    if (c.renewal_date)    lines.push('  Policy Renewal:    ' + c.renewal_date);
    if (c.current_premium) lines.push('  Current Premium:   ' + c.current_premium);
    if (c.referrer)        lines.push('  Referred Via:      ' + c.referrer + (c.referrer_name ? ' — ' + c.referrer_name : ''));
    lines.push('');

    data.sections.forEach(function (sec) {
      lines.push(sec.title.toUpperCase());
      sec.rows.forEach(function (row) {
        var padded = (row[0] + ':').padEnd(30);
        lines.push('  ' + padded + row[1]);
      });
      lines.push('');
    });

    if (data.comments) {
      lines.push('COMMENTS / ADDITIONAL NOTES');
      lines.push('  ' + data.comments);
      lines.push('');
    }

    lines.push('================================================================');
    lines.push('  J. Jacobs & Associates Insurance  |  jjainsurance.com');
    lines.push('  4301 S. Baldwin Rd, Lake Orion, MI 48359  |  (248) 693-6455');
    lines.push('================================================================');
    return lines.join('\n');
  }

  // ── PDF Generation ─────────────────────────────────────────────────────────

  function generateQuotePDF(data) {
    if (!data || typeof window.jspdf === 'undefined') return null;
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ unit: 'pt', format: 'letter', orientation: 'portrait' });

    // ── Palette & layout constants ──────────────────────────────────────────
    var NAVY  = [20,  54,  94];
    var NAVY2 = [28,  78, 140];
    var LIGHT = [245, 247, 250];
    var SUBHD = [232, 238, 247];
    var DARK  = [25,  35,  55];
    var MUTED = [100, 115, 135];
    var WHITE = [255, 255, 255];
    var LROW  = [248, 250, 253];
    var PW = 612, PH = 792, M = 40, G = 8;
    var CW = PW - M * 2;   // 532 pt usable width
    var y = 0, stripe = false;

    // ── Page header ─────────────────────────────────────────────────────────
    doc.setFillColor(NAVY[0], NAVY[1], NAVY[2]);
    doc.rect(0, 0, PW, 72, 'F');
    doc.setTextColor(WHITE[0], WHITE[1], WHITE[2]);
    doc.setFont('helvetica', 'bold');  doc.setFontSize(17);
    doc.text('J. Jacobs & Associates Insurance', M, 28);
    doc.setFont('helvetica', 'normal'); doc.setFontSize(9);
    doc.text('4301 S. Baldwin Rd, Lake Orion, MI 48359  •  (248) 693-6455  •  jjainsurance.com', M, 46);
    doc.setFontSize(8);
    doc.text('Independent Insurance Agency  •  50+ carrier markets  •  Michigan since 1981', M, 62);
    y = 88;

    // ── Title row ───────────────────────────────────────────────────────────
    doc.setTextColor(DARK[0], DARK[1], DARK[2]);
    doc.setFont('helvetica', 'bold'); doc.setFontSize(14);
    doc.text('Quote Request Summary', M, y); y += 16;
    var pdfDate = new Date().toLocaleDateString('en-US', { weekday:'long', month:'long', day:'numeric', year:'numeric' });
    doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5);
    doc.setTextColor(MUTED[0], MUTED[1], MUTED[2]);
    doc.text('Submitted: ' + pdfDate + '   •   ' + (data.mode === 'full' ? 'Full Quote' : 'Quick Quote'), M, y);
    y += 20;

    // ── Products pill ───────────────────────────────────────────────────────
    if (data.products.length) {
      doc.setFillColor(LIGHT[0], LIGHT[1], LIGHT[2]);
      doc.roundedRect(M, y, CW, 24, 3, 3, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(7.5);
      doc.setTextColor(NAVY[0], NAVY[1], NAVY[2]);
      doc.text('PRODUCTS:', M + 8, y + 16);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(DARK[0], DARK[1], DARK[2]);
      var ps = doc.splitTextToSize(data.products.join('  •  '), CW - 80);
      doc.text(ps[0], M + 72, y + 16);
      y += 32;
    }

    // ── Layout helpers ───────────────────────────────────────────────────────

    // Page-break guard
    function pb(need) {
      if (y + need > PH - 50) { doc.addPage(); y = 48; stripe = false; }
    }

    // Navy card header bar (like iq-head)
    function cardHead(title) {
      pb(24); y += 8;
      doc.setFillColor(NAVY2[0], NAVY2[1], NAVY2[2]);
      doc.rect(M, y, CW, 18, 'F');
      doc.setTextColor(WHITE[0], WHITE[1], WHITE[2]);
      doc.setFont('helvetica', 'bold'); doc.setFontSize(8);
      doc.text(title.toUpperCase(), M + 8, y + 13);
      y += 20; stripe = false;
    }

    // Navy sub-section label with line (like iq-sec-label)
    function subLbl(title) {
      pb(18); y += 5;
      doc.setFont('helvetica', 'bold'); doc.setFontSize(7);
      doc.setTextColor(NAVY2[0], NAVY2[1], NAVY2[2]);
      doc.text(title.toUpperCase(), M + 8, y + 10);
      var tw = doc.getTextWidth(title.toUpperCase());
      doc.setDrawColor(180, 195, 210); doc.setLineWidth(0.4);
      doc.line(M + 10 + tw, y + 6.5, M + CW - 8, y + 6.5);
      y += 16;
    }

    // Light-coloured block header for Vehicle 1, Driver 1, etc.
    function blockHead(title) {
      pb(22); y += 4;
      doc.setFillColor(SUBHD[0], SUBHD[1], SUBHD[2]);
      doc.roundedRect(M + 2, y, CW - 4, 15, 2, 2, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(7.5);
      doc.setTextColor(NAVY[0], NAVY[1], NAVY[2]);
      doc.text(title, M + 10, y + 11);
      y += 17; stripe = false;
    }

    // Render a row of up to 4 {l, v} field cells; empty cells are skipped.
    // Each cell: tiny uppercase grey label on top, bold dark value below.
    function fRow(fields) {
      var flds = (fields || []).filter(function (f) { return f && f.v; });
      if (!flds.length) return;
      var n = Math.min(flds.length, 4);
      var ROW_H = 28;
      pb(ROW_H);
      if (stripe) {
        doc.setFillColor(LROW[0], LROW[1], LROW[2]);
        doc.rect(M, y, CW, ROW_H, 'F');
      }
      stripe = !stripe;
      var colW = (CW - 16 - (n - 1) * G) / n;
      for (var ci = 0; ci < n; ci++) {
        if (!flds[ci]) continue;
        var cx = M + 8 + ci * (colW + G);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(6.5);
        doc.setTextColor(MUTED[0], MUTED[1], MUTED[2]);
        doc.text(String(flds[ci].l).toUpperCase().slice(0, 42), cx, y + 9);
        doc.setFont('helvetica', 'bold'); doc.setFontSize(8.5);
        doc.setTextColor(DARK[0], DARK[1], DARK[2]);
        var vv = doc.splitTextToSize(String(flds[ci].v), colW - 4);
        doc.text(vv[0] || '', cx, y + 21);
      }
      y += ROW_H;
    }

    // ── Data helpers ─────────────────────────────────────────────────────────

    // {l, v} from a field ID
    function fv(id, label) {
      var val = byId(id);
      return val ? { l: label, v: val } : null;
    }

    // {l, v} from a radio group name
    function rv(name, label) {
      var radios = document.querySelectorAll('input[name="' + name + '"]');
      for (var ri = 0; ri < radios.length; ri++) {
        if (radios[ri].checked && !isHidden(radios[ri])) {
          return { l: label, v: radios[ri].value };
        }
      }
      return null;
    }

    // true if a section div is currently shown
    function secVis(id) {
      var el = document.getElementById(id);
      return el && !el.hasAttribute('hidden') && el.style.display !== 'none';
    }

    // true if a specific element (and all ancestors) are visible
    function elVis(id) {
      var el = document.getElementById(id);
      return el && !isHidden(el);
    }

    // ── CONTACT INFORMATION ──────────────────────────────────────────────────
    cardHead('Contact Information');
    fRow([fv('first_name','First name'), fv('last_name','Last name'), fv('email','Email'), fv('phone','Phone')]);
    fRow([fv('dob','Date of birth'), fv('zip','ZIP code'), fv('occupation','Occupation'), fv('current_carrier','Current carrier')]);
    fRow([fv('renewal_date','Renewal date'), fv('current_premium','Current premium'), fv('referrer','How they heard'), fv('referrer_name','Referred by')]);
    var spF = byId('spouse_first_name'), spL = byId('spouse_last_name');
    if (spF || spL) {
      var spName = [spF, spL].filter(Boolean).join(' ');
      fRow([{ l:'Second Named Insured', v:spName }, fv('spouse_dob','Date of birth'), fv('street_address','Street address'), fv('city','City')]);
    } else if (byId('street_address')) {
      fRow([fv('street_address','Street address'), fv('address_line_2','Apt / Suite'), fv('city','City'), null]);
    }

    // ── AUTO ─────────────────────────────────────────────────────────────────
    if (secVis('section-auto')) {

      cardHead('Vehicles');
      for (var vi = 1; vi <= 8; vi++) {
        if (!byId('vehicle_'+vi+'_year') && !byId('vehicle_'+vi+'_make')) break;
        blockHead('Vehicle ' + vi);
        fRow([fv('vehicle_'+vi+'_year','Year'), fv('vehicle_'+vi+'_make','Make'), fv('vehicle_'+vi+'_model','Model'), fv('vehicle_'+vi+'_vin','VIN')]);
        fRow([fv('vehicle_'+vi+'_collision','Collision?'), fv('vehicle_'+vi+'_title','Title held by'), rv('vehicle_'+vi+'_gar','Garaged at home?'), rv('vehicle_'+vi+'_lien','Lien / lease?')]);
        fRow([rv('vehicle_'+vi+'_rs','Rideshare use?'), rv('vehicle_'+vi+'_biz','Business use?'), rv('vehicle_'+vi+'_coll_type','Collision type'), null]);
      }

      cardHead('Drivers');
      for (var di = 1; di <= 8; di++) {
        if (!byId('driver_'+di+'_first') && !byId('driver_'+di+'_last')) break;
        blockHead('Driver ' + di);
        fRow([fv('driver_'+di+'_first','First name'), fv('driver_'+di+'_last','Last name'), fv('driver_'+di+'_dob','Date of birth'), fv('driver_'+di+'_gender','Gender')]);
        fRow([fv('driver_'+di+'_incidents','Violations / claims?'), fv('driver_'+di+'_incidents_detail','Description'), rv('driver_'+di+'_lic','License status'), fv('driver_'+di+'_edu','Education')]);
        fRow([fv('driver_'+di+'_occ','Occupation'), rv('driver_'+di+'_gs','Good student disc?'), null, null]);
      }

      if (elVis('auto_prior_carrier')) {
        cardHead('Current Auto Insurance');
        fRow([fv('auto_prior_carrier','Prior carrier'), fv('auto_prior_prem','Annual premium'), fv('auto_prior_exp','Expiration date'), rv('a_lapse','Coverage lapse?')]);
        fRow([fv('a_bipd','Current BI/PD'), fv('a_pip_cur','Current PIP'), rv('a_lic_issue','License suspension?'), null]);
      }

      if (elVis('auto_liability')) {
        cardHead('Desired Auto Coverage');
        fRow([fv('auto_liability','BI / PD limits'), fv('a_um','UM / UIM'), fv('auto_pip','PIP'), null]);
        fRow([fv('auto_comp_ded','Comp deductible'), fv('auto_collision_ded','Collision deductible'), rv('a_glass','Glass coverage?'), rv('auto_towing','Towing & roadside?')]);
        fRow([rv('a_rent','Rental car?'), null, null, null]);
      }
    }

    // ── HOME ─────────────────────────────────────────────────────────────────
    if (secVis('section-home')) {
      var resType = (function () {
        var rr = document.querySelectorAll('input[name="h_res_type"]');
        for (var i = 0; i < rr.length; i++) { if (rr[i].checked) return rr[i].value; }
        return '';
      }());
      var isRenters  = resType === 'Renters';
      var isCondo    = resType === 'Condo';
      var isLandlord = resType === 'Landlord';

      cardHead('Home — Property');
      fRow([fv('home_address','Property address'), fv('year_built','Year built'), resType ? {l:'Residence type', v:resType} : null, null]);

      if (isLandlord && elVis('ll_units')) {
        cardHead('Landlord / Rental Details');
        fRow([fv('ll_units','Number of units'), fv('ll_monthly_rent','Monthly rent / unit'), fv('ll_loss_rents','Loss of rents'), rv('ll_form','Policy form')]);
        fRow([rv('ll_vandalism','Vandalism?'), fv('ll_liability','Premises liability'), fv('ll_notes','Notes'), null]);
      }

      if (elVis('home_purchase_date') || elVis('h_prior_carrier')) {
        cardHead('Prior Insurance');
        fRow([fv('home_purchase_date','Purchase / closing'), fv('home_mortgage','Mortgage?'), fv('h_mkt_val','Market value'), fv('home_deeded','Deed holder(s)')]);
        fRow([fv('h_prior_carrier','Prior carrier'), fv('h_prior_len','Yrs w/ carrier'), fv('h_prior_exp','Prior expiration'), fv('h_cur_prem','Current premium')]);
      }

      if (elVis('home_cov_c')) {
        cardHead('Coverage Requested');
        if (!isRenters) {
          fRow([fv('home_cov_a','Cov A — Dwelling'), fv('home_cov_b','Cov B — Other structures'), fv('home_cov_c','Cov C — Personal property'), fv('home_cov_d','Cov D — Loss of use')]);
        } else {
          fRow([fv('home_cov_c','Cov C — Personal property'), fv('home_cov_d','Cov D — Add\'l living expense'), null, null]);
        }
        fRow([fv('home_liability','Liability'), fv('home_deductible','Deductible'), fv('home_water_backup','Water backup'), rv('home_service_line','Service line?')]);
        fRow([rv('home_personal_injury','Personal injury end.?'), fv('h_pay_plan','Payment plan'), null, null]);
      }

      if (!isRenters && elVis('home-structure-card')) {
        cardHead('Structure');
        fRow([fv('square_feet','Sq footage'), fv('home_stories','Stories'), fv('home_construction','Construction type'), fv('siding','Exterior siding')]);
        fRow([fv('home_bathrooms','Bathrooms'), fv('h_gar_cars','Garage — cars'), rv('h_gar_type','Garage type'), rv('home_basement','Basement?')]);
        fRow([fv('h_bsmt_pct','Basement finished'), rv('home_basement_walkout','Walkout basement?'), null, null]);
      }

      if (!isRenters && elVis('home-systems-card')) {
        cardHead('Systems & Updates');
        fRow([fv('home_roof_type','Roof type'), fv('home_roof_year','Roof replaced'), fv('home_heat','Heating type'), fv('h_heat_upd','Heating updated')]);
        fRow([rv('h_fire_pl','Fireplace?'), rv('home_stove','Wood stove?'), fv('home_stove_room','Stove location'), rv('home_alarm','Alarm monitored?')]);
        fRow([rv('h_breakers','Circuit breakers?'), fv('h_elec_upd','Electrical updated'), fv('h_plumb','Plumbing type'), fv('h_plumb_upd','Plumbing updated')]);
      }

      if (elVis('home_jewelry_amt')) {
        cardHead('Scheduled Valuables');
        fRow([fv('home_jewelry_amt','Jewelry'), fv('home_firearms_amt','Firearms'), fv('home_fineart_amt','Fine art / antiques'), fv('home_other_valuables','Furs / collectibles')]);
      }

      // Additional Risk card
      var dogYes = rv('home_dogs', 'Dogs?');
      var anyRisk = dogYes || elVis('home_pool_ig') || elVis('h_wsens');
      if (anyRisk) {
        cardHead('Additional Risk');

        // Dogs
        if (dogYes) {
          subLbl('Dogs');
          var dogCntV = byId('home_dog_count');
          fRow([dogYes, dogCntV ? {l:'How many?', v:dogCntV} : null, null, null]);
          for (var dgi = 1; dgi <= 4; dgi++) {
            var dbr = byId('home_dog_'+dgi+'_breed');
            if (!dbr) break;
            fRow([{l:'Dog '+dgi+' — breed', v:dbr}, rv('home_dog_'+dgi+'_bite','Dog '+dgi+' — ever bitten?'), null, null]);
          }
        }

        // Pool & Trampoline (hidden for Condo / Renters)
        if (!isCondo && !isRenters) {
          var igEl = document.getElementById('home_pool_ig');
          var agEl = document.getElementById('home_pool_ag');
          var htEl = document.getElementById('home_pool_hottub');
          var poolTypes = [];
          if (igEl && igEl.checked) poolTypes.push('In-ground pool');
          if (agEl && agEl.checked) poolTypes.push('Above-ground pool');
          if (htEl && htEl.checked) poolTypes.push('Hot tub / spa');
          var trampV = rv('home_trampoline', 'Trampoline?');
          if (poolTypes.length || (trampV && trampV.v === 'Yes')) {
            subLbl('Pool & Trampoline');
            if (poolTypes.length) {
              fRow([{l:'Pool / hot tub type(s)', v:poolTypes.join(', ')}, rv('h_slide','Slide?'), rv('h_dive','Diving board?'), rv('h_pool_fence','Pool fenced?')]);
              fRow([rv('h_pool_gate','Locking gate?'), null, null, null]);
            }
            if (trampV && trampV.v === 'Yes') {
              fRow([trampV, rv('h_tramp_net','Safety net?'), rv('h_tramp_fence','In fenced yard?'), null]);
            }
          }
        }

        subLbl('Smart Home & Safety');
        fRow([rv('h_wsens','Water leak sensors?'), rv('h_wshut','Auto water shutoff?'), rv('h_gen','Whole-house generator?'), null]);

        subLbl('Home Use');
        fRow([rv('home_business','Business from home?'), rv('home_rental_use','Home rented to others?'), rv('h_mj','Marijuana on property?'), fv('home_claims_count','Claims — last 5 yrs')]);
      }
    }

    // ── REMAINING SECTIONS (condo, renters, rental, life, umbrella, etc.) ───
    // Use the generic collected rows from data.sections, excluding already-rendered sections.
    var handledTitles = { 'Auto details': 1, 'Home details': 1 };
    data.sections.forEach(function (sec) {
      if (handledTitles[sec.title] || !sec.rows || !sec.rows.length) return;
      cardHead(sec.title);
      for (var si = 0; si < sec.rows.length; si += 2) {
        var r1 = sec.rows[si], r2 = sec.rows[si + 1];
        fRow([
          r1 ? { l: r1[0], v: r1[1] } : null,
          r2 ? { l: r2[0], v: r2[1] } : null
        ]);
      }
    });

    // ── COMMENTS ────────────────────────────────────────────────────────────
    if (data.comments) {
      cardHead('Comments / Additional Notes');
      pb(20);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5);
      doc.setTextColor(DARK[0], DARK[1], DARK[2]);
      var cLines = doc.splitTextToSize(data.comments, CW - 16);
      cLines.forEach(function (line) {
        pb(14);
        doc.text(line, M + 8, y + 12);
        y += 14;
      });
      y += 8;
    }

    // ── FOOTER on every page ─────────────────────────────────────────────────
    var total = doc.getNumberOfPages();
    for (var pi = 1; pi <= total; pi++) {
      doc.setPage(pi);
      doc.setDrawColor(180, 195, 210); doc.setLineWidth(0.5);
      doc.line(M, PH - 44, PW - M, PH - 44);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(7.5);
      doc.setTextColor(MUTED[0], MUTED[1], MUTED[2]);
      doc.text('J. Jacobs & Associates Insurance  •  jjainsurance.com  •  (248) 693-6455  •  Lake Orion, Michigan', M, PH - 30);
      doc.text('Page ' + pi + ' of ' + total, PW - M - 44, PH - 30);
      doc.setFontSize(7); doc.setTextColor(160, 170, 185);
      doc.text('This document summarizes your quote request. A licensed agent will contact you within one business day.', M, PH - 18);
    }

    return doc.output('datauristring').split(',')[1];
  }

  // ── Download trigger ───────────────────────────────────────────────────────

  var _capturedData   = null;
  var _capturedPDFb64 = null;   // cached at submit time so download works after form.hidden

  function triggerPDFDownload() {
    if (!_capturedPDFb64) return;
    var btn = document.getElementById('btn-download-pdf');
    if (btn) { btn.disabled = true; btn.textContent = 'Generating PDF…'; }

    setTimeout(function () {
      try {
        var b64 = _capturedPDFb64;
        if (b64) {
          var a = document.createElement('a');
          a.href = 'data:application/pdf;base64,' + b64;
          var fname = (_capturedData && _capturedData.contact.name || 'quote').toLowerCase().replace(/\s+/g, '-');
          a.download = 'quote-summary-' + fname + '-' + new Date().toISOString().slice(0, 10) + '.pdf';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          if (btn) btn.textContent = 'Download Again';
        } else {
          if (btn) btn.textContent = 'Download Quote Summary (PDF)';
        }
      } catch (err) {
        if (btn) btn.textContent = 'Download Quote Summary (PDF)';
      }
      if (btn) btn.disabled = false;
    }, 80);
  }

  // ── Init ──────────────────────────────────────────────────────────────────

  function init() {
    var form = document.getElementById('quote-form');
    if (!form) return;

    // Worker endpoint — falls back to hardcoded URL if the attribute is missing
    var workerUrl = (form.dataset && form.dataset.worker)
      ? form.dataset.worker
      : 'https://jja-al3-worker.jacobs31.workers.dev';

    // Download button listener (delegated — button is outside the form)
    document.addEventListener('click', function (e) {
      if (e.target && (e.target.id === 'btn-download-pdf' || e.target.closest('#btn-download-pdf'))) {
        triggerPDFDownload();
      }
    });

    // ── Form submit override ──
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Turnstile gate — make sure the human-check produced a token before we
      // send. An empty token means the challenge has not completed (or the
      // Turnstile script was blocked). The Worker would reject it anyway; this
      // gives the visitor a clear message instead of a generic send error.
      var tsField = form.querySelector('[name="cf-turnstile-response"]');
      if (!tsField || !tsField.value) {
        var tsWidget = form.querySelector('.cf-turnstile');
        if (tsWidget) tsWidget.scrollIntoView({ behavior: 'smooth', block: 'center' });
        alert('Please complete the "I\'m not a robot" check just above the Submit button, then submit again.\n\nIf you don\'t see it, please call us at (248) 693-6455 and we\'ll gladly take your information by phone.');
        return;
      }

      var submitBtn = form.querySelector('[type=submit]');
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }

      // Collect structured data (for PDF generation)
      _capturedData = collectFormData();

      // Generate PDF now — included as base64 attachment in the Worker email
      var pdfB64 = generateQuotePDF(_capturedData); // null if jsPDF not loaded
      _capturedPDFb64 = pdfB64; // cache so download button can reuse after form.hidden

      // Convert FormData to a plain object so we can JSON-serialize it
      // (hidden/disabled fields are already excluded by the pre-submit handler)
      var fd = new FormData(form);
      var formObj = {};
      fd.forEach(function (val, key) {
        if (formObj[key] !== undefined) {
          formObj[key] = formObj[key] + ',' + val;
        } else {
          formObj[key] = val;
        }
      });

      // POST JSON to the Cloudflare Worker
      fetch(workerUrl, {
        method:  'POST',
        body:    JSON.stringify({ formData: formObj, pdf_b64: pdfB64 || null }),
        headers: { 'Content-Type': 'application/json' }
      })
      .then(function (res) {
        if (!res.ok) throw new Error('status ' + res.status);

        // GA4 conversion: a real quote request was submitted successfully.
        // GA4 attributes this to the session's landing page automatically.
        try {
          if (window.gtag) window.gtag('event', 'generate_lead', {
            form_type: 'quote',
            page_path: (location.pathname || '/quotes/')
          });
        } catch (e) {}

        // Hide form, show success state
        form.hidden = true;

        var success = document.getElementById('quote-success');
        if (success) {
          var firstNameEl = success.querySelector('[data-firstname]');
          if (firstNameEl && _capturedData && _capturedData.contact.name) {
            firstNameEl.textContent = _capturedData.contact.name.split(' ')[0];
          }
          success.hidden = false;
          success.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      })
      .catch(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Submit Quote Request';
        }
        alert('There was a problem sending your request.\nPlease try again or call us at (248) 693-6455.');
      });
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
