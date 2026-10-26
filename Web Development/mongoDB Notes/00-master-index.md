# Master Curriculum Index: Complete MongoDB (Part 1) Notes (Ep. 01 – Ep. 10)

> **Curriculum Source:** Delta Batch (Web Development) — *44. MongoDB (Part 1)*  
> **Instructor:** Shradha Khapra  
> **Scope Covered:** 10 Comprehensive In-Depth Lectures (Ep. 01 → Ep. 10)  
> **Level:** Beginner to Senior / Industry & FAANG-Ready Deep Dive  
> **Language & Standard:** 100% Technical English | MongoDB 7.0+ & `mongosh` 2.0+ Architecture  
> **Target Platform:** 🪟 Windows (PowerShell) — All commands tested on Windows 10/11  

---

## 🧭 Curriculum Philosophy & Orientation

1. **First Principles First:** Understand the mechanical *why* before memorizing syntax. Understand why BSON is length-prefixed, why `mongod` uses a background daemon architecture, and why collections are created lazily.
2. **Visual & Memory-First Mental Models:** Anchor abstract concepts (like cursors, write concerns, embedded documents, and storage reclamation) to physical analogies and ASCII data flow diagrams.
3. **Spec-Grounded Industry Standard:** Adhere strictly to modern MongoDB CRUD specifications (`insertOne`, `insertMany`, `updateOne`, `deleteMany`) rather than deprecated legacy methods (`insert`, `update`, `remove`).
4. **Predict-First Debugging:** Challenge yourself on edge cases, return payloads, case sensitivity, and common anti-patterns before reading the solution.

---

## 🗺️ Complete 10-Episode Curriculum Roadmap

```
PHASE 1: CLIENT-SERVER ARCHITECTURE & DATA STORAGE (Ep. 01 – Ep. 03)
├── Ep. 01: The Mongo Shell (mongosh, mongod Daemon, Port 27017, JS REPL, Context Switching)
├── Ep. 02: How We Store Data (BSON vs JSON, Binary Serialization, 16MB Limit, Data Types)
└── Ep. 03: Documents & Collections (SQL to MongoDB Mapping, Schema Flexibility, Data Modeling)
                    │
                    ▼
PHASE 2: CREATE OPERATIONS (Ep. 04 – Ep. 05)
├── Ep. 04: INSERT in DB (InsertOne, Lazy Collection Creation, ObjectId Anatomy, Dynamic Schema)
└── Ep. 05: INSERT in DB (InsertMany, Bulk Writes, Network Round-Trips, Ordered vs Unordered)
                    │
                    ▼
PHASE 3: READ OPERATIONS & QUERY SELECTORS (Ep. 06 – Ep. 07)
├── Ep. 06: FIND in DB (find vs findOne, Cursors, Shell Batching, Projections, Equality Filters)
└── Ep. 07: Query Operators (Comparison: $gt, $gte, $lt, $in; Logical: $or, $and, $not, $nor)
                    │
                    ▼
PHASE 4: UPDATE, NESTING & DELETE OPERATIONS (Ep. 08 – Ep. 10)
├── Ep. 08: UPDATE in DB (updateOne, updateMany, replaceOne, $set, $unset, $inc, Upserts)
├── Ep. 09: Nesting & Sub-Documents (Embedded Objects, Dot Notation Syntax, Quoting Rules)
└── Ep. 10: DELETE in DB & Drop Database (deleteOne, deleteMany, drop vs deleteMany({}), dropDatabase)
```

---

## 📂 Quick Episode Navigation Matrix

| Ep. | Lecture Title | Key Concepts & Mechanics | Note Link |
| :---: | :--- | :--- | :---: |
| **01** | The Mongo Shell | `mongod` vs `mongosh`, port 27017, Node.js REPL, `use db`, `db`, `show dbs`, lazy database creation. | [Read Notes](./01-the-mongo-shell.md) |
| **02** | How We Store Data (BSON) | BSON vs JSON matrix, length-prefixed byte skipping, `ObjectId`, `Date`, `Decimal128`, 16MB document limit. | [Read Notes](./02-how-we-store-data-bson.md) |
| **03** | Document & Collection | SQL-to-MongoDB mapping matrix, dynamic polymorphic schema, denormalization vs normalization, embedding rules. | [Read Notes](./03-document-and-collection.md) |
| **04** | INSERT in DB (InsertOne) | `insertOne()`, lazy collection creation, 12-byte `ObjectId` anatomy, custom `_id`, `E11000` duplicate key error. | [Read Notes](./04-insert-in-db-insertone.md) |
| **05** | INSERT in DB (InsertMany) | `insertMany([])`, bulk write optimization, network latency, `ordered: true` vs `ordered: false` execution. | [Read Notes](./05-insert-in-db-insertmany.md) |
| **06** | FIND in DB | `find()` vs `findOne()`, cursor streaming, batch iteration (`it`), equality filtering, query projections. | [Read Notes](./06-find-in-db.md) |
| **07** | Query Operators | Comparison (`$gt`, `$gte`, `$in`, `$ne`) and Logical (`$or`, `$and`, `$not`, `$nor`) selectors, compound queries. | [Read Notes](./07-query-operators.md) |
| **08** | UPDATE in DB | `updateOne()`, `updateMany()`, `replaceOne()`, field modifiers (`$set`, `$unset`, `$inc`, `$rename`), upsert pattern. | [Read Notes](./08-update-in-db.md) |
| **09** | Nesting & Embedded Documents | Embedded sub-documents, dot notation syntax (`"parent.child"`), mandatory quotes, surgical nested updates. | [Read Notes](./09-nesting-and-embedded-documents.md) |
| **10** | DELETE in DB & Drop Database | `deleteOne()`, `deleteMany()`, `drop()` vs `deleteMany({})`, `dropDatabase()`, WiredTiger storage reclamation. | [Read Notes](./10-delete-in-db-and-drop-database.md) |

---

## ⚡ Master MongoDB CRUD Syntax Cheat Sheet

```javascript
// ==========================================
// 1. DATABASE & COLLECTION NAVIGATION
// ==========================================
use college                    // Switch context to "college" database
db                            // Print active database name
show dbs                      // List all non-empty databases on disk
show collections              // List all collections in current database
db.dropDatabase()             // Permanently delete current database from disk
db.student.drop()             // Permanently delete "student" collection and all its indexes

// ==========================================
// 2. CREATE (INSERTION)
// ==========================================
// Insert a single document
db.student.insertOne({ name: "adam", age: 19, marks: 88 })

// Insert multiple documents (Bulk write)
db.student.insertMany([
  { name: "catlyn", marks: 64, city: "Delhi" },
  { name: "donald", marks: 58, city: "Mumbai" }
], { ordered: false })        // ordered: false continues on duplicate key errors

// ==========================================
// 3. READ (QUERYING)
// ==========================================
db.student.find()                               // Return all documents (Cursor)
db.student.findOne({ name: "adam" })            // Return first matching document object (or null)
db.student.find({ city: "Delhi" })              // Exact equality match

// Projections (1 = include, 0 = exclude)
db.student.find({}, { name: 1, marks: 1, _id: 0 })

// Comparison Operators
db.student.find({ marks: { $gt: 75 } })         // marks > 75
db.student.find({ marks: { $gte: 75 } })        // marks >= 75
db.student.find({ marks: { $lt: 60 } })         // marks < 60
db.student.find({ marks: { $lte: 60 } })        // marks <= 60
db.student.find({ marks: { $ne: 88 } })         // marks !== 88
db.student.find({ marks: { $gte: 60, $lte: 80 } }) // Range: 60 <= marks <= 80
db.student.find({ city: { $in: ["Delhi", "Mumbai"] } }) // Set membership (OR inside one field)
db.student.find({ city: { $nin: ["Delhi", "Mumbai"] } }) // Not in set

// Logical Operators
db.student.find({
  $or: [
    { marks: { $gt: 75 } },
    { city: "Delhi" }
  ]
})

db.student.find({
  $and: [
    { marks: { $gte: 60 } },
    { city: "Delhi" }
  ]
})

// Querying Nested Sub-Documents (Dot Notation requires quotes!)
db.student.find({ "performance.marks": 88 })

// ==========================================
// 4. UPDATE (MODIFICATION)
// ==========================================
// Update single document (Surgical modification with $set)
db.student.updateOne(
  { name: "adam" },
  { $set: { marks: 99 } }
)

// Update multiple documents
db.student.updateMany(
  { city: "Delhi" },
  { $set: { city: "New Delhi" } }
)

// Update operators
db.student.updateOne({ name: "adam" }, { $inc: { marks: 2 } })            // Increment by +2
db.student.updateOne({ name: "adam" }, { $unset: { age: "" } })           // Delete "age" field
db.student.updateOne({ name: "adam" }, { $currentDate: { updated: true } }) // Stamp current Date

// Surgical nested update
db.student.updateOne(
  { name: "farah" },
  { $set: { "performance.grade": "A+" } }
)

// Upsert (Update if found, Insert if not found)
db.student.updateOne(
  { name: "emma" },
  { $set: { marks: 91, city: "London" } },
  { upsert: true }
)

// Replace entire document (Keeps original _id)
db.student.replaceOne(
  { name: "bob" },
  { name: "shradha", marks: 94, state: "Haryana" }
)

// ==========================================
// 5. DELETE (REMOVAL)
// ==========================================
db.student.deleteOne({ state: "Haryana" })       // Delete first matching document
db.student.deleteMany({ marks: { $lt: 75 } })    // Delete all matching documents
db.student.deleteMany({})                        // Delete ALL documents in collection
```

---

## 🎯 Master Anti-Pattern & Debugging Matrix

| Bug / Anti-Pattern | Bad Code | Why It Fails | Correct Solution |
| :--- | :--- | :--- | :--- |
| **Omitting `$set` in updates** | `db.student.updateOne({ name: "adam" }, { marks: 99 })` | MongoDB strictly rejects updates without atomic operators to prevent accidental overwrites. | `db.student.updateOne({ name: "adam" }, { $set: { marks: 99 } })` |
| **Unquoted Dot Notation** | `db.student.find({ performance.marks: 88 })` | In JavaScript, unquoted dots are illegal property separator tokens in object literal keys. | `db.student.find({ "performance.marks": 88 })` |
| **Overwriting Sub-Objects** | `db.student.updateOne({ name: "farah" }, { $set: { performance: { grade: "A+" } } })` | Replaces the entire `performance` sub-document, destroying sibling fields like `marks`! | `db.student.updateOne({ name: "farah" }, { $set: { "performance.grade": "A+" } })` |
| **Passing Array to `insertOne`** | `db.student.insertOne([ { a: 1 }, { b: 2 } ])` | `insertOne` expects an object. It stores the array as a single document instead of multiple records. | `db.student.insertMany([ { a: 1 }, { b: 2 } ])` |
| **Omitting Array in `insertMany`**| `db.student.insertMany({ a: 1 }, { b: 2 })` | `insertMany` treats argument 2 as options. Throws `Argument "docs" must be an array`. | `db.student.insertMany([ { a: 1 }, { b: 2 } ])` |
| **Calling `.sort()` on `findOne`** | `db.student.findOne().sort({ marks: -1 })` | `findOne` returns a raw document (or `null`), not a cursor. It has no `.sort()` method. | `db.student.find().sort({ marks: -1 }).limit(1)` |
| **Calling `deleteMany()` without `{}`** | `db.student.deleteMany()` | MongoDB prevents accidental collection wipes by requiring an explicit filter object. | `db.student.deleteMany({})` |
| **Case Sensitive String Mismatch** | `db.student.find({ city: "delhi" })` | BSON string comparisons are strictly case-sensitive. Won't match `"Delhi"`. | Exact match `"Delhi"` or regex `/^delhi$/i`. |
| **Duplicate `_id` Violation** | `db.student.insertOne({ _id: 101, ... })` twice | Violates the unique B-Tree index on `_id`. Throws `E11000 duplicate key error`. | Use unique IDs or let MongoDB generate `ObjectId`. |
| **Relational Over-Normalization** | Separate collections for addresses, phones, hobbies | Forces multiple queries or expensive `$lookup` joins. Defeats document database speed. | Embed 1:1 and 1:few related data directly inside the document. |

---

## 🏆 35-Question FAANG Active-Recall Question Bank

### 🔹 Module 1: Architecture, BSON, & Daemons (Ep. 01 – Ep. 03)
1. **Q:** What is the technical difference between `mongod` and `mongosh`?  
   *Answer:* `mongod` is the core background database daemon handling storage, cache, and queries; `mongosh` is the client-side interactive Node.js REPL.
2. **Q:** On which default port and IP address does local MongoDB run?  
   *Answer:* Port `27017` on `127.0.0.1` (`localhost`).
3. **Q:** Why doesn't a newly created database appear in `show dbs` immediately after running `use newdb`?  
   *Answer:* MongoDB implements **lazy allocation**; it creates no physical disk files until the first collection and document are inserted.
4. **Q:** What is BSON and why is it preferred over JSON for internal storage?  
   *Answer:* Binary JSON. It supports rich binary data types and encodes length-prefixed fields, allowing the engine to skip bytes during traversal without parsing characters.
5. **Q:** What is the maximum size of a single MongoDB BSON document, and why does this limit exist?  
   *Answer:* Exactly 16 Megabytes. It protects the RAM working set and prevents server memory exhaustion.
6. **Q:** What technology should you use in MongoDB if you must store files larger than 16MB?  
   *Answer:* **GridFS**, which chunks files into 255 KiB fragments across `fs.files` and `fs.chunks`.
7. **Q:** How many bytes is an `ObjectId`, and what are its three internal components?  
   *Answer:* 12 bytes total: 4-byte Unix timestamp, 5-byte random machine/PID identifier, and 3-byte incrementing counter.
8. **Q:** How can you extract the creation date of a document from its `_id`?  
   *Answer:* Call `doc._id.getTimestamp()`.
9. **Q:** What are the three default databases created on a fresh MongoDB installation?  
   *Answer:* `admin`, `config`, and `local`.
10. **Q:** Can data in the `local` database be replicated across a replica set?  
    *Answer:* No. Data in `local` (including the `oplog.rs`) is strictly instance-specific.

---

### 🔹 Module 2: Insertion, Bulk Operations, & ObjectId (Ep. 04 – Ep. 05)
11. **Q:** What does `db.collection.insertOne()` return upon a successful write?  
    *Answer:* An object: `{ acknowledged: true, insertedId: ObjectId(...) }`.
12. **Q:** What error is thrown when inserting a document with an already existing `_id`?  
    *Answer:* `MongoServerError: E11000 duplicate key error collection`.
13. **Q:** Can an `_id` field contain a custom value (like a string or integer)?  
    *Answer:* Yes, any valid BSON type except an array, provided it is unique within that collection.
14. **Q:** Why is `insertMany()` significantly faster than looping `insertOne()` 1,000 times?  
    *Answer:* It bundles documents into a single network round-trip instead of 1,000 individual TCP socket round-trips.
15. **Q:** What is the difference between `ordered: true` and `ordered: false` in `insertMany`?  
    *Answer:* `ordered: true` (default) stops execution at the first failure; `ordered: false` attempts all remaining documents despite errors.
16. **Q:** If document #3 in an ordered `insertMany` fails, what happens to documents #1 and #2?  
    *Answer:* Documents #1 and #2 remain permanently saved in the database (MongoDB does not automatically roll back).
17. **Q:** What data structure is returned by `insertMany` in `insertedIds`?  
    *Answer:* A key-value dictionary where keys are zero-based array indices (`{ '0': ObjectId(...), '1': ObjectId(...) }`).

---

### 🔹 Module 3: Read Queries, Cursors, & Operators (Ep. 06 – Ep. 07)
18. **Q:** What is the fundamental difference in return type between `find()` and `findOne()`?  
    *Answer:* `find()` returns a `FindCursor`; `findOne()` returns a single deserialized BSON document (or `null`).
19. **Q:** How many documents does `mongosh` display from a cursor before prompting `"Type 'it' for more"`?  
    *Answer:* Exactly 20 documents.
20. **Q:** Why is checking `if (db.users.find({ email }))` a critical bug in Node.js backend code?  
    *Answer:* Because a cursor object is always truthy in JavaScript, even if 0 documents matched! Use `findOne()` instead.
21. **Q:** Write a query to find all students who scored $\ge 75$ marks.  
    *Answer:* `db.student.find({ marks: { $gte: 75 } })`.
22. **Q:** What is the difference between `$gt` and `$gte`?  
    *Answer:* `$gt` is strictly greater than ($>$); `$gte` is greater than or equal to ($\ge$).
23. **Q:** When should you prefer `$in` over multiple `$or` clauses?  
    *Answer:* Whenever matching multiple possible values against a **single field** (`{ city: { $in: ["A", "B"] } }`).
24. **Q:** Write a query to find students who live in Delhi OR scored $> 75$.  
    *Answer:* `db.student.find({ $or: [{ city: "Delhi" }, { marks: { $gt: 75 } }] })`.
25. **Q:** How does MongoDB handle comma-separated conditions like `{ city: "Delhi", marks: 75 }`?  
    *Answer:* It treats them as an **implicit AND** (both conditions must match).
26. **Q:** When is an explicit `$and` operator strictly required?  
    *Answer:* When querying the same field or operator multiple times (avoiding JavaScript object key collisions).
27. **Q:** What does `{ marks: { $ne: 88 } }` return for a document that completely lacks the `marks` field?  
    *Answer:* It matches and returns the document.

---

### 🔹 Module 4: Updates, Nesting, & Deletions (Ep. 08 – Ep. 10)
28. **Q:** What happens if you call `updateOne` without an atomic update operator like `$set`?  
    *Answer:* Modern MongoDB throws an error (`Update document requires atomic operators`).
29. **Q:** Explain why `matchedCount` can be 1 while `modifiedCount` is 0 in an update response.  
    *Answer:* The document matched the filter, but its existing field value was already identical to the requested update, so no disk write was needed.
30. **Q:** What is the difference between `updateOne` and `replaceOne`?  
    *Answer:* `updateOne` surgically modifies specified fields; `replaceOne` replaces the entire document body while preserving only the `_id`.
31. **Q:** What does `{ upsert: true }` do?  
    *Answer:* Updates the document if a match is found; inserts a new document if no match is found.
32. **Q:** Why are quotes mandatory when querying nested fields with dot notation (`"performance.marks"`)?  
    *Answer:* Because unquoted dots are illegal identifier characters in JavaScript object keys.
33. **Q:** What is the catastrophic risk of updating a nested field using `{ $set: { performance: { grade: "A+" } } }`?  
    *Answer:* It replaces the entire `performance` sub-document, obliterating sibling fields like `marks`! Use `"performance.grade"` instead.
34. **Q:** Why is `db.collection.drop()` orders of magnitude faster than `db.collection.deleteMany({})` for 5M records?  
    *Answer:* `drop()` unlinks the physical collection file and drops indexes in one system call, whereas `deleteMany({})` must scan, delete, and update B-Tree index pages 5 million times.
35. **Q:** Does deleting 10GB of documents with `deleteMany()` immediately free 10GB of space on the OS hard drive?  
    *Answer:* No. WiredTiger retains the allocated disk blocks inside its `.wt` files to reuse for future inserts without OS file expansion overhead.

---

## ⚡ Indexing & Performance Foundations (Preview)

> **Core Rule:** Without an index, MongoDB must perform a **Collection Scan (`COLLSCAN`)** — scanning every single document in the collection. With an index, it performs an **Index Scan (`IXSCAN`)** in $O(\log N)$ time using a B-Tree.

### Essential Index Commands in `mongosh`:

```javascript
// 1. Create a Single-Field Index (1 = Ascending, -1 = Descending)
db.student.createIndex({ marks: 1 })

// 2. Create a Compound Index (Prefix rule applies: query must filter by leftmost key first)
db.student.createIndex({ city: 1, marks: -1 })

// 3. Create a Unique Index (Rejects duplicates at the database layer)
db.student.createIndex({ email: 1 }, { unique: true })

// 4. List all indexes on a collection
db.student.getIndexes()

// 5. Measure query performance with explain()
db.student.find({ marks: { $gte: 75 } }).explain("executionStats")
// Check: executionStats.totalDocsExamined vs executionStats.nReturned
// If stage is "COLLSCAN", you examined all documents! If "IXSCAN", you used the B-Tree index.

// 6. Drop an index
db.student.dropIndex({ marks: 1 })
```

---

## 🪟 Windows Database Administration & CLI Quick Reference

For Windows developers using **PowerShell**, MongoDB includes native command-line utilities (available via MongoDB Database Tools):

### Service Management (PowerShell as Administrator):

```powershell
# Start MongoDB Service
net start MongoDB

# Check Status
Get-Service MongoDB

# Stop MongoDB Service
net stop MongoDB

# Restart MongoDB Service
Restart-Service MongoDB
```

### Database Backup & Restore (`mongodump` / `mongorestore`):

```powershell
# Backup the entire "college" database to C:\backups:
mongodump --db college --out C:\backups\mongodb_backup

# Restore the "college" database from backup:
mongorestore --db college C:\backups\mongodb_backup\college

# Drop existing collections before restoring (clean restore):
mongorestore --db college --drop C:\backups\mongodb_backup\college
```

### Data Import & Export (`mongoexport` / `mongoimport`):

```powershell
# Export "students" collection to JSON:
mongoexport --db college --collection students --out C:\backups\students.json --jsonArray

# Export "students" collection to CSV:
mongoexport --db college --collection students --type=csv --fields name,age,marks,city --out C:\backups\students.csv

# Import JSON file into "students" collection:
mongoimport --db college --collection students --file C:\backups\students.json --jsonArray

# Import CSV file into "students" collection:
mongoimport --db college --collection students --type=csv --headerline --file C:\backups\students.csv
```

---

## 🚀 Part 2 Advanced Curriculum Roadmap

After mastering the core CRUD foundations in this guide, the journey continues with:

| Phase | Topics | Key Focus Areas |
| :--- | :--- | :--- |
| **Phase 5** | **Aggregation Pipeline** | `$match`, `$group`, `$project`, `$sort`, `$limit`, `$unwind`, `$lookup` (MongoDB JOIN equivalent), multi-stage data pipelines. |
| **Phase 6** | **Mongoose ODM Deep Dive** | Schemas, Models, validation rules, pre/post middleware hooks, custom instance & static methods, virtual properties. |
| **Phase 7** | **Data Modeling & Relationships** | 1:1, 1:N, N:N relationships, Embedding vs Referencing, bucket pattern for time-series, two-way referencing. |
| **Phase 8** | **Transactions & ACID Semantics** | Multi-document ACID transactions with sessions (`session.startTransaction()`, `session.commitTransaction()`). |
| **Phase 9** | **Production Architecture** | Replica Sets (Primary-Secondary failover), Sharding (Horizontal scaling with shard keys), Atlas Cloud security & monitoring. |

---

## 🎓 Completion & Mastery Checklist

- [ ] Installed MongoDB 7.0+ & `mongosh` 2.0+ on Windows and configured System PATH.
- [ ] Confirmed difference between `mongod` (server daemon) and `mongosh` (JS client).
- [ ] Grasped BSON internal serialization, length-prefixed traversal, and 16MB document boundary.
- [ ] Executed all CRUD operations: `insertOne`, `insertMany`, `find`, `findOne`, `updateOne`, `updateMany`, `replaceOne`, `deleteOne`, `deleteMany`.
- [ ] Mastered query operators: Comparison (`$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$ne`) and Logical (`$or`, `$and`, `$not`, `$nor`).
- [ ] Manipulated embedded sub-documents with dot notation (`"parent.child"`).
- [ ] Understood `drop()` vs `deleteMany({})` and WiredTiger storage space allocation.
- [ ] Connected native `mongosh` queries to Node.js / Mongoose backend patterns.
