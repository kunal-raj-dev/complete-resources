# 🚀 C++ & DSA — Interview-Ready Knowledge Base

> **Primary Revision & Placement Preparation Repository:** A lecture-derived, interview-grade knowledge base built from the [Complete C++ DSA Course | Apna College](https://youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt&si=KuxJx7f5ootw2zs-) taught by Shradha Khapra.

---

## 📌 Repository Overview

This repository is designed to replace passive video re-watching with an active, structured study environment. Every lecture note is derived directly from the instructor's actual lecture explanations, timestamped raw transcripts, and code demonstrations, augmented with essential conceptual context and FAANG-level interview questions.

---

## 📂 Architecture & Directory Structure

```text
C++ DSA - Interview Notes/
│
├── README.md                          # Repository guide, architecture & resume instructions
├── 00_course_master_index.md          # Complete 144-lecture manifest with live note links & status
├── 01_course_roadmap.md               # Visual multi-phase curriculum roadmap
├── 02_complete_interview_bank.md      # Long-term C++ & DSA master interview question bank
├── 03_rapid_revision.md               # High-density 24h pre-interview revision cheat sheet
├── course_concept_map.md              # Prerequisite and cross-topic concept dependency graph
├── playlist_manifest.json             # Complete YouTube playlist inventory (144 lectures)
├── processing_manifest.json           # Real-time pipeline processing and audit ledger
│
├── 01_cpp_basics/                     # Topic 1: Flowchart, Datatypes, Loops, Patterns, Functions
├── 02_bitwise_number_systems/         # Topic 2: Binary Conversions, 2's Complement, Bitwise Tricks
├── 03_arrays_and_vectors/             # Topic 3: Contiguous Memory, Kadane, Moore, 2-Pointers, Prefix/Suffix
├── 04_pointers/                       # Topic 4: Addresses, Dereferencing, Double Pointers, Pointer Math
├── 05_binary_search/                  # Topic 5: Iterative & Recursive Halving, Rotated & Mountain Arrays
├── 12_recursion_and_backtracking/     # Topic 12: Subsets, Permutations, N-Queens, Sudoku, Merge/Quick Sort
├── 14_linked_list/                    # Topic 14: Singly, Doubly, Circular Lists, Floyd's Cycle, LRU Cache
│
├── .transcripts/                      # Timestamped raw audio/caption audit trail
│   ├── 01_cpp_basics/
│   ├── 02_bitwise_number_systems/
│   ├── 03_arrays_and_vectors/
│   ├── 04_pointers/
│   └── 05_binary_search/
│
├── .scripts/                          # Pipeline automation, manifest generator, and audit scripts
└── .temp/                             # Scratch space for temporary processing
```

---

## 🏷️ Three-Tier Content Hierarchy

To maintain transparency between what was spoken in the lecture and supplementary material, every note enforces strict callout categorization:

1. `> 🔵 **Lecture Content**`: Direct representation of what the instructor explained, demonstrated, or coded.
2. `> 🟡 **Additional Essential Context**`: Critical conceptual theory, mathematical proofs, or standard language rules necessary to fully understand the topic.
3. `> 🔥 **Interview Extension**`: FAANG interview follow-ups, competitive programming edge cases, and time/space optimizations.

---

## 🔄 Resume Mechanism & Updating Notes

The repository is built with **full resume support** driven by `playlist_manifest.json` and `processing_manifest.json`.

### How to Run / Resume Processing:
If processing is interrupted (such as by YouTube rate limiting `HTTP 429` / `IpBlocked`):
1. **Check Manifest:** Open `playlist_manifest.json` or `processing_manifest.json` to inspect current lecture states.
2. **Fetch Pending Transcripts:**
   ```bash
   python .scripts/fetch_transcripts.py
   ```
   The script automatically skips lectures that already possess a valid non-empty transcript in `.transcripts/`.
3. **Re-generate / Audit Notes:** Run the audit pipeline scripts in `.scripts/` to generate or upgrade newly acquired lectures.
4. **Update Master Indexes:**
   ```bash
   python .scripts/generate_master_index.py
   ```

---

## 📊 Inventory & Verification Audit Summary

- **Total Videos Discovered:** **144**
- **Lectures Fully Audited & Note-Generated:** **44**
  - **Topic 01 (C++ Basics):** 5 Lectures (01 to 05)
  - **Topic 02 (Bitwise Operations):** 2 Lectures (06 to 07)
  - **Topic 03 (Arrays & Vectors):** 8 Lectures (08 to 15)
  - **Topic 04 (Pointers):** 1 Lecture (16)
  - **Topic 05 (Binary Search):** 3 Lectures (17 to 19)
  - **Topic 12 (Recursion & Backtracking):** 13 Lectures (42 to 51, 53 to 55)
  - **Topic 14 (Linked List):** 12 Lectures (57 to 67, 78)
- **Lectures Blocked by YouTube IP Rate Limit (429):** **100**
  - *Note:* Under Section 4 of engineering instructions, **no fake content was fabricated**. Blocked lectures remain safely queued in `processing_manifest.json` for resume processing.
- **Raw Timestamped Transcripts Stored:** 19 files in `.transcripts/`
- **Topic Master Indexes Generated:** 7
- **Topic Revision Sheets Generated:** 7
- **Topic Interview Question Banks Generated:** 7
- **Root Synthesis Documents Generated:** 5 (`00_course_master_index.md`, `01_course_roadmap.md`, `02_complete_interview_bank.md`, `03_rapid_revision.md`, `course_concept_map.md`)
