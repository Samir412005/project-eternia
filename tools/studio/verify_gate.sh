#!/bin/bash
# PROJECT ETERNIA — Studio verification gate.
#
# Runs four gates in order and prints PASS/FAIL per gate + a final verdict.
#   Gate 1 — Headless import: 0 SCRIPT ERRORs
#   Gate 2 — gdUnit tests: 5/5 PASS (exit 0, no FAILED)
#   Gate 3 — Real screenshots: exist, >= 10 KB, non-black (PIL mean luminance)
#   Gate 4 — Android APK: export exit 0 + apksigner v1+v2+v3, 1 signer
#
# THE GATE REPORTS ONLY. It never fixes game files, never commits, never
# touches scenes, scripts or assets. Run it from anywhere:
#   ./tools/studio/verify_gate.sh [--skip-apk]
# The --skip-apk flag skips Gate 4 (slow export) for quick checks.
#
# Exit code: 0 only if ALL gates PASS. Anything else = NOT READY.
set -u

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
GODOT="${GODOT_BIN:-$HOME/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64}"
JDK="$HOME/workspace/game-apk/tools/jdk17"
APKSIGNER="$HOME/workspace/game-apk/tools/android-sdk/build-tools/34.0.0/apksigner"
TMPDIR="/tmp/studio-gate"
LOG="$PROJECT_DIR/reports/studio-gate-$(date +%Y%m%d-%H%M%S).log"
SKIP_APK=0
[ "${1:-}" = "--skip-apk" ] && SKIP_APK=1

mkdir -p "$PROJECT_DIR/reports" "$TMPDIR"
PASS_COUNT=0
FAIL_COUNT=0
{
echo "================================================================"
echo "STUDIO VERIFICATION GATE — PROJECT ETERNIA"
echo "Date (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Project: $PROJECT_DIR"
echo "Branch: $(cd "$PROJECT_DIR" && git branch --show-current 2>/dev/null || echo unknown)"
echo "Godot: $GODOT"
echo "================================================================"
} | tee "$LOG"

gate_result() { # $1 = name, $2 = PASS|FAIL, $3 = detail
  if [ "$2" = "PASS" ]; then PASS_COUNT=$((PASS_COUNT + 1)); else FAIL_COUNT=$((FAIL_COUNT + 1)); fi
  echo "[$2] $1 — $3" | tee -a "$LOG"
}

# ---------------------------------------------------------------- Gate 1
echo "--- Gate 1: headless import ---" | tee -a "$LOG"
IMPORT_LOG="$TMPDIR/gate1-import.log"
timeout 300 "$GODOT" --headless --path "$PROJECT_DIR" --import >"$IMPORT_LOG" 2>&1
IMPORT_EXIT=$?
SCRIPT_ERRORS=$(grep -ci "script error" "$IMPORT_LOG" || true)
echo "import exit=$IMPORT_EXIT, SCRIPT ERROR lines=$SCRIPT_ERRORS" | tee -a "$LOG"
if [ "$IMPORT_EXIT" -eq 0 ] && [ "$SCRIPT_ERRORS" -eq 0 ]; then
  gate_result "Gate 1 — headless import" "PASS" "exit 0, 0 SCRIPT ERRORs"
else
  gate_result "Gate 1 — headless import" "FAIL" "exit=$IMPORT_EXIT, SCRIPT ERRORs=$SCRIPT_ERRORS (see $IMPORT_LOG)"
  grep -i "script error" "$IMPORT_LOG" | head -10 | tee -a "$LOG" || true
fi

# ---------------------------------------------------------------- Gate 2
echo "--- Gate 2: gdUnit tests ---" | tee -a "$LOG"
GDUNIT_LOG="$TMPDIR/gate2-gdunit.log"
timeout 300 "$GODOT" --headless --path "$PROJECT_DIR" \
  -s addons/gdUnit4/bin/GdUnitCmdTool.gd --ignoreHeadlessMode -a tests/gdunit \
  >"$GDUNIT_LOG" 2>&1
GDUNIT_EXIT=$?
# gdUnit prints a summary line; capture it for the report.
GDUNIT_SUMMARY=$(grep -E "tests? (passed|failed)|TESTS (PASSED|FAILED)|SUCCESS|FAILURE" "$GDUNIT_LOG" | tail -3 | tr '\n' ' ' || true)
FAILED_LINES=$(grep -ci "failed" "$GDUNIT_LOG" || true)
echo "gdunit exit=$GDUNIT_EXIT, 'failed' lines=$FAILED_LINES" | tee -a "$LOG"
[ -n "$GDUNIT_SUMMARY" ] && echo "summary: $GDUNIT_SUMMARY" | tee -a "$LOG"
if [ "$GDUNIT_EXIT" -eq 0 ] && [ "$FAILED_LINES" -eq 0 ]; then
  gate_result "Gate 2 — gdUnit tests" "PASS" "exit 0, no FAILED lines${GDUNIT_SUMMARY:+; $GDUNIT_SUMMARY}"
else
  gate_result "Gate 2 — gdUnit tests" "FAIL" "exit=$GDUNIT_EXIT, FAILED lines=$FAILED_LINES (see $GDUNIT_LOG)"
fi

# ---------------------------------------------------------------- Gate 3
echo "--- Gate 3: real screenshots ---" | tee -a "$LOG"
SHOT_LOG="$TMPDIR/gate3-shots.log"
python3 - "$PROJECT_DIR/screenshots-aetheria" >"$SHOT_LOG" 2>&1 <<'PYEOF'
import os, sys
from PIL import Image
shot_dir = sys.argv[1]
files = sorted(f for f in os.listdir(shot_dir) if f.lower().endswith(".png"))
if not files:
    print("NO_SCREENSHOTS")
    sys.exit(1)
bad = 0
for name in files:
    path = os.path.join(shot_dir, name)
    size = os.path.getsize(path)
    try:
        with Image.open(path) as im:
            w, h = im.size
            gray = im.convert("L").resize((64, 36))
            mean = sum(gray.getdata()) / (64 * 36)
    except Exception as e:
        print(f"BAD {name}: unreadable ({e})")
        bad += 1
        continue
    status = "OK"
    if size < 10 * 1024 or mean < 2.0 or mean > 253.0:
        status = "BAD"
        bad += 1
    print(f"{status} {name}: {w}x{h}, {size} bytes, mean luminance {mean:.1f}")
print(f"TOTAL {len(files)} screenshots, {bad} bad")
sys.exit(1 if bad else 0)
PYEOF
SHOT_EXIT=$?
cat "$SHOT_LOG" | tee -a "$LOG"
if [ "$SHOT_EXIT" -eq 0 ]; then
  gate_result "Gate 3 — real screenshots" "PASS" "all screenshots exist, >= 10 KB, non-black"
else
  gate_result "Gate 3 — real screenshots" "FAIL" "see $SHOT_LOG"
fi

# ---------------------------------------------------------------- Gate 4
if [ "$SKIP_APK" -eq 1 ]; then
  echo "--- Gate 4: Android APK — SKIPPED (--skip-apk) ---" | tee -a "$LOG"
else
  echo "--- Gate 4: Android APK export + signature ---" | tee -a "$LOG"
  APK="$TMPDIR/eternia-gate.apk"
  rm -f "$APK" "$APK.idsig"
  EXPORT_LOG="$TMPDIR/gate4-export.log"
  # NOTE: Godot's export subprocess runs apksigner itself, and apksigner
  # needs java on PATH — without it the export succeeds but the APK is
  # UNSIGNED (verified 2026-11-15: "All located 'apksigner' tools failed
  # to execute"). So the export runs with jdk17/bin on PATH.
  timeout 600 env PATH="$JDK/bin:$PATH" "$GODOT" --headless --path "$PROJECT_DIR" \
    --export-release "Android Mobile" "$APK" >"$EXPORT_LOG" 2>&1
  EXPORT_EXIT=$?
  echo "export exit=$EXPORT_EXIT" | tee -a "$LOG"
  if [ "$EXPORT_EXIT" -ne 0 ] || [ ! -f "$APK" ]; then
    gate_result "Gate 4 — Android APK" "FAIL" "export exit=$EXPORT_EXIT, APK missing (see $EXPORT_LOG)"
    tail -15 "$EXPORT_LOG" | tee -a "$LOG" || true
  else
    APK_SIZE=$(stat -c%s "$APK")
    VERIFY_LOG="$TMPDIR/gate4-apksigner.log"
    # NOTE: apksigner 0.9 prints the scheme lines only with -v ("Verified
    # using v1 scheme (JAR signing): true"). Plain --print-certs prints
    # only the signer certs, so the v1/v2/v3 greps must use -v.
    JAVA_HOME="$JDK" PATH="$JDK/bin:$PATH" "$APKSIGNER" verify -v --print-certs "$APK" >"$VERIFY_LOG" 2>&1
    VERIFY_EXIT=$?
    V1=$(grep -c "Verified using v1 scheme (JAR signing): true" "$VERIFY_LOG" || true)
    V2=$(grep -c "Verified using v2 scheme (APK Signature Scheme v2): true" "$VERIFY_LOG" || true)
    V3=$(grep -c "Verified using v3 scheme (APK Signature Scheme v3): true" "$VERIFY_LOG" || true)
    SIGNERS=$(grep -o "Number of signers: [0-9]*" "$VERIFY_LOG" | grep -o "[0-9]*" || echo 0)
    echo "apk size=$APK_SIZE bytes, apksigner exit=$VERIFY_EXIT, v1=$V1 v2=$V2 v3=$V3 signers=$SIGNERS" | tee -a "$LOG"
    if [ "$VERIFY_EXIT" -eq 0 ] && [ "$V1" -eq 1 ] && [ "$V2" -eq 1 ] && [ "$V3" -eq 1 ] && [ "$SIGNERS" = "1" ] && [ "$APK_SIZE" -gt 10000000 ]; then
      gate_result "Gate 4 — Android APK" "PASS" "$APK_SIZE bytes, v1+v2+v3 verified, 1 signer"
    else
      gate_result "Gate 4 — Android APK" "FAIL" "verify exit=$VERIFY_EXIT v1=$V1 v2=$V2 v3=$V3 signers=$SIGNERS size=$APK_SIZE (see $VERIFY_LOG)"
    fi
  fi
fi

# ---------------------------------------------------------------- Verdict
echo "================================================================" | tee -a "$LOG"
if [ "$FAIL_COUNT" -eq 0 ]; then
  echo "VERDICT: PASS — all $PASS_COUNT gates passed. READY." | tee -a "$LOG"
  echo "Log: $LOG"
  exit 0
else
  echo "VERDICT: FAIL — $PASS_COUNT passed, $FAIL_COUNT failed. NOT READY." | tee -a "$LOG"
  echo "Log: $LOG"
  exit 1
fi
