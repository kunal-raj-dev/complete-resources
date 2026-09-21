# 💼 Topic Interview Question Bank — Topic 09: Maths for DSA

---

### Q1: How do you compute modular division $(a / b) \pmod M$?
**Answer:**
Division is not defined directly under modulo arithmetic. When $M$ is a prime number, by Fermat's Little Theorem:
$$b^{M-1} \equiv 1 \pmod M \implies b \cdot b^{M-2} \equiv 1 \pmod M$$
Thus, the modular multiplicative inverse of $b$ is $b^{-1} \equiv b^{M-2} \pmod M$.
Therefore:
$$(a / b) \pmod M = (a \cdot b^{M-2}) \pmod M$$
computed via modular binary exponentiation in $O(\log M)$ time.
