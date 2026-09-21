# Lecture 58: Reverse a Linked List: Iterative & Recursive (LeetCode 206)

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
