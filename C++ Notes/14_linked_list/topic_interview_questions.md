# Topic 14 Interview Questions: Linked List

> **Curated Question Bank:** FAANG interview questions, Floyd's Cycle mathematical proof, and in-place node splicing edge cases.

---

## 📌 Conceptual & Mathematical Questions

### Q1: [Mathematical Proof] Why does Floyd's Cycle Detection Algorithm guarantee that moving one pointer to `head` and advancing both at equal speed meets at the cycle starting node?
- **Proof:**
  - Let $L_1$ be the distance from `head` to the cycle starting node.
  - Let $L_2$ be the distance from the cycle starting node to the meeting point.
  - Let $C$ be the total perimeter of the cycle.
  - Total distance traveled by `slow`: $D_{\text{slow}} = L_1 + L_2$.
  - Total distance traveled by `fast`: $D_{\text{fast}} = L_1 + L_2 + nC$ (where $n \ge 1$ is the number of loops completed by `fast`).
  - Since `fast` moves twice as fast as `slow`:
    $$2 \times D_{\text{slow}} = D_{\text{fast}}$$
    $$2(L_1 + L_2) = L_1 + L_2 + nC$$
    $$L_1 + L_2 = nC \implies \mathbf{L_1 = nC - L_2}$$
  - This proves that the distance from `head` to the cycle start ($L_1$) is exactly equal to moving forward from the meeting point to the cycle start ($nC - L_2$).
  - Therefore, advancing one pointer from `head` and one from the meeting point at 1 step per cycle causes them to collide precisely at the cycle start node!

---

### Q2: [LeetCode 138] How do you clone a Linked List with Random Pointers in $O(1)$ auxiliary space without using a Hash Map?
- **Short Answer:** The **3-Pass In-Place Interleaving** algorithm:
  1. **Pass 1 (Interleaving):** Create a duplicate copy of each node and insert it immediately after the original node: `A -> A' -> B -> B' -> C -> C'`.
  2. **Pass 2 (Assign Random Pointers):** For each original node `curr`, set `curr->next->random = curr->random ? curr->random->next : nullptr`.
  3. **Pass 3 (Decouple Lists):** Restore the original list and extract the cloned list by separating alternating pointers.
- **Complexity:** $O(N)$ Time, $O(1)$ Auxiliary Space.

---

### Q3: Why does `delete` must be called on every dynamically allocated node in C++ when destroying a Linked List?
- **Short Answer:** Because C++ lacks an automated garbage collector.
- **Detailed Explanation:** Nodes created with `new Node(val)` reside on the Heap. Merely setting `head = nullptr` removes the pointer to the first node, leaving all node blocks orphaned on the Heap and causing a catastrophic **Memory Leak**.
- **Destructor Implementation:**
  ```cpp
  ~LinkedList() {
      Node* curr = head;
      while (curr) {
          Node* nextNode = curr->next;
          delete curr;
          curr = nextNode;
      }
      head = tail = nullptr;
  }
  ```
