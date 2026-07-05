#!/usr/bin/env python3
r"""
checkpoint.py — JJA "we finished something" ritual.

Run this from C:\Website at the end of each work session:

    python checkpoint.py

It does two things, in order:
  1. update_handoff.py  — regenerates the AUTO:STATE block in PROJECT-HANDOFF.md
                          (and mirrors it to PROJECT-CONTEXT.md) so the handoff is current.
  2. backup_website.py  — zips C:\Website (+ KB + worker) to C:\AI Backup, which
                          Google Drive for Desktop syncs to the cloud. Keeps the 2 most
                          recent zips per folder.

Run it on the real machine (not a cloud-sync sandbox copy): update_handoff.py reads the
live files, and a stale/truncated sandbox copy could regenerate the handoff from bad input.

Flags:
    --no-backup     update the handoff only (skip the backup)
    --dry-run       pass through to update_handoff.py (preview, no writes); skips backup
"""

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(script, extra=None):
    path = BASE / script
    if not path.exists():
        print(f"  ! {script} not found at {path} — skipping.")
        return False
    cmd = [sys.executable, str(path)] + (extra or [])
    print(f"\n=== running {script} {' '.join(extra or [])}===")
    result = subprocess.run(cmd, cwd=str(BASE))
    ok = result.returncode == 0
    print(f"=== {script} {'OK' if ok else 'FAILED (exit %d)' % result.returncode} ===")
    return ok


def main():
    dry = "--dry-run" in sys.argv
    no_backup = "--no-backup" in sys.argv or dry

    print("JJA checkpoint — refresh handoff" + ("" if no_backup else " + backup"))

    ok_handoff = run("update_handoff.py", ["--dry-run"] if dry else None)

    ok_backup = True
    if not no_backup:
        ok_backup = run("backup_website.py")
    else:
        print("\n(skipping backup)")

    print("\n--- checkpoint summary ---")
    print(f"  handoff update : {'OK' if ok_handoff else 'check output above'}")
    print(f"  backup         : {'skipped' if no_backup else ('OK' if ok_backup else 'check output above')}")
    print("Done.")
    sys.exit(0 if (ok_handoff and ok_backup) else 1)


if __name__ == "__main__":
    main()
