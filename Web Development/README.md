# 🌐 Web Development — Complete Interview-Ready Knowledge Base

> A comprehensive, production-grade knowledge base covering modern web development, browser engineering, JavaScript language semantics, DOM manipulation, asynchronous architecture, and frontend systems.

---

## 📂 Modules & Learning Paths

### 🔹 [JavaScript Notes](./JavaScript%20Notes/README.md)
A lecture-derived, interview-grade JavaScript curriculum built from Anurag Singh's *Complete JavaScript Course (ProCodrr)*.

- **Total In-Depth Notes:** **43 Complete Lectures**
- **Master Guide & Manifest:** **[00-master-index.md](./JavaScript%20Notes/00-master-index.md)**
- **Coverage:**
  1. **Module 01: Core JavaScript Fundamentals (Ep. 01 – Ep. 25)**
     - V8 Engine Architecture (Ignition & TurboFan), Script Linking (`defer` vs `async`), 7 Primitives vs Objects, Variable Scoping (`let`, `const`, `var`), Temporal Dead Zone (TDZ).
     - Chrome DevTools Line-by-Line Stepping, Scope Chains (Global vs Script vs Block), Memory Heap Profiling (`@id`), Shallow Size vs Retained Size.
     - Operators, Implicit & Relational Type Coercion, Decision-Making (`if-else`, `switch`, `ternary`), Object References, Shallow vs Deep Cloning (`structuredClone`), While Loops & Two-Pointers.
  2. **Module 08: DOM, Modern Events Architecture & Web Storage (Ep. 51 – Ep. 68)**
     - Critical Rendering Path (CRP), DOM & CSSOM Tree Construction, Render Tree, Layout (Reflow) & Paint (Repaint) Costs.
     - Element Selectors (`getElementById` vs `querySelector`), Live `HTMLCollection` vs Static `NodeList`, `innerText` vs `textContent` (Layout flushes & XSS prevention).
     - HTML Attributes vs Live DOM Properties, `classList` API, Element vs Node Traversal (`parentElement`, `children`, `nodeType`), `append` vs `appendChild`, `DocumentFragment` batching, Detached DOM Tree Memory Leaks.
     - Event Listener Subsystem, Observer Pattern, Event Objects (`e.target` vs `e.currentTarget`), Keyboard Events (`e.code` vs `e.key`), Pointer Events API.
     - 3-Phase Event Propagation (Capturing, Target, Bubbling), `stopPropagation()` vs `stopImmediatePropagation()`, Event Delegation (`e.target.closest`), Synthetic Event Simulation (`isTrusted`, `form.requestSubmit()`).
     - Web Storage API (`localStorage` vs `sessionStorage`), Same-Origin Policy, ~5MB Quota, JSON Serialization Traps, XSS Security Boundaries.

---

### 🔹 [MongoDB Notes](./mongoDB%20Notes/README.md)
A comprehensive, industry-standard MongoDB curriculum built from Shradha Khapra's *Delta Batch (Web Development) — 44. MongoDB (Part 1)*.

- **Total In-Depth Notes:** **10 Complete Lectures (Ep. 01 – Ep. 10)**
- **Master Guide & Manifest:** **[00-master-index.md](./mongoDB%20Notes/00-master-index.md)**
- **Coverage:**
  1. **Phase 1: Architecture & Data Storage (Ep. 01 – Ep. 03)**: `mongod` daemon, `mongosh` Node.js REPL, default port 27017, database contexts (`use db`, `db`, `show dbs`), BSON vs JSON binary serialization, 16MB document boundary, 12-byte `ObjectId` anatomy, SQL-to-MongoDB mapping, dynamic polymorphic schemas.
  2. **Phase 2: CRUD: Create Operations & Bulk Ingestion (Ep. 04 – Ep. 05)**: `insertOne()`, lazy collection allocation, dynamic schemas, `insertMany([])`, network round-trip batch optimization, `ordered: true` vs `ordered: false` execution semantics.
  3. **Phase 3: CRUD: Read Operations & Query Selectors (Ep. 06 – Ep. 07)**: `find()` vs `findOne()`, cursor streaming, batch iteration (`it`), query projections, Comparison operators (`$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$ne`), Logical operators (`$or`, `$and`, `$not`, `$nor`), implicit vs explicit AND.
  4. **Phase 4: CRUD: Update, Nesting, & Delete Operations (Ep. 08 – Ep. 10)**: `updateOne()`, `updateMany()`, `replaceOne()`, field modifiers (`$set`, `$unset`, `$inc`, `$rename`, `$currentDate`), upsert pattern (`upsert: true`), embedded sub-documents, dot notation syntax (`"parent.child"`), surgical nested updates, `deleteOne()`, `deleteMany()`, `deleteMany({})` vs `drop()`, `dropDatabase()`, and WiredTiger storage reclamation.

---

## 🗺️ Architectural Structure

```text
Web Development/
│
├── README.md                          # Web Development Track Guide
├── JavaScript Notes/
│   ├── README.md                      # JavaScript Notes Directory Guide
│   ├── 00-master-index.md             # Complete Master Manifest & Study Roadmap
│   └── 01-story-of-javascript.md ... 68-local-storage-explained-in-depth.md
└── mongoDB Notes/
    ├── README.md                      # MongoDB Notes Directory Guide & Quickstart
    ├── 00-master-index.md             # 10-Episode Master Index, Syntax Cheat Sheet & FAANG Bank
    └── 01-the-mongo-shell.md ... 10-delete-in-db-and-drop-database.md
```

---

## 🎯 Pedagogical Standards

Every lesson in this knowledge base strictly adheres to the **14-Section Progressive Learning Architecture**:
- Intuitive mental models & real-world analogies
- Smallest reproducible code examples
- Step-by-step state traces & ASCII memory diagrams
- Common mistakes & anti-pattern debugging matrices
- "Predict First" output challenge questions with expandable explanations
- Specification guarantees vs engine implementation details
- Standardized ⚡ 30-Second Revision summaries (5 core pillars)
- Hands-on practice tasks & interview readiness checklists
