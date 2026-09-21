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

## 🔥 Interview Questions

### Q1: Why does the Sieve inner loop start at $i \times i$ instead of $2 \times i$?
**Answer:** Any multiple $k \times i$ with $k < i$ has already been marked as composite by a prime factor smaller than $i$. For example, when $i = 5$, $2 \times 5 = 10$ was marked by $2$, $3 \times 5 = 15$ was marked by $3$, and $4 \times 5 = 20$ was marked by $2$. Thus, the earliest unmarked multiple of $i$ is strictly $i \times i$.
