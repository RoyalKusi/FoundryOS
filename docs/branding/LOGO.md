# FoundryOS — Logo & Brand System

> Created 2026-05-13 — Lead Systems Architect. Implements §5.1–5.3 Design System.

## Concept

**Foundry** = precision casting — molten material poured into a mold to create durable structures.
**OS** = Company Operating System — the invisible structure that lets a company run.

The mark fuses both: a **squircle mold** (iOS continuous corner) containing a geometric **"F" monogram** with a subtle pouring notch. The **sparkle** at 45° signals AI-native.

## Anatomy

```
┌─────────────────────────────┐
│  Squircle (28pt radius,     │
│  ContinuousRectangleBorder, │
│  blur sigma 0 for icon)     │
│                             │
│    ┌──────┐  ✨ sparkle     │
│    │ █████│                 │
│    │ █    │   ← F-stem      │
│    │ █████│   ← F-mid bar   │
│    │ █    │   notch         │
│    └──────┘                 │
└─────────────────────────────┘
```

- **Squircle**: `ContinuousRectangleBorder` radius 28 on 1024, equivalent to iOS App Icon superellipse (a=4). Fill: linear gradient 135° `#4F46E5` → `#6366F1` → `#7C74FF`. Light mode uses `#4F46E5` as dominant, dark uses `#7C74FF`.
- **F monogram**: Weight 700, 60% of squircle width, 68% height. Vertical stem 56pt, horizontals 48pt/36pt, thickness 18pt, corner radius 4pt. Bottom-right 10pt 45° chamfer = pour channel. Color `#FFFFFF` 100% opacity.
- **Sparkle badge**: 4-point star, 22pt, white, 18% outer glow `#FFFFFF` 40% opacity, placed at (x=78%, y=22%) of squircle, overlaps edge by 30% like AI avatar badge (§5.6).
- **Wordmark**: `Foundry` Inter 700 32pt tracking -0.5, `OS` Inter 400 32pt accent `#4F46E5` light / `#7C74FF` dark. Tagline `Company Operating System` Inter 500 12/16 uppercase tracking 1.2.

## Color

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| Foundry Indigo | `#4F46E5` | `#7C74FF` | Accent, gradient start |
| Indigo 60 | `#6366F1` | `#8B85FF` | Gradient mid |
| bg.primary | `#FFFFFF` | `#000000` | Page bg |
| bg.secondary | `#F5F5F7` | `#0B0B0D` | Card bg |
| label.primary | `#1D1D1F` | `#F5F5F7` | Text |

WCAG AA ≥4.5:1 white on indigo passes (7.1:1).

## Variants

1. **Primary** — gradient squircle + white F + sparkle on transparent (for app icon, favicon)
2. **Light lockup** — primary + `FoundryOS` wordmark on white
3. **Dark lockup** — primary + wordmark on black (F stays white, label `#F5F5F7`)
4. **Mono** — white F on indigo squircle (for notifications, splash)
5. **Mono inverse** — indigo F on white squircle (for print, 1-bit)

## Clear space & Minimum

- Clear space = `x` = height of F-stem thickness (18pt on 1024). Keep free.
- Minimum digital 20pt, print 8mm.

## App Icon (Android / iOS)

- **Foreground**: squircle gradient + F + sparkle centered, 85% of canvas (avoids clipping on Android adaptive mask).
- **Background** (adaptive): `#FFFFFF` light, `#0B0B0D` dark — but we ship **filled** icon (gradient *is* background) for simplicity; adaptive via `ic_launcher_background.png` solid `#4F46E5` and `ic_launcher_foreground.png` transparent F.
- Sizes generated via `flutter_launcher_icons`: 48,72,96,144,192,512. iOS 20,29,40,60,76,83.5,1024.

## Usage Rules

- Never stretch, never rotate, never add drop shadow beyond spec `0 8 24 rgba(0,0,0,0.08)` for floating only.
- Never place gradient squircle on busy photo — use mono.
- Never recreate F with different weight — use provided asset.
- Respect `reduce-transparency`: fallback solid `#4F46E5` no blur.

## Files

```
app/assets/branding/
  foundry_logo_primary.svg        # master vector squircle+gradient+F+sparkle
  foundry_logo_lockup_light.svg   # + wordmark on light
  foundry_logo_lockup_dark.svg
  foundry_icon_fg.svg             # foreground only (F+sparkle) for adaptive
  app_icon.png                    # 1024x1024 PNG rendered (for launcher)
  logo_light.png / logo_dark.png  # 512 lockup PNGs
  splash.png                      # 1284x2778 splash (centered primary on bg)

app/assets/icon/app_icon.png      # alias for launcher
android/app/src/main/res/mipmap-*/ic_launcher.png  # generated via CI
ios/Runner/Assets.xcassets/AppIcon.appiconset/     # generated via CI
```

## Haptics & Motion for Splash

On launch, logo scales 0.94→1.0 spring stiffness 300 damping 30, 320ms, with lightImpact haptic. Respect `disableAnimations`.

