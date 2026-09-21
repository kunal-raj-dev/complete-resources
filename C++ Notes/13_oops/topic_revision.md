# ⚡ Rapid Revision — Topic 13: OOPs in C++

> **Target:** 5-minute pre-interview refresher on C++ OOP concepts and system design questions.

---

## 🔑 Quick Rule Refresher
- **Shallow Copy:** Bitwise copy; triggers double-free when pointers exist.
- **Deep Copy:** Allocate separate heap buffer and copy dereferenced values.
- **`vptr` & `vtable`:** Enables dynamic dispatch for `virtual` functions (costs 8 bytes per object for pointer).
- **Abstract Class:** Class containing at least one pure virtual function (`= 0`).
- **Diamond Problem:** Solved by `class B : virtual public A`.
