# Technical Implementation 01: Project Setup & Dynamic Terminal Theme

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Architecture/03-monorepo-structure.md`](../../Documentation/Architecture/03-monorepo-structure.md), [`Documentation/Design/01-design-system-and-theming.md`](../../Documentation/Design/01-design-system-and-theming.md), [`Documentation/Customization/01-customization-overview.md`](../../Documentation/Customization/01-customization-overview.md)

---

## Step 1: Bootstrap `apps/mobile` & Configure `pubspec.yaml`

### Objective
Create the Android-first Flutter project inside `apps/mobile/`, initialize the required asset directories (`assets/manifests/`, `assets/shaders/`, `assets/sprites/kaijus/`, `assets/sprites/scenarios/`), and configure `pubspec.yaml` with the locked PoC dependency stack (no `build_runner` required).

### Commands to Run
From the repository root:

```bash
flutter create --platforms=android --org com.unixtamagotchi --project-name tamagotchi_mobile apps/mobile
```

Create the asset and source subdirectories inside `apps/mobile/`:
- `apps/mobile/assets/manifests/`
- `apps/mobile/assets/shaders/`
- `apps/mobile/assets/sprites/kaijus/`
- `apps/mobile/assets/sprites/scenarios/`
- `apps/mobile/lib/core/theme/`
- `apps/mobile/lib/core/widgets/`
- `apps/mobile/lib/core/sprite_engine/`
- `apps/mobile/lib/core/dither_engine/`
- `apps/mobile/lib/core/naming/`
- `apps/mobile/lib/models/`
- `apps/mobile/lib/state/`
- `apps/mobile/lib/plugins/models/`
- `apps/mobile/lib/plugins/executors/`
- `apps/mobile/lib/features/room/view/`
- `apps/mobile/lib/features/room/widgets/`
- `apps/mobile/lib/features/store/view/`
- `apps/mobile/lib/features/switch/view/`
- `apps/mobile/lib/features/settings/view/`
- `apps/mobile/lib/features/evolution/view/`

### Target File: `apps/mobile/pubspec.yaml`
Replace `apps/mobile/pubspec.yaml` with:

```yaml
name: tamagotchi_mobile
description: "Unix Tamagotchi - Tactical 1-Bit Kaiju / Titan Companion (PoC)"
publish_to: "none"
version: 1.0.4+1

environment:
  sdk: ">=3.3.0 <4.0.0"
  flutter: ">=3.19.0"

dependencies:
  flutter:
    sdk: flutter

  # Reactive State Management
  flutter_riverpod: ^2.5.1

  # 2D Game Engine (Viewport & Sprite Animation)
  flame: ^1.18.0

  # Local Offline Binary Storage (PoC)
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Terminal Monospace Typography (VT323)
  google_fonts: ^6.2.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  flame_test: ^1.16.0

flutter:
  uses-material-design: true
  assets:
    - assets/manifests/poc_default_manifest.json
    - assets/sprites/kaijus/
    - assets/sprites/scenarios/
  shaders:
    - assets/shaders/bayer_dither.frag
```

### Target File: `apps/mobile/analysis_options.yaml`
Ensure `apps/mobile/analysis_options.yaml` contains clean lint rules:

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    prefer_final_fields: true
```

### Bootstrap Placeholders (Required Before Running `flutter pub get`)
Create a temporary minimal `apps/mobile/assets/manifests/poc_default_manifest.json` (this will be populated with the full manifest in File 05):

```json
{
  "timestamp": "2026-10-31T00:00:00.000Z",
  "plugins": [],
  "scenarios": [],
  "actions": [],
  "customizations": []
}
```

Create a temporary minimal `apps/mobile/assets/shaders/bayer_dither.frag` so Flutter's shader compiler succeeds during `flutter pub get` (this will be replaced with the full Bayer shader in File 03):

```glsl
#version 460 core
#include <flutter/runtime_effect.glsl>

uniform vec2 uResolution;
uniform vec4 uColorLight;
uniform vec4 uColorDark;
uniform float uLuminanceBias;
uniform sampler2D uTexture;

out vec4 fragColor;

void main() {
  vec2 uv = FlutterFragCoord().xy / uResolution;
  vec4 tex = texture(uTexture, uv);
  fragColor = mix(uColorDark, uColorLight, tex.r + uLuminanceBias);
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter pub get
```

> **NEXT STEP**: Once `flutter pub get` succeeds, proceed immediately to **[Step 2: Implement Dynamic `AppPalette` & Industrial Terminal `AppTheme`](#step-2-implement-dynamic-apppalette--industrial-terminal-apptheme)** in this file.

---

## Step 2: Implement Dynamic `AppPalette` & Industrial Terminal `AppTheme`

### Objective
Implement the semantic palette token extension (`AppPalette`) and `AppTheme` in `lib/core/theme/` so that:
1. No widget ever hardcodes color hex literals.
2. Selecting any `PALETTE` customization plugin dynamically updates both the Flutter widget tree (`Theme.of(context).extension<AppPalette>()!`) and the `bayer_dither.frag` shader uniforms (`uColorLight`, `uColorDark`).
3. Typography uses `VT323` via `google_fonts` across the entire app.

### Target File: `apps/mobile/lib/core/theme/app_palette.dart`
Create `apps/mobile/lib/core/theme/app_palette.dart`:

```dart
import 'package:flutter/material.dart';

/// Semantic color tokens for the Tactical 1-Bit Cyber-Specimen OS.
/// Driven dynamically by the active PALETTE customization plugin.
@immutable
class AppPalette extends ThemeExtension<AppPalette> {
  final String id;
  final String displayName;
  final Color background; // Maps to shader uColorLight (e.g. Khaki #C5BEAA)
  final Color surface;    // Slightly lighter/alt panel fill (e.g. #D4D99C)
  final Color foreground; // Maps to shader uColorDark / Ink (e.g. Charcoal #141512)
  final Color accent;     // Copper/Amber highlight for stat labels & active states
  final Color emergency;  // Crimson red (#B72828) for critical/alert banners
  final Color disabled;   // Muted ink for disabled controls

  const AppPalette({
    required this.id,
    required this.displayName,
    required this.background,
    required this.surface,
    required this.foreground,
    required this.accent,
    this.emergency = const Color(0xFFB72828),
    this.disabled = const Color(0xFF7A7669),
  });

  /// Default palette matching `Desing References/Godzila.webp` and prototype screens.
  static const AppPalette classicKhaki = AppPalette(
    id: 'palette_classic_khaki',
    displayName: 'CLASSIC_KHAKI',
    background: Color(0xFFC5BEAA),
    surface: Color(0xFFD0C9B6),
    foreground: Color(0xFF141512),
    accent: Color(0xFFB85E2B),
    emergency: Color(0xFFB72828),
    disabled: Color(0xFF7A7669),
  );

  static const AppPalette amberMonitor = AppPalette(
    id: 'palette_amber_monitor',
    displayName: 'AMBER_MONITOR',
    background: Color(0xFF1E160C),
    surface: Color(0xFF2B1F11),
    foreground: Color(0xFFFFB000),
    accent: Color(0xFFFFD066),
    emergency: Color(0xFFFF4444),
    disabled: Color(0xFF7A5810),
  );

  static const AppPalette gameBoyGreen = AppPalette(
    id: 'palette_game_boy_green',
    displayName: 'GAME_BOY_GREEN',
    background: Color(0xFF9BBC0F),
    surface: Color(0xFF8BAC0F),
    foreground: Color(0xFF0F380F),
    accent: Color(0xFF306230),
    emergency: Color(0xFF9B0F0F),
    disabled: Color(0xFF557214),
  );

  static const AppPalette blueTerminal = AppPalette(
    id: 'palette_blue_terminal',
    displayName: 'BLUE_TERMINAL',
    background: Color(0xFFB8C8D8),
    surface: Color(0xFFC8D8E8),
    foreground: Color(0xFF0E1A24),
    accent: Color(0xFF2B6CB0),
    emergency: Color(0xFFB72828),
    disabled: Color(0xFF6B7F94),
  );

  static const List<AppPalette> builtInPresets = [
    classicKhaki,
    amberMonitor,
    gameBoyGreen,
    blueTerminal,
  ];

  /// Parses hex strings like `#C5BEAA` or `0xFFC5BEAA` into a Flutter [Color].
  static Color parseHex(String? hex, Color fallback) {
    if (hex == null || hex.isEmpty) return fallback;
    final cleaned = hex.replaceAll('#', '').replaceAll('0x', '').replaceAll('0X', '');
    final buffer = StringBuffer();
    if (cleaned.length == 6) buffer.write('FF');
    buffer.write(cleaned);
    final parsed = int.tryParse(buffer.toString(), radix: 16);
    return parsed != null ? Color(parsed) : fallback;
  }

  /// Constructs an [AppPalette] dynamically from a `PALETTE` CustomizationPluginConfig's `renderData`.
  factory AppPalette.fromPluginRenderData({
    required String id,
    required String displayName,
    required Map<String, dynamic> renderData,
  }) {
    final bg = parseHex(renderData['uColorLight'] as String?, classicKhaki.background);
    final fg = parseHex(renderData['uColorDark'] as String?, classicKhaki.foreground);
    final surf = parseHex(renderData['surface'] as String?, bg);
    final acc = parseHex(renderData['accent'] as String?, classicKhaki.accent);
    final emg = parseHex(renderData['emergency'] as String?, classicKhaki.emergency);

    return AppPalette(
      id: id,
      displayName: displayName,
      background: bg,
      surface: surf,
      foreground: fg,
      accent: acc,
      emergency: emg,
    );
  }

  static AppPalette of(BuildContext context) {
    return Theme.of(context).extension<AppPalette>() ?? AppPalette.classicKhaki;
  }

  @override
  AppPalette copyWith({
    String? id,
    String? displayName,
    Color? background,
    Color? surface,
    Color? foreground,
    Color? accent,
    Color? emergency,
    Color? disabled,
  }) {
    return AppPalette(
      id: id ?? this.id,
      displayName: displayName ?? this.displayName,
      background: background ?? this.background,
      surface: surface ?? this.surface,
      foreground: foreground ?? this.foreground,
      accent: accent ?? this.accent,
      emergency: emergency ?? this.emergency,
      disabled: disabled ?? this.disabled,
    );
  }

  @override
  AppPalette lerp(ThemeExtension<AppPalette>? other, double t) {
    if (other is! AppPalette) return this;
    return AppPalette(
      id: t < 0.5 ? id : other.id,
      displayName: t < 0.5 ? displayName : other.displayName,
      background: Color.lerp(background, other.background, t)!,
      surface: Color.lerp(surface, other.surface, t)!,
      foreground: Color.lerp(foreground, other.foreground, t)!,
      accent: Color.lerp(accent, other.accent, t)!,
      emergency: Color.lerp(emergency, other.emergency, t)!,
      disabled: Color.lerp(disabled, other.disabled, t)!,
    );
  }
}
```

### Target File: `apps/mobile/lib/core/theme/app_theme.dart`
Create `apps/mobile/lib/core/theme/app_theme.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_palette.dart';

class AppTheme {
  /// Builds the Industrial Diagnostic Terminal [ThemeData] from the active [AppPalette].
  static ThemeData buildTerminalTheme(
    AppPalette palette, {
    bool useGoogleFontsNetwork = true,
  }) {
    TextStyle terminalStyle({
      required double fontSize,
      required Color color,
      FontWeight fontWeight = FontWeight.normal,
      double height = 1.1,
      double letterSpacing = 0.5,
    }) {
      final base = TextStyle(
        fontFamily: 'VT323',
        fontSize: fontSize,
        color: color,
        fontWeight: fontWeight,
        height: height,
        letterSpacing: letterSpacing,
      );
      if (!useGoogleFontsNetwork) return base;
      try {
        return GoogleFonts.vt323(textStyle: base);
      } catch (_) {
        return base;
      }
    }

    final textTheme = TextTheme(
      displayLarge: terminalStyle(
        fontSize: 28,
        color: palette.foreground,
        fontWeight: FontWeight.bold,
      ),
      titleLarge: terminalStyle(
        fontSize: 22,
        color: palette.accent,
        fontWeight: FontWeight.bold,
      ),
      titleMedium: terminalStyle(
        fontSize: 19,
        color: palette.foreground,
        fontWeight: FontWeight.bold,
      ),
      bodyLarge: terminalStyle(
        fontSize: 20,
        color: palette.foreground,
      ),
      bodyMedium: terminalStyle(
        fontSize: 17,
        color: palette.foreground,
      ),
      bodySmall: terminalStyle(
        fontSize: 14,
        color: palette.foreground,
      ),
      labelLarge: terminalStyle(
        fontSize: 18,
        color: palette.foreground,
        fontWeight: FontWeight.bold,
      ),
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: palette.background,
      primaryColor: palette.foreground,
      fontFamily: 'VT323',
      textTheme: textTheme,
      colorScheme: ColorScheme.light(
        primary: palette.foreground,
        onPrimary: palette.background,
        secondary: palette.accent,
        onSecondary: palette.background,
        error: palette.emergency,
        onError: palette.background,
        surface: palette.surface,
        onSurface: palette.foreground,
      ),
      extensions: <ThemeExtension<dynamic>>[
        palette,
      ],
    );
  }
}
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/core/theme
```

> **NEXT STEP**: File `01-project-setup-and-theme.md` is complete. Proceed immediately to **[`02-terminal-widget-library.md` — Step 1: Core Terminal Chrome & Decorations](02-terminal-widget-library.md#step-1-core-terminal-chrome--decorations)**.
