# Episode 08 — Modifying Documents: updateOne, updateMany, replaceOne, & Field Update Operators

> **One-Line Mental Model:** `updateOne` with `$set` performs targeted surgical alterations on specific fields without touching the rest of the document, whereas `replaceOne` tears down the entire existing document and replaces it with a new one while preserving only the immutable `_id`.

---

## 📌 Source Metadata
> **Course:** Delta Batch (Web Development)  
> **Module:** 44. MongoDB (Part 1)  
> **Lecture:** 08. UPDATE in DB  
> **Duration:** 07:20  
> **Methods Explored:** `db.collection.updateOne()`, `db.collection.updateMany()`, `db.collection.replaceOne()`  
> **Operators Explored:** `$set`, `$unset`, `$inc`, `$rename`, `$currentDate`  
> **Status:** AUDITED & EXPANDED  

---

## 🎯 What You Will Learn

- How the **Update** operation fits into MongoDB's CRUD lifecycle.
- The syntax contract: `db.collection.update*(<filter>, <update>, <options>)`.
- Why update operators (like **`$set`**) are strictly mandatory and what happens if you omit them.
- Updating a single record with **`updateOne()`** and inspecting `matchedCount` vs `modifiedCount`.
- Updating multiple matching documents in batch using **`updateMany()`**.
- The distinct behavior of **`replaceOne()`**: completely swapping a document's body while preserving its immutable `_id`.
- Essential production update operators: `$set`, `$unset`, `$inc`, `$min`, `$max`, `$rename`, and `$currentDate`.
- The **Upsert Pattern (`{ upsert: true }`)**: atomic check-and-insert/update.

---

## 1. The Idea in Simple Words

### Simple Explanation
Imagine you have a student named Adam who took a re-test and his marks changed from `88` to `99`:
- You do **not** want to delete Adam and re-type his entire profile.
- You do **not** want to accidentally wipe out his `age`, `email`, or enrollment details.
- You only want to change his `marks` field.

To do this, MongoDB provides **`updateOne()`** combined with the **`$set`** operator. `$set` acts like a surgeon's scalpel: it changes only the specific fields you target and leaves all other fields completely untouched.

If you want to update everyone from Delhi to "New Delhi", you use **`updateMany()`**. And if you want to scrap an entire record and replace it with new information while keeping the same ID card number, you use **`replaceOne()`**.

### Technical Explanation
MongoDB updates are atomic at the document level. Update commands require two primary arguments:
1. **Filter (Query):** Specifies which document(s) to target.
2. **Update Specification:** Declares the mutations to apply. In modern MongoDB, this must be an update operator document (e.g. `{ $set: { ... } }`) or an aggregation pipeline. Passing a raw document without operators is rejected by `updateOne` and `updateMany` to protect against accidental document overwrite.

The operation returns an acknowledgment containing:
- `matchedCount`: How many documents matched the filter criteria.
- `modifiedCount`: How many documents were actually altered on disk (if a document already had `marks: 99`, `matchedCount` is 1, but `modifiedCount` is 0!).
- `upsertedCount`: How many new documents were inserted via an upsert.

---

## 2. 🧠 Mental Model: The Surgeon ($set) vs The Demolition Crew (replaceOne)

```
ORIGINAL DOCUMENT:
{ _id: 101, name: "bob", city: "Delhi", marks: 75 }

CASE A: db.student.updateOne({ name: "bob" }, { $set: { city: "New Delhi" } })
┌────────────────────────────────────────────────────────┐
│ Surgeon ($set) modifies ONLY the targeted property:    │
│ { _id: 101, name: "bob", city: "New Delhi", marks: 75 }│
└────────────────────────────────────────────────────────┘

CASE B: db.student.replaceOne({ name: "bob" }, { name: "shradha", state: "Haryana" })
┌────────────────────────────────────────────────────────┐
│ Demolition (replaceOne) wipes out the entire body!     │
│ { _id: 101, name: "shradha", state: "Haryana" }        │
│ (The original marks and city are completely gone!)     │
└────────────────────────────────────────────────────────┘
```

---

## 3. Basic Syntax & Anatomy

```javascript
// 1. Update at most a single matching document
db.collection.updateOne(
  <filter>,     // Criteria to select the document
  <update>,     // Update operators and fields to change
  <options>     // Optional: { upsert: boolean, writeConcern: document }
)

// 2. Update all matching documents
db.collection.updateMany(
  <filter>,
  <update>,
  <options>
)

// 3. Completely replace a single document's content
db.collection.replaceOne(
  <filter>,
  <replacementDocument>,
  <options>
)
```

### Return Object Structure

```javascript
{
  acknowledged: true,
  insertedId: null,   // Populated with ObjectId only if an upsert occurred
  matchedCount: 1,    // Number of documents matching the filter
  modifiedCount: 1,   // Number of documents actually modified
  upsertedCount: 0    // Number of documents inserted via upsert
}
```

---

## 4. Step-by-Step Lecture Walkthrough

### 🎯 Step 1: Update a single document using `updateOne`
**Goal:** Update Adam's marks from `88` to `99`.

```javascript
// Execute updateOne with $set:
db.student.updateOne(
  { name: "adam" },
  { $set: { marks: 99 } }
)

// OUTPUT:
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}

// Verify with find():
db.student.find({ name: "adam" })
// Adam's marks are now 99! His age (19) remains perfectly preserved!
```

---

### 🎯 Step 2: Update multiple documents using `updateMany`
**Goal:** Rename `"Delhi"` to `"New Delhi"` for all students residing in Delhi.

```javascript
// Bob and Catlyn both live in "Delhi"
db.student.updateMany(
  { city: "Delhi" },
  { $set: { city: "New Delhi" } }
)

// OUTPUT:
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 2,
  modifiedCount: 2,
  upsertedCount: 0
}

// Verify with find():
db.student.find()
// Both Bob and Catlyn now have city: "New Delhi"!
```

---

### 🎯 Step 3: Replace an entire document using `replaceOne`
**Goal:** Replace Bob's document entirely with a new student profile: Shradha from Haryana.

```javascript
// Replace Bob's document:
db.student.replaceOne(
  { name: "bob" },
  { name: "shradha", marks: 94, state: "Haryana" }
)

// OUTPUT:
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}

// Inspect the result in db.student.find():
[
  {
    _id: ObjectId("64fec88c4d37352da5df8407"),
    name: 'adam',
    age: 19,
    marks: 99
  },
  {
    _id: ObjectId("64fec9714d37352da5df8408"), // <-- ORIGINAL _id of Bob is PRESERVED!
    name: 'shradha',
    marks: 94,
    state: 'Haryana'                            // <-- City: "New Delhi" is completely gone!
  },
  {
    _id: ObjectId("64fec9f54d37352da5df8409"),
    name: 'catlyn',
    marks: 64,
    city: 'New Delhi'
  },
  {
    _id: ObjectId("64fec9f54d37352da5df840a"),
    name: 'donald',
    marks: 58,
    city: 'Mumbai'
  }
]
```

---

## 5. The Core Update Operators Matrix

MongoDB provides powerful field modifiers beyond `$set`:

| Operator | Function | Example Syntax | Result |
| :--- | :--- | :--- | :--- |
| **`$set`** | Sets field value (creates field if absent). | `{ $set: { grade: "A+" } }` | Adds or updates `grade` to `"A+"`. |
| **`$unset`** | Deletes a field from the document. | `{ $unset: { age: "" } }` | The `age` key is deleted from the BSON document. |
| **`$inc`** | Increments a number by a relative amount. | `{ $inc: { marks: 5 } }` | Adds 5 to existing marks (e.g. 94 $\to$ 99). |
| **`$min`** | Updates only if the new value is less. | `{ $min: { lowestScore: 50 } }`| Updates if existing lowestScore > 50. |
| **`$max`** | Updates only if the new value is greater.| `{ $max: { highScore: 100 } }` | Updates if existing highScore < 100. |
| **`$rename`**| Renames a field key in place. | `{ $rename: { "state": "province" } }`| Renames field `state` $\to$ `province`. |
| **`$currentDate`**| Sets a field to current date/timestamp.| `{ $currentDate: { updatedAt: true } }`| Updates `updatedAt` to current `ISODate()`. |

### Practical Code Examples: `$inc` and `$unset`

```javascript
// Give 2 bonus marks to Shradha:
db.student.updateOne(
  { name: "shradha" },
  { $inc: { marks: 2 } }
)
// Marks become 94 + 2 = 96!

// Remove the `state` field completely from Shradha:
db.student.updateOne(
  { name: "shradha" },
  { $unset: { state: "" } }
)
// Document now only has _id, name, and marks.
```

---

## 6. 🔥 The Upsert Pattern: `{ upsert: true }`

In web backend applications (like user profiles or shopping carts), you frequently encounter this workflow:
*"If the user setting exists, update it. If it doesn't exist yet, create it!"*

In traditional SQL, this requires complex `INSERT ... ON DUPLICATE KEY UPDATE` syntax.
In MongoDB, simply append `{ upsert: true }`:

```javascript
db.student.updateOne(
  { name: "emma" },           // Filter: No student named "emma" exists!
  { $set: { marks: 91, city: "London" } },
  { upsert: true }            // Option
)

// OUTPUT:
{
  acknowledged: true,
  insertedId: ObjectId("64fecd1234567890abcdef12"), // New document created!
  matchedCount: 0,
  modifiedCount: 0,
  upsertedCount: 1
}
```

---

## 7. Important Differences: `updateOne` vs `replaceOne`

| Feature | `updateOne` with `$set` | `replaceOne` |
| :--- | :--- | :--- |
| **Operation Type** | Field-level partial modification | Full-document structural replacement |
| **Update Operators** | **Mandatory** (`$set`, `$inc`, etc.) | **Forbidden** (Expects plain document) |
| **Untargeted Fields** | Fully preserved | Completely deleted |
| **`_id` Behavior** | Preserved | Preserved (Immutable) |
| **Use Case** | Updating password, score, email | Form resubmission replacing entire record |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Omitting `$set` in `updateOne`
```javascript
// ❌ CRASH:
db.student.updateOne(
  { name: "adam" },
  { marks: 99 } // Missing $set!
)

// 🔍 WHY: MongoDB requires an update operator to prevent accidental replacement!
// MongoInvalidArgumentError: Update document requires atomic operators

// ✅ CORRECT:
db.student.updateOne(
  { name: "adam" },
  { $set: { marks: 99 } }
)
```

### Mistake 2: Confusing `matchedCount` with `modifiedCount`
```javascript
// Suppose Adam already has marks: 99
db.student.updateOne({ name: "adam" }, { $set: { marks: 99 } })

// Return:
{ matchedCount: 1, modifiedCount: 0 }
// 🔍 WHY: MongoDB is smart! It checks if the new value equals the existing value.
// If identical, it skips the expensive disk write!
// matchedCount = 1 (found him), modifiedCount = 0 (no disk write needed).
```

### Mistake 3: Trying to change the `_id` field in an update
```javascript
// ❌ FATAL ERROR:
db.student.updateOne({ name: "adam" }, { $set: { _id: 999 } })

// 🔍 WHY: The `_id` field is strictly immutable once written.
// MongoServerError: Performing an update on the path '_id' would modify the immutable field '_id'
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** If `$set` targets a field that **does not exist**, MongoDB doesn't throw an error—it dynamically creates the new field on that specific document!

- **Q: Does `updateOne()` throw an error if no documents match the filter?**
  - *Click Answer:* No. It simply returns `{ matchedCount: 0, modifiedCount: 0 }`.
- **Q: How does `updateMany({}, { $set: { status: "Active" } })` behave?**
  - *Click Answer:* Because the filter `{}` is empty, it adds `status: "Active"` to **every single document** in the entire collection!

---

## 10. 🔥 Interview Deep Dive

### Conceptual Reasoning: Idempotency in Database Updates
**Q:** *What is an Idempotent update operation and why is `$set` idempotent while `$inc` is not?*

**Answer:**
An operation is **idempotent** if applying it multiple times produces the exact same system state as applying it once ($f(f(x)) = f(x)$).
- **`$set: { marks: 99 }` is Idempotent:** If a network timeout occurs and your backend server retries the update 5 times, `marks` will still be `99`.
- **`$inc: { marks: 2 }` is NOT Idempotent:** If your backend retries the request 5 times due to a dropped connection, marks will increase by $2 \times 5 = +10$! In distributed networks, non-idempotent operations require idempotency keys or unique transaction IDs.

---

## 🧠 What You Actually Need to Remember

1. **`updateOne(filter, { $set: { ... } })`** updates at most 1 matching document.
2. **`updateMany(filter, { $set: { ... } })`** updates all matching documents.
3. **`$set` is mandatory** for partial updates; omitting it throws an error.
4. **`replaceOne(filter, newDoc)`** replaces the document body while keeping `_id`.
5. **`matchedCount` vs `modifiedCount`:** `modifiedCount` is 0 if field value was already identical.
6. **`{ upsert: true }`** inserts a new document if no filter match is found.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - `updateOne`: First match only.
  - `updateMany`: All matches.
  - `replaceOne`: Full document swap (keeps `_id`).
  - `$set`: Add or modify field.
  - `$unset`: Delete field.
  - `$inc`: Mathematical relative increment/decrement.
  - Option `{ upsert: true }`: Update or insert.
- **Key Mental Model:** `$set` is a precision scalpel modifying specific cells; `replaceOne` is a bulldozer clearing the lot while keeping the street address (`_id`).
- **Common Trap:** Omitting `$set` in `updateOne` or trying to update `_id`.
- **Code Pattern:**
  ```javascript
  db.student.updateOne(
    { name: "adam" },
    { $set: { marks: 99 } }
  )
  ```

---

## 11. 🌐 Real-World Production Scenario: User Profile Updates & Shopping Cart

In production apps, update operations handle critical business logic:

```javascript
// 👤 User Profile Update (Settings Page)
// When a user changes their display name and bio from their profile settings:
db.users.updateOne(
  { _id: ObjectId("64fec88c4d37352da5df8407") },
  {
    $set: {
      displayName: "Kunal Raj Dev",
      bio: "Full-stack developer | Building cool stuff",
      "settings.theme": "dark"    // Dot notation for nested update!
    },
    $currentDate: { updatedAt: true }  // Timestamp the modification
  }
)

// 🛒 Shopping Cart: Increment Item Quantity
// When a user clicks "+1" on a cart item:
db.carts.updateOne(
  { userId: ObjectId("64fec88c..."), "items.productId": ObjectId("64fed571...") },
  { $inc: { "items.$.quantity": 1 } }  // $ is the positional operator for array elements
)

// 🔐 Login Tracking: Upsert Pattern
// Record login activity — create if first login, update if returning:
db.loginActivity.updateOne(
  { userId: ObjectId("64fec88c..."), date: new Date().toISOString().split('T')[0] },
  {
    $inc: { loginCount: 1 },
    $set: { lastLoginAt: new Date() },
    $setOnInsert: { firstLoginAt: new Date() }  // Only set on insert, not on update!
  },
  { upsert: true }
)
```

---

## 12. 🔗 Mongoose Bridge: Update Operations in Node.js

```javascript
const User = mongoose.model('User', userSchema);

// ✅ updateOne equivalent:
await User.updateOne(
  { email: 'kunal@example.com' },
  { $set: { displayName: 'Kunal Raj Dev' } }
);

// ✅ findOneAndUpdate — Returns the UPDATED document (most common in APIs!):
const updatedUser = await User.findOneAndUpdate(
  { email: 'kunal@example.com' },
  { $set: { bio: 'Building cool stuff' } },
  { new: true }  // ✅ Return the document AFTER update (default returns BEFORE)
);
res.json(updatedUser);  // Send updated profile back to frontend

// ✅ updateMany equivalent:
await User.updateMany(
  { role: 'user' },
  { $set: { 'settings.notifications': true } }
);

// ✅ Upsert in Mongoose:
await User.updateOne(
  { email: 'new@user.com' },
  { $set: { displayName: 'New User', role: 'user' } },
  { upsert: true }
);
```

| mongosh | Mongoose | Key Difference |
| :--- | :--- | :--- |
| `updateOne(filter, update)` | `Model.updateOne(filter, update)` | Same syntax |
| `updateMany(filter, update)` | `Model.updateMany(filter, update)` | Same syntax |
| `replaceOne(filter, doc)` | `Model.replaceOne(filter, doc)` | Same syntax |
| N/A | `Model.findOneAndUpdate(filter, update, { new: true })` | Returns updated doc — most used in APIs! |
| N/A | `Model.findByIdAndUpdate(id, update, { new: true })` | Shorthand for findOneAndUpdate with `_id` |

---

## 13. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
1. In `mongosh`, execute:
   - Update Adam's marks to 99 using `updateOne`.
   - Update all students living in "Delhi" to "New Delhi" using `updateMany`.
   - Replace Bob's document entirely with `{ name: "shradha", marks: 94, state: "Haryana" }` using `replaceOne`.
2. Give Shradha 2 bonus marks using `{ $inc: { marks: 2 } }`.
3. Remove the `state` field using `{ $unset: { state: "" } }`.
4. Test an upsert: update a student named `"albus"` with `marks: 100` and `{ upsert: true }`.

### Interview Readiness Checklist
- [ ] Why does `updateOne()` require `$set` instead of accepting a plain object?
- [ ] What is the difference between `matchedCount` and `modifiedCount`?
- [ ] What happens to fields not mentioned in a `replaceOne()` call?
- [ ] What is an upsert and when should it be used?
