# Payments: 04 Security & Anti-Cheat Architecture (Flutter)

This document specifies the defense-in-depth mechanisms for protecting credit balances, in-app purchases, and pet state integrity in Flutter for the **Unix Tamagotchi**.

---

## 1. Flutter Code Obfuscation & Binary Hardening

Flutter compiles to native ARM machine code (AOT), which is already significantly harder to decompile than Java/Kotlin bytecode or JavaScript bundles. To further thwart reverse engineers using tools like Ghidra:

### Enabling Obfuscation in Flutter Builds:
```bash
flutter build appbundle --release \
  --obfuscate \
  --split-debug-info=./build/debug-info
```
- `--obfuscate`: Strips class names, method names, and identifiers from compiled symbols.
- `--split-debug-info`: Extracts symbol maps out of the binary, storing them privately for crash analysis.

---

## 2. Keystore-Backed Storage (`flutter_secure_storage`)

For sensitive local variables (such as local encryption keys and user auth tokens), use **`flutter_secure_storage`**, which binds directly to the **Android Keystore** and **iOS Keychain**:

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureVault {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
      keyCipherAlgorithm: KeyCipherAlgorithm.RSA_ECB_OAEPWithSHA_256AndMGF1Padding,
      storageCipherAlgorithm: StorageCipherAlgorithm.AES_GCM_NoPadding,
    ),
  );

  static Future<void> saveAuthToken(String token) async {
    await _storage.write(key: 'jwt_token', value: token);
  }
}
```

---

## 3. Anti-Clock-Tampering (Monotonic Time Tracking in Dart)

```dart
class TimeIntegrityCheck {
  static int _lastKnownEpoch = DateTime.now().millisecondsSinceEpoch;
  static final Stopwatch _stopwatch = Stopwatch()..start();

  /// Validates that system time has not moved backward relative to the monotonic CPU clock
  static bool isClockTampered() {
    final currentEpoch = DateTime.now().millisecondsSinceEpoch;
    final elapsedWallTime = currentEpoch - _lastKnownEpoch;
    final elapsedCpuTime = _stopwatch.elapsedMilliseconds;

    // If wall clock moved backward or deviated wildly from CPU clock
    if (elapsedWallTime < -5000 || (elapsedWallTime - elapsedCpuTime).abs() > 60000) {
      debugPrint('[SECURITY ALERT] Clock tampering detected!');
      return true;
    }

    _lastKnownEpoch = currentEpoch;
    return false;
  }
}
```
