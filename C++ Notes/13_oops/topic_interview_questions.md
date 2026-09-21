# 💼 Topic Interview Question Bank — Topic 13: OOPs

---

### Q1: What is the Diamond Problem in C++ and how is it resolved?
**Answer:**
The Diamond Problem occurs in multiple inheritance when a class `D` inherits from both `B` and `C`, and both `B` and `C` inherit from class `A`. As a result, `D` contains two duplicate copies of `A`'s member variables, leading to compiler ambiguity when accessing `A`'s fields.
It is resolved using **Virtual Inheritance**: `class B : virtual public A` and `class C : virtual public A`. The compiler ensures only a single shared instance of `A` is constructed.
