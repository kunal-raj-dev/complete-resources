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

## 🧠 Core Intuition — Why This Works
Procedural programming focuses on functions calling other functions. Object-Oriented Programming focuses on **objects** that represent real-world entities containing both state (data) and behavior (functions).
*Analogy:* Think of a `Car` class as a blueprint. It defines that every car has an engine size (state) and can accelerate (behavior). An object `myMustang` is an actual car built from that blueprint.

## 🎯 Pattern Recognition — When to Use This
- **Trigger cues:** "design a parking lot", "design a library system", "base class", "override".
- **Pattern:** Use OOP to group related data and functionality, hide internal state to prevent misuse (Encapsulation), and share common code among related entities (Inheritance/Polymorphism).

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

## ⚠️ Common Interview Mistakes
1. **Forgetting Virtual Destructor:** Deleting a derived object via a base pointer when the base destructor is not `virtual` leaks memory because the derived destructor is never called.
2. **Object Slicing:** Passing derived objects by value to a function expecting a base object slices off the derived members. Always pass by pointer or reference.
3. **Misusing `new` and `delete`:** Shallow copying objects with pointers and getting a double-free crash.

## 🔥 Interview Q&A

### Q1: Why must a base class destructor always be declared `virtual`?
**Answer:**
If a derived class object is deleted through a base class pointer (`Base* b = new Derived(); delete b;`), and the base destructor is **not** virtual, the program exhibits undefined behavior. The compiler statically binds the destructor call and executes only `~Base()`, skipping `~Derived()`. Any heap memory or system resources acquired by the derived class will leak.

### Q2: What is Object Slicing in C++?
**Answer:**
Object slicing occurs when a derived class object is assigned to a base class object by value: `Base b = derivedObj;`. The derived-specific member variables are sliced away, leaving only the base sub-object. Polymorphism also fails because the VPtr is reset to the base class.

### Q3: What is the Diamond Problem and how does C++ solve it?
**Answer:**
The Diamond Problem occurs when class $D$ inherits from two classes $B$ and $C$, which both inherit from class $A$. $D$ then contains two separate, ambiguous copies of $A$'s members. C++ solves this using **Virtual Inheritance**: `class B : virtual public A` and `class C : virtual public A`. The compiler ensures only a single shared instance of $A$ exists in $D$.

### Q4: Can a constructor be virtual?
**Answer:**
No. A constructor's job is to establish the exact type of the object. When a constructor is called, the virtual table pointer (`vptr`) is just being set up. Virtual functions require a fully constructed `vptr` to resolve dynamically.

### Q5: What is the difference between overriding and overloading?
**Answer:**
Overloading (Compile-Time) means having multiple functions with the same name but different parameters in the same scope. Overriding (Run-Time) occurs when a derived class provides a specific implementation for a virtual function already defined in its base class with the exact same signature.

## 🏆 Related Problems
- Systems Design Interviews: "Design a Parking Lot", "Design an Elevator System". These directly test OOP principles, interfaces, and inheritance.
- Leetcode LRU Cache (combining Hash Map with Doubly Linked List nodes as objects).

## 🔗 Cross-Topic Connections
- **Pointers & Memory:** Essential for understanding deep copy and virtual pointers.
- **System Design:** Foundational mapping of real-world entities into software entities.

## ⚡ 2-Minute Revision Flash Card
- **Encapsulation:** Hide data, expose API (`private` vars, `public` getters/setters).
- **Abstraction:** Hide complexity (Pure virtual functions `virtual void f() = 0`).
- **Inheritance:** Reuse code (`class Derived : public Base`).
- **Polymorphism:** Same name, different behavior (Overloading vs Virtual Overriding).
- **VPtr & VTable:** How dynamic dispatch works under the hood.
- **Rule of Three:** If you write a custom destructor, copy constructor, or copy assignment operator, you probably need to write all three.
