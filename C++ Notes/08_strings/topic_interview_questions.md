# 💼 Topic Interview Question Bank — Topic 08: Strings

---

### Q1: What is Small String Optimization (SSO) in C++?
**Answer:**
Modern C++ `std::string` implementations avoid heap allocation for small strings (typically $\le 15$ or $22$ bytes) by storing the character array directly inside the string object's internal buffer on the stack. Only when the string exceeds this threshold is memory dynamically allocated on the heap.
