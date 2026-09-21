# 💼 Topic 13 Interview Question Bank: OOPs in C++

> **Curated FAANG Question Bank:** Virtual destructors, diamond inheritance, slicing, and memory management.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why must a Base class destructor always be declared `virtual`?
- **Answer:** If a derived class object is deleted through a base class pointer (`Base* ptr = new Derived(); delete ptr;`), and the base class destructor is NOT virtual, the compiler performs static binding and calls ONLY the base class destructor! The derived class destructor is never invoked, leaking any resources or heap memory allocated in the derived class. Declaring `virtual ~Base()` ensures dynamic dispatch correctly invokes `~Derived()` first, followed by `~Base()`.

### Q2: What is Object Slicing in C++?
- **Answer:** Object slicing occurs when a derived class object is assigned to a base class object by value (rather than pointer or reference): `Base b = derivedObj;`. The derived-specific member variables and virtual pointer are sliced away, leaving only the base sub-object. This disables polymorphism, as `b` is literally just a `Base` object in memory.

### Q3: What is the Diamond Problem and how does C++ solve it?
- **Answer:** The Diamond Problem occurs when class $D$ inherits from two classes $B$ and $C$, which both inherit from class $A$. $D$ contains two separate, ambiguous copies of $A$'s member variables. C++ solves this using **Virtual Inheritance**: `class B : virtual public A` and `class C : virtual public A`. The compiler ensures only a single shared instance of $A$ exists in $D$.

### Q4: Explain the difference between `override` and `final` specifiers.
- **Answer:** `override` is a safety check: it tells the compiler that the function is intended to override a virtual function in a base class. If the base class function signature changes, compilation fails instead of silently creating a new overloaded function. `final` prevents a virtual function from being overridden further down the hierarchy, or prevents a class from being inherited at all.

### Q5: What is the "Rule of Three" in C++?
- **Answer:** The Rule of Three states that if a class requires a user-defined destructor, copy constructor, or copy assignment operator, it almost certainly requires all three. This is usually because the class manages a dynamically allocated resource (like raw heap memory, file handles, or network sockets), and the default compiler-generated shallow copy operations will lead to double-frees or resource leaks.

### Q6: Can you call a virtual function from a constructor or destructor?
- **Answer:** Yes, but it will NOT exhibit polymorphic behavior. During the execution of a base class constructor or destructor, the derived class part of the object has either not been constructed yet, or has already been destroyed. Therefore, calling a virtual function inside the base constructor will call the *base class's* version of the function, to prevent accessing uninitialized derived class memory.

### Q7: What is the size of an empty class in C++?
- **Answer:** 1 byte. To ensure that two distinct objects of the same class have different, unique memory addresses, the C++ standard dictates that the size of any object must be at least 1 byte. However, if the class has a virtual function, its size increases by the size of a pointer (usually 8 bytes on 64-bit systems) to store the `vptr`.

### Q8: Can a constructor be virtual? What about a destructor?
- **Answer:** A constructor **cannot** be virtual. Virtual functions rely on the `vptr` and `vtable`, but the `vptr` is only fully initialized *during* the constructor's execution. Therefore, dynamic dispatch is impossible during object construction. 
Conversely, a destructor **must** often be virtual. If you delete a derived object through a base class pointer without a virtual destructor, only the base class destructor is called, causing a massive memory leak of the derived parts.

### Q9: What is the difference between `malloc/free` and `new/delete`?
- **Answer:** 
  - `malloc()` allocates raw memory on the heap and returns a `void*`. It does not call constructors.
  - `new` allocates memory AND calls the constructor to properly initialize the object.
  - `free()` deallocates raw memory.
  - `delete` calls the destructor first, then deallocates memory. Never mix them (`malloc` with `delete` is undefined behavior).

### Q10: What is a Deep Copy vs a Shallow Copy, and when do we need a custom Copy Constructor?
- **Answer:** A shallow copy simply copies the values of member variables (the default behavior). If a class has pointers to dynamically allocated memory, a shallow copy copies the pointer address, causing two objects to point to the exact same heap memory (leading to double-free crashes). A Deep Copy allocates brand new heap memory for the copy. You need a custom Copy Constructor and Assignment Operator (Rule of Three) whenever your class manages dynamic memory.

### Q11: Explain the "Diamond Problem" in multiple inheritance and how to solve it.
- **Answer:** If class `B` and `C` both inherit from `A`, and class `D` inherits from both `B` and `C`, `D` will contain *two separate copies* of `A`'s member variables, leading to ambiguity and bloated size. We solve this using **Virtual Inheritance** (`class B : virtual public A`). This ensures that `D` receives only one shared instance of `A`.

### Q12: What is an Abstract Class and an Interface in C++?
- **Answer:** C++ does not have an explicit `interface` keyword. An **Abstract Class** is any class that contains at least one **Pure Virtual Function** (`virtual void func() = 0;`). It cannot be instantiated. An **Interface** is effectively an Abstract Class where *all* functions are pure virtual and it has no member variables.

### Q13: What happens if you call a virtual function from inside a constructor or destructor?
- **Answer:** The virtual mechanism is effectively disabled. If a base class constructor calls a virtual function, it calls the *base* class's version, not the derived class's version. This is because the derived part of the object hasn't been constructed yet (or has already been destroyed), so calling a derived method would access uninitialized memory.
