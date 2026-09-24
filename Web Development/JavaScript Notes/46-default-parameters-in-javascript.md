# Episode 46 — Default Parameters in JavaScript (ES6)

> **One-Line Mental Model:** A default parameter is an automatic backup generator: it sits dormant if real power is supplied, but kicks in automatically the moment the input is missing or strictly `undefined`.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #46  
> **Video ID:** `r7I1ViZR08o`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=r7I1ViZR08o)  
> **Duration:** 10:50  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- The modern ES6 syntax for declaring **Default Parameters**.
- Exactly what condition triggers the default: **Strictly `undefined`** (and why `null`, `0`, and `""` do NOT trigger it).
- Why the legacy `param = param || "default"` pattern causes severe falsy bugs.
- **Call-Time Evaluation:** Why default values evaluate fresh on every invocation.
- Using previous parameters to compute subsequent default parameters.
- Parameter **Temporal Dead Zone (TDZ)** rules.
- Using functions and expressions as dynamic default values.

---

## 1. The Idea in Simple Words

### Simple Explanation
In [Episode 28](./28-introduction-to-functions.md), you learned that if you don't pass an argument to a function parameter, JavaScript sets that parameter to `undefined`.

In older JavaScript, if you wanted a parameter to have a fallback value (like a default discount of $10\%$, or a default username of `"Guest"`), you had to write boilerplate code inside the function body:
```javascript
function greet(name) {
  name = name || "Guest"; // Legacy approach
  console.log("Hello, " + name);
}
```

ES6 introduced **Default Parameters**, allowing you to write the fallback value right inside the function signature:
```javascript
function greet(name = "Guest") {
  console.log(`Hello, ${name}`);
}
```

If someone passes a name (`greet("Alice")`), it uses `"Alice"`. If someone passes nothing (`greet()`), it automatically falls back to `"Guest"`!

### Technical Explanation
In ECMAScript 2015+, formal parameters can specify an **Initializer** (`FormalParameter : BindingElement`). 

When a function execution context initializes parameter bindings, it inspects each argument. If the corresponding argument is omitted or is explicitly the primitive **`undefined`**, the engine evaluates the initializer expression and binds its result to the parameter. If any other value is passed—including falsy values like `null`, `0`, `false`, `NaN`, or `""`—the default initializer is **not** evaluated, and the passed value is preserved.

---

## 2. 🧠 Mental Model: The Backup Battery

```
 [ Power Grid (Argument) ] ────> Is power ON?
                                        │
                         ┌──────────────┴──────────────┐
                   YES (Valid Value)              NO (undefined)
                         │                             │
                         ▼                             ▼
             [ Use Customer Value ]        [ Kick ON Backup Generator ]
             "Alice", 0, null, false               (Default Value)
```

---

## 3. Core Concept: Syntax & Behavior

```javascript
function calculateBill(price, taxRate = 0.05, tip = 10) {
  return price + (price * taxRate) + tip;
}

// 1. Using all defaults:
console.log(calculateBill(100)); // 100 + 5 + 10 = 115

// 2. Overriding some defaults:
console.log(calculateBill(100, 0.10)); // 100 + 10 + 10 = 120

// 3. Overriding all defaults:
console.log(calculateBill(100, 0.10, 20)); // 100 + 10 + 20 = 130
```

---

## 4. The Critical Rule: ONLY `undefined` Triggers Defaults

This is one of the most critical boundary cases in JavaScript:

```javascript
function testDefault(val = "Default Value") {
  console.log(val);
}

testDefault();          // "Default Value" (Omitted -> undefined)
testDefault(undefined);  // "Default Value" (Explicitly undefined)

testDefault(null);      // null  <── DOES NOT TRIGGER DEFAULT!
testDefault(0);         // 0     <── DOES NOT TRIGGER DEFAULT!
testDefault("");        // ""    <── DOES NOT TRIGGER DEFAULT!
testDefault(false);     // false <── DOES NOT TRIGGER DEFAULT!
testDefault(NaN);       // NaN   <── DOES NOT TRIGGER DEFAULT!
```

### 🧠 Why the Legacy `||` Pattern Was Dangerous:
In older code, developers wrote `val = val || "default"`.
Because `0`, `""`, and `false` are falsy in JavaScript ([Episode 09](./09-truthy-and-falsy-values.md)), passing `0` (a completely valid number!) accidentally wiped out the user's input:
```javascript
// Legacy bug:
function setVolume(vol) {
  vol = vol || 50; // Passing 0 accidentally sets volume to 50!
}
```
ES6 Default Parameters completely fix this because they trigger **only on `undefined`**!

---

## 5. Dynamic Evaluation at Call Time

Default expressions are **not** evaluated once when the code loads; they are evaluated **at runtime on every single call**:

```javascript
function getRandomNumber() {
  console.log("Generating random number...");
  return Math.floor(Math.random() * 100);
}

function assignId(id = getRandomNumber()) {
  console.log("ID assigned:", id);
}

// Pass 1: Calls getRandomNumber()
assignId(); 

// Pass 2: Calls getRandomNumber() again! (Fresh unique value!)
assignId();

// Pass 3: Value provided -> getRandomNumber() is NEVER CALLED!
assignId(42); 
```

---

## 6. Dependent Defaults & Left-to-Right Evaluation

Earlier parameters in the signature are already initialized and can be used by subsequent default parameters:

```javascript
// ✅ VALID: 'tax' and 'total' reference earlier parameters
function calculateReceipt(price, tax = price * 0.1, total = price + tax) {
  console.log(`Price: $${price}, Tax: $${tax}, Total: $${total}`);
}

calculateReceipt(100); // Price: $100, Tax: $10, Total: $110
calculateReceipt(200); // Price: $200, Tax: $20, Total: $220
```

### ⚠️ The Parameter TDZ Error (Right-to-Left Dependency):
```javascript
// ❌ WRONG: 'b' has not been initialized yet when 'a' is evaluated!
function invalid(a = b, b = 10) {
  return a + b;
}
invalid(); // 💥 ReferenceError: Cannot access 'b' before initialization
```
- Parameters have their own scope and are evaluated strictly from **left to right**. Attempting to use a parameter before its declaration hits the **Temporal Dead Zone (TDZ)**!

---

## 7. Common Mistakes & Anti-Patterns

### 1. Putting Default Parameters Before Required Parameters
```javascript
// ⚠️ POOR PRACTICE:
function createUser(role = "Guest", username) {
  console.log(`${username} is a ${role}`);
}

// To use the default role, you must awkward pass undefined:
createUser(undefined, "Alice");
```
- **Best Practice:** Always place parameters with default values at the **end** of your parameter list:
  ```javascript
  function createUser(username, role = "Guest") {
    console.log(`${username} is a ${role}`);
  }
  createUser("Alice"); // Clean!
  ```

---

## 8. ❓ Confusion Checks

### ❓ How do default parameters affect `function.length`?
In [Episode 28](./28-introduction-to-functions.md), you learned `fn.length` counts formal parameters. 
**Rule:** `fn.length` counts only parameters **before the first default parameter**!
```javascript
function a(x, y, z) {}
console.log(a.length); // 3

function b(x, y = 10, z) {}
console.log(b.length); // 1 (Stops counting at y!)
```

### ❓ Can I use a required parameter validator as a default?
**Yes!** A clever JavaScript pattern:
```javascript
const required = (paramName) => {
  throw new Error(`Missing required parameter: ${paramName}`);
};

function processOrder(id = required("id"), amount = required("amount")) {
  console.log("Order processed:", id, amount);
}

processOrder(101); // 💥 Error: Missing required parameter: amount
```

---

## 9. ⚠️ Edge Cases & Boundary Conditions

### Skipping a Default Parameter
If you want to use the default value for an earlier parameter while supplying a value for a later parameter, pass **`undefined`**:
```javascript
function greet(greeting = "Hello", name = "World") {
  console.log(`${greeting}, ${name}!`);
}

greet(undefined, "Alice"); // "Hello, Alice!"
```

---

## 10. 🧠 Brain Triggers

> 🧠 **Brain Trigger 1:** If a function says `function test(x = 5) {}`, what does `test(null)` assign to `x`?
> **Answer:** `null`. Defaults trigger ONLY on `undefined`.

> 🧠 **Brain Trigger 2:** If you pass `test("")`, does it use the default?
> **Answer:** No. Empty string `""` is a valid string, so `x` becomes `""`.

---

## 11. 🔥 Interview Deep Dive

### Q1: Predict the output:
```javascript
let x = 1;

function foo(x, y = function() { x = 2; }) {
  var x = 3;
  y();
  console.log(x);
}

foo();
console.log(x);
```
<details>
<summary><b>View Answer & Analysis</b></summary>

**Output:**
```text
3
1
```
**Explanation:**
1. When default parameters are present, ECMAScript creates an **intermediate Parameter Scope** between the outer scope and the function body scope.
2. In the parameter scope: `x` is initialized to `undefined`. `y` closes over this parameter `x`.
3. Inside the function body: `var x = 3` creates a local variable `x` scoped to the body.
4. When `y()` executes, it modifies the `x` in the **parameter scope** (`x = 2`), leaving the body `x` untouched (`3`).
5. `console.log(x)` inside prints `3`.
6. Outer global `x` was never modified, so it prints `1`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: The Modern Standard
Default parameters replace fragile manual checks (`if (x === undefined) x = ...`) and error-prone `||` coercion traps.

### 🟡 SHOULD KNOW: Default Parameters in Destructuring
Default values can be combined directly with destructuring ([Episode 49](./49-destructuring-in-javascript.md)):
```javascript
function renderButton({ text = "Click Me", color = "blue" } = {}) {
  console.log(`Rendering ${color} button: ${text}`);
}
renderButton(); // Rendering blue button: Click Me
```

### 🔵 DEEP DIVE: Parameter Scope vs. Body Scope
Under ES6 specification (§14.1.20), if a function contains parameter initializers, a separate declarative environment record is created for the parameter list. Variable declarations inside the function body do not shadow parameters in the same environment.

### ⚫ IMPLEMENTATION DETAIL: Bytecode Initialization Branch
In V8 Ignition bytecode, default parameters emit a test instruction:
`Ldar a0` $\to$ `TestUndetectable / TestReferenceEqual (undefined)` $\to$ `JumpIfFalse`. If not undefined, it jumps past the default expression bytecode.

---

## 🧠 What You Actually Need to Remember
1. Default parameters set fallbacks directly in the function header: `(a = 10)`.
2. **Only `undefined` triggers the default**; `null`, `0`, and `""` do not.
3. Defaults are evaluated at call time, not definition time.
4. Earlier parameters can be used by subsequent default parameters (`a, b = a * 2`).
5. Always place parameters with defaults at the end of the signature.
6. Passing `undefined` explicitly triggers the default fallback.

---

## ⚡ 30-Second Revision
- **Syntax:** `function fn(x = 10) { ... }`
- **Trigger:** `x === undefined` (omitted or explicitly `undefined`).
- **Does NOT trigger on:** `null`, `0`, `false`, `""`.
- **Dynamic:** Evaluates fresh on every invocation.
- **Positioning:** Place default parameters at the end.
- **`fn.length`:** Excludes parameters with defaults.

---

## 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task
Write a function `createAvatar(url = "default-avatar.png", size = 50)` that prints `"Avatar: [url], Size: [size]px"`. Test calling it with:
1. No arguments
2. Only a custom size of 100
3. A custom URL `"user.jpg"` and default size
```javascript
// Solution:
function createAvatar(url = "default-avatar.png", size = 50) {
  console.log(`Avatar: ${url}, Size: ${size}px`);
}

createAvatar();                       // Avatar: default-avatar.png, Size: 50px
createAvatar(undefined, 100);          // Avatar: default-avatar.png, Size: 100px
createAvatar("user.jpg");             // Avatar: user.jpg, Size: 50px
```

### Interview Readiness Checklist
- [ ] Can I define the exact condition that triggers default parameters?
- [ ] Do I know why `param = param || "default"` is an anti-pattern for numbers and booleans?
- [ ] Can I explain what happens if a default parameter tries to access a parameter to its right?
- [ ] Do I understand how default parameters affect `function.length`?
- [ ] Can I explain the separate Parameter Scope in modern ECMAScript?
