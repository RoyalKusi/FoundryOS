#!/usr/bin/env bash
set -euo pipefail
echo "=== FoundryOS Setup Android + Logo ==="
# 1. Generate logo
echo "Generating logo assets..."
pip install -q Pillow || pip3 install -q Pillow
python3 scripts/generate_logo.py || true
python3 scripts/build_icons.py || true

# 2. Ensure Flutter scaffold
if [ ! -d "app/android" ]; then
  echo "Creating Flutter android/ios scaffold..."
  cd app
  flutter create . --platforms=android,ios --org com.foundryos.app --project-name foundryos_app
  cd ..
  # regenerate icons after scaffold
  python3 scripts/build_icons.py || true
fi

# 3. Install deps
echo "flutter pub get..."
cd app && flutter pub get
if [ -f "assets/icon/app_icon.png" ]; then
  dart run flutter_launcher_icons || echo "launcher icons manual fallback OK"
fi

# 4. Build APK
echo "Building APK debug..."
flutter build apk --debug
echo "✅ APK at app/build/app/outputs/flutter-apk/app-debug.apk"
ls -lh build/app/outputs/flutter-apk/*.apk || ls -lh app/build/app/outputs/flutter-apk/*.apk
echo "Install on device: adb install -r app/build/app/outputs/flutter-apk/app-debug.apk"
