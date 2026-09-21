# Lecture 56: Object-Oriented Programming (OOPs) in C++ Complete Masterclass

> **One-Line Purpose:** Master the 4 pillars of Object-Oriented Programming (Encapsulation, Abstraction, Inheritance, Polymorphism), virtual functions, vtables, and deep vs shallow copying for placement interviews.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #56  
> **Video ID:** `mlIUKyZIUUU`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=mlIUKyZIUUU)  
> **Duration:** 02:04:23  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- **Classes vs Objects:** Blueprint vs instantiated memory.
- **Access Modifiers:** `public`, `private`, `protected`.
- **Constructors & Destructors:** Parameterized, Copy Constructor (Deep vs Shallow Copy), Destructor cleanup.
- **Encapsulation & Abstraction:** Data hiding and abstract interface design via pure virtual functions (`= 0`).
- **Inheritance:** Single, Multilevel, Multiple, Hierarchical, Hybrid, and the **Diamond Problem** solved via `virtual` base classes.
- **Polymorphism:**
  - Compile-Time: Function Overloading and Operator Overloading.
  - Run-Time: `virtual` member functions, Dynamic Dispatch, `vptr` pointer and `vtable`.
- **Advanced C++ OOP Keywords:** `static`, `friend`, `override`, `final`.

---

## 🔵 Lecture Content

### 1. The 4 Core Pillars of OOP

```text
┌──────────────────────────────────────────────────────────────┐
│                    THE 4 PILLARS OF OOPS                     │
├─────────────────┬─────────────────┬──────────────────────────┤
│ Encapsulation   │ Abstraction     │ Inheritance & Poly       │
├─────────────────┼─────────────────┼──────────────────────────┤
│ Bundling data   │ Hiding internal │ Code reuse via hierarchy │
│ and functions;  │ implementation; │ and dynamic runtime      │
│ private fields. │ public APIs.    │ method dispatch.         │
└─────────────────┴─────────────────┴──────────────────────────┘
```

---

### 2. Deep Copy vs Shallow Copy

A default copy constructor performs a **shallow copy** (bitwise member-by-member copy). If a class manages dynamic heap memory via a raw pointer, shallow copying duplicates the pointer address, not the allocated memory:
1. Double Free Error: When both objects destruct, they call `delete` on the same address.
2. Unintended Side Effects: Modifying heap memory via one object mutates the other.

#### Implementing a Custom Deep Copy Constructor:
```cpp
#include <iostream>
#include <cstring>
using namespace std;

class Student {
public:
    string name;
    double* cgpa;

    Student(string name, double cgpaVal) {
        this->name = name;
        this->cgpa = new double(cgpaVal);
    }

    // Deep Copy Constructor
    Student(const Student& other) {
        this->name = other.name;
        this->cgpa = new double(*other.cgpa); // Allocate independent heap memory!
    }

    // Destructor to prevent memory leak
    ~Student() {
        delete cgpa;
    }
};
```

---

### 3. Run-Time Polymorphism: Virtual Functions & `vtable`

When a base class pointer points to a derived class object, calling a non-virtual function invokes the **base class method** (Static Binding).
Adding the `virtual` keyword enables **Dynamic Binding**:
- The compiler inserts a hidden pointer (`vptr`) into every object of a class with virtual functions.
- `vptr` points to a class-wide `vtable` (array of function pointers).
- At runtime, the function call is resolved by looking up the derived class's override in the `vtable`.

```cpp
class Shape {
public:
    virtual void draw() {
        cout << "Drawing generic shape" << endl;
    }
    virtual ~Shape() {} // Essential: Virtual destructor ensures derived cleanup
};

class Circle : public Shape {
public:
    void draw() override {
        cout << "Drawing Circle" << endl;
    }
};

void render(Shape* s) {
    s->draw(); // Calls Circle::draw() at runtime if s is a Circle!
}
```

---

### 4. Pure Virtual Functions & Abstract Classes
A class with at least one pure virtual function (`virtual void f() = 0;`) cannot be directly instantiated and acts as an interface.

---

## 🔥 Interview Questions

### Q1: Why must a base class destructor always be declared `virtual`?
**Answer:**
If a derived class object is deleted through a base class pointer (`Base* b = new Derived(); delete b;`), and the base destructor is **not** virtual, the program exhibits undefined behavior. The compiler statically binds the destructor call and executes only `~Base()`, skipping `~Derived()`. Any heap memory or system resources acquired by the derived class will leak.
