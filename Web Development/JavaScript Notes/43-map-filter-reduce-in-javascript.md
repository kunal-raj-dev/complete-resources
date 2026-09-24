# Episode 43 — Map, Filter, and Reduce in JavaScript

> **One-Line Mental Model:** The Holy Trinity of functional programming: `map` transforms every element 1-to-1, `filter` sifts elements through a truthy sieve, and `reduce` rolls the entire array into a single snowball value.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete JavaScript Course | ProCodrr)  
> **Instructor:** Anurag Singh  
> **Episode:** #43  
> **Video ID:** `Kc3kSIpL6x8`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Kc3kSIpL6x8)  
> **Duration:** 01:05:01  
> **Status:** AUDITED  

---

## 🎯 What You Will Learn
- The functional distinction between **`map()`**, **`filter()`**, and **`reduce()`**.
- How all three methods enforce **Immutability** by returning new values without modifying the original array.
- The famous **`['1', '7', '11'].map(parseInt)` interview trap** (and why it outputs `[1, NaN, 3]`).
- How to filter collections based on truthy/falsy predicates.
- The inner mechanics of `reduce()`: **Accumulator**, **Current Value**, and **Initial Value**.
- What fatal error occurs when calling `reduce()` on an empty array without an initial value.
- Advanced `reduce()` patterns: Frequency counters, object grouping, and pipeline chaining.

---

## 1. The Idea in Simple Words

### Simple Explanation
Imagine you have an orchard basket containing 10 apples:
1. **`map()` (Transformation):** You peel every apple. You still have **exactly 10 items**, but each one has been transformed into a peeled apple.
2. **`filter()` (Selection):** You inspect the apples and keep only the red ones. You now have **fewer than or equal to 10 items** (e.g. 6 red apples).
3. **`reduce()` (Accumulation):** You throw all the apples into a blender and press puree. You now have **one single smoothie** (a single accumulated result).

None of these methods destroy your original basket; they always produce fresh outputs!

### Technical Explanation
- **`Array.prototype.map(callbackFn)`**: Projects each element through a transformer function, constructing a **brand-new array of identical length** containing the return values.
- **`Array.prototype.filter(callbackFn)`**: Evaluates each element against a predicate function, constructing a **new array containing only elements** where `callbackFn` evaluated to a truthy value via `ToBoolean`.
- **`Array.prototype.reduce(callbackFn [, initialValue])`**: Executes a reducer function on each element in sequence, passing the return value from the calculation on the preceding element. The final result is a **single value** (primitive, object, or array).

---

## 2. 🧠 Mental Model: The Factory Processing Line

```
 INPUT ARRAY: [ 1, 2, 3, 4 ]

 ┌────────────────────────────────────────────────────────┐
 │ 1. map(x => x * 10)                                    │
 │    Output: [ 10, 20, 30, 40 ] (Same Length, New Data)  │
 ├────────────────────────────────────────────────────────┤
 │ 2. filter(x => x > 2)                                  │
 │    Output: [ 3, 4 ] (Subset of Items)                  │
 ├────────────────────────────────────────────────────────┤
 │ 3. reduce((acc, x) => acc + x, 0)                      │
 │    Output: 10 (Single Consolidated Value)              │
 └────────────────────────────────────────────────────────┘
```

---

## 3. `Array.prototype.map()` in Depth

### Syntax
```javascript
const newArray = arr.map((element, index, array) => {
  return transformedValue;
});
```

### Smallest Useful Example:
```javascript
const numbers = [2, 4, 6];
const doubled = numbers.map((n) => n * 2);

console.log(doubled); // [4, 8, 12]
console.log(numbers); // [2, 4, 6] (ORIGINAL UNTOUCHED!)
```

### ⚠️ The Famous `['1', '7', '11'].map(parseInt)` Interview Trap:
```javascript
console.log(['1', '7', '11'].map(parseInt));
// Output: [1, NaN, 3]! 💥
```

#### 🧠 Why on Earth Does This Happen?
1. `map` passes **THREE arguments** to its callback: `(element, index, array)`.
2. `parseInt` accepts **TWO arguments**: `(string, radixBase)`.
3. When passed directly:
   - **Iteration 0:** `parseInt('1', 0)` $\to$ Radix 0 defaults to decimal $\to$ **`1`**.
   - **Iteration 1:** `parseInt('7', 1)` $\to$ Base-1 is mathematically invalid $\to$ **`NaN`**!
   - **Iteration 2:** `parseInt('11', 2)` $\to$ Binary `"11"` ($1\times2^1 + 1\times2^0$) $\to$ **`3`**!

#### ✅ The Fix: Explicit parameter passing or `Number`:
```javascript
['1', '7', '11'].map((str) => parseInt(str, 10)); // [1, 7, 11]
['1', '7', '11'].map(Number);                     // [1, 7, 11]
```

---

## 4. `Array.prototype.filter()` in Depth

### Syntax
```javascript
const filteredArray = arr.filter((element, index, array) => {
  return booleanCondition; // Return truthy to keep, falsy to discard
});
```

### Smallest Useful Example:
```javascript
const users = [
  { name: "Alice", active: true },
  { name: "Bob", active: false },
  { name: "Charlie", active: true }
];

const activeUsers = users.filter((u) => u.active);
console.log(activeUsers);
// [ { name: "Alice", active: true }, { name: "Charlie", active: true } ]
```

### Filtering Out Falsy Values Instantly:
```javascript
const mixedData = [0, "hello", false, 42, "", null, undefined, "world"];
const truthyOnly = mixedData.filter(Boolean);

console.log(truthyOnly); // ["hello", 42, "world"]
```

---

## 5. `Array.prototype.reduce()` in Depth

`reduce()` is the most powerful and versatile array method in JavaScript.

### Syntax
```javascript
const result = arr.reduce((accumulator, currentValue, currentIndex, array) => {
  return updatedAccumulator;
}, initialValue);
```

### 1. Simple Summing Example:
```javascript
const numbers = [10, 20, 30];

const sum = numbers.reduce((acc, current) => {
  console.log(`acc: ${acc}, current: ${current}`);
  return acc + current;
}, 0); // initialValue = 0

console.log("Total Sum:", sum); // 60
```
#### Trace Table:
| Step | `acc` | `current` | `return acc + current` |
|:---:|:---:|:---:|:---:|
| **Init** | `0` | — | — |
| **Pass 1** | `0` | `10` | `10` |
| **Pass 2** | `10` | `20` | `30` |
| **Pass 3** | `30` | `30` | **`60`** |

---

## 6. What Happens if `initialValue` is Omitted in `reduce()`?

If you do NOT provide `initialValue`:
1. `accumulator` is automatically initialized to **the first element of the array** (`arr[0]`).
2. Iteration begins at **index 1** (skipping the first item as `current`).

```javascript
[10, 20, 30].reduce((acc, curr) => acc + curr); // 60 (acc starts at 10)
```

### 💥 The Fatal Empty Array Trap:
If you call `reduce()` on an empty array with **NO initial value**, JavaScript throws a fatal runtime exception:
```javascript
[].reduce((acc, curr) => acc + curr);
// 💥 Uncaught TypeError: Reduce of empty array with no initial value!
```

> 🔥 **Golden Rule:** **ALWAYS provide an `initialValue`** (e.g. `0`, `""`, `{}`, `[]`) to make your `reduce()` calls 100% crash-proof!

---

## 7. Advanced `reduce()` Patterns

### Pattern A: Word Frequency Counter (Tally Map)
```javascript
const votes = ["Yes", "No", "Yes", "Yes", "No", "Abstain"];

const tally = votes.reduce((acc, vote) => {
  acc[vote] = (acc[vote] || 0) + 1;
  return acc;
}, {}); // Initial value is an empty object {}

console.log(tally); // { Yes: 3, No: 2, Abstain: 1 }
```

### Pattern B: Grouping Objects by Category
```javascript
const products = [
  { name: "Laptop", category: "Electronics" },
  { name: "Apple", category: "Groceries" },
  { name: "Phone", category: "Electronics" }
];

const grouped = products.reduce((acc, p) => {
  if (!acc[p.category]) acc[p.category] = [];
  acc[p.category].push(p.name);
  return acc;
}, {});

console.log(grouped);
// { Electronics: ["Laptop", "Phone"], Groceries: ["Apple"] }
```

---

## 8. Method Chaining (Functional Pipelines)

Because `map()` and `filter()` return brand-new arrays, you can chain them together into readable declarative pipelines:

```javascript
const cart = [
  { item: "Shoes", price: 100, inStock: true },
  { item: "Hat", price: 25, inStock: false },
  { item: "Jacket", price: 200, inStock: true }
];

// Pipeline: Keep in-stock -> apply 10% tax -> sum grand total
const grandTotal = cart
  .filter((item) => item.inStock)
  .map((item) => item.price * 1.1)
  .reduce((acc, priceWithTax) => acc + priceWithTax, 0);

console.log(`Grand Total: $${grandTotal.toFixed(2)}`); // $330.00
```

---

## 9. Common Mistakes & Anti-Patterns

### 1. Forgetting to Return in the Reducer
```javascript
// ❌ BUG: Forgetting 'return acc;' causes accumulator to become undefined!
const total = [1, 2, 3].reduce((acc, curr) => {
  acc += curr; // Missing: return acc;
}, 0);
console.log(total); // undefined!
```

### 2. Using `map()` When You Don't Care About the Return Array
If you only want side effects (logging or updating external state), use `forEach()` or `for...of`. Using `map()` without storing or returning the array wastes memory allocating a throwaway array.

---

## 10. ❓ Confusion Checks

### ❓ Can `filter()` transform the values inside the array?
**No, never.** `filter()` only decides *whether* to include an item or not; it cannot alter the item itself. To alter items, follow it with `.map()`.

### ❓ Can `reduce()` replace both `map()` and `filter()`?
**Yes!** In fact, `reduce()` is the mathematical super-set: any transformation or filtering pipeline can be implemented using `reduce()`:
```javascript
// Re-implementing filter + map using reduce:
const doubledEvens = [1, 2, 3, 4].reduce((acc, n) => {
  if (n % 2 === 0) acc.push(n * 2);
  return acc;
}, []);
console.log(doubledEvens); // [4, 8]
```

---

## 11. 🧠 Brain Triggers

> 🧠 **Brain Trigger 1:** If an array has 5 elements, how many times does `map()` execute its callback?
> **Answer:** Exactly 5 times.

> 🧠 **Brain Trigger 2:** If an array has 5 elements and `initialValue` is provided, how many times does `reduce()` execute? What if `initialValue` is omitted?
> **Answer:** With initial value: 5 times. Without initial value: 4 times (first item becomes initial accumulator).

---

## 12. 🔥 Interview Deep Dive

### Q1: Implement a custom `myReduce` polyfill from scratch:
```javascript
Array.prototype.myReduce = function(callback, initialValue) {
  if (typeof callback !== "function") {
    throw new TypeError(callback + " is not a function");
  }

  let accumulator = initialValue;
  let startIndex = 0;

  // Handle omitted initialValue:
  if (arguments.length < 2) {
    if (this.length === 0) {
      throw new TypeError("Reduce of empty array with no initial value");
    }
    accumulator = this[0];
    startIndex = 1;
  }

  for (let i = startIndex; i < this.length; i++) {
    if (i in this) {
      accumulator = callback(accumulator, this[i], i, this);
    }
  }

  return accumulator;
};

console.log([1, 2, 3].myReduce((a, b) => a + b, 10)); // 16
```

---

## 13. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Immutability in State Management
In modern libraries like React and Redux, mutating state directly breaks re-rendering. `map()` and `filter()` are foundational tools in React because they create fresh array references without mutating existing state.

### 🟡 SHOULD KNOW: Performance of Long Chains
Chaining `.filter().map().filter()` allocates intermediate arrays in memory at every step. For arrays with millions of elements, a single `reduce()` or a single traditional `for` loop is significantly faster and uses less heap memory.

### 🔵 DEEP DIVE: The `reduceRight()` Sister Method
`Array.prototype.reduceRight()` works identically to `reduce()`, except it traverses the array in reverse order (from index `arr.length - 1` down to `0`). Useful for composing mathematical functions right-to-left.

### ⚫ IMPLEMENTATION DETAIL: V8 Typed Arrays & Numeric Reduction
In V8, reducing primitive numerical arrays uses specialized SIMD vectorization routines in TurboFan to accumulate values in hardware registers, bypassing function call overhead for hot mathematical loops.

---

## 🧠 What You Actually Need to Remember
1. **`map()`:** Transforms every item; output length === input length.
2. **`filter()`:** Keeps items where callback is truthy; output length $\le$ input length.
3. **`reduce()`:** Accumulates items into a single final value.
4. None of these three methods mutate the original array.
5. `['1', '7', '11'].map(parseInt)` fails because `map` passes index as radix.
6. Always provide an `initialValue` to `reduce()` to prevent empty-array crashes.

---

## ⚡ 30-Second Revision
- **`map`:** 1-to-1 conversion $\to$ new array.
- **`filter`:** Keeps truthy matches $\to$ new array.
- **`reduce`:** Accumulates array into 1 result.
- **`reduce` crash:** `[].reduce(fn)` with no initial value $\to$ `TypeError`.
- **Immutability:** Pure methods; original array stays untouched.
- **Chaining:** `arr.filter(...).map(...).reduce(...)`.

---

## 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task
Given this student score list, write a one-line chained pipeline to:
1. Filter students who scored $\ge 70$.
2. Calculate the average score of those passing students.
```javascript
const scores = [85, 42, 90, 68, 95];

// Solution:
const passingScores = scores.filter((s) => s >= 70);
const avgPassing = passingScores.reduce((acc, s) => acc + s, 0) / passingScores.length;

console.log("Average Passing Score:", avgPassing); // 90
```

### Interview Readiness Checklist
- [ ] Can I explain `map` vs `filter` vs `reduce` in under 30 seconds?
- [ ] Can I explain why `['1', '7', '11'].map(parseInt)` outputs `[1, NaN, 3]`?
- [ ] Do I know what happens when `reduce()` runs on an empty array without an initial value?
- [ ] Can I write a custom polyfill for `Array.prototype.reduce`?
- [ ] Can I use `reduce` to create a frequency counter map or group objects?
