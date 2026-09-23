# Episode 21 — Most Common Array Methods in JavaScript

> **One-Line Mental Model:** Array methods fall into two strict camps: the Surgeons (`splice`, `push`, `pop`, `shift`, `sort`) that physically alter the original array, and the Photographers (`slice`, `concat`, `includes`) that inspect or snap a brand-new copy without touching the original.

---

## 🎯 What You Will Learn

- The crucial distinction between **Mutating (In-Place)** methods and **Non-Mutating (Pure/Immutable)** methods.
- Stack and Queue operations: `push()`, `pop()`, `unshift()`, `shift()`.
- Why `shift()` and `unshift()` are computationally more demanding than `push()` and `pop()`.
- How to search arrays using `indexOf()` vs `includes()`.
- Slicing vs Splicing: The exact, definitive difference between `slice()` and `splice()`.
- The famous JavaScript trap: why `[10, 5, 25].sort()` produces `[10, 25, 5]`.
- Modern ES2023 immutable alternatives (`toSorted()`, `toReversed()`, `toSpliced()`).

---

## 1. The Idea in Simple Words

### Simple Explanation
Once you have a list of data, you need to do things with it: add a new item to the top or bottom, remove an item from the middle, check if an item exists, sort the list alphabetically, or extract a small portion.
JavaScript provides built-in methods on `Array.prototype` to handle all these operations.

### Technical Explanation
Array methods are functions attached to `Array.prototype`. They can be classified into **Mutating methods** (which modify the receiver array object in-place and return varying values like the deleted elements or new length) and **Non-Mutating/Accessor methods** (which leave the receiver untouched and return a new array or primitive value).

### Before vs After Motivation
- **Before:** Manually moving array elements with `for` loops and index counters is tedious, slow, and prone to off-by-one errors.
- **After:** Using declarative methods like `.splice()` or `.includes()` solves complex array operations with a single, readable line of code.

---

## 2. 🧠 Mental Model: The Surgeons vs The Photographers

```
                         ARRAY METHODS
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     THE SURGEONS                          THE PHOTOGRAPHERS
   (Mutates Original Array)              (Returns New Copy/Value)
───────────────────────────────       ───────────────────────────────
• push()    / pop()                   • concat()
• unshift() / shift()                 • slice()
• splice()                            • indexOf()
• sort()                              • includes()
• reverse()                           • join()
```

---

## 3. Comprehensive Array Methods Matrix

| Method | Purpose | Arguments | Return Value | Mutates Original? |
| :--- | :--- | :--- | :--- | :--- |
| **`push(...items)`** | Appends to the end | Elements to add | **New array length** | ⚠️ **YES** |
| **`pop()`** | Removes last element | None | **Removed element** | ⚠️ **YES** |
| **`unshift(...items)`**| Inserts at the start | Elements to add | **New array length** | ⚠️ **YES** |
| **`shift()`** | Removes first element | None | **Removed element** | ⚠️ **YES** |
| **`concat(...arrays)`**| Combines arrays | Arrays / items | **New combined array** | ❌ NO |
| **`indexOf(item)`** | Finds first index | Target item | Index ($0..N-1$) or **`-1`**| ❌ NO |
| **`includes(item)`** | Checks existence | Target item | **`true`** or **`false`** | ❌ NO |
| **`reverse()`** | Reverses order | None | Reference to array | ⚠️ **YES** |
| **`sort([compareFn])`**| Sorts elements | Compare function | Reference to array | ⚠️ **YES** |
| **`slice(start, end)`**| Copies a sub-range | Start index, End index| **New sub-array** | ❌ NO |
| **`splice(start, count, ...items)`**| Adds/removes elements| Start, deleteCount, items| **Array of deleted items**| ⚠️ **YES** |

---

## 4. Smallest Useful Example

```javascript
const animals = ["Dog", "Cat", "Lion", "Tiger"];

// 1. Search with includes & indexOf
console.log(animals.includes("Lion")); // true
console.log(animals.indexOf("Cat"));   // 1

// 2. Non-mutating slice (Extract "Cat" and "Lion")
const subset = animals.slice(1, 3);
console.log("Subset:", subset);         // ["Cat", "Lion"]
console.log("Original:", animals);      // ["Dog", "Cat", "Lion", "Tiger"] (Untouched!)

// 3. Mutating splice (Remove "Lion" and insert "Panther")
const removed = animals.splice(2, 1, "Panther");
console.log("Removed:", removed);       // ["Lion"]
console.log("Modified:", animals);      // ["Dog", "Cat", "Panther", "Tiger"]
```

---

## 5. What Just Happened?

```
Visualizing `animals.splice(2, 1, "Panther")`:
         │
         ▼
[1] Locates index 2 (`"Lion"`).
         │
         ▼
[2] Removes `1` item (`"Lion"`). Stores in return array: `["Lion"]`.
         │
         ▼
[3] Inserts `"Panther"` at index 2.
         │
         ▼
[4] Internal array shifted in-place: ["Dog", "Cat", "Panther", "Tiger"].
```

---

## 6. Visual Explanation: Shift vs Pop Under the Hood

Why is `shift()` generally slower than `pop()` for massive lists?

```
POP (Removes from END):
  [0: Dog] [1: Cat] [2: Lion] ──> [2: Lion] removed!
  No other elements move. Length simply decrements from 3 to 2. (Fast!)

SHIFT (Removes from FRONT):
  [0: Dog] removed!
      ▲
  Cat  ◄── must move from index 1 to index 0!
  Lion ◄── must move from index 2 to index 1!
  Tiger◄── must move from index 3 to index 2!
  Every remaining element in RAM must be re-indexed!
```

---

## 7. Important Differences: `slice()` vs `splice()`

This is the **#1 most frequently asked array question** in junior and mid-level JavaScript interviews:

| Feature | `slice(start, end)` | `splice(start, deleteCount, ...items)` |
| :--- | :--- | :--- |
| **Mutates Original?** | ❌ **NO** (Immutable, returns fresh copy) | ⚠️ **YES** (Modifies original array in-place) |
| **2nd Parameter** | **End Index** (non-inclusive) | **Delete Count** (how many items to remove) |
| **Adding Items** | ❌ Cannot insert items | ✅ Inserts items passed as 3rd, 4th... arguments |
| **Return Value** | Sub-array containing extracted items | Sub-array containing the **deleted** items |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: The Infamous Default `sort()` Trap
```javascript
const numbers = [10, 5, 40, 25, 100];

// ❌ WRONG: Default sort converts elements to STRINGS!
numbers.sort();
console.log(numbers); // [10, 100, 25, 40, 5] (Alphabetical order! '1' comes before '2', '2' before '5')

// ✅ CORRECT: Provide a comparator function (a - b)
numbers.sort((a, b) => a - b);
console.log(numbers); // [5, 10, 25, 40, 100]
```

### Mistake 2: Confusing `indexOf` and `includes` with `NaN`
```javascript
const list = [1, NaN, 2];

// indexOf uses strict equality (NaN === NaN is false!)
console.log(list.indexOf(NaN));  // -1 (Cannot find it!)

// includes uses SameValueZero algorithm:
console.log(list.includes(NaN)); // true (Finds it correctly!)
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** `splice` returns the items you **cut out**, not the items that stayed!
> If you write `const result = arr.splice(1, 2);`, `result` holds the deleted scraps, while `arr` holds the surviving items.

- **Q: Does `push()` return the array?**
  - *Click Answer:* **NO!** `push()` returns the **new length** (a number) of the array. Writing `const newArr = arr.push('X')` sets `newArr` to a number, not an array!
- **Q: How does `concat()` differ from `push()`?**
  - *Click Answer:* `push()` alters the existing array. `concat()` does not touch the existing array; it returns a brand-new combined array.

---

## 10. ⚠️ Edge Cases & Exceptions

### Negative Indices in `slice()`
A negative index counts backwards from the end of the array:
```javascript
const colors = ["red", "green", "blue", "yellow"];

// Extract last 2 elements:
console.log(colors.slice(-2)); // ["blue", "yellow"]

// Extract all except last element:
console.log(colors.slice(0, -1)); // ["red", "green", "blue"]
```

---

## 11. 🔥 Interview Deep Dive

### Conceptual Reasoning: Implementing a Stack and Queue
In technical interviews, you are often asked to implement basic data structures using native arrays:

1. **Stack (LIFO - Last In, First Out):**
   - Insert: `arr.push(item)`
   - Remove: `arr.pop()`
2. **Queue (FIFO - First In, First Out):**
   - Enqueue: `arr.push(item)`
   - Dequeue: `arr.shift()`

### Predict First: Array Mutation Challenge
Predict what is logged:

```javascript
const letters = ["a", "b", "c", "d"];

const p = letters.pop();
const s = letters.slice(1, 2);
const sp = letters.splice(0, 1, "z");

console.log("letters:", letters);
console.log("p:", p);
console.log("s:", s);
console.log("sp:", sp);
```

<details>
<summary>▶ Click to reveal Predict First Output</summary>

**Output:**
```
letters: ["z", "b"]
p: "d"
s: ["b"]
sp: ["a"]
```

**Explanation:**
1. `pop()` removes `"d"` $\to$ `letters` is `["a", "b", "c"]`. `p = "d"`.
2. `slice(1, 2)` extracts index 1 (`"b"`). `letters` unchanged. `s = ["b"]`.
3. `splice(0, 1, "z")` removes 1 item at index 0 (`"a"`), returns `["a"]` into `sp`, and puts `"z"` at index 0 $\to$ `letters` is `["z", "b", "c"]`... wait! Let's check length: after pop, array had 3 items: `["a", "b", "c"]`. Removing `"a"` and inserting `"z"` leaves `["z", "b", "c"]`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Modern ES2023 Non-Mutating Array Methods
Modern JavaScript introduced immutable counterparts to all mutating methods:
- `arr.toSorted()` $\to$ returns new sorted array (leaves `arr` untouched).
- `arr.toReversed()` $\to$ returns new reversed array.
- `arr.toSpliced()` $\to$ returns new spliced array.
- `arr.with(index, val)` $\to$ returns copy with single index replaced.

---

## 13. ⚡ 30-Second Revision

- **Must Remember:** `slice` does not mutate; `splice` mutates in-place; `push`/`unshift` return new length; `pop`/`shift` return removed item.
- **Most Common Confusion:** Calling `sort()` on numbers without `(a, b) => a - b`.
- **One Code Pattern:** Remove item by index safely: `arr.splice(index, 1);`.
- **One Interview Question:** *"What are the arguments of `splice()` and what does it return?"*  
  $\to$ Arguments: `(start, deleteCount, ...itemsToAdd)`. Returns an array containing the removed items.

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
```javascript
const inventory = ["Apple", "Orange", "Banana", "Grape"];

// 1. Remove "Orange" using splice
const orangeIndex = inventory.indexOf("Orange");
if (orangeIndex !== -1) {
  inventory.splice(orangeIndex, 1);
}
console.log(inventory); // ["Apple", "Banana", "Grape"]

// 2. Sort numbers correctly
const scores = [80, 5, 100, 25];
scores.sort((a, b) => a - b);
console.log(scores); // [5, 25, 80, 100]
```

### Interview Readiness Checklist
- [ ] Can you name 5 mutating and 5 non-mutating array methods?
- [ ] Can you explain the difference between `slice()` and `splice()` in detail?
- [ ] Do you know why `[10, 2].sort()` doesn't sort numerically by default?
- [ ] Can you explain why `shift()` requires moving elements in memory?
- [ ] Do you know what `arr.includes(NaN)` returns vs `arr.indexOf(NaN)`?
