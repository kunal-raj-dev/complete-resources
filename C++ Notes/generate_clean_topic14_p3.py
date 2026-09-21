import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t14_dir = os.path.join(root, "14_linked_list")

notes = {}

# 07: Doubly Linked List
notes["07_doubly_linked_list.md"] = r"""# Lecture 63: Doubly Linked List: Bidirectional Pointers & In-Place Splicing

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
"""

# 08: Circular Linked List
notes["08_circular_linked_list.md"] = r"""# Lecture 64: Circular Linked List: Tail Pointer & Modulo Traversal

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
"""

# 09: Flatten a Multilevel Doubly Linked List
notes["09_flatten_multilevel_doubly_linked_list.md"] = r"""# Lecture 65: Flatten a Multilevel Doubly Linked List: DFS Splice (LeetCode 430)

> **One-Line Purpose:** Master 2D multilevel hierarchy flattening by splicing child doubly linked lists in-place between consecutive parent nodes using iterative DFS traversal in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #65  
> **Video ID:** `I8b0rff5F9M`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=I8b0rff5F9M)  
> **Duration:** 24:47  
> **Transcript:** `.transcripts/14_linked_list/065_Flatten_a_Doubly_Linked_List___Leetcode_430___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The structure of a Multilevel Doubly Linked List: nodes containing `prev`, `next`, and an optional `child` pointer.
- Why flattening corresponds to a **Depth-First Search (DFS) Pre-order Traversal**.
- The 5-step pointer rewiring procedure:
  1. Find child list tail.
  2. Stitch child tail to `curr->next`.
  3. Stitch `curr` to child head.
  4. Nullify `curr->child`.
  5. Repeat traversal seamlessly.
- How to achieve strict $O(N)$ time and $O(1)$ auxiliary space without recursion stack overhead.

---

## 🔵 Lecture Context

Multilevel Linked Lists represent hierarchical trees disguised as linked structures. Flattening tests non-trivial pointer arithmetic, preserving bidirectional invariants across parent and child levels.

---

## 1. Problem Statement

You are given a doubly linked list where each node has a `next` pointer, a `prev` pointer, and a `child` pointer that may point to a separate doubly linked list.
Flatten the list so that all the nodes appear in a single-level doubly linked list. The nodes should appear in **depth-first order**.

```
1 <-> 2 <-> 3 <-> 4
            |
            7 <-> 8
                  |
                  11 <-> 12

Flattened Order: 1 <-> 2 <-> 3 <-> 7 <-> 8 <-> 11 <-> 12 <-> 4
```

---

## 2. The 5-Step In-Place Splicing Algorithm

Traverse the list using pointer `curr`:
If `curr->child != nullptr`:
1. **Locate Child Tail:** Advance a pointer `tail = curr->child` until `tail->next == nullptr`.
2. **Connect Child Tail to Next:**
   - `tail->next = curr->next;`
   - If `curr->next != nullptr`: `curr->next->prev = tail;`
3. **Connect Curr to Child Head:**
   - `curr->next = curr->child;`
   - `curr->child->prev = curr;`
4. **Reset Child Pointer:**
   - `curr->child = nullptr;`
5. Advance `curr = curr->next`.

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
    Node(int _val) : val(_val), prev(nullptr), next(nullptr), child(nullptr) {}
};

class Solution {
public:
    Node* flatten(Node* head) {
        if (head == nullptr) return nullptr;

        Node* curr = head;
        while (curr != nullptr) {
            // If current node has a child branch
            if (curr->child != nullptr) {
                // 1. Find the tail of the child branch
                Node* tail = curr->child;
                while (tail->next != nullptr) {
                    tail = tail->next;
                }

                // 2. Connect child tail to curr->next
                tail->next = curr->next;
                if (curr->next != nullptr) {
                    curr->next->prev = tail;
                }

                // 3. Connect curr to child head
                curr->next = curr->child;
                curr->child->prev = curr;

                // 4. Nullify child pointer
                curr->child = nullptr;
            }

            // Advance to next node (which might be the newly spliced child!)
            curr = curr->next;
        }

        return head;
    }
};
```

- **Time Complexity:** $O(N)$ (Each node is visited at most twice).
- **Auxiliary Space Complexity:** $O(1)$ (In-place pointer rewiring).

---

## 🔍 Detailed Trace: Splicing `3` with child `7 <-> 8` and `curr->next = 4`

1. `curr` is at 3. `curr->child` is 7.
2. `tail` traverses to 8.
3. Stitch 8 to 4: `8->next = 4`, `4->prev = 8`.
4. Stitch 3 to 7: `3->next = 7`, `7->prev = 3`.
5. Nullify: `3->child = nullptr`.
6. List is now: `1 <-> 2 <-> 3 <-> 7 <-> 8 <-> 4`.
7. `curr` advances to 7 and continues traversal!

---

## 🧠 Mental Model: Unfolding an Accordion

Think of each child list as an accordion fold tucked under a main street. To flatten it, you cut the main street after the parent, unfold the child street into the gap, stitch both ends back to the pavement, and continue walking forward.

---

## ⚠️ Common Mistakes

1. **Forgetting to nullify `curr->child`:** LeetCode requires all `child` pointers in the final list to be `nullptr`.
2. **Missing `curr->next != nullptr` check:** If the parent node was the last node of its level, `curr->next` is `nullptr`, so accessing `curr->next->prev` triggers a segmentation fault.

---

## 🖥️ System-Specific Notes

- The iterative splicing approach uses $O(1)$ memory, which avoids stack overflow for deep multilevel structures with $10^5$ nested levels.

---

## 🟡 Additional Essential Context

This can also be implemented recursively using a `std::stack<Node*>`:
Push `curr->next` onto the stack, explore `curr->child`, and pop from the stack when a branch terminates.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does the while loop visit each node at most twice?  
**A:** We visit nodes once during the main traversal, and the child search only traverses each child segment once to find its tail. Thus, total operations are bounded by $2N = O(N)$.

---

### 🔥 Interview Questions

#### Q1: What is the benefit of the iterative splicing approach over recursive DFS?
- **Short Answer:** Iterative splicing runs in $O(1)$ auxiliary space without stack overhead, whereas recursive DFS takes $O(N)$ stack frames in the worst case of degenerate vertical trees.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// 1 <-> 2 with child 3 on node 1
// Flattened: 1 <-> 3 <-> 2
```

---

## Edge Cases

1. **No Child Pointers (Flat List):** Loop completes with zero modifications in $O(N)$ time.
2. **All Nodes Have Children (Vertical Spine):** Spliced sequentially into a linear chain.

---

## Complexity Analysis

- **Time Complexity:** $O(N)$ where $N$ is the total number of nodes.
- **Auxiliary Space Complexity:** $O(1)$ (Pointer updates only).

---

## Key Takeaways

1. **DFS Pre-order Order:** Child branches are explored before the parent's next sibling.
2. **In-place Splicing:** Connect child tail to next node; connect curr to child head.
3. **Zero Heap Allocation:** Pure pointer rewiring.

---

## ⚡ 2-Minute Revision

- Find child tail: `while (tail->next) tail = tail->next;`.
- Stitch: `tail->next = curr->next; if (curr->next) curr->next->prev = tail;`.
- Connect: `curr->next = curr->child; curr->child->prev = curr; curr->child = nullptr;`.
"""

print("Writing batch 3 linked list...")
for fn, content in notes.items():
    with open(os.path.join(t14_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 07, 08, 09 in Topic 14.")
