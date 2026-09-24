# Episode 23 — The Right Way to Copy Objects and Arrays (Shallow vs Deep Copy)

> **One-Line Mental Model:** Reference copy duplicates the key to the same house; Shallow copy builds a new house but shares the same inner rooms; Deep copy replicates the entire house brick-by-brick from the foundation to the attic.

---

## 🎯 What You Will Learn

- The 3 levels of copying: **Reference Assignment**, **Shallow Copy**, and **Deep Copy**.
- The 4 techniques for shallow copying: Spread syntax (`...`), `Object.assign()`, `Array.prototype.slice()`, and `Array.prototype.concat()`.
- Why shallow copying fails when objects contain nested objects or arrays.
- The modern, official standard for true deep copying: **`structuredClone()`**.
- The legacy `JSON.parse(JSON.stringify())` workaround and its 5 fatal flaws.
- How to write a rock-solid custom recursive `deepClone` utility from scratch.

---

## 1. The Idea in Simple Words

### Simple Explanation
If you have an object `user1` and write `const user2 = user1;`, you have NOT copied the object. You have simply made a second name pointing to the exact same object. Changing `user2.name` will change `user1.name`.
To make an independent duplicate, you must choose between:
1. **Shallow Copy:** Copies only top-level properties. If a property is an object or array, the object reference is copied, leaving nested objects shared!
2. **Deep Copy:** Recursively clones every single level of nested objects and arrays so that absolutely zero memory is shared.

### Technical Explanation
Under ECMAScript and HTML specifications:
- **Reference Assignment (`=`)** copies the object reference directly.
- **Shallow Copy** copies own enumerable properties. For primitives, values are copied; for object properties, the object reference is copied into the new container.
- **Deep Copy via `structuredClone()`** invokes the HTML Structured Clone Algorithm. It creates recursive copies for composite structures, handles circular references, preserves typed arrays, Dates, RegExps, Maps, and Sets, but throws a `DataCloneError` on functions and DOM nodes.

### Before vs After Motivation
- **Before:** Developers use `{ ...state }` in Redux or React and are shocked when mutating `state.user.preferences` causes bizarre, unpredictable bugs due to shared references.
- **After:** Using `structuredClone()` guarantees true data isolation across application state changes.

---

## 2. 🧠 Mental Model: The 3 Levels of Copying

```
LEVEL 1: REFERENCE ASSIGNMENT (`user2 = user1`)
   user1 ───┐
            ├───> [ HOUSE @101 ] (Only ONE house exists in memory!)
   user2 ───┘

LEVEL 2: SHALLOW COPY (`user2 = { ...user1 }`)
   user1 ───> [ NEW HOUSE A @101 ] ──┐
                                     ├───> Points to SHARED Living Room @301!
   user2 ───> [ NEW HOUSE B @201 ] ──┘     (Inner objects are shared!)

LEVEL 3: DEEP CLONE (`user2 = structuredClone(user1)`)
   user1 ───> [ HOUSE A @101 ] ───> [ Living Room A @301 ]
   user2 ───> [ HOUSE B @201 ] ───> [ Living Room B @401 ]
   (100% independent! Modifying Room B never affects Room A!)
```

---

## 3. Copying Techniques Comparison Matrix

| Method | Type | Syntax | Handles Nested Objects? | Preserves Functions? | Handles Circular Refs? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Spread (`...`)** | Shallow | `{ ...obj }`, `[...arr]` | ❌ No (Shares refs) | ✅ Yes | N/A (Shallow) |
| **`Object.assign()`** | Shallow | `Object.assign({}, obj)`| ❌ No (Shares refs) | ✅ Yes | N/A (Shallow) |
| **`structuredClone()`** | **Deep** | `structuredClone(obj)` | **✅ YES** | ❌ DataCloneError | **✅ YES** |
| **`JSON.parse(...)`** | Deep (Hack)| `JSON.parse(JSON.stringify(o))`| ✅ Yes | ❌ Strips them! | ❌ Crashes! |

---

## 4. Smallest Useful Example

```javascript
const user1 = {
  name: "Anurag",
  address: { city: "Delhi", pincode: 110001 },
  skills: ["JavaScript", "React"]
};

// 1. Shallow Copy using Spread (...)
const shallowUser = { ...user1 };
shallowUser.name = "Adarsh"; // Top-level change: SAFE
shallowUser.address.city = "Bangalore"; // Nested change: UNSAFE!

console.log("user1 city:", user1.address.city); // "Bangalore" (Mutated original!)

// 2. True Deep Copy using structuredClone()
const deepUser = structuredClone(user1);
deepUser.address.city = "Mumbai";

console.log("user1 city:", user1.address.city);   // "Bangalore" (Untouched!)
console.log("deepUser city:", deepUser.address.city); // "Mumbai" (Independent!)
```

---

## 5. What Just Happened?

```
Trace of Shallow vs Deep Copy:
         │
         ▼
[1] `shallowUser = { ...user1 }`:
    • Allocates new object in Heap for `shallowUser`.
    • Copies primitive `"Anurag"` to `shallowUser.name`.
    • Copies the object reference to `shallowUser.address`!
    • Both `user1.address` and `shallowUser.address` reference the exact same object.
         │
         ▼
[2] `deepUser = structuredClone(user1)`:
    • Allocates new object for `deepUser`.
    • Recursively inspects `user1.address`.
    • Allocates an entirely NEW object on Heap for `deepUser.address`.
    • Copies primitive values `"Bangalore"` and `110001` into the new object.
    • Modifying `deepUser.address` affects ONLY the new allocation.
```

---

## 6. Visual Explanation: The Fatal Flaws of `JSON.parse(JSON.stringify())`

Many developers still rely on the JSON stringify trick. Here is why it breaks in production:

```javascript
const complexData = {
  func: () => "Hello",           // 1. FUNCTIONS: Discarded completely!
  un: undefined,                 // 2. UNDEFINED: Discarded completely!
  sym: Symbol("id"),             // 3. SYMBOLS: Discarded completely!
  date: new Date(),              // 4. DATES: Converted to plain strings (methods lost)!
  nan: NaN,                      // 5. NaN & Infinity: Converted to null!
  // big: 100n                  // 6. BIGINT: Throws TypeError (Cannot serialize BigInt)!
};

const brokenClone = JSON.parse(JSON.stringify(complexData));
console.log(brokenClone);
// { date: '2026-09-24T...', nan: null }
// Notice: func, un, and sym were completely WIPED OUT!
```

> ⚠️ **Further JSON Limitations:**
> - **Circular References:** If an object references itself (`obj.self = obj;`), `JSON.stringify(obj)` throws `TypeError: Converting circular structure to JSON`.
> - **Prototype Loss:** Custom class instances lose their prototypes, turning into plain object literals (`{}`).
> - **BigInt Support:** Attempting to stringify a `BigInt` throws a fatal `TypeError`.

---

## 7. Important Differences: Shallow Array Copying Methods

| Method | Syntax | Notes |
| :--- | :--- | :--- |
| **Spread Operator** | `const copy = [...arr];` | **Modern Standard** (cleanest, most readable) |
| **`slice()`** | `const copy = arr.slice();` | Fast, historical standard |
| **`concat()`** | `const copy = [].concat(arr);` | Slightly verbose |
| **`Array.from()`** | `const copy = Array.from(arr);`| Useful when converting array-likes or iterables |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Attempting to deep copy an object containing functions with `structuredClone`
```javascript
const user = {
  name: "Anurag",
  greet() { console.log("Hello!"); }
};

// ❌ CRASH: structuredClone rejects functions!
structuredClone(user); 
// DOMException: Failed to execute 'structuredClone': function could not be cloned.
```

### Mistake 2: Mutating props received in React components
```javascript
// ❌ MUTATION BUG
function UserCard({ user }) {
  // Shallow copy:
  const updatedUser = { ...user };
  updatedUser.preferences.theme = "dark"; // Mutated parent state directly!
}
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** `Object.assign({}, source)` and `{ ...source }` do the EXACT same thing!
> Both perform a **1-level shallow copy**. Neither performs a deep copy.

- **Q: Does `structuredClone()` work in Node.js?**
  - *Click Answer:* Yes! `structuredClone()` was added as a global standard in Node.js v17.0.0 and in all modern browsers since March 2022.
- **Q: How does `structuredClone()` handle circular references?**
  - *Click Answer:* It maintains an internal identity map of previously cloned objects. When it encounters an object it has already cloned, it links to the clone instead of recursing infinitely.

---

## 10. ⚠️ Edge Cases & Exceptions

### Writing a Custom `deepClone` Function
When you need to copy objects that contain functions (which `structuredClone` rejects), use a recursive cloner with `WeakMap` for circular reference safety:

```javascript
function deepClone(value, hash = new WeakMap()) {
  // 1. Primitives and functions (immutable or non-clonable)
  if (value === null || typeof value !== "object") {
    return value;
  }

  // 2. Handle circular references
  if (hash.has(value)) {
    return hash.get(value);
  }

  // 3. Handle Dates and RegExps
  if (value instanceof Date) return new Date(value);
  if (value instanceof RegExp) return new RegExp(value);

  // 4. Handle Arrays vs Objects
  const copy = Array.isArray(value) ? [] : {};
  hash.set(value, copy);

  for (const key of Object.keys(value)) {
    copy[key] = deepClone(value[key], hash); // Recursive call
  }

  return copy;
}
```

---

## 11. 🔥 Interview Deep Dive

### Conceptual Reasoning: When is a Shallow Copy preferable over a Deep Copy?
1. **Performance:** Deep cloning a large tree with 10,000 nodes takes measurable CPU time and memory allocation. If you only need to modify `user.name`, a shallow copy `{ ...user, name: "New" }` is hundreds of times faster.
2. **Structural Sharing:** Frameworks like React and libraries like Redux rely on **Structural Sharing**. By only shallow-copying the modified path of an object tree, unchanged subtrees keep their reference addresses, allowing React components to skip re-rendering (`React.memo`).

### Predict First: Copy Quiz
Predict what is logged:

```javascript
const original = [1, [2, 3]];
const shallow = [...original];

shallow[0] = 99;
shallow[1][0] = 88;

console.log("original[0]:", original[0]);
console.log("original[1][0]:", original[1][0]);
```

<details>
<summary>▶ Click to reveal Predict First Output</summary>

**Output:**
```
original[0]: 1
original[1][0]: 88
```

**Explanation:**
- `original[0]` is a primitive number `1`. The shallow copy received a distinct value copy, so `original[0]` remains `1`.
- `original[1]` is a nested array `[2, 3]`. The shallow copy copied the **memory reference** of that inner array. Mutating `shallow[1][0] = 88` modified the shared array in heap memory, so `original[1][0]` became `88`!
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Lodash `cloneDeep`
In older production codebases prior to `structuredClone`, developers imported the popular utility library **Lodash**:
```javascript
import cloneDeep from "lodash/cloneDeep";
const safeCopy = cloneDeep(complexObject);
```
In modern JavaScript (2022+), you can replace `cloneDeep` with native `structuredClone()` in 95% of use cases, reducing your client bundle size.

---

## 🧠 What You Actually Need to Remember

1. **Three Levels of Copying:** Reference assignment (`b = a`) copies only the object reference; shallow copying (`{ ...a }`) copies top-level properties but shares nested references; deep copying (`structuredClone(a)`) duplicates nested objects recursively.
2. **Shallow Copy Limitations:** Spread operators and `Object.assign()` only clone the outermost layer; modifying nested objects or arrays mutates the original data.
3. **The `structuredClone()` Standard:** The native web/Node API for deep cloning serializable structures; safely handles circular references, Dates, Sets, Maps, and TypedArrays.
4. **`structuredClone()` Non-Cloneables:** Throws `DataCloneError` when encountering functions, class methods, or DOM nodes.
5. **Flaws of JSON Serialization:** `JSON.parse(JSON.stringify(x))` silently strips `undefined`, functions, and Symbols, converts `Date` to a string, coerces `NaN` to `null`, and throws on circular structures.
6. **Framework Immutability:** State management frameworks (React, Redux) rely on shallow copying each updated branch to maintain referential equality checks.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - Reference assignment (`b = a`) copies only the object reference; no new object is created.
  - Shallow copies (`{ ...obj }`, `Object.assign()`) clone top-level properties, but nested objects remain shared references.
  - Native `structuredClone()` produces deep clones, correctly handling circular references, Dates, Sets, Maps, and TypedArrays.
  - `structuredClone()` throws a `DataCloneError` on functions, class instances, or DOM nodes.
  - Avoid `JSON.parse(JSON.stringify())` due to data loss (functions, `undefined`, `Symbol`, `BigInt`, `Date` methods) and crashing on circular references.
- **Key Mental Model:** Reference copy gives another person your car keys; shallow copy duplicates the car body but keeps the original engine inside; deep copy manufactures an entirely separate car from scratch.
- **Common Trap:** Mutating a nested property in a shallow copy (`{ ...user }`), mistakenly believing that spreading an object deeply clones nested child objects.
- **Interview Question:** *"What are the limitations of `structuredClone()` compared to a custom cloner?"* $\to$ `structuredClone()` cannot clone functions, methods, or DOM nodes (throws `DataCloneError`), ignores Symbol properties, and drops custom prototype chains (instances become plain objects).
- **Code Pattern:**
  ```javascript
  // Deep clone a nested structure safely
  const cloned = structuredClone(state);
  ```

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
```javascript
// Test shallow vs deep copy in console
const original = { title: "Course", chapters: ["Intro", "Setup"] };

// Create one shallow copy and one deep copy
const shallow = { ...original };
const deep = structuredClone(original);

// Mutate nested array
shallow.chapters.push("Variables");

console.log("Original chapters:", original.chapters); // ["Intro", "Setup", "Variables"] (Altered!)
console.log("Deep chapters:", deep.chapters);         // ["Intro", "Setup"] (Safe!)
```

### Interview Readiness Checklist
- [ ] Can you explain the 3 levels of copying in JavaScript?
- [ ] Can you list 3 ways to make a shallow copy of an array?
- [ ] Do you know how `structuredClone()` differs from `JSON.parse(JSON.stringify())`?
- [ ] Can you explain why `structuredClone()` throws an error when an object contains a function?
- [ ] Can you explain why React state management relies on shallow copying instead of deep cloning?
