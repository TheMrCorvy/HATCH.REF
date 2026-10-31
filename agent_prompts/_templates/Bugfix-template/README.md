# `agent_prompts/Bugfix-<feature-name>/` — Bugfix Entrypoint Guide (Template)

> **How to use this template**: Copy this folder to `agent_prompts/Bugfix-<feature-name>/` whenever a bug, regression, or specification mismatch needs to be fixed by an AI agent.  
> **Single Source of Truth Rule**: Every bugfix or behavior change **MUST** update the corresponding specification file(s) in [`../../Documentation/`](../../Documentation/README.md) so the documentation and codebase never drift apart.

---

## 1. General Explanation of the Issue / Change

- **Feature / Subsystem Affected**: `<e.g., DitheredViewport / KaijuStateNotifier / Pair-Bond NFC>`
- **Symptom / Root Cause**: `<Describe what is currently broken or diverging from the plan>`
- **Expected Outcome**: `<Describe the target behavior after the fix>`

---

## 2. Governing `Documentation/` Specs to Verify & Update

- [`Documentation/<Domain>/<file>.md`](../../Documentation/README.md) — `<Explain what section governs this behavior and whether it needs updating>`

---

## 3. Chained Execution Order

Agent: Follow the technical files below in strict sequential order. Do not skip steps.

1. **[`01-technical-fix.md`](01-technical-fix.md)** → Start at **[Step 1: Apply Code Fix](01-technical-fix.md#step-1-apply-code-fix)**

---

> **ENTRYPOINT FOR AGENT**: Proceed immediately to **[`01-technical-fix.md` — Step 1: Apply Code Fix](01-technical-fix.md#step-1-apply-code-fix)**.
