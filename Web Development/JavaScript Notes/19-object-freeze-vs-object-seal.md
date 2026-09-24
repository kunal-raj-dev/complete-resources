# Episode 19 — Object.freeze() vs Object.seal() in JavaScript

> **One-Line Mental Model:** `Object.seal()` is an envelope glued shut (cannot add or delete pages, but you can scribble over existing text); `Object.freeze()` is that same envelope encased in a solid block of ice (cannot add, cannot delete, cannot touch existing text).

---

## 🎯 What You Will Learn

- Why declaring an object with `const` does **NOT** prevent its properties from being modified or deleted.
- The exact capabilities and restrictions of **`Object.seal()`** vs **`Object.freeze()`**.
- How property descriptors (`writable`, `configurable`, `enumerable`) control immutability behind the scenes.
- The vital catch: **Shallow Immutability** (why nested objects remain 100% mutable).
- How to write a robust **`deepFreeze()`** utility function.
- Why non-strict mode silently ignores invalid mutations while `"use strict";` throws a `TypeError`.

---

## 1. The Idea in Simple Words

### Simple Explanation
In JavaScript, beginners think writing `const user = { role: "student" };` makes the user unchangeable. But you can still write `user.role = "admin"` and it updates!
To actually protect the data inside an object from being tampered with, JavaScript gives us two specialized tools:
1. **`Object.seal()`:** "Locks the doors"—you cannot add new properties, and you cannot delete existing properties. But you **can** still edit existing property values.
2. **`Object.freeze()`:** "Puts it in deep freeze"—you cannot add, you cannot delete, and you **cannot** edit existing property values. It becomes completely read-only.

### Technical Explanation
Under the ECMAScript specification:
- `Object.seal(obj)` marks the object as non-extensible (`preventExtensions`), and sets `configurable: false` on all own property descriptors. Existing writable properties can still be modified.
- `Object.freeze(obj)` marks the object as non-extensible, and sets **both `configurable: false` AND `writable: false`** on all existing own data property descriptors.

### Before vs After Motivation
- **Before:** Shared configuration objects or Redux state stores are accidentally mutated across components, causing unpredictable bugs.
- **After:** Freezing state objects ensures total immutability, making state changes predictable and debuggable.

---

## 2. 🧠 Mental Model: The Envelope vs The Block of Ice

```
                     LEVELS OF OBJECT RESTRICTION
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
const user = {...}          Object.seal(user)           Object.freeze(user)
  [The Sticky Note]          [The Glued Envelope]         [The Block of Ice]
────────────────────        ────────────────────        ────────────────────
• Reassign binding: ❌      • Reassign binding: ❌      • Reassign binding: ❌
• Add new keys:     ✅      • Add new keys:     ❌      • Add new keys:     ❌
• Delete keys:      ✅      • Delete keys:      ❌      • Delete keys:      ❌
• Edit values:      ✅      • Edit values:      ✅      • Edit values:      ❌
```

---

## 3. Basic Syntax & Inspection APIs

```javascript
const user = { name: "Anurag", age: 25 };

// Sealing an object
Object.seal(user);
console.log(Object.isSealed(user)); // true
console.log(Object.isFrozen(user)); // false

// Freezing an object
Object.freeze(user);
console.log(Object.isFrozen(user)); // true
```

---

## 4. Smallest Useful Example

```javascript
"use strict"; // Enforces errors instead of silent failures

const product = {
  id: "PROD_101",
  price: 999,
  details: { color: "blue" }
};

// Freeze the product
Object.freeze(product);

// 1. Trying to edit existing property:
// product.price = 799; 
// ❌ TypeError: Cannot assign to read only property 'price' of object

// 2. Trying to add a new property:
// product.discount = 10; 
// ❌ TypeError: Cannot add property discount, object is not extensible

// 3. Trying to delete an existing property:
// delete product.id; 
// ❌ TypeError: Cannot delete property 'id' of object

// 4. SHALLOW IMMUTABILITY CATCH: Nested object is NOT frozen!
product.details.color = "red"; // ✅ SUCCEEDS!
console.log(product.details.color); // "red"
```

---

## 5. What Just Happened?

```
Internal Property Descriptors of `user.price`:
         │
         ▼
[1] Before Freeze:
    { value: 999, writable: true, enumerable: true, configurable: true }
         │
         ▼
[2] After `Object.freeze(user)`:
    • `writable` flipped to `false` (No editing values).
    • `configurable` flipped to `false` (Cannot delete, cannot reconfigure).
    • Object internal `[[Extensible]]` set to `false` (Cannot add new keys).
```

---

## 6. Visual Explanation: Property Descriptor Hierarchy

```
┌────────────────────────────────────────────────────────┐
│ OPERATION            │ Plain const │ seal() │ freeze() │
├──────────────────────┼─────────────┼────────┼──────────┤
│ Add new property     │     ✅      │   ❌   │    ❌    │
│ Delete property      │     ✅      │   ❌   │    ❌    │
│ Modify existing value│     ✅      │   ✅   │    ❌    │
│ Change descriptors   │     ✅      │   ❌   │    ❌    │
│ Mutate nested object │     ✅      │   ✅   │    ✅*   │
└────────────────────────────────────────────────────────┘
(* Shallow immutability applies to both!)
```

---

## 7. Important Differences: `seal()` vs `freeze()`

| Feature | `Object.seal()` | `Object.freeze()` |
| :--- | :--- | :--- |
| **Adds new keys?** | ❌ Forbidden | ❌ Forbidden |
| **Deletes keys?** | ❌ Forbidden | ❌ Forbidden |
| **Edits values?** | **✅ Allowed** | **❌ Forbidden** |
| **`writable` descriptor** | Stays `true` | Flipped to `false` |
| **`configurable` descriptor**| Flipped to `false` | Flipped to `false` |
| **Inspection method** | `Object.isSealed()` | `Object.isFrozen()` |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Believing `Object.freeze()` protects nested objects (Shallow Freeze)
```javascript
const user = {
  name: "Adarsh",
  address: { city: "Bangalore" }
};

Object.freeze(user);

// user.name = "Akash"; // Blocked!
user.address.city = "Delhi"; // ❌ SUCCEEDS! address was NOT frozen!
console.log(user.address.city); // "Delhi"
```

### Mistake 2: Missing `"use strict";` in testing
In non-strict mode, attempting to modify a frozen object fails silently without throwing an error:
```javascript
// Non-strict mode
const obj = Object.freeze({ a: 1 });
obj.a = 99; // Silently ignored!
console.log(obj.a); // Still 1
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** `Object.freeze()` is strictly **shallow**!
> When you freeze an object, the engine freezes the immediate properties of that object. If a property references another nested object, the reference itself cannot be reassigned on the parent, but the referenced child object remains completely unfrozen!

- **Q: Does `Object.freeze()` work on Arrays?**
  - *Click Answer:* **Yes!** Because Arrays are objects in JavaScript. Freezing an array prevents `push()`, `pop()`, `shift()`, and modifying indices (`arr[0] = 99` throws TypeError in strict mode).
- **Q: Can you unfreeze an object once frozen?**
  - *Click Answer:* **No.** There is no `Object.unfreeze()`. Immutability is a one-way street in JavaScript. To edit a frozen object, you must create a new copy.

---

## 10. ⚠️ Edge Cases & Exceptions

### Deep Freeze Implementation
To truly freeze an entire object graph including all nested objects and arrays, you must recursively freeze every property:

```javascript
function deepFreeze(obj) {
  // Retrieve all property names
  const propNames = Object.getOwnPropertyNames(obj);

  // Freeze properties before freezing parent
  for (const name of propNames) {
    const value = obj[name];
    if (value && typeof value === "object") {
      deepFreeze(value); // Recursive call
    }
  }

  return Object.freeze(obj);
}

const secureConfig = deepFreeze({
  api: { url: "https://api.example.com", key: "SECRET" }
});

// secureConfig.api.key = "HACKED"; // ❌ TypeError: Cannot assign to read only property!
```

---

## 11. 🔥 Interview Deep Dive

### Conceptual Reasoning: Explain Object Property Descriptors
Every property on a JavaScript object is backed by an internal **Property Descriptor** record containing four attributes:
1. **`value`:** The actual data stored.
2. **`writable`:** Boolean indicating whether the value can be changed via assignment.
3. **`enumerable`:** Boolean indicating whether the property shows up in `for...in` loops and `Object.keys()`.
4. **`configurable`:** Boolean indicating whether the property can be deleted and whether its descriptor attributes can be modified.

`Object.seal()` sets `configurable: false`.  
`Object.freeze()` sets `configurable: false` AND `writable: false`.

### Predict First: Seal vs Freeze Output
Predict what is logged:

```javascript
const objA = { x: 10 };
const objB = { y: 20 };

Object.seal(objA);
Object.freeze(objB);

objA.x = 99;
objB.y = 99;

console.log("objA.x:", objA.x);
console.log("objB.y:", objB.y);
```

<details>
<summary>▶ Click to reveal Predict First Output</summary>

**Output:**
```
objA.x: 99
objB.y: 20
```

**Explanation:**
- `objA` was **sealed**: editing existing properties is allowed $\to$ `99`.
- `objB` was **frozen**: editing existing properties is blocked $\to$ remains `20`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: The `Object.preventExtensions()` Baseline
There is a three-tiered ladder of immutability in JavaScript:
1. **`Object.preventExtensions(obj)`:** Prevents adding new properties (can still delete, can still edit).
2. **`Object.seal(obj)`:** Prevents adding new properties AND prevents deleting properties (can still edit).
3. **`Object.freeze(obj)`:** Prevents adding, deleting, AND editing.

---

## 🧠 What You Actually Need to Remember

1. **`const` vs Immutability:** `const` only prevents reassigning the variable identifier binding; it does not protect the object's internal properties from mutation.
2. **`Object.seal()` Effects:** Prevents adding new properties and deleting existing properties, but allows modifying existing writable property values.
3. **`Object.freeze()` Effects:** Prevents adding, deleting, or reassigning existing properties; marks all existing own data properties as `writable: false` and `configurable: false`.
4. **Shallow Scope Limitation:** Both `Object.seal()` and `Object.freeze()` are strictly shallow; nested child objects and array elements remain mutable unless recursively frozen.
5. **Strict Mode Errors:** In strict mode (`"use strict"`), attempting to mutate a frozen or sealed object throws a `TypeError`; in non-strict mode, it fails silently.
6. **No Unfreezing:** There is no `Object.unfreeze()`; immutability cannot be undone on an existing object instance.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - `const` prevents identifier reassignment; `Object.freeze()` prevents mutating object properties.
  - `Object.seal()` prevents adding and deleting keys, but permits mutating existing property values.
  - `Object.freeze()` prevents adding, deleting, and updating properties entirely.
  - Freezing and sealing are strictly shallow; nested objects remain mutable unless recursively frozen.
  - In strict mode (`"use strict"`), attempting to mutate a frozen or sealed property throws a `TypeError`.
- **Key Mental Model:** `Object.seal()` glues the door shut (no new rooms, no deleting rooms, but you can rearrange furniture); `Object.freeze()` encases the entire house in solid ice.
- **Common Trap:** Assuming `Object.freeze()` protects nested child objects (`frozenParent.child.prop = "hacked"` succeeds unless a recursive deep freeze is used).
- **Interview Question:** *"What is the difference between `Object.freeze()` and `Object.seal()`?"* $\to$ Both prevent adding and deleting properties (`configurable: false`). However, `seal()` keeps `writable: true` (existing properties can be modified), whereas `freeze()` sets `writable: false` (no modifications allowed).
- **Code Pattern:**
  ```javascript
  const config = Object.freeze({ api: "https://api.com", timeout: 5000 });
  ```

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
```javascript
// Test immutability on an array
const techStack = ["JavaScript", "React", "Node"];
Object.freeze(techStack);

console.log("Is frozen:", Object.isFrozen(techStack)); // true
// techStack.push("Python"); // Observe the TypeError!
```

### Interview Readiness Checklist
- [ ] Can you explain why `const` does not make object properties immutable?
- [ ] Can you list what `seal()` allows that `freeze()` forbids?
- [ ] Do you know what happens to nested objects when a parent is frozen?
- [ ] Can you describe the 4 fields of a Property Descriptor?
- [ ] Can you write a `deepFreeze` function from scratch?
