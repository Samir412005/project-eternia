#!/bin/bash
# PROJECT ETERNIA - Phase 1 validation. Run from the project root.
# Produces tests/reports/validation_report.md with real command output.
set -u
GODOT="${GODOT_BIN:-/home/hatch/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64}"
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
REPORT="$PROJECT_DIR/tests/reports/validation_report.md"
mkdir -p "$PROJECT_DIR/tests/reports"
{
echo "# Validation Report — PROJECT ETERNIA Phase 1"
echo ""
echo "Date (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Godot: $GODOT"
echo ""
echo "## 1. Godot version"
"$GODOT" --version 2>&1
echo ""
echo "## 2. Project import (headless)"
cd "$PROJECT_DIR"
timeout 120 "$GODOT" --headless --path . --import 2>&1 | tail -20
echo "import exit: ${PIPESTATUS[0]}"
echo ""
echo "## 3. Automated tests (tests/run_tests.gd)"
timeout 120 "$GODOT" --headless --path . -s tests/run_tests.gd 2>&1 | tail -60
echo ""
echo "## 4. Headless run of main scene (10 seconds)"
timeout 60 "$GODOT" --headless --path . res://scenes/main/main.tscn --quit-after 600 2>&1 | tail -20
echo ""
echo "## 5. APK artifact"
ls -la "$PROJECT_DIR/builds/android/" 2>&1
} | tee "$REPORT"
echo "Report: $REPORT"
