# 💼 Topic 09 Interview Question Bank: Mathematics for DSA

> **Curated FAANG Question Bank:** Modular inverse, overflow hazards, prime factorization, and logarithmic powers.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why does the Sieve of Eratosthenes inner loop start at $i \times i$?
- **Answer:** Any composite multiple $k \times i$ where $k < i$ has already been marked composite by a smaller prime factor $k$. For example, when $i = 5$, multiples $2 \times 5 = 10$, $3 \times 5 = 15$, and $4 \times 5 = 20$ were already marked by 2 and 3. The earliest unmarked multiple is strictly $5 \times 5 = 25$.

---

### Q2: How does Binary Exponentiation compute $X^N$ in $O(\log N)$ time?
- **Answer:** Using the divide-and-conquer property:
  - If $N$ is even, $X^N = (X^2)^{N/2}$.
  - If $N$ is odd, $X^N = X \times (X^2)^{(N-1)/2}$.
  Halving the exponent $N$ in each step reduces multiplications from $N$ to $\log_2 N$. Always handle $N < 0$ by inverting $X = 1/X$ and casting $N$ to `long long` to prevent `-INT_MIN` overflow.

---

### Q3: Why is `(A - B) % M` handled with `((A % M) - (B % M) + M) % M`?
- **Answer:** In C++, the modulo operator `%` preserves the sign of the dividend. If $A \% M < B \% M$, the difference is negative. Adding $M$ before applying `% M` ensures the result strictly lands in the non-negative remainder range $[0, M - 1]$.
