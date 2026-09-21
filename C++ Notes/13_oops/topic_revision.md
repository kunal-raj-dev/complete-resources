# ⚡ Topic 13 Revision: Object-Oriented Programming (OOPs) in C++

> **High-Density Review:** The 4 pillars, VTable/VPtr dynamic dispatch, Deep vs Shallow copy, and Virtual Destructors.

---

## 1. The 4 Pillars of OOP
1. **Encapsulation:** Bundling data and methods into a class while restricting direct access via access specifiers (`private`, `protected`, `public`).
2. **Abstraction:** Hiding complex implementation details and exposing only clean interfaces (Abstract classes, pure virtual functions `= 0`).
3. **Inheritance:** Deriving new classes from existing ones (`public`, `protected`, `private` inheritance).
4. **Polymorphism:**
   - **Compile-Time (Static):** Function Overloading, Operator Overloading, Templates.
   - **Run-Time (Dynamic):** Virtual Functions (`virtual`), Function Overriding via VTable.

---

## 2. VTable and VPtr Architecture
```text
Object Memory Layout:
[ __vptr ] ---> [ &Base::func1 ]
[ data1  ]      [ &Derived::func2 ]
[ data2  ]
```
- Each class containing at least one virtual function has a static **VTable** (array of function pointers).
- Each instantiated object contains an invisible **VPtr** pointing to the class VTable.
- Function call `ptr->func()` resolves dynamically: `*(ptr->__vptr[index])()`.

---

## 3. Copy Mechanics
- **Shallow Copy:** Default behavior. Copies pointer addresses. Leads to double-free crashes when both objects are destroyed.
- **Deep Copy:** Custom copy constructor that allocates *new* heap memory and copies the *values*.
```cpp
// Deep Copy Constructor Pattern
MyClass(const MyClass& other) {
    this->data = new int(*(other.data));
}
```

---

## 4. Key OOP Keywords
- `virtual`: Opts a function into dynamic dispatch (vtable).
- `override`: Verifies at compile time that the function correctly matches a virtual function signature in the base class.
- `final`: Prevents a class from being inherited or a virtual function from being overridden.
- `friend`: Allows an external function or class to access `private` and `protected` members of the class.
- `static`: Class-level variable/function. Shared across all instances. Cannot access `this` pointer.

---

## 5. Critical Edge Cases to Remember
- **Virtual Destructors:** ALWAYS use them in a base class if you intend to delete derived objects polymorphically (via a base pointer).
- **Diamond Problem:** Class D inherits B and C, which both inherit A. Use `virtual` inheritance (`class B : virtual public A`) so D only gets one copy of A.
- **Object Slicing:** Never pass polymorphic objects by value (e.g., `void process(Base obj)`). Always pass by pointer or reference (`void process(Base* obj)`).

---

## 5. Advanced Pointer Concepts
- **`this` Pointer:** A hidden constant pointer passed as a secret argument to all non-static member functions, pointing to the object invoking the function.
- **Smart Pointers (C++11):** 
  - `std::unique_ptr`: Exclusive ownership, cannot be copied, only moved. Destroys object when out of scope.
  - `std::shared_ptr`: Shared ownership, uses reference counting. Destroys object when count hits zero.
  - `std::weak_ptr`: Observes a `shared_ptr` without increasing the reference count. Prevents cyclic dependency memory leaks.

## 6. Access Specifiers and Inheritance
- **Public Inheritance:** Public stays public, protected stays protected.
- **Protected Inheritance:** Both public and protected become protected in derived class.
- **Private Inheritance:** Both public and protected become private in derived class.
- **Friend Functions:** `friend` functions or classes bypass access specifiers and can read `private` members of a class. Friendship is NOT inherited.

## 7. Virtual Tables (vtable) and Dynamic Dispatch
- If a class has at least one virtual function, the compiler creates a `vtable` (array of function pointers) for the class.
- Every object of this class contains a hidden pointer (`vptr`) pointing to the class's `vtable`.
- At runtime, polymorphic calls (`basePtr->func()`) look up the correct function address in the `vtable`, enabling dynamic dispatch.

## ⚡ 2-Minute Revision Flash Card
- **4 Pillars:** Encapsulation (data hiding), Abstraction (implementation hiding), Inheritance (code reuse), Polymorphism (many forms).
- **Virtual Destructors:** ALWAYS use `virtual ~Base()` to prevent derived class memory leaks.
- **Pure Virtual Function:** `virtual void func() = 0;` creates an Abstract Class.
- **Static Members:** Belong to the class, not the object. Cannot access `this`.
