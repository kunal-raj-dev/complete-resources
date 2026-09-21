# ⚡ Topic 09 Revision: Mathematics & Number Theory for DSA

> **High-Density Review:** Prime generation, Euclidean GCD, Modular Arithmetic, and Binary Exponentiation.

---

## 1. Prime Numbers & Sieve of Eratosthenes
- **Primality Check:** Check divisors up to $\lfloor\sqrt{N}\rfloor$ in $O(\sqrt{N})$.
- **Sieve of Eratosthenes:** Generate all primes up to $N$ in $O(N \log \log N)$ time.
  - Inner multiple loop starts at $i \times i$ (smaller multiples already crossed out by smaller primes).
  - Use `1LL * i * i <= N` to prevent signed 32-bit integer overflow!

---

## 2. Essential Formulas
```
Euclidean GCD:            gcd(a, b) = (b == 0 ? a : gcd(b, a % b))
LCM Formula:              lcm(a, b) = (a / gcd(a, b)) * b   // Divide first to prevent overflow!
Binary Exponentiation:    a^b = (a^(b/2))^2 * (b % 2 ? a : 1) in O(log b)
Modular Arithmetic:       (A + B) % M = ((A % M) + (B % M)) % M
                          (A * B) % M = ((A % M) * (B % M)) % M
                          (A - B) % M = ((A % M) - (B % M) + M) % M
```
