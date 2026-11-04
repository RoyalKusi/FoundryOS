# Icon Assets

Primary icon is generated via `scripts/generate_logo.py` + `scripts/build_icons.py`.

- Source SVGs: `app/assets/branding/foundry_logo_primary.svg` (1024 master)
- Generated PNG: `app/assets/branding/app_icon.png` (1024) → copied to `app/assets/icon/app_icon.png` for `flutter_launcher_icons`
- Android adaptive: `mipmap-*/ic_launcher_background.png` + `ic_launcher_foreground.png`
- iOS: `ios/Runner/Assets.xcassets/AppIcon.appiconset/`

To regenerate locally:

```bash
pip install Pillow
python3 scripts/generate_logo.py
python3 scripts/build_icons.py
```

Or run full setup:

```bash
chmod +x scripts/setup_android.sh
./scripts/setup_android.sh
```

CI will auto-generate on every push if files missing.

Preview SVGs directly in VS Code or Figma — they are the source of truth.
