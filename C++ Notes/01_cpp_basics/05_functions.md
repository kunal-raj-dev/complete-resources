# Lecture 05: Functions, Memory Call Stack & Pass-by-Value

> **One-Line Purpose:** Understand modular program design, the internal mechanics of the Call Stack and Stack Frames, Pass-by-Value semantics, and reusable mathematical implementations ($nCr$, Factorials, Sum of Digits).

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #05  
> **Video ID:** `P08Z_NC8GuY`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=P08Z_NC8GuY)  
> **Duration:** 49:13  
> **Transcript:** `.transcripts/01_cpp_basics/005_Lecture_5__Functions___DSA_Series_by_Shradha_Khapra_Ma_am___C__.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- Why functions are essential for code modularity, readability, and avoiding code duplication (DRY principle).
- The distinction between **Formal Parameters** (in function definition) and **Actual Arguments** (passed by caller).
- The internal architecture of the **Call Stack** and **Stack Frames (Activation Records)** during execution.
- How **Pass-by-Value** operates in memory, why modifications to copies do not alter original caller variables, and the memory cost of copying.
- Variable Scopes: Local, Block, and Global scopes and their lifetimes.
- Key implementations: Factorial ($N!$), Sum of Digits, and Binomial Coefficient ($nCr$).

---

## 🔵 Lecture Context

Functions form the bedrock of clean software architecture and recursion. Understanding the CPU call stack—how activation records are pushed, how local variables are allocated in stack memory, and how stack frames unwind upon `return`—is the exact prerequisite needed to master Recursion (Lectures 42-55) and Graph DFS (Lectures 113-136).

---

## 1. Anatomy of a Function & Calling Mechanism

> 🔵 **Lecture Content**

A function is a reusable block of code that performs a specific task.

```cpp
return_type function_name(parameter_type param1, parameter_type param2) {
    // Function body
    return result; // Must match return_type
}
```

```cpp
#include <iostream>
using namespace std;

// Function Declaration & Definition
int add(int a, int b) { // 'a' and 'b' are Formal Parameters
    return a + b;
}

int main() {
    int x = 10, y = 20;
    int sum = add(x, y); // 'x' and 'y' are Actual Arguments
    cout << "Sum: " << sum << endl;
    return 0;
}
```

---

## 2. The Memory Call Stack & Stack Frames

When a C++ program runs, the Operating System allocates a dedicated memory region called the **Call Stack**.

```
High Memory
  ┌─────────────────────────────────┐
  │         Stack Frame: add()      │  ← Pushed when add(x, y) is invoked
  │   - Parameters: a = 10, b = 20  │
  │   - Return Address: inside main │
  ├─────────────────────────────────┤
  │         Stack Frame: main()     │  ← Pushed when program starts
  │   - Local: x = 10, y = 20       │
  │   - Local: sum = ?              │
  └─────────────────────────────────┘
Low Memory
```

### Step-by-Step Lifecycle:
1. `main()` starts: A stack frame for `main` is allocated containing its local variables `x`, `y`, and `sum`.
2. `add(x, y)` called: CPU suspends `main`, pushes a new stack frame for `add()`, and copies the values of `x` and `y` into `a` and `b`.
3. `add()` completes: Its return value is sent back to `main`, its stack frame is **popped** (freed instantly from memory), and execution resumes in `main()`.

> 🧠 **Brain Trigger**
> 
> What happens if functions keep calling functions indefinitely without returning?
> 
> **Answer:** Each call allocates a new stack frame. Eventually, the allocated stack memory limit is exceeded, causing a **Stack Overflow** crash (`SIGSEGV` / segmentation fault).

---

## 3. Pass-by-Value Mechanics

> 🔵 **Lecture Content**

In C++, default parameter passing is **Pass-by-Value**. The function receives a distinct, isolated **copy** of the argument's data. Any changes made inside the function affect only the copy in its local stack frame.

```cpp
#include <iostream>
using namespace std;

void changeValue(int x) {
    x = x + 100; // Only modifies local parameter 'x'
}

int main() {
    int a = 10;
    changeValue(a);
    cout << "Value of a: " << a << endl; // Still prints 10!
    return 0;
}
```

> 🟡 **Additional Essential Context: Pass-by-Reference Preview**
> 
> To allow a function to modify the caller's variable directly without creating a memory copy, we pass the parameter by reference using the ampersand (`&`):

```cpp
void reallyChange(int &x) { // 'x' is now an alias for the caller's variable
    x = x + 100;
}
```


---

## 4. Lecture Problem Implementations

### Problem 1: Factorial of $N$ ($N!$)
$$N! = 1 \times 2 \times 3 \times \dots \times N \quad (0! = 1)$$

```cpp
long long factorial(int n) {
    if (n < 0) return -1; // Error sentinel
    long long fact = 1;
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    return fact;
}
```

---

### Problem 2: Sum of Digits of an Integer
Given an integer $N$, compute the sum of its decimal digits.

```cpp
int sumOfDigits(int n) {
    int sum = 0;
    n = abs(n); // Handle negative inputs gracefully
    while (n > 0) {
        int lastDigit = n % 10;
        sum += lastDigit;
        n /= 10;
    }
    return sum;
}
```

---

### Problem 3: Binomial Coefficient ($nCr$)
Calculate combinations:
$$nCr = \frac{n!}{r! \times (n - r)!}$$

```cpp
#include <iostream>
using namespace std;

long long fact(int n) {
    long long ans = 1;
    for (int i = 1; i <= n; i++) ans *= i;
    return ans;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    long long fact_n = fact(n);
    long long fact_r = fact(r);
    long long fact_nmr = fact(n - r);

    return fact_n / (fact_r * fact_nmr);
}

int main() {
    int n = 8, r = 2;
    cout << "8C2 = " << nCr(n, r) << endl; // Prints 28
    return 0;
}
```

---

## ⚠️ Common Mistakes

1. **Integer Overflow in Factorials:** $N!$ grows exponentially. A 32-bit `int` overflows at $13!$. A 64-bit `long long` overflows at $21!$. For $nCr$ in production and interviews, calculating $\frac{n!}{r!(n-r)!}$ directly via factorials causes overflow prematurely.
   > 🔥 **Interview Extension: Optimized $nCr$ Without Full Factorials**
   > $$nCr = \prod_{i=1}^r \frac{n - r + i}{i}$$
   > Calculating iteratively while dividing at each step keeps intermediate numbers small:

```cpp
long long nCrOptimized(int n, int r) {
    if (r < 0 || r > n) return 0;
    if (r > n - r) r = n - r; // Symmetry: nCr = nC(n-r)
    long long res = 1;
    for (int i = 1; i <= r; i++) {
        res = res * (n - r + i) / i;
    }
    return res;
}
```


---

## 🔥 Interview Questions

### Q1: [Memory Architecture] Where do local variables and function parameters reside in memory?
- **Short Answer:** Inside the function's individual **Stack Frame** on the runtime call stack.
- **Detailed Explanation:** When a function is called, space is pushed onto the stack for its arguments, local variables, and return address. Once the function finishes, the stack pointer (`ESP`/`RSP`) is moved back, and that memory is immediately reclaimed.
- **Follow-up:** Can a function safely return a pointer to its local variable?
  - **Answer:** **NO!** Returning a pointer or reference to a local stack variable causes a **Dangling Pointer** bug. When the function returns, its stack frame is invalidated, and dereferencing the address invokes Undefined Behavior.

### Q2: [C++ Feature] What is Function Overloading and how is it resolved?
- **Short Answer:** Defining multiple functions with the exact same name but differing parameter signatures; resolved at **compile-time**.
- **Detailed Explanation:** The compiler uses **Name Mangling** to embed the parameter types into the generated symbol name (e.g., `_Z3addii` for `add(int, int)` vs `_Z3adddd` for `add(double, double)`). Note: Functions differing *only* by return type cannot be overloaded.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
using namespace std;

void modify(int a) {
    a *= 2;
}

int main() {
    int x = 5;
    modify(x);
    cout << x << endl;
    return 0;
}
```
**Output:** `5`  
**Explanation:** `modify()` receives a copy of `x`. The modification `a *= 2` updates only the local parameter `a` inside `modify()`'s stack frame. The variable `x` in `main()` is unaffected.

---

## Key Takeaways

1. **Stack Memory:** Every function call creates an activation record (stack frame) containing arguments and local variables.
2. **Pass-by-Value:** Default in C++; creates an isolated copy.
3. **DRY Principle:** Isolate repeated calculations (like factorials) into dedicated functions.
4. **Defensive Arithmetic:** Watch for integer overflow when computing factorials and combinations.

---

## ⚡ 2-Minute Revision

- **Call Stack:** LIFO (Last-In First-Out) data structure managed by CPU hardware.
- **Activation Record:** Contains local variables, parameters, and instruction pointer return address.
- **$nCr$ Symmetry:** $nCr = nC(n-r)$ (reduces loop iterations).
- **Dangling Reference Trap:** Never return `&local_var` from a function.
