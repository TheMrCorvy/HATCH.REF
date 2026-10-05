# Furniture: 02 Data Model & Ownership

## 1. Relational Schema (PostgreSQL)

To support the multiplayer 'group of 1' ownership model in the future Supabase backend, the database separates catalog definitions from instantiated inventory.

```sql
-- Catalog Definitions (Read-Only to Users)
CREATE TABLE furniture_catalog (
    id VARCHAR(50) PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    stat_modifiers JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- Purchased Inventory
CREATE TABLE furniture_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    catalog_item_id VARCHAR(50) REFERENCES furniture_catalog(id),
    purchased_by_user_id UUID NOT NULL REFERENCES auth.users(id),
    placed_in_group_id UUID NOT NULL REFERENCES groups(id),
    position_slot INT,
    purchased_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexing for fast lookups in habitats
CREATE INDEX idx_furniture_group_id ON furniture_instances(placed_in_group_id);
```

## 2. Ownership & Dissolution Rules

The Unix Tamagotchi ecosystem groups kaijus, but limits true asset ownership to individuals.

> [!IMPORTANT]
> A user's `purchased_by_user_id` **never changes**. This ensures no loss of virtual property when relationships/groups change.

*   **Group Sharing:** All members (SOLO, COUPLE, FAMILY, FRIENDS) in a group can see the furniture in their shared habitat. Any kaiju belonging to the group receives the passive stat modifiers.
*   **Dissolution Protocol:** If a group is dissolved (e.g., a COUPLE breaks up):
    *   The backend triggers a re-assignment query.
    *   `UPDATE furniture_instances SET placed_in_group_id = (user's solo group id) WHERE purchased_by_user_id = user.id`
    *   Furniture immediately returns to the original purchaser's solo group.
    *   If a user didn't purchase anything, they will spawn back into the default empty terminal room.

## 3. Dart Data Models

Using Freezed for immutable local data models in `lib/models/furniture_model.dart`:

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'furniture_model.freezed.dart';
part 'furniture_model.g.dart';

@freezed
class FurnitureItem with _$FurnitureItem {
  const factory FurnitureItem({
    required String id,
    @JsonKey(name: 'catalog_item_id') required String catalogItemId,
    @JsonKey(name: 'purchased_by_user_id') required String purchasedByUserId,
    @JsonKey(name: 'placed_in_group_id') required String placedInGroupId,
    @JsonKey(name: 'position_slot') int? positionSlot,
    @JsonKey(name: 'purchased_at') required DateTime purchasedAt,
  }) = _FurnitureItem;

  factory FurnitureItem.fromJson(Map<String, dynamic> json) => _$FurnitureItemFromJson(json);
}
```

## 4. State Management (Riverpod)

The Riverpod layer monitors the active group ID and fetches the respective furniture subset. 

```dart
// lib/providers/furniture_provider.dart

final activeGroupFurnitureProvider = FutureProvider<List<FurnitureItem>>((ref) async {
  final currentGroupId = ref.watch(currentGroupIdProvider);
  final repository = ref.read(furnitureRepositoryProvider);
  
  if (currentGroupId == null) return [];
  
  return await repository.fetchFurnitureForGroup(currentGroupId);
});
```
