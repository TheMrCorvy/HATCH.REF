# Customization: 02 Ownership & Group Behavior

This document details the ownership model, database schemas, and state management for customizations within the "group of 1" architecture.

## 1. Ownership Rules

The Unix Tamagotchi architecture dictates that pets belong to GROUPS, not individual users. Customizations, however, are managed with the following rules:

- **Set By (User):** Customizations are created and owned by a specific `user_id`. This ownership never changes.
- **Applied To (Group):** Customizations are applied to the active `group_id` the user is currently part of.
- **Dissolution Policy:** When a group dissolves, customizations do not disappear. Instead, they revert to the original user's solo group.
  - *SQL Action:* `UPDATE user_customizations SET group_id = (user's solo group) WHERE user_id = user.id`
- **Defaults:** If a member hasn't set a specific customization, they see the fallback DEFAULT values (e.g. #C5BEAA khaki / #141512 charcoal).

## 2. Visibility Rules

- **Client-Side Rendering:** The server stores per-user preferences. Each client renders the environment according to its authenticated user's preferences.
- **Isolated Views:** In a group, each member sees their own visual customizations (e.g., User A sees a green palette, User B sees an amber palette, both interacting with the same pet).
- **Shared Exceptions:** Pet nicknames are shared globally across the group.

## 3. Database Schema

The backend utilizes the following DDL for storing customization data.

```sql
-- Preset definitions available in the system
CREATE TABLE customization_presets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- e.g., 'palette', 'boot_message'
    parameters JSONB NOT NULL, -- e.g., {"uColorLight": "#C5BEAA", "uColorDark": "#141512"}
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User-specific customization state
CREATE TABLE user_customizations (
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    group_id UUID NOT NULL REFERENCES groups(id),
    customization_type VARCHAR(50) NOT NULL,
    preset_id UUID REFERENCES customization_presets(id),
    custom_params JSONB, -- Overrides or custom text (e.g., nickname, boot msg)
    set_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, group_id, customization_type)
);
```

## 4. Flutter / Dart Implementation

### 4.1 Data Models

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'customization_models.freezed.dart';
part 'customization_models.g.dart';

@freezed
class CustomizationPreset with _$CustomizationPreset {
  const factory CustomizationPreset({
    required String id,
    required String name,
    required String type,
    required Map<String, dynamic> parameters,
  }) = _CustomizationPreset;

  factory CustomizationPreset.fromJson(Map<String, dynamic> json) =>
      _$CustomizationPresetFromJson(json);
}

@freezed
class UserCustomization with _$UserCustomization {
  const factory UserCustomization({
    required String userId,
    required String groupId,
    required String customizationType,
    String? presetId,
    Map<String, dynamic>? customParams,
    required DateTime setAt,
  }) = _UserCustomization;

  factory UserCustomization.fromJson(Map<String, dynamic> json) =>
      _$UserCustomizationFromJson(json);
}
```

### 4.2 State Management (Riverpod)

A Riverpod provider tracks the active customizations and drives the UI/shader updates.

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'customization_models.dart';

part 'active_customizations_provider.g.dart';

@riverpod
class ActiveCustomizations extends _$ActiveCustomizations {
  @override
  FutureOr<List<UserCustomization>> build() async {
    // Fetch user customizations based on current user_id and active group_id
    final repository = ref.read(customizationRepositoryProvider);
    return await repository.fetchActiveCustomizations();
  }

  /// Helper to get the current palette colors
  Map<String, String> getPaletteUniforms() {
    final state = this.state.valueOrNull ?? [];
    final paletteConfig = state.where((c) => c.customizationType == 'palette').firstOrNull;
    
    // Return custom or default colors
    if (paletteConfig?.customParams != null) {
        return {
            'uColorLight': paletteConfig!.customParams!['uColorLight'],
            'uColorDark': paletteConfig.customParams!['uColorDark'],
        };
    }
    
    // Default Unix Tamagotchi Palette
    return {
      'uColorLight': '#C5BEAA', // Khaki
      'uColorDark': '#141512', // Charcoal
    };
  }
}
```

### 4.3 Shader Integration

The 1-bit dithering shader receives `uColorLight` and `uColorDark` uniforms based on the Riverpod state, enabling seamless, per-user palette swaps on the fly.
