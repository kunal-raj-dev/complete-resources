# Episode 02 — How We Store Data: BSON (Binary JSON), Data Types, & Serialization

> **One-Line Mental Model:** If JSON is an uncompressed printed novel that the engine must read word-for-word, BSON is a compiled binary ledger with indexed byte offsets and explicit type tags that the database can traverse at hardware speed.

---

## 📌 Source Metadata
> **Course:** Delta Batch (Web Development)  
> **Module:** 44. MongoDB (Part 1)  
> **Lecture:** 02. How we store data? (BSON)  
> **Duration:** 03:05  
> **Documentation Ref:** [MongoDB JSON and BSON Specification](https://www.mongodb.com/json-and-bson)  
> **Status:** AUDITED & EXPANDED  

---

## 🎯 What You Will Learn

- Why MongoDB does **not** store documents as raw JSON on disk or in memory.
- The fundamental architecture of **BSON (Binary JSON)** and how it extends JSON.
- The **JSON vs. BSON Comparison Matrix**: encoding, type support, human readability, and speed.
- The mechanical reason BSON is faster: **Length Prefixes and Type Codes** enabling byte-skipping traversal.
- Specialized BSON data types: `ObjectId`, `Date`, `BinData`, `Int32`, `Int64 (Long)`, and `Decimal128`.
- The **16 Megabyte (16 MB) Document Size Limit**: Why it exists and the engineering principles behind it.

---

## 1. The Idea in Simple Words

### Simple Explanation
When you use MongoDB in your code or shell, everything looks like standard JSON:
```json
{ "name": "Adarsh", "age": 25 }
```
However, saving raw text JSON directly to your hard drive would be disastrous for a database:
1. **Numbers are vague:** In JSON, `25` and `25.0000000001` are both just "numbers". There is no distinction between integers, decimals, and large timestamps.
2. **Reading is slow:** To find the field `"age"` in a massive JSON string, the computer must scan every character from left to right, parsing commas, quotes, and brackets.

To solve this, MongoDB invented **BSON (Binary JSON)**. BSON converts your human-friendly JSON into a compact, typed binary format that the computer's CPU can read, jump through, and manipulate thousands of times faster.

### Technical Explanation
BSON is a binary serialization format used both as a data storage format and as the network transfer format for MongoDB. BSON was designed to achieve three specific goals:
1. **Lightweight:** Minimal spatial overhead compared to verbose text encodings.
2. **Traversable:** Each element in BSON is prefixed with a 1-byte type identifier, the field name (null-terminated cstring), and the length of the payload. This allows query executors to calculate byte offsets and skip unneeded sub-documents without parsing their interior contents.
3. **Efficient:** Encoding and decoding between native language types (like C structs, V8 objects, or Python dicts) and BSON is computationally cheap.

### Before vs After Motivation
- **Before (Raw JSON / XML Storage):** Massive string parsing overhead on every query, lack of native Date/Timestamp types (forcing developers to store dates as fragile ISO strings or integers), and loss of numeric precision (floating-point rounding bugs).
- **After (BSON Architecture):** Zero ambiguity in numeric precision, instant byte-offset skipping during query filters, native 64-bit UTC millisecond `Date` objects, and compact binary hashes.

---

## 2. 🧠 Mental Model: The Book Index vs Scanning Every Word

```
RAW JSON (Text Parsing Overhead):
   { "id": 101, "bio": "Very long paragraph...", "score": 98 }
     ▲
     └── The engine MUST parse every character of "bio" to find "score"!

BSON (Binary Traversal with Byte-Offsets):
   [TotalDocSize: 4B][Type: 0x10][Key: "id\0"][Val: 101]
   [Type: 0x02][Key: "bio\0"][PayloadLength: 200B][Payload: "Very long..."]
   [Type: 0x10][Key: "score\0"][Val: 98][DocTerminator: 0x00]
                     ▲
                     └── Engine sees [PayloadLength: 200B] -> Jumps 200 bytes instantly
                         to read "score" directly without parsing "bio"!
```

---

## 3. The JSON vs BSON Comparison Matrix

This matrix directly reflects official MongoDB architecture and lecture curriculum:

| Dimension | JSON (JavaScript Object Notation) | BSON (Binary JSON) |
| :--- | :--- | :--- |
| **Encoding** | UTF-8 String (Human-readable text) | Binary representation (0s and 1s) |
| **Primary Purpose** | Universal data interchange format on the web | High-performance database storage & traversal |
| **Readability** | Human and Machine readable | Machine only (requires decoding tool like `mongosh`) |
| **Numeric Types** | Single generic "Number" (IEEE 754 Float) | `Int32`, `Int64 (Long)`, `Double`, `Decimal128` |
| **Date Support** | ❌ None (Stored as string or Unix epoch int) | ✅ Native 64-bit UTC millisecond timestamp |
| **Binary Data** | ❌ None (Requires Base64 string encoding) | ✅ Native `BinData` (byte arrays, hashes, UUIDs) |
| **Special Types** | String, Number, Boolean, Array, Object, null | + `ObjectId`, `Regex`, `Timestamp`, `MinKey`, `MaxKey` |
| **Traversal Speed** | Slow (character-by-character parsing) | Extremely Fast (length-prefixed byte skipping) |
| **Space Efficiency** | Often smaller for tiny text docs | Optimized for fast byte alignment, slightly more metadata overhead |

---

## 4. Specialized BSON Data Types

### 1. `ObjectId` (Type Code `0x07`)
A globally unique 12-byte identifier automatically generated as the default `_id` field:
- **Bytes 0–3 (4 bytes):** Unix epoch timestamp in seconds.
- **Bytes 4–8 (5 bytes):** Random process identifier (unique per machine/process).
- **Bytes 9–11 (3 bytes):** Incrementing counter initialized to a random value.

```javascript
// mongosh demonstration
ObjectId("64fec88c4d37352da5df8407").getTimestamp()
// Returns: 2023-09-11T07:44:12.000Z
```

### 2. `Date` (Type Code `0x09`)
A 64-bit integer representing the number of milliseconds since the Unix epoch (Jan 1, 1970).
```javascript
new Date() // ISODate("2026-10-26T07:15:00.000Z")
```

### 3. High-Precision Numbers: `Decimal128` (Type Code `0x13`)
Provides 34 decimal digits of precision with an exponent range of −6143 to +6144. Essential for financial applications (currency, banking, stock trades) where floating-point rounding errors (e.g., `0.1 + 0.2 === 0.30000000000000004`) cannot be tolerated.
```javascript
NumberDecimal("999999999.99")
```

### 4. `BinData` (Type Code `0x05`)
Stores raw binary payloads (UUIDs, cryptographic signatures, small image thumbnails).
```javascript
UUID() // Binary.createFromBase64("...", 4)
```

---

## 5. What Just Happened? The Serialization Flow

When you write a document in your application and send it to MongoDB:

```
[1] Node.js Application:
    const user = { name: "Adam", age: 19, marks: 88 };
         │
         ▼
[2] MongoDB Node.js Driver (BSON Serializer):
    Converts JavaScript Object -> Binary Byte Buffer (BSON).
    - Injects `_id: ObjectId(...)` if not present.
    - Encodes "Adam" as UTF-8 string with length.
    - Encodes 19 as 32-bit integer (0x10).
         │
         ▼
[3] Network Transmission:
    Transmitted over TCP port 27017 via MongoDB Wire Protocol.
         │
         ▼
[4] WiredTiger Storage Engine (mongod):
    Writes BSON payload to WiredTiger memory cache and appends to disk journal.
         │
         ▼
[5] Querying in mongosh:
    `mongod` reads BSON bytes from disk -> sends BSON over socket ->
    `mongosh` deserializes BSON -> prints pretty-formatted JSON to your console!
```

---

## 6. The 16 Megabyte (16 MB) Document Limit

MongoDB enforces a strict **maximum BSON document size of 16 megabytes**.

### Why does this limit exist?
1. **RAM Protection:** When MongoDB fetches a document, it must load the entire document into the WiredTiger cache in RAM. Unrestricted document sizes would cause memory thrashing and Out-Of-Memory (OOM) server crashes.
2. **Network Performance:** Transferring huge documents over sockets blocks the event loop and saturates network bandwidth.
3. **Encouraging Clean Data Modeling:** A document exceeding 16MB is almost always an architectural anti-pattern (such as pushing millions of array elements into a single record).

### What if you need to store files larger than 16MB?
Use **GridFS**: MongoDB’s built-in file specification that chunks large files (e.g. video files, PDFs, high-res images) into 255 KiB discrete chunks across two collections (`fs.files` and `fs.chunks`).

---

## 7. Common Mistakes & Anti-Patterns

### Mistake 1: Storing Dates as plain ISO Strings
```javascript
// ❌ BAD PRACTICE:
db.orders.insertOne({ orderDate: "2026-10-26T12:00:00Z" })

// 🔍 WHY: Stored as a string. You cannot perform date math, range queries
// ($gte with actual Date operators), or index-optimized date aggregations.
// ✅ CORRECT:
db.orders.insertOne({ orderDate: new Date() })
```

### Mistake 2: Storing currency/money as standard Numbers
```javascript
// ❌ DANGEROUS FOR E-COMMERCE / BANKING:
db.accounts.insertOne({ balance: 19.99 }) // Stored as standard double float!

// 🔍 WHY: Floating-point arithmetic causes cumulative precision drift.
// ✅ CORRECT:
db.accounts.insertOne({ balance: NumberDecimal("19.99") })
```

### Mistake 3: Storing large images/videos directly inside a document
```javascript
// ❌ WRONG: Attempting to embed a 50MB video inside a BSON document.
// Result: MongoServerError: BSONObj size is invalid (exceeds 16MB)
// ✅ CORRECT: Store the video in S3 / GridFS and save only the URL/Reference in MongoDB.
```

---

## 8. 🧠 Brain Triggers & Confusion Checks

> **Click Moment:** You *type* JSON in your terminal, and `mongosh` *displays* JSON on your screen. But on disk and over the network, it is **100% BSON**! JSON is merely the human presentation layer.

- **Q: Does BSON take more disk space than JSON?**
  - *Click Answer:* For tiny documents with short strings, BSON can have slightly more overhead due to explicit length headers and type tags. However, for numbers (which are packed into 4 or 8 binary bytes instead of ASCII character digits) and for traversal speed, BSON is vastly superior.
- **Q: Can I extract the exact creation timestamp of any document without adding a `createdAt` field?**
  - *Click Answer:* Yes! The default `_id: ObjectId(...)` encodes the 4-byte UTC creation second directly into its first 8 hexadecimal characters. `doc._id.getTimestamp()` extracts it instantly!

---

## 9. ⚠️ Edge Cases & Exceptions

### Sorting across Different BSON Types
What happens if you run `{ $sort: { field: 1 } }` on a collection where `field` contains different data types (strings in some documents, numbers in others)?
MongoDB defines a strict **BSON Comparison Order**:
1. MinKey (lowest)
2. Null
3. Numbers (`Int32`, `Int64`, `Double`, `Decimal128`)
4. Symbol, String
5. Object
6. Array
7. BinData
8. ObjectId
9. Boolean
10. Date
11. Timestamp
12. Regular Expression
13. MaxKey (highest)

---

## 10. 🔥 Interview Deep Dive

### Predict First: The Floating Point Trap
Predict what is logged when querying floating-point math:

```javascript
db.inventory.insertOne({ item: "A", quantity: 0.1 + 0.2 })
db.inventory.find({ quantity: 0.3 })
```

<details>
<summary>▶ Click to reveal Predict First Output</summary>

**Output:**
```
// (No documents returned! Empty result)
```

**Explanation:**
In standard IEEE 754 floating-point math (which standard JavaScript and BSON Double use), `0.1 + 0.2` evaluates to `0.30000000000000004`. Therefore, exact equality matching against `0.3` fails!
To store exact numbers without drift, always use `NumberDecimal("0.1")` or store values in smallest integer units (e.g. cents instead of dollars).
</details>

---

## 🧠 What You Actually Need to Remember

1. **BSON stands for Binary JSON:** It is the storage and network wire format of MongoDB.
2. **Speed Advantage:** BSON uses **length-prefixed fields** allowing the query engine to skip bytes without parsing string characters.
3. **Type Richness:** Supports `ObjectId`, `Date`, `BinData`, and explicit integer types (`Int32`, `Int64`, `Decimal128`) absent in standard JSON.
4. **Hard Size Limit:** Max BSON document size is **16 MB**.
5. **ObjectId Timestamp:** `_id` embeds a 4-byte timestamp extractable via `.getTimestamp()`.

---

## ⚡ 30-Second Revision

- **Essential Facts:**
  - JSON = Text-based, UTF-8, human-readable, 6 basic types.
  - BSON = Binary-encoded, machine-optimized, traversable, rich data types.
  - Limit: 16 MB per document (use GridFS for larger binary files).
  - ObjectId: 12 bytes total (4B timestamp + 5B random + 3B counter).
- **Key Mental Model:** JSON is a novel you must read page-by-page; BSON is a ledger with exact byte offsets allowing instant random jumps.
- **Common Trap:** Storing financial numbers as standard floats instead of `NumberDecimal`.
- **Code Pattern:**
  ```javascript
  // Extracting timestamp from ObjectId in mongosh
  const id = ObjectId("64fec88c4d37352da5df8407");
  print(id.getTimestamp()); // 2023-09-11T07:44:12.000Z
  ```

---

## 11. 🌐 Real-World Production Scenario: E-Commerce Order with BSON Types

In a real e-commerce application (like Amazon, Flipkart, or Shopify), BSON data types are critical for storing orders correctly:

```javascript
// mongosh — A production-grade order document using proper BSON types:
db.orders.insertOne({
  orderId: ObjectId(),                              // Unique order ID with embedded timestamp
  customerId: ObjectId("64fec88c4d37352da5df8407"),  // Reference to customer document
  items: [
    { sku: "LAPTOP-001", name: "Dell XPS 15", qty: 1, price: NumberDecimal("89999.99") },
    { sku: "MOUSE-042", name: "Logitech MX Master", qty: 2, price: NumberDecimal("6499.00") }
  ],
  totalAmount: NumberDecimal("102997.99"),           // ✅ NumberDecimal prevents floating-point drift!
  paymentMethod: "UPI",
  shippingAddress: {
    street: "42 MG Road",
    city: "Bangalore",
    state: "Karnataka",
    pinCode: 560001
  },
  status: "confirmed",
  createdAt: new Date(),                             // ✅ Native BSON Date (not a string!)
  estimatedDelivery: new Date("2026-11-02T10:00:00Z")
})
```

**Why this matters:**
- `NumberDecimal("89999.99")` prevents the `0.1 + 0.2 ≠ 0.3` floating-point bug in financial calculations.
- `new Date()` enables efficient date range queries (`$gte`, `$lte`) and indexing.
- `ObjectId()` for `orderId` gives you a free creation timestamp via `.getTimestamp()`.

---

## 12. 🔗 Mongoose Bridge: BSON Types in Node.js

When building a Node.js backend with Mongoose, BSON types map to Mongoose schema types:

```javascript
const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  customerId: { type: mongoose.Schema.Types.ObjectId, ref: 'Customer', required: true },
  items: [{
    sku:   { type: String, required: true },
    name:  { type: String, required: true },
    qty:   { type: Number, min: 1 },
    price: { type: mongoose.Schema.Types.Decimal128, required: true }  // ✅ Maps to BSON Decimal128
  }],
  totalAmount: { type: mongoose.Schema.Types.Decimal128, required: true },
  status: { type: String, enum: ['pending', 'confirmed', 'shipped', 'delivered'], default: 'pending' },
  createdAt: { type: Date, default: Date.now }  // ✅ Maps to BSON Date
});

const Order = mongoose.model('Order', orderSchema);
```

| BSON Type | Mongoose Schema Type | Example |
| :--- | :--- | :--- |
| `ObjectId` | `mongoose.Schema.Types.ObjectId` | `ref: 'User'` for population |
| `Date` | `Date` | `default: Date.now` |
| `Decimal128` | `mongoose.Schema.Types.Decimal128` | Currency, financial values |
| `BinData` | `Buffer` | Binary files, hashes |
| `Int32` / `Double` | `Number` | Counts, scores, ages |
| `String` | `String` | Names, emails, descriptions |
| `Boolean` | `Boolean` | Flags, toggles |
| `Array` | `[SchemaType]` | Lists, tags, items |

---

## 13. 🛠️ Tiny Practice Task & Interview Readiness Checklist

### Practice Task:
1. Open `mongosh`.
2. Generate a new `ObjectId` using `ObjectId()` and inspect its string representation.
3. Call `.getTimestamp()` on it to verify the embedded UTC time.
4. Create a document demonstrating `NumberDecimal` and `new Date()`:
   ```javascript
   db.demo.insertOne({
     txId: ObjectId(),
     amount: NumberDecimal("4500.50"),
     createdAt: new Date()
   })
   ```
5. Retrieve it with `db.demo.find()` and inspect the formatted BSON types.

### Interview Readiness Checklist
- [ ] Can you name 4 data types supported in BSON that do not exist in JSON?
- [ ] Why is BSON faster for database query engines than text JSON?
- [ ] What is the maximum size of a single MongoDB document and why does that limit exist?
- [ ] What are the 3 component parts of a 12-byte `ObjectId`?
