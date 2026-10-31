# Technical Implementation 03: Bayer Dither Shader & Flame Viewport

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Design/03-kaiju-dithered-sprite-engine.md`](../../Documentation/Design/03-kaiju-dithered-sprite-engine.md), [`Documentation/Design/06-1bit-dithering-rendering-pipeline.md`](../../Documentation/Design/06-1bit-dithering-rendering-pipeline.md)

---

## Step 1: Bayer Dither Fragment Shader (Impeller-Safe)

### Objective
Write the production GLSL fragment shader `apps/mobile/assets/shaders/bayer_dither.frag` matching `Documentation/Design/06-1bit-dithering-rendering-pipeline.md`:
1. Uses screen-space coordinates mapped to a 256×256 virtual grid for the 4×4 Bayer matrix modulo (`bayer4x4`), ensuring moving sprites swim through a fixed LCD dither grid.
2. Uses conditional index resolution in `bayer4x4(ivec2 p)` so Impeller's AOT compiler on Android (Vulkan/OpenGL ES) and Skia both compile without dynamic array-indexing errors.
3. Exposes runtime uniforms `uResolution`, `uColorLight`, `uColorDark`, `uLuminanceBias`, and `uTexture` (`sampler2D`).

### Target File: `apps/mobile/assets/shaders/bayer_dither.frag`
Overwrite `apps/mobile/assets/shaders/bayer_dither.frag` with:

```glsl
#version 460 core
#include <flutter/runtime_effect.glsl>

uniform vec2 uResolution;      // floats 0, 1
uniform vec4 uColorLight;      // floats 2, 3, 4, 5 (Active palette background)
uniform vec4 uColorDark;       // floats 6, 7, 8, 9 (Active palette foreground/ink)
uniform float uLuminanceBias;  // float 10 (OS_LUMINANCE offset: -0.35 to +0.35)
uniform sampler2D uTexture;    // sampler 0 (Off-screen Flame scene texture)

out vec4 fragColor;

float bayer4x4(ivec2 p) {
    int x = p.x & 3;
    int y = p.y & 3;
    int index = y * 4 + x;
    if (index == 0)  return 0.0 / 16.0;
    if (index == 1)  return 8.0 / 16.0;
    if (index == 2)  return 2.0 / 16.0;
    if (index == 3)  return 10.0 / 16.0;
    if (index == 4)  return 12.0 / 16.0;
    if (index == 5)  return 4.0 / 16.0;
    if (index == 6)  return 14.0 / 16.0;
    if (index == 7)  return 6.0 / 16.0;
    if (index == 8)  return 3.0 / 16.0;
    if (index == 9)  return 11.0 / 16.0;
    if (index == 10) return 1.0 / 16.0;
    if (index == 11) return 9.0 / 16.0;
    if (index == 12) return 15.0 / 16.0;
    if (index == 13) return 7.0 / 16.0;
    if (index == 14) return 13.0 / 16.0;
    return 5.0 / 16.0;
}

void main() {
    vec2 fragCoord = FlutterFragCoord().xy;
    vec2 safeRes = max(uResolution, vec2(1.0, 1.0));
    vec2 uv = fragCoord / safeRes;
    vec4 texColor = texture(uTexture, uv);

    // Transparent pixels map cleanly to uColorLight
    if (texColor.a < 0.1) {
        fragColor = uColorLight;
        return;
    }

    // Perceived luminance + diagnostic OS_LUMINANCE bias
    float luminance = clamp(
        dot(texColor.rgb, vec3(0.299, 0.587, 0.114)) + uLuminanceBias,
        0.0,
        1.0
    );

    // Screen-space virtual 256x256 pixel coordinates for chunky 1-bit dithering
    ivec2 virtualPixel = ivec2(floor(uv * 256.0));
    float threshold = bayer4x4(virtualPixel);

    if (luminance > threshold) {
        fragColor = uColorLight;
    } else {
        fragColor = uColorDark;
    }
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter analyze
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 2: Kaiju Sprite Engine & Procedural Pixel-Art Fallback](#step-2-kaiju-sprite-engine--procedural-pixel-art-fallback)** in this file.

---

## Step 2: Kaiju Sprite Engine & Procedural Pixel-Art Fallback

### Objective
Implement `KaijuDefinition` (`lib/core/sprite_engine/kaiju_definition.dart`) and the procedural pixel-art Flame Canvas renderer (`lib/core/sprite_engine/procedural_pixel_renderer.dart`) per `Documentation/Design/03-kaiju-dithered-sprite-engine.md`:
1. Defines the two PoC store catalog Kaijus: `godzilla` (120 CR) and `cyber_godzilla` (120 CR).
2. Attempts to load PNG sprite sheets (`assets/sprites/kaijus/<type>_spritesheet.png`) first.
3. If PNG sprite sheets or scenario layer PNGs are not present on disk, `ProceduralPixelRenderer` renders multi-frame grayscale pixel-art directly onto the 256×256 Flame `Canvas` (including the containment room furniture props, city skyline window, Godzilla's dorsal plates, tail sway, eating a ball of humans, sleeping with smoke puffs, and atomic breath / cyber-laser cone with continuous luminance gradients that the Bayer shader turns into crisp 1-bit dithered patterns matching `Desing References/Godzila.webp` and `Desing References/Mecha+Godzila.png`).

### Target File: `apps/mobile/lib/core/sprite_engine/kaiju_definition.dart`
Create `apps/mobile/lib/core/sprite_engine/kaiju_definition.dart`:

```dart
import 'package:flame/components.dart';
import 'package:flame/sprite.dart';
import 'package:flutter/foundation.dart';

@immutable
class KaijuDefinition {
  final String itemId;
  final String kaijuType;
  final String displayName;
  final int priceCredits;
  final String traitsDescription;
  final String spriteSheetAsset;
  final int frameWidth;
  final int frameHeight;
  final Map<String, SpriteAnimationData> actions;

  const KaijuDefinition({
    required this.itemId,
    required this.kaijuType,
    required this.displayName,
    required this.priceCredits,
    required this.traitsDescription,
    required this.spriteSheetAsset,
    required this.frameWidth,
    required this.frameHeight,
    required this.actions,
  });

  SpriteAnimationData getAnimationData(String action) {
    return actions[action] ?? actions['idle']!;
  }
}

final KaijuDefinition godzillaDefinition = KaijuDefinition(
  itemId: 'item_godzilla',
  kaijuType: 'godzilla',
  displayName: 'GODZILLA',
  priceCredits: 120,
  traitsDescription:
      'APEX SAURIAN TITAN. DORSAL PLATES, ATOMIC BREATH DISCHARGE, BALANCED METABOLIC STATS.',
  spriteSheetAsset: 'kaijus/godzilla_spritesheet.png',
  frameWidth: 128,
  frameHeight: 128,
  actions: {
    'idle': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.25,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 0),
    ),
    'eating': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.20,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 128),
    ),
    'sleeping': SpriteAnimationData.sequenced(
      amount: 2,
      stepTime: 0.60,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 256),
    ),
    'playing': SpriteAnimationData.sequenced(
      amount: 6,
      stepTime: 0.12,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 384),
    ),
  },
);

final KaijuDefinition cyberGodzillaDefinition = KaijuDefinition(
  itemId: 'item_cyber_godzilla',
  kaijuType: 'cyber_godzilla',
  displayName: 'CYBER_GODZILLA',
  priceCredits: 120,
  traitsDescription:
      'CYBERNETIC APEX TITAN CONSTRUCT. REINFORCED STEEL HULL, LASER DISCHARGE, HIGH OUTPUT.',
  spriteSheetAsset: 'kaijus/cyber_godzilla_spritesheet.png',
  frameWidth: 128,
  frameHeight: 128,
  actions: {
    'idle': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.25,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 0),
    ),
    'eating': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.20,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 128),
    ),
    'sleeping': SpriteAnimationData.sequenced(
      amount: 2,
      stepTime: 0.60,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 256),
    ),
    'playing': SpriteAnimationData.sequenced(
      amount: 6,
      stepTime: 0.12,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 384),
    ),
  },
);

final List<KaijuDefinition> kaijuCatalog = [
  godzillaDefinition,
  cyberGodzillaDefinition,
];

KaijuDefinition getKaijuDefinition(String kaijuType) {
  return kaijuCatalog.firstWhere(
    (d) => d.kaijuType == kaijuType,
    orElse: () => godzillaDefinition,
  );
}
```

### Target File: `apps/mobile/lib/core/sprite_engine/procedural_pixel_renderer.dart`
Create `apps/mobile/lib/core/sprite_engine/procedural_pixel_renderer.dart`:

```dart
import 'dart:math' as math;
import 'package:flame/components.dart';
import 'package:flutter/material.dart';

/// Procedural pixel-art fallback component for scenario layers when PNG assets
/// are not yet bundled in `assets/sprites/scenarios/`.
/// Draws in grayscale luminance values (0.0..1.0) so `bayer_dither.frag` converts
/// shaded regions into authentic 1-bit ordered Bayer dither patterns.
class ProceduralScenarioLayerComponent extends PositionComponent {
  final String layerKey;

  ProceduralScenarioLayerComponent({
    required this.layerKey,
    required Vector2 position,
    required Vector2 size,
    required int priority,
  }) : super(position: position, size: size, priority: priority);

  @override
  void render(Canvas canvas) {
    const double px = 4.0; // Chunky 4x4 virtual pixel blocks on 256x256 canvas
    final lightBg = Paint()
      ..color = const Color(0xFFE8E4D5)
      ..isAntiAlias = false;
    final midShade = Paint()
      ..color = const Color(0xFF888888)
      ..isAntiAlias = false;
    final darkInk = Paint()
      ..color = const Color(0xFF141512)
      ..isAntiAlias = false;

    if (layerKey.contains('wall') || layerKey.contains('bg') || layerKey.contains('room')) {
      // Fill light background
      canvas.drawRect(Offset.zero & size.toSize(), lightBg);

      // Draw containment floor horizon & shaded floor grid (luminance 0.55 -> dithered!)
      canvas.drawRect(const Rect.fromLTWH(0, 196, 256, 60), midShade);
      canvas.drawRect(const Rect.fromLTWH(0, 192, 256, px), darkInk);

      // Draw skyline silhouette & containment props (matching Godzila.webp & habitat lore)
      // Left: Oversized containment bed & industrial pipe
      canvas.drawRect(const Rect.fromLTWH(12, 168, 52, 24), darkInk);
      canvas.drawRect(const Rect.fromLTWH(16, 172, 44, 12), midShade);

      // Right: Oversized study desk & skyline buildings
      final buildingHeights = [44.0, 68.0, 36.0, 84.0, 56.0, 64.0];
      for (int i = 0; i < buildingHeights.length; i++) {
        final bx = 160.0 + i * 15.0;
        final bh = buildingHeights[i];
        final by = 192.0 - bh;
        canvas.drawRect(Rect.fromLTWH(bx, by, 12.0, bh), darkInk);
        // Building lit windows
        for (double wy = by + 6; wy < 186; wy += 8) {
          canvas.drawRect(Rect.fromLTWH(bx + 3, wy, 3, 4), lightBg);
          canvas.drawRect(Rect.fromLTWH(bx + 7, wy, 3, 4), lightBg);
        }
      }
    }
  }
}

/// Procedural multi-frame pixel-art Kaiju component used automatically when
/// `assets/sprites/kaijus/<type>_spritesheet.png` is not present on disk.
/// Produces shaded luminance gradients for dorsal plates, armour, and atomic breath
/// so `bayer_dither.frag` renders the exact 1-bit dithered look of `Godzila.webp`.
class ProceduralKaijuComponent extends PositionComponent {
  final String kaijuType;
  String actionState;
  double _elapsed = 0.0;

  ProceduralKaijuComponent({
    required this.kaijuType,
    this.actionState = 'idle',
    Vector2? position,
  }) : super(
          position: position ?? Vector2(128, 148),
          size: Vector2(128, 128),
          anchor: Anchor.center,
          priority: 50,
        );

  @override
  void update(double dt) {
    super.update(dt);
    _elapsed += dt;
  }

  @override
  void render(Canvas canvas) {
    final frame = (_elapsed * 6.0).floor();
    final breathBob = (frame % 2 == 0) ? 0.0 : 4.0;
    final isCyber = kaijuType == 'cyber_godzilla';

    final darkInk = Paint()
      ..color = const Color(0xFF101010)
      ..isAntiAlias = false;
    final midGray = Paint()
      ..color = const Color(0xFF6E6E6E)
      ..isAntiAlias = false;
    final lightGray = Paint()
      ..color = const Color(0xFFB5B5B5)
      ..isAntiAlias = false;
    final highlight = Paint()
      ..color = const Color(0xFFF2F2F2)
      ..isAntiAlias = false;

    void drawBlock(double gx, double gy, double gw, double gh, Paint paint) {
      canvas.drawRect(Rect.fromLTWH(gx * 4.0, gy * 4.0 + breathBob, gw * 4.0, gh * 4.0), paint);
    }

    if (actionState == 'sleeping') {
      // Dormant coiled posture on the habitat floor
      drawBlock(6, 20, 18, 7, darkInk);
      drawBlock(8, 21, 14, 4, isCyber ? midGray : darkInk);
      // Closed eye slit
      drawBlock(7, 22, 3, 1, highlight);
      // Dorsal fins resting
      drawBlock(12, 18, 3, 2, midGray);
      drawBlock(16, 18, 3, 2, midGray);
      drawBlock(20, 19, 3, 2, midGray);
      // Floating dithered sleep smoke / Zzz puffs
      final puffOffset = (frame % 4).toDouble();
      drawBlock(5 - puffOffset, 15 - puffOffset, 2, 2, midGray);
      drawBlock(3 - puffOffset, 12 - puffOffset, 3, 2, lightGray);
      return;
    }

    // Upright saurian/cyber titan silhouette (32x32 virtual blocks @ 4px each = 128x128)
    // Tail sweeping right
    final tailSwing = (frame % 4 < 2) ? 0.0 : 1.0;
    drawBlock(20, 22 - tailSwing, 6, 4, darkInk);
    drawBlock(25, 20 - tailSwing, 4, 3, darkInk);

    // Massive legs & claws
    drawBlock(11, 22, 5, 6, darkInk);
    drawBlock(16, 22, 5, 6, darkInk);
    drawBlock(9, 27, 4, 2, darkInk);
    drawBlock(14, 27, 4, 2, darkInk);

    // Torso & chest armor
    drawBlock(11, 11, 9, 12, darkInk);
    if (isCyber) {
      // Mecha chest triple-reactor ports (matching Mecha+Godzila.png)
      drawBlock(12, 13, 6, 8, lightGray);
      drawBlock(13, 15, 1, 2, darkInk);
      drawBlock(15, 15, 1, 2, darkInk);
      drawBlock(17, 15, 1, 2, darkInk);
    } else {
      // Shaded saurian belly scales (dithered by Bayer matrix)
      drawBlock(11, 14, 3, 7, midGray);
    }

    // Jagged Dorsal Plates along the back (glowing when playing/rampaging)
    final finPaint = (actionState == 'playing' && frame % 2 == 0) ? lightGray : midGray;
    drawBlock(19, 8, 4, 3, darkInk);
    drawBlock(20, 9, 2, 1, finPaint);
    drawBlock(20, 12, 5, 3, darkInk);
    drawBlock(21, 13, 3, 1, finPaint);
    drawBlock(20, 16, 4, 3, darkInk);
    drawBlock(21, 17, 2, 1, finPaint);

    // Head, snout & jaw (facing left like Godzila.webp)
    drawBlock(8, 6, 9, 6, darkInk);
    if (isCyber) {
      drawBlock(9, 5, 4, 2, lightGray); // Mecha crest
      drawBlock(9, 7, 7, 4, midGray);
    }
    // Eye
    drawBlock(10, 7, 2, 2, highlight);

    // Arms & claws
    drawBlock(8, 13, 4, 3, darkInk);
    drawBlock(7, 15, 2, 2, darkInk);

    // Action-specific foreground animations
    if (actionState == 'eating') {
      // Open jaw devouring a compressed ball of human people (with stipple particles)
      drawBlock(7, 10, 5, 2, darkInk);
      final chomp = (frame % 2 == 0) ? 0.0 : 1.0;
      drawBlock(3 + chomp, 10, 4, 4, midGray);
      drawBlock(4 + chomp, 11, 2, 2, darkInk);
      // Stipple crumbs
      drawBlock(2, 14 + chomp, 1, 1, darkInk);
      drawBlock(5, 15, 1, 1, midGray);
    } else if (actionState == 'playing') {
      // Iconic dithered cone of Atomic Breath / Cyber Laser (matching Godzila.webp!)
      drawBlock(7, 10, 5, 2, darkInk);
      for (int bx = 0; bx < 9; bx++) {
        final spread = (9 - bx) * 0.85;
        final centerY = 12.0 + (9 - bx) * 0.7;
        // Multi-step grayscale gradient so Bayer 4x4 shader produces the exact stipple cone
        final lum = (0.20 + (bx / 9.0) * 0.55).clamp(0.15, 0.85);
        final gray = (lum * 255).round();
        final beamPaint = Paint()
          ..color = Color.fromARGB(255, gray, gray, gray)
          ..isAntiAlias = false;
        final jitter = math.sin(_elapsed * 18.0 + bx) * 0.6;
        drawBlock(
          bx.toDouble(),
          centerY - spread / 2 + jitter,
          1.2,
          spread,
          beamPaint,
        );
      }
    }
  }
}
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/core/sprite_engine
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 3: Off-Screen Render-to-Texture `KaijuGame` & `DitheredViewport`](#step-3-off-screen-render-to-texture-kaijugame--ditheredviewport)** in this file.

---

## Step 3: Off-Screen Render-to-Texture `KaijuGame` & `DitheredViewport`

### Objective
Implement `KaijuGame` (`lib/core/dither_engine/kaiju_game.dart`) and `DitheredViewport` (`lib/core/dither_engine/dithered_viewport.dart`):
1. `KaijuGame` runs at a fixed `256×256` virtual camera resolution, attempts to load the PNG spritesheet (`images.load`), and automatically falls back to `ProceduralKaijuComponent` + `ProceduralScenarioLayerComponent` if the PNG asset is not found on disk.
2. `DitheredViewport` loads `assets/shaders/bayer_dither.frag` via `FragmentProgram.fromAsset` and uses a custom `RenderProxyBox` (`DitherShaderRenderObject`) to capture the child `RepaintBoundary` layer (`offsetLayer.toImageSync`), bind `shader.setImageSampler(0, image)`, bind `uResolution`, `uColorLight`, `uColorDark`, and `uLuminanceBias`, and draw with `FilterQuality.none`.

### Target File: `apps/mobile/lib/core/dither_engine/kaiju_game.dart`
Create `apps/mobile/lib/core/dither_engine/kaiju_game.dart`:

```dart
import 'package:flame/camera.dart';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import '../sprite_engine/kaiju_definition.dart';
import '../sprite_engine/procedural_pixel_renderer.dart';

class KaijuGame extends FlameGame {
  KaijuDefinition _kaijuDef;
  String _currentAction;
  Color _backgroundColor;

  PositionComponent? _kaijuComponent;
  SpriteAnimationComponent? _spriteKaijuComponent;
  ProceduralKaijuComponent? _proceduralKaijuComponent;

  KaijuGame({
    required KaijuDefinition kaijuDef,
    String currentAction = 'idle',
    Color backgroundColor = const Color(0xFFC5BEAA),
  })  : _kaijuDef = kaijuDef,
        _currentAction = currentAction,
        _backgroundColor = backgroundColor,
        super(
          camera: CameraComponent.withFixedResolution(width: 256, height: 256),
        );

  @override
  Color backgroundColor() => _backgroundColor;

  @override
  Future<void> onLoad() async {
    camera.viewfinder.anchor = Anchor.topLeft;

    // 1. Add default containment room layer (procedural fallback if PNG missing)
    world.add(
      ProceduralScenarioLayerComponent(
        layerKey: 'default_room_wall',
        position: Vector2.zero(),
        size: Vector2(256, 256),
        priority: 0,
      ),
    );

    // 2. Load Kaiju sprite sheet or procedural pixel-art fallback
    await _buildKaijuComponent();
  }

  Future<void> _buildKaijuComponent() async {
    if (_kaijuComponent != null) {
      _kaijuComponent!.removeFromParent();
    }

    try {
      final spriteSheet = await images.load(_kaijuDef.spriteSheetAsset);
      final animData = _kaijuDef.getAnimationData(_currentAction);
      final animation = SpriteAnimation.fromFrameData(spriteSheet, animData);

      final spriteComp = SpriteAnimationComponent(
        animation: animation,
        size: Vector2(
          _kaijuDef.frameWidth.toDouble(),
          _kaijuDef.frameHeight.toDouble(),
        ),
        position: Vector2(128, 148),
        anchor: Anchor.center,
        priority: 50,
        paint: Paint()..filterQuality = FilterQuality.none,
      );
      _spriteKaijuComponent = spriteComp;
      _proceduralKaijuComponent = null;
      _kaijuComponent = spriteComp;
      world.add(spriteComp);
    } catch (_) {
      // Automatic fallback to procedural pixel-art Flame Canvas rendering
      final procComp = ProceduralKaijuComponent(
        kaijuType: _kaijuDef.kaijuType,
        actionState: _currentAction,
        position: Vector2(128, 148),
      );
      _proceduralKaijuComponent = procComp;
      _spriteKaijuComponent = null;
      _kaijuComponent = procComp;
      world.add(procComp);
    }
  }

  void updateState({
    required KaijuDefinition kaijuDef,
    required String action,
    required Color backgroundColor,
  }) {
    _backgroundColor = backgroundColor;

    final typeChanged = kaijuDef.kaijuType != _kaijuDef.kaijuType;
    final actionChanged = action != _currentAction;
    _kaijuDef = kaijuDef;
    _currentAction = action;

    if (typeChanged) {
      _buildKaijuComponent();
      return;
    }

    if (actionChanged) {
      if (_proceduralKaijuComponent != null) {
        _proceduralKaijuComponent!.actionState = _currentAction;
      } else if (_spriteKaijuComponent != null) {
        images.load(_kaijuDef.spriteSheetAsset).then((sheet) {
          final animData = _kaijuDef.getAnimationData(_currentAction);
          _spriteKaijuComponent?.animation =
              SpriteAnimation.fromFrameData(sheet, animData);
        });
      }
    }
  }
}
```

### Target File: `apps/mobile/lib/core/dither_engine/dithered_viewport.dart`
Create `apps/mobile/lib/core/dither_engine/dithered_viewport.dart`:

```dart
import 'dart:ui' as ui;
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import '../sprite_engine/kaiju_definition.dart';
import '../theme/app_palette.dart';
import 'kaiju_game.dart';

/// Composites the low-res Flame [KaijuGame] through `assets/shaders/bayer_dither.frag`
/// using off-screen render-to-texture (`setImageSampler(0, image)`) and nearest-neighbor
/// upscaling (`FilterQuality.none`).
class DitheredViewport extends StatefulWidget {
  final KaijuDefinition kaijuDef;
  final String action;
  final double luminanceBias;

  const DitheredViewport({
    super.key,
    required this.kaijuDef,
    required this.action,
    this.luminanceBias = 0.0,
  });

  @override
  State<DitheredViewport> createState() => _DitheredViewportState();
}

class _DitheredViewportState extends State<DitheredViewport> {
  late final KaijuGame _game;
  ui.FragmentProgram? _program;

  @override
  void initState() {
    super.initState();
    _game = KaijuGame(
      kaijuDef: widget.kaijuDef,
      currentAction: widget.action,
    );
    _loadShader();
  }

  Future<void> _loadShader() async {
    try {
      final program =
          await ui.FragmentProgram.fromAsset('assets/shaders/bayer_dither.frag');
      if (mounted) {
        setState(() {
          _program = program;
        });
      }
    } catch (_) {
      // Graceful fallback in headless test environments where shader compilation isn't active
    }
  }

  @override
  void didUpdateWidget(covariant DitheredViewport oldWidget) {
    super.didUpdateWidget(oldWidget);
    final palette = AppPalette.of(context);
    _game.updateState(
      kaijuDef: widget.kaijuDef,
      action: widget.action,
      backgroundColor: palette.background,
    );
  }

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    _game.updateState(
      kaijuDef: widget.kaijuDef,
      action: widget.action,
      backgroundColor: palette.background,
    );

    final gameWidget = RepaintBoundary(
      child: GameWidget(game: _game),
    );

    if (_program == null) {
      return Container(
        color: palette.background,
        child: gameWidget,
      );
    }

    return _BayerDitherShaderFilter(
      program: _program!,
      lightColor: palette.background,
      darkColor: palette.foreground,
      luminanceBias: widget.luminanceBias,
      child: gameWidget,
    );
  }
}

class _BayerDitherShaderFilter extends SingleChildRenderObjectWidget {
  final ui.FragmentProgram program;
  final Color lightColor;
  final Color darkColor;
  final double luminanceBias;

  const _BayerDitherShaderFilter({
    required this.program,
    required this.lightColor,
    required this.darkColor,
    required this.luminanceBias,
    required super.child,
  });

  @override
  RenderObject createRenderObject(BuildContext context) {
    return DitherShaderRenderObject(
      program: program,
      lightColor: lightColor,
      darkColor: darkColor,
      luminanceBias: luminanceBias,
    );
  }

  @override
  void updateRenderObject(
    BuildContext context,
    covariant DitherShaderRenderObject renderObject,
  ) {
    renderObject
      ..program = program
      ..lightColor = lightColor
      ..darkColor = darkColor
      ..luminanceBias = luminanceBias;
  }
}

class DitherShaderRenderObject extends RenderProxyBox {
  ui.FragmentProgram _program;
  Color _lightColor;
  Color _darkColor;
  double _luminanceBias;

  DitherShaderRenderObject({
    required ui.FragmentProgram program,
    required Color lightColor,
    required Color darkColor,
    required double luminanceBias,
  })  : _program = program,
        _lightColor = lightColor,
        _darkColor = darkColor,
        _luminanceBias = luminanceBias;

  set program(ui.FragmentProgram value) {
    if (_program == value) return;
    _program = value;
    markNeedsPaint();
  }

  set lightColor(Color value) {
    if (_lightColor == value) return;
    _lightColor = value;
    markNeedsPaint();
  }

  set darkColor(Color value) {
    if (_darkColor == value) return;
    _darkColor = value;
    markNeedsPaint();
  }

  set luminanceBias(double value) {
    if (_luminanceBias == value) return;
    _luminanceBias = value;
    markNeedsPaint();
  }

  @override
  bool get isRepaintBoundary => true;

  @override
  void paint(PaintingContext context, Offset offset) {
    final child = this.child;
    if (child == null || size.isEmpty) return;

    try {
      // Paint child into an off-screen OffsetLayer and capture as ui.Image
      final recorder = ui.PictureRecorder();
      final offscreenCanvas = Canvas(recorder);
      final childContext = PaintingContext(OffsetLayer(), Offset.zero & size);
      super.paint(childContext, Offset.zero);
      final offsetLayer = child?.layer as OffsetLayer?;

      ui.Image image;
      if (offsetLayer != null) {
        image = offsetLayer.toImageSync(Offset.zero & size);
      } else {
        context.paintChild(child, offset);
        offscreenCanvas.drawRect(
          Offset.zero & size,
          Paint()..color = _lightColor,
        );
        final pic = recorder.endRecording();
        image = pic.toImageSync(
          size.width.ceil().clamp(1, 2048),
          size.height.ceil().clamp(1, 2048),
        );
        pic.dispose();
      }

      final shader = _program.fragmentShader()
        ..setFloat(0, size.width)
        ..setFloat(1, size.height)
        ..setFloat(2, _lightColor.red / 255.0)
        ..setFloat(3, _lightColor.green / 255.0)
        ..setFloat(4, _lightColor.blue / 255.0)
        ..setFloat(5, 1.0)
        ..setFloat(6, _darkColor.red / 255.0)
        ..setFloat(7, _darkColor.green / 255.0)
        ..setFloat(8, _darkColor.blue / 255.0)
        ..setFloat(9, 1.0)
        ..setFloat(10, _luminanceBias)
        ..setImageSampler(0, image);

      final paint = Paint()
        ..shader = shader
        ..filterQuality = FilterQuality.none
        ..isAntiAlias = false;

      context.canvas.save();
      context.canvas.translate(offset.dx, offset.dy);
      context.canvas.drawRect(Offset.zero & size, paint);
      context.canvas.restore();

      image.dispose();
    } catch (_) {
      // Fallback if rasterization is unsupported in current test harness
      super.paint(context, offset);
    }
  }
}
```

### Step 3 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/core
```

> **NEXT STEP**: File `03-dither-shader-and-flame-viewport.md` is complete. Proceed immediately to **[`04-offline-state-and-name-generator.md` — Step 1: Immutable Domain Models & JoJo Name Generator](04-offline-state-and-name-generator.md#step-1-immutable-domain-models--jojo-name-generator)**.
