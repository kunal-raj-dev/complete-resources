# Episode 06 — Querying Documents: db.collection.find vs findOne, Cursors, & Filtering

> **One-Line Mental Model:** `find()` returns a cursor pipeline (a stream pointer to all matching documents), whereas `findOne()` opens the valve just enough to return the first matching document directly as a raw BSON object.

---

## 📌 Source Metadata
> **Course:** Delta Batch (Web Development)  
> **Module:** 44. MongoDB (Part 1)  
> **Lecture:** 06. FIND in DB  
> **Duration:** 05:35  
> **Methods Explored:** `db.collection.find()`, `db.collection.findOne()`  
> **Status:** AUDITED & EXPANDED  

---

## 🎯 What You Will Learn

- How the **Read** operation fits into MongoDB's CRUD architecture.
- The fundamental difference between **`find()`** and **`findOne()`**.
- Understanding **Cursors**: how MongoDB streams data in batches of 20 documents and how to use the `it` iterator.
- Executing exact match equality queries: `db.collection.find({ key: value })`.
- Combining multiple query conditions for an **implicit AND** filter: `db.collection.find({ key1: val1, key2: val2 })`.
- Return type contracts: **Cursor Object** vs **Raw BSON Document (or `null`)**.
- Modern production techniques: **Projections** (including/excluding fields) and cursor chaining (`.limit()`, `.skip()`, `.sort()`).

---

## 1. The Idea in Simple Words

### Simple Explanation
Once you have saved documents into a MongoDB collection, you need a way to look them up:
- If you ask: *"Show me all students who live in Delhi"*, there could be 2 students, 200 students, or 2 million students. MongoDB uses **`find()`**, which gives you an active pointer (a **Cursor**) that scrolls through all matching results.
- If you ask: *"Find me the student named Adam"* or *"Get the first person from Delhi"*, you only want one specific record. MongoDB uses **`findOne()`**, which searches until it finds the very first match, hands you the single record, and immediately stops looking.

### Technical Explanation
- **`db.collection.find(filter, projection)`** queries the collection and returns a **`FindCursor`**. A cursor is a client-side pointer to the database query result set. Instead of loading an entire million-row result set into RAM at once, MongoDB streams documents from `mongod` in configurable batches (default batch size: 101 documents or 4MB on the wire; `mongosh` prints up to 20 documents by default).
- **`db.collection.findOne(filter, projection)`** executes a query that internally specifies a cursor limit of 1, reads the first document from the stream, and returns the deserialized BSON document directly. If no document matches the filter, `findOne()` returns `null`.

### Before vs After Motivation
- **Before (SQL `SELECT`):** `SELECT * FROM student WHERE city = 'Delhi';` always returns a tabular result set (even if only 1 row or 0 rows match).
- **After (MongoDB `find` & `findOne`):** Direct JavaScript object integration. `findOne()` gives you an object ready to use immediately (`const user = await User.findOne(...)`), and `find()` gives you an iterable stream that prevents memory overload.

---

## 2. 🧠 Mental Model: The Library Catalog vs The Book on the Desk

```
                     COLLECTION: `student`
       [Adam (Delhi)] [Bob (Delhi)] [Catlyn (Delhi)] [Donald (Mumbai)]
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
    db.student.find({ city: "Delhi" })   db.student.findOne({ city: "Delhi" })
            │                                 │
            ▼                                 ▼
     RETURNS A CURSOR                  RETURNS A DOCUMENT
   (Interactive Pointer)               (Direct BSON Object)
   ┌──────────────────────┐            ┌──────────────────────┐
   │ -> Match 1: Adam     │            │ {                    │
   │    Match 2: Bob      │            │   _id: ObjectId(...),│
   │    Match 3: Catlyn   │            │   name: "Adam",      │
   │                      │            │   city: "Delhi"      │
   │ (Type 'it' for more) │            │ }                    │
   └──────────────────────┘            └──────────────────────┘
```

---

## 3. Basic Syntax & Anatomy

```javascript
// 1. Find all documents in a collection (No filter)
db.collection.find()

// 2. Find all documents matching a filter
db.collection.find( { <field>: <value> } )

// 3. Find only the first matching document
db.collection.findOne( { <field>: <value> } )

// 4. Multi-field equality query (Implicit AND)
db.collection.find( { <field1>: <value1>, <field2>: <value2> } )

// 5. Query with Projection (1 = Include, 0 = Exclude)
db.collection.find( { <filter> }, { <field1>: 1, _id: 0 } )
```

---

## 4. Smallest Useful Example

Following the exact lecture progression on the `student` collection:

```javascript
// [1] Retrieve ALL documents currently in the collection
db.student.find()

// OUTPUT:
[
  { _id: ObjectId("64fec88c4d37352da5df8407"), name: 'adam', age: 19, marks: 88 },
  { _id: ObjectId("64fec9714d37352da5df8408"), name: 'bob', city: 'Delhi', marks: 75 },
  { _id: ObjectId("64fec9f54d37352da5df8409"), name: 'catlyn', marks: 64, city: 'Delhi' },
  { _id: ObjectId("64fec9f54d37352da5df840a"), name: 'donald', marks: 58, city: 'Mumbai' }
]

// [2] Query for students who live in Delhi using find()
db.student.find({ city: "Delhi" })

// OUTPUT: Returns BOTH Bob and Catlyn
[
  { _id: ObjectId("64fec9714d37352da5df8408"), name: 'bob', city: 'Delhi', marks: 75 },
  { _id: ObjectId("64fec9f54d37352da5df8409"), name: 'catlyn', marks: 64, city: 'Delhi' }
]

// [3] Query for students who live in Delhi using findOne()
db.student.findOne({ city: "Delhi" })

// OUTPUT: Returns ONLY Bob (the first match in natural storage order) as a raw object!
{
  _id: ObjectId("64fec9714d37352da5df8408"),
  name: 'bob',
  city: 'Delhi',
  marks: 75
}

// [4] Querying for a single unique document by name
db.student.findOne({ name: "adam" })

// OUTPUT:
{
  _id: ObjectId("64fec88c4d37352da5df8407"),
  name: 'adam',
  age: 19,
  marks: 88
}

// [5] Multi-condition query (Implicit AND: city is "Delhi" AND marks are 75)
db.student.find({ city: "Delhi", marks: 75 })

// OUTPUT:
[
  { _id: ObjectId("64fec9714d37352da5df8408"), name: 'bob', city: 'Delhi', marks: 75 }
]
```

---

## 5. What Just Happened?

```
Trace of `db.student.findOne({ city: "Delhi" })`:
         │
         ▼
[1] Client sends OP_MSG `find` command to mongod: { filter: { city: "Delhi" }, limit: 1 }.
         │
         ▼
[2] mongod query planner checks if an index exists on `city`.
    (No index found -> defaults to Collection Scan `COLLSCAN`).
         │
         ▼
[3] Storage engine reads documents sequentially:
    - Doc 1 (Adam): Has no city field -> Skip.
    - Doc 2 (Bob): city is "Delhi" -> MATCH FOUND!
         │
         ▼
[4] Because limit is 1, query executor halts scanning immediately!
         │
         ▼
[5] mongod serializes Bob's document into BSON and returns it to the client.
    Client receives the raw document (not a cursor).
```

---

## 6. Visual Explanation: Cursors and the `it` Iterator

When a query matches hundreds of documents, `mongosh` displays the first 20 records and pauses:

```
               COLLECTION SCAN MATCHES 150 DOCUMENTS
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
       FIRST BATCH (1 to 20)            REMAINING (21 to 150)
    Displayed immediately in shell         Held in server cursor
                 │                               │
                 ▼                               ▼
    Terminal displays:                  Type `it` in terminal
    "Type 'it' for more"          ───>  Fetches Next Batch (21 to 40)
```

In Node.js backend code, a cursor allows memory-efficient streaming:
```javascript
const cursor = db.collection('students').find();
for await (const doc of cursor) {
  console.log(doc.name); // Processed one document at a time without loading all into RAM!
}
```

---

## 7. Important Differences: `find()` vs `findOne()`

| Dimension | `db.collection.find()` | `db.collection.findOne()` |
| :--- | :--- | :--- |
| **Return Type** | `FindCursor` (Iterable stream) | Single BSON Document or `null` |
| **No Match Behavior**| Empty cursor (`[]` in shell) | Returns `null` |
| **Server Limit** | Unlimited (or user-defined limit) | Hardcoded `limit: 1` |
| **Shell Display** | Formatted array `[ { ... }, { ... } ]` | Formatted object `{ ... }` |
| **Backend Method Chaining**| Supports `.sort()`, `.limit()`, `.skip()` | Direct value (Cannot chain cursor methods) |
| **Primary Use Case** | Lists, searches, paginated feeds | Looking up a single user by ID/Email |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Attempting to call `.limit()` or `.sort()` on `findOne()`
```javascript
// ❌ CRASH:
db.student.findOne({ city: "Delhi" }).sort({ marks: -1 })
// TypeError: db.student.findOne(...).sort is not a function

// 🔍 WHY: `findOne()` returns a plain document object (or null), NOT a cursor!
// Only cursors have `.sort()`, `.limit()`, and `.skip()`.
// ✅ CORRECT (To get the top student in Delhi):
db.student.find({ city: "Delhi" }).sort({ marks: -1 }).limit(1)
```

### Mistake 2: Checking `find()` output for truthiness in backend JavaScript
```javascript
// ❌ DANGEROUS BUG IN NODE.JS BACKEND:
const users = await db.collection("users").find({ email: "test@example.com" });
if (users) {
  // BUG: A cursor object is ALWAYS truthy in JavaScript, even if 0 documents matched!
  console.log("User exists!"); 
}

// ✅ CORRECT:
const user = await db.collection("users").findOne({ email: "test@example.com" });
if (user) {
  console.log("User exists!"); // Executes only if document is not null
}
```

### Mistake 3: Forgetting case sensitivity in string queries
```javascript
// ❌ NO RESULTS:
db.student.find({ city: "delhi" }) // Returns []

// 🔍 WHY: String comparisons in BSON are strictly case-sensitive ("Delhi" !== "delhi")!
// ✅ FIX: Use exact case or a regex query:
db.student.find({ city: /^delhi$/i })
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** `findOne()` does not return an array with one element `[{...}]`—it returns the bare object `{...}` directly! 
> If nothing matches, `findOne()` returns `null`, while `find()` returns an empty cursor.

- **Q: Does `db.student.find({})` and `db.student.find()` do the exact same thing?**
  - *Click Answer:* Yes! Passing an empty filter object `{}` matches all documents in the collection, exactly like omitting the argument.
- **Q: How can I return only the `name` and `marks` fields and hide the `_id`?**
  - *Click Answer:* Use a **Projection**:
    `db.student.find({}, { name: 1, marks: 1, _id: 0 })`

---

## 10. ⚠️ Edge Cases & Exceptions

### Querying for Missing vs Null Fields
- `db.student.find({ age: null })` will match:
  1. Documents where `age` is explicitly set to `null` (`{ name: "foo", age: null }`).
  2. Documents that **do not have an `age` field at all** (like `bob`, `catlyn`, and `donald`)!
- If you strictly want documents that have the `age` field, use the `$exists` operator:
  `db.student.find({ age: { $exists: true } })`

---

## 11. 🔥 Interview Deep Dive

### Conceptual Reasoning: Cursors and Memory Leaks
**Q:** *What happens on the MongoDB server if an application opens a cursor with `find()` but never reads all the documents and forgets to close it?*

**Answer:**
To prevent memory exhaustion from orphaned client queries, MongoDB implements a **Cursor Idle Timeout**:
1. By default, any open server cursor that has not received a `getMore` request for **10 minutes** is automatically closed and reclaimed from memory by `mongod`.
2. In long-running background tasks (e.g. data migrations), developers can pass `.noCursorTimeout()` to prevent premature closure, but they must manually close the cursor in a `finally` block to avoid memory leaks.

---

## 🧠 What You Actually Need to Remember

1. **`find(filter)`** returns a **Cursor** to all matching records.
2. **`findOne(filter)`** returns the **First Document Object** or `null`.
3. **Empty filter `{}`** matches everything.
4. **Multiple fields `{ k1: v1, k2: v2 }`** acts as an implicit **AND**.
5. **Case Sensitivity:** Queries on string fields are case-sensitive by default.
6. **Cursor Batching:** Shell iterates in batches of 20 (`it` command).

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - Read all: `db.collection.find()`.
  - Filter: `db.collection.find({ field: value })`.
  - Read one: `db.collection.findOne({ field: value })`.
  - Empty result: `find()` returns `[]`, `findOne()` returns `null`.
- **Key Mental Model:** `find()` is a video stream; `findOne()` is a single snapshot photograph.
- **Common Trap:** Calling `.sort()` on `findOne()`.
- **Code Pattern:**
  ```javascript
  // Multi-condition query
  db.student.find({ city: "Delhi", marks: 75 })
  ```

---

## 12. 🌐 Real-World Production Scenario: REST API Search Endpoint

In a real Express.js REST API, `find` and `findOne` power search and detail endpoints:

```javascript
const express = require('express');
const mongoose = require('mongoose');
const app = express();

const Student = mongoose.model('Student', new mongoose.Schema({
  name:  { type: String, required: true },
  marks: Number,
  city:  String
}));

// GET /api/students — Uses find() with query parameters
app.get('/api/students', async (req, res) => {
  const { city, minMarks, page = 1, limit = 20 } = req.query;
  const filter = {};
  
  if (city) filter.city = city;                           // Equality filter
  if (minMarks) filter.marks = { $gte: Number(minMarks) }; // Comparison operator
  
  // ✅ Cursor-based pagination (equivalent of mongosh's `it` for more results)
  const students = await Student.find(filter)
    .select('name marks city -_id')   // Projection: include name, marks, city; exclude _id
    .sort({ marks: -1 })              // Sort by marks descending
    .skip((page - 1) * limit)         // Skip previous pages
    .limit(Number(limit));            // Limit results per page
  
  res.json(students);
});

// GET /api/students/:id — Uses findOne() (or findById)
app.get('/api/students/:id', async (req, res) => {
  // ✅ findById is a shorthand for findOne({ _id: id })
  const student = await Student.findById(req.params.id);
  
  if (!student) return res.status(404).json({ error: 'Student not found' });
  //  ↑ This is why findOne returns null (not an empty array) — easy null-check!
  
  res.json(student);
});
```

**Key Backend Patterns:**
- **Pagination:** `.skip()` + `.limit()` replaces `mongosh`'s `it` iterator for web apps.
- **Projection:** `.select('name marks -_id')` is the Mongoose equivalent of `find({}, { name: 1, marks: 1, _id: 0 })`.
- **404 Handling:** `findOne()` returning `null` makes it trivial to send HTTP 404 responses.

---

## 13. 🔗 Mongoose Bridge: find/findOne Chaining

| mongosh | Mongoose | Notes |
| :--- | :--- | :--- |
| `db.student.find()` | `await Student.find()` | Returns array (not cursor) in Mongoose |
| `db.student.find({ city: "Delhi" })` | `await Student.find({ city: 'Delhi' })` | Same filter syntax |
| `db.student.findOne({ name: "adam" })` | `await Student.findOne({ name: 'adam' })` | Returns object or `null` |
| `db.student.find({}, { name: 1, _id: 0 })` | `await Student.find().select('name -_id')` | Projection syntax |
| `db.student.find().sort({ marks: -1 })` | `await Student.find().sort({ marks: -1 })` | Identical chaining |
| `db.student.find().limit(5)` | `await Student.find().limit(5)` | Identical |
| `db.student.find().skip(20).limit(10)` | `await Student.find().skip(20).limit(10)` | Pagination |
| N/A (use `findById` with ObjectId) | `await Student.findById(id)` | Mongoose-only shorthand |

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
1. In `mongosh`, run `db.student.find()` to see all students.
2. Run `db.student.find({ city: "Delhi" })` and verify both Bob and Catlyn appear.
3. Run `db.student.findOne({ city: "Delhi" })` and verify only Bob appears as a plain object.
4. Test a non-existent match: `db.student.findOne({ name: "nonexistent" })` and confirm it logs `null`.
5. Execute a projection query showing only names: `db.student.find({}, { name: 1, _id: 0 })`.

### Interview Readiness Checklist
- [ ] What is a Cursor in MongoDB and why doesn't `find()` return an array of all records at once?
- [ ] What is the return value of `findOne()` when no documents match?
- [ ] How does `find({ city: "Delhi", marks: 75 })` evaluate multiple criteria?
- [ ] What is the difference between `{ field: 1 }` and `{ field: 0 }` in a query projection?
