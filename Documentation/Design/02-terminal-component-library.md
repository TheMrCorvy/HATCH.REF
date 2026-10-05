# Design: 02 Terminal Component Library (Flutter)

This document provides Flutter widget implementations for the unified UI component system used across the **Unix Tamagotchi**, strictly adhering to the industrial terminal aesthetic.

---

## 1. `<RetroButton>` (Terminal Action Button)

Renders a terminal prompt button with bracket styling (`[ > ACTION ]`). Active or focused states use the copper accent color.

```dart
import 'package:flutter/material.dart';

class RetroButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool disabled;
  final bool isActive;

  const RetroButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.disabled = false,
    this.isActive = false,
  });

  @override
  Widget build(BuildContext context) {
    final textColor = disabled 
        ? const Color(0xFF888888) 
        : (isActive ? const Color(0xFFB85E2B) : const Color(0xFF141512));
    
    final borderColor = disabled 
        ? const Color(0xFF888888) 
        : const Color(0xFF141512);

    return InkWell(
      onTap: disabled ? null : onPressed,
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: borderColor, width: 1.5),
          color: const Color(0xFFC5BEAA), // Khaki Background
        ),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        child: Text(
          '[ > ${label.toUpperCase()} ]',
          style: TextStyle(
            fontFamily: 'VT323',
            fontSize: 18,
            color: textColor,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
```

---

## 2. `<TerminalProgressBar>` (Stat Meter Widget)

Renders a segmented bar that simulates shading by fading from solid fill → ticks → checkerboard hatch → empty. Uses the 3-color palette (Charcoal, Khaki, Copper).

```dart
import 'package:flutter/material.dart';

class TerminalProgressBar extends StatelessWidget {
  final String label;
  final int value; // 0 to 100
  final int totalBlocks;

  const TerminalProgressBar({
    super.key,
    required this.label,
    required this.value,
    this.totalBlocks = 10,
  });

  @override
  Widget build(BuildContext context) {
    final clamped = value.clamp(0, 100);
    final filled = ((clamped / 100) * totalBlocks).round();
    final empty = totalBlocks - filled;

    // Approximating the dithered shading via text characters for the terminal UI
    final bar = '█' * filled + '░' * empty;
    
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        children: [
          SizedBox(
            width: 90,
            child: Text(
              label.toUpperCase().padRight(9),
              style: const TextStyle(
                fontFamily: 'VT323',
                fontSize: 18,
                color: Color(0xFFB85E2B), // Copper accent
              ),
            ),
          ),
          Text(
            '[$bar] $clamped%',
            style: const TextStyle(
              fontFamily: 'VT323',
              fontSize: 18,
              color: Color(0xFF141512), // Charcoal ink
              letterSpacing: 1.0,
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 3. `<BottomNavigationBar>` (Persistent Navigation)

Monospace terminal tabs with copper accent highlighting.

```dart
import 'package:flutter/material.dart';

class RetroBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onIndexChanged;

  const RetroBottomNav({
    super.key,
    required this.currentIndex,
    required this.onIndexChanged,
  });

  @override
  Widget build(BuildContext context) {
    final items = ['01:ROOM', '02:SHOP', '03:SWAP', '04:CONF'];

    return Container(
      decoration: const BoxDecoration(
        color: Color(0xFFC5BEAA), // Khaki Background
        border: Border(
          top: BorderSide(
            color: Color(0xFF141512), // Charcoal ink
            width: 1.5,
          ),
        ),
      ),
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: List.generate(items.length, (i) {
          final isSelected = currentIndex == i;
          final label = items[i];

          return GestureDetector(
            onTap: () => onIndexChanged(i),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              color: isSelected ? const Color(0xFF141512) : Colors.transparent, // Invert on selection
              child: Text(
                '[$label]',
                style: TextStyle(
                  fontFamily: 'VT323',
                  fontSize: 17,
                  color: isSelected ? const Color(0xFFC5BEAA) : const Color(0xFF141512),
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          );
        }),
      ),
    );
  }
}
```

---

## 4. New Terminal Widgets

### `<HazardStripeDecoration>`
Adds diagonal black/cream stripes for borders and warnings.

```dart
import 'package:flutter/material.dart';

class HazardStripeDecoration extends StatelessWidget {
  final double height;
  
  const HazardStripeDecoration({super.key, this.height = 10.0});

  @override
  Widget build(BuildContext context) {
    // CustomPainter or ShaderMask used here to draw diagonal stripes
    // using Color(0xFF141512) and Color(0xFFC5BEAA).
    return Container(
      height: height,
      color: const Color(0xFF141512), // Placeholder for actual stripe implementation
      child: const Text(
        '\\\\\\\\\\\\\\\\', 
        style: TextStyle(color: Color(0xFFC5BEAA), fontSize: 10, letterSpacing: 2)
      ),
    );
  }
}
```

### `<TerminalLogPanel>`
A rolling log of system and game events.

```dart
import 'package:flutter/material.dart';

class TerminalLogPanel extends StatelessWidget {
  final List<String> logs;

  const TerminalLogPanel({super.key, required this.logs});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      padding: const EdgeInsets.all(8.0),
      color: const Color(0xFF141512), // Charcoal Background
      child: ListView.builder(
        itemCount: logs.length,
        itemBuilder: (context, index) {
          return Text(
            '> ${logs[index]}',
            style: const TextStyle(
              fontFamily: 'VT323',
              fontSize: 14,
              color: Color(0xFFC5BEAA), // Khaki text
            ),
          );
        },
      ),
    );
  }
}
```

### `<SystemHeaderBar>`
Top diagnostic header showing system status.

```dart
import 'package:flutter/material.dart';

class SystemHeaderBar extends StatelessWidget {
  final String subSystem;
  
  const SystemHeaderBar({super.key, required this.subSystem});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8.0),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: Color(0xFF141512), width: 1.5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('SUB_SYS: $subSystem', style: const TextStyle(fontFamily: 'VT323', fontSize: 16)),
          const Text('SECURED_SESSION', style: TextStyle(fontFamily: 'VT323', fontSize: 16)),
        ],
      ),
    );
  }
}
```

### `<CameraReticleOverlay>`
Decorative camera corner marks around the kaiju viewport.

```dart
import 'package:flutter/material.dart';

class CameraReticleOverlay extends StatelessWidget {
  final Widget child;

  const CameraReticleOverlay({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        const Positioned(top: 0, left: 0, child: Text('┌', style: TextStyle(fontSize: 24, fontFamily: 'VT323'))),
        const Positioned(top: 0, right: 0, child: Text('┐', style: TextStyle(fontSize: 24, fontFamily: 'VT323'))),
        const Positioned(bottom: 0, left: 0, child: Text('└', style: TextStyle(fontSize: 24, fontFamily: 'VT323'))),
        const Positioned(bottom: 0, right: 0, child: Text('┘', style: TextStyle(fontSize: 24, fontFamily: 'VT323'))),
      ],
    );
  }
}
```
