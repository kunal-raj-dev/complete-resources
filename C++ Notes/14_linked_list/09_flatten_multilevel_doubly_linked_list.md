# Lecture 65: Flatten a Multilevel Doubly Linked List: DFS Splice (LeetCode 430)

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
