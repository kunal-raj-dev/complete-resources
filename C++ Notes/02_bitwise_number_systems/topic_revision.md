# Topic 02 Revision: Bitwise Operations & Number Systems

> **High-Density Revision Guide:** Binary representations, 2's complement, bitwise arithmetic, and core bit manipulation idioms.

---

## 1. Positional Bases & 2's Complement
- **Value Equation:** $\sum d_i \times 2^i$.
- **Two's Complement:** Formula: $-X = \sim X + 1$.
- **Why 2's Complement?** Eliminates negative zero (`+0` vs `-0`), allowing addition and subtraction to share a single CPU circuit.
- **Asymmetric Range:** $n$ signed bits span $[-2^{n-1}, 2^{n-1}-1]$. For 32-bit `int`: $[-2,147,483,648, +2,147,483,647]$.

---

## 2. Bitwise Operators Cheat Sheet

| Operation | C++ Syntax | Core Property |
|---|---|---|
| **AND** | `a & b` | $1$ only if both bits are $1$. Used for masking. |
| **OR** | `a \| b` | $1$ if either bit is $1$. Used for setting bits. |
| **XOR** | `a ^ b` | $1$ if bits differ. Properties: $A \oplus A = 0$, $A \oplus 0 = A$. |
| **NOT** | `~a` | Inverts all bits. $\sim a = -(a + 1)$ in 2's complement. |
| **Left Shift** | `a << k` | Multiplies by $2^k$ (shifts left, zeroes fill right). |
| **Right Shift** | `a >> k` | Divides by $2^k$ (arithmetic shift preserves sign for signed types). |

---

## 3. High-Frequency Bitwise Idioms
- **Check Odd / Even:** `(n & 1) != 0` (True if odd).
- **Check Power of 2:** `(n > 0) && ((n & (n - 1)) == 0)`.
- **Clear Lowest Set Bit:** `n = n & (n - 1)`.
- **Isolate Lowest Set Bit:** `lowest = n & (-n)`.
- **Check $k$-th Bit:** `(n & (1 << k)) != 0`.
- **Set $k$-th Bit:** `n |= (1 << k)`.
- **Clear $k$-th Bit:** `n &= ~(1 << k)`.
- **Toggle $k$-th Bit:** `n ^= (1 << k)`.
- **Single Number Problem:** XOR all array elements together $\to$ duplicate pairs cancel to $0$, leaving the unique element ($O(N)$ time, $O(1)$ space).

---

## 4. C++ Data Type Modifiers
- `unsigned`: Non-negative values only. Extends 32-bit integer range to $\approx 4.29 \times 10^9$.
- `long long`: Guaranteed at least 64 bits ($\approx \pm 9 \times 10^{18}$). Must use `LL` suffix for literals (`1LL << k`).
