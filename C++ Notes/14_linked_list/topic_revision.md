# Topic 14 Revision: Linked List

> **High-Density Revision Guide:** Core patterns, pointer rewiring blueprints, cycle proofs, and memory models.

---

## 1. Array vs Linked List Comparison
- **Memory Layout:** Arrays are contiguous; Linked Lists are non-contiguous heap nodes connected by pointers.
- **Random Access:** Array $O(1)$; Linked List $O(N)$ (requires traversal from `head`).
- **Insertion at Head:** Array $O(N)$ (shifting required); Linked List $O(1)$ (direct pointer update).
- **Cache Locality:** Array has near-perfect spatial locality; Linked List suffers from frequent CPU cache misses.

---

## 2. Core Pointer Patterns

### A. Reverse a Linked List (Iterative 3-Pointers)
```cpp
ListNode* prev = nullptr;
ListNode* curr = head;
while (curr) {
    ListNode* nextNode = curr->next;
    curr->next = prev;
    prev = curr;
    curr = nextNode;
}
return prev;
```

### B. Slow & Fast Pointers (Tortoise & Hare)
- **Middle of List:** `slow` advances 1 step, `fast` advances 2 steps. When `fast` reaches the end, `slow` is at the middle.
- **Cycle Detection (Floyd's Algorithm):** If a cycle exists, `fast` and `slow` will meet inside the loop in $O(N)$ time.
- **Cycle Entry Point:** Move `slow` to `head`. Advance both `slow` and `fast` by 1 step simultaneously. They meet at the **cycle entry node**.

### C. Dummy Head Technique
Allocates a sentinel node (`ListNode dummy(0);`) on the stack. Eliminates special-case branching when modifying or inserting at the head of the list.

### D. LRU Cache Design
- **Data Structure:** Doubly Linked List (maintains access recency in $O(1)$) + Hash Map (`unordered_map<int, Node*>` for $O(1)$ key-to-node lookup).
- **Operations:** Both `get(key)` and `put(key, value)` execute in strict $O(1)$ time.
