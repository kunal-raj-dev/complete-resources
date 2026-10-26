# Episode 05 — Inserting Data (Part 2): db.collection.insertMany, Bulk Writes, & Ordered Semantics

> **One-Line Mental Model:** `insertMany()` is a bulk freight train that bundles an array of documents into a single network payload, saving hundreds of round-trip network hops compared to calling `insertOne()` in a loop.

---

## 📌 Source Metadata
> **Course:** Delta Batch (Web Development)  
> **Module:** 44. MongoDB (Part 1)  
> **Lecture:** 05. INSERT in DB (InsertMany)  
> **Duration:** 01:47  
> **Method Explored:** `db.collection.insertMany([<doc1>, <doc2>, ...], <options>)`  
> **Status:** AUDITED & EXPANDED  

---

## 🎯 What You Will Learn

- How to insert multiple documents simultaneously using **`db.collection.insertMany()`**.
- The syntax requirement of wrapping documents in a **JavaScript Array (`[...]`)**.
- Inspecting the bulk response payload: `{ acknowledged: true, insertedIds: { '0': ..., '1': ... } }`.
- Performance mechanics: **Network Round-Trip Latency** (`insertMany` vs looped `insertOne`).
- The critical production concept of **Ordered (`ordered: true`) vs Unordered (`ordered: false`)** bulk execution.
- How MongoDB handles partial failures, duplicate key exceptions, and rollback behavior during bulk writes.

---

## 1. The Idea in Simple Words

### Simple Explanation
Suppose a school admits 100 new students. 
- You *could* walk to the registrar's office, hand them 1 form, walk back, walk there again with form 2, and repeat that 100 times. That is what running `insertOne()` inside a JavaScript `for` loop does. Every single student requires a separate network round-trip across your local network or the internet.
- Or, you could take all 100 student forms, put them into a single envelope (`[form1, form2, ...]`), and deliver them in one trip. 

That is **`insertMany()`**. You pass an array of documents, and MongoDB inserts all of them in a single bulk operation.

### Technical Explanation
`db.collection.insertMany()` takes an array of BSON documents and sends them to the `mongod` server as a single bulk write command (`insert`). 

Internally, MongoDB splits large arrays into discrete write batches (limited to 100,000 operations or 48MB per batch). The server processes the documents sequentially or in parallel depending on the `ordered` flag, allocates individual `ObjectId`s for any documents lacking an `_id`, writes them to the journal, and returns an indexed map of all generated `insertedIds`.

### Before vs After Motivation
- **Before (`for` loop with `insertOne`):** High network latency overhead, high CPU serialization churn on the server, and slow bulk imports.
- **After (`insertMany`):** Optimal network throughput, sub-millisecond multi-document ingestion, and granular control over error recovery strategies.

---

## 2. 🧠 Mental Model: The Individual Couriers vs The Cargo Freight

```
LOOPED insertOne (100 Network Round-Trips):
Client ──[Doc 1]──> mongod (Wait for Ack)
Client <──[Ack 1]── mongod
Client ──[Doc 2]──> mongod (Wait for Ack)
Client <──[Ack 2]── mongod
... (100 times! High Network Latency!)

BULK insertMany (1 Single Network Round-Trip):
Client ──[ Doc 1, Doc 2, Doc 3, ..., Doc 100 ]──> mongod
Client <──[ Ack with insertedIds map {0: id, 1: id...} ]── mongod
```

---

## 3. Basic Syntax & Anatomy

```javascript
db.collection.insertMany(
  [ <document 1>, <document 2>, ... ], // (Required): Array of BSON documents
  {
    writeConcern: <document>,          // (Optional): Write acknowledgement level
    ordered: <boolean>                 // (Optional): Default: true
  }
)
```

### Return Payload Structure
Unlike `insertOne` which returns a single `insertedId`, `insertMany` returns a dictionary/map of `insertedIds` where keys represent the **zero-based array indices** of the input documents:

```javascript
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("64fec9f54d37352da5df8409"),
    '1': ObjectId("64fec9f54d37352da5df840a")
  }
}
```

---

## 4. Smallest Useful Example

Following the exact lecture implementation:

```javascript
// [1] Ensure you are inside the `college` database
use college

// [2] Bulk insert two new students: "catlyn" and "donald"
db.student.insertMany([
  { name: "catlyn", marks: 64, city: "Delhi" },
  { name: "donald", marks: 58, city: "Mumbai" }
])

// OUTPUT:
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("64fec9f54d37352da5df8409"),
    '1': ObjectId("64fec9f54d37352da5df840a")
  }
}

// [3] Verify the full collection state
db.student.find()

// OUTPUT:
[
  {
    _id: ObjectId("64fec88c4d37352da5df8407"),
    name: 'adam',
    age: 19,
    marks: 88
  },
  {
    _id: ObjectId("64fec9714d37352da5df8408"),
    name: 'bob',
    city: 'Delhi',
    marks: 75
  },
  {
    _id: ObjectId("64fec9f54d37352da5df8409"),
    name: 'catlyn',
    marks: 64,
    city: 'Delhi'
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

## 5. What Just Happened?

```
[1] User enters `db.student.insertMany([ {...}, {...} ])`.
         │
         ▼
[2] mongosh verifies the first argument is a genuine Array.
    (If not an array, throws TypeError immediately without sending network packet).
         │
         ▼
[3] Client generates ObjectIds for index 0 ("catlyn") and index 1 ("donald").
         │
         ▼
[4] Array is serialized into a single BSON payload and transmitted across socket 27017.
         │
         ▼
[5] mongod receives the batch, writes both records into the `student` collection,
    and returns a BulkWriteResult with `{ acknowledged: true, insertedIds: { '0': ..., '1': ... } }`.
```

---

## 6. 🔥 The Critical Industry Concept: `ordered: true` vs `ordered: false`

The optional `ordered` boolean is one of the most frequently tested MongoDB interview topics:

```
              ┌────────────────────────────────────────────────────────┐
              │ BATCH TO INSERT: [Doc 0 (OK), Doc 1 (DUPLICATE KEY!),  │
              │                   Doc 2 (OK), Doc 3 (OK)]              │
              └────────────────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
            ORDERED: TRUE (Default)                       ORDERED: FALSE
                    │                                             │
      - Inserts Doc 0 (Success)                     - Inserts Doc 0 (Success)
      - Attempts Doc 1 -> FAILS (E11000)            - Attempts Doc 1 -> FAILS (Recorded)
      - IMMEDIATELY ABORTS!                         - CONTINUES EXECUTION!
      - Doc 2 and Doc 3 are NEVER inserted!         - Inserts Doc 2 (Success)
                                                    - Inserts Doc 3 (Success)
```

### Code Demonstration: Ordered vs Unordered

```javascript
// Suppose we have an existing document: { _id: 1, name: "Existing" }

// CASE 1: Default (ordered: true)
db.items.insertMany(
  [
    { _id: 2, name: "Item 2" },
    { _id: 1, name: "Duplicate Item 1" }, // <-- FAILS HERE!
    { _id: 3, name: "Item 3" }
  ]
)
// Result: Item 2 is saved. Operation crashes on Item 1. Item 3 is NEVER processed!

// CASE 2: Unordered (ordered: false)
db.items.insertMany(
  [
    { _id: 20, name: "Item 20" },
    { _id: 1, name: "Duplicate Item 1" }, // <-- FAILS HERE!
    { _id: 30, name: "Item 30" }
  ],
  { ordered: false }
)
// Result: Item 20 and Item 30 ARE SAVED! The error for Item 1 is reported in the summary.
```

---

## 7. Important Differences: `insertOne` vs `insertMany`

| Feature | `db.collection.insertOne()` | `db.collection.insertMany()` |
| :--- | :--- | :--- |
| **Input Argument** | Single Object `{}` | Array of Objects `[ {}, {} ]` |
| **Return Field** | `insertedId` (Single value) | `insertedIds` (Key-value map: index $\to$ id) |
| **Network Payload** | 1 Document per TCP request | $N$ Documents bundled per TCP request |
| **`ordered` Option** | N/A (Only 1 document) | Yes (`ordered: true` / `ordered: false`) |
| **Best Used For** | User signup, single form submit | CSV/JSON data seeds, log batch ingestion |

---

## 8. Common Mistakes & Anti-Patterns

### Mistake 1: Forgetting the outer Array brackets `[...]`
```javascript
// ❌ SYNTAX ERROR / CRASH:
db.student.insertMany({ name: "catlyn" }, { name: "donald" })

// 🔍 WHY: `insertMany` expects the documents to be inside an array!
// Passing multiple arguments causes MongoDB to treat argument 2 as options!
// MongoArgumentError: Argument "docs" must be an array of documents

// ✅ CORRECT:
db.student.insertMany([ { name: "catlyn" }, { name: "donald" } ])
```

### Mistake 2: Expecting full rollback on error (MongoDB is NOT relational by default)
```javascript
// ❌ WRONG ASSUMPTION:
// "If insertMany fails on document 5 of 10, the first 4 will be rolled back like SQL."

// 🔍 WHY: Unless wrapped in an explicit multi-document ACID transaction,
// MongoDB does NOT roll back prior successful writes! Documents 0 through 4 remain saved!
```

---

## 9. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** `insertMany` does not mean "transaction". 
> Documents that succeed before a failure remain in the database unless you explicitly roll them back inside a session transaction.

- **Q: Does `insertMany([])` (an empty array) throw an error?**
  - *Click Answer:* No. It simply returns `{ acknowledged: true, insertedIds: {} }` without writing anything to disk.
- **Q: Is there a maximum size for the array in `insertMany`?**
  - *Click Answer:* Yes. MongoDB drivers limit individual batch payloads to 100,000 documents or 48 megabytes. If your array exceeds this, modern drivers automatically split it into multiple consecutive bulk writes.

---

## 10. ⚠️ Edge Cases & Exceptions

### Inserting an Array of Custom `_id`s with Duplicate Keys
If you pass `{ ordered: false }` and 3 out of 100 documents have duplicate `_id` values:
- Exactly 97 documents are successfully written.
- MongoDB returns a `BulkWriteError` containing an array of the 3 failed operations with their respective indices and error codes.

---

## 11. 🔥 Interview Deep Dive

### Conceptual Reasoning: Network Latency Calculations
**Q:** *Why is inserting 10,000 documents via `insertMany` up to 100x faster than calling `insertOne` in a `for` loop?*

**Answer:**
Let network latency between application server and database server be $L = 5\text{ ms}$.
- **Looped `insertOne`:** 10,000 sequential operations $\times 5\text{ ms} = 50,000\text{ ms} = \mathbf{50\text{ seconds}}$ spent purely waiting on network packet travel, regardless of database speed!
- **Bulk `insertMany`:** 10,000 documents batched into a single TCP connection payload: $1 \times 5\text{ ms} = \mathbf{5\text{ ms}}$ network latency. The database writes them to memory concurrently in a fraction of a second.

---

## 🧠 What You Actually Need to Remember

1. **`db.collection.insertMany([doc1, doc2])`** requires an **array** of documents.
2. **Bulk Response:** Returns `{ acknowledged: true, insertedIds: { '0': id, '1': id } }`.
3. **Ordered Semantics:** `ordered: true` stops at the first failure; `ordered: false` attempts all documents.
4. **No Automatic Rollback:** Partial writes remain in the database unless using explicit multi-document transactions.
5. **Efficiency:** Drastically reduces network round-trip overhead.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - Signature: `db.collection.insertMany([ { ... }, { ... } ])`.
  - Always wrap objects inside brackets `[...]`.
  - Keys in `insertedIds` represent array indices (`0`, `1`, `2`).
  - Use `{ ordered: false }` when you want valid documents to be inserted even if some fail.
- **Key Mental Model:** A shipping container packing all your documents into a single truckload instead of sending a courier for each envelope.
- **Common Trap:** Omitting the outer `[...]` brackets.
- **Code Pattern:**
  ```javascript
  db.student.insertMany([
    { name: "catlyn", marks: 64, city: "Delhi" },
    { name: "donald", marks: 58, city: "Mumbai" }
  ])
  ```

---

## 12. 🌐 Real-World Production Scenario: Seeding a Database from CSV/JSON

In production, `insertMany` is the backbone of data migration, CSV imports, and database seeding:

```javascript
// mongosh — Seeding an e-commerce product catalog:
db.products.insertMany([
  { sku: "LAPTOP-001", name: "Dell XPS 15",      price: NumberDecimal("89999.99"), category: "Electronics", stock: 45, rating: 4.5, createdAt: new Date() },
  { sku: "PHONE-002",  name: "iPhone 15 Pro",    price: NumberDecimal("134900.00"), category: "Electronics", stock: 120, rating: 4.8, createdAt: new Date() },
  { sku: "BOOK-003",   name: "Clean Code",       price: NumberDecimal("499.00"),    category: "Books",       stock: 500, rating: 4.6, createdAt: new Date() },
  { sku: "SHIRT-004",  name: "Nike Dri-FIT Tee", price: NumberDecimal("1995.00"),   category: "Clothing",    stock: 200, rating: 4.2, createdAt: new Date() },
  { sku: "HEADPH-005", name: "Sony WH-1000XM5",  price: NumberDecimal("29990.00"),  category: "Electronics", stock: 75,  rating: 4.9, createdAt: new Date() }
], { ordered: false })

// ✅ ordered: false ensures all valid products are inserted even if one SKU is a duplicate
// ✅ NumberDecimal for prices prevents floating-point rounding bugs
// ✅ Single network round-trip for all 5 products (instead of 5 separate TCP calls)
```

**Windows Tip — Import from JSON file using `mongoimport`:**
```powershell
# Import a JSON file directly into MongoDB (Windows PowerShell):
mongoimport --db college --collection students --file C:\data\students.json --jsonArray

# Import a CSV file:
mongoimport --db college --collection students --type csv --headerline --file C:\data\students.csv
```

---

## 13. 🔗 Mongoose Bridge: `insertMany` in Node.js

```javascript
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  sku:      { type: String, required: true, unique: true },
  name:     { type: String, required: true },
  price:    { type: mongoose.Schema.Types.Decimal128, required: true },
  category: { type: String, enum: ['Electronics', 'Books', 'Clothing', 'Home'], required: true },
  stock:    { type: Number, default: 0, min: 0 },
  rating:   { type: Number, min: 0, max: 5 }
}, { timestamps: true });

const Product = mongoose.model('Product', productSchema);

// ✅ Equivalent of db.products.insertMany([...]):
try {
  const products = await Product.insertMany([
    { sku: 'LAPTOP-001', name: 'Dell XPS 15', price: '89999.99', category: 'Electronics', stock: 45 },
    { sku: 'PHONE-002', name: 'iPhone 15 Pro', price: '134900.00', category: 'Electronics', stock: 120 }
  ], { ordered: false });  // ordered: false works in Mongoose too!
  
  console.log(`Inserted ${products.length} products`);
} catch (err) {
  // With ordered: false, some docs may succeed even if others fail
  console.error('Bulk write errors:', err.writeErrors?.length);
}
```

---

## 14. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
1. In `mongosh`, execute `use college`.
2. Insert `"catlyn"` and `"donald"` using `db.student.insertMany(...)`.
3. Test the `{ ordered: false }` behavior by inserting an array where one document intentionally contains a duplicate `_id`:
   ```javascript
   db.student.insertMany(
     [
       { _id: 500, name: "Test A" },
       { _id: 500, name: "Test Duplicate" },
       { _id: 501, name: "Test B" }
     ],
     { ordered: false }
   )
   ```
4. Query `db.student.find({ _id: { $in: [500, 501] } })` to confirm `Test A` and `Test B` were saved despite the error.

### Interview Readiness Checklist
- [ ] What is the difference between `ordered: true` and `ordered: false` in `insertMany`?
- [ ] What data structure does `insertedIds` return?
- [ ] What happens to previously inserted documents if document #4 in an ordered `insertMany` fails?
