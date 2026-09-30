# Design: 03 1-Bit Dithered Sprite Engine (Flame)

This document details the multi-frame bitmap spritesheet data structures, high-framerate animation engine, and character rendering rules for digital pets in the **Unix Tamagotchi**, utilizing Flame.

---

## 1. 1-Bit Dithered Sprite Design Rules

1. **Pixel Art Format**: Pets are drawn as actual pixel art using PNG sprite sheets, rather than ASCII text characters.
2. **Animation Sheets**: Every pet has a single PNG sprite sheet containing all frames for various animation states, organized in a consistent grid.
3. **Framerate**: Animations run at smooth **30+ FPS** (with tweens, breathing, blinking, and particle effects).
4. **Rendering Pipeline**: Sprites are drawn in a Flame game viewport at a low virtual resolution (e.g., 256×256) and upscaled using nearest-neighbor filtering to achieve crisp, chunky pixels. Shading and volume are added via a post-processing Bayer dithering fragment shader.

---

## 2. Dart Spritesheet Models & Catalog (`lib/core/sprite_engine/`)

The `PetDefinition` model references asset paths and grid data rather than hardcoded text strings.

```dart
class PetDefinition {
  final String petType;
  final String displayName;
  final int priceCredits;
  final String spriteSheetAsset; // e.g. 'bunny_spritesheet.png'
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

## 3. Pet Definitions (e.g., `lib/core/sprite_engine/bunny_sprites.dart`)

```dart
import 'package:flame/sprite.dart';

final bunnyDefinition = PetDefinition(
  petType: 'bunny',
  displayName: 'Terminal Bunny',
  priceCredits: 120,
  spriteSheetAsset: 'pets/bunny_spritesheet.png',
  frameWidth: 64,
  frameHeight: 64,
  actions: {
    // Idle cycle row 0, 4 frames, 0.2s per frame
    'idle': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.2,
      textureSize: Vector2(64, 64),
      texturePosition: Vector2(0, 0),
    ),

    // Eat cycle row 1, 4 frames
    'eating': SpriteAnimationData.sequenced(
      amount: 4,
      stepTime: 0.15,
      textureSize: Vector2(64, 64),
      texturePosition: Vector2(0, 64),
    ),

    // Sleep cycle row 2, 2 frames
    'sleeping': SpriteAnimationData.sequenced(
      amount: 2,
      stepTime: 0.5,
      textureSize: Vector2(64, 64),
      texturePosition: Vector2(0, 128),
    ),

    // Play cycle row 3, 6 frames
    'playing': SpriteAnimationData.sequenced(
      amount: 6,
      stepTime: 0.1,
      textureSize: Vector2(64, 64),
      texturePosition: Vector2(0, 192),
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
