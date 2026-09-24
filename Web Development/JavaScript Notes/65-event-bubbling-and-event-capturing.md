# Episode 65 — Event Bubbling and Event Capturing in JavaScript

---

## 🎯 What You Will Learn

- How the browser executes the 3-phase DOM event lifecycle: Capturing, Target, and Bubbling.
- Why bubbling is the web default and how to opt into the capturing phase using `{ capture: true }`.
- The crucial architectural difference between `event.stopPropagation()` and `event.stopImmediatePropagation()`.
- Why `event.target` differs from `event.currentTarget` during event propagation.
- Which DOM events do NOT bubble (and how to handle them using capturing or alternative events).
- How to implement clean modal backdrops and resilient analytics listeners without breaking the event chain.

---

## 1. The Idea in Simple Words

### Simple Explanation
When you click on a button inside a box on a webpage, you are not just clicking the button — you are also clicking the box it sits in, the section containing that box, the webpage body, and the browser window itself! The browser handles this by taking the event on a two-way journey: first, it travels from the top window *down* to the button you clicked (Capturing), activates the button (Target), and then bubbles back *up* through every parent box to the top (Bubbling). This lets parent boxes listen to and react to things happening inside their children.

### Technical Explanation
The W3C DOM Level 2 Event specification standardizes event dispatch into three sequential phases along a pre-computed propagation path:
1. **Capturing Phase:** Traverses downward from `Window` through the document tree to the direct parent of the target.
2. **Target Phase:** Invokes listeners registered on the target node itself (`event.target`).
3. **Bubbling Phase:** Traverses upward from the target's direct parent through every ancestor node back to `Window`.
Listeners default to executing in the bubbling phase (`capture: false`). Invoking `stopPropagation()` terminates further traversal along the path, while `stopImmediatePropagation()` additionally halts subsequent sibling listeners attached to the active node.

### Before vs After Motivation
- **Before:** Early browsers had irreconcilable models: Netscape only supported capturing down, while Microsoft Internet Explorer only supported bubbling up. Developers wrote brittle browser-sniffing code.
- **After:** The standardized 3-phase model gives developers complete control. You can intercept events early at the top using capturing (for security and telemetry), or handle them naturally at ancestor nodes using bubbling (for event delegation and UI state management).

---

## 2. Mental Model: The Deep-Sea Diving Expedition

Think of the DOM tree as an underwater diving expedition:
- **Event Capturing (Trickling Phase)**: The diver plunges from the water surface (`window`), descending deeper and deeper through atmospheric layers (`document` $\to$ `<html>` $\to$ `<body>` $\to$ container divs) until reaching the sunken treasure chest on the seabed (`e.target`).
- **Target Phase**: The diver touches the treasure chest (`e.target`).
- **Event Bubbling Phase**: Air bubbles released at the seabed immediately begin their ascent, floating straight up through every water layer back to the surface (`window`).
- **`e.stopPropagation()`**: An impenetrable iron net deployed at any depth. Once bubbles hit the net, they cannot rise any further to higher ancestors.
- **`e.stopImmediatePropagation()`**: Not only deploys the iron net upward, but immediately silences any other diver standing right next to you on the same platform.

```
       [ Surface: window ]
           │          ▲
  Capture  │          │  Bubble
  (Down)   │          │  (Up)
           ▼          │
       [ Target Element ]  (Seabed)
```

---

## 3. Basic Syntax / API

```javascript
// Default listener (runs during the BUBBLING phase)
element.addEventListener("click", callback);

// Capturing listener (runs during the CAPTURING phase)
element.addEventListener("click", callback, true); // boolean shorthand
element.addEventListener("click", callback, { capture: true }); // modern options object

// Advanced options configuration
element.addEventListener("click", callback, {
  capture: false, // Bubbling phase (default)
  once: true,     // Unbinds automatically after 1 invocation
  passive: true   // Promises callback will never call preventDefault()
});
```

### Stopping Event Propagation

| Method | Behavior | Affects Other Listeners on Same Node? | Affects Browser Default Action? |
| :--- | :--- | :--- | :--- |
| `event.stopPropagation()` | Halts propagation upward (bubbling) or downward (capturing) to other DOM nodes. | **No** (other listeners on this element still run). | **No** (default action still happens). |
| `event.stopImmediatePropagation()` | Halts propagation to other nodes **AND** stops subsequent sibling listeners on the *same element*. | **Yes** (subsequent sibling listeners are blocked). | **No** (default action still happens). |
| `event.preventDefault()` | Cancels the native browser action (e.g. following links, submitting forms). | **No** (propagation continues unaffected). | **Yes** (cancels default action). |

---

## 4. Smallest Useful Example

```javascript
// Parent and child bubbling demo
const parent = document.querySelector("#parent");
const child = document.querySelector("#child");

parent.addEventListener("click", () => {
  console.log("Parent received the bubbled click!");
});

child.addEventListener("click", () => {
  console.log("Child clicked directly!");
});

// Clicking #child logs:
// 1. "Child clicked directly!"
// 2. "Parent received the bubbled click!"
```

---

## 5. What Just Happened?

```
User clicks on #child element
         │
         ▼
[1] Capturing Phase: Browser traverses Window -> Document -> Body -> #parent.
    (No capture listeners found, so nothing fires yet).
         │
         ▼
[2] Target Phase: Browser arrives at #child.
    - Executes child's click listener -> Logs: "Child clicked directly!".
         │
         ▼
[3] Bubbling Phase: Event begins ascending upward.
    - Reaches #parent -> Executes parent's click listener -> Logs: "Parent received the bubbled click!".
    - Continues bubbling through Body -> Document -> Window.
```

1. **First:** The browser identifies `#child` as the target node via hit testing.
2. **Next:** It builds the propagation path: `[Window, Document, HTML, Body, #parent, #child]`.
3. **Changed:** The engine marches down (capture), triggers target listeners, then marches up (bubble).
4. **State:** Handlers execute sequentially and synchronously on the JavaScript main thread.

---

## 6. Visualize It

### The Complete Event Propagation Lifecycle
```
                 WINDOW
                 │    ▲
    1. Capture   │    │   3. Bubble
    (Trickling)  │    │   (Rising)
                 ▼    │
                DOCUMENT
                 │    ▲
                 ▼    │
                BODY
                 │    ▲
                 ▼    │
             #PARENT DIV
                 │    ▲
                 ▼    │
              #CHILD BUTTON
           [ 2. TARGET PHASE ]
```

### `stopPropagation()` vs `stopImmediatePropagation()`
```
Element: <button id="btn">

Listener A: console.log("A");
Listener B: e.stopPropagation(); console.log("B");
Listener C: console.log("C");
Parent Listener: console.log("Parent");

─── Case 1: with e.stopPropagation() ───
Output: "A" -> "B" -> "C"
(Parent Listener is BLOCKED from bubbling)

─── Case 2: with e.stopImmediatePropagation() on Listener B ───
Output: "A" -> "B"
(Listener C on the same element AND Parent Listener are BOTH BLOCKED)
```

---

## 7. Important Differences

### Comparison: Event Bubbling vs Event Capturing

| Feature / Trait | Event Bubbling | Event Capturing (Trickling) |
| :--- | :--- | :--- |
| **Direction of Flow** | Inside $\to$ Outside (`Target` $\to$ `Window`) | Outside $\to$ Inside (`Window` $\to$ `Target`) |
| **Default in Browsers** | **Yes** (Default mode) | **No** (Opt-in required) |
| **How to Enable** | `addEventListener(type, fn, false)` or omitted | `addEventListener(type, fn, true)` |
| **Options Object** | `{ capture: false }` | `{ capture: true }` |
| **Execution Order** | Deepest child fires first; ancestors fire last | Highest root fires first; child fires last |
| **Standard Use Case** | Event delegation, local UI state management | Global telemetry/analytics, security gates |

### Comparison: `event.target` vs `event.currentTarget`

| Property | Definition | Does It Change During Propagation? |
| :--- | :--- | :--- |
| `event.target` | The innermost element that originally triggered the event. | **No** (remains constant across all handlers). |
| `event.currentTarget` | The element whose listener is currently executing (`=== this`). | **Yes** (points to the element currently processing the event). |

---

## 8. Common Mistakes & Anti-Patterns

### 1. Overusing `e.stopPropagation()` (The Sledgehammer Anti-Pattern)
Developers often place `e.stopPropagation()` on nested buttons to fix an immediate problem (like avoiding a card click).
- **The Consequence:** Global document listeners (such as click-outside dropdown menus, analytics trackers, and heatmapping tools like Hotjar) are completely blinded because the event never reaches `document` or `window`.
- **The Fix:** Inspect `e.target` or use `.closest()` in the parent handler instead of terminating propagation:
```javascript
// ✅ BETTER: Check origin instead of stopping propagation
parentCard.addEventListener("click", (e) => {
  if (e.target.closest(".favorite-btn")) return; // Ignore if heart icon clicked
  openCardDetails();
});
```

### 2. Confusing `preventDefault()` with `stopPropagation()`
Calling `event.preventDefault()` halts default browser actions (such as navigating a link or submitting a form). It **does NOT halt event bubbling**. Bubbling continues unhindered unless you explicitly call `event.stopPropagation()`.

### 3. Assuming Target Phase Respects the `capture` Flag
In modern browsers conforming to the WHATWG DOM specification, when an event reaches the target element (`target` phase), listeners execute in the **exact order they were registered**, regardless of whether their `capture` flag is `true` or `false`!

---

## 9. 🧠 Check Your Understanding

### Q1: In what sequence do the three DOM event phases execute?
> **Answer:** 1. Capturing Phase (descending from `Window` down to the target's parent). 2. Target Phase (executing on the target element itself). 3. Bubbling Phase (ascending from the target's parent back up to `Window`).

### Q2: What is the difference between `event.stopPropagation()` and `event.stopImmediatePropagation()`?
> **Answer:** `stopPropagation()` prevents the event from traveling further up or down the DOM tree to other ancestor or descendant elements. `stopImmediatePropagation()` does that too, AND immediately prevents any remaining listeners attached to the *same* element from executing.

### Q3: Name three DOM events that do NOT bubble.
> **Answer:** `focus`, `blur`, `mouseenter`, `mouseleave`, `load`, `unload`, and element-specific `scroll`.

### Q4: If an element has two click listeners—one registered with `{ capture: true }` and one registered with `{ capture: false }`—which one runs first if that element is the clicked target?
> **Answer:** On the target node itself, listeners execute in the **order they were registered**, regardless of the `capture` option. The `capture` flag only affects execution during descent on ancestor nodes.

---

## 10. ⚠️ Confusion & Edge Cases

### 1. Non-Bubbling Events and Their Workarounds
| Non-Bubbling Event | Bubbling Alternative | Capturing Workaround |
| :--- | :--- | :--- |
| `focus` | `focusin` | `parent.addEventListener("focus", fn, true)` |
| `blur` | `focusout` | `parent.addEventListener("blur", fn, true)` |
| `mouseenter` | `mouseover` | `parent.addEventListener("mouseenter", fn, true)` |
| `mouseleave` | `mouseout` | `parent.addEventListener("mouseleave", fn, true)` |

### 2. `event.composedPath()`
To inspect the complete array of DOM nodes through which an event will travel (or has traveled), inspect `e.composedPath()`:
```javascript
button.addEventListener("click", (e) => {
  console.log(e.composedPath());
  // Returns: [button, div#child, div#parent, body, html, document, Window]
});
```

### 3. Native Backdrop Modal Dismissal Pattern
```javascript
const modalBackdrop = document.querySelector("#modal-backdrop");
const modalCard = document.querySelector("#modal-card");

// Dismiss when clicking the outer grey backdrop
modalBackdrop.addEventListener("click", (e) => {
  // Only close if the user clicked directly on the backdrop, NOT inside the card!
  if (e.target === modalBackdrop) {
    modalBackdrop.classList.remove("open");
  }
});
```
*(Notice: We did NOT need `e.stopPropagation()` on the modal card! Checking `e.target === modalBackdrop` cleanly avoids propagation bugs).*

---

## 11. 🎯 Interview Deep Dive

### Output Tracing: Execution Order with `stopPropagation`
```javascript
const parent = document.querySelector("#parent");
const child = document.querySelector("#child");

parent.addEventListener("click", () => console.log("1"), false);
parent.addEventListener("click", () => console.log("2"), true);
child.addEventListener("click", (e) => {
  console.log("3");
  e.stopPropagation();
}, false);
child.addEventListener("click", () => console.log("4"), false);
parent.addEventListener("click", () => console.log("5"), false);

// User clicks on #child
```

### Predict first:
What gets logged in the console?

<details>
<summary>View Output & Explanation</summary>

```
2
3
4
```

**Explanation:**
1. **Capturing phase:** Checks `parent` $\to$ listener `2` has `capture: true` $\to$ Logs `"2"`.
2. **Target phase:** Arrives at `child`:
   - First listener runs $\to$ Logs `"3"`. It calls `e.stopPropagation()`.
   - Second listener on `child` runs $\to$ Logs `"4"` (because `stopPropagation` does not silence sibling listeners on the exact same element).
3. **Bubbling phase:** The bubbling path to `parent` is terminated by `e.stopPropagation()`. Parent listeners `1` and `5` **never execute**.
</details>

### Debugging Scenario: Global Analytics Tracker Silenced by Feature Code
**Problem:** A checkout button handler contains `e.stopPropagation()`. The marketing analytics team complains that clicks on the checkout button are not showing up in tracking dashboards.
**Solution:** Register the global analytics listener on `window` in the **Capturing Phase**:
```javascript
window.addEventListener("click", (e) => {
  analytics.track("click", { tag: e.target.tagName, id: e.target.id });
}, { capture: true });
```
Because the Capturing Phase executes *before* the event reaches the target element, the analytics tracker runs first. Any subsequent call to `e.stopPropagation()` inside the button's click handler happens too late to block the analytics listener!

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Robust Click-Outside Dropdown Pattern
```javascript
const button = document.querySelector("#menu-toggle");
const menu = document.querySelector("#dropdown-menu");

button.addEventListener("click", () => {
  menu.classList.toggle("open");
});

window.addEventListener("click", (e) => {
  // If click was outside both the menu and the toggle button, close the menu
  if (!menu.contains(e.target) && !button.contains(e.target)) {
    menu.classList.remove("open");
  }
});
```

### 🟡 SHOULD KNOW: Resilient Global Telemetry Plugin
```javascript
function installResilientTelemetry() {
  const eventTypes = ["click", "submit", "keydown"];
  
  eventTypes.forEach((type) => {
    // Register on window in CAPTURE phase so it fires before any app listeners
    window.addEventListener(type, (event) => {
      const payload = {
        type: event.type,
        targetTag: event.target.tagName,
        targetId: event.target.id,
        timestamp: performance.now()
      };
      
      if (navigator.sendBeacon) {
        navigator.sendBeacon("/api/telemetry", JSON.stringify(payload));
      }
    }, { capture: true, passive: true });
  });
}
installResilientTelemetry();
```

### 🔵 DEEP DIVE: The Historical Browser Wars Compromise
During the mid-1990s "Browser Wars", Microsoft Internet Explorer implemented **Event Bubbling** (starting at target and bubbling up), arguing that user intent begins at the specific clicked element. Netscape Navigator 4 implemented **Event Capturing** (starting at top window and trickling down), arguing that top-level containers should have primary authority over input dispatch. The W3C resolved this divide in the DOM Level 2 Event specification by combining both: events capture down first, invoke target listeners, and then bubble back up, letting developers choose which phase to observe.

### ⚫ IMPLEMENTATION DETAIL — Chromium Example: Blink `EventDispatcher`
> ⚙️ **Implementation Detail — Chromium Example**
> In Chromium's Blink rendering engine, when an event is dispatched via `EventDispatcher::DispatchEventAtTarget`, Blink first calls `EventPath::InitializeWith` to walk the DOM parent chain up to `Window`, storing the exact sequence of `Node` pointers in a vector. During the capture phase, it iterates this vector in reverse (index $N-1$ down to 1). At the target (index 0), it invokes target handlers. During the bubble phase, it iterates from index 1 up to $N-1$. If `event.stopPropagation()` is invoked, Blink sets a internal boolean flag `propagation_stopped_ = true` on the `blink::Event` object, causing the iteration loop to immediately `break`.

---

## 13. ⚡ 30-Second Revision

- **Must Remember:** Events follow 3 phases: 1. Capture (down), 2. Target (at node), 3. Bubble (up). Standard listeners run during the bubbling phase.
- **Most Common Confusion:** `stopPropagation()` stops other nodes from receiving the event; `stopImmediatePropagation()` also stops other listeners on the *same* node.
- **One Code Pattern:** Use `{ capture: true }` on `window` for global analytics to guarantee tracking even if child code calls `stopPropagation()`.
- **One Interview Question:** Why do `focus` and `blur` not bubble, and how do you capture them on an ancestor? Use `focusin`/`focusout`, or listen to `focus` in the capturing phase (`capture: true`).

---

## 14. 🛠️ Tiny Practice Task

Open your browser DevTools Console (`F12`), paste the snippet below, and click anywhere on the page:

```javascript
window.addEventListener("click", () => console.log("1. Window [Capture]"), true);
document.body.addEventListener("click", () => console.log("2. Body [Capture]"), true);
document.body.addEventListener("click", () => console.log("3. Body [Bubble]"), false);
window.addEventListener("click", () => console.log("4. Window [Bubble]"), false);
```

**Experiment:**
1. Click anywhere on the webpage — observe the exact alternating order: Capture runs top-to-bottom (`Window` then `Body`), followed by Bubble running bottom-to-top (`Body` then `Window`).
2. Add a button dynamically with `e.stopPropagation()` in its bubble listener — observe how `Window [Bubble]` is suppressed, but both capture listeners still run!
