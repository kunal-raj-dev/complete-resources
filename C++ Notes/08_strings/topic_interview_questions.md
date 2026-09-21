# 💼 Topic 08 Interview Question Bank: Strings

> **Curated FAANG Question Bank:** Small String Optimization, string immutability in other languages vs C++, sliding window bounds, and buffer overflows.

---

## 📌 Conceptual & Architectural Questions

### Q1: What is Small String Optimization (SSO) in C++?
- **Answer:** Standard library implementations of `std::string` avoid expensive heap allocation for short strings (typically $\le 15$ or $22$ characters) by reusing the pointer/size union members as an internal stack-allocated buffer. Memory is only allocated on the heap when string length exceeds the internal capacity.

---

### Q2: How does `std::string_view` (C++17) improve performance over `const std::string&`?
- **Answer:** `std::string_view` is a non-owning reference consisting of a raw pointer to existing character data and a length integer (16 bytes on 64-bit systems). It allows substring and slicing operations in $O(1)$ time with **zero heap allocations**, whereas passing or substringing `std::string` creates heap copies.

---

### Q3: How do you reverse words in a string with $O(1)$ auxiliary space?
- **Answer:**
  1. Remove extra leading, trailing, and redundant middle spaces in-place using two pointers.
  2. Reverse the entire trimmed string.
  3. Iterate through the string and reverse each individual word between spaces.
