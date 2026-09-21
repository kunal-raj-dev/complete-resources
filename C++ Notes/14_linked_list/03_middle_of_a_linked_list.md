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


## 🧠 Core Intuition — Why This Works
To find the middle of a linked list, a naive approach requires traversing the list completely to count the nodes ($N$), and then traversing again to $N/2$. The elegant optimization is the **Tortoise and Hare (Slow and Fast Pointers)** technique. If a fast pointer moves twice as fast as a slow pointer, when the fast pointer reaches the end, the slow pointer will be exactly halfway through the list!

## 🎯 Pattern Recognition — When to Use This
- **"Find the middle of a sequence"**: Directly points to Slow and Fast pointers.
- **"Find the $k$-th node from the end"**: Use two pointers separated by $k$ nodes. Move both until the lead pointer hits the end.
- **Preparing for Merge Sort / Palindrome checks**: These algorithms explicitly require breaking a linked list into two halves.

## 🔍 Dry Run Trace
**Example:** `1 -> 2 -> 3 -> 4 -> 5 -> NULL`
- **Initial:** `slow` at `1`, `fast` at `1`.
- **Step 1:** `slow` to `2`, `fast` to `3`.
- **Step 2:** `slow` to `3`, `fast` to `5`.
- **Step 3:** `fast->next` is `NULL`, loop terminates. `slow` is at `3` (the middle).

**Example (Even length):** `1 -> 2 -> 3 -> 4 -> 5 -> 6 -> NULL`
- **Initial:** `slow` at `1`, `fast` at `1`.
- **Step 1:** `slow` to `2`, `fast` to `3`.
- **Step 2:** `slow` to `3`, `fast` to `5`.
- **Step 3:** `slow` to `4`, `fast` to `NULL`.
- Loop terminates. `slow` is at `4` (second middle, which is standard for even lists).

## ⚠️ Common Interview Mistakes
1. **Loop condition errors:** Using `while (fast != NULL)` without checking `fast->next != NULL`. If `fast` is at the last node, `fast->next` is `NULL`, and evaluating `fast->next->next` will cause a Segmentation Fault. The correct condition is `while (fast != NULL && fast->next != NULL)`.
2. **First middle vs. Second middle:** By default, initializing `slow = head` and `fast = head` gives the **second middle** for even-length lists (e.g., node 4 for `1..6`). If you specifically need the **first middle** (node 3) (useful when breaking the list exactly in half for Merge Sort), initialize `fast = head->next`.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ because the fast pointer traverses the list once. Actually, it visits $N/2$ nodes doing 2 steps at a time.
- **Space Complexity:** $O(1)$ auxiliary space.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can we use this approach to find the $K$-th element from the middle?
**Answer:** No. Finding the $K$-th element requires knowing the length. You can find the $K$-th from the *end* using two pointers spaced $K$ apart, but finding something relative to the middle still fundamentally requires finding the middle first, which dictates $O(N)$ time.

### Q2: How does this help in sorting a Linked List?
**Answer:** Merge Sort on linked lists requires dividing the list into two halves recursively. The slow and fast pointer approach is the standard $O(1)$ space method to find the midpoint to split the list, allowing $O(N \log N)$ sorting without allocating array copies.

## 🏆 Related Problems
- **[234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)**: Uses the middle node to reverse the second half.
- **[148. Sort List](https://leetcode.com/problems/sort-list/)**: Uses the middle node to perform Merge Sort.
- **[19. Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)**: A variation of the dual-pointer technique.

## 🔗 Cross-Topic Connections
- **Merge Sort:** The divide step requires finding the middle.
- **Two Pointers:** The core mechanism (Tortoise and Hare).

## ⚡ 2-Minute Revision Flash Card
- **Core Logic:** `slow = head`, `fast = head`. `while (fast != NULL && fast->next != NULL) { slow = slow->next; fast = fast->next->next; }`
- **Result:** `slow` will be the middle. For even lists, it's the second middle.
- **For First Middle:** Use `fast = head->next`.
- **Trap:** Beware of `fast->next->next` dereferencing a `NULL` pointer!
