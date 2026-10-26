# 🍃 MongoDB Notes — Complete Curriculum & Study Guide

> **Curriculum Source:** Delta Batch (Web Development) — *44. MongoDB (Part 1)*  
> **Instructor:** Shradha Khapra  
> **Total Lectures Covered:** **10 Comprehensive In-Depth Lectures (Ep. 01 → Ep. 10)**  
> **Core Focus:** MongoDB 7.0+ Architecture, `mongosh` 2.0+ Shell, BSON Internals, Document Modeling, Complete CRUD Lifecycle, Query Selectors, Embedded Sub-Documents, and WiredTiger Storage Reclamation  
> **Language & Standard:** 100% Technical English | Production-Grade Industry Standards  

---

## 📖 Master Curriculum Index & Comprehensive Guide

👉 **[Open Complete 10-Episode Master Curriculum Index (`00-master-index.md`)](./00-master-index.md)**  
*(Includes Complete 4-Phase Learning Roadmap, Full CRUD Master Syntax Cheat Sheet, Master Anti-Pattern & Debugging Matrix, and 35-Question FAANG Active-Recall Question Bank).*

---

## 📂 Quick Episode Navigation

| Ep. | Lecture Title | Key Topics Covered | Note Link |
| :---: | :--- | :--- | :---: |
| **01** | The Mongo Shell | `mongod` Server vs `mongosh` Client, Port 27017, Node.js REPL, `show dbs`, `use college`, `db` pointer, Lazy Database Creation | [Read Notes](./01-the-mongo-shell.md) |
| **02** | How We Store Data (BSON) | JSON vs BSON matrix, length-prefixed byte skipping, `ObjectId`, `Date`, `Decimal128`, 16MB document size limit | [Read Notes](./02-how-we-store-data-bson.md) |
| **03** | Document & Collection | Relational SQL to MongoDB concept mapping, dynamic polymorphic schemas, data denormalization vs normalization | [Read Notes](./03-document-and-collection.md) |
| **04** | INSERT in DB (InsertOne) | `insertOne()`, lazy collection creation, 12-byte `ObjectId` anatomy, custom `_id`, `E11000` duplicate key errors | [Read Notes](./04-insert-in-db-insertone.md) |
| **05** | INSERT in DB (InsertMany) | `insertMany([])`, bulk write optimization, network latency, `ordered: true` vs `ordered: false` execution | [Read Notes](./05-insert-in-db-insertmany.md) |
| **06** | FIND in DB | `find()` vs `findOne()`, cursor streaming, batch iteration (`it`), equality filtering, query projections | [Read Notes](./06-find-in-db.md) |
| **07** | Query Operators | Comparison (`$gt`, `$gte`, `$in`, `$ne`) and Logical (`$or`, `$and`, `$not`, `$nor`) selectors, compound queries | [Read Notes](./07-query-operators.md) |
| **08** | UPDATE in DB | `updateOne()`, `updateMany()`, `replaceOne()`, field modifiers (`$set`, `$unset`, `$inc`, `$rename`), upsert pattern | [Read Notes](./08-update-in-db.md) |
| **09** | Nesting & Embedded Documents | Embedded sub-documents, dot notation syntax (`"parent.child"`), mandatory quotes, surgical nested updates | [Read Notes](./09-nesting-and-embedded-documents.md) |
| **10** | DELETE in DB & Drop Database | `deleteOne()`, `deleteMany()`, `drop()` vs `deleteMany({})`, `dropDatabase()`, WiredTiger storage reclamation | [Read Notes](./10-delete-in-db-and-drop-database.md) |

---

## 🛠️ Windows Environment Setup & Quick Start (Complete Guide)

> **⚠️ Important:** This section is written specifically for **Windows** users. All commands use **PowerShell** and Windows-native tools.

### Step 1: Download & Install MongoDB Community Server

1. Visit the official download page: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Select:
   - **Version:** `7.0.x` (latest stable)
   - **Platform:** `Windows`
   - **Package:** `MSI`
3. Run the `.msi` installer:
   - Choose **"Complete"** installation type.
   - ✅ Check **"Install MongoDB as a Service"** (this ensures `mongod` starts automatically on boot).
   - ✅ Check **"Install MongoDB Compass"** (the official GUI tool).
4. The default installation path is:
   ```
   C:\Program Files\MongoDB\Server\7.0\
   ```

### Step 2: Add MongoDB to System PATH (if not auto-configured)

```powershell
# Check if mongod is accessible:
mongod --version

# If "not recognized" error appears, add MongoDB bin to PATH:
# 1. Open Start Menu → Search "Environment Variables" → Click "Edit the system environment variables"
# 2. Click "Environment Variables" → Under "System Variables" → Select "Path" → Click "Edit"
# 3. Click "New" → Add: C:\Program Files\MongoDB\Server\7.0\bin
# 4. Click OK → OK → OK
# 5. Restart PowerShell terminal

# Verify installation:
mongod --version
# Expected output: db version v7.0.x
```

### Step 3: Install `mongosh` (MongoDB Shell)

`mongosh` may be installed separately from MongoDB Server:

```powershell
# Option A: Download MSI from https://www.mongodb.com/try/download/shell
# Option B: Install via winget (Windows Package Manager):
winget install MongoDB.Shell

# Verify:
mongosh --version
# Expected output: 2.x.x
```

### Step 4: Managing the MongoDB Service on Windows

```powershell
# ✅ Start the MongoDB service:
net start MongoDB

# ✅ Stop the MongoDB service:
net stop MongoDB

# ✅ Check service status:
Get-Service MongoDB

# ✅ Restart the service:
Restart-Service MongoDB

# ✅ Set to start automatically on boot (already default if installed as service):
Set-Service -Name MongoDB -StartupType Automatic
```

### Step 5: Launch the Shell & Verify

```powershell
# Open PowerShell and connect to the local MongoDB server:
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/...
# Using MongoDB: 7.0.x
# Using Mongosh: 2.x.x
# test>
```

### Step 6: Verify Installation & Active Context

```javascript
// Test JS runtime
test> 1 + 2
3

// Inspect databases
test> show dbs
admin   40.00 KiB
config  96.00 KiB
local   72.00 KiB

// Switch to working database
test> use college
switched to db college

// Verify current database pointer
college> db
college
```

### 🔧 Troubleshooting Windows Issues

| Problem | Solution |
| :--- | :--- |
| `MongoNetworkError: connect ECONNREFUSED` | Run `net start MongoDB` in PowerShell (as Admin) |
| `'mongosh' is not recognized` | Add `mongosh` to PATH or reinstall via `winget install MongoDB.Shell` |
| `mongod: command not found` | Add `C:\Program Files\MongoDB\Server\7.0\bin` to system PATH |
| Service won't start | Check data directory exists: `C:\data\db` or the configured `dbPath` in `mongod.cfg` |
| Port 27017 already in use | Run `netstat -ano | findstr :27017` to find the conflicting process |

---

## 🌐 MongoDB Atlas Cloud Setup (Free Tier — M0)

For development/testing without a local installation, use MongoDB Atlas (fully managed cloud):

### Quick Start:
1. **Sign up** at [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
2. **Create a Free Cluster:**
   - Click "Build a Database" → Select **M0 FREE** tier
   - Choose provider (AWS/GCP/Azure) and nearest region
   - Name your cluster (e.g., `dev-cluster`)
3. **Configure Access:**
   - Create a database user (username + password)
   - Add your IP to the whitelist (or use `0.0.0.0/0` for development)
4. **Get Connection String:**
   - Click "Connect" → "Connect with MongoDB Shell"
   - Copy the connection string:
     ```
     mongodb+srv://username:password@dev-cluster.xxxxx.mongodb.net/
     ```
5. **Connect from `mongosh`:**
   ```powershell
   mongosh "mongodb+srv://username:password@dev-cluster.xxxxx.mongodb.net/college"
   ```
6. **Connect from Node.js (Mongoose):**
   ```javascript
   const mongoose = require('mongoose');
   mongoose.connect('mongodb+srv://username:password@dev-cluster.xxxxx.mongodb.net/college');
   ```

---

## 🔗 Mongoose (Node.js ODM) — Quick Reference Bridge

> **What is Mongoose?** An Object Data Modeling (ODM) library for Node.js that provides schema validation, type casting, and query building on top of the native MongoDB driver.

### Installation:
```powershell
# In your Node.js project directory:
npm init -y
npm install mongoose
```

### How `mongosh` Commands Map to Mongoose:

| mongosh (Shell) | Mongoose (Node.js Backend) |
| :--- | :--- |
| `use college` | `mongoose.connect('mongodb://127.0.0.1:27017/college')` |
| `db.student.insertOne({...})` | `await Student.create({...})` |
| `db.student.insertMany([...])` | `await Student.insertMany([...])` |
| `db.student.find({ city: "Delhi" })` | `await Student.find({ city: "Delhi" })` |
| `db.student.findOne({ name: "adam" })` | `await Student.findOne({ name: "adam" })` |
| `db.student.updateOne(filter, update)` | `await Student.updateOne(filter, update)` |
| `db.student.updateMany(filter, update)` | `await Student.updateMany(filter, update)` |
| `db.student.replaceOne(filter, doc)` | `await Student.replaceOne(filter, doc)` |
| `db.student.deleteOne(filter)` | `await Student.deleteOne(filter)` |
| `db.student.deleteMany(filter)` | `await Student.deleteMany(filter)` |
| `db.student.drop()` | `await mongoose.connection.db.dropCollection('students')` |
| `db.dropDatabase()` | `await mongoose.connection.db.dropDatabase()` |

### Minimal Mongoose App (Complete Working Example):

```javascript
// app.js — Run with: node app.js
const mongoose = require('mongoose');

// 1. Connect to local MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/college')
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.error('❌ Connection failed:', err));

// 2. Define a Schema (Mongoose enforces structure on top of MongoDB's flexibility)
const studentSchema = new mongoose.Schema({
  name:  { type: String, required: true },
  age:   { type: Number, min: 0 },
  marks: { type: Number, min: 0, max: 100 },
  city:  { type: String },
  performance: {
    marks: Number,
    grade: String
  }
});

// 3. Create a Model (Maps to the "students" collection — Mongoose auto-pluralizes)
const Student = mongoose.model('Student', studentSchema);

// 4. CRUD Operations
async function main() {
  // CREATE
  const adam = await Student.create({ name: 'adam', age: 19, marks: 88 });
  console.log('Inserted:', adam);

  // READ
  const found = await Student.find({ marks: { $gte: 75 } });
  console.log('Students with marks >= 75:', found);

  // UPDATE
  await Student.updateOne({ name: 'adam' }, { $set: { marks: 99 } });
  console.log('Updated Adam\'s marks to 99');

  // DELETE
  await Student.deleteOne({ name: 'adam' });
  console.log('Deleted Adam');

  // Cleanup & Disconnect
  await mongoose.connection.close();
  console.log('🔌 Disconnected from MongoDB');
}

main();
```

---

## 🚀 Advanced Topics Preview (Part 2 Roadmap)

These topics build on the CRUD foundations covered in this curriculum and are typically covered in subsequent modules:

| Topic | What It Does | Why It Matters |
| :--- | :--- | :--- |
| **Aggregation Pipeline** | Multi-stage data transformation (`$match → $group → $sort → $project`) | Powers dashboards, analytics, and reporting queries |
| **Indexing** | B-Tree indexes on fields (`createIndex()`) | Turns O(N) collection scans into O(log N) index seeks |
| **Mongoose ODM** | Schema validation, middleware hooks, virtual fields | Enforces data integrity in Node.js applications |
| **MongoDB Atlas** | Cloud-hosted managed MongoDB clusters | Zero-ops deployment with backups, monitoring, and scaling |
| **Transactions** | Multi-document ACID transactions (`session.startTransaction()`) | Ensures all-or-nothing consistency across multiple writes |
| **Replica Sets** | Primary-Secondary replication for high availability | Automatic failover if the primary server crashes |
| **Sharding** | Horizontal data distribution across multiple servers | Scales reads/writes across clusters for billions of documents |
| **Change Streams** | Real-time event listeners on database changes | Powers live notifications, chat apps, and real-time dashboards |
| **Text Search** | Full-text search with `$text` and `$search` operators | Search functionality within string fields (like product names) |
| **GridFS** | File storage for objects exceeding 16MB document limit | Store and stream videos, images, and PDFs directly in MongoDB |

---

## 📚 Study Methodology & Retention Strategy

1. **Active Recall Before Checking Solutions:** Each note contains **"Predict First"** interactive accordions (`<details><summary>`). Read the problem, predict the exact output in your head, and then expand the solution.
2. **First Principles First:** Never just memorize syntax like `db.student.find({ "performance.marks": 88 })`. Understand *why* dot notation requires string quotes in JavaScript and *why* top-level queries fail on sub-documents.
3. **Execute in `mongosh`:** Every code example in these notes has been verified and tested against MongoDB 7.0+. Open your PowerShell terminal and run each command step-by-step.
4. **Lock in with the 30-Second Revision:** Before jumping to the next lecture, spend 30 seconds reviewing the summary box at the end of each note.
5. **Bridge to Backend:** After mastering each `mongosh` command, write the equivalent Mongoose code in a Node.js file. This builds muscle memory for full-stack development.
