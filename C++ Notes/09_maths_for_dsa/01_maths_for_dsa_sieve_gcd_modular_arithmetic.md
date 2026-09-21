# Lecture 34: Maths for DSA: Euclid's GCD, Sieve of Eratosthenes & Modular Arithmetic

> **One-Line Purpose:** Master foundational discrete mathematics for competitive programming and technical interviews: prime sieving, Euclidean logarithmic GCD, and modular arithmetic rules.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #34  
> **Video ID:** `Y4KdgqV1IqA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Y4KdgqV1IqA)  
> **Duration:** 55:48  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- Why trial division takes $O(\sqrt{N})$ time and how prime factors appear in symmetrical pairs.
- The **Sieve of Eratosthenes** and its harmonic series complexity derivation: $O(N \log \log N)$.
- **Euclid's Algorithm** for Greatest Common Divisor (GCD) and why $\gcd(a, b) = \gcd(b, a \pmod b)$ runs in $O(\log(\min(a, b)))$.
- Mathematical laws of **Modular Arithmetic** under addition, subtraction, and multiplication.
- **Modular Exponentiation (Binary Exponentiation)** running in $O(\log B)$ time.

---

## 🔵 Lecture Content

### 1. Prime Numbers & The Sieve of Eratosthenes

A number $N > 1$ is prime if its only positive divisors are $1$ and $N$.
- **Sieve Algorithm:**
  1. Create boolean array `isPrime[0...N]` initialized to `true`.
  2. Mark `0` and `1` as `false`.
  3. For each $i$ from $2$ up to $\sqrt{N}$:
     - If `isPrime[i]` is `true`, mark all multiples $i \times i, i \times i + i, \dots$ as `false`.

```cpp
#include <vector>
#include <iostream>
using namespace std;

vector<bool> sieveOfEratosthenes(int n) {
    vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            // Optimization: start crossing out from i * i
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    return isPrime;
}
```
- **Time Complexity:** $O(N \log(\log N))$ — Harmonic series over primes: $\sum_{p \le N} \frac{N}{p} \approx N \ln(\ln N)$.
- **Space Complexity:** $O(N)$ boolean array.

---

### 2. Greatest Common Divisor (GCD): Euclidean Algorithm

$$\gcd(a, b) = \begin{cases} a & \text{if } b = 0 \\ \gcd(b, a \pmod b) & \text{otherwise} \end{cases}$$

```cpp
int gcd(int a, int b) {
    while (b != 0) {
        int rem = a % b;
        a = b;
        b = rem;
    }
    return a;
}

int lcm(int a, int b) {
    return (a / gcd(a, b)) * b; // Division first prevents intermediate overflow
}
```
- **Time Complexity:** $O(\log(\min(a, b)))$ steps (Lamé's theorem proves consecutive Fibonacci numbers represent the worst case).

---

### 3. Modular Arithmetic & Modular Exponentiation

Properties:
1. $(a + b) \pmod M = ((a \pmod M) + (b \pmod M)) \pmod M$
2. $(a - b) \pmod M = ((a \pmod M) - (b \pmod M) + M) \pmod M$ (Prevents negative results)
3. $(a \times b) \pmod M = ((a \pmod M) \times (b \pmod M)) \pmod M$

#### Fast Modular Exponentiation ($A^B \pmod M$ in $O(\log B)$)
```cpp
long long powerMod(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;

    while (exp > 0) {
        if (exp & 1) { // If exp is odd
            res = (res * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}
```

---

## 🧠 Core Intuition — Why This Works
**Sieve:** If a number is prime, none of its multiples can be prime. Instead of checking if each number is divisible by primes (which is slow), we "broadcast" the primality outwards: as soon as we confirm a prime, we jump forward by its value and cross out all its multiples.
**GCD (Euclid):** If a number $D$ divides $A$ and $B$, it must also divide $A - B$. By repeatedly subtracting the smaller from the larger, we preserve the common divisors. The modulo operator `%` is just a fast way of doing repeated subtraction.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "Count primes up to N", "Find greatest common divisor", "Answer modulo $10^9+7$".
- **Keywords:** Sieve of Eratosthenes, Euclidean Algorithm, Modular Arithmetic.

## 📐 Algorithm Walk-Through
**Sieve:**
1. Initialize `isPrime` array of size `N+1` to `true`.
2. `isPrime[0] = isPrime[1] = false`.
3. Loop `i` from $2$ to $\sqrt{N}$:
   - If `isPrime[i]` is true:
     - Loop `j` from $i \times i$ to $N$ with step $i$.
     - Mark `isPrime[j] = false`.

**GCD:**
1. Loop while `b != 0`.
2. Save `rem = a % b`.
3. Shift: `a = b`, `b = rem`.
4. Return `a`.

## 🔍 Dry Run Trace (GCD)
`a = 48, b = 18`
1. `rem = 48 % 18 = 12`. `a = 18, b = 12`.
2. `rem = 18 % 12 = 6`. `a = 12, b = 6`.
3. `rem = 12 % 6 = 0`. `a = 6, b = 0`.
4. `b == 0`, loop ends. Return `6`.

## ⚠️ Common Interview Mistakes
- **Sieve:** Starting the inner loop at $2 \times i$ instead of $i \times i$, wasting time checking multiples that were already crossed out by smaller primes.
- **LCM:** Doing `(a * b) / gcd` instead of `(a / gcd) * b`. If $a$ and $b$ are near $10^9$, $a \times b$ overflows a 32-bit integer before division.
- **Modulo Subtraction:** Doing `(a - b) % M`. In C++, modulo of a negative number is negative. Always do `((a - b) % M + M) % M`.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why does the Sieve inner loop start at $i \times i$ instead of $2 \times i$?
**Answer:** Any multiple $k \times i$ with $k < i$ has already been marked as composite by a prime factor smaller than $i$. For example, when $i = 5$, $2 \times 5 = 10$ was marked by $2$, $3 \times 5 = 15$ was marked by $3$, and $4 \times 5 = 20$ was marked by $2$. Thus, the earliest unmarked multiple of $i$ is strictly $i \times i$.

### Q2: Why does the Sieve outer loop stop at $\sqrt{N}$?
**Answer:** If $N$ is not prime, it can be factored as $N = a \times b$. If both $a$ and $b$ were strictly greater than $\sqrt{N}$, then $a \times b > N$, which is a contradiction. Therefore, every composite number up to $N$ must have at least one prime factor $\le \sqrt{N}$.

### Q3: What is the Time Complexity of Sieve and how is it derived?
**Answer:** The inner loop runs $N/2 + N/3 + N/5 + N/7 \dots$ times. This is $N \times (\frac{1}{2} + \frac{1}{3} + \frac{1}{5} \dots)$. The sum of the reciprocals of primes up to $N$ diverges as $\log(\log N)$. Thus, the overall time is $O(N \log \log N)$.

### Q4: Why is modular arithmetic required in Competitive Programming?
**Answer:** To prevent integer overflow when dealing with massive combinations or permutations (e.g., $1000!$). Modulo $10^9+7$ is chosen because it fits within a 32-bit signed integer, and its square $(10^{18})$ fits perfectly in a 64-bit integer (`long long`). Also, it's prime, enabling modular inverses.

## 🏆 Related Problems (Leetcode)
- **LeetCode 204:** Count Primes (Direct Sieve implementation)
- **LeetCode 1979:** Find Greatest Common Divisor of Array
- **LeetCode 50:** Pow(x, n) (Binary exponentiation)

## 🔗 Cross-Topic Connections
- **Bit Manipulation:** Fast modular exponentiation heavily utilizes bitwise AND (`& 1`) and Right Shift (`>> 1`).
- **Dynamic Programming:** Combinatorics DP problems often require massive modular calculations.

## ⚡ 2-Minute Revision Flash Card
- **Sieve:** Outer loop up to $\sqrt{N}$. Inner loop starts at $i \times i$, steps by $i$. Time: $O(N \log \log N)$.
- **GCD:** `while(b != 0) { rem = a%b; a=b; b=rem; }` Time: $O(\log(\min(a,b)))$.
- **LCM:** `(a / gcd(a,b)) * b` (divide first to avoid overflow).
- **Modulo Trap:** Subtraction needs `+ M`: `((a - b) % M + M) % M`.
