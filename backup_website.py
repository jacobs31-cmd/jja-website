"""
backup_website.py — JJA Nightly Backup Script
==============================================
Backs up C:\\Website, C:\\JJA Knowledge Base, and C:\\worker to C:\\AI Backup.
Google Drive for Desktop syncs that folder automatically to the cloud.
Keeps the 2 most recent zip files for each folder.

Run manually:   python "C:\\Website\\backup_website.py"
Scheduled:      Windows Task Scheduler runs this daily at midnight (see setup_backup_task.ps1)
"""

import os
import zipfile
import datetime
import glob
import sys
import subprocess

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

# Folders to back up — add more entries here if needed in the future
BACKUP_TARGETS = [
    {
        "folder":  r"C:\Website",
        "label":   "JJA_Website",
        "exclude": {"backup_website.py", "backup_log.txt", "setup_backup_task.ps1",
                    ".git", "__pycache__"},
    },
    {
        "folder":  r"C:\JJA Knowledge Base",
        "label":   "JJA_KnowledgeBase",
        "exclude": {"__pycache__"},
    },
    {
        "folder":  r"C:\worker",
        "label":   "JJA_WebIntake",
        "exclude": {"node_modules", ".wrangler", ".git", "__pycache__",
                    ".tmp.driveupload", ".tmp.drivedownload", "_backups"},
    },
    {
        "folder":  r"C:\Claude Projects\Marketing",
        "label":   "JJA_Marketing",
        "exclude": {"__pycache__", ".git"},
    },
]

# Backups go here — Google Drive for Desktop syncs this folder to the cloud.
BACKUP_FOLDER = r"C:\AI Backup"

MAX_BACKUPS = 2       # number of recent backups to keep per folder
LOG_FILE    = r"C:\AI Backup\backup_log.txt"

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # log write failure is non-fatal


def ensure_backup_folder() -> str:
    """Create C:\\AI Backup if it doesn't exist and return the path."""
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    return BACKUP_FOLDER


def zip_folder(source_folder: str, label: str, exclude: set, dest_folder: str) -> str:
    """Zip source_folder into dest_folder and return the zip path."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name  = f"{label}_Backup_{timestamp}.zip"
    zip_path  = os.path.join(dest_folder, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_folder):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file in exclude:
                    continue
                abs_path = os.path.join(root, file)
                arc_name = os.path.relpath(abs_path, source_folder)
                zf.write(abs_path, arc_name)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    log(f"Created: {zip_name} ({size_mb:.1f} MB)")
    return zip_path


def prune_old_backups(label: str, dest_folder: str):
    """Delete all but the MAX_BACKUPS most recent zips for this label."""
    pattern = os.path.join(dest_folder, f"{label}_Backup_*.zip")
    zips = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    for old_zip in zips[MAX_BACKUPS:]:
        os.remove(old_zip)
        log(f"Deleted old backup: {os.path.basename(old_zip)}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    log("=== JJA Nightly Backup Starting ===")

    # Tidy superseded handoff copies before backing up.
    # SAFE: archive_stale_docs.py only moves HANDOFF-<something>.md into C:\worker\_archive.
    # Wrapped so a failure here can never stop the backup.
    try:
        archive_script = r"C:\worker\archive_stale_docs.py"
        if os.path.isfile(archive_script):
            r = subprocess.run([sys.executable, archive_script],
                               capture_output=True, text=True, timeout=120)
            for line in (r.stdout or "").splitlines():
                log("[archive] " + line)
            if r.returncode != 0:
                log(f"[archive] non-zero exit {r.returncode}: {(r.stderr or '').strip()[:200]}")
    except Exception as e:
        log(f"[archive] skipped (non-fatal): {e}")

    dest_folder = ensure_backup_folder()
    log(f"Saving to: {dest_folder}")

    errors = 0
    for target in BACKUP_TARGETS:
        folder  = target["folder"]
        label   = target["label"]
        exclude = target["exclude"]

        if not os.path.isdir(folder):
            log(f"WARNING: Folder not found, skipping — {folder}")
            errors += 1
            continue

        log(f"--- Backing up {folder} ---")
        zip_folder(folder, label, exclude, dest_folder)
        prune_old_backups(label, dest_folder)

    if errors:
        log(f"=== Backup Complete with {errors} warning(s) ===\n")
    else:
        log("=== Backup Complete ===\n")


if __name__ == "__main__":
    main()
