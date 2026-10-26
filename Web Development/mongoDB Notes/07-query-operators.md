# Episode 07 — Query Selectors: Comparison ($gt, $gte, $in) & Logical ($or, $and, $not) Operators

> **One-Line Mental Model:** Query operators are specialized JSON expression tokens prefixed with `$` that tell the database engine to perform mathematical comparisons, set memberships, or boolean logic instead of simple literal equality.

---

## 📌 Source Metadata
> **Course:** Delta Batch (Web Development)  
> **Module:** 44. MongoDB (Part 1)  
> **Lecture:** 07. Query Operators  
> **Duration:** 08:43  
> **Documentation Ref:** [MongoDB Query and Projection Operators](https://www.mongodb.com/docs/manual/reference/operator/query/)  
> **Status:** AUDITED & EXPANDED  

---

## 🎯 What You Will Learn

- The syntax rules of MongoDB **Operator Expressions** (the `$` symbol convention).
- Complete mastery of **Comparison Query Operators**: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`.
- Complete mastery of **Logical Query Operators**: `$or`, `$and`, `$not`, `$nor`.
- Solving real-world criteria:
  - Numerical ranges (e.g. students with marks $> 75$).
  - Discrete sets (e.g. students living in `["Delhi", "Mumbai"]`).
  - Compound conditions (e.g. scored $> 75$ OR lives in Delhi).
- Why Comparison operators nest inside field names (`{ field: { $gt: val } }`) while Logical operators wrap arrays of conditions (`{ $or: [ {...}, {...} ] }`).
- Case-sensitivity nuances in string set lookups (`$in`).

---

## 1. The Idea in Simple Words

### Simple Explanation
In Episode 06, we wrote equality queries:
```javascript
db.student.find({ city: "Delhi" })
```
This is fine for exact matches. But what if you need:
- All students who scored **higher than 75**?
- All products with a price **between 100 and 500**?
- All customers from **either Tokyo, London, or New York**?
- All users who are **either VIP members OR spent more than $1000**?

You cannot express "greater than" or "OR" using standard JavaScript colon notation `{ marks: > 75 }` because that is invalid syntax. 
MongoDB solves this with **Query Operators**: special keywords starting with `$` (like `$gt` for *greater than*, `$in` for *inside a list*, and `$or` for *either-or logic*).

### Technical Explanation
MongoDB query selectors are declarative BSON expressions evaluated by the query planner. 
- **Comparison Selectors** evaluate a target document's field value against an operand using BSON comparison semantics. They are formatted as: `{ <field>: { <operator>: <value> } }`.
- **Logical Selectors** take one or more expression objects and evaluate them using boolean truth tables. Operators like `$or` and `$and` are formatted as: `{ <operator>: [ { <expression1> }, { <expression2> } ] }`. 

The query optimizer evaluates these operators against available B-Tree indexes. When an index exists on the queried field, comparison operators like `$gt` perform efficient index range scans (`IXSCAN`) rather than scanning every document in the collection (`COLLSCAN`).

---

## 2. 🧠 Mental Model: The Query Filter Architecture

```
1. COMPARISON OPERATOR (Inside the Field):
   Target Field ───> { marks: { $gt: 75 } }
                      │        │    └── Operand Value
                      │        └─────── Comparison Operator ($gt)
                      └──────────────── Target Field Key

2. LOGICAL OPERATOR (Wraps Array of Sub-Queries):
   Logical Gate ───> { $or: [ { marks: { $gt: 75 } }, { city: "Delhi" } ] }
                       │    │   └────── Clause 1 ─────┘  └───── Clause 2 ────┘
                       │    └─ Array of Independent Query Objects
                       └────── Logical Operator ($or, $and, $nor)
```

---

## 3. The Complete Operator Reference Matrix

### 🔹 Comparison Operators

| Operator | Meaning | Syntax Example | Matches |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Equal to | `{ marks: { $eq: 88 } }` | Matches where field equals 88. (Equivalent to `{ marks: 88 }`). |
| **`$ne`** | Not equal to | `{ city: { $ne: "Delhi" } }` | Matches where field is not "Delhi" or field does not exist. |
| **`$gt`** | Greater than ($>$) | `{ marks: { $gt: 75 } }` | Values strictly greater than 75. |
| **`$gte`**| Greater than or equal ($\ge$) | `{ marks: { $gte: 75 } }` | Values 75 or higher. |
| **`$lt`** | Less than ($<$) | `{ marks: { $lt: 60 } }` | Values strictly below 60. |
| **`$lte`**| Less than or equal ($\le$) | `{ marks: { $lte: 60 } }` | Values 60 or below. |
| **`$in`** | In array (Set membership) | `{ city: { $in: ["Delhi", "Mumbai"] } }` | Matches any document where city is either "Delhi" OR "Mumbai". |
| **`$nin`**| Not in array | `{ city: { $nin: ["Delhi", "Mumbai"] } }`| Matches documents where city is neither "Delhi" nor "Mumbai". |

### 🔹 Logical Operators

| Operator | Meaning | Syntax Example | Rule |
| :--- | :--- | :--- | :--- |
| **`$or`** | Logical OR | `{ $or: [ { cond1 }, { cond2 } ] }` | Document matches if **at least one** condition is true. |
| **`$and`** | Logical AND | `{ $and: [ { cond1 }, { cond2 } ] }` | Document matches only if **all** conditions are true. |
| **`$not`** | Logical NOT | `{ marks: { $not: { $gt: 75 } } }` | Inverts query; matches documents where condition is false or field missing. |
| **`$nor`** | Logical NOR | `{ $nor: [ { cond1 }, { cond2 } ] }` | Matches documents that fail **every** specified condition. |

---

## 4. Solving the Lecture Problems Step-by-Step

### 🎯 Problem 1: Find all students where marks > 75

```javascript
// Query:
db.student.find({ marks: { $gt: 75 } })

// OUTPUT:
[
  {
    _id: ObjectId("64fec88c4d37352da5df8407"),
    name: 'adam',
    age: 19,
    marks: 88
  }
]
// (Only Adam has marks strictly greater than 75!)
```

#### Variation: Test with `$gt: 60`
```javascript
db.student.find({ marks: { $gt: 60 } })

// OUTPUT: Matches Adam (88), Bob (75), and Catlyn (64)
[
  { _id: ObjectId("64fec88c..."), name: 'adam', marks: 88, age: 19 },
  { _id: ObjectId("64fec971..."), name: 'bob', city: 'Delhi', marks: 75 },
  { _id: ObjectId("64fec9f5..."), name: 'catlyn', marks: 64, city: 'Delhi' }
]
```

#### Variation: Test with `$gte: 75` (Greater than OR Equal)
```javascript
db.student.find({ marks: { $gte: 75 } })

// OUTPUT: Matches Adam (88) AND Bob (75)
[
  { _id: ObjectId("64fec88c..."), name: 'adam', marks: 88, age: 19 },
  { _id: ObjectId("64fec971..."), name: 'bob', city: 'Delhi', marks: 75 }
]
```

---

### 🎯 Problem 2: Find all students who live in Delhi OR Mumbai

Rather than writing complex repetitive conditions, use the **`$in`** operator with an array of acceptable values:

```javascript
// Query:
db.student.find({ city: { $in: ["Delhi", "Mumbai"] } })

// OUTPUT: Matches Bob (Delhi), Catlyn (Delhi), and Donald (Mumbai)
[
  { _id: ObjectId("64fec971..."), name: 'bob', city: 'Delhi', marks: 75 },
  { _id: ObjectId("64fec9f5..."), name: 'catlyn', marks: 64, city: 'Delhi' },
  { _id: ObjectId("64fec9f5..."), name: 'donald', marks: 58, city: 'Mumbai' }
]
```

#### ⚠️ Case Sensitivity Trap:
```javascript
db.student.find({ city: { $in: ["delhi", "mumbai"] } })
// OUTPUT: [] (Empty! Exact string matching is required)
```

---

### 🎯 Problem 3: Find students who scored > 75 OR live in Delhi

This problem spans **two completely different fields** (`marks` and `city`). We must use the **`$or`** operator wrapping an array of clauses:

```javascript
// Query:
db.student.find({
  $or: [
    { marks: { $gt: 75 } },
    { city: "Delhi" }
  ]
})

// OUTPUT:
[
  {
    _id: ObjectId("64fec88c4d37352da5df8407"),
    name: 'adam',
    age: 19,
    marks: 88      // Matches Clause 1: marks > 75!
  },
  {
    _id: ObjectId("64fec9714d37352da5df8408"),
    name: 'bob',
    city: 'Delhi', // Matches Clause 2: city is "Delhi"!
    marks: 75
  },
  {
    _id: ObjectId("64fec9f54d37352da5df8409"),
    name: 'catlyn',
    marks: 64,
    city: 'Delhi'  // Matches Clause 2: city is "Delhi"!
  }
]
// (Donald is excluded because marks (58) <= 75 and city is "Mumbai" !== "Delhi")
```

---

## 5. What Just Happened Under the Hood?

```
Evaluation of: db.student.find({ $or: [ { marks: { $gt: 75 } }, { city: "Delhi" } ] })

FOR EACH DOCUMENT IN COLLECTION:
┌────────────────────────────────────────────────────────────────────────┐
│ Document 1 (Adam):                                                     │
│ - marks (88) > 75? TRUE.                                               │
│ -> Short-Circuit! Include Adam in result set.                          │
├────────────────────────────────────────────────────────────────────────┤
│ Document 2 (Bob):                                                      │
│ - marks (75) > 75? FALSE.                                              │
│ - city === "Delhi"? TRUE.                                              │
│ -> Include Bob in result set.                                          │
├────────────────────────────────────────────────────────────────────────┤
│ Document 3 (Catlyn):                                                   │
│ - marks (64) > 75? FALSE.                                              │
│ - city === "Delhi"? TRUE.                                              │
│ -> Include Catlyn in result set.                                       │
├────────────────────────────────────────────────────────────────────────┤
│ Document 4 (Donald):                                                   │
│ - marks (58) > 75? FALSE.                                              │
│ - city === "Delhi"? FALSE ("Mumbai").                                  │
│ -> Exclude Donald from result set.                                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Combining Operators: Range Queries (AND logic)

To find values within a range (e.g. marks between 60 and 80 inclusive: $60 \le \text{marks} \le 80$), combine `$gte` and `$lte` inside the same field object:

```javascript
db.student.find({
  marks: {
    $gte: 60,
    $lte: 80
  }
})

// Matches Bob (75) and Catlyn (64)!
```

---

## 7. When is Explicit `$and` Strictly Mandatory?

In MongoDB, writing multiple fields in a query object is an **implicit AND**:
```javascript
// Implicit AND (Clean & Idiomatic):
db.student.find({ city: "Delhi", marks: 75 })
```

However, explicit **`$and`** is strictly mandatory in two situations:
1. **Querying the same operator or field multiple times:**
   ```javascript
   // ❌ WRONG (JavaScript key collision: second $or overwrites first!):
   db.student.find({
     $or: [ { a: 1 }, { b: 1 } ],
     $or: [ { c: 1 }, { d: 1 } ]
   })

   // ✅ CORRECT (Using explicit $and):
   db.student.find({
     $and: [
       { $or: [ { a: 1 }, { b: 1 } ] },
       { $or: [ { c: 1 }, { d: 1 } ] }
     ]
   })
   ```
2. **Combining dynamic expressions in aggregation pipelines.**

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Placing the comparison operator outside the field
```javascript
// ❌ SYNTAX ERROR / UNINTENDED QUERY:
db.student.find({ $gt: { marks: 75 } })

// 🔍 WHY: Comparison operators ($gt, $lt, $in) evaluate a SPECIFIC field.
// They must be nested INSIDE the field object!
// ✅ CORRECT:
db.student.find({ marks: { $gt: 75 } })
```

### Mistake 2: Forgetting that `$or` expects an Array
```javascript
// ❌ WRONG:
db.student.find({ $or: { marks: 75, city: "Delhi" } })

// 🔍 WHY: $or evaluates a list of separate conditions. It requires an array `[...]`!
// MongoServerError: $or must be an array
// ✅ CORRECT:
db.student.find({ $or: [ { marks: 75 }, { city: "Delhi" } ] })
```

### Mistake 3: Using `$or` instead of `$in` for the same field
```javascript
// ❌ UNNECESSARILY VERBOSE & SLOWER:
db.student.find({
  $or: [
    { city: "Delhi" },
    { city: "Mumbai" },
    { city: "Bangalore" }
  ]
})

// ✅ FAST & IDIOMATIC (Use $in when checking 1 field against multiple values):
db.student.find({ city: { $in: ["Delhi", "Mumbai", "Bangalore"] } })
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** Think of `$in` as a compact `$or` for a **single field**.
> `{ city: { $in: ["A", "B"] } }` is 100% equivalent to `{ $or: [ { city: "A" }, { city: "B" } ] }`, but cleaner and better optimized by the query planner.

- **Q: What does `{ marks: { $ne: 88 } }` return for a document that doesn't have a `marks` field?**
  - *Click Answer:* It returns the document! `$ne` matches any document where the field is not 88, which includes documents where the field is absent.
- **Q: Can `$nin` take single values instead of an array?**
  - *Click Answer:* No. Both `$in` and `$nin` strictly require an array of target values.

---

## 10. 🔥 Interview Deep Dive

### Index Utilization: `$in` vs `$or` vs `$nin`
**Q:** *How do indexes perform when using `$in`, `$or`, and `$nin`?*

**Answer:**
1. **`$in` on an indexed field:** MongoDB performs index seeks for each value in the array. Very fast ($O(\log N)$).
2. **`$or` on indexed fields:** MongoDB can use a **separate index for each clause** in the `$or` array, merge the resulting index streams, and deduplicate documents! For example, `{ $or: [{ marks: { $gt: 75 } }, { city: "Delhi" }] }` can use an index on `marks` AND an index on `city` simultaneously!
3. **`$nin` and `$ne`:** Negative operators generally cannot use B-Tree indexes effectively because they specify what *not* to find. They typically trigger a full collection scan (`COLLSCAN`) unless compounded with positive equality criteria.

---

## 🧠 What You Actually Need to Remember

1. **Comparison Syntax:** `{ field: { $operator: value } }` (`$gt`, `$gte`, `$lt`, `$lte`, `$ne`).
2. **Set Membership:** `{ field: { $in: [val1, val2] } }` for matching any value in a list.
3. **Logical Syntax:** `{ $or: [ { cond1 }, { cond2 } ] }` requires an **array of condition objects**.
4. **Range Queries:** `{ field: { $gte: min, $lte: max } }`.
5. **Implicit AND:** Commas separate fields for AND logic; use explicit `$and` only when resolving key collisions.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - Greater than: `$gt`; Greater than equal: `$gte`.
  - Less than: `$lt`; Less than equal: `$lte`.
  - In array: `$in`; Not in array: `$nin`.
  - Logical: `$or`, `$and`, `$nor`, `$not`.
  - `$or` takes an array of independent query documents.
- **Key Mental Model:** Comparison operators are lenses inspecting a single field; Logical operators are circuit gates combining multiple lenses.
- **Common Trap:** Writing `{ $gt: { marks: 75 } }` instead of `{ marks: { $gt: 75 } }`.
- **Code Pattern:**
  ```javascript
  // Scored > 75 OR lives in Delhi
  db.student.find({
    $or: [
      { marks: { $gt: 75 } },
      { city: "Delhi" }
    ]
  })
  ```

---

## 11. 🌐 Real-World Production Scenario: E-Commerce Product Filtering

On any e-commerce site (Amazon, Flipkart, Myntra), the filter sidebar uses MongoDB query operators:

```javascript
// mongosh — "Show me Electronics between ₹1000 and ₹50000 with rating >= 4.0"
db.products.find({
  $and: [
    { category: "Electronics" },
    { price: { $gte: NumberDecimal("1000"), $lte: NumberDecimal("50000") } },
    { rating: { $gte: 4.0 } },
    { stock: { $gt: 0 } }  // Only show in-stock items
  ]
}).sort({ rating: -1 }).limit(20)

// ✅ This is exactly how Flipkart's "Price Range" + "Rating" + "Availability" filters work!
// ✅ $gte/$lte handle range sliders, $gt: 0 handles "in stock only" toggle
```

**More Real-World Filter Examples:**
```javascript
// 🛒 "Show products in categories: Laptops, Phones, or Tablets"
db.products.find({ category: { $in: ["Laptops", "Phones", "Tablets"] } })

// ⭐ "Show products NOT from banned sellers"
db.products.find({ sellerId: { $nin: ["banned-001", "banned-002"] } })

// 🔍 "Show products that are either on sale OR have free shipping"
db.products.find({
  $or: [
    { onSale: true },
    { freeShipping: true }
  ]
})

// 📊 "Show products where discount is NOT greater than 50%" (prevent scam listings)
db.products.find({ discount: { $not: { $gt: 50 } } })
```

---

## 12. 🚀 Advanced Preview: Aggregation Pipeline (Coming in Part 2)

Query operators are the foundation for MongoDB's **Aggregation Pipeline** — a powerful multi-stage data processing framework:

```javascript
// Preview: Aggregate students by city and compute average marks
db.student.aggregate([
  { $match: { marks: { $gte: 60 } } },     // Stage 1: Filter (uses query operators!)
  { $group: {                               // Stage 2: Group by city
      _id: "$city",
      avgMarks: { $avg: "$marks" },
      count: { $sum: 1 }
    }
  },
  { $sort: { avgMarks: -1 } },             // Stage 3: Sort by average marks
  { $project: {                             // Stage 4: Reshape output
      city: "$_id",
      avgMarks: { $round: ["$avgMarks", 1] },
      studentCount: "$count",
      _id: 0
    }
  }
])

// Output:
// [{ city: "Delhi", avgMarks: 79.5, studentCount: 2 },
//  { city: "Mumbai", avgMarks: 72.0, studentCount: 1 }]
```

**Key Insight:** The `$match` stage in aggregation uses the exact same query operator syntax (`$gt`, `$gte`, `$in`, `$or`) you learned in this episode!

---

## 13. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
1. In `mongosh`, execute:
   - Find all students where `marks > 75`.
   - Find all students where `marks >= 75`.
   - Find all students where `city` is in `["Delhi", "Mumbai"]`.
   - Find all students where `marks > 75` OR `city === "Delhi"`.
2. Write a range query returning students with marks strictly between 60 and 80 ($60 < \text{marks} < 80$).
3. Test the `$nor` operator: Find students who neither scored $> 75$ nor live in Delhi. (Donald should be the only result!).

### Interview Readiness Checklist
- [ ] Can you differentiate between comparison syntax and logical syntax?
- [ ] When is explicit `$and` strictly required in MongoDB queries?
- [ ] How does `$in` optimize queries compared to writing multiple `$or` clauses?
- [ ] Why does `$ne` / `$nin` generally perform poorly on large unindexed collections?
