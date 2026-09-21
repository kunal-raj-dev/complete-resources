import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t14_dir = os.path.join(root, "14_linked_list")

notes = {}

# 01: Introduction to Linked List
notes["01_introduction_to_linked_list.md"] = r"""# Lecture 57: Introduction to Linked List: Memory Anatomy & Operations

> **One-Line Purpose:** Master the foundations of Linked Lists, understanding non-contiguous heap memory allocation, node pointer anatomy, and implementing complete insertion, deletion, search, and destructor cleanup operations.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #57  
> **Video ID:** `LyuuqCVkP5I`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=LyuuqCVkP5I)  
> **Duration:** 50:43  
> **Transcript:** `.transcripts/14_linked_list/057_Introduction_to_Linked_List___Data_Structures___Algorithms.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What a Linked List is and why it exists alongside Arrays and Vectors.
- Non-contiguous memory allocation on the Heap versus contiguous stack/heap buffers.
- Node anatomy in C++: data payload and the self-referential `next` pointer.
- Fundamental CRUD operations: `push_front`, `push_back`, `pop_front`, `pop_back`, and `insert(pos, val)`.
- Why C++ classes for Linked Lists require an explicit **Destructor (`~List()`)** to prevent memory leaks.

---

## 🔵 Lecture Context

Arrays and Vectors require contiguous memory blocks. In contrast, Linked Lists represent dynamic chains of independently allocated nodes. Mastering pointer manipulation in Linked Lists is the prerequisite for Stacks, Queues, Graphs (Adjacency Lists), and LRU Caches (Lecture 78).

---

## 1. Why Linked List Exists (Array vs Linked List)

| Metric | Array / Vector | Singly Linked List |
|---|---|---|
| **Memory Layout** | Strictly contiguous in RAM | Non-contiguous (scattered across heap) |
| **Insertion at Head** | $O(N)$ (Requires shifting all elements right) | $O(1)$ (Update head pointer) |
| **Deletion at Head** | $O(N)$ (Requires shifting all elements left) | $O(1)$ (Update head pointer, delete node) |
| **Random Access (`arr[i]`)**| $O(1)$ via pointer arithmetic | $O(N)$ (Must traverse sequentially from head) |
| **Memory Overhead** | Zero pointer overhead per element | Extra 8 bytes per node for `next` pointer |
| **Cache Locality** | Excellent (CPU prefetching works) | Poor (Pointer hopping causes cache misses) |

---

## 2. Node Anatomy & C++ Implementation

A Node contains data and a pointer to the next node:
```cpp
class Node {
public:
    int data;
    Node* next;

    Node(int val) {
        data = val;
        next = nullptr;
    }
};
```

---

## 3. Complete C++ Linked List Class Implementation

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;

    Node(int val) {
        data = val;
        next = nullptr;
    }
};

class List {
private:
    Node* head;
    Node* tail;

public:
    List() {
        head = nullptr;
        tail = nullptr;
    }

    // Destructor: Clean up all dynamically allocated nodes
    ~List() {
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
        tail = newNode;
    }

    // 3. Delete from Beginning: O(1)
    void pop_front() {
        if (head == nullptr) return;

        Node* temp = head;
        head = head->next;
        if (head == nullptr) {
            tail = nullptr; // List became empty
        }
        delete temp;
    }

    // 4. Delete from End: O(N)
    void pop_back() {
        if (head == nullptr) return;

        // Only one element
        if (head == tail) {
            delete head;
            head = tail = nullptr;
            return;
        }

        // Traverse to find the second-to-last node
        Node* temp = head;
        while (temp->next != tail) {
            temp = temp->next;
        }

        delete tail;
        tail = temp;
        tail->next = nullptr;
    }

    // 5. Insert at Position: O(N)
    void insert(int val, int pos) {
        if (pos < 0) return;
        if (pos == 0) {
            push_front(val);
            return;
        }

        Node* temp = head;
        for (int i = 0; i < pos - 1; i++) {
            if (temp == nullptr) return; // Out of bounds
            temp = temp->next;
        }

        if (temp == nullptr) return;
        if (temp == tail) {
            push_back(val);
            return;
        }

        Node* newNode = new Node(val);
        newNode->next = temp->next;
        temp->next = newNode;
    }

    // 6. Search for Value: O(N)
    int search(int key) {
        Node* temp = head;
        int idx = 0;
        while (temp != nullptr) {
            if (temp->data == key) return idx;
            temp = temp->next;
            idx++;
        }
        return -1;
    }

    // 7. Print List: O(N)
    void print() {
        Node* temp = head;
        while (temp != nullptr) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL\n";
    }
};

int main() {
    List ll;
    ll.push_front(3);
    ll.push_front(2);
    ll.push_front(1);
    ll.push_back(4);
    ll.print(); // Output: 1 -> 2 -> 3 -> 4 -> NULL

    ll.pop_front();
    ll.print(); // Output: 2 -> 3 -> 4 -> NULL

    cout << "Search 3: Index " << ll.search(3) << "\n";
    return 0;
}
```

---

## 🔍 Detailed Trace: Inserting at Position 1 in `1 -> 3 -> NULL`

To insert `2` at index 1:
1. Traverse to index `pos - 1 = 0` (node containing `1`).
2. Create `newNode = new Node(2)`.
3. Set `newNode->next = temp->next` (`2->next` points to `3`).
4. Set `temp->next = newNode` (`1->next` points to `2`).
5. Result: `1 -> 2 -> 3 -> NULL`.

---

## 🧠 Mental Model: Train Cars

Think of a Linked List as a freight train:
- Each car holds freight (`data`) and a coupler (`next` pointer).
- `head` is the locomotive engine; `tail` is the caboose.
- To add a car in the middle, you uncouple the link, attach the new car's coupler to the train behind it, and attach the front car's coupler to the new car.

---

## ⚠️ Common Mistakes

1. **Dangling Pointers and Memory Leaks:** Losing the pointer to a node before calling `delete`. Always save `Node* temp = head; head = head->next; delete temp;`.
2. **Dereferencing `nullptr`:** Writing `temp->next` without verifying `temp != nullptr`.
3. **Broken Reconnection Order:** Setting `temp->next = newNode` *before* `newNode->next = temp->next`. This overwrites `temp->next`, permanently orphaning the rest of the list!

---

## 🖥️ System-Specific Notes

- On 64-bit architectures, pointers are 8 bytes. For `int` data (4 bytes), padding adds 4 bytes of alignment overhead, meaning each `Node` occupies 16 bytes on the heap to store 4 bytes of data.

---

## 🟡 Additional Essential Context

In technical interviews (e.g. LeetCode), problems typically provide raw node structs:
```cpp
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};
```
Interviewers expect you to manipulate raw pointers without relying on class wrappers.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why is `pop_back()` in a Singly Linked List $O(N)$ even when we have a `tail` pointer?  
**A:** Because to delete the tail, we must update the *second-to-last* node's `next` pointer to `nullptr`. Since singly linked lists only have forward pointers, finding the second-to-last node requires traversing $N-1$ nodes from `head`.

---

### 🔥 Interview Questions

#### Q1: What happens if you do not implement a destructor for a custom Linked List class in C++?
- **Short Answer:** It causes a severe memory leak.
- **Detailed Explanation:** When the `List` object goes out of scope, only its local member variables (`head` and `tail` pointers) are popped off the stack. The dynamically allocated `Node` objects on the heap remain allocated in memory until the program terminates.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
#include <iostream>
using namespace std;
struct Node { int val; Node* next; Node(int v): val(v), next(nullptr) {} };

int main() {
    Node* a = new Node(10);
    Node* b = new Node(20);
    a->next = b;
    cout << a->val << " " << a->next->val << "\n";
    delete a;
    delete b;
    return 0;
}
```
**Output:** `10 20`

---

## Edge Cases

1. **Empty List (`head == nullptr`):** Operations must not dereference `head`.
2. **Single Element List (`head == tail`):** `pop_front()` and `pop_back()` must reset both `head` and `tail` to `nullptr`.

---

## Complexity Analysis

| Operation | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| `push_front` | $O(1)$ | $O(1)$ |
| `push_back` | $O(1)$ (with `tail`) | $O(1)$ |
| `pop_front` | $O(1)$ | $O(1)$ |
| `pop_back` | $O(N)$ | $O(1)$ |
| `search` | $O(N)$ | $O(1)$ |
| `insert(pos)`| $O(N)$ | $O(1)$ |

---

## Key Takeaways

1. **Non-contiguous memory:** Nodes linked dynamically via pointers.
2. **$O(1)$ Head Operations:** Instant insertion and deletion at the front.
3. **Destructor cleanup:** Always delete allocated heap memory sequentially.

---

## ⚡ 2-Minute Revision

- Node: `data` + `next`.
- Insertion at head: `newNode->next = head; head = newNode;`.
- Reconnection order: Always set `newNode->next` before breaking existing links.
"""

# 02: Reverse a Linked List
notes["02_reverse_a_linked_list.md"] = r"""# Lecture 58: Reverse a Linked List: Iterative & Recursive (LeetCode 206)

> **One-Line Purpose:** Master the canonical 3-pointer iterative pointer reversal technique and recursive unwinding rewiring to reverse singly linked lists in $O(N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #58  
> **Video ID:** `R-CKBYnOv1U`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=R-CKBYnOv1U)  
> **Duration:** 10:29  
> **Transcript:** `.transcripts/14_linked_list/058_Reverse_a_Linked_List___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The problem requirements of LeetCode 206: reversing a singly linked list in-place.
- The **Golden 3-Pointer Iterative Technique**: `prev`, `curr`, and `next_node`.
- The 4-step pointer rewiring sequence inside the traversal loop.
- The **Recursive Reversal Pattern**: reversing subproblems and reconnecting `head->next->next = head`.
- Edge case handling for empty lists and single-node lists.

---

## 🔵 Lecture Context

Reversing a Linked List is the most frequently tested linked-list interview question. It forms the core subroutine for Palindrome Linked List (LeetCode 234), Reverse Nodes in K-Group (LeetCode 25), and Add Two Numbers (LeetCode 445).

---

## 1. Problem Statement

Given the `head` of a singly linked list, reverse the list and return the reversed list's head.

```
Original: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
Reversed: 5 -> 4 -> 3 -> 2 -> 1 -> NULL
```

---

## 2. Approach 1: The Golden 3-Pointer Iterative Method ($O(1)$ Space)

To reverse the pointers without losing reference to the upcoming nodes, maintain three pointers:
- `prev`: Points to the previous node (initialized to `nullptr`).
- `curr`: Points to the node currently being reversed (initialized to `head`).
- `next_node`: Temporarily stores the upcoming node (`curr->next`).

### The 4-Step Golden Loop:
1. **Save next:** `next_node = curr->next;` (Prevents losing the rest of the list).
2. **Reverse link:** `curr->next = prev;` (Point current node backward).
3. **Advance prev:** `prev = curr;` (Move previous pointer forward).
4. **Advance curr:** `curr = next_node;` (Move current pointer forward).

When `curr` reaches `nullptr`, `prev` points to the new head!

```cpp
#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;

        while (curr != nullptr) {
            ListNode* next_node = curr->next; // Step 1: Save ahead
            curr->next = prev;               // Step 2: Reverse pointer
            prev = curr;                     // Step 3: Advance prev
            curr = next_node;                // Step 4: Advance curr
        }

        return prev; // prev is the new head
    }
};
```

- **Time Complexity:** $O(N)$ (Single pass through the list).
- **Auxiliary Space Complexity:** $O(1)$ (Three pointer variables).

---

## 3. Approach 2: Recursive Reversal ($O(N)$ Space)

```cpp
class SolutionRecursive {
public:
    ListNode* reverseList(ListNode* head) {
        // Base Case: Empty list or single node
        if (head == nullptr || head->next == nullptr) {
            return head;
        }

        // Recursive Call: Reverse the rest of the list
        ListNode* newHead = reverseList(head->next);

        // Self-Work: Reconnect pointers during unwinding
        // head->next is currently the tail of the reversed sublist!
        head->next->next = head;
        head->next = nullptr;

        return newHead;
    }
};
```

---

## 🔍 Detailed Trace: Iterative Reversal on `1 -> 2 -> 3 -> NULL`

| Step | `prev` | `curr` | `next_node` | Action Taken | List State |
|---|---|---|---|---|---|
| Init | `NULL` | `1` | `NULL` | Start | `1 -> 2 -> 3 -> NULL` |
| 1 | `1` | `2` | `2` | `1->next = NULL` | `NULL <- 1   2 -> 3 -> NULL` |
| 2 | `2` | `3` | `3` | `2->next = 1` | `NULL <- 1 <- 2   3 -> NULL` |
| 3 | `3` | `NULL` | `NULL` | `3->next = 2` | `NULL <- 1 <- 2 <- 3` |

Loop ends. Return `prev` (Node 3).

---

## 🧠 Mental Model: Reversing One-Way Arrows

Think of the list as cars on a one-way street. You stand at car `curr`. Before you turn the car around to point at `prev`, you must write down the address of car `next_node`. Once turned, you step forward to make `curr` the new `prev`.

---

## ⚠️ Common Mistakes

1. **Forgetting to save `curr->next`:** Overwriting `curr->next = prev` before storing `curr->next` permanently severs your connection to the remaining nodes, causing premature termination.
2. **Forgetting to set `head->next = nullptr` in recursion:** Causes a memory cycle between the first two nodes (`1 <-> 2`), leading to infinite loops during traversal.

---

## 🖥️ System-Specific Notes

- In competitive programming and systems development, always prefer the **iterative approach** because the recursive approach consumes $O(N)$ call-stack memory, risking stack overflow for lists with $N \ge 10^5$ nodes.

---

## 🟡 Additional Essential Context

The iterative 3-pointer pattern is reused identically in:
- **Reverse Linked List II (LeetCode 92):** Reversing a sub-segment `[left ... right]`.
- **Palindrome Linked List (LeetCode 234):** Find middle, reverse second half, compare halves.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is the invariant condition that holds at the end of each iteration?  
**A:** `prev` is the head of the reversed portion processed so far, and `curr` is the head of the remaining unreversed portion.

---

### 🔥 Interview Questions

#### Q1: Can you reverse a linked list using a Stack? What are the trade-offs?
- **Short Answer:** Yes, pushing all nodes onto a stack and popping them reverses order, but takes $O(N)$ auxiliary space instead of $O(1)$.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// Input: head = NULL
// Output: NULL (Handled cleanly by while (curr != nullptr) returning prev = NULL)
```

---

## Edge Cases

1. **Empty List (`head == nullptr`):** Returns `nullptr`.
2. **Single Node (`head->next == nullptr`):** Returns `head` unchanged.

---

## Complexity Analysis

| Approach | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| **Iterative 3-Pointer** | **$O(N)$** | **$O(1)$** |
| Recursive | $O(N)$ | $O(N)$ (Call stack) |

---

## Key Takeaways

1. **The 4 Steps:** Save next $\to$ Reverse link $\to$ Move prev $\to$ Move curr.
2. **Return pointer:** Return `prev` (new head), not `curr`.
3. **Space optimal:** Iterative runs in strict $O(1)$ auxiliary memory.

---

## ⚡ 2-Minute Revision

```cpp
ListNode *prev = nullptr, *curr = head;
while (curr) {
    ListNode *nxt = curr->next;
    curr->next = prev;
    prev = curr;
    curr = nxt;
}
return prev;
```
"""

print("Writing batch 1 linked list...")
for fn, content in notes.items():
    with open(os.path.join(t14_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 01, 02 in Topic 14.")
