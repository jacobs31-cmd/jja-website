// ============================================================================
// generateHomeAL3() — wired into al3-worker.js as of 2026-05-20
//
// All field positions confirmed by Hawksoft import testing (v5/v6 test files).
//
// Key confirmed positions (HRU data string, 0-indexed):
//   [23:26]  HOF   dwelling/owner-occ/single-family
//   [26:30]  year built (4-digit)
//   [30]     '1'   num families
//   [31:34]  '100' Feet from Hydrant (default)
//   [52:54]  DW/DM/DL construction code
//   [59]     '1'   fixed field
//   [62]     '4'   Protection Class (default)
//   [67:70]  EXV   territory (Hawksoft derives from address)
//   [72]     'D'   dwelling style
//   [73:77]  '0100' rooms code (→ 10 rooms)
//   [77:79]  '02'  fire station distance (→ 2 miles)
//   [89:92]  '001' num units
//   [114:116] living area in hundreds (2-char zero-padded)
//   [117:119] stories ('01','02','03','15')
//   [128]    heat source G/E/O
//   [132]    burglar alarm A/L
//   [172:174] wood stove 'DY' (export pos; import pos still TBD)
//   [174]    wood stove probe '1'
//   [198:206] purchase date YYYYMMDD
//   [218]    pool I/O/H
//   [229:249] renovations: wiring/plumbing/heating/roof in YYYYC blocks
//
// IIG segment (total=167, data=160, child of 6HRU R10001):
//   [29:34]  total living area (5-char sq ft, zero-padded) CONFIRMED
//
// REP segment (total=240, data=233, child of 6HRU R10001):
//   [29:30]  stories (1-char: '1','2','3') CONFIRMED
//   [33:38]  basement area (5-char sq ft, zero-padded) CONFIRMED
//
// AEI segment (total=41, data=34, child of 6HRU R10001):
//   [23:26]='DOG', [28:32]=4-char breed code, [33]='N'/'Y' bite
// ============================================================================
//
// This file is reference-only. The live function is in al3-worker.js.
