# Episode 27 — Do-While Loop in JavaScript

> **One-Line Mental Model:** The `do...while` loop is an "act first, ask questions later" loop that guarantees the body runs at least once before checking if it should repeat.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #27  
> **Video ID:** `XSevUMHPC3o`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=XSevUMHPC3o)  
> **Duration:** 10:40  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- The architectural difference between pre-test loops (`while`, `for`) and post-test loops (`do...while`).
- Why the `do...while` loop body is mathematically guaranteed to execute at least once.
- The syntax requirements, including the mandatory trailing semicolon `;`.
- Practical use cases: Prompt-driven user validation, retry mechanisms, and menu loops.
- A master comparison matrix: `for` vs. `while` vs. `do...while`.
- Common mistakes, variable scoping traps, and infinite loop debugging.

---

## 1. The Idea in Simple Words

### Simple Explanation
In both the `while` loop ([Episode 25](./25-while-loop-in-javascript.md)) and the `for` loop ([Episode 26](./26-for-loop-in-javascript.md)), the security guard checks your ticket **before** you enter the door. If the ticket is invalid right from the start (`condition === false`), you never enter the room at all (zero executions).

The `do...while` loop turns this around: it lets you walk into the room, do your work once, and checks your ticket only **at the exit door**. If your ticket says "repeat", it sends you back to the entrance for another round; if not, you leave.

### Technical Explanation
The ECMAScript `do-while` statement (`do Statement while ( Expression );`) is a **post-test iteration statement**. The engine executes the embedded `Statement` block *before* evaluating the `Expression`. After the statement finishes, `Expression` is evaluated and converted to a boolean via `ToBoolean`. If the result is `true`, execution loops back to the start of the `Statement`. If `false`, execution proceeds to the next statement in the program.

### Before vs After Motivation
- **Pre-Test (`while` Loop):**
  ```javascript
  let password = "";
  // Must prime the condition beforehand or duplicate prompt code
  while (password !== "secret123") {
    password = prompt("Enter password:");
  }
  ```
- **Post-Test (`do...while` Loop):**
  ```javascript
  let password;
  // Natural flow: Prompt first, then test if valid!
  do {
    password = prompt("Enter password:");
  } while (password !== "secret123");
  ```

---

## 2. 🧠 Mental Model: The Rollercoaster Ride Exit Turnstile

```
            [Enter Ride Platform]
                      │
                      ▼
            ┌───────────────────┐
            │   Enjoy the Ride  │  <─── Guaranteed AT LEAST 1 Ride
            │    (Execute Body) │
            └───────────────────┘
                      │
                      ▼
         [Exit Turnstile Checkpoint]
         "Want to ride again?" (while condition)
                      │
             ┌────────┴────────┐
        Yes (True)        No (False)
             │                 │
             ▼                 ▼
     [Go Back to Ride]   [Exit to Theme Park]
```

---

## 3. Core Concept & Syntax

```javascript
do {
  // Statement(s) executed at least once
  // Step forward (update counter / change state)
} while (condition); // Mandatory trailing semicolon
```

### Key Structural Rules:
1. `do` keyword marks the start of the body block.
2. The body executes unconditionally on the first pass.
3. `while (condition);` appears at the bottom.
4. The trailing semicolon `;` is grammatically required by ECMAScript to close the `do...while` statement.

---

## 4. Smallest Useful Example & Execution Walkthrough

```javascript
let count = 10;

do {
  console.log(`Current count: ${count}`);
  count++;
} while (count < 3);

console.log(`Final count outside loop: ${count}`);
```

### Output:
```text
Current count: 10
Final count outside loop: 11
```

### What Just Happened? Step-by-Step Execution
1. Variable `count` is initialized to `10`.
2. Engine reaches `do` block. It enters immediately **without checking any condition**.
3. Body runs: Logs `"Current count: 10"`.
4. `count++` evaluates: `count` becomes `11`.
5. Engine reaches `while (count < 3)`.
6. Condition test: `11 < 3` evaluates to `false`.
7. Loop terminates immediately.
8. Next line runs: Logs `"Final count outside loop: 11"`.

> 💡 **Notice:** Even though `count < 3` was false from the very beginning, the body still executed once!

---

## 5. Visual Comparison: Pre-Test vs Post-Test

```
┌─────────────────────────────────┬─────────────────────────────────┐
│ PRE-TEST (while / for)          │ POST-TEST (do...while)          │
├─────────────────────────────────┼─────────────────────────────────┤
│          [ Condition? ]         │          [ Execute Body ]       │
│             /       \           │                 │               │
│          Yes         No         │                 ▼               │
│          /             \        │          [ Condition? ]         │
│         ▼               ▼       │             /       \           │
│  [ Execute Body ]    [ Skip ]   │          Yes         No         │
│         │                       │          /             \        │
│         └───> (Re-check)        │         ▼               ▼       │
│                                 │   [ Re-run Body ]    [ Exit ]   │
│ Min Executions: 0               │ Min Executions: 1               │
└─────────────────────────────────┴─────────────────────────────────┘
```

---

## 6. Master Comparison Matrix: `for` vs `while` vs `do...while`

| Feature | `for` Loop | `while` Loop | `do...while` Loop |
|:---|:---|:---|:---|
| **Condition Test Point** | Pre-test (before body) | Pre-test (before body) | **Post-test (after body)** |
| **Minimum Executions** | **0** | **0** | **1 (Guaranteed)** |
| **Best Used When** | Number of iterations is known | Condition depends on external state | Action must happen at least once |
| **Pillars Location** | All in one header | Separated across lines | Separated across lines |
| **Trailing Semicolon** | No | No | **Yes (`while (cond);`)** |

---

## 7. Common Mistakes & Anti-Patterns

### 1. Declaring Loop Variables Inside the `do` Block
```javascript
// ❌ WRONG: let/const inside do block is not accessible in while condition
do {
  let userInput = prompt("Enter a number:");
} while (userInput !== "0"); // ReferenceError: userInput is not defined!
```
- **Why it fails:** The curly braces of `do { ... }` define an independent block scope. Variables declared with `let` or `const` inside this block die at the closing brace `}` and cannot be seen by the condition on the next line.
- **✅ Correct:**
  ```javascript
  let userInput; // Declare in outer scope
  do {
    userInput = prompt("Enter a number:");
  } while (userInput !== "0");
  ```

### 2. Forgetting the Trailing Semicolon
```javascript
// ⚠️ POOR PRACTICE: Missing trailing semicolon
do {
  doWork();
} while (isPending) // Relies on Automatic Semicolon Insertion (ASI)
```
- Always explicitly add the `;` after `while (...)` to avoid ambiguous parsing with subsequent statements.

---

## 8. ❓ Confusion Checks

### ❓ Can I use `break` and `continue` inside a `do...while` loop?
**Yes.** 
- `break` immediately jumps out of the entire `do...while` construct.
- `continue` skips the rest of the body and jumps directly to the **bottom condition evaluation** (`while (cond)`).

```javascript
let i = 0;
do {
  i++;
  if (i === 2) continue; // Jumps directly to while (i < 4)
  console.log(i);
} while (i < 4);
// Output: 1, 3, 4
```

### ❓ When should I pick `do...while` over standard `while`?
Pick `do...while` **only** when running the action at least once is a mandatory prerequisite to evaluating the condition. Common examples:
- Prompting a user for input at least once.
- Fetching initial data before checking pagination cursor.
- Rolling a dice or generating a random number that must exist before validation.

---

## 9. ⚠️ Edge Cases & Boundary Conditions

### Accidental Infinite Loops via Flawed Steppers
If the update step is placed inside an inner conditional that is not met:
```javascript
let x = 1;
do {
  console.log(x);
  if (x > 5) {
    x++; // Never reached! Infinite loop freezes tab!
  }
} while (x < 10);
```

---

## 10. 🧠 Brain Triggers

> 🧠 **Brain Trigger 1:** If the condition is `while (false)`, how many times does `do { ... } while (false);` run?
> **Answer:** Exactly once. The body runs, then `false` is evaluated, and the loop stops immediately.

> 🧠 **Brain Trigger 2:** Why is `do...while` rarely used for looping over an Array?
> **Answer:** Because if an array is empty (`arr.length === 0`), a `do...while` loop still executes once, trying to access `arr[0]` (which is `undefined`), leading to bugs or crashes. Standard `for` or `while` loops safely execute 0 times for empty arrays.

---

## 11. 🔥 Interview Deep Dive

### Q1: Predict the output of this code snippet:
```javascript
let x = 5;
let iterations = 0;

do {
  iterations++;
  x *= 2;
} while (x < 5);

console.log(`Iterations: ${iterations}, x: ${x}`);
```
<details>
<summary><b>View Answer & Analysis</b></summary>

**Output:**
```text
Iterations: 1, x: 10
```
**Explanation:**
1. Body executes unconditionally on pass 1: `iterations` becomes `1`, and `x` becomes `10` ($5 \times 2$).
2. Condition is tested: `10 < 5` is `false`.
3. Loop exits. Final values: `iterations = 1`, `x = 10`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: The Post-Test Invariant
A post-test loop cannot have an execution count of zero. If a business logic requirement states *"Display menu, then check if user chose Exit"*, `do...while` is the natural syntactic choice.

### 🟡 SHOULD KNOW: Scope Mechanics at the Boundary
Because `while (cond);` syntactically belongs to the `do-while` statement, any variables evaluated in `cond` must be declared in the parent scope enclosing the `do` statement, never inside the block body.

### 🔵 DEEP DIVE: Converting `while` to `do...while`
Any `while` loop can be rewritten as a `do...while` loop by guarding it with an initial `if`:
```javascript
// while (cond) { body(); }
// is equivalent to:
if (cond) {
  do {
    body();
  } while (cond);
}
```

### ⚫ IMPLEMENTATION DETAIL: Engine Jump Instructions
In engine bytecode (such as V8 Ignition), a `while` loop emits a conditional branch at the top jumping past the loop body. A `do...while` loop avoids the initial branch instruction, executing straight into the loop body bytecode and evaluating a single conditional jump backwards at the end of the block.

---

## 🧠 What You Actually Need to Remember
1. `do...while` runs its body **first**, then checks the condition.
2. It is guaranteed to run **at least once**.
3. The condition is followed by a required semicolon: `while (condition);`.
4. Variables used in the condition must be declared **outside** the `do` block.
5. Never use `do...while` for array iteration if the array could be empty.

---

## ⚡ 30-Second Revision
- **Syntax:** `do { /* body */ } while (condition);`
- **Execution Guarantee:** $N \ge 1$ executions.
- **Key Difference:** Pre-test (`while`) checks first; Post-test (`do...while`) checks last.
- **Scoping Rule:** Outer variables only for the `while` condition.
- **Primary Use Case:** Input prompts and interactive retry loops.

---

## 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task
Write a `do...while` loop that generates random numbers between 1 and 6 (simulating a dice roll using `Math.floor(Math.random() * 6) + 1` from [Episode 08](./08-math-object-in-javascript.md)) and keeps rolling until it rolls a `6`. Print each roll.
```javascript
// Solution:
let roll;
do {
  roll = Math.floor(Math.random() * 6) + 1;
  console.log(`Rolled: ${roll}`);
} while (roll !== 6);
```

### Interview Readiness Checklist
- [ ] Can I explain why `do...while` always executes at least once?
- [ ] Do I know why declaring `let x` inside `do { let x = 1; } while (x < 5)` throws a ReferenceError?
- [ ] Can I choose correctly between `for`, `while`, and `do...while` for a given problem?
- [ ] Do I know what happens when `continue` is used inside a `do...while` loop?
- [ ] Can I predict output for boundary conditions where the initial value violates the condition?
