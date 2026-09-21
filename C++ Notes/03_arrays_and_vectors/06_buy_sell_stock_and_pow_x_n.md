# Lecture 13: Buy & Sell Stock & Binary Exponentiation (`Pow(x, n)`)

> **One-Line Purpose:** Master the single-pass minimum tracking pattern for Best Time to Buy & Sell Stock ($O(N)$), and divide-and-conquer Binary Exponentiation for `Pow(x, n)` ($O(\log N)$) with `INT_MIN` overflow handling.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #13  
> **Video ID:** `WBzZCm46mFo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=WBzZCm46mFo)  
> **Duration:** 29:10  
> **Transcript:** `.transcripts/03_arrays_and_vectors/013_Buy_and_Sell_Stock_Problem_and_Pow_X_N__Power_exponential_Problem_-_Leetcode___.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The single-pass dynamic minimum tracking strategy for LeetCode 121 (Best Time to Buy and Sell Stock).
- Why naive multiplication for $x^n$ fails for large $n$ ($O(N)$ vs $1.0$s time limit).
- The mathematical halving principle of **Binary Exponentiation** ($O(\log N)$).
- How to handle negative exponents and prevent 32-bit signed integer overflow when $n = -2^{31}$ (`INT_MIN`).
- Bitwise iteration for Binary Exponentiation using bit shifts.

---

## 🔵 Lecture Context

Both problems taught in this lecture represent foundational algorithmic paradigms:
1. **Best Time to Buy & Sell Stock** represents Greedy prefix state tracking.
2. **Pow(x, n)** introduces Binary Halving (Divide and Conquer), which directly carries over to modular exponentiation in cryptography, Matrix Exponentiation, and Binary Search.

---

## 1. Problem 1: Best Time to Buy and Sell Stock (LeetCode 121)

> 🔵 **Lecture Content**

**Problem:** You are given an array `prices` where `prices[i]` is the stock price on day $i$. You want to maximize profit by choosing a single day to buy and a distinct future day to sell. Return the maximum profit achievable. If no profit can be achieved, return `0`.

### Core Intuition:
To maximize profit when selling on day $i$, you must have bought the stock at the **lowest possible price prior to day $i$**.
- Maintain a running minimum: `bestBuy = min(bestBuy, prices[i])`.
- At every day $i$, the profit from selling today is: `profit = prices[i] - bestBuy`.
- Update global max: `maxProfit = max(maxProfit, profit)`.

```cpp
#include <vector>
#include <climits>
#include <iostream>
using namespace std;

int maxProfit(const vector<int>& prices) {
    int bestBuy = INT_MAX;
    int maxProfit = 0;

    for (int price : prices) {
        if (price < bestBuy) {
            bestBuy = price; // Found a cheaper day to buy
        } else {
            maxProfit = max(maxProfit, price - bestBuy); // Potential profit selling today
        }
    }
    return maxProfit;
}
```
- **Time Complexity:** $O(N)$ single pass.
- **Space Complexity:** $O(1)$ auxiliary space.

---

## 2. Problem 2: `Pow(x, n)` via Binary Exponentiation (LeetCode 50)

> 🔵 **Lecture Content**

**Problem:** Implement `pow(x, n)`, which calculates $x$ raised to the power $n$ ($x^n$).

### Why Naive Multiplication Fails:
Multiplying $x$ sequentially $n$ times takes $O(n)$ time. When $n = 2^{31}-1 \approx 2.14 \times 10^9$, this performs $2 \times 10^9$ operations, severely violating the $10^8$ operations/sec limit and causing Time Limit Exceeded (TLE).

---

### The Binary Exponentiation Principle ($O(\log N)$)
Observe what happens when we square the base:
- If $n$ is **even**:
  $$x^n = (x^2)^{n/2}$$
  Example: $2^{10} = (2^2)^5 = 4^5$
- If $n$ is **odd**:
  $$x^n = x \times (x^2)^{(n-1)/2}$$
  Example: $4^5 = 4 \times (4^2)^2 = 4 \times 16^2$

At each step, the exponent is divided by 2. The total operations scale with the number of bits in $n$: $\log_2(n) \le 32$ steps!

---

### The Critical `INT_MIN` Trap
In C++, 32-bit signed integer range is $[-2,147,483,648, +2,147,483,647]$.  
If $n = -2,147,483,648$ (`INT_MIN`), attempting $-n$ causes **integer overflow** because $+2,147,483,648$ exceeds `INT_MAX`.  
**Solution:** Store $n$ in a 64-bit `long long binForm` before taking its absolute value.

---

### C++ Implementation
```cpp
#include <iostream>
using namespace std;

double myPow(double x, int n) {
    long long binForm = n; // Safe from INT_MIN overflow

    if (binForm < 0) {
        x = 1.0 / x;
        binForm = -binForm;
    }

    double ans = 1.0;
    while (binForm > 0) {
        // If current bit is 1, multiply into accumulator
        if (binForm % 2 == 1) {
            ans *= x;
        }
        x *= x;          // Square the base
        binForm /= 2;    // Halve the exponent
    }

    return ans;
}

int main() {
    cout << "2^10 = " << myPow(2.0, 10) << endl;     // 1024
    cout << "2^-3 = " << myPow(2.0, -3) << endl;     // 0.125
    cout << "3^5  = " << myPow(3.0, 5) << endl;      // 243
    return 0;
}
```

- **Time Complexity:** $O(\log_2 N)$
- **Space Complexity:** $O(1)$

---

## 🔍 Binary Exponentiation Trace: `myPow(3, 5)`

Initial: `x = 3`, `binForm = 5` ($101_2$), `ans = 1.0`

| Step | `binForm` (binary) | `binForm % 2` | Action on `ans` | Action on `x` | `binForm / 2` |
|---|---|---|---|---|---|
| 1 | 5 (`101`) | 1 (Odd) | `ans = 1.0 * 3 = 3.0` | `x = 3 * 3 = 9` | 2 |
| 2 | 2 (`010`) | 0 (Even) | No change (`ans = 3.0`) | `x = 9 * 9 = 81` | 1 |
| 3 | 1 (`001`) | 1 (Odd) | `ans = 3.0 * 81 = 243.0`| `x = 81 * 81` | 0 (Terminates) |

**Result:** `243.0`. Correct! Total iterations = 3.

---

## Key Takeaways

1. **Stock Minimum Tracking:** Track the lowest price seen so far to compute optimal sell profit on day $i$ in $O(N)$.
2. **Binary Halving:** Square the base, halve the power $\implies O(\log N)$ time.
3. **Edge Cases:** Handle $x^0 = 1$, negative exponents via reciprocal base ($1/x$), and use `long long` to prevent `INT_MIN` negation overflow.

---

## ⚡ 2-Minute Revision

- **Stock:** `bestBuy = min(bestBuy, price); maxProfit = max(maxProfit, price - bestBuy);`.
- **Pow:**
  ```cpp
  while (binForm > 0) {
      if (binForm & 1) ans *= x;
      x *= x;
      binForm >>= 1;
  }
  ```
- **Complexity:** Stock is $O(N)$, Pow is $O(\log N)$.
