# Design: 03 1-Bit Dithered Sprite Engine (Flame)

This document details the multi-frame bitmap spritesheet data structures, high-framerate animation engine, and character rendering rules for digital kaijus in the **Unix Tamagotchi**, utilizing Flame.

---

## 1. 1-Bit Dithered Sprite Design Rules

1. **Pixel Art Format**: Kaijus are drawn as authentic pixel art using PNG sprite sheets, rather than ASCII text characters.
2. **Animation Sheets**: Every Kaiju has a PNG sprite sheet containing all frames for its animation states (idle, eating, sleeping, rampaging/playing), organized in a consistent grid.
3. **Framerate**: Animations run at smooth **30+ FPS** (with breathing cycles, dorsal fin glow tweens, and atomic breath particle dispersal).
4. **Visual Standard**: The aesthetic benchmark is defined by `Desing References/Godzila.webp`, depicting Godzilla looming over urban skyscrapers while unleashing a dithered cone of atomic breath.
5. **Rendering Pipeline**: Sprites are drawn in a Flame game viewport at a low virtual resolution (e.g., 256×256) and upscaled using nearest-neighbor filtering to achieve crisp, chunky pixels. Shading, volume, and energy blasts are processed via a Bayer dithering fragment shader.

---

## 2. Dart Spritesheet Models & Catalog (`lib/core/sprite_engine/`)

The `KaijuDefinition` model references asset paths and grid data:

```dart
class KaijuDefinition {
  final String kaijuType;
  final String displayName;
  final int priceCredits;
  final String spriteSheetAsset; // e.g. 'kaijus/godzilla_spritesheet.png'
  final int frameWidth;
  final int frameHeight;
  final Map<String, SpriteAnimationData> actions;

  const KaijuDefinition({
    required this.kaijuType,
    required this.displayName,
    required this.priceCredits,
    required this.spriteSheetAsset,
    required this.frameWidth,
    required this.frameHeight,
    required this.actions,
  });

  SpriteAnimationData? getAnimationData(String action) {
    return actions[action] ?? actions['idle'];
  }
}
```

---

## 3. Kaiju Definitions (e.g., `lib/core/sprite_engine/godzilla_sprites.dart`)

```dart
import 'package:flame/sprite.dart';

final godzillaDefinition = KaijuDefinition(
  kaijuType: 'godzilla',
  displayName: 'Godzilla',
  priceCredits: 120,
  spriteSheetAsset: 'kaijus/godzilla_spritesheet.png',
  frameWidth: 128,
  frameHeight: 128,
  actions: {
    // Idle cycle: row 0, 4 frames, 0.25s per frame (subtle breathing & tail sway)
    'idle': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.25,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 0),
    ),

    // Eat cycle: row 1, 4 frames (devouring a compressed ball of human people)
    'eating': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.2,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 128),
    ),

    // Sleep cycle: row 2, 2 frames (dormant slumber with smoke puff)
    'sleeping': SpriteAnimationData.sequenced(
      amount: 2,
      stepTime: 0.6,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 256),
    ),

    // Rampage / Play cycle: row 3, 6 frames (atomic breath sweep, matching Godzila.webp)
    'playing': SpriteAnimationData.sequenced(
      amount: 6,
      stepTime: 0.12,
      textureSize: Vector2(128, 128),
      texturePosition: Vector2(0, 384),
    ),
  },
);
```

---

## 4. Flame Integration: Kaiju Viewport Widget

The `KaijuViewport` is implemented as a Flame `GameWidget`, containing a `SpriteAnimationComponent`. This entirely replaces the old text-based approach.

```dart
import 'package:flame/game.dart';
import 'package:flame/components.dart';
import 'package:flutter/material.dart';

class KaijuGame extends FlameGame {
  final KaijuDefinition kaijuDef;
  String currentAction;
  late SpriteAnimationComponent kaijuComponent;

  KaijuGame({required this.kaijuDef, this.currentAction = 'idle'});

  @override
  Future<void> onLoad() async {
    final spriteSheet = await images.load(kaijuDef.spriteSheetAsset);
    
    final animationData = kaijuDef.getAnimationData(currentAction)!;
    final animation = SpriteAnimation.fromFrameData(spriteSheet, animationData);

    kaijuComponent = SpriteAnimationComponent(
      animation: animation,
      size: Vector2(kaijuDef.frameWidth.toDouble(), kaijuDef.frameHeight.toDouble()),
      position: size / 2,
      anchor: Anchor.center,
    );

    add(kaijuComponent);
  }

  void changeAction(String newAction) async {
    if (newAction == currentAction) return;
    currentAction = newAction;
    
    final spriteSheet = await images.load(kaijuDef.spriteSheetAsset);
    final animationData = kaijuDef.getAnimationData(currentAction)!;
    kaijuComponent.animation = SpriteAnimation.fromFrameData(spriteSheet, animationData);
  }
}

class KaijuViewport extends StatelessWidget {
  final KaijuDefinition kaijuDef;
  final String action;

  const KaijuViewport({
    super.key,
    required this.kaijuDef,
    required this.action,
  });

  @override
  Widget build(BuildContext context) {
    // The GameWidget runs the Flame game loop (30+ FPS) rendering the kaiju
    return Container(
      color: const Color(0xFFC5BEAA), // Khaki terminal background
      child: GameWidget(
        game: KaijuGame(kaijuDef: kaijuDef, currentAction: action),
      ),
    );
  }
}
```
