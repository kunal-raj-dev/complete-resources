# Episode 63 — Keyboard Events in JavaScript

---

## 🎯 What You Will Learn

- How `keydown` and `keyup` capture user keyboard interactions across the DOM.
- Why the legacy `keypress` event is deprecated and should never be used in modern code.
- The fundamental distinction between physical key slots (`e.code`) and semantic characters (`e.key`).
- Why non-interactive HTML elements cannot listen to keyboard events without `tabindex`.
- How to implement robust keyboard shortcuts, modal dismissals, and game loops without layout bugs.
- How to safely handle modifier keys, IME text composition, and Caps Lock detection.

---

## 1. The Idea in Simple Words

### Simple Explanation
When you use a computer, every key on your keyboard is a physical button wired to an electrical sensor. When your finger presses a key down, an event fires. If you keep holding it down, the computer repeats the letter. When you finally lift your finger off, a different event fires. JavaScript lets your webpage listen to these button presses so you can make shortcut keys (like `Ctrl+K`), close popups with `Escape`, or move video game characters.

### Technical Explanation
Keyboard events in the Web platform inherit from `UIEvent` and the root `Event` interface via the `KeyboardEvent` class. When a user interacts with a physical key, the operating system kernel sends scan codes to the browser host window. The browser's input pipeline converts these platform messages into DOM events (`keydown`, `keyup`) targeted at `document.activeElement`. Modern specifications (DOM Level 3 Events) deprecate legacy numeric ASCII codes (`keyCode`, `which`) in favor of standardized string attributes: `event.key` for localized semantic characters and `event.code` for hardware-relative physical positions.

### Before vs After Motivation
- **Before:** Webpages only responded to mouse clicks. Power users had to click tiny buttons on screen, accessibility tools could not navigate interactive widgets, and hotkeys like `Cmd+K` or `Escape` were impossible.
- **After:** Webpages can respond to every keystroke, capture multi-key shortcuts, build accessible keyboard navigation (WAI-ARIA), control game loops via hardware coordinates, and detect modifier keys across international layouts.

---

## 2. Mental Model: The Mechanical Typewriter

Think of the computer keyboard as a physical mechanical typewriter wired to a digital sensor:
- **`keydown`** is the instant your finger depresses the mechanical key switch. If you hold it down, the typewriter hammer repeatedly strikes the paper in rapid succession (represented by `e.repeat === true`).
- **`keyup`** is the moment your finger lifts off the key switch, breaking physical contact. It fires exactly once per press-and-release cycle.
- **`keypress`** is the old ink-ribbon strike that recorded only printable symbols. If you pressed `Shift` alone, no ink touched the paper, so no `keypress` occurred. Because of historical inconsistencies and mobile soft keyboards, this legacy ribbon has been retired (deprecated).
- **`e.code` vs `e.key`**:
  - `e.code` identifies the **physical plastic keycap location** on the hardware grid (e.g., `KeyA`, `Digit1`, `ShiftLeft`). Even if you switch your OS language to Hindi, Arabic, or French, or turn Caps Lock on, the physical slot on your desk never moves.
  - `e.key` represents the **semantic character printed on screen** after all OS localization and modifier mappings are applied (e.g., `"a"`, `"A"`, `"Enter"`).

```
         [ Physical Keycap on Keyboard Grid ]  ───>  e.code ("KeyW")
                         │
                         ▼ (OS Language / Caps Lock / Shift Mapping)
             [ Rendered Text Character ]       ───>  e.key  ("w" or "W")
```

---

## 3. Basic Syntax / API

```javascript
// Listening to keyboard events on the global window
window.addEventListener("keydown", (event) => {
  console.log(event.key);  // Semantic character: "Enter", "a", "ArrowUp"
  console.log(event.code); // Physical key identifier: "KeyA", "Space"
});

window.addEventListener("keyup", (event) => {
  console.log("Key released:", event.key);
});
```

### Core `KeyboardEvent` Properties

| Property | Type | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `key` | `string` | The semantic printed character, factoring in Shift, Caps Lock, and OS layout. | `"a"`, `"A"`, `"Enter"`, `"ArrowUp"`, `" "` (Space) |
| `code` | `string` | The physical key location on the keyboard, independent of language layout. | `"KeyA"`, `"Digit1"`, `"Enter"`, `"ArrowUp"`, `"Space"` |
| `repeat` | `boolean` | `true` if the event is firing repeatedly because the key is held down. | `true` / `false` |
| `ctrlKey` | `boolean` | `true` if the `Control` key was pressed. | `true` / `false` |
| `shiftKey`| `boolean` | `true` if the `Shift` key was pressed. | `true` / `false` |
| `altKey`  | `boolean` | `true` if the `Alt` (Option on macOS) key was pressed. | `true` / `false` |
| `metaKey` | `boolean` | `true` if the `Meta` key (`Cmd` on macOS, `Windows` key on Windows) was pressed. | `true` / `false` |
| `isComposing` | `boolean` | `true` if the event is part of an IME composition session (e.g. CJK input). | `true` / `false` |
| `keyCode` | `number` | **[DEPRECATED]** Legacy numeric ASCII/virtual key code. Do not use! | `65`, `13`, `27` |
| `which` | `number` | **[DEPRECATED]** Legacy duplicate of `keyCode`. Do not use! | `65`, `13` |

---

## 4. Smallest Useful Example

```javascript
// Close a modal dialog when the user presses the Escape key
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    console.log("Escape pressed! Closing modal dialog...");
  }
});
```

---

## 5. What Just Happened?

```
User presses 'Escape' key
         │
         ▼
[1] OS keyboard driver registers key switch closure and delivers platform event to browser.
         │
         ▼
[2] Browser determines currently focused element (or defaults to <body> / window).
         │
         ▼
[3] Browser constructs a KeyboardEvent object:
      - event.key = "Escape"
      - event.code = "Escape"
      - event.repeat = false
         │
         ▼
[4] Window listener checks `event.key === "Escape"` -> Evaluates to true.
         │
         ▼
[5] Console logs message and modal closes cleanly.
```

1. **First:** The user presses the physical Escape key switch on their keyboard.
2. **Next:** The operating system dispatches the raw hardware interrupt through the browser host window to the DOM event dispatcher.
3. **Changed:** A `KeyboardEvent` object is constructed with `key: "Escape"` and sent down the capture and bubble tree.
4. **State:** The callback executes immediately on the main thread, allowing the application to close the modal before rendering the next frame.

---

## 6. Visualize It

### Keystroke Lifecycle & Auto-Repeat
```
                   [User Depresses Key Down]
                               │
                               ▼
                        ┌─────────────┐
                        │   keydown   │ <─── (e.repeat = false)
                        └──────┬──────┘
                               │ (Key held down past OS delay, ~500ms)
                               ▼
                        ┌─────────────┐
                        │   keydown   │ <─── (e.repeat = true, repeats every ~30-50ms)
                        │   keydown   │
                        │   keydown   │
                        └──────┬──────┘
                               │
                    [User Lifts Finger Off Key]
                               │
                               ▼
                        ┌─────────────┐
                        │    keyup    │ <─── (e.repeat = false, fires exactly ONCE)
                        └─────────────┘
```

### Physical Location (`e.code`) vs Semantic Character (`e.key`)
```
Physical Key Pressed: [ G ] on US QWERTY Keyboard
────────────────────────────────────────────────────────────────────────
State                  e.code                 e.key
────────────────────────────────────────────────────────────────────────
Normal                 "KeyG"                 "g"
Shift Held             "KeyG"                 "G"
Caps Lock ON           "KeyG"                 "G"
Caps Lock + Shift      "KeyG"                 "g"
French AZERTY Mode     "KeyG"                 "g"
Hindi Phonetic Mode    "KeyG"                 "ग"
Greek Layout           "KeyG"                 "γ"
────────────────────────────────────────────────────────────────────────
Physical Key Pressed: Left Shift
Normal                 "ShiftLeft"            "Shift"
Physical Key Pressed: Right Shift
Normal                 "ShiftRight"           "Shift"
```

---

## 7. Important Differences

### Comparison: `keydown` vs `keyup` vs `keypress` (Deprecated) vs `input`

| Feature / Trait | `keydown` | `keyup` | `keypress` (Deprecated) | `input` Event |
| :--- | :--- | :--- | :--- | :--- |
| **When it fires** | Instant key is depressed | Instant key is released | While key was pressed (printable only) | Value changed in form input |
| **Repeats on hold?** | Yes (`e.repeat = true`) | No (fires once on release) | Yes | Yes (as value updates) |
| **Fires for non-char keys?** | Yes (`Shift`, `F5`, `Escape`, etc.) | Yes (`Shift`, `F5`, etc.) | **No** (Modifiers ignored) | **No** (Value must change) |
| **Can cancel default?** | Yes (`e.preventDefault()`) | No (action already committed) | Yes | Too late (already updated) |
| **Target Element** | Focused element or Window | Focused element or Window | Focused element or Window | Form controls only |
| **Captures copy/paste?** | Only shortcut keys (`Ctrl+V`) | Only shortcut keys (`Ctrl+V`) | No | **Yes** (Context menu, drag-drop) |
| **Specification Status** | Standard (DOM Level 3) | Standard (DOM Level 3) | **Obsolete / Deprecated** | Standard (HTML5) |

### Comparison: `e.key` vs `e.code`

| Feature | `e.key` | `e.code` |
| :--- | :--- | :--- |
| **Primary Meaning** | Semantic character / intention | Physical hardware position |
| **Affected by Layout?** | Yes (changes between QWERTY, AZERTY, Hindi) | No (always refers to the physical key slot) |
| **Affected by Shift/Caps?** | Yes (`"g"` becomes `"G"`) | No (always `"KeyG"`) |
| **Best Used For** | Hotkeys (`Ctrl+S`, `Escape`), text processing | Game controls (`WASD`), hardware key simulators |

---

## 8. Common Mistakes & Anti-Patterns

### 1. Using Deprecated `keyCode` or `which`
```javascript
// ❌ WRONG: Deprecated, inconsistent across platforms and mobile
window.addEventListener("keydown", (e) => {
  if (e.keyCode === 13) {
    submit();
  }
});

// ✅ CORRECT: Modern, standardized string property
window.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    submit();
  }
});
```

### 2. Confusing Spacebar `e.key` with Empty String or `"Space"`
When the Spacebar is pressed, `e.key` is a single space string `" "`, NOT an empty string `""` and NOT `"Space"`:
```javascript
// ❌ WRONG: e.key is never "Space" or ""
if (e.key === "Space" || e.key === "") {
  // Never matches!
}

// ✅ CORRECT: e.key is a single space, or use e.code for the physical key
if (e.key === " " || e.code === "Space") {
  // Successfully detects Spacebar!
}
```

### 3. Expecting Generic Elements to Fire Keyboard Events Without Focus
```html
<div id="card">Click to select</div>
```
```javascript
// ❌ FAILS: The div cannot receive keyboard focus, so this listener NEVER fires!
const card = document.querySelector("#card");
card.addEventListener("keydown", (e) => console.log(e.key));

// ✅ FIX: Add tabindex to make the div focusable
card.setAttribute("tabindex", "0");
```

### 4. Relying on Keyboard Events to Validate Form Input
Users can paste text with a mouse right-click, use voice dictation, or use mobile predictive text. If you only listen to `keydown`, those changes are completely missed.
- Use `keydown` for hotkeys and shortcut handling.
- Use the `input` event on `<input>` / `<textarea>` for text value synchronization.

---

## 9. 🧠 Check Your Understanding

### Q1: What is the exact difference between `e.key` and `e.code`?
> **Answer:** `e.code` identifies the physical key location on the keyboard hardware grid (e.g. `"KeyA"`), regardless of OS language layout or modifier keys. `e.key` represents the resulting semantic character (e.g. `"a"`, `"A"`, `"अ"`), taking into account Shift, Caps Lock, and keyboard language layouts.

### Q2: Why will a `keydown` listener on a `<div id="box">` never fire by default?
> **Answer:** Keyboard events are dispatched only to the currently focused element (`document.activeElement`). Generic elements like `<div>`, `<span>`, and `<p>` are not focusable by default. To make them receive keyboard events, you must set `tabindex="0"` (or `tabindex="-1"`).

### Q3: If a user holds down a key for 3 seconds, how many `keydown` and `keyup` events fire?
> **Answer:** Multiple `keydown` events fire (the first with `e.repeat === false`, followed by repetitive `keydown` events with `e.repeat === true` at the OS auto-repeat frequency). Exactly **one** `keyup` event fires when the user releases the key.

### Q4: Why does calling `e.preventDefault()` inside `keyup` fail to prevent a character from appearing in an input field?
> **Answer:** The default action of typing a character into an input field occurs during the `keydown` processing phase. By the time `keyup` fires, the character has already been inserted into the input's value buffer. `preventDefault()` on `keyup` is executed too late.

---

## 10. ⚠️ Confusion & Edge Cases

### 1. Mobile Virtual Keyboards (`keyCode === 229`)
On mobile devices (iOS, Android), soft keyboards route keystrokes through an Input Method Editor (IME) engine for autocorrect and word suggestions. Frequently, mobile browsers fire `keydown` events where `e.key === "Unidentified"` and `e.keyCode === 229`. **Never rely on keyboard events for input validation on mobile devices.** Always listen to the `input` event and inspect `event.inputType`.

### 2. Caps Lock Inversion with Shift
If Caps Lock is active and the user presses `Shift + A`, the browser computes `e.key = "a"` (lowercase). However, `e.code` remains `"KeyA"`.

### 3. Detecting Caps Lock Without Pressing It
To check if Caps Lock is currently active during any keyboard or mouse event, use the `event.getModifierState()` API:
```javascript
input.addEventListener("keydown", (e) => {
  if (e.getModifierState("CapsLock")) {
    capsWarning.textContent = "Warning: Caps Lock is ON!";
  } else {
    capsWarning.textContent = "";
  }
});
```

### 4. IME Composition Sessions (`e.isComposing`)
When typing in languages that require multi-keystroke composition (Chinese, Japanese, Korean):
```javascript
window.addEventListener("keydown", (e) => {
  // If user presses Enter to confirm IME glyph candidate, do NOT submit the form!
  if (e.key === "Enter" && !e.isComposing) {
    submitForm();
  }
});
```

---

## 11. 🎯 Interview Deep Dive

### Conceptual: `tabindex` Values & DOM Keyboard Accessibility
- **`tabindex="0"`**: Inserts the element into the sequential tab navigation order based on DOM tree position. Enables mouse focus, Tab key focus, and direct keyboard event listeners.
- **`tabindex="-1"`**: Makes the element programmatically focusable via JavaScript (`element.focus()`), but excludes it from sequential Tab navigation. Essential for custom modals, dialogs, and error summary banners.
- **`tabindex="> 0"` (Positive values)**: Forces an explicit tab order that overrides natural DOM order. This is an accessibility anti-pattern because it disrupts screen reader expectations.

### Output Tracing: Event Propagation with `Shift + A`
```javascript
window.addEventListener("keydown", (e) => {
  console.log("Window KeyDown:", e.key);
});

const input = document.createElement("input");
document.body.appendChild(input);
input.focus();

input.addEventListener("keydown", (e) => {
  console.log("Input KeyDown:", e.key);
  e.stopPropagation();
});

// User types capital 'A' by holding Shift and pressing 'a'
```

### Predict first:
What gets logged in the console?

<details>
<summary>View Output & Explanation</summary>

```
Input KeyDown: Shift
Input KeyDown: A
```

**Explanation:**
1. To produce capital `A`, the user first depresses `Shift`. The `input` (being focused) receives a `keydown` event for `"Shift"`. Its listener logs `"Input KeyDown: Shift"` and immediately calls `e.stopPropagation()`, stopping the event before it bubbles to `window`.
2. While holding `Shift`, the user presses `a`. The input receives a second `keydown` event with `e.key === "A"`. Its listener logs `"Input KeyDown: A"` and calls `e.stopPropagation()`.
3. The window's bubble listener never fires for either keypress.
</details>

### Debugging Scenario: Native `<button>` vs `<div onclick="...">`
**Problem:** A developer built a custom clickable card using `<div onclick="openItem()">`. Mouse users can click it, but keyboard-only users cannot select it.
**Solution:**
A native `<button>` element has three built-in accessibility superpowers:
1. It is natively focusable via Tab without needing `tabindex`.
2. It automatically fires a synthetic `click` event when the user presses `Enter` or `Space` while focused.
3. Screen readers announce it with the `button` role automatically.

If a `<div>` must be used, you must manually provide:
```html
<div role="button" tabindex="0" id="card">Open Item</div>
```
```javascript
const card = document.querySelector("#card");
function activate() { console.log("Activated!"); }

card.addEventListener("click", activate);
card.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault(); // Prevent Space from scrolling the page
    activate();
  }
});
```

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Robust Game Loop Controller with `Set`
When users hold multiple keys (e.g., `W + D` to move diagonally), relying on OS repeat events creates stuttering because of the initial OS delay. Instead, track active key states in a `Set`:

```javascript
const pressedKeys = new Set();

window.addEventListener("keydown", (e) => {
  pressedKeys.add(e.code); // Store physical key code
});

window.addEventListener("keyup", (e) => {
  pressedKeys.delete(e.code);
});

function gameLoop() {
  if (pressedKeys.has("KeyW") || pressedKeys.has("ArrowUp")) player.y -= 5;
  if (pressedKeys.has("KeyS") || pressedKeys.has("ArrowDown")) player.y += 5;
  if (pressedKeys.has("KeyA") || pressedKeys.has("ArrowLeft")) player.x -= 5;
  if (pressedKeys.has("KeyD") || pressedKeys.has("ArrowRight")) player.x += 5;
  
  requestAnimationFrame(gameLoop);
}
requestAnimationFrame(gameLoop);
```

### 🟡 SHOULD KNOW: Global Shortcut Manager Pattern
```javascript
class ShortcutManager {
  constructor() {
    this.shortcuts = new Map();
    window.addEventListener("keydown", this.handleKeyDown.bind(this));
  }

  register(combination, callback) {
    this.shortcuts.set(combination.toLowerCase(), callback);
  }

  handleKeyDown(e) {
    // Avoid triggering shortcuts while typing inside text fields
    const tag = e.target.tagName;
    const isInput = e.target.isContentEditable || tag === "INPUT" || tag === "TEXTAREA";
    
    const parts = [];
    if (e.ctrlKey) parts.push("ctrl");
    if (e.metaKey) parts.push("meta");
    if (e.shiftKey) parts.push("shift");
    if (e.altKey) parts.push("alt");
    
    const key = e.key.toLowerCase();
    if (!["control", "meta", "shift", "alt"].includes(key)) {
      parts.push(key);
    }

    const combination = parts.join("+");
    if (this.shortcuts.has(combination)) {
      if (isInput && combination !== "escape") return;
      e.preventDefault();
      this.shortcuts.get(combination)(e);
    }
  }
}
```

### 🔵 DEEP DIVE: SPA Memory Leak Prevention
When attaching global keyboard listeners in React or Vue components, always unbind the exact function reference on unmount:
```javascript
useEffect(() => {
  const handleKeyDown = (e) => {
    if (e.key === "Escape") onClose();
  };

  window.addEventListener("keydown", handleKeyDown);
  return () => {
    window.removeEventListener("keydown", handleKeyDown); // Cleanup
  };
}, [onClose]);
```

### ⚫ IMPLEMENTATION DETAIL — Chromium Example: Keystroke Dispatch Pipeline
> ⚙️ **Implementation Detail — Chromium Example**
> In Chromium, raw hardware interrupts are captured by the browser process's `RenderWidgetHostView` from the OS windowing subsystem. The OS scan code is converted into a `blink::WebKeyboardEvent`. The browser process ships this event via IPC (`mojom::WidgetInputHandler`) to the renderer process. Inside the renderer, Blink's `KeyboardEventManager` determines `document.activeElement` and builds a C++ `blink::KeyboardEvent`. It then invokes the DOM event dispatch pipeline across capture, target, and bubble phases.

---

## 13. ⚡ 30-Second Revision

- **Must Remember:** `e.code` is the hardware plastic key slot (`"KeyW"`, `"Space"`). `e.key` is the character printed on screen (`"w"`, `"W"`, `" "`).
- **Most Common Confusion:** Pressing the Spacebar produces `e.key === " "` (single space string), never `"Space"` or `""`.
- **One Code Pattern:** Use a `Set` with `keydown`/`keyup` tracking `e.code` for smooth, stutter-free diagonal game movement.
- **One Interview Question:** Why don't `<div>` elements respond to `keydown`? Because they are not focusable by default; they require `tabindex="0"`.

---

## 14. 🛠️ Tiny Practice Task

Open your browser DevTools Console (`F12`), paste the snippet below, and try pressing various keys (such as `Space`, `Escape`, `Shift`, `Caps Lock`, and letter keys):

```javascript
window.addEventListener("keydown", (e) => {
  console.log({
    key: e.key,
    code: e.code,
    repeat: e.repeat,
    capsLock: e.getModifierState("CapsLock")
  });
});
```

**Experiment:**
1. Press `Space` — observe what `key` vs `code` logs.
2. Hold down the `A` key — watch when `repeat` turns from `false` to `true`.
3. Turn on Caps Lock and press `Shift + A` — observe how `code` remains `"KeyA"` while `key` prints lowercase `"a"`.
