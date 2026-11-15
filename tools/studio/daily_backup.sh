#!/usr/bin/env bash
# daily_backup.sh — Daily backup of the project-eternia repo (real-developers batch).
# Creates a dated git bundle (ALL branches) + a zip of untracked-but-important
# work files, into ~/workspace/cloud-sync/backups/, keeps the last 7 of each,
# and appends one log line per run to backups/backup.log.
#
# Usage:  tools/studio/daily_backup.sh            (run from anywhere)
# Cron:   runs daily (see cron job "eternia-daily-backup").
#
# NOTES:
# - This is a LOCAL backup only. Syncing to the Hugging Face cloud repo
#   (https://huggingface.co/datasets/gfhtgfghfcvvf/eternia-studio-assets)
#   stays MANUAL via the signed-in browser upload — no API token exists
#   and this script never creates one or any credential.
# - The bundle is verified with `git bundle verify` before the run is
#   logged as OK. A failed verify exits non-zero and logs FAIL.
# - Barone rule (research report §9/§11 item 6): a solo dev with no backup
#   nearly lost a year of work. This script is the fix.

set -euo pipefail

REPO="$HOME/workspace/project-eternia"
DEST="$HOME/workspace/cloud-sync/backups"
KEEP=7
DATE="$(date +%Y%m%d-%H%M%S)"
LOG="$DEST/backup.log"

mkdir -p "$DEST"

BUNDLE="$DEST/project-eternia-$DATE.bundle"
ZIP="$DEST/project-eternia-untracked-$DATE.zip"

# 1. Git bundle of all branches (+ HEAD).
git -C "$REPO" bundle create "$BUNDLE" --all >/dev/null
git -C "$REPO" bundle verify "$BUNDLE" >/dev/null
BUNDLE_SIZE="$(du -h "$BUNDLE" | cut -f1)"

# 2. Zip of untracked-but-important files (git-ignored junk excluded by
#    --exclude-standard, e.g. .godot/ cache). Skipped when there is nothing.
UNTRACKED="$(git -C "$REPO" ls-files --others --exclude-standard | wc -l)"
if [ "$UNTRACKED" -gt 0 ]; then
    git -C "$REPO" ls-files --others --exclude-standard -z \
        | (cd "$REPO" && zip -q -@ "$ZIP")
    ZIP_SIZE="$(du -h "$ZIP" | cut -f1)"
    ZIP_NOTE="untracked=$UNTRACKED ($ZIP_SIZE)"
else
    ZIP_NOTE="untracked=0 (no zip)"
fi

# 2b. Patch of uncommitted modifications to TRACKED files. A bundle holds
#     commits only — without this, a day of uncommitted work would be lost
#     with the disk. Skipped when the tree is clean.
PATCH="$DEST/project-eternia-uncommitted-$DATE.patch"
if [ -n "$(git -C "$REPO" status --porcelain | grep -v '^??')" ]; then
    git -C "$REPO" diff > "$PATCH"
    PATCH_NOTE="uncommitted-diff=$(du -h "$PATCH" | cut -f1)"
else
    PATCH_NOTE="uncommitted-diff=none (clean tree)"
fi

# 3. Prune: keep only the newest $KEEP bundles, zips and patches.
#    (|| true: ls exits 2 when a glob matches nothing — e.g. no patches yet
#    on a clean tree — and set -e + pipefail would otherwise kill the run.)
(cd "$DEST" && ls -t project-eternia-*.bundle 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f) || true
(cd "$DEST" && ls -t project-eternia-untracked-*.zip 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f) || true
(cd "$DEST" && ls -t project-eternia-uncommitted-*.patch 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm -f) || true

echo "$DATE OK bundle=$BUNDLE ($BUNDLE_SIZE) $ZIP_NOTE $PATCH_NOTE" >> "$LOG"
echo "Backup OK: $BUNDLE ($BUNDLE_SIZE) | $ZIP_NOTE | $PATCH_NOTE"
