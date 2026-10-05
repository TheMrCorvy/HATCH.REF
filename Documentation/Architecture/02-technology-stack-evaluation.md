# Architecture: 02 Technology Stack Evaluation

This document details the definitive technical stack for the **Unix Tamagotchi**, explaining why **Flutter (Dart 3.x) paired with Flame** was chosen over alternative frameworks (Godot, React Native, Unity, KMP) for our "Tactical 1-Bit Cyber-Specimen OS" aesthetic.

---

## 1. Framework Evaluation: Why Flutter + Flame Wins

The application demands a hybrid rendering model: ~70% of the experience consists of complex terminal UI (scrollable lists, store catalogs, tabs, sliders, data tables), while ~30% is a highly stylized, shader-driven kaiju viewport.

| Framework | UI Capabilities | Custom Shader/VFX | Ecosystem | Overall Score |
| :--- | :--- | :--- | :--- | :--- |
| **Flutter + Flame** | ⭐⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐⭐ (Great via FragmentProgram) | ⭐⭐⭐⭐⭐ | **9.5/10** |
| **Godot Engine** | ⭐⭐ (Poor for App UI) | ⭐⭐⭐⭐⭐ (Best-in-class) | ⭐⭐⭐ (Good for Games) | **7.5/10** |
| **React Native** | ⭐⭐⭐⭐ (Good) | ⭐ (Poor/Complex) | ⭐⭐⭐⭐ | **6.0/10** |
| **Unity** | ⭐⭐ (Poor for App UI) | ⭐⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐⭐⭐ | **7.0/10** |

### Key Deciding Factors:
1. **App-Heavy Layout Architecture**: Building complex scrollable store catalogs, inventory lists, and evolution history screens in Godot's UI system would require 3-4x more effort. Flutter's widget system natively solves these UI challenges.
2. **Flame Engine Integration**: Flame embeds seamlessly into Flutter, providing a lightweight game loop, sprite animation management, and access to Dart's `FragmentProgram` API for custom GLSL shaders without the overhead of Unity or Godot.
3. **1-Bit Dithering Pipeline**: Flame allows rendering the kaiju scene to an off-screen low-resolution canvas, applying our custom Bayer matrix dither shader, and upscaling to the native UI via nearest-neighbor filtering.
4. **Dart 3 Soundness**: Dart 3 pattern matching and records make building the dormant plugin architecture robust and compile-time safe.

---

## 2. Key Package Ecosystem

The following packages constitute the core stack for the application:

| Package | pub.dev Link | Role in Unix Tamagotchi |
| :--- | :--- | :--- |
| **`flame`** | [pub.dev/packages/flame](https://pub.dev/packages/flame) | **2D Engine Core**: Manages the kaiju viewport, sprite animation loops, particle stippling effects, and the fragment shader pipeline for 1-bit dithering. |
| **`flutter_riverpod`** | [pub.dev/packages/flutter_riverpod](https://pub.dev/packages/flutter_riverpod) | **Reactive State Management**: Compile-safe, testable state management ideal for dynamic plugin registration and offline-first state. |
| **`hive_flutter`** | [pub.dev/packages/hive_flutter](https://pub.dev/packages/hive_flutter) | **Zero-Latency Storage**: Lightning-fast local binary key-value database for offline PoC state. |
| **`supabase_flutter`** | [pub.dev/packages/supabase_flutter](https://pub.dev/packages/supabase_flutter) | **Backend SDK**: Connects to the PostgreSQL database for dynamic plugin manifests, multiplayer syncing, and user data. |
| **`in_app_purchase`** | [pub.dev/packages/in_app_purchase](https://pub.dev/packages/in_app_purchase) | **Monetization**: Native IAP integration for Android and iOS. |
| **`google_fonts`** | [pub.dev/packages/google_fonts](https://pub.dev/packages/google_fonts) | **Typography**: Delivers the `VT323` monospace font essential for the industrial terminal aesthetic. |

---

## 3. Shader Pipeline: `FragmentProgram` API

To achieve the "Tactical 1-Bit Cyber-Specimen OS" look, we leverage Flutter's `FragmentProgram` API inside the Flame viewport. 
- Custom GLSL shaders execute an **ordered Bayer matrix checkerboard** pattern to apply 1-bit shading over continuous color gradients.
- **Nearest-Neighbor Upscaling** ensures the dithered output retains crisp, chunky pixels on high-DPI mobile screens, seamlessly composited behind the native-resolution Flutter UI.

---

## 4. State Management: Flutter Riverpod

**Riverpod** (`flutter_riverpod` 2.5+) is selected over BLoC and Provider for the following architectural reasons:

1. **Global Dependency Injection without `BuildContext`**:
   The `PluginRegistry` and action execution pipeline can access stores and trigger mutations outside the UI widget tree.
2. **Safe Dynamic Provider Discovery**:
   As new action plugins are loaded from the backend, Riverpod providers can dynamically adapt without rebuilding the root widget tree.
3. **Immutability & Code Generation**:
   Combined with `freezed`, kaiju state mutations are completely pure and deterministic.

---

## 5. Backend Evaluation: Supabase vs Alternatives

| Dimension | Supabase (Selected) | Custom Dart Server (Shelf) | Firebase |
| :--- | :--- | :--- | :--- |
| **Flutter SDK Support** | 🏆 Official `supabase_flutter` | Manual HTTP client | Official FlutterFire |
| **Plugin Tables & RLS** | 🏆 PostgreSQL JSONB tables | PostgreSQL via custom ORM | NoSQL Firestore |
| **Social OAuth (Google/Apple/X)** | 🏆 Built-in GoTrue OAuth | Must implement OAuth2 flow | Built-in |
| **Realtime WebSockets** | 🏆 PostgreSQL CDC Realtime | Custom WebSocket server | Firestore snapshots |
| **Self-Hosting** | 🏆 Fully Dockerized | Custom Docker container | ❌ Proprietary Cloud |

**Verdict**: **Supabase** delivers standard PostgreSQL tables with Row-Level Security, ready-to-use Social Auth, and Realtime WebSockets, while allowing managers to edit the `action_plugins` and `scenario_plugins` tables directly via the Supabase Studio dashboard.
