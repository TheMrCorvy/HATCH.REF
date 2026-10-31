# Ownership: 03 Solo ↔ Group Transitions

## 1. Lifecycle Overview
The player lifecycle seamlessly flows between solo and multiplayer contexts without losing progression or ownership context.

1. **Registration**: Auto-creation of `SOLO` group.
2. **Multiplayer (`COUPLE` or `FRIENDS`)**: User touches phones once with their partner or friend (or shares a single-use invite code) to share their Kaiju in a `COUPLE` or `FRIENDS` group.
3. **Dissolution/Leaving**: Group disbands, user returns to `SOLO` group (with cloned shared kaijus).

## 2. Transition Mechanics

### Sharing a Kaiju & Joining a Group
When a user touches phones for the first time with their partner (`COUPLE`) or friend (`FRIENDS`) to share their Kaiju:
- The selected Kaiju from the initiator's `SOLO` group can be transferred directly into the shared `COUPLE` or `FRIENDS` group (and set as its `active_group_kaijus` entry) so both users immediately see and care for that exact same Kaiju online.
- Any other unshared Kaijus in the user's personal `SOLO` group remain in the `SOLO` group, which enters a **dormant** state (`0.1x` standby stat decay) while the user is actively viewing the shared multiplayer group.

### Leaving a Group
When a user leaves (or the group dissolves), they receive clones of the shared kaijus, which are added to their `SOLO` group. The `SOLO` group fully reactivates.

### Switching Active Groups
A user can belong to their `SOLO` group plus a `COUPLE` and/or `FRIENDS` group. The application UI shows **one active group at a time**, and within that group, all members see the **same active Kaiju** (`active_group_kaijus`).

## 3. User Lifecycle State Diagram
```mermaid
stateDiagram-v2
    [*] --> ActiveSolo: Register
    
    state ActiveSolo {
        [*] --> ViewSoloRoom
        ViewSoloRoom --> InteractSoloKaijus
    }
    
    ActiveSolo --> ActiveMultiplayer: One-Time Touch Pairing / Switch to Group
    
    state ActiveMultiplayer {
        [*] --> ViewSharedRoom
        ViewSharedRoom --> InteractSharedKaijus
        note right of ViewSharedRoom
            Solo group enters 
            Dormant state (0.1x decay)
        end note
    }
    
    ActiveMultiplayer --> ActiveSolo: Leave/Switch to Solo
    ActiveMultiplayer --> ActiveSolo: Group Dissolves (Clone Kaijus)
```

## 4. Flutter/Dart Implementation Model
The Riverpod state management needs to reflect the active group context clearly.

```dart
// lib/models/group_context.dart

enum GroupType { solo, couple, friends }

class GroupContext {
  final String groupId;
  final String groupName;
  final GroupType type;
  final bool isDormant; // Relevant for background processing

  const GroupContext({
    required this.groupId,
    required this.groupName,
    required this.type,
    this.isDormant = false,
  });
  
  factory GroupContext.fromJson(Map<String, dynamic> json) {
    return GroupContext(
      groupId: json['id'],
      groupName: json['name'],
      type: GroupType.values.firstWhere((e) => e.name.toUpperCase() == json['group_type']),
    );
  }
}

// lib/providers/active_group_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ActiveGroupNotifier extends StateNotifier<GroupContext?> {
  ActiveGroupNotifier() : super(null);

  void switchGroup(GroupContext newGroup) {
    // Save current group state, trigger UI transition, load new group kaijus
    state = newGroup;
  }
}

final activeGroupProvider = StateNotifierProvider<ActiveGroupNotifier, GroupContext?>((ref) {
  return ActiveGroupNotifier();
});
```

## 5. Edge Cases
- **Accumulation on Dissolution**: If a user has 5 kaijus in their `SOLO` group, joins a multiplayer group with 3 kaijus, and that group dissolves, the user ends up with 8 kaijus. Since there is no server-side kaiju cap, this is valid. The UI must handle variable-length kaiju lists (scrollable terminal view).
