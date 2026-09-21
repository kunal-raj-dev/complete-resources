# Topic 01 Interview Questions: C++ Basics & Fundamentals

> **Curated Question Bank:** High-frequency technical interview questions, conceptual traps, debugging puzzles, and implementation challenges with detailed solutions.

---

## 📌 Conceptual & Architectural Questions

### Q1: What is the exact difference between a Declaration and a Definition in C++?
- **Short Answer:** A declaration announces the existence and type signature of a symbol to the compiler, while a definition actually allocates memory or provides the implementation body.
- **Detailed Explanation:**
  ```cpp
  extern int x;     // Declaration: informs compiler x exists somewhere, no memory allocated
  int x = 10;       // Definition: allocates 4 bytes in data segment and initializes it
  
  int add(int, int); // Declaration: function prototype
  int add(int a, int b) { return a + b; } // Definition: provides machine code body
  ```
- **Interview Relevance:** Fundamental C++ syntax question testing understanding of compilation modularity.

---

### Q2: Why is `std::endl` considered harmful in performance-sensitive applications or competitive programming?
- **Short Answer:** `std::endl` inserts a newline character AND explicitly flushes the underlying stream buffer, causing substantial I/O overhead.
- **Detailed Explanation:** In standard output streams, data is buffered in memory and flushed in blocks (usually 4KB or 8KB) or when the OS decides. Using `std::endl` forces a system call (`write` in UNIX, `WriteFile` in Windows) on every invocation. In tight loops (e.g., printing $10^5$ elements), this can turn an $O(N)$ CPU operation into an I/O bottleneck that takes seconds rather than milliseconds.
- **Trap / Follow-up:** What should you use instead?
  - **Answer:** Use `'\n'`. To achieve fast I/O in competitive programming, pair with `ios_base::sync_with_stdio(false); cin.tie(NULL);`.

---

### Q3: What happens when signed integer overflow occurs in C++?
- **Short Answer:** Signed integer overflow is **Undefined Behavior (UB)** according to the ISO C++ standard.
- **Detailed Explanation:** Unlike unsigned arithmetic (which is strictly defined to wrap around modulo $2^W$), signed overflow has no standard guarantee. Modern optimizing compilers (GCC, Clang) assume that signed overflow *never* happens and may optimize away boundary checks like `if (x + 1 > x)` entirely.
- **Interview Trap:** Assuming that `INT_MAX + 1 == INT_MIN`. While this happens on standard 2's complement hardware without optimizations, relying on it in C++ is a catastrophic bug due to compiler optimizations.

---

## 💻 Output Prediction & Debugging Questions

### Q4: [Debugging] Identify the bug in the following factorial code:
```cpp
int factorial(int n) {
    int res = 1;
    for (int i = 1; i <= n; i++) {
        res *= i;
    }
    return res;
}
```
- **Bug Analysis:** For $n \ge 13$, $13! = 6,227,020,800$, which strictly exceeds the maximum capacity of a 32-bit signed `int` ($2^{31}-1 \approx 2.14 \times 10^9$). The computation silently overflows, yielding negative or corrupted values.
- **Correction:** Use `long long` (which safely supports up to $20!$), and implement an error check for $n < 0$.

---

### Q5: [Output Prediction] What does this code print?
```cpp
#include <iostream>
using namespace std;

int main() {
    int x = 1;
    if (x-- == 1) {
        cout << "A ";
    }
    if (--x == -1) {
        cout << "B ";
    }
    cout << x;
    return 0;
}
```
- **Output:** `A B -1`
- **Trace:**
  1. `x-- == 1`: Post-decrement evaluates `x` (1) first. `1 == 1` is True $\to$ prints `"A "`. After comparison, `x` decrements to `0`.
  2. `--x == -1`: Pre-decrement decrements `x` first from `0` to `-1`. Then evaluates `-1 == -1` (True) $\to$ prints `"B "`.
  3. `cout << x`: Prints current value `-1`.

---

## 🎯 Implementation & Edge-Case Questions

### Q6: Write an optimal function to calculate Binomial Coefficient $nCr$ without causing premature integer overflow.
```cpp
#include <iostream>
using namespace std;

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    if (r == 0 || r == n) return 1;

    // Utilize symmetry: nCr == nC(n - r)
    if (r > n - r) {
        r = n - r;
    }

    long long result = 1;
    for (int i = 1; i <= r; i++) {
        result *= (n - r + i);
        result /= i; // Guaranteed to divide evenly at every step
    }
    return result;
}

int main() {
    cout << "10C3 = " << nCr(10, 3) << endl; // Prints 120
    cout << "50C2 = " << nCr(50, 2) << endl; // Prints 1225
    return 0;
}
```
- **Why this works:** The product of any $k$ consecutive integers is always divisible by $k!$. Thus, dividing by $i$ at each step always produces an integer result, preventing unnecessary accumulation of huge intermediate numerators.
- **Complexity:** Time: $O(r)$, Space: $O(1)$.
