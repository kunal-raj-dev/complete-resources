# Lecture 07: Bitwise Operators & Data Type Modifiers

> **One-Line Purpose:** Master bit-level operations (`&`, `|`, `^`, `~`, `<<`, `>>`), data type modifiers (`unsigned`, `long long`), and essential interview bit manipulation algorithms (Power of 2, Single Number, Brian Kernighan's count).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #07  
> **Video ID:** `r-u4uh3QvsQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=r-u4uh3QvsQ)  
> **Duration:** 38:33  
> **Transcript:** `.transcripts/02_bitwise_number_systems/007_Bitwise_Operators__Data_Type_Modifiers___more___DSA_Series_by_Shradha_Khapra_Ma_am.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The exact truth tables and binary execution of bitwise operators: `&`, `|`, `^`, `~`, `<<`, and `>>`.
- The mathematical equivalence of bit shifts: $a \ll b = a \times 2^b$ and $a \gg b = \lfloor a / 2^b \rfloor$.
- Operator precedence traps when combining bitwise and relational operators.
- C++ Data Type Modifiers: `unsigned`, `signed`, `short`, `long`, and `long long`.
- Core FAANG Bit Manipulation Algorithms:
  - Checking if a number is a Power of 2 ($O(1)$).
  - Isolating the unique element via XOR cancellation ($O(N)$ time, $O(1)$ space).
  - Counting set bits via Brian Kernighan's Algorithm.

---

## 🔵 Lecture Context

Bitwise manipulation operates directly on CPU register registers in single-cycle clock instructions. In technical interviews, bitwise tricks frequently replace auxiliary hash maps or loops, reducing $O(N)$ space solutions to $O(1)$ memory.

---

## 1. Bitwise Operators Deep Dive

> 🔵 **Lecture Content**

| Operator | Name | Syntax | Description | Example (A = 5 [0101], B = 3 [0011]) |
|---|---|---|---|---|
| `&` | Bitwise AND | `A & B` | 1 only if **both** bits are 1 | `0101 & 0011 = 0001` (1) |
| `\|` | Bitwise OR | `A \| B` | 1 if **at least one** bit is 1 | `0101 \| 0011 = 0111` (7) |
| `^` | Bitwise XOR | `A ^ B` | 1 if bits are **different**; 0 if same | `0101 ^ 0011 = 0110` (6) |
| `~` | Bitwise NOT | `~A` | Inverts all bits ($0 \to 1, 1 \to 0$) | `~5 = -6` (in 2's complement: `~x = -(x + 1)`) |
| `<<` | Left Shift | `A << k` | Shifts bits left by $k$, filling with 0s | `5 << 1 = 10` ($5 \times 2^1$) |
| `>>` | Right Shift | `A >> k` | Shifts bits right by $k$ | `5 >> 1 = 2` ($\lfloor 5 / 2^1 \rfloor$) |

---

## 2. Fundamental Properties of XOR (`^`)

The XOR operator is one of the most powerful tools in DSA:
1. **Self-Inverse:** $A \oplus A = 0$
2. **Identity:** $A \oplus 0 = A$
3. **Commutative & Associative:** $A \oplus B \oplus C = B \oplus A \oplus C$

### Application: Single Number (LeetCode 136)
**Problem:** Given a non-empty array of integers where every element appears twice except for one unique element, find that unique element.

```cpp
#include <vector>
#include <iostream>
using namespace std;

int singleNumber(const vector<int>& nums) {
    int unique = 0;
    for (int num : nums) {
        unique ^= num; // Duplicate pairs cancel each other out to 0!
    }
    return unique;
}
```
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$ (Direct optimal upgrade over $O(N)$ hash map approach).

---

## 3. Core Bitwise Algorithms

> 🔵 **Lecture Content & Interview Extension**

### A. Check if a Number is a Power of 2 (LeetCode 231)
A number $N$ is a power of 2 if and only if its binary representation has **exactly one set bit** (e.g., $4 = 100_2$, $8 = 1000_2$, $16 = 10000_2$).

When you subtract 1 from $N$, that single set bit becomes 0, and all trailing bits become 1:
$$N = 8 = 1000_2$$
$$N - 1 = 7 = 0111_2$$
$$N \ \& \ (N - 1) = 1000_2 \ \& \ 0111_2 = 0000_2$$

```cpp
bool isPowerOfTwo(int n) {
    return (n > 0) && ((n & (n - 1)) == 0);
}
```

> ⚠️ **Precedence Trap:**
> Relational operator `==` has higher precedence than bitwise `&`!
> Writing `n & (n - 1) == 0` is parsed as `n & ((n - 1) == 0)`. **Always enclose bitwise expressions in parentheses: `((n & (n - 1)) == 0)`.**

---

### B. Brian Kernighan's Algorithm (Count Set Bits / LeetCode 191)
The expression `n = n & (n - 1)` clears the **lowest set bit** of `n` in $O(1)$ time.

```cpp
int countSetBits(int n) {
    int count = 0;
    while (n > 0) {
        n = n & (n - 1); // Clears the least significant set bit
        count++;
    }
    return count;
}
```
- **Complexity:** $O(\text{number of set bits})$. Runs in at most 32 iterations for 32-bit integers.

---

## 4. C++ Data Type Modifiers

Modifiers alter the meaning and memory range of fundamental types.

| Modifier | Target Type | Effect on Size & Range |
|---|---|---|
| `unsigned` | `int`, `char`, `long` | Disallows negative numbers. Doubles the positive capacity ($0 \dots 2^{32}-1 \approx 4.29 \times 10^9$ for `int`). |
| `signed` | `int`, `char`, `long` | Default. Preserves negative and positive range via 2's complement. |
| `short` | `int` | At least 16 bits (2 bytes). Range: $-32,768 \dots +32,767$. |
| `long` | `int` | At least 32 bits (4 bytes). |
| `long long` | `int` | At least 64 bits (8 bytes). Range: $\approx -9 \times 10^{18} \dots +9 \times 10^{18}$. |

```cpp
long long bigNumber = 9000000000000000000LL; // Note 'LL' literal suffix
unsigned int positiveOnly = 4000000000U;
```

---

## ⚠️ Common Mistakes

1. **Negative Bit Shifts:** In C++, shifting by a negative count (e.g., `x << -1`) or by $\ge$ the bit-width of the type (e.g., `(int)x << 32`) is **Undefined Behavior**.
2. **Right-Shifting Negative Numbers:** Shifting a signed negative integer right (`x >> 1`) performs an **Arithmetic Shift** (copies MSB sign bit 1), not a Logical Shift. For logical 0-fill shifts, cast to `unsigned`.

---

## 🔥 Interview Questions

### Q1: How do you swap two variables without using a temporary variable?
- **Code:**
  ```cpp
  a = a ^ b;
  b = a ^ b; // b becomes (a ^ b) ^ b = a
  a = a ^ b; // a becomes (a ^ b) ^ a = b
  ```
- **Caution:** If `&a == &b` (both point to the identical memory address), `a ^ a` sets the variable to 0.

### Q2: How do you isolate the lowest set bit of an integer?
- **Formula:** `lowestSetBit = x & (-x);`
- **Explanation:** In 2's complement, `-x = ~x + 1`. This flips all bits above the lowest set bit and preserves the lowest set bit, so `x & (-x)` isolates that single bit.

---

## Key Takeaways

1. **XOR Magic:** Cancels pairs ($X \oplus X = 0$), extracts unique values.
2. **Shift Equivalences:** `x << k` is $x \times 2^k$; `x >> k` is $\lfloor x / 2^k \rfloor$.
3. **Power of 2 Trick:** `(n > 0) && ((n & (n - 1)) == 0)`.
4. **Kernighan's Speed:** `n & (n - 1)` clears lowest set bit in a single step.

---

## ⚡ 2-Minute Revision

- `x & 1`: Checks if least significant bit is 1 (True if odd, False if even).
- `1 << k`: Generates a mask with only the $k$-th bit set ($2^k$).
- `n & (1 << k)`: Tests if the $k$-th bit of `n` is set.
- `n | (1 << k)`: Sets the $k$-th bit of `n`.
- `n & ~(1 << k)`: Clears the $k$-th bit of `n`.
- `n ^ (1 << k)`: Toggles the $k$-th bit of `n`.
