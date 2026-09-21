# Lecture 59: Middle of a Linked List: Fast & Slow Pointers (LeetCode 876)

> **One-Line Purpose:** Master the Tortoise & Hare (Slow-Fast Pointer) pattern to locate the midpoint of a singly linked list in a single pass with strict $O(N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #59  
> **Video ID:** `nzaHG0dme4g`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=nzaHG0dme4g)  
> **Duration:** 10:32  
> **Transcript:** `.transcripts/14_linked_list/059_Middle_of_a_Linked_List___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 876: returning the middle node of a singly linked list.
- The distinction between **Approach 1 (Two-Pass Count Method)** and **Approach 2 (One-Pass Tortoise & Hare)**.
- The 2x speed differential invariant: since `fast` travels at twice the speed of `slow`, when `fast` reaches the end of the track, `slow` is precisely at the midpoint.
- The termination condition handling both Odd-length lists (`fast->next == nullptr`) and Even-length lists (`fast == nullptr`).

---

## 🔵 Lecture Context

The Tortoise and Hare two-pointer pattern is one of the most vital paradigms in linked-list algorithms. It is reused in Floyd's Cycle Detection (Lecture 60), Palindrome Linked List, and Merge Sort on Linked Lists (Lecture 51).

---

## 1. Problem Statement

Given the `head` of a singly linked list, return the middle node of the linked list.
- If there are two middle nodes (even length), return the **second middle node**.

```
Odd length:  1 -> 2 -> 3 -> 4 -> 5 -> NULL      ==> Middle is 3
Even length: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> NULL ==> Middle is 4 (Second middle)
```

---

## 2. Approach 1: Two-Pass Count Method

1. **Pass 1:** Traverse the list to count total nodes $N$.
2. **Pass 2:** Traverse to index $\lfloor N / 2 \rfloor$ and return that node.
- **Time Complexity:** $O(N) + O(N/2) = O(N)$ time.
- **Limitation:** Requires traversing the list twice.

---

## 3. Approach 2: One-Pass Fast & Slow Pointers (Optimal)

Initialize two pointers at `head`:
- `slow`: Advances **1 step** per iteration (`slow = slow->next`).
- `fast`: Advances **2 steps** per iteration (`fast = fast->next->next`).

### Mathematical Invariant:
$$\text{Distance}(\text{fast}) = 2 \times \text{Distance}(\text{slow})$$
When `fast` reaches the end of the list ($N$ steps), `slow` has covered exactly $N/2$ steps, positioning it right at the middle!

### Loop Termination Condition:
`while (fast != nullptr && fast->next != nullptr)`
- If length is **Even**: `fast` becomes `nullptr`.
- If length is **Odd**: `fast->next` becomes `nullptr`.

---

## 4. Complete C++ Implementation

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
    ListNode* middleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;

        // Traverse until fast reaches the end
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;       // 1 step
            fast = fast->next->next; // 2 steps
        }

        return slow; // Points to the middle node
    }
};

int main() {
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);

    Solution solver;
    ListNode* mid = solver.middleNode(head);
    cout << "Middle value: " << mid->val << "\n"; // Output: 3
    return 0;
}
```

- **Time Complexity:** $O(N)$ (Single pass).
- **Auxiliary Space Complexity:** $O(1)$ (Two pointers).

---

## 🔍 Detailed Trace

### Case 1: Odd Length `[1, 2, 3, 4, 5]`
- Init: `slow` at 1, `fast` at 1.
- Step 1: `slow` at 2, `fast` at 3.
- Step 2: `slow` at 3, `fast` at 5.
- Next check: `fast->next == nullptr` $\to$ Loop terminates!
- Return `slow` (Node 3). Correct!

### Case 2: Even Length `[1, 2, 3, 4, 5, 6]`
- Init: `slow` at 1, `fast` at 1.
- Step 1: `slow` at 2, `fast` at 3.
- Step 2: `slow` at 3, `fast` at 5.
- Step 3: `slow` at 4, `fast` at `nullptr`.
- Next check: `fast == nullptr` $\to$ Loop terminates!
- Return `slow` (Node 4: Second middle). Correct!

---

## 🧠 Mental Model: Runners on a Track

Imagine a race between a tortoise running at 1 m/s and a hare running at 2 m/s. When the hare crosses the finish line, the tortoise is exactly halfway through the race course.

---

## ⚠️ Common Mistakes

1. **Reversing Condition Order:** Writing `while (fast->next != nullptr && fast != nullptr)`. If `fast` is `nullptr`, evaluating `fast->next` *first* triggers a segmentation fault! Always check `fast != nullptr` first (short-circuit safety).
2. **First Middle vs Second Middle:** In Merge Sort on Linked Lists, you need the **first middle** for even lengths (to split into equal halves `[1, 2, 3]` and `[4, 5, 6]`). For first middle, initialize `fast = head->next`.

---

## 🖥️ System-Specific Notes

- Single pass operations improve L1/L2 cache prefetching because the hardware prefetcher only streams memory forward once without reloading from RAM in a second pass.

---

## 🟡 Additional Essential Context

To obtain the **First Middle** for even lengths:
```cpp
ListNode* slow = head;
ListNode* fast = head->next;
while (fast != nullptr && fast->next != nullptr) {
    slow = slow->next;
    fast = fast->next->next;
}
// For [1, 2, 3, 4], slow returns 2 (first middle)
```

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why is fast and slow pointers considered optimal if both Approach 1 and Approach 2 have $O(N)$ time complexity?  
**A:** In computer architecture, performing $\approx N/2$ pointer reads in a single pass has roughly half the cache misses and instructions of performing $1.5 N$ pointer reads across two passes.

---

### 🔥 Interview Questions

#### Q1: How would you delete the middle node in a single pass (LeetCode 2095)?
- **Short Answer:** Maintain a `prev` pointer trailing one step behind `slow`. When `fast` reaches the end, rewire `prev->next = slow->next` and delete `slow`.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// List: 10 -> NULL
// fast at 10, fast->next is NULL -> Loop does not run.
// Returns slow (10). Correct!
```

---

## Edge Cases

1. **Single Node (`head->next == nullptr`):** Returns `head` immediately.
2. **Two Nodes (`1 -> 2 -> NULL`):** Returns node 2 (second middle).

---

## Complexity Analysis

- **Time Complexity:** $O(N)$ (Takes $\lceil N/2 \rceil$ iterations).
- **Auxiliary Space Complexity:** $O(1)$ (Only two pointer variables).

---

## Key Takeaways

1. **Speed ratio:** Fast moves 2 steps; slow moves 1 step.
2. **Termination:** `fast != nullptr && fast->next != nullptr`.
3. **Single pass efficiency:** Halves the work of the two-pass approach.

---

## ⚡ 2-Minute Revision

```cpp
ListNode *slow = head, *fast = head;
while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
}
return slow;
```
