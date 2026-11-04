# FoundryOS — APK Build Guide

## Option A: One-command local (requires Flutter 3.24+)

```bash
pip install Pillow
python3 scripts/generate_logo.py
python3 scripts/build_icons.py
chmod +x scripts/setup_android.sh
./scripts/setup_android.sh
# → app/build/app/outputs/flutter-apk/app-debug.apk
adb install -r app/build/app/outputs/flutter-apk/app-debug.apk
```

If `android/` missing, `setup_android.sh` runs `flutter create . --platforms=android,ios`.

## Option B: CI Artifact (no local Flutter needed)

1. Push this commit to `main` (or trigger workflow manually: Actions → Build APK + Logo → Run workflow)
2. Wait ~6 min for `logo-and-apk` job
3. Download:
   - `foundryos-debug-apk` → `app-debug.apk` (installable)
   - `foundryos-logo-assets` → PNGs + icons
   - `foundryos-release-apk` → release unsigned (for Play Console)

Artifact URL: `https://github.com/<org>/FoundryOS/actions/runs/<run-id>`

## Option C: Docker (for consistent build)

```bash
docker run --rm -v $PWD:/workspace -w /workspace/app cirrusci/flutter:stable \
  bash -c "flutter pub get && flutter build apk --debug"
```

## Troubleshooting

- **Icon missing**: Run `python3 scripts/build_icons.py` — generates `assets/icon/app_icon.png` + `mipmap-*`.
- **Android scaffold missing**: `cd app && flutter create . --platforms=android,ios --org com.foundryos.app`
- **Gradle JDK**: Use Java 17 (`actions/setup-java@v4` with `java-version: 17` in CI).
- **Unsigned release**: `flutter build apk --release` produces unsigned; for signed add `android/key.properties` + `android/app/upload-keystore.jks` (see Flutter docs).

## Logo regeneration

Source SVGs are ground truth (`app/assets/branding/*.svg`). To update colors:

1. Edit `docs/branding/LOGO.md` + SVGs
2. Update tokens in `app/lib/theme/app_colors.dart` (`#4F46E5` light / `#7C74FF` dark)
3. Re-run `scripts/build_icons.py`

The app also has a **painted fallback** (`lib/widgets/app_logo.dart` → `_LogoPainter`) so UI shows logo even if PNG not yet generated.
