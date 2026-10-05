# Design: 03 1-Bit Dithered Sprite Engine (Flame)

This document details the multi-frame bitmap spritesheet data structures, high-framerate animation engine, and character rendering rules for digital pets in the **Unix Tamagotchi**, utilizing Flame.

---

## 1. 1-Bit Dithered Sprite Design Rules

1. **Pixel Art Format**: Kaijus are drawn as authentic pixel art using PNG sprite sheets, rather than ASCII text characters.
2. **Animation Sheets**: Every Kaiju has a PNG sprite sheet containing all frames for its animation states (idle, eating, sleeping, rampaging/playing), organized in a consistent grid.
3. **Framerate**: Animations run at smooth **30+ FPS** (with breathing cycles, dorsal fin glow tweens, and atomic breath particle dispersal).
4. **Visual Standard**: The aesthetic benchmark is defined by `Desing References/Godzila.webp`, depicting Godzilla looming over urban skyscrapers while unleashing a dithered cone of atomic breath.
5. **Rendering Pipeline**: Sprites are drawn in a Flame game viewport at a low virtual resolution (e.g., 256×256) and upscaled using nearest-neighbor filtering to achieve crisp, chunky pixels. Shading, volume, and energy blasts are processed via a Bayer dithering fragment shader.

---

## 2. Dart Spritesheet Models & Catalog (`lib/core/sprite_engine/`)

The `PetDefinition` model references asset paths and grid data:

```dart
class PetDefinition {
  final String petType;
  final String displayName;
  final int priceCredits;
  final String spriteSheetAsset; // e.g. 'kaijus/godzilla_spritesheet.png'
  final int frameWidth;
  final int frameHeight;
  final Map<String, SpriteAnimationData> actions;

  const PetDefinition({
    required this.petType,
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

final godzillaDefinition = PetDefinition(
  petType: 'godzilla',
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

## 4. Flame Integration: Pet Viewport Widget

The `PetViewport` is implemented as a Flame `GameWidget`, containing a `SpriteAnimationComponent`. This entirely replaces the old text-based approach.

```dart
import 'package:flame/game.dart';
import 'package:flame/components.dart';
import 'package:flutter/material.dart';

class PetGame extends FlameGame {
  final PetDefinition petDef;
  String currentAction;
  late SpriteAnimationComponent petComponent;

  PetGame({required this.petDef, this.currentAction = 'idle'});

  @override
  Future<void> onLoad() async {
    final spriteSheet = await images.load(petDef.spriteSheetAsset);
    
    final animationData = petDef.getAnimationData(currentAction)!;
    final animation = SpriteAnimation.fromFrameData(spriteSheet, animationData);

    petComponent = SpriteAnimationComponent(
      animation: animation,
      size: Vector2(petDef.frameWidth.toDouble(), petDef.frameHeight.toDouble()),
      position: size / 2,
      anchor: Anchor.center,
    );

    add(petComponent);
  }

  void changeAction(String newAction) async {
    if (newAction == currentAction) return;
    currentAction = newAction;
    
    final spriteSheet = await images.load(petDef.spriteSheetAsset);
    final animationData = petDef.getAnimationData(currentAction)!;
    petComponent.animation = SpriteAnimation.fromFrameData(spriteSheet, animationData);
  }
}

class PetViewport extends StatelessWidget {
  final PetDefinition petDef;
  final String action;

  const PetViewport({
    super.key,
    required this.petDef,
    required this.action,
  });

  @override
  Widget build(BuildContext context) {
    // The GameWidget runs the Flame game loop (30+ FPS) rendering the pet
    return Container(
      color: const Color(0xFFC5BEAA), // Khaki terminal background
      child: GameWidget(
        game: PetGame(petDef: petDef, currentAction: action),
      ),
    );
  }
}
```
