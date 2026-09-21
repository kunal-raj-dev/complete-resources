# Topic 04 Interview Questions: Pointers & Memory Management

> **Curated Question Bank:** Systems programming questions, pointer puzzles, and memory safety edge cases.

---

## 📌 Pointers Interview Question Bank

### Q1: What is a Dangling Pointer, a Wild Pointer, and a Memory Leak?
- **Wild Pointer:** A pointer that has not been initialized to anything (contains random garbage memory address).
- **Dangling Pointer:** A pointer pointing to a memory location that has been deleted, freed, or whose variable has gone out of scope (e.g. stack frame popped).
- **Memory Leak:** Memory allocated on the Heap (`new` or `malloc`) that is no longer accessible by any pointer, but has not been freed with `delete` or `free`.

---

### Q2: What is the output of the following C++ snippet?
```cpp
#include <iostream>
using namespace std;

int main() {
    int arr[] = {10, 20, 30, 40};
    int* ptr = arr;

    cout << *ptr++ << " ";
    cout << *ptr << " ";
    cout << *++ptr << " ";
    return 0;
}
```
- **Output:** `10 20 30`
- **Trace:**
  1. `*ptr++`: Post-increment has higher precedence than `*`, but yields the original `ptr` for dereferencing first. Evaluates `*ptr` (10), prints `10`, then `ptr` increments to point to `arr[1]`.
  2. `*ptr`: Dereferences current position `arr[1]` (20). Prints `20`.
  3. `*++ptr`: Pre-increment increments `ptr` first to point to `arr[2]`, then dereferences. Prints `30`.

---

### Q3: Why is `i[arr]` valid C++ syntax and equal to `arr[i]`?
- **Short Answer:** Because `arr[i]` is defined by the C/C++ language standard as `*(arr + i)`.
- **Explanation:** Addition is commutative: `arr + i == i + arr`. Therefore:
  $$arr[i] \equiv *(arr + i) \equiv *(i + arr) \equiv i[arr]$$
  While valid, writing `i[arr]` is bad practice as it confuses maintainers. Interviewers ask this to test deep knowledge of array-pointer translation mechanics.

---

### Q4: What is a `void*` (Generic Pointer) and what are its restrictions?
- **Short Answer:** A pointer that can point to any data type without type information.
- **Restrictions:**
  1. It **cannot be dereferenced** directly (`*vptr` is a compile error) because the compiler does not know the size of the underlying type.
  2. It **cannot undergo pointer arithmetic** (`vptr++` is invalid in standard C++) because step size cannot be determined. It must be explicitly cast to a concrete type first (e.g., `static_cast<int*>(vptr)`).
