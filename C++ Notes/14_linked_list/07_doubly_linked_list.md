# Lecture 63: Doubly Linked List: Bidirectional Pointers & In-Place Splicing

> **One-Line Purpose:** Master bidirectional pointer mechanics in Doubly Linked Lists (DLL), establishing forward and backward invariant traversals and enabling $O(1)$ node deletion given a direct node reference.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #63  
> **Video ID:** `bO5DasTsaRQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=bO5DasTsaRQ)  
> **Duration:** 32:16  
> **Transcript:** `.transcripts/14_linked_list/063_Doubly_Linked_List_Tutorial.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The fundamental limitation of Singly Linked Lists: impossibility of backward traversal ($O(N)$ predecessor lookup).
- Doubly Linked List (DLL) node anatomy: `data`, `next`, and `prev` pointers.
- Complete DLL operations: `push_front`, `push_back`, `pop_front`, `pop_back`, and deletion of a target node.
- The 4-pointer rewiring sequence required to delete a node in strict $O(1)$ time.
- Memory trade-offs: 24 bytes per node vs 16 bytes in singly linked lists.

---

## 🔵 Lecture Context

Doubly Linked Lists solve the single biggest shortcoming of singly linked lists: deleting an arbitrary node in $O(1)$ time without needing a reference to its predecessor. This capability makes DLL the core underlying data structure for LRU Cache (Lecture 78), Deque, and OS Process Schedulers.

---

## 1. Why Doubly Linked Lists Exist

In a Singly Linked List:
- If you are given a pointer to node $X$ in the middle of the list and told to delete it, you **cannot** update the previous node's pointer without traversing from `head` ($O(N)$).
- You cannot traverse backward.

In a Doubly Linked List:
- Each node stores a pointer to its previous neighbor (`prev`).
- Any node can be detached in $O(1)$ time by rewiring its neighbors:
  `curr->prev->next = curr->next;`
  `curr->next->prev = curr->prev;`

---

## 2. Complete C++ Doubly Linked List Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    Node* prev;

    Node(int val) {
        data = val;
        next = nullptr;
        prev = nullptr;
    }
};

class DoublyList {
private:
    Node* head;
    Node* tail;

public:
    DoublyList() {
        head = nullptr;
        tail = nullptr;
    }

    ~DoublyList() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* nextNode = curr->next;
            delete curr;
            curr = nextNode;
        }
        head = tail = nullptr;
    }

    // 1. Insert at Beginning: O(1)
    void push_front(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = tail = newNode;
            return;
        }
        newNode->next = head;
        head->prev = newNode;
        head = newNode;
    }

    // 2. Insert at End: O(1)
    void push_back(int val) {
        Node* newNode = new Node(val);
        if (head == nullptr) {
            head = tail = newNode;
            return;
        }
        tail->next = newNode;
        newNode->prev = tail;
        tail = newNode;
    }

    // 3. Delete from Beginning: O(1)
    void pop_front() {
        if (head == nullptr) return;

        Node* temp = head;
        head = head->next;
        if (head != nullptr) {
            head->prev = nullptr;
        } else {
            tail = nullptr; // List became empty
        }
        delete temp;
    }

    // 4. Delete from End: O(1) (Crucial DLL advantage!)
    void pop_back() {
        if (head == nullptr) return;

        Node* temp = tail;
        tail = tail->prev;
        if (tail != nullptr) {
            tail->next = nullptr;
        } else {
            head = nullptr; // List became empty
        }
        delete temp;
    }

    // 5. Delete specific node: O(1)
    void deleteNode(Node* target) {
        if (target == nullptr) return;
        if (target == head) { pop_front(); return; }
        if (target == tail) { pop_back(); return; }

        target->prev->next = target->next;
        target->next->prev = target->prev;
        delete target;
    }

    // Forward print
    void printForward() {
        Node* temp = head;
        cout << "Forward: ";
        while (temp != nullptr) {
            cout << temp->data << " <-> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }

    // Backward print
    void printBackward() {
        Node* temp = tail;
        cout << "Backward: ";
        while (temp != nullptr) {
            cout << temp->data << " <-> ";
            temp = temp->prev;
        }
        cout << "NULL\n";
    }
};

int main() {
    DoublyList dll;
    dll.push_back(10);
    dll.push_back(20);
    dll.push_back(30);
    dll.push_front(5);

    dll.printForward();  // 5 <-> 10 <-> 20 <-> 30 <-> NULL
    dll.printBackward(); // 30 <-> 20 <-> 10 <-> 5 <-> NULL

    dll.pop_back();      // Deletes 30 in O(1) time
    dll.printForward();  // 5 <-> 10 <-> 20 <-> NULL
    return 0;
}
```

---

## 🔍 Detailed Trace: In-Place Node Splice

Given `A <-> B <-> C`. To delete `B`:
1. `B->prev` points to `A`. Set `A->next = B->next` (`A->next` now points to `C`).
2. `B->next` points to `C`. Set `C->prev = B->prev` (`C->prev` now points to `A`).
3. Delete `B`.
Result: `A <-> C`. Spliced in $O(1)$ operations with zero loops.

---

## 🧠 Mental Model: Holding Hands in a Circle

In a singly linked list, each person holds only the shoulder of the person in front of them. In a doubly linked list, each person clasps hands with both the person in front and the person behind. When someone steps out, the two neighbors grasp each other's hands directly.

---

## ⚠️ Common Mistakes

1. **Forgetting to update `prev` pointer:** Updating `curr->next = ...` but forgetting `next_node->prev = curr`, leaving an inconsistent bidirectional state.
2. **Null Checks on Boundary Deletions:** Attempting `target->prev->next` when `target == head` causes a null-pointer dereference (`nullptr->next`).

---

## 🖥️ System-Specific Notes

- In 64-bit systems, a DLL node has: 4 bytes (data) + 4 bytes (padding) + 8 bytes (`next`) + 8 bytes (`prev`) = **24 bytes per node**.
- In C++ STL, `std::list` is implemented as a Doubly Linked List.

---

## 🟡 Additional Essential Context

The sentinel pattern with two dummy nodes (`dummyHead` and `dummyTail`) eliminates all null checks in DLL implementations, as used in LRU Cache.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can DLL delete the tail in $O(1)$ time while Singly Linked List takes $O(N)$?  
**A:** Because DLL's `tail` pointer has direct access to `tail->prev`, allowing the second-to-last node to be updated immediately without traversal.

---

### 🔥 Interview Questions

#### Q1: How do you reverse a Doubly Linked List in-place?
- **Short Answer:** Swap the `next` and `prev` pointers of every node in a single linear traversal.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// DLL: 1 <-> 2 <-> 3
// Reverse: Swap prev and next for each node.
// Output: 3 <-> 2 <-> 1
```

---

## Edge Cases

1. **Single Node DLL:** Deleting head/tail must reset both `head` and `tail` to `nullptr`.
2. **Empty List:** Operations must be no-ops without throwing exceptions.

---

## Complexity Analysis

| Operation | Singly Linked List | Doubly Linked List |
|---|---|---|
| `push_front` | $O(1)$ | $O(1)$ |
| `push_back` | $O(1)$ | $O(1)$ |
| `pop_front` | $O(1)$ | $O(1)$ |
| `pop_back` | $O(N)$ | **$O(1)$** |
| `deleteNode(target)` | $O(N)$ | **$O(1)$** |

---

## Key Takeaways

1. **Bidirectional Links:** Enables backward traversal and $O(1)$ deletion.
2. **Splicing Formula:** `curr->prev->next = curr->next; curr->next->prev = curr->prev;`.
3. **Memory Overhead:** 24 bytes per node vs 16 bytes for singly linked lists.

---

## ⚡ 2-Minute Revision

- Node: `data`, `next`, `prev`.
- Splicing: `target->prev->next = target->next; target->next->prev = target->prev;`.
- Delete tail: `tail = tail->prev; tail->next = nullptr;`.


## 🧠 Core Intuition — Why This Works
A Doubly Linked List (DLL) solves the primary weakness of a Singly Linked List: unidirectional traversal. By adding a `prev` pointer to each node, we can traverse backwards in $O(1)$ time. This makes operations like deleting a known node or inserting before a node strictly $O(1)$, because we don't need to traverse from the head to find the preceding node!

## 🎯 Pattern Recognition — When to Use This
- **"Delete a node in $O(1)$ time given its pointer"**: Singly linked lists require $O(N)$ to find the previous node (unless using a value-swap trick). DLLs do it inherently.
- **LRU Cache Implementation**: The most famous use case for DLLs. You need $O(1)$ removal of a node from the middle and $O(1)$ insertion at the head.
- **Complex UI Histories**: Browser back/forward buttons, music playlist next/previous logic.

## 🔍 Dry Run Trace
**Example:** Deleting node `B` from `A <-> B <-> C`
- We are given a pointer to `B`.
- `B->prev` is `A`. `B->next` is `C`.
- Step 1: `B->prev->next = B->next` (makes `A` point forward to `C`)
- Step 2: `B->next->prev = B->prev` (makes `C` point backward to `A`)
- Step 3: `delete B`
Result: `A <-> C`. Both forward and backward links are maintained.

## ⚠️ Common Interview Mistakes
1. **Forgetting `prev` pointer updates:** When inserting or deleting, candidates often perfectly wire the `next` pointers but forget the `prev` pointers. Always verify both directions!
2. **Head/Tail edge cases:** Deleting the head node means `head->prev` doesn't exist, and `B->prev` becomes `NULL`. Checking `if (node->prev != NULL)` before assignment is mandatory to avoid null pointer dereferences.
3. **Memory Leaks:** Forgetting to actually free the memory after bypassing the node.

## 📊 Complexity Analysis
- **Access:** $O(N)$
- **Insert/Delete at ends:** $O(1)$
- **Insert/Delete given a pointer:** $O(1)$ (This is the defining advantage over Singly LL)
- **Space Overhead:** $O(1)$ extra space per node (for the `prev` pointer).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can a DLL be implemented with a single pointer?
**Answer:** Yes! An **XOR Linked List** compresses the `prev` and `next` pointers into a single field by storing their bitwise XOR: `ptr = prev ^ next`. When traversing forward from `prev`, the next node is `ptr ^ prev`. When traversing backward from `next`, the previous node is `ptr ^ next`. This reduces memory overhead back to that of a Singly LL while maintaining bi-directional traversal capabilities.

### Q2: Why isn't a DLL used everywhere if it's strictly better than Singly LL for insertions/deletions?
**Answer:** Memory overhead and maintenance complexity. The extra pointer takes up 8 bytes (on 64-bit systems) per node, increasing the memory footprint by 33%-50%. Additionally, maintaining two pointers per link doubles the chance of bugs and cache misses. Singly linked lists are preferred unless $O(1)$ reverse traversal or deletion is strictly required.

## 🏆 Related Problems
- **[146. LRU Cache](https://leetcode.com/problems/lru-cache/)**: The ultimate test of Doubly Linked Lists combined with Hash Maps.
- **[460. LFU Cache](https://leetcode.com/problems/lfu-cache/)**: An even more complex cache using multiple DLLs.
- **[432. All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/)**: Requires advanced DLL manipulation.

## 🔗 Cross-Topic Connections
- **Hash Maps:** Often paired together (e.g., in LRU cache) so that the Hash Map provides $O(1)$ lookup to the node, and the DLL provides $O(1)$ structural modification.

## ⚡ 2-Minute Revision Flash Card
- **Structure:** `struct Node { int val; Node* prev; Node* next; }`
- **Superpower:** $O(1)$ deletion from the middle (given the node pointer).
- **Core Deletion Logic:** `node->prev->next = node->next; node->next->prev = node->prev;`
- **Trap:** Always guard against `NULL` for head/tail boundary nodes!
