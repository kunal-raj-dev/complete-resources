# ⚡ Rapid Revision — Topic 07: C++ STL

> **Target:** 5-minute pre-interview refresher on STL complexity guarantees and container selection.

---

## 🔑 Container Selection Cheatsheet
- Need random access + fast push_back: `std::vector`.
- Need fast push/pop at both ends: `std::deque`.
- Need fast sorted lookup / uniqueness: `std::set` ($O(\log N)$).
- Need fastest key-value lookup: `std::unordered_map` ($O(1)$ avg).
- Need maximum or minimum priority access: `std::priority_queue` ($O(\log N)$ push/pop).
