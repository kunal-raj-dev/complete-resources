# Topic 04 Revision: Pointers & Memory Management

> **High-Density Revision Guide:** Pointers, addresses, indirection, and arithmetic rules.

---

## 1. Syntax & Core Operators
- `&x`: Address-of operator (returns hexadecimal RAM address of `x`).
- `*ptr`: Dereference operator (accesses memory at address `ptr`).
- `int** dptr = &ptr`: Double pointer storing address of pointer `ptr`.
- `nullptr`: Modern C++11 keyword; type-safe, cannot be confused with integer 0.

---

## 2. Pointer Arithmetic Rules
- `ptr + 1` adds `sizeof(*ptr)` bytes to the memory address.
- If `ptr` is `int*` at `0x100`, `ptr + 1` is `0x104`.
- If `ptr` is `double*` at `0x100`, `ptr + 1` is `0x108`.
- `ptr2 - ptr1`: Returns the **count of elements** between the pointers, not raw bytes.

---

## 3. Arrays vs Pointers
- `arr` is an immutable base address pointer: `arr == &arr[0]`.
- `arr[i] \equiv *(arr + i) \equiv i[arr]`.
- `arr++` is a **compiler error**; `ptr++` is valid.
- In functions, `int arr[]` decays completely into `int* arr`.

---

## 4. References vs Pointers
- **References (`&`):** Must be initialized when declared; cannot be `nullptr`; cannot be reseated to another variable; syntax identical to normal variables.
- **Pointers (`*`):** Can be uninitialized or `nullptr`; can be reseated dynamically; requires explicit dereferencing (`*`).
