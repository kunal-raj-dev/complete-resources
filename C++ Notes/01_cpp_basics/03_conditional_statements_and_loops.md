# Lecture 03: Conditional Statements & Loops

> **One-Line Purpose:** Master branching control flow (`if-else`, ternary, `switch`) and iterative execution models (`while`, `for`, `do-while`) along with jump controls (`break`, `continue`) and algorithmic loop termination patterns.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #03  
> **Video ID:** `qR9U6bKxJ7g`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=qR9U6bKxJ7g)  
> **Duration:** 01:34:39  
> **Transcript:** `.transcripts/01_cpp_basics/003_Lecture_3__Conditional_Statements___Loops___DSA_Series_by_Shradha_Ma_am___C__.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The execution mechanics of single-branch (`if`), dual-branch (`if-else`), and multi-branch (`if-else if-else`) constructs.
- How the Ternary Operator (`?:`) functions as an expression rather than a statement.
- The semantics of the `switch-case` statement, fallthrough behavior, and why `break` is critical.
- Differences between entry-controlled loops (`while`, `for`) and exit-controlled loops (`do-while`).
- Precise execution timing of `continue` and `break` across loop variants.
- Practical problems solved in the lecture: Case character identification, sum of odd numbers from 1 to $N$, and primality test with early termination.

---

## 🔵 Lecture Context

Branching and looping are the fundamental primitives of algorithmic control flow. In DSA, virtually every search, traversal, sorting, and state-machine algorithm relies on conditional looping. Understanding boundary conditions and loop invariants prevents off-by-one errors and infinite loop deadlocks in technical interviews.

---

## 1. Conditional Branching Constructs

> 🔵 **Lecture Content**

### A. The `if - else if - else` Ladder
Evaluates conditions sequentially from top to bottom. The first condition that evaluates to `true` executes its corresponding block, bypassing all remaining branches.

```cpp
#include <iostream>
using namespace std;

int main() {
    int score = 85;

    if (score >= 90) {
        cout << "Grade: A" << endl;
    } else if (score >= 80) {
        cout << "Grade: B" << endl;
    } else if (score >= 70) {
        cout << "Grade: C" << endl;
    } else {
        cout << "Grade: F" << endl;
    }

    return 0;
}
```

### B. Lecture Example: Character Case Detection
Determine if an input character is Lowercase, Uppercase, or Non-alphabetical using ASCII values.

```cpp
#include <iostream>
using namespace std;

int main() {
    char ch;
    cout << "Enter character: ";
    cin >> ch;

    if (ch >= 'a' && ch <= 'z') {
        cout << "Lowercase Alphabet" << endl;
    } else if (ch >= 'A' && ch <= 'Z') {
        cout << "Uppercase Alphabet" << endl;
    } else {
        cout << "Not an English letter" << endl;
    }

    return 0;
}
```

> 🧠 **Brain Trigger**
> 
> Why does `ch >= 'a' && ch <= 'z'` work without explicitly typing ASCII numbers 97 and 122?
> 
> **Answer:** In C++, character literals like `'a'` and `'z'` are internally stored as their integral ASCII values. The comparison operator automatically compares their underlying numeric values. This is far more readable and portable than hardcoding `97` and `122`.

---

### C. The Ternary Operator (`?:`)
A compact alternative to simple `if-else` blocks. Unlike `if-else` (which is a statement), ternary is an **expression** that returns a value.

```cpp
// Syntax: (condition) ? expression_if_true : expression_if_false;
int a = 10, b = 20;
int maxVal = (a > b) ? a : b;
```

---

### D. The `switch` Statement
Dispatches execution to one of multiple `case` labels based on the evaluated value of an integral or enumeration expression.

```cpp
int day = 3;
switch (day) {
    case 1: cout << "Monday"; break;
    case 2: cout << "Tuesday"; break;
    case 3: cout << "Wednesday"; break;
    default: cout << "Other day";
}
```

> ⚠️ **Common Trap: Fallthrough in Switch**
> If `break` is omitted, execution cascades into all subsequent cases regardless of whether their condition matches until a `break` or the end of the `switch` is reached.

---

## 2. Iterative Loops: `while`, `for`, `do-while`

> 🔵 **Lecture Content**

### Comparison Table

| Loop Type | Classification | Condition Check Timing | Minimum Executions |
|---|---|---|---|
| `while` | Entry-controlled | Before loop body executes | $0$ times |
| `for` | Entry-controlled | Before loop body executes | $0$ times |
| `do-while` | Exit-controlled | After loop body executes | **$1$ time** |

---

### Example 1: Sum of Odd Numbers from $1$ to $N$

```cpp
#include <iostream>
using namespace std;

int main() {
    int n = 10;
    int oddSum = 0;

    for (int i = 1; i <= n; i++) {
        if (i % 2 != 0) {
            oddSum += i;
        }
    }

    cout << "Sum of odd numbers from 1 to " << n << " is: " << oddSum << endl;
    return 0;
}
```

### Example 2: Prime Check with Early Termination (`break`)

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter n: ";
    cin >> n;

    if (n <= 1) {
        cout << "Not Prime" << endl;
        return 0;
    }

    bool isPrime = true;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            isPrime = false;
            break; // Terminate loop immediately upon finding first divisor
        }
    }

    if (isPrime) cout << n << " is Prime." << endl;
    else cout << n << " is Composite." << endl;

    return 0;
}
```

---

## 3. Jump Statements: `break` vs `continue`

| Feature | `break` | `continue` |
|---|---|---|
| **Effect** | Terminate and exit the innermost loop entirely. | Skip the remaining statements in the *current* iteration. |
| **Next Step** | Control jumps to the statement immediately following the loop. | In `for`: Jumps to update statement (`i++`). In `while`: Jumps back to condition check. |

> ⚠️ **Critical Bug in `while` loops with `continue`**

```cpp
int i = 1;
while (i <= 5) {
    if (i == 3) {
        continue; // INFINITE LOOP! i is never incremented, stays 3 forever!
    }
    cout << i << " ";
    i++;
}
```

> In a `while` loop, you must ensure the loop counter is incremented **before** `continue` is called.

---

## ⚠️ Common Mistakes

1. **Semicolon After Loop Header:**
   ```cpp
   for (int i = 0; i < 5; i++); // SEMICOLON BUG!
   {
       cout << i; // Treated as a separate standalone block!
   }
   ```
2. **Floating-point Loop Iterators:** Using `float` for loop counters accumulates IEEE 754 precision errors, potentially resulting in an extra or missed iteration. Always use integer loop counters.

---

## 🔥 Interview Questions

### Q1: [Control Flow] How does the compiler implement a `switch` statement internally versus an `if-else` chain?
- **Short Answer:** `if-else` compiles to sequential comparison jumps ($O(N)$), while `switch` can be optimized by the compiler into a **Jump Table** ($O(1)$) when cases are dense integers.
- **Detailed Explanation:** If case values are clustered integers, the compiler constructs a table of code addresses. The switch expression directly indexes into the array of pointers in constant time. For sparse values, the compiler falls back to binary search trees or sequential branches.
- **Why Interviewers Ask:** Tests understanding of compiler optimizations and high-performance branching.

### Q2: [Loop Invariants] What is a Loop Invariant, and why is it used in algorithm proofs?
- **Short Answer:** A formal condition that is true before the loop starts, remains true after each iteration, and guarantees correct program state upon loop termination.
- **Detailed Explanation:** In algorithms like Binary Search or QuickSort partitioning, specifying a clear invariant (e.g., "the target is strictly within `[left, right]`") prevents subtle off-by-one errors and edge-case misbehavior.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
using namespace std;

int main() {
    int sum = 0;
    for (int i = 1; i <= 5; i++) {
        if (i % 2 == 0) continue;
        sum += i;
    }
    cout << sum << endl;
    return 0;
}
```
**Output:** `9`  
**Explanation:**  
- `i = 1`: odd $\to$ `sum = 0 + 1 = 1`  
- `i = 2`: even $\to$ `continue` skips  
- `i = 3`: odd $\to$ `sum = 1 + 3 = 4`  
- `i = 4`: even $\to$ `continue` skips  
- `i = 5`: odd $\to$ `sum = 4 + 5 = 9`  
- Final output: `9`.

---

## Key Takeaways

1. **Branching:** `if-else` evaluates sequentially; `switch` provides multi-way branching for integral values.
2. **Do-While Guarantee:** Guarantees execution at least once regardless of initial condition.
3. **Break vs Continue:** `break` exits the loop; `continue` skips to the next cycle.
4. **Primality Complexity:** Stopping at $\sqrt{N}$ reduces operation count from $10^9$ to $31622$, a critical factor in competitive programming.

---

## ⚡ 2-Minute Revision

- **Ternary:** `cond ? true_val : false_val`.
- **`switch` Limitations:** Operands must be integers, characters, or enums (strings and floats are prohibited in standard C++).
- **Infinite Loop Recipe:** Missing loop counter increment, condition that never becomes false (`while(true)`), or `continue` executed before counter update.
