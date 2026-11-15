# Validation
Run from the project root:
```bash
bash tools/validation/validate.sh
```
It imports the project headless, runs `tests/run_tests.gd`, runs the
main scene headless for 600 frames, and lists the APK.
Report: `tests/reports/validation_report.md`.
