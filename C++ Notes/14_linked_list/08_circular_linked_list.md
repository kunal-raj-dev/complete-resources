# Lecture 64: Circular Linked List: Tail Pointer & Modulo Traversal

> **One-Line Purpose:** Master Circular Linked List (CLL) architectures, optimizing insertion and deletion using a single `tail` pointer and formulating continuous cyclic scheduling loops.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #64  
> **Video ID:** `e6lZY5Yha8U`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=e6lZY5Yha8U)  
> **Duration:** 33:56  
> **Transcript:** `.transcripts/14_linked_list/064_Circular_Linked_List_in_Data_Structures.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What a Circular Linked List is and how its terminal node loops back to `head` (`tail->next == head`).
- Why maintaining a single **`tail` pointer** grants $O(1)$ access to both head (`tail->next`) and tail (`tail`), making a separate `head` pointer redundant.
- Operations: `insertAtHead`, `insertAtTail`, `deleteHead`, `deleteTail`, and cyclic traversal.
- Real-world applications: OS Round-Robin CPU scheduling, multiplayer game turn rotation, and media players.

---

## 🔵 Lecture Context

In linear linked lists, reaching `nullptr` terminates traversal. Circular lists represent closed endless loops, requiring do-while loops or stop-node tracking to prevent infinite execution.

---

## 1. Problem Statement & Architecture

In a Singly Circular Linked List, the last node's `next` pointer points back to the first node instead of `nullptr`.

```
Linear:   1 -> 2 -> 3 -> NULL
Circular: 1 -> 2 -> 3 ---+
          ^              |
          +--------------+
```

### 💡 The Tail Pointer Optimization:
If we store only `head`, finding the last node takes $O(N)$ time.
If we store only `tail`:
- `tail` is the last node! ($O(1)$ access)
- `tail->next` is the head node! ($O(1)$ access)
Maintaining a single `tail` pointer provides instant $O(1)$ operations at both ends!

---

## 2. Complete C++ Circular Linked List Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

class CircularList {
private:
    Node* tail;

public:
    CircularList() {
        tail = nullptr;
    }

    ~CircularList() {
        if (tail == nullptr) return;
        Node* curr = tail->next;
        tail->next = nullptr; // Break circle to make linear
        while (curr != nullptr) {
            Node* nextNode = curr->next;
            delete curr;
            curr = nextNode;
        }
        tail = nullptr;
    }

    // 1. Insert at Head: O(1)
    void push_front(int val) {
        Node* newNode = new Node(val);
        if (tail == nullptr) {
            tail = newNode;
            tail->next = tail; // Points to itself
            return;
        }
        newNode->next = tail->next; // Point new node to head
        tail->next = newNode;       // Tail now points to new head
    }

    // 2. Insert at Tail: O(1)
    void push_back(int val) {
        Node* newNode = new Node(val);
        if (tail == nullptr) {
            tail = newNode;
            tail->next = tail;
            return;
        }
        newNode->next = tail->next; // Point new node to head
        tail->next = newNode;       // Old tail points to new node
        tail = newNode;             // Advance tail pointer!
    }

    // 3. Delete Head: O(1)
    void pop_front() {
        if (tail == nullptr) return;

        // Only one node
        if (tail->next == tail) {
            delete tail;
            tail = nullptr;
            return;
        }

        Node* head = tail->next;
        tail->next = head->next;
        delete head;
    }

    // 4. Print List: O(N)
    void print() {
        if (tail == nullptr) {
            cout << "Empty List\n";
            return;
        }

        Node* temp = tail->next; // Start at head
        do {
            cout << temp->data << " -> ";
            temp = temp->next;
        } while (temp != tail->next);
        cout << "(Back to Head)\n";
    }
};

int main() {
    CircularList cll;
    cll.push_back(10);
    cll.push_back(20);
    cll.push_back(30);
    cll.push_front(5);

    cll.print(); // Output: 5 -> 10 -> 20 -> 30 -> (Back to Head)
    cll.pop_front();
    cll.print(); // Output: 10 -> 20 -> 30 -> (Back to Head)
    return 0;
}
```

---

## 🔍 Detailed Trace: `push_back(30)` on `10 -> 20 -> (10)`

1. Currently `tail` is node `20`, `tail->next` is `10` (head).
2. Create `newNode(30)`.
3. `newNode->next = tail->next` (`30->next` points to `10`).
4. `tail->next = newNode` (`20->next` points to `30`).
5. `tail = newNode` (tail pointer moves to `30`).
Result: `10 -> 20 -> 30 -> (Back to 10)`.

---

## 🧠 Mental Model: Carousel

Think of a playground carousel. There is no beginning and no end. Maintaining a tail pointer is like putting a red ribbon on one seat. The seat right in front of the red ribbon is seat #1.

---

## ⚠️ Common Mistakes

1. **Infinite Loop in Traversal:** Writing `while (temp != nullptr)`. In a circular list, `temp` is never `nullptr`! Always use `do ... while (temp != head)`.
2. **Deleting the Only Node:** If `tail->next == tail`, deleting without resetting `tail = nullptr` creates a dangling pointer.

---

## 🖥️ System-Specific Notes

- In operating systems, the **Round Robin Scheduler** keeps a circular queue of runnable threads. When a thread's time slice expires, the CPU context-switches to `curr->next`.

---

## 🟡 Additional Essential Context

The classical **Josephus Problem** (counting out game where every $k$-th person is eliminated) is solved naturally using a Circular Linked List in $O(N \cdot k)$ time.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why is a single `tail` pointer superior to keeping both `head` and `tail` in a Circular Linked List?  
**A:** Because `head` is always implicitly available in $O(1)$ via `tail->next`. Storing `head` as a separate member variable creates redundancy and requires updating two pointers on insertions.

---

### 🔥 Interview Questions

#### Q1: How do you detect if a given linked list is circular?
- **Short Answer:** Use Floyd's cycle-finding algorithm, or advance from `head` and check if you reach `head` again before hitting `nullptr`.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// Single node: cll.push_back(1);
// cll.print();
// Output: 1 -> (Back to Head)
```

---

## Edge Cases

1. **Empty List:** `tail == nullptr`. Handled gracefully.
2. **Single Element Loop:** `tail->next == tail`.

---

## Complexity Analysis

| Operation | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| `push_front` | $O(1)$ | $O(1)$ |
| `push_back` | $O(1)$ | $O(1)$ |
| `pop_front` | $O(1)$ | $O(1)$ |
| `print` | $O(N)$ | $O(1)$ |

---

## Key Takeaways

1. **Single Tail Pointer:** Yields $O(1)$ head and tail operations.
2. **Do-While Loop:** Ensures full single-loop traversal.
3. **Destructor cleanup:** Break circle (`tail->next = nullptr`) before linear deletion.

---

## ⚡ 2-Minute Revision

- Head is `tail->next`.
- Loop traversal: `do { temp = temp->next; } while (temp != head);`.
- Space: $O(1)$.
