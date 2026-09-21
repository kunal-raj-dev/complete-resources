# Lecture 02: Variables, Data Types & Operators

> **One-Line Purpose:** Understand how memory is modeled, allocated, and manipulated in C++ using primitive data types, type conversion/casting rules, and arithmetic, logical, relational, and bitwise operators.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #02  
> **Video ID:** `Dxu7GKtdbnA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Dxu7GKtdbnA)  
> **Duration:** 01:16:44  
> **Transcript:** `.transcripts/01_cpp_basics/002_Lecture_2___Variable__Data_Types___Operators___DSA_Series_by_Shradha_Ma_am___C__.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What variables are and how the operating system allocates contiguous memory blocks for them.
- The fundamental C++ primitive data types (`int`, `char`, `float`, `double`, `bool`), their storage sizes, ranges, and ASCII representations.
- How to measure memory usage using the `sizeof` operator.
- The mechanics of Implicit Type Conversion (Type Promotion) versus Explicit Type Casting (`static_cast`).
- Stream extraction using `std::cin` and why buffer handling matters.
- All operator families: Arithmetic, Relational, Logical (including short-circuit behavior), Assignment, and Unary Increment/Decrement (`++x` vs `x++`).

---

## 🔵 Lecture Context

This lecture forms the syntactic and memory foundation for all subsequent DSA implementations. In DSA, optimal memory choice (e.g., choosing `int` vs `long long` to prevent integer overflow) and avoiding common operator traps (e.g., integer division truncating decimals or unexpected side-effects in post-increment) prevent subtle bugs in competitive programming and interview coding.

---

## 1. Variables & Memory Anatomy

> 🔵 **Lecture Content**

A **variable** is a named storage location in memory. When you declare:
```cpp
int age = 25;
```
The compiler reserves 4 bytes in the computer's RAM, associates the identifier `age` with that memory address (e.g., `0x7ffee4b2`), and writes the binary pattern for `25` into those bytes.

### Identifier Naming Rules:
1. May contain letters (`a-z`, `A-Z`), digits (`0-9`), and underscores (`_`).
2. **Must not** begin with a digit (e.g., `1variable` is invalid).
3. Case-sensitive (`Age` and `age` are distinct).
4. Cannot use C++ reserved keywords (`int`, `return`, `class`, etc.).

---

## 2. Primitive Data Types in C++

| Data Type | Typical Size | Description | Range (Typical 64-bit Architecture) |
|---|---|---|---|
| `int` | 4 Bytes (32 bits) | Signed integers | $-2^{31}$ to $2^{31}-1$ ($\approx -2.14 \times 10^9$ to $+2.14 \times 10^9$) |
| `char` | 1 Byte (8 bits) | Single character stored via ASCII value | $-128$ to $127$ (or $0$ to $255$ if unsigned) |
| `float` | 4 Bytes (32 bits) | Single-precision floating point | $\approx 7$ decimal digits of precision |
| `double` | 8 Bytes (64 bits) | Double-precision floating point | $\approx 15$ decimal digits of precision |
| `bool` | 1 Byte (8 bits) | Boolean truth value (`true` or `false`) | `true` ($1$) or `false` ($0$) |

```cpp
#include <iostream>
using namespace std;

int main() {
    int age = 22;
    char grade = 'A';
    float PI = 3.14159f;
    double price = 99.9999;
    bool isPassed = true;

    cout << "sizeof(int): " << sizeof(int) << " bytes" << endl;
    cout << "sizeof(char): " << sizeof(char) << " byte" << endl;
    cout << "sizeof(float): " << sizeof(float) << " bytes" << endl;
    cout << "sizeof(double): " << sizeof(double) << " bytes" << endl;
    cout << "sizeof(bool): " << sizeof(bool) << " byte" << endl;

    return 0;
}
```

> 🧠 **Brain Trigger**
> 
> Why does a `bool` require 1 full byte (8 bits) when it only stores 0 or 1 (which mathematically requires only 1 bit)?
> 
> **Answer:** Modern computer architectures (CPU memory controllers) address memory in byte-sized chunks. A single bit cannot be directly addressed or referenced by a pointer in standard hardware.

---

## 3. Type Conversion vs Type Casting

> 🔵 **Lecture Content**

### A. Implicit Conversion (Type Promotion)
Automatic conversion performed by the compiler from a smaller data type to a larger data type to prevent data loss.
```cpp
char ch = 'A'; // ASCII value 65
int num = ch;  // Automatically promoted to int: 65

int a = 5;
double b = 2.5;
double result = a + b; // 'a' promoted to double (5.0), result = 7.5
```

### B. Explicit Casting (Type Casting)
Manually converting a type when the conversion could involve data loss or truncation.
```cpp
double price = 100.99;
int roundedPrice = (int)price; // C-style cast -> 100 (truncates decimal part)

// Modern C++ standard practice:
int modernPrice = static_cast<int>(price); 
```

---

## 4. Operators Deep Dive

### A. Arithmetic Operators
- `+`, `-`, `*`, `/`, `%`
- **Integer Division Trap:**
  ```cpp
  int a = 5, b = 2;
  cout << a / b;        // Outputs 2, NOT 2.5! (Fractional part truncated)
  cout << (double)a / b; // Outputs 2.5 (Float division)
  ```
- **Modulo Operator (`%`):** Returns the remainder of integer division. `5 % 2 = 1`. Modulo **cannot** be applied to floating-point operands in C++.

### B. Relational Operators
- `==`, `!=`, `<`, `>`, `<=`, `>=`
- Always return a Boolean result (`1` for true, `0` for false).

### C. Logical Operators & Short-Circuit Evaluation
- `&&` (AND): True if both operands are true.
- `||` (OR): True if at least one operand is true.
- `!` (NOT): Inverts truth value.

> 🔥 **Interview Extension: Short-Circuit Evaluation**
> In expression `A && B`, if `A` is `false`, `B` is **never executed**.
> In expression `A || B`, if `A` is `true`, `B` is **never executed**.
> 
> Example:

```cpp
int x = 0;
if (false && (++x > 0)) { }
cout << x; // Outputs 0! ++x was skipped entirely due to short-circuiting.
```


### D. Unary Increment (`++`) & Decrement (`--`)

| Operator | Syntax | Operation Order |
|---|---|---|
| **Pre-Increment** | `++a` | Increments `a` first, then returns the updated value. |
| **Post-Increment** | `a++` | Returns current value first, then increments `a`. |

```cpp
int a = 10;
int b = ++a; // a becomes 11, b is assigned 11

int x = 10;
int y = x++; // y is assigned 10, x becomes 11
```

---

## ⚠️ Common Mistakes

1. **Integer Division in Averages:**
   ```cpp
   int sum = 15, count = 2;
   double avg = sum / count; // BUG: sum/count evaluates to integer 7, then assigned as 7.0!
   double correctAvg = (double)sum / count; // Correct: 7.5
   ```
2. **Undefined Behavior with Multiple Unary Operators in Single Expression:**
   ```cpp
   int a = 5;
   int b = a++ + ++a; // UNDEFINED BEHAVIOR in C++ standard! Do not write this in code.
   ```
3. **Single Equals vs Double Equals:**
   ```cpp
   if (isValid = true) // Assigns true to isValid, condition always evaluates to true!
   if (isValid == true) // Correct comparison
   ```

---

## 🖥️ System-Specific Notes

- The C++ standard specifies *minimum* sizes for types, not fixed exact sizes. `sizeof(int)` is guaranteed to be at least 16 bits, but on almost all modern 32-bit and 64-bit systems, it is 32 bits (4 bytes).
- For guaranteed exact-width integer types across platforms, production code and competitive programming use `<cstdint>` (`int32_t`, `int64_t`, `uint64_t`).

---

## 🎯 Core Concept Check

**Q1:** What is the result of `sizeof('A')` in C++ versus C?  
**A:** In C++, character literals have type `char`, so `sizeof('A') == 1`. In C, character literals are promoted to `int`, so `sizeof('A') == sizeof(int)` (typically 4).

**Q2:** Can the modulo operator `%` be used with negative integers in C++?  
**A:** Since C++11, integer division truncates toward zero, and the sign of `a % b` is defined to be the sign of the dividend `a`. For example, `-7 % 3 = -1`, whereas `7 % -3 = 1`.

---

## 🔥 Interview Questions

### Q1: [Overflow Risk] How do you prevent integer overflow when computing `mid` in Binary Search?
- **Short Answer:** Use `mid = left + (right - left) / 2;` instead of `mid = (left + right) / 2;`.
- **Detailed Explanation:** When `left` and `right` are both close to $2^{31}-1$, `left + right` exceeds the maximum capacity of a 32-bit signed integer, causing signed integer overflow (Undefined Behavior, producing a negative index and subsequent segmentation fault).
- **Why Interviewers Ask:** Assesses real-world awareness of data type limits and defensive coding habits.

### Q2: [Logic & Internals] What is the difference between `(int)x` and `static_cast<int>(x)`?
- **Short Answer:** `static_cast` provides compile-time type safety checks, whereas C-style cast can blindly perform dangerous pointer reinterprets.
- **Detailed Explanation:** C-style cast attempts a combination of `const_cast`, `static_cast`, and `reinterpret_cast`. `static_cast` is explicit, searchable in codebases, and produces compile errors if an invalid conversion is attempted.

---

## 💻 Output / Debugging Questions

### Output Prediction 1
```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 5;
    int b = a++;
    int c = ++a;
    cout << a << " " << b << " " << c << endl;
    return 0;
}
```
**Output:** `7 5 7`  
**Explanation:**  
1. `b = a++`: `b` receives current value `5`, `a` increments to `6`.  
2. `c = ++a`: `a` increments to `7`, `c` receives updated value `7`.  
3. Final values: `a = 7`, `b = 5`, `c = 7`.

### Output Prediction 2
```cpp
#include <iostream>
using namespace std;

int main() {
    cout << (5 > 3 && 4 < 2 || 10 > 2) << endl;
    return 0;
}
```
**Output:** `1`  
**Explanation:** Operator precedence: `&&` has higher precedence than `||`.  
- `5 > 3` is True, `4 < 2` is False $\to$ `True && False` evaluates to False.  
- Next: `False || (10 > 2)` $\to$ `False || True` evaluates to True (`1`).

---

## Key Takeaways

1. **Type Sizing:** `char` (1 byte), `int` (4 bytes), `float` (4 bytes), `double` (8 bytes), `bool` (1 byte).
2. **Division Safety:** Always cast one operand to `double` or `float` when fractional results are expected.
3. **Pre vs Post Increment:** `++x` modifies and evaluates to the new value; `x++` evaluates to the old value and then modifies.
4. **Short-Circuit Evaluation:** Logical `&&` and `||` abort evaluation as soon as the outcome is mathematically guaranteed.

---

## ⚡ 2-Minute Revision

- **ASCII Codes to Memorize:** `'A'` = 65, `'a'` = 97, `'0'` = 48.
- **Integer Limits:** Signed 32-bit `int` holds up to $\approx 2 \times 10^9$. For calculations exceeding this (like factorials or big sums), switch to `long long` (8 bytes, up to $\approx 9 \times 10^{18}$).
- **Short-circuiting:** `false && (anything)` will not evaluate `anything`; `true || (anything)` will not evaluate `anything`.
- **Casting:** Prefer `static_cast<target_type>(val)` in C++ over C-style `(target_type)val`.
