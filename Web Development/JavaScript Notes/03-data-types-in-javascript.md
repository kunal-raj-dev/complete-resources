# Episode 03 — Data Types in JavaScript

> **One-Line Mental Model:** Primitives are raw building blocks carved from solid granite (immutable values stored directly by value); Objects are treasure chests whose keys and addresses can be shared.

---

## 🎯 What You Will Learn

- The two fundamental data categories in JavaScript: **Primitives** vs **Non-Primitives (Objects)**.
- The 7 Primitive data types in modern JavaScript: `number`, `string`, `boolean`, `undefined`, `null`, `bigint`, and `symbol`.
- How the `typeof` operator works and the famous historical bug `typeof null === 'object'`.
- The real technical difference between `undefined` (engine-level uninitialized state) and `null` (developer-level intentional absence).
- How explicit type conversion works across types (`Number()`, `String()`, `Boolean()`, unary `+`, `parseInt`).
- Why primitive values are strictly **immutable** in memory even when reassigned to variables.

---

## 1. The Idea in Simple Words

### Simple Explanation
In computer programming, every piece of information belongs to a specific "type." Just like in the physical world where you can drink water, read a book, and count coins—but you cannot count water or drink a book—a computer handles words, numbers, and yes/no switches differently.

In JavaScript, data is split into two major groups:
1. **Primitives:** Simple, single, standalone values (like the number `42`, the text `"hello"`, or the boolean `true`).
2. **Non-Primitives (Objects):** Complex collections that can hold multiple primitive values grouped together (like an address book or a list of shopping items).

### Technical Explanation
The ECMAScript specification categorizes values into **Primitive values** and **Objects**. A primitive is data that is not an object and has no methods of its own (though JavaScript wraps primitives in temporary *primitive wrapper objects* when property access is attempted). Primitives are immutable—their internal value cannot be modified in-place; any operation produces a brand new primitive value. The language defines exactly **7 primitive types**: `Undefined`, `Null`, `Boolean`, `Number`, `String`, `Symbol` (ES6), and `BigInt` (ES2020).

### Before vs After Motivation
- **Before:** Developers who do not understand data types suffer from silent bugs: adding numbers that accidentally concatenate as strings (`"10" + 20 = "1020"`), receiving `NaN` from calculations, or crashing on `TypeError: Cannot read properties of undefined`.
- **After:** Understanding type rules enables clean conversions, defensive input validation, predictable arithmetic, and total confidence when debugging.

---

## 2. 🧠 Mental Model: The Granite Blocks vs The Shipping Containers

- **Primitives are Granite Blocks:** 
  If you carve the number `5` or the text `"apple"` into a block of solid granite, you cannot open it up and change a piece inside. If you want the number `6` or `"apples"`, you do not mutate the stone; you throw away the stone and carve an entirely new granite block.
- **Objects are Shipping Containers:** 
  A container has an identifying reference. Inside the container, you can add properties, remove properties, or change values without changing the container's identity.

```
PRIMITIVE (Granite Block - Immutable):
   ┌─────────┐
   │  "cat"  │  ─── Cannot change 'c' to 'b' in-place!
   └─────────┘

NON-PRIMITIVE (Shipping Container - Mutable):
   ┌───────────────────────────┐
   │ Object Reference          │
   │ ├── name: "Mittens"       │ ─── Can change properties inside!
   │ └── age: 3                │
   └───────────────────────────┘
```

---

## 3. Basic Syntax & The 7 Primitive Types

| Primitive Type | Representation | Example Values | `typeof` Output |
| :--- | :--- | :--- | :--- |
| **`number`** | 64-bit floating-point (IEEE 754) | `42`, `3.14`, `-0`, `Infinity`, `NaN` | `"number"` |
| **`string`** | Sequence of UTF-16 code units | `"hello"`, `'world'`, `` `template` `` | `"string"` |
| **`boolean`** | Logical truth values | `true`, `false` | `"boolean"` |
| **`undefined`**| Uninitialized default state | `undefined` | `"undefined"` |
| **`null`** | Intentional absence of an object | `null` | `"object"` *(Historical Bug)* |
| **`bigint`** | Arbitrary precision integers | `9007199254740991n`, `100n` | `"bigint"` |
| **`symbol`** | Globally unique identifier | `Symbol("id")`, `Symbol.iterator` | `"symbol"` |

---

## 4. Smallest Useful Example

```javascript
// Inspecting primitive types with typeof
console.log(typeof 100);             // "number"
console.log(typeof "JavaScript");    // "string"
console.log(typeof true);            // "boolean"
console.log(typeof undefined);       // "undefined"
console.log(typeof null);            // "object" (Historical engine bug!)
console.log(typeof 9007199254740992n); // "bigint"
console.log(typeof Symbol("key"));   // "symbol"
```

---

## 5. What Just Happened?

```
V8 evaluates `typeof` on different values
         │
         ▼
[1] `typeof 100`: Inspects binary representation -> Classifies as 64-bit IEEE 754 float -> returns "number".
         │
         ▼
[2] `typeof "JavaScript"`: Sequence of characters -> Classifies as UTF-16 string -> returns "string".
         │
         ▼
[3] `typeof undefined`: Engine checks type descriptor -> matches Undefined type -> returns "undefined".
         │
         ▼
[4] `typeof null`: Early type tag interaction -> returns "object" (permanent historical legacy quirk)!
```

1. **First:** The `typeof` operator inspects the internal runtime type tag of the supplied operand.
2. **Next:** It resolves the language-level string identifying the category.
3. **Changed:** Primitives return their exact category name, with the notable exception of `null`.
4. **State:** The string literal is returned synchronously to the caller.

---

## 6. Visual Explanation: Type Conversion Matrix

### Converting to Number (`Number(x)` vs `+x` vs `parseInt(x)`)

```
Input Value             Number(val) / +val         parseInt(val, 10)
────────────────────────────────────────────────────────────────────────
"42"                    42                         42
"42px"                  NaN (Strict!)              42 (Parses until non-digit!)
"px42"                  NaN                        NaN
"" (empty string)       0                          NaN
"   " (whitespace)      0                          NaN
true                    1                          NaN
false                   0                          NaN
null                    0                          NaN
undefined               NaN                        NaN
```

---

## 7. Important Differences

### Comparison: `undefined` vs `null`

> 💡 **Visual Analogy:** 
> - `undefined`: A cardboard box that was delivered, but nobody opened it or put anything inside yet.
> - `null`: A cardboard box with a sign written by the developer: *"This box is intentionally empty."*

| Feature | `undefined` | `null` |
| :--- | :--- | :--- |
| **Meaning** | Value does not exist because it has not been defined yet. | Value intentionally set to represent "no value" or "empty". |
| **Originator** | Usually the **JavaScript engine** (default value of declared variables, missing function returns, non-existent object properties). | Usually the **developer** (explicitly clearing an object reference or database field). |
| **`typeof` return** | `"undefined"` | `"object"` |
| **Converted to Number** | `Number(undefined) === NaN` | `Number(null) === 0` |
| **Converted to Boolean**| `false` (falsy) | `false` (falsy) |
| **Equality Check** | `undefined == null` is `true` | `undefined === null` is `false` |

---

## 8. Common Mistakes & Anti-Patterns

### 1. The Accidental String Concatenation Trap
```javascript
const inputA = "50";
const inputB = 20;

// ❌ WRONG: '+' operator concatenates if either operand is a string!
console.log(inputA + inputB); // "5020" (String concatenation!)

// ✅ CORRECT: Explicitly convert to number first
console.log(Number(inputA) + inputB); // 70
console.log(+inputA + inputB);        // 70 (Unary plus shorthand)
```

### 2. Forgetting the Radix in `parseInt`
```javascript
// ⚠️ DANGEROUS: Always provide the second parameter (radix 10 for decimal)
const val = parseInt("08"); // In older JS engines, "0" prefix meant octal (base 8)!

// ✅ CORRECT:
const safeVal = parseInt("08", 10); // 8
```

### 3. Attempting to Mutate a Primitive String
```javascript
let str = "hello";
str[0] = "H"; // Silently fails in sloppy mode; throws TypeError in strict mode!
console.log(str); // "hello" (Unchanged! Primitives are strictly immutable!)

// ✅ CORRECT: Strings must be replaced by constructing a new string
str = "H" + str.slice(1);
console.log(str); // "Hello"
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

### 🧠 Brain Trigger: Why is `typeof NaN` equal to `"number"`?
How can "Not-a-Number" be a number?
> **Answer:** In computer science (IEEE 754 standard), `NaN` is a special numeric bit pattern representing a failed or undefined mathematical operation (such as `0 / 0` or `Number("hello")`). It belongs to the `Number` type system because it is produced by numeric operations and stored in floating-point registers.

### ❓ Confusion Check: If strings are primitives, how can we call methods like `"hello".toUpperCase()`?
> **Answer (Autoboxing):** When you access a property or method on a primitive (like `.length` or `.toUpperCase()`), JavaScript behind the scenes creates a temporary **wrapper object** (`new String("hello")`), invokes the method, returns the result, and immediately discards the wrapper object for garbage collection!

---

## 10. ⚠️ Edge Cases & Exceptions

### 1. `NaN` Does Not Equal Itself!
`NaN` is the only value in JavaScript that is not equal to itself:
```javascript
console.log(NaN === NaN); // false!
console.log(NaN == NaN);  // false!

// How to reliably check for NaN:
console.log(Number.isNaN(NaN)); // true (Modern standard check)
```

### 2. The Safe Integer Boundary (`Number.MAX_SAFE_INTEGER`)
JavaScript numbers are standard 64-bit IEEE 754 floats. They can only safely represent integers up to $2^{53} - 1$ ($9,007,199,254,740,991$):
```javascript
console.log(9007199254740991 + 1); // 9007199254740992
console.log(9007199254740991 + 2); // 9007199254740992 (Precision lost!)

// Solution: Use BigInt for integers beyond 9 quadrillion!
console.log(9007199254740991n + 2n); // 9007199254740993n (Exact!)
```

### 3. Mixing `BigInt` and `Number` Throws a `TypeError`
You cannot mix BigInt and standard Number in arithmetic without explicit conversion:
```javascript
console.log(10n + 5); // ❌ TypeError: Cannot mix BigInt and other types!
console.log(10n + BigInt(5)); // ✅ 15n
```

---

## 11. 🔥 Interview Deep Dive

### Conceptual: Explain the `typeof null === 'object'` Bug and Why it Cannot be Fixed
**Question:** Why does `typeof null` evaluate to `"object"`, and why didn't TC39 fix it in ES6?
**Answer:** A commonly cited historical explanation is that early JavaScript implementations used tagged value representations in which `null` interacted with the object type tag. The exact internal representation is implementation-specific and is not an ECMAScript requirement. Later, when a formal proposal to correct `typeof null` to return `"null"` was tested, significant portions of the existing web broke because existing production code and libraries relied on `typeof null === "object"`. To preserve the web's fundamental backward-compatibility guarantee, the behavior remains permanently standardized in the ECMAScript specification.

### Output Tracing: Type Coercion Challenge
```javascript
console.log(1 + "2" + 3);
console.log(1 + +"2" + 3);
console.log(10 - "2");
console.log(Number(null) + Number(undefined));
```

### Predict first:
What gets logged in the console?

<details>
<summary>View Output & Explanation</summary>

```
"123"
6
8
NaN
```

**Explanation:**
1. `1 + "2"` evaluates to `"12"` (string concatenation). Then `"12" + 3` evaluates to `"123"`.
2. `+"2"` is a unary plus that converts `"2"` to number `2`. Expression becomes `1 + 2 + 3 = 6`.
3. The `-` subtraction operator is not overloaded for strings; it forces numeric conversion: `10 - 2 = 8`.
4. `Number(null)` is `0`; `Number(undefined)` is `NaN`. `0 + NaN` evaluates to `NaN`.
</details>

---

## 12. 🔬 Optional Deep Dive

### 🟢 MUST KNOW: Strict Equality vs Loose Equality
- `===` (Strict Equality): Checks both **value** and **type** without coercion. (`null === undefined` $\to$ `false`).
- `==` (Loose Equality): Performs implicit type coercion if types differ. (`null == undefined` $\to$ `true`).

### 🟡 SHOULD KNOW: BigInt Limitations
BigInt cannot represent fractional decimal numbers (e.g. `5n / 2n` truncates towards zero to `2n`). It is primarily used for database primary keys (UUIDs / 64-bit Twitter tweet IDs), financial math, and cryptographic hashing.

### 🔵 DEEP DIVE: Symbols as Private Object Properties
Symbols are unique and immutable primitives used to create non-enumerable, collision-free object property keys:
```javascript
const id1 = Symbol("id");
const id2 = Symbol("id");
console.log(id1 === id2); // false! Every Symbol is unique.
```

### ⚫ IMPLEMENTATION DETAIL — V8 Smi (Small Integer) Representation
> ⚙️ **Implementation Detail — Chromium Example**
> In the V8 engine, 64-bit floating-point numbers require heap allocation (HeapNumber objects), which incurs garbage collection overhead. To optimize performance, V8 uses a pointer tagging trick called **Smi (Small Integer)**: 31-bit signed integers (on 32-bit systems) or 32-bit signed integers (on 64-bit systems) are stored directly inside the pointer itself with the lowest bit set to `0`, avoiding memory allocation entirely!

## 🧠 What You Actually Need to Remember

1. **Two Categories:** Primitives (standalone, immutable values) vs Non-Primitives (Objects/Arrays, mutable composite reference collections).
2. **7 Primitive Types:** `number`, `string`, `boolean`, `undefined`, `null`, `bigint`, `symbol`.
3. **Immutability of Primitives:** A primitive value cannot be modified in-place; any operation produces a brand-new primitive value.
4. **`undefined` vs `null`:** `undefined` is the engine default for uninitialized variables; `null` is the developer's intentional assignment representing absence of an object.
5. **The `typeof null` Bug:** Evaluates to `"object"` due to a 1995 legacy type tag representation; permanently standardized to avoid breaking the web.
6. **`NaN` Invariant:** `NaN` stands for "Not-a-Number", is of type `"number"`, and never equals anything—including itself (`NaN === NaN` is `false`). Use `Number.isNaN(val)`.
7. **Explicit Conversion:** Use `Number(val)` or unary `+val` for strict parsing; `parseInt(val, 10)` parses leading digits until non-digit characters.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - JavaScript has 7 primitive types: `number`, `string`, `boolean`, `undefined`, `null`, `bigint`, `symbol`.
  - Primitives are immutable values; objects and arrays are mutable composite reference types.
  - `typeof null === 'object'` is a permanent historical legacy quirk; verify `null` with `val === null`.
  - `NaN` is of type `"number"` and is the only JavaScript value not equal to itself (`NaN === NaN` is `false`).
  - `parseInt("10px", 10)` parses leading digits to `10`, whereas `Number("10px")` evaluates to `NaN`.
- **Key Mental Model:** Variables holding primitives hold the value itself; variables holding objects hold a reference pointing to an object identity.
- **Common Trap:** Trying to mutate a string in-place (`str[0] = 'a'`), which fails silently in non-strict mode or throws in strict mode.
- **Interview Question:** *"Why does `typeof null` return `'object'` and how do you accurately test for `null`?"* $\to$ A commonly cited historical explanation is that early implementations used tagged value representations where `null` interacted with the object type tag (the exact internal representation is engine-specific and not a spec guarantee). It is preserved for web backward compatibility. Always test accurately with `val === null` or `Object.is(val, null)`.
- **Code Pattern:**
  ```javascript
  const isRealObject = (val) => typeof val === "object" && val !== null;
  ```

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task
Open your browser DevTools Console (`F12`), paste the snippet below, and observe the conversions:

```javascript
console.log({
  nullToNum: Number(null),
  undefToNum: Number(undefined),
  emptyStrToNum: Number(""),
  strWithPx: parseInt("100px", 10),
  strWithPxNumber: Number("100px"),
  nanCheck: Number.isNaN(NaN)
});
```

### Interview Readiness Checklist
- [ ] Can I name all 7 primitive data types from memory?
- [ ] Can I explain the exact difference between `null` and `undefined`?
- [ ] Can I explain why `typeof null` returns `"object"`?
- [ ] Can I predict what `Number(null)` vs `Number(undefined)` returns?
- [ ] Can I explain why strings cannot be modified in-place using `str[0] = 'X'`?
