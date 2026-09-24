# Episode 32 — What is Hoisting in JavaScript?

> **One-Line Mental Model:** Hoisting is not code physically moving to the top of your file; it is the natural consequence of Phase 1 (Memory Creation Phase) registering declarations before a single line executes.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #32  
> **Video ID:** `E5af3VAaGCs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=E5af3VAaGCs)  
> **Duration:** 25:30  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- What **Hoisting** really is (and dispelling the myth of "physical code relocation").
- How the **Execution Context Creation Phase** ([Episode 30](./30-execution-context-in-javascript.md)) directly causes hoisting.
- How **Function Declarations** are hoisted with their complete function bodies.
- How **`var`** is hoisted and initialized to `undefined`.
- How **`let`** and **`const`** ARE hoisted, but kept strictly in the **Temporal Dead Zone (TDZ)** ([Episode 04](./04-javascript-variables-explained-in-depth.md)).
- Why calling a `var` function expression throws `TypeError`, while calling a `const` function expression throws `ReferenceError`.
- How to solve classic multi-tier hoisting interview trick questions.

---

## 1. The Idea in Simple Words

### Simple Explanation
Imagine a theater director arriving at a stage in the morning before an evening play.
- The director walks onto the stage and writes down the names of all actors, sets up prop tables, and memorizes every monologue in the script.
- That evening, when the curtain rises (Line 1 of code), an actor can walk on stage and deliver a speech from page 20 because the director already stored the speech in memory that morning!

In many textbooks, you will read: *"JavaScript moves all variable and function declarations to the top of the file."* 

**This is a myth!** Your JavaScript source file is never physically rearranged, manipulated, or rewritten. Hoisting is simply the observable result of **Declaration Processing**: before statement code executes, the JavaScript engine processes all declarations within the scope according to ECMAScript language rules.

### Technical Explanation
In ECMAScript, **Hoisting** describes the behavior where identifier declarations are bound to their respective Environment Records during the instantiation phase of an Execution Context, before runtime code evaluation begins.

Because declarations are processed before statement execution:
1. **`FunctionDeclaration`s:** The identifier is bound and immediately initialized to the function object.
2. **`var` Declarations:** The identifier is bound to the VariableEnvironment and initialized to `undefined`.
3. **`let`, `const`, and `class` Declarations:** The identifiers are bound to the LexicalEnvironment, but remain in an **uninitialized** state. Any attempt to read or write to them before their syntactic declaration line evaluates triggers an engine-level `ReferenceError` (the **Temporal Dead Zone**).

---

## 2. 🧠 Mental Model: The Myth vs. The Reality

```
MYTH: Physical Code Rearranging (False!)
┌──────────────────────────────────────────┐
│ function greet() { ... } // Engine moves │ <── NO! The engine does NOT
│ var username = undefined; // this up?    │     physically move your code!
│ greet();                                 │
│ username = "Alice";                      │
└──────────────────────────────────────────┘

REALITY: Declaration Processing Before Statement Run (True!)
┌────────────────────────────────────────────────────────────────────────┐
│ Conceptual Phase 1: Declaration Binding (Before Execution)             │
│ • greet: Bound directly to Function Object                             │
│ • username (var): Bound & initialized to undefined                     │
│ • age (let): Bound, but LOCKED in TDZ (Uninitialized)                  │
├────────────────────────────────────────────────────────────────────────┤
│ Conceptual Phase 2: Statement Execution (Line-by-Line Run)             │
│ • Line 1: greet(); ───> Works! (Function binding exists and is ready)  │
│ • Line 2: console.log(username); ───> Logs "undefined"                 │
│ • Line 3: console.log(age); ───> Throws ReferenceError (TDZ Lock)      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Hoisting Across Different Declarations

| Declaration Type | Hoisted into Memory? | Initial Value in Phase 1 | Accessing Before Line Results In: |
|:---|:---:|:---:|:---|
| **Function Declaration** | **Yes** | **Full Function Body** | **Executes perfectly** |
| **`var`** | **Yes** | **`undefined`** | **Returns `undefined`** |
| **`let`** | **Yes** | *None (Uninitialized)* | **`ReferenceError` (TDZ)** |
| **`const`** | **Yes** | *None (Uninitialized)* | **`ReferenceError` (TDZ)** |
| **`class`** | **Yes** | *None (Uninitialized)* | **`ReferenceError` (TDZ)** |
| **Function Expression (`var`)** | **Yes** | **`undefined`** | **`TypeError: fn is not a function`** |
| **Function Expression (`const`)**| **Yes** | *None (Uninitialized)* | **`ReferenceError: Cannot access...`** |

---

## 4. Smallest Useful Examples & Execution Walkthrough

### Example 1: Function Declaration (Fully Hoisted)
```javascript
sayHello(); // Works! Prints: "Hello, World!"

function sayHello() {
  console.log("Hello, World!");
}
```
**Why it works:** During Phase 1, `sayHello` is completely compiled and stored with its body. When Line 1 runs, the function is 100% ready.

---

### Example 2: `var` Hoisting (Initialized to `undefined`)
```javascript
console.log(city); // Prints: undefined
var city = "Tokyo";
console.log(city); // Prints: "Tokyo"
```
**Why it prints `undefined`:** In Phase 1, `city` is allocated and assigned `undefined`. In Phase 2, line 1 logs that `undefined`. On line 2, `"Tokyo"` replaces `undefined`.

---

### Example 3: `let` & `const` Hoisting (The Temporal Dead Zone)
```javascript
console.log(country); // Uncaught ReferenceError: Cannot access 'country' before initialization
let country = "Japan";
```
**Proof that `let` is hoisted:** If `country` were not hoisted, JavaScript would throw `ReferenceError: country is not defined`! Instead, it explicitly says: *"Cannot access 'country' **before initialization**"*. The engine knows the variable exists, but prevents access because it is in the TDZ!

---

## 5. The Function Expression Trap: `TypeError` vs `ReferenceError`

Interviewers frequently test this distinction:

### Scenario A: Function Expression with `var`
```javascript
greetUser(); // 💥 TypeError: greetUser is not a function

var greetUser = function() {
  console.log("Welcome!");
};
```
- **Why `TypeError`?** 
  - In Phase 1, `greetUser` is created as `var` $\to$ initialized to `undefined`.
  - In Phase 2, Line 1 attempts to invoke `undefined()`! 
  - Since `undefined` is not callable, the engine throws a `TypeError`.

### Scenario B: Function Expression with `const`
```javascript
greetAdmin(); // 💥 ReferenceError: Cannot access 'greetAdmin' before initialization

const greetAdmin = () => {
  console.log("Welcome Admin!");
};
```
- **Why `ReferenceError`?**
  - `const greetAdmin` is hoisted into the **TDZ**.
  - Attempting to evaluate `greetAdmin` on Line 1 hits the TDZ lock, throwing a `ReferenceError` before any call can even be attempted!

---

## 6. Precedence: Functions vs. Variables

What happens if a variable and a function share the exact same identifier name?

```javascript
console.log(typeof test); // "function"

var test = "Hello";
function test() {
  return "I am a function";
}

console.log(typeof test); // "string"
```

### 🧠 Why?
1. In Phase 1, **Function Declarations take priority**: `test` is registered as a function.
2. The `var test` declaration is scanned, but the engine sees `test` already exists, so it does not overwrite it with `undefined`.
3. In Phase 2:
   - Line 1: `typeof test` evaluates to `"function"`.
   - Line 3: `test = "Hello"` executes, overwriting the function with a string!
   - Line 8: `typeof test` is now `"string"`.

---

## 7. Common Mistakes & Anti-Patterns

### 1. Declaring Function Declarations Inside Blocks in Non-Strict Mode
```javascript
if (true) {
  function run() { console.log("Run A"); }
} else {
  function run() { console.log("Run B"); }
}
run(); // In older browsers/sloppy mode, behavior was historically inconsistent!
```
- In modern strict mode (ES6+), block-scoped function declarations are scoped to their enclosing `{}` block. Always use function expressions (`const run = ...`) if conditional function definitions are required.

---

## 8. ❓ Confusion Checks

### ❓ Are `let` and `const` hoisted?
**YES.** They are hoisted into the Lexical Environment, but unlike `var`, they are not initialized with `undefined`. They remain uninitialized in the **Temporal Dead Zone (TDZ)** from the start of the block until the declaration line is reached.

### ❓ Are JavaScript Classes hoisted?
**Yes, but like `let` and `const`, classes are hoisted in the TDZ!**
```javascript
const car = new Vehicle(); // ReferenceError: Cannot access 'Vehicle' before initialization
class Vehicle {}
```

---

## 9. ⚠️ Edge Cases & Boundary Conditions

### The TDZ in Default Parameters
A parameter cannot reference another parameter declared after it, because the second parameter is still in its TDZ:
```javascript
function calculate(a = b, b = 2) { // ❌ Throws ReferenceError!
  return a + b;
}
calculate();
```
*(Here, `b` is evaluated before it has been initialized in the parameter scope).*

---

## 10. 🧠 Brain Triggers

> 🧠 **Brain Trigger 1:** Why is calling `foo()` valid before `function foo() {}`, but invalid before `var foo = () => {}`?
> **Answer:** `function foo() {}` is a Function Declaration (hoisted with body). `var foo = () => {}` is a variable assignment; during Phase 1, `foo` is only `undefined`.

> 🧠 **Brain Trigger 2:** What is the exact error thrown by accessing an uninitialized `let` variable vs an undeclared variable?
> **Answer:** Uninitialized `let`: `ReferenceError: Cannot access 'x' before initialization`. Undeclared variable: `ReferenceError: x is not defined`.

---

## 11. 🔥 Interview Deep Dive

### Q1: Predict the exact console output of this classic interview challenge:
```javascript
var a = 1;

function b() {
  a = 10;
  return;
  function a() {}
}

b();
console.log(a);
```
<details>
<summary><b>View Answer & Analysis</b></summary>

**Output:**
```text
1
```
**Explanation:**
1. Global `var a = 1` is initialized.
2. Inside `b()`'s Function Execution Context, Phase 1 scans local declarations:
   - It finds `function a() {}`!
   - This creates a **local variable `a`** scoped inside `b` that shadows the global `a`.
3. In Phase 2 of `b()`:
   - `a = 10` reassigns the **local** `a` from a function to the number `10`.
   - `return;` exits.
4. The global `a` was never touched!
5. `console.log(a)` in global scope logs `1`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Function Declarations vs Expressions
- Use **Function Declarations** when you want utility functions accessible anywhere in the scope regardless of declaration order.
- Use **`const` Function Expressions / Arrow Functions** when you want strict, predictable, top-to-bottom initialization order.

### 🟡 SHOULD KNOW: The Temporal Dead Zone Start and End Points
The TDZ begins when the execution context containing the block scope is entered. The TDZ ends at the exact character index where the `let` or `const` declaration statement completes evaluation.

### 🔵 DEEP DIVE: B/S/R (Binding, Storage, Read) Lifecycle
Every variable binding lifecycle in ECMAScript consists of 3 distinct stages:
1. **Declaration:** The identifier is bound to scope (happens in Phase 1 for all).
2. **Initialization:** The binding is allocated memory and given an initial value (`var` gets `undefined` in Phase 1; `let`/`const` wait until Phase 2).
3. **Assignment:** A runtime value is written into the initialized binding (`x = 5`).

### ⚫ Implementation Detail — V8 Engine
During parsing in V8, the parser builds an **Abstract Syntax Tree (AST)** and collects all `Declaration` nodes into a `Scope` object before bytecode generation. No instructions are generated to "move" physical source code; the engine simply references the declared scope bindings by index offsets.

---

## 🧠 What You Actually Need to Remember
1. Hoisting is the observable result of **Declaration Processing** before statement execution, **not** physical code movement.
2. **Function Declarations** are hoisted completely with their code body.
3. **`var`** is hoisted and initialized to `undefined`.
4. **`let` and `const`** are hoisted into the **Temporal Dead Zone (TDZ)**; accessing them before initialization throws a `ReferenceError`.
5. Invoking a `var` function expression before its definition line throws `TypeError: fn is not a function`.
6. Function declarations take precedence over `var` declarations with the same name during scope binding.

---

## ⚡ 30-Second Revision
- **Cause:** Declaration binding instantiation before statement execution.
- **Function Declaration:** Fully hoisted $\to$ can be called anywhere.
- **`var`:** Hoisted with `undefined`.
- **`let`/`const`/`class`:** Hoisted into TDZ $\to$ throws `ReferenceError`.
- **`var fn = () => {}`:** Calling early $\to$ `TypeError: fn is not a function`.
- **Rule of Thumb:** Always declare variables and functions at the top of their usage scope.

---

## 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task
Predict the output of the following snippet before running it in DevTools:
```javascript
console.log(myVar);
console.log(myFunc);

var myVar = 100;

var myFunc = function() {
  return "Hello";
};

function myFunc() {
  return "World";
}

console.log(myFunc());
```
*(Hint: Remember precedence during Phase 1, followed by assignment in Phase 2!)*

### Interview Readiness Checklist
- [ ] Can I debunk the "physical code moving" myth with technical accuracy?
- [ ] Do I know why `var` logs `undefined` while `let` throws `ReferenceError`?
- [ ] Can I explain the difference between `TypeError` and `ReferenceError` in function hoisting?
- [ ] Do I understand what happens when a `var` and a `function` share the same name?
- [ ] Can I define the exact start and end boundaries of the Temporal Dead Zone?
