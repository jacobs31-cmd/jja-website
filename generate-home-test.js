#!/usr/bin/env node
'use strict';

// ─── helpers ──────────────────────────────────────────────────────────────────
const rpad  = (s, n) => (s == null ? '' : String(s)).slice(0, n).padEnd(n, ' ');
const mkSeg = (lvl, code, data) => {
  const total = 7 + data.length;
  if (String(total).length > 3) throw new Error(`Segment ${code} total ${total} overflows 3 digits`);
  return `${lvl}${code}${String(total).padStart(3,'0')}${data}`;
};

// Slot a value into a fixed-width string at an absolute data position
const slot = (str, pos, val) =>
  str.slice(0, pos) + val + str.slice(pos + val.length);

// Standard 23-char preamble:  spaces(3) + ownId(6) + parentLvl(1)+parentCode(3)+parentId(6) + spaces(4)
const mkPre = (ownId, pLvl, pCode, pId) =>
  `   ${rpad(ownId,6)}${pLvl}${pCode}${rpad(pId,6)}    `;

// Top-level preamble (no parent): spaces(3) + ownId(6) + spaces(10) + spaces(4) = 23
const topPre = ownId => `   ${rpad(ownId,6)}          ` + '    ';

// Date/time
const now       = new Date();
const YYMMDD    = now.toISOString().slice(2,10).replace(/-/g,'');
const YYYYMMDD  = now.toISOString().slice(0,10).replace(/-/g,'');
const HHMM      = now.toISOString().slice(11,16).replace(':','');

// ISO date -> YYMMDD / YYYYMMDD
const fmt6 = iso => iso ? iso.replace(/-/g,'').slice(2,8) : '      ';
const fmt8 = iso => iso ? iso.replace(/-/g,'').slice(0,8)  : '        ';

const genderCode = v =>
  v && v[0].toLowerCase()==='m' ? 'M' :
  v && v[0].toLowerCase()==='f' ? 'F' : ' ';

// ─── home-specific helpers ─────────────────────────────────────────────────────
// 8-char dollar amount (e.g. $350,000 -> '00350000')
const homeAmt = v => {
  const n = parseInt(String(v||0).replace(/[^0-9]/g,'')) || 0;
  return String(n).padStart(8,'0').slice(-8);
};
// 5-char deductible (e.g. $1,000 -> '01000')
const homeDed = v => {
  const n = parseInt(String(v||0).replace(/[^0-9]/g,'')) || 0;
  return String(n).padStart(5,'0').slice(-5);
};

const storiesCode = v => {
  if (/tri.?level|split/i.test(v||'')) return '02'; // tri-level -> treat as 2-story
  if (/3/.test(v||''))                 return '03';
  if (/2/.test(v||''))                 return '02';
  if (/1\.5|half/i.test(v||''))        return '15';
  return '01';
};
const constrCode = v => {
  if (/brick/i.test(v||'') && !/wood/i.test(v||'')) return 'DM';
  if (/log/i.test(v||''))  return 'DL';
  return 'DW'; // wood frame default
};
// Heat source: G=Gas, E=Electric, O=Oil
// Handles full form option text: "Natural gas (forced air)", "Electric", "Fuel oil", etc.
const heatCode = v => {
  if (/gas/i.test(v||''))      return 'G';
  if (/electric/i.test(v||'')) return 'E';
  if (/oil/i.test(v||''))      return 'O';
  return ' ';
};
// Burglar alarm: A=central/monitored, L=local/self-monitored, blank=none
// Handles: "Yes -- professionally monitored", "Yes -- self-monitored (app only)", "No"
const alarmCode = v => {
  if (/professional|central|monitor/i.test(v||'')) return 'A';
  if (/local|self/i.test(v||''))                   return 'L';
  return ' ';
};
// Pool code: I=inground, O=above-ground, H=hot tub, blank=none
const poolCode = v => {
  if (/inground/i.test(v||''))      return 'I';
  if (/above.?ground/i.test(v||'')) return 'O';
  if (/hot tub|spa/i.test(v||''))   return 'H';
  if (/yes/i.test(v||''))           return 'O'; // fallback
  return ' ';
};
// Renovation block: 5-char YYYYC group, or 5 spaces if no year
const renovBlock = year =>
  (year && /^\d{4}$/.test(String(year).trim())) ? `${year}C` : '     ';
// Living area in HRU: hundreds, 2-char zero-padded (2200 sq ft -> '22')
const livingArea = sqft => {
  const n = Math.round(parseInt(String(sqft||'0').replace(/[^0-9]/g,'')) / 100);
  return String(Math.min(n, 99)).padStart(2,'0');
};

// ─── test form data ────────────────────────────────────────────────────────────
const form = {
  first_name: 'Joseph', last_name: 'Smith',
  email: 'joseph.smith@email.com', phone: '2485551234',
  street_address: '4567 Oak Hill Dr', city: 'Lake Orion', state: 'MI', zip: '48360',
  dob: '1975-06-15', gender: 'Male', occupation: 'Engineer',
  spouse_first_name: 'Linda', spouse_last_name: 'Smith', spouse_dob: '1977-09-22',

  // Property
  home_address:      '',           // blank = use mailing address
  year_built:        '1998',
  home_stories:      '2 stories',
  home_construction: 'Wood frame',
  home_roof_year:    '2018',

  // Underwriting / HRU fields
  // home_sqft and home_basement_sqft are test-only; real form uses type selects
  home_sqft:           '2200',       // total living area (sq ft) -- test value
  home_basement_sqft:  '1000',       // basement area (sq ft) -- test value for probing REP[33:38]
  home_garage_sqft:    '400',        // garage area (sq ft) -- test value for probing IIG positions
  // Form field values (match actual quote form option text exactly):
  home_heat:           'Natural gas (forced air)',
  home_alarm:          'Yes -- professionally monitored',
  home_stove:          'Yes',
  home_purchase_date:  '2006-02-04', // YYYY-MM-DD
  home_pool:           'Yes -- above-ground pool',
  home_dogs:           'Yes',
  home_dog_breed:      'Other',  // using 'OT  ' to confirm breed position works
  home_dog_bite:       'No',
  home_wiring_year:    '2002',       // 4-digit year of rewiring, or blank
  home_plumbing_year:  '2002',       // 4-digit year of plumbing update, or blank
  home_heating_year:   '2002',       // 4-digit year of heating system update, or blank

  // Coverages
  home_cov_a:           '$350,000',
  home_cov_b:           '$35,000',
  home_liability:       '$300,000',
  home_deductible:      '$1,000',
  home_water_backup:    '$25,000',
  home_service_line:    'Yes -- add it',
  home_personal_injury: 'Yes',
  home_jewelry_amt:     '$5,000',
  home_firearms_amt:    '$2,500',
};

// ─── generateHomeAL3 ──────────────────────────────────────────────────────────
function generateHomeAL3(f) {
  const hasSpouse    = !!(f.spouse_first_name && f.spouse_last_name);
  const displayFirst = hasSpouse
    ? `${f.first_name} & ${f.spouse_first_name}` : (f.first_name || '');

  const riskStreet = f.home_address || f.street_address || '';
  const riskCity   = f.city  || '';
  const riskState  = f.state || 'MI';
  const riskZip    = (f.zip  || '').slice(0,5);

  let cvhN = 1;
  const nextCvhId = () => `W${String(cvhN++).padStart(5,'0')}`;

  // ── assert helper ──────────────────────────────────────────────────────────
  const check = (label, data, expected) => {
    if (data.length !== expected)
      throw new Error(`${label}: data length ${data.length}, expected ${expected}`);
  };

  // ── CVH segment builder (total=323, data=316) ──────────────────────────────
  const buildCVH = (ownId, code, limitAmt, ded, limitType, desc) => {
    const p  = mkPre(ownId, '6', 'HRU', 'R10001');  // 23 chars
    let fd = '';
    fd += rpad(code,        5);   // [23:28]
    fd += rpad('',         25);   // [28:53]
    fd += rpad('',         12);   // [53:65]  premium blank
    fd += rpad('',         30);   // [65:95]
    fd += rpad(limitAmt||'', 8); // [95:103] limit amount
    fd += rpad(ded||'',      5); // [103:108] deductible
    fd += rpad('',         12);   // [108:120]
    fd += rpad(limitType||'',2); // [120:122] limit type
    fd += rpad('',         27);   // [122:149]
    fd += rpad(desc||'',   71);   // [149:220] description
    fd += rpad('',         96);   // [220:316]
    const data = p + fd;
    check(`CVH(${code})`, data, 316);
    return mkSeg('6','CVH',data);
  };

  // ── HRU segment builder (total=680, data=673) ──────────────────────────────
  // Positions confirmed from Hawksoft import/export testing:
  //   [23:26]  = 'HOF' (house, owner-occ, single-family)
  //   [26:30]  = year built (4-digit)
  //   [30]     = num families '1'
  //   [31:34]  = Feet from Hydrant (3-char: '100') -- confirmed from import; NOT basement
  //   [34:52]  = spaces (18)
  //   [52:54]  = construction ('DW'=wood frame,'DM'=masonry,'DL'=log)
  //   [54:59]  = spaces (5)
  //   [59]     = '1' (fixed field, matches export)
  //   [60:62]  = spaces (2)
  //   [62]     = Protection Class (1-char: '4') -- confirmed from import; NOT garage
  //   [63:67]  = spaces (4)
  //   [67:70]  = territory -- leave blank; Hawksoft auto-derives from address
  //   [70:72]  = spaces (2)
  //   [72]     = 'D' dwelling style
  //   [73:77]  = '0100' rooms code
  //   [77:79]  = '02' bath code
  //   [79:89]  = spaces (10)
  //   [89:92]  = '001' num units
  //   [92:114] = spaces (22)
  //   [114:116]= living area in hundreds (2-char: 2200->22) -- redundant; real import via IIG
  //   [116]    = space
  //   [117:119]= stories ('01','02','03','15') -- redundant; real import via REP
  //   [119:128]= spaces (9)
  //   [128]    = heat source ('G','E','O') confirmed import
  //   [129:132]= spaces (3)
  //   [132]    = burglar alarm ('A'=monitored,'L'=local) confirmed import
  //   [133:172]= spaces (39)
  //   [172:174]= wood stove ('DY'=yes) -- export position; import position still TBD
  //   [174:198]= spaces (24)
  //   [198:206]= purchase date (YYYYMMDD) confirmed import
  //   [206:218]= spaces (12)
  //   [218]    = pool ('I'=inground,'O'=above-ground,'H'=hot tub) confirmed import
  //   [219:229]= spaces (10)
  //   [229:234]= wiring renovation  (YYYYC or 5 spaces)
  //   [234:239]= plumbing renovation(YYYYC or 5 spaces)
  //   [239:244]= heating renovation (YYYYC or 5 spaces)
  //   [244:249]= roof renovation    (YYYYC or 5 spaces)
  //   [249:673]= spaces (424)
  const buildHRU = () => {
    const p = mkPre('R10001', '5', 'LAG', 'L10001');  // 23 chars
    let fd = '';
    fd += 'HOF';                                              // [23:26]  dwelling/occ/subtype
    fd += rpad(f.year_built || '',              4);           // [26:30]  year built
    fd += '1';                                                // [30]     num families
    fd += rpad('100',                           3);           // [31:34]  Feet from Hydrant (100 ft default)
    fd += rpad('',                             18);           // [34:52]  spaces
    fd += rpad(constrCode(f.home_construction), 2);           // [52:54]  construction
    fd += rpad('',                              5);           // [54:59]  spaces
    fd += '1';                                                // [59]     unknown fixed field
    fd += rpad('',                              2);           // [60:62]  spaces
    fd += '4';                                                // [62]     Protection Class (4 = default)
    fd += rpad('',                              4);           // [63:67]  spaces
    fd += rpad('EXV',                           3);           // [67:70]  territory probe (EXV)
    fd += rpad('',                              2);           // [70:72]  spaces
    fd += 'D';                                                // [72]     dwelling style
    fd += rpad('0100',                          4);           // [73:77]  rooms code
    fd += rpad('02',                            2);           // [77:79]  bath code
    fd += rpad('',                             10);           // [79:89]  spaces
    fd += '001';                                              // [89:92]  num units
    fd += rpad('',                             22);           // [92:114] spaces
    fd += livingArea(f.home_sqft);                            // [114:116]living area in hundreds
    fd += ' ';                                                // [116]    space
    fd += storiesCode(f.home_stories);                        // [117:119]stories
    fd += rpad('',                              9);           // [119:128]spaces
    fd += heatCode(f.home_heat);                              // [128]    heat source
    fd += rpad('',                              3);           // [129:132]spaces
    fd += alarmCode(f.home_alarm);                            // [132]    burglar alarm
    fd += rpad('',                             39);           // [133:172]spaces
    fd += /yes/i.test(f.home_stove || '') ? 'DY' : '  ';     // [172:174]wood stove (export pos)
    fd += '1';                                                // [174]     wood stove probe: count=1
    fd += rpad('',                             23);           // [175:198]spaces
    fd += fmt8(f.home_purchase_date);                         // [198:206]purchase date
    fd += rpad('',                             12);           // [206:218]spaces
    fd += poolCode(f.home_pool);                              // [218]    pool
    fd += rpad('',                             10);           // [219:229]spaces
    fd += renovBlock(f.home_wiring_year);                     // [229:234]wiring renovation
    fd += renovBlock(f.home_plumbing_year);                   // [234:239]plumbing renovation
    fd += renovBlock(f.home_heating_year);                    // [239:244]heating renovation
    fd += renovBlock(f.home_roof_year);                       // [244:249]roof renovation
    fd += rpad('',                            424);           // [249:673]remaining spaces
    const data = p + fd;
    check('HRU', data, 673);
    return mkSeg('6', 'HRU', data);
  };

  // ─── assemble segments ─────────────────────────────────────────────────────
  let out = '';

  // MHG (total=196, data=189)
  {
    let d = rpad('',189);
    d = slot(d,  9, 'HWKSFT');  // [9:15]  MUST be HWKSFT
    d = slot(d, 76, YYMMDD);    // [76:82] date YYMMDD
    d = slot(d, 82, ' ');
    d = slot(d, 83, HHMM);      // [83:87] time HHMM
    d = slot(d, 87, '   0');
    check('MHG', d, 189);
    out += mkSeg('1','MHG',d);
  }

  // TRG (total=212, data=205)
  {
    let d = rpad('',205);
    d = slot(d, 14, '3P ');
    d = slot(d, 17, 'PHOME');
    d = slot(d, 22, ' QTEBN');
    d = slot(d, 28, '0');
    d = slot(d,160, 'NBQ');
    check('TRG', d, 205);
    out += mkSeg('2','TRG',d);
  }

  // ACI (total=249, data=242)
  {
    let d = rpad('',242);
    d = slot(d,  0, 'A');
    d = slot(d,  4, rpad('J. Jacobs and Associates',60));
    d = slot(d, 64, rpad('4301 S. Baldwin Rd',60));
    d = slot(d,124, rpad('Lake Orion',19));
    d = slot(d,143, 'MI');
    d = slot(d,145, '48359');
    d = slot(d,154, '2486936455');
    check('ACI', d, 242);
    out += mkSeg('2','ACI',d);
  }

  // 5BIS Name (total=172, data=165)
  {
    let d = topPre('B10001') + rpad('',165-23);
    d = slot(d, 23, hasSpouse ? 'F' : 'I');
    d = slot(d, 32, rpad(displayFirst, 26));
    d = slot(d, 58, ' ');
    d = slot(d, 59, rpad(f.last_name||'',15));
    check('5BIS', d, 165);
    out += mkSeg('5','BIS',d);
  }

  // 9BIS Address (total=343, data=336)
  {
    let d = topPre('B10001') + rpad('',336-23);
    d = slot(d,  23, rpad(riskStreet,60));
    d = slot(d,  83, rpad(riskCity,19));
    d = slot(d, 102, rpad(riskState,2));
    d = slot(d, 104, rpad(riskZip,5));
    d = slot(d, 113, rpad((f.phone||'').replace(/[^0-9]/g,'').slice(0,10),10));
    check('9BIS', d, 336);
    out += mkSeg('9','BIS',d);
  }

  // 5ISI (total=275, data=268)
  {
    const p = mkPre('B20001','5','BIS','B10001');
    let d = p + rpad('',268-23);
    d = slot(d,  23, fmt6(f.dob));
    d = slot(d,  31, genderCode(f.gender));
    if (hasSpouse) d = slot(d, 34, fmt6(f.spouse_dob));
    d = slot(d,  46, rpad(f.occupation||'',20));
    d = slot(d, 120, fmt8(f.dob));
    if (hasSpouse) d = slot(d,128, fmt8(f.spouse_dob));
    check('ISI', d, 268);
    out += mkSeg('5','ISI',d);
  }

  // 5NID (total=125, data=118) -- required by Hawksoft, all blank
  {
    const p = mkPre('B20001','5','BIS','B10001');
    const d = p + rpad('',118-23);
    check('NID', d, 118);
    out += mkSeg('5','NID',d);
  }

  // 6COM Email (total=416, data=409)
  {
    const p = mkPre('F20001','5','BIS','B10001');
    let d = p + rpad('',409-23);
    d = slot(d, 23, 'EMAIL');
    d = slot(d, 28, rpad(f.email||'',50));
    check('COM', d, 409);
    out += mkSeg('6','COM',d);
  }

  // 5BPI (total=511, data=504)
  {
    const p = mkPre('F10001','5','BIS','B10001');
    let d = p + rpad('',504-23);
    d = slot(d,  23, 'H');
    d = slot(d,  24, rpad('WEB'+YYYYMMDD,15));
    d = slot(d,  64, 'HOME ');
    check('BPI', d, 504);
    out += mkSeg('5','BPI',d);
  }

  // 5LAG Location Address (total=636, data=629)
  {
    const p = mkPre('L10001','5','BPI','F10001');
    let d = p + rpad('',629-23);
    d = slot(d,  30, '0001');
    d = slot(d,  34, rpad(riskStreet,60));
    d = slot(d,  94, rpad(riskCity,19));
    d = slot(d, 113, rpad(riskState,2));
    d = slot(d, 115, rpad(riskZip,5));
    check('LAG', d, 629);
    out += mkSeg('5','LAG',d);
  }

  // 6HRU Home Risk Unit (total=680, data=673)
  out += buildHRU();

  // 5IIG Improvement Information Group (total=167, data=160)
  // Child of 6HRU R10001. Confirmed positions:
  //   [29:34] = total living area (5 chars, sq ft zero-padded: 2200->'02200') CONFIRMED
  //   [34:39] = PROBE 1 -- tried garage 400->'00400', Hawksoft showed blank
  //   [39:44] = PROBE 2 -- tried basement, did not import
  //   [44:49] = PROBE 3 -- garage probe round 2 (400->'00400')
  //   [49:54] = PROBE 4 -- garage probe round 3 (400->'00400')
  {
    const p = mkPre('R20001','6','HRU','R10001');
    let d = p + rpad('', 160-23);
    const sqft  = parseInt(String(f.home_sqft||'0').replace(/[^0-9]/g,'')) || 0;
    const gSqft = parseInt(String(f.home_garage_sqft||'0').replace(/[^0-9]/g,'')) || 0;
    d = slot(d, 29, String(sqft).padStart(5,'0'));         // [29:34] living area CONFIRMED
    d = slot(d, 44, String(gSqft).padStart(5,'0'));        // [44:49] garage PROBE 3
    d = slot(d, 49, String(gSqft).padStart(5,'0'));        // [49:54] garage PROBE 4
    check('IIG', d, 160);
    out += mkSeg('5','IIG',d);
  }

  // 5REP Replacement Cost segment (total=240, data=233)
  // Child of 6HRU R10001. Confirmed positions:
  //   [29:30] = stories (1 char: '1','2','3') CONFIRMED
  //   [33:38] = Basement Area (5 chars, sq ft zero-padded: 1000->'01000') CONFIRMED
  //             (v4 was accidentally sending living area here -- now fixed)
  {
    const p = mkPre('R20001','6','HRU','R10001');
    let d = p + rpad('', 233-23);
    const bSqft = parseInt(String(f.home_basement_sqft||'0').replace(/[^0-9]/g,'')) || 0;
    const sto   = storiesCode(f.home_stories).replace(/^0/,'') || '1'; // '1','2','3'
    d = slot(d, 29, sto);                                  // [29:30] stories CONFIRMED
    d = slot(d, 33, String(bSqft).padStart(5,'0'));        // [33:38] Basement Area CONFIRMED
    check('REP', d, 233);
    out += mkSeg('5','REP',d);
  }

  // 6AEI Animal/Dog segments (children of 6HRU R10001)
  // Layout confirmed from reference PL.al3 export (total=41, data=34):
  //   [23:26] = 'DOG'
  //   [26:28] = '  ' (2 spaces)
  //   [28:32] = 4-char breed code (e.g. 'CHOW', 'LAB ', 'GSHP', 'OT  '=Other)
  //   [32]    = ' '
  //   [33]    = bite indicator ('N'=never bitten, 'Y'=yes)
  const breedCode = name => {
    const n = (name||'').toLowerCase();
    if (/chow/i.test(n))                         return 'CHOW';
    if (/pit.?bull|staffordshire/i.test(n))      return 'PTBL';
    if (/rottweiler|rottw/i.test(n))             return 'ROTT';
    if (/german.?shep|gsd|alsatian/i.test(n))   return 'GSHP';
    if (/doberman/i.test(n))                     return 'DOBE';
    if (/akita/i.test(n))                        return 'AKIT';
    if (/malamute/i.test(n))                     return 'MALA';
    if (/husky|siberian/i.test(n))               return 'HUSK';
    if (/wolf/i.test(n))                         return 'WOLF';
    if (/labrador|lab\b/i.test(n))               return 'LAB ';
    if (/golden.?ret|golden/i.test(n))           return 'GOLD';
    if (/beagle/i.test(n))                       return 'BEAG';
    if (/bulldog/i.test(n))                      return 'BULL';
    if (/poodle/i.test(n))                       return 'POOD';
    return 'OT  '; // Other
  };
  if (/yes/i.test(f.home_dogs||'') && f.home_dog_breed) {
    let aeiN = 1;
    const breeds = f.home_dog_breed.split(/[,\/;]+/).map(s => s.trim()).filter(Boolean);
    const biteFlag = /yes/i.test(f.home_dog_bite||'') ? 'Y' : 'N';
    for (const breed of breeds) {
      const p = mkPre('R2000'+aeiN, '6', 'HRU', 'R10001');
      let d = p + rpad('', 34-23);  // 11 chars of content
      d = slot(d, 23, 'DOG');
      d = slot(d, 26, '  ');
      d = slot(d, 28, rpad(breedCode(breed), 4));
      d = slot(d, 32, ' ');
      d = slot(d, 33, biteFlag);
      check('AEI('+breed+')', d, 34);
      out += mkSeg('6','AEI',d);
      aeiN++;
    }
  }

  // CVH coverage segments (all children of HRU R10001)
  const covA    = homeAmt(f.home_cov_a);
  const covB    = homeAmt(f.home_cov_b);
  const ded     = homeDed(f.home_deductible);

  const covAnum = parseInt(String(f.home_cov_a||'0').replace(/[^0-9]/g,'')) || 0;
  const covPP   = homeAmt(Math.round(covAnum * 0.50));
  const covLOU  = homeAmt(Math.round(covAnum * 0.20));

  const liabNum = parseInt(String(f.home_liability||'300000').replace(/[^0-9]/g,'')) || 300000;
  const covPL   = homeAmt(liabNum);

  // DWELL: Coverage A, replacement cost
  out += buildCVH(nextCvhId(), 'DWELL', covA,   '',  'PC', 'Dwelling');
  // OS: Coverage B, other structures
  out += buildCVH(nextCvhId(), 'OS',    covB,   ded,  '', 'Other Structures');
  // PP: Coverage C, personal property (~50% of Cov A)
  out += buildCVH(nextCvhId(), 'PP',    covPP,  ded,  '', 'Personal Property');
  // LOU: Coverage D, loss of use (~20% of Cov A)
  out += buildCVH(nextCvhId(), 'LOU',   covLOU, ded,  '', 'Loss of Use');
  // PL: Coverage E, personal liability
  out += buildCVH(nextCvhId(), 'PL',    covPL,  '',   '', 'Personal Liability');
  // MEDPM: Coverage F, medical payments ($1,000 standard)
  out += buildCVH(nextCvhId(), 'MEDPM', '00001000', '', '', 'Medical Payments to Others');

  if (f.home_personal_injury && /yes/i.test(f.home_personal_injury)) {
    out += buildCVH(nextCvhId(), 'PIHOM', '', '', '', 'Personal Injury Coverage');
  }
  if (f.home_water_backup && !/no thanks/i.test(f.home_water_backup)) {
    out += buildCVH(nextCvhId(), 'SEWER',
      homeAmt(f.home_water_backup), '', '', 'Water Backup and Sump Overflow Coverage');
  }
  if (f.home_service_line && /yes/i.test(f.home_service_line)) {
    out += buildCVH(nextCvhId(), 'ESLC', '00020000', '', '', 'Service Line Coverage');
  }
  if (f.home_jewelry_amt && !/none|^0$/i.test(f.home_jewelry_amt.trim())) {
    out += buildCVH(nextCvhId(), 'VIP01',
      homeAmt(f.home_jewelry_amt), '', '', 'Jewelry Blanket');
  }
  if (f.home_firearms_amt && !/none|^0$/i.test(f.home_firearms_amt.trim())) {
    out += buildCVH(nextCvhId(), 'VIP01',
      homeAmt(f.home_firearms_amt), '', '', 'Firearms Blanket');
  }

  return out;
}

// run
const al3 = generateHomeAL3(form);
process.stdout.write(al3);
