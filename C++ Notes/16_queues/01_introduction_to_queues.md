# Lecture 79: Introduction to Queues: FIFO Discipline & Memory Layouts

> **One-Line Purpose:** Master First-In-First-Out (FIFO) queue abstract data types, analyzing fixed array false-overflow and linked list node chains.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #79  
> **Video ID:** `Khf9v67Ya30`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Khf9v67Ya30)  
> **Duration:** 18:55  
> **Status:** AUDITED  

---

## 🔵 Implementation via Singly Linked List

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

template <typename T>
class Queue {
private:
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };

    Node* head;
    Node* tail;
    int count;

public:
    Queue() : head(nullptr), tail(nullptr), count(0) {}

    ~Queue() {
        while (!empty()) pop();
    }

    void push(T val) {
        Node* newNode = new Node(val);
        if (empty()) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        count++;
    }

    void pop() {
        if (empty()) throw runtime_error("Queue Underflow");
        Node* temp = head;
        head = head->next;
        if (!head) tail = nullptr;
        delete temp;
        count--;
    }

    T front() const {
        if (empty()) throw runtime_error("Queue is empty");
        return head->data;
    }

    bool empty() const { return head == nullptr; }
    int size() const { return count; }
};
```
