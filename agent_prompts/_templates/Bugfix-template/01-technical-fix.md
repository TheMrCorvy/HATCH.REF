# Technical Implementation: `<Bugfix / Feature Name>`

> **Parent Guide**: [`README.md`](README.md)

---

## Step 1: Apply Code Fix

### Target Files
- `lib/<path>/<file>.dart`

### Technical Instructions & Diffs
Apply the following changes:

```diff
-// Old implementation
+// New implementation
```

### Step 1 Verification
Run:
```bash
flutter analyze
```

> **NEXT STEP**: Once `flutter analyze` passes with 0 errors, proceed immediately to **[Step 2: Add / Update Regression Tests & Sync `Documentation/`](#step-2-add--update-regression-tests--sync-documentation)** below.

---

## Step 2: Add / Update Regression Tests & Sync `Documentation/`

### 1. Regression Test
Add or update the corresponding test in `test/<unit|widget|integration>/<file>_test.dart`:

```dart
// Test verifying the fix
```

### 2. Mandatory `Documentation/` Sync Check (Single Source of Truth)
Check [`../../Documentation/`](../../Documentation/README.md):
- Does this fix alter any schema, state model, API signature, balance constant, or architectural flow documented in `Documentation/`?
- Was this bug caused by an ambiguity or error in `Documentation/`?
- **If YES**: Update the corresponding `Documentation/<Domain>/<file>.md` file right now before finishing your task.

> **FINAL STEP COMPLETE**: Once all tests pass (`flutter test`) and `Documentation/` is verified to be 100% in sync with the codebase, report completion to the user.
