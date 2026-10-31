# Technical Implementation 02: Terminal Widget Library

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Design/01-design-system-and-theming.md`](../../Documentation/Design/01-design-system-and-theming.md), [`Documentation/Design/02-terminal-component-library.md`](../../Documentation/Design/02-terminal-component-library.md), [`Documentation/Design/05-1bit-terminal-wireframes.md`](../../Documentation/Design/05-1bit-terminal-wireframes.md)

---

## Step 1: Core Terminal Chrome & Decorations

### Objective
Implement the decorative terminal chrome widgets in `lib/core/widgets/`:
1. `LcdGridBackground` — Renders the subtle 1-bit pixel matrix grid over `AppPalette.background` (matching `Desing References/Prototipes/*.png`) and frames the screen with a double-line industrial terminal border.
2. `HazardStripeDecoration` — Draws crisp 45° diagonal alternating caution stripes using `CustomPainter` and `AppPalette` tokens.
3. `CameraReticleOverlay` — Draws corner camera reticles (`┌ ┐ └ ┘`) and optional top-left (`[LOC: CH-04]`, `[FRM: 60HZ]`) and bottom-right (`TYPE`, `STAT`) viewport telemetry labels.
4. `DottedDivider` & `TerminalSectionHeader` — Industrial dividers for diagnostic tables and sections.

### Target File: `apps/mobile/lib/core/widgets/lcd_grid_background.dart`
Create `apps/mobile/lib/core/widgets/lcd_grid_background.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

/// Wraps a screen in the signature LCD dot-matrix grid texture and double terminal border.
class LcdGridBackground extends StatelessWidget {
  final Widget child;
  final bool showOuterFrame;

  const LcdGridBackground({
    super.key,
    required this.child,
    this.showOuterFrame = true,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);

    return Container(
      color: palette.background,
      child: CustomPaint(
        painter: _LcdGridPainter(
          gridColor: palette.foreground.withOpacity(0.06),
        ),
        child: showOuterFrame
            ? Container(
                margin: const EdgeInsets.all(6.0),
                decoration: BoxDecoration(
                  border: Border.all(color: palette.foreground, width: 2.0),
                ),
                padding: const EdgeInsets.all(2.0),
                child: Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: palette.foreground, width: 1.0),
                  ),
                  child: child,
                ),
              )
            : child,
      ),
    );
  }
}

class _LcdGridPainter extends CustomPainter {
  final Color gridColor;

  const _LcdGridPainter({required this.gridColor});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = gridColor
      ..strokeWidth = 1.0;

    const double step = 6.0;
    for (double x = 0; x < size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (double y = 0; y < size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant _LcdGridPainter oldDelegate) {
    return oldDelegate.gridColor != gridColor;
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/hazard_stripe_decoration.dart`
Create `apps/mobile/lib/core/widgets/hazard_stripe_decoration.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

/// Renders diagonal 45-degree caution stripes using active AppPalette tokens.
class HazardStripeDecoration extends StatelessWidget {
  final double height;
  final bool isEmergency;

  const HazardStripeDecoration({
    super.key,
    this.height = 12.0,
    this.isEmergency = false,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    final stripeColor = isEmergency ? palette.emergency : palette.foreground;

    return SizedBox(
      height: height,
      width: double.infinity,
      child: ClipRect(
        child: CustomPaint(
          painter: _HazardStripePainter(
            stripeColor: stripeColor,
            backgroundColor: palette.background,
          ),
        ),
      ),
    );
  }
}

class _HazardStripePainter extends CustomPainter {
  final Color stripeColor;
  final Color backgroundColor;

  const _HazardStripePainter({
    required this.stripeColor,
    required this.backgroundColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final bgPaint = Paint()..color = backgroundColor;
    canvas.drawRect(Offset.zero & size, bgPaint);

    final fgPaint = Paint()
      ..color = stripeColor
      ..style = PaintingStyle.fill;

    const double stripeWidth = 10.0;
    const double gapWidth = 10.0;
    const double step = stripeWidth + gapWidth;

    for (double x = -size.height; x < size.width + size.height; x += step) {
      final path = Path()
        ..moveTo(x, size.height)
        ..lineTo(x + stripeWidth, size.height)
        ..lineTo(x + stripeWidth + size.height, 0)
        ..lineTo(x + size.height, 0)
        ..close();
      canvas.drawPath(path, fgPaint);
    }
  }

  @override
  bool shouldRepaint(covariant _HazardStripePainter oldDelegate) {
    return oldDelegate.stripeColor != stripeColor ||
        oldDelegate.backgroundColor != backgroundColor;
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/camera_reticle_overlay.dart`
Create `apps/mobile/lib/core/widgets/camera_reticle_overlay.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

/// Decorative camera corner marks (`┌ ┐ └ ┘`) and optional HUD telemetry around viewports.
class CameraReticleOverlay extends StatelessWidget {
  final Widget child;
  final String? topLeftLine1;
  final String? topLeftLine2;
  final String? bottomRightLine1;
  final String? bottomRightLine2;

  const CameraReticleOverlay({
    super.key,
    required this.child,
    this.topLeftLine1,
    this.topLeftLine2,
    this.bottomRightLine1,
    this.bottomRightLine2,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    final reticleStyle = TextStyle(
      fontFamily: 'VT323',
      fontSize: 22,
      height: 1.0,
      color: palette.foreground,
      fontWeight: FontWeight.bold,
    );
    final hudStyle = TextStyle(
      fontFamily: 'VT323',
      fontSize: 13,
      height: 1.1,
      color: palette.foreground.withOpacity(0.75),
    );

    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: palette.foreground, width: 1.5),
      ),
      child: Stack(
        fit: StackFit.expand,
        children: [
          child,
          Positioned(top: 2, left: 4, child: Text('┌', style: reticleStyle)),
          Positioned(top: 2, right: 4, child: Text('┐', style: reticleStyle)),
          Positioned(bottom: 2, left: 4, child: Text('└', style: reticleStyle)),
          Positioned(bottom: 2, right: 4, child: Text('┘', style: reticleStyle)),
          if (topLeftLine1 != null || topLeftLine2 != null)
            Positioned(
              top: 8,
              left: 16,
              child: IgnorePointer(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (topLeftLine1 != null) Text(topLeftLine1!, style: hudStyle),
                    if (topLeftLine2 != null) Text(topLeftLine2!, style: hudStyle),
                  ],
                ),
              ),
            ),
          if (bottomRightLine1 != null || bottomRightLine2 != null)
            Positioned(
              bottom: 8,
              right: 16,
              child: IgnorePointer(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    if (bottomRightLine1 != null)
                      Text(bottomRightLine1!, style: hudStyle),
                    if (bottomRightLine2 != null)
                      Text(bottomRightLine2!, style: hudStyle),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/dotted_divider.dart`
Create `apps/mobile/lib/core/widgets/dotted_divider.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class DottedDivider extends StatelessWidget {
  final double height;

  const DottedDivider({super.key, this.height = 12.0});

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    return SizedBox(
      height: height,
      width: double.infinity,
      child: CustomPaint(
        painter: _DottedLinePainter(color: palette.foreground.withOpacity(0.55)),
      ),
    );
  }
}

class _DottedLinePainter extends CustomPainter {
  final Color color;

  const _DottedLinePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 1.0;

    final y = size.height / 2;
    for (double x = 0; x < size.width; x += 4.0) {
      canvas.drawLine(Offset(x, y), Offset(x + 2.0, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant _DottedLinePainter oldDelegate) {
    return oldDelegate.color != color;
  }
}

class TerminalSectionHeader extends StatelessWidget {
  final String title;

  const TerminalSectionHeader({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          Text(
            title.toUpperCase(),
            style: TextStyle(
              fontFamily: 'VT323',
              fontSize: 19,
              fontWeight: FontWeight.bold,
              color: palette.foreground,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Container(
              height: 1.5,
              color: palette.foreground,
            ),
          ),
        ],
      ),
    );
  }
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/core/widgets
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 2: Interactive Terminal Controls, Bars & Navigation](#step-2-interactive-terminal-controls-bars--navigation)** in this file.

---

## Step 2: Interactive Terminal Controls, Bars & Navigation

### Objective
Implement the interactive terminal widgets in `lib/core/widgets/`:
1. `RetroButton` (`lib/core/widgets/retro_button.dart`) — Bracket-styled button (`[ > LABEL ]` or `[ LABEL ]`) with optional top icon, active copper state, inverted dark state, and disabled state.
2. `TerminalProgressBar` (`lib/core/widgets/terminal_progress_bar.dart`) — Supports both the 3-column framed vital card (`VitalMeterCard` for `VITALS.ENERGY`, `VITALS.SATUR`, `VITALS.JOY` matching `Desing References/Prototipes/Captura de pantalla 2026-09-29 185328.png`) and the horizontal segmented block bar (`[████████░░] 80%`).
3. `TerminalLogPanel` (`lib/core/widgets/terminal_log_panel.dart`) — Rolling diagnostic log box with `| > ` prefix lines.
4. `SystemHeaderBar` & `SystemFooterBar` (`lib/core/widgets/system_header_bar.dart`) — Top diagnostic bar (`SUB_SYS`, module version, timestamp) and bottom status bar (`MEMORY: 48KB/64KB`, `[SECURED_SESSION]`, `PID: 8832`).
5. `RetroBottomNav` (`lib/core/widgets/retro_bottom_nav.dart`) — Persistent 4-tab terminal bar (`[01:ROOM]`, `[02:SHOP]`, `[03:SWAP]`, `[04:CONF]`).
6. `TerminalSubTabBar` (`lib/core/widgets/terminal_sub_tab_bar.dart`) — Top 2-tab switcher (`[ SYS_DIAG ]` / `[ CUSTOMIZE ]`) used in `04:CONF`.

### Target File: `apps/mobile/lib/core/widgets/retro_button.dart`
Create `apps/mobile/lib/core/widgets/retro_button.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class RetroButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final bool disabled;
  final bool isActive;
  final bool isInverted;
  final bool includePromptArrow;
  final IconData? topIcon;
  final EdgeInsetsGeometry padding;

  const RetroButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.disabled = false,
    this.isActive = false,
    this.isInverted = false,
    this.includePromptArrow = true,
    this.topIcon,
    this.padding = const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);

    final Color bgColor;
    final Color fgColor;
    final Color borderColor;

    if (disabled) {
      bgColor = palette.background;
      fgColor = palette.disabled;
      borderColor = palette.disabled;
    } else if (isInverted) {
      bgColor = palette.foreground;
      fgColor = palette.background;
      borderColor = palette.foreground;
    } else if (isActive) {
      bgColor = palette.surface;
      fgColor = palette.accent;
      borderColor = palette.accent;
    } else {
      bgColor = palette.surface;
      fgColor = palette.foreground;
      borderColor = palette.foreground;
    }

    final formattedLabel = includePromptArrow
        ? '[ > ${label.toUpperCase()} ]'
        : '[ ${label.toUpperCase()} ]';

    return Material(
      color: bgColor,
      child: InkWell(
        onTap: disabled ? null : onPressed,
        child: Container(
          decoration: BoxDecoration(
            border: Border.all(color: borderColor, width: 1.5),
          ),
          padding: padding,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (topIcon != null) ...[
                Icon(topIcon, size: 18, color: fgColor),
                const SizedBox(height: 2),
              ],
              Text(
                formattedLabel,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: 'VT323',
                  fontSize: 18,
                  color: fgColor,
                  fontWeight: FontWeight.bold,
                  height: 1.0,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/terminal_progress_bar.dart`
Create `apps/mobile/lib/core/widgets/terminal_progress_bar.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

/// Standard horizontal ASCII/block stat meter (`VITALS.HUNGER [████████░░] 80%`).
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
    final palette = AppPalette.of(context);
    final clamped = value.clamp(0, 100);
    final filled = ((clamped / 100) * totalBlocks).round();
    final empty = totalBlocks - filled;
    final bar = '█' * filled + '░' * empty;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0),
      child: Row(
        children: [
          SizedBox(
            width: 110,
            child: Text(
              label.toUpperCase(),
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                fontFamily: 'VT323',
                fontSize: 17,
                color: palette.accent,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          Expanded(
            child: Text(
              '[$bar] $clamped%',
              style: TextStyle(
                fontFamily: 'VT323',
                fontSize: 17,
                color: palette.foreground,
                letterSpacing: 1.0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// Framed compact vital card matching `Desing References/Prototipes/Captura de pantalla 2026-09-29 185328.png`.
class VitalMeterCard extends StatelessWidget {
  final String label;
  final int value;

  const VitalMeterCard({
    super.key,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    final clamped = value.clamp(0, 100);
    const totalTicks = 10;
    final filledTicks = ((clamped / 100.0) * totalTicks).round();

    return Container(
      padding: const EdgeInsets.fromLTRB(6, 4, 6, 4),
      decoration: BoxDecoration(
        border: Border.all(color: palette.foreground, width: 1.2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label.toUpperCase(),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontFamily: 'VT323',
              fontSize: 14,
              color: palette.foreground,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 2),
          Row(
            children: List.generate(totalTicks, (i) {
              final isFilled = i < filledTicks;
              return Expanded(
                child: Container(
                  height: 6,
                  margin: const EdgeInsets.only(right: 1.5),
                  decoration: BoxDecoration(
                    color: isFilled ? palette.foreground : Colors.transparent,
                    border: Border.all(color: palette.foreground, width: 0.8),
                  ),
                ),
              );
            }),
          ),
          const SizedBox(height: 2),
          Align(
            alignment: Alignment.centerRight,
            child: Text(
              '$clamped%',
              style: TextStyle(
                fontFamily: 'VT323',
                fontSize: 15,
                color: palette.accent,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/terminal_log_panel.dart`
Create `apps/mobile/lib/core/widgets/terminal_log_panel.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class TerminalLogPanel extends StatelessWidget {
  final List<String> logs;
  final double height;

  const TerminalLogPanel({
    super.key,
    required this.logs,
    this.height = 68.0,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);

    return Container(
      height: height,
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
      decoration: BoxDecoration(
        color: palette.background,
        border: Border.all(color: palette.foreground, width: 1.2),
      ),
      child: ListView.builder(
        padding: EdgeInsets.zero,
        itemCount: logs.length,
        itemBuilder: (context, index) {
          final line = logs[index];
          final formatted = line.startsWith('>') ? line : '> $line';
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 1.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 2.5,
                  height: 14,
                  margin: const EdgeInsets.only(right: 6, top: 2),
                  color: palette.foreground,
                ),
                Expanded(
                  child: Text(
                    formatted,
                    style: TextStyle(
                      fontFamily: 'VT323',
                      fontSize: 15,
                      color: palette.foreground,
                      height: 1.1,
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/system_header_bar.dart`
Create `apps/mobile/lib/core/widgets/system_header_bar.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class SystemHeaderBar extends StatelessWidget {
  final String leftText;
  final String centerText;
  final String rightText;
  final bool highlightLeftValue;

  const SystemHeaderBar({
    super.key,
    required this.leftText,
    this.centerText = '0X4F92 // 1.0.4-BETA',
    this.rightText = '18:53:19',
    this.highlightLeftValue = false,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    final style = TextStyle(
      fontFamily: 'VT323',
      fontSize: 16,
      color: palette.foreground,
      fontWeight: FontWeight.bold,
    );

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: palette.foreground, width: 1.5),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Flexible(
            child: Text(
              leftText.toUpperCase(),
              overflow: TextOverflow.ellipsis,
              style: style.copyWith(
                color: highlightLeftValue ? palette.accent : palette.foreground,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 6.0),
            child: Text(centerText.toUpperCase(), style: style),
          ),
          Text(rightText.toUpperCase(), style: style),
        ],
      ),
    );
  }
}

class SystemFooterBar extends StatelessWidget {
  final String leftLabel;
  final String centerBadge;
  final String rightLabel;

  const SystemFooterBar({
    super.key,
    this.leftLabel = 'MEMORY: 48KB/64KB',
    this.centerBadge = 'SECURED_SESSION',
    this.rightLabel = 'PID: 8832',
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);
    final style = TextStyle(
      fontFamily: 'VT323',
      fontSize: 14,
      color: palette.foreground,
    );

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(leftLabel.toUpperCase(), style: style),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6.0, vertical: 1.5),
            color: palette.foreground,
            child: Text(
              centerBadge.toUpperCase(),
              style: style.copyWith(
                color: palette.background,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          Text(rightLabel.toUpperCase(), style: style),
        ],
      ),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/widgets/retro_bottom_nav.dart`
Create `apps/mobile/lib/core/widgets/retro_bottom_nav.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class RetroBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onIndexChanged;

  const RetroBottomNav({
    super.key,
    required this.currentIndex,
    required this.onIndexChanged,
  });

  static const List<String> tabs = [
    '01:ROOM',
    '02:SHOP',
    '03:SWAP',
    '04:CONF',
  ];

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);

    return Container(
      decoration: BoxDecoration(
        color: palette.background,
        border: Border(
          top: BorderSide(color: palette.foreground, width: 1.5),
        ),
      ),
      padding: const EdgeInsets.symmetric(vertical: 6.0, horizontal: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: List.generate(tabs.length, (i) {
          final isSelected = currentIndex == i;
          final label = tabs[i];

          return GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: () => onIndexChanged(i),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
              color: isSelected ? palette.foreground : Colors.transparent,
              child: Text(
                '[$label]',
                style: TextStyle(
                  fontFamily: 'VT323',
                  fontSize: 17,
                  color: isSelected ? palette.background : palette.foreground,
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

### Target File: `apps/mobile/lib/core/widgets/terminal_sub_tab_bar.dart`
Create `apps/mobile/lib/core/widgets/terminal_sub_tab_bar.dart`:

```dart
import 'package:flutter/material.dart';
import '../theme/app_palette.dart';

class TerminalSubTabBar extends StatelessWidget {
  final List<String> tabs;
  final int selectedIndex;
  final ValueChanged<int> onTabSelected;

  const TerminalSubTabBar({
    super.key,
    required this.tabs,
    required this.selectedIndex,
    required this.onTabSelected,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppPalette.of(context);

    return Row(
      children: List.generate(tabs.length, (index) {
        final isSelected = index == selectedIndex;
        return Expanded(
          child: Padding(
            padding: EdgeInsets.only(
              left: index == 0 ? 0 : 3.0,
              right: index == tabs.length - 1 ? 0 : 3.0,
            ),
            child: GestureDetector(
              onTap: () => onTabSelected(index),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                decoration: BoxDecoration(
                  color: isSelected ? palette.foreground : palette.surface,
                  border: Border.all(color: palette.foreground, width: 1.5),
                ),
                alignment: Alignment.center,
                child: Text(
                  tabs[index].toUpperCase(),
                  style: TextStyle(
                    fontFamily: 'VT323',
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                    color: isSelected ? palette.background : palette.foreground,
                  ),
                ),
              ),
            ),
          ),
        );
      }),
    );
  }
}
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/core
```

> **NEXT STEP**: File `02-terminal-widget-library.md` is complete. Proceed immediately to **[`03-dither-shader-and-flame-viewport.md` — Step 1: Bayer Dither Fragment Shader (Impeller-Safe)](03-dither-shader-and-flame-viewport.md#step-1-bayer-dither-fragment-shader-impeller-safe)**.
