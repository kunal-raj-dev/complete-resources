# Lecture 68: Introduction to Stacks: Implementations & Memory Mechanics

> **One-Line Purpose:** Master the Last-In-First-Out (LIFO) abstract data type, implementing stacks via arrays, vectors, and linked lists with constant-time operations.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #68  
> **Video ID:** `0X-fV-1ir9c`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=0X-fV-1ir9c)  
> **Duration:** 22:11  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

- Understand the LIFO access discipline and Stack ADT operations: `push()`, `pop()`, `top()`, `empty()`, `size()`.
- Compare Array-based vs Linked-List-based implementations: fixed buffer vs dynamic heap allocation.
- Standard Library `std::stack` adaptor mechanics.

---

## 🔵 Complete C++ Implementation via Linked List

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

template <typename T>
class Stack {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };

    Node* head;
    int count;

public:
    Stack() : head(nullptr), count(0) {}

    ~Stack() {
        while (!empty()) {
            pop();
        }
    }

    void push(T val) {
        Node* newNode = new Node(val);
        newNode->next = head;
        head = newNode;
        count++;
    }

    void pop() {
        if (empty()) throw runtime_error("Stack Underflow");
        Node* temp = head;
        head = head->next;
        delete temp;
        count--;
    }

    T top() const {
        if (empty()) throw runtime_error("Stack is empty");
        return head->data;
    }

    bool empty() const { return head == nullptr; }
    int size() const { return count; }
};
```
- **Time Complexity:** All operations (`push`, `pop`, `top`, `empty`, `size`) are strictly $O(1)$.
