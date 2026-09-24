# Episode 54 — `getAttribute` and `setAttribute` in JavaScript (Attributes vs. Properties)

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #54  
> **Video ID:** `38mNZls3lUU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=38mNZls3lUU)  
> **Duration:** 27:29  
> **Transcript:** `.transcripts/54_38mNZls3lUU.txt`  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- The critical difference between an **HTML Attribute** and a **JavaScript DOM Property**.
- How to read, write, check, and delete attributes using `getAttribute`, `setAttribute`, `hasAttribute`, and `removeAttribute`.
- Why setting a custom property (`el.role = "admin"`) does NOT update the HTML markup or CSS selectors.
- The dangerous **Boolean Attribute Trap** (`disabled="false"` still disables a button!).
- How the **Dirty Value Flag** causes `input.value` and `input.getAttribute("value")` to split apart.
- How to store clean custom metadata using the HTML5 `data-*` and `dataset` API.

---

## 1. The Idea in Simple Words

### Simple Explanation
When you write an HTML tag like `<input id="search" type="text" value="Coffee">`, there are two separate things happening:
1. **The HTML Attribute:** The raw words written in the HTML text file (`id="search"`, `type="text"`).
2. **The DOM Property:** The live JavaScript object variable living in the computer's memory (`input.id`, `input.type`, `input.value`).

Most of the time, the browser keeps these two in sync. But they are NOT the same thing! Attributes are always strings in the markup. Properties can be real JavaScript booleans, numbers, or objects.

### Technical Explanation
HTML **attributes** are initial configuration parameters stored in the element's markup attribute store (`NamedNodeMap`). DOM **properties** are instance fields on the JavaScript object wrapping the DOM node on the heap. When the browser initializes a DOM node, it reflects standard attributes into DOM properties. The official methods `getAttribute()` and `setAttribute()` interact directly with the underlying markup attribute store rather than the JavaScript object's properties.

### Before → After (Why does this matter?)

#### BEFORE (Thinking ad-hoc JS properties change the HTML):
```javascript
// Adding a custom property to the JS object:
card.status = "active";
console.log(card.getAttribute("status")); // null!
// CSS selector card[status="active"] FAILS to match because HTML was never updated!
```

#### AFTER (Using the official attribute API):
```javascript
// Setting the actual markup attribute:
card.setAttribute("status", "active");
console.log(card.getAttribute("status")); // "active"
// HTML markup now shows <div status="active"> and CSS selector matches instantly!
```

---

## 2. Mental Model

Think of HTML attributes as the **printed blueprint specs** on a wall, and DOM properties as the **live electrical wiring** inside the building:
- When the house is built, the electricians wire the switches based on the printed blueprint.
- Turning a switch on or off changes the **live wiring state** (DOM property).
- Flipping the light switch does *not* erase or rewrite the architect's printed paper blueprint on the wall!
- `getAttribute` reads the printed blueprint; `element.prop` checks the live electrical circuit.

```
┌────────────────────────────────────────────────────────┐
│                   THE TWO DOM LAYERS                   │
├───────────────────────────┬────────────────────────────┤
│ HTML Attribute Layer      │ JavaScript Property Layer  │
│ (The Printed Blueprint)   │ (The Live Wiring)          │
├───────────────────────────┼────────────────────────────┤
│ Stored in HTML markup     │ Stored in JS object memory │
│ Strictly strings          │ Booleans, numbers, strings │
│ getAttribute("value")     │ element.value              │
│ Default / Initial state   │ Current live dynamic state │
└───────────────────────────┴────────────────────────────┘
```

---

## 3. Basic Syntax / API

```javascript
// 1. Read attribute string (returns string or null if missing)
element.getAttribute("attributeName");

// 2. Write attribute (REQUIRES 2 arguments: name and string value)
element.setAttribute("attributeName", "value");

// 3. Check existence (returns true or false)
element.hasAttribute("attributeName");

// 4. Remove completely from markup
element.removeAttribute("attributeName");

// 5. HTML5 Custom Dataset
element.dataset.userId = "101"; // writes data-user-id="101"
```

---

## 4. Smallest Useful Example

```html
<h1 id="title" class="main-heading">Welcome</h1>
```

```javascript
const heading = document.querySelector("#title");

// 1. Read attribute
console.log(heading.getAttribute("class")); // "main-heading"

// 2. Add a tooltip attribute via setAttribute
heading.setAttribute("title", "Hover tooltip");

// 3. Verify markup update
console.log(heading.hasAttribute("title")); // true

// 4. Clean up
heading.removeAttribute("title");
```

---

## 5. What Just Happened?

Let's trace `heading.setAttribute("title", "Hover tooltip");`:
1. **Step 1 (Method Dispatch):** JavaScript calls `Element.prototype.setAttribute` with arguments `"title"` and `"Hover tooltip"`.
2. **Step 2 (Attribute Store Mutation):** The browser adds the key-value pair `title="Hover tooltip"` to the element's internal `NamedNodeMap`.
3. **Step 3 (Property Reflection):** Because `title` is a standardized global HTML attribute, the browser automatically reflects this change to the JavaScript DOM property `heading.title`.
4. **Step 4 (DevTools Update):** The Elements panel in DevTools immediately updates to show `<h1 id="title" class="main-heading" title="Hover tooltip">`.

---

## 6. Visualize It

### Why Custom Properties Do Not Affect Markup
```
heading.procodrr = "anurag";
                    │
                    ▼
     [V8 JavaScript Heap Object]   <── Property exists here!
                    │
                    ✕ (Does NOT cross boundary)
                    ▼
     [Blink C++ ElementData]       <── NamedNodeMap has no record of 'procodrr'!
                    │
                    ▼
       HTML Markup in DevTools:    <h1>Welcome</h1> (Unchanged!)
```

### The Keyword Conflict: `class` vs. `className`
In HTML, the attribute is named `class`. In JavaScript, `class` is a reserved programming keyword.
```
HTML Markup:  <div class="card">
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
getAttribute("class")       element.className
(Attribute API)             (DOM Property)
```

---

## 7. Important Differences

### HTML Attributes vs. DOM Properties

| Feature | HTML Attributes (`getAttribute` / `setAttribute`) | DOM Properties (`element.prop`) |
| :--- | :--- | :--- |
| **Location** | Element's HTML markup string (`NamedNodeMap`) | JavaScript heap object memory |
| **Data Types** | Strictly **strings** | Strings, Booleans, Numbers, Objects |
| **Case Sensitivity**| Case-insensitive in HTML (`"ID"` === `"id"`) | Case-sensitive (`className`, not `classname`) |
| **Custom Data** | Declared in markup; matches CSS `[attr]` | Attached to JS object; invisible to CSS |
| **Naming Quirks** | `class`, `for`, `tabindex` | `className`, `htmlFor`, `tabIndex` |
| **Best Used For** | Initial markup, CSS selectors, custom `data-*` | Live interactive state, event handlers |

---

## 8. Common Mistakes

### 1. Setting Boolean Attributes with String `"false"`
❌ **Wrong:**
```javascript
const submitBtn = document.querySelector("#submit-btn");

// DANGEROUS: You intended to enable the button, but you DISABLED it!
submitBtn.setAttribute("disabled", "false");
```
**Why?**  
In HTML, boolean attributes (like `disabled`, `readonly`, `checked`) are evaluated based on **presence**, not value. As long as the attribute exists in the tag (`<button disabled="false">`), the browser treats it as **active/true**!

✅ **Correct:**
```javascript
// Option 1: Remove the attribute entirely
submitBtn.removeAttribute("disabled");

// Option 2: Use the boolean DOM property directly (Cleaner!)
submitBtn.disabled = false;
```

---

### 2. Omitting the Second Argument in `setAttribute`
❌ **Wrong:**
```javascript
// TypeError: Failed to execute 'setAttribute' on 'Element': 2 arguments required
element.setAttribute("hidden");
```
**Why?**  
`setAttribute` strictly requires two arguments: the name and the value.

✅ **Correct:**
```javascript
// Pass an empty string for boolean flags:
element.setAttribute("hidden", "");
```

---

### 3. Inventing Custom Attributes without `data-`
❌ **Wrong:**
```html
<div user_id="42" role="admin"></div>
```
**Why?**  
Custom attributes without the `data-` prefix violate HTML5 validation and risk colliding with future standard HTML attributes.

✅ **Correct:**
```html
<div data-user-id="42" data-role="admin"></div>
```
```javascript
const el = document.querySelector("div");
console.log(el.dataset.userId); // "42" (automatic camelCase conversion!)
```

---

## 9. 🧠 Check Your Understanding

1. **Why does `heading.getAttribute("class")` work, but `heading.class` return `undefined` or syntax error?**  
   *Answer:* `class` is a reserved keyword in JavaScript. Standard DOM properties map it to `heading.className`. In `getAttribute("class")`, `"class"` is a quoted string literal, bypassing keyword restrictions.
2. **What does `input.getAttribute("value")` return after a user types new text into a form input?**  
   *Answer:* It returns the original **default/initial value** from the HTML markup, NOT what the user just typed.
3. **What is the return type of `element.getAttribute("tabindex")` vs. `element.tabIndex`?**  
   *Answer:* `getAttribute` returns a string (e.g. `"0"`), while the DOM property `tabIndex` returns a real JavaScript number (`0`).
4. **How does `data-user-role="manager"` get accessed via the `dataset` API?**  
   *Answer:* As `element.dataset.userRole` (hyphenated names automatically convert to camelCase).

---

## 10. ⚠️ Confusion & Edge Cases

### 1. The "Dirty Value Flag" on Form Inputs
Watch this classic beginner confusion:
```html
<input id="search" type="text" value="Apple">
```
```javascript
const input = document.getElementById("search");

// User types "Banana" on screen...
console.log(input.value);                 // "Banana" (Live current value)
console.log(input.getAttribute("value")); // "Apple"  (Default attribute!)
```
- The moment the user modifies an `<input>`, the browser sets an internal **dirty value flag** to `true`.
- Once dirty, the live `.value` property is completely disconnected from the default `value` attribute.
- If you call `form.reset()`, the input reverts back to `"Apple"`.

### 2. Relative vs. Absolute URL Resolution (`href` & `src`)
```javascript
const link = document.createElement("a");
link.setAttribute("href", "/about");

console.log(link.getAttribute("href")); // "/about" (exact string from markup)
console.log(link.href);                 // "https://example.com/about" (canonical URL!)
```
- `getAttribute("href")` returns the exact text written in HTML.
- `link.href` resolves the relative path against the current document's domain.

---

## 11. 🎯 Interview Deep Dive

### Q1: Conceptual: Explain why attributes and properties desynchronize in HTML forms.
**Answer**:
Form inputs require two independent concepts of state:
1. **Default State (Attribute):** Declared in the markup via the `value` attribute. It defines what the input holds on initial page load and what it reverts to when a user clicks a "Reset Form" button.
2. **Current State (Property):** Controlled by `input.value`. When a user types into the box, only the current state updates. Mutating the live user state must not destroy the original default value needed for form reset cycles.

### Q2: Output Prediction:
```javascript
// ### Predict first: What does each line log?
const div = document.createElement("div");
div.setAttribute("custom", "100");
div.custom = 200;

console.log(div.getAttribute("custom"));
console.log(div.custom);
```

**Answer:**
```text
"100"
200
```

**Why?**
- `div.setAttribute("custom", "100")` stores `"100"` in the DOM element's markup attribute store (`NamedNodeMap`).
- `div.custom = 200` attaches an arbitrary property to the JavaScript object on the heap.
- Because `custom` is not a standard HTML attribute, no reflection occurs. They remain two separate, isolated values.

### Q3: Debugging Scenario:
A button is styled with this CSS:
```css
button[enabled] { background-color: #22c55e; }
```
A developer toggles the button using this function:
```javascript
function toggle(btn) {
  if (btn.getAttribute("enabled") === "true") {
    btn.setAttribute("enabled", "false");
  } else {
    btn.setAttribute("enabled", "true");
  }
}
```
**Symptom:** Once toggled, the button stays green forever, even when `enabled="false"`. Why?  
**Answer:**  
- **Cause:** CSS `button[enabled]` is an **attribute presence selector**. It matches as long as the `enabled` attribute exists on the tag, regardless of whether its value is `"true"` or `"false"`.
- **Fix:** Toggle attribute presence using `hasAttribute`, `setAttribute`, and `removeAttribute`:
```javascript
function toggle(btn) {
  if (btn.hasAttribute("enabled")) {
    btn.removeAttribute("enabled");
  } else {
    btn.setAttribute("enabled", "");
  }
}
```

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: HTML5 Custom Data Attributes (`dataset`)
Any attribute starting with `data-` is automatically collected into the element's `dataset` object:
- `data-user-id="101"` $\to$ `el.dataset.userId`
- `data-auth-token="xyz"` $\to$ `el.dataset.authToken`
- Assigning `el.dataset.status = "done"` automatically writes `data-status="done"` back into the HTML markup!

### ⚫ IMPLEMENTATION DETAIL — Chromium Example
> ⚙️ **Implementation Detail — Chromium Example**  
> In Chromium, JavaScript interacts with DOM nodes through V8 wrapper objects. Calling `el.setAttribute()` transitions through V8 bindings into Blink's C++ `Element::setAttribute()` method, which mutates the underlying `ElementData` vector. Conversely, setting an arbitrary property like `el.myProp = 123` simply sets a field on the V8 JavaScript object wrapper without notifying Blink or changing the C++ DOM node.

---

## 13. ⚡ 30-Second Revision

### Must Remember
- **Attributes** live in HTML markup (strings only); **Properties** live in JavaScript memory (any type).
- `getAttribute()` / `setAttribute()` read and write the markup layer.
- `setAttribute()` requires **2 arguments**: name and string value.
- Boolean attributes are enabled by **presence**: `<button disabled="false">` is still disabled! Use `removeAttribute()` or `.disabled = false`.
- For form inputs, `input.value` is the live user text; `getAttribute("value")` is the initial default.
- Custom metadata should always use `data-*` and `element.dataset`.

### Most Common Confusion
- **`class` vs `className`:** HTML markup uses `class`; JavaScript dot-property uses `className`; `getAttribute("class")` takes `"class"`.

### One Code Pattern
```javascript
// Reading and writing custom metadata correctly:
const card = document.querySelector(".card");
card.dataset.state = "expanded"; // Sets data-state="expanded" in HTML
console.log(card.dataset.state); // "expanded"
```

### One Interview Question
> **Question:** Why does setting `input.setAttribute("value", "ABC")` fail to change what is visible on screen if the user has already typed in the input?  
> **Answer:** User interaction sets the input's internal "dirty value flag", permanently decoupling the live `.value` property from the default `value` attribute until the form is reset.

---

## 14. 🛠️ Tiny Practice Task

Open your browser DevTools Console (F12) on any webpage:
1. Create a dynamic button:
   ```javascript
   const btn = document.createElement("button");
   btn.textContent = "Click Me";
   ```
2. Set custom metadata using `dataset`:
   ```javascript
   btn.dataset.actionId = "submit_form";
   btn.dataset.clickCount = "0";
   console.log(btn.outerHTML); // Notice data-action-id and data-click-count!
   ```
3. Test boolean attribute behavior:
   ```javascript
   btn.setAttribute("disabled", "false");
   console.log("Is button disabled?", btn.disabled); // Prints true!
   btn.removeAttribute("disabled");
   console.log("Is button disabled now?", btn.disabled); // Prints false!
   ```
