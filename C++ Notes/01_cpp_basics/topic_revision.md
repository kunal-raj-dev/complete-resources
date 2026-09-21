# Topic 01 Revision: C++ Basics & Fundamentals

> **High-Density Revision Guide:** Core concepts, memory models, compilation stages, operator behaviors, and fundamental patterns.

---

## 1. Core Architecture & Compilation
- **Compilation Pipeline:** Source Code (`.cpp`) $\to$ **Preprocessor** (expands macros/includes) $\to$ **Compiler** (generates assembly `.s`) $\to$ **Assembler** (generates object code `.o`/`.obj`) $\to$ **Linker** (resolves symbols and standard library code) $\to$ **Executable** (`.exe`).
- **Standard Entry Point:** `int main()` must return an exit code integer to the operating system shell (`0` indicates success).
- **Streams:** `std::cin` extracts bytes from input buffer; `std::cout` inserts bytes into output buffer. `std::endl` appends `'\n'` and forces a costly buffer flush. Prefer `'\n'`.

---

## 2. Memory Types & Primitive Sizing

| Type | Typical Size | Typical Range | Key Traps |
|---|---|---|---|
| `bool` | 1 Byte | `0` or `1` | Cannot address individual bits; uses 1 full byte. |
| `char` | 1 Byte | $-128 \dots 127$ / $0 \dots 255$ | ASCII based (`'A'=65`, `'a'=97`, `'0'=48`). |
| `int` | 4 Bytes | $-2.14 \times 10^9 \dots +2.14 \times 10^9$ | Overflows past $2^{31}-1$. Use `long long` for large sums. |
| `float` | 4 Bytes | $\approx 7$ decimal digits | IEEE 754 precision issues; never use as loop counter. |
| `double` | 8 Bytes | $\approx 15$ decimal digits | Standard floating-point type for mathematical computations. |

---

## 3. Critical Operator Rules & Gotchas
1. **Integer Division:** `int / int` truncates fractional parts toward zero (`5 / 2 = 2`). Cast one operand to `double` for decimal division (`(double)5 / 2 = 2.5`).
2. **Modulo:** Only valid on integers. The sign of `a % b` is determined by dividend `a`.
3. **Short-Circuit Evaluation:**
   - In `A && B`: if `A` is false, `B` is not evaluated.
   - In `A || B`: if `A` is true, `B` is not evaluated.
4. **Unary Increment:**
   - `++x` (Pre-increment): Increment first, then return new value.
   - `x++` (Post-increment): Return old value, then increment.
   - Multiple unsequenced modifications like `x++ + ++x` are **Undefined Behavior**.

---

## 4. Control Flow & Loop Invariants
- **`switch` Optimization:** Can be compiled into an $O(1)$ Jump Table if case constants are dense integers. Requires `break` to avoid unintended fallthrough.
- **`do-while` Guarantee:** Guarantees body execution at least once because condition is evaluated at exit.
- **`continue` in `while` Trap:** Must ensure iterator increment occurs before `continue` statement to prevent infinite looping.
- **Optimized Primality:** Check divisors only up to $\lfloor\sqrt{N}\rfloor$ ($O(\sqrt{N})$) because factors always appear in complementary pairs $(d, N/d)$.

---

## 5. Functions & Call Stack Anatomy
- **Stack Frame:** Allocated on the call stack per function invocation. Contains formal parameter copies, local variables, and the return instruction address.
- **Pass-by-Value:** Default parameter mechanism in C++. Operates on an isolated copy in the local frame.
- **Dangling Pointer Warning:** Never return a pointer or reference to a local stack variable; the memory is reclaimed immediately upon function exit.
- **$nCr$ Optimization:** Compute iteratively with running division: $\prod_{i=1}^r \frac{n - r + i}{i}$ to prevent premature integer overflow from full factorials.
