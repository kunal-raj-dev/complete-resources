# Lecture 60: Detect & Remove Cycle: Floyd's Algorithm & Proof (LeetCode 141 & 142)

> **One-Line Purpose:** Master Floyd's Cycle-Finding Algorithm (Tortoise & Hare), mathematically prove the Cycle Origin entry point, and break loops in-place to prevent infinite traversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #60  
> **Video ID:** `-1E8ZMS0gSs`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-1E8ZMS0gSs)  
> **Duration:** 30:24  
> **Transcript:** `.transcripts/14_linked_list/060_Detect___Remove_Cycle_in_Linked_List___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What a cycle in a linked list is and why it causes infinite loops during standard traversal.
- **Part 1 (LeetCode 141):** How to detect if a cycle exists in $O(N)$ time and $O(1)$ space using Floyd's Algorithm.
- **Part 2 (LeetCode 142):** The rigorous mathematical proof explaining why resetting `slow = head` and moving both pointers at equal speed finds the exact cycle entry node.
- **Part 3:** How to safely break the cycle by updating the last node's `next` pointer to `nullptr`.

---

## 🔵 Lecture Context

Floyd's Cycle-Finding Algorithm is a Tier-1 interview question. It appears not only in linked lists, but also in array problems with duplicate values (e.g. Find the Duplicate Number, LeetCode 287) and Brent's algorithm in cryptography.

---

## 1. Problem 1: Cycle Detection (LeetCode 141)

Given the `head` of a linked list, determine if the list has a cycle in it.

### Core Idea:
Initialize `slow = head` and `fast = head`.
- `slow` moves 1 step; `fast` moves 2 steps.
- If there is NO cycle: `fast` or `fast->next` will reach `nullptr`.
- If there IS a cycle: `fast` enters the loop and continuously reduces the gap between itself and `slow` by 1 node per iteration until `slow == fast`!

```cpp
bool hasCycle(ListNode *head) {
    ListNode *slow = head;
    ListNode *fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            return true; // Cycle detected!
        }
    }

    return false; // Reached end -> No cycle
}
```

---

## 2. Problem 2: Find Cycle Origin (LeetCode 142) & Mathematical Proof

When `slow == fast`, they meet somewhere inside the cycle. Where is the cycle starting node?

### 📐 The Mathematical Proof:
```
       L1 (Distance to cycle start)          d (Meeting offset)
head ----------------------------> [Entry] -------------> [Meeting Point]
                                      ^                        |
                                      |                        |
                                      +------------------------+
                                            C - d (Remaining)
```
Let:
- $L_1$: Distance from `head` to the cycle Entry node.
- $C$: Total length of the cycle.
- $d$: Distance from Entry node to the Meeting point.

When `slow` and `fast` meet:
- Distance traveled by `slow`: $D_{\text{slow}} = L_1 + d$.
- Distance traveled by `fast`: $D_{\text{fast}} = L_1 + k \cdot C + d$ (where $k \ge 1$ is the number of full cycle loops).

Since `fast` travels at twice the speed of `slow`:
$$D_{\text{fast}} = 2 \times D_{\text{slow}}$$
$$L_1 + k \cdot C + d = 2(L_1 + d)$$
$$L_1 + k \cdot C + d = 2L_1 + 2d$$
$$L_1 = k \cdot C - d$$
$$L_1 = (k - 1) \cdot C + (C - d)$$

### 💡 The Golden Deduction:
The distance from `head` to the Entry node ($L_1$) is mathematically identical to the distance from the Meeting point to the Entry node ($(C - d)$) plus $(k-1)$ full loops!
Therefore:
1. Reset `slow = head`.
2. Keep `fast` at the meeting point.
3. Advance both pointers **1 step at a time**.
4. The exact node where they collide is the **Cycle Entry Node**!

---

## 3. Complete C++ Implementation: Detect, Find Entry & Remove Cycle

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
    // LeetCode 142: Find Starting Node of Cycle
    ListNode *detectCycle(ListNode *head) {
        ListNode *slow = head;
        ListNode *fast = head;
        bool hasCycle = false;

        // Step 1: Detect meeting point
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle) return nullptr;

        // Step 2: Find entry node using mathematical invariant
        slow = head;
        while (slow != fast) {
            slow = slow->next;
            fast = fast->next;
        }

        return slow; // Cycle entry node
    }

    // Remove Cycle completely
    void removeCycle(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        bool hasCycle = false;

        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle) return;

        slow = head;
        // Special case: Cycle starts at head itself!
        if (slow == fast) {
            while (fast->next != slow) {
                fast = fast->next;
            }
            fast->next = nullptr; // Break loop
            return;
        }

        // Standard case: Advance until their next pointers meet at entry
        while (slow->next != fast->next) {
            slow = slow->next;
            fast = fast->next;
        }

        // fast->next is the entry; fast is the last node of the cycle!
        fast->next = nullptr; // Break cycle
    }
};
```

---

## 🧠 Mental Model: Circular Track

Think of two cars on a circular race track. If Car A goes at 100 km/h and Car B goes at 200 km/h, Car B is closing the distance on Car A by 100 km/h on every loop. Because the relative speed is 1, Car B cannot "jump over" Car A without meeting at the exact same discrete point.

---

## ⚠️ Common Mistakes

1. **Cycle at Head Bug:** If the entire list is a circular loop (`fast == slow == head`), running `while (slow != fast)` immediately terminates without finding the end! Always handle `slow == fast == head` separately when breaking cycles.
2. **Using Hash Sets:** Using `unordered_set<ListNode*>` solves the problem in $O(N)$ time, but consumes $O(N)$ extra space, failing the $O(1)$ memory interview requirement.

---

## 🖥️ System-Specific Notes

- Floyd's cycle detection handles arbitrarily long linked lists up to $10^9$ nodes within microseconds because relative distance decreases by 1 on each step.

---

## 🟡 Additional Essential Context

Floyd's algorithm solves **LeetCode 287 (Find the Duplicate Number)**:
An array of $n+1$ integers where each integer is in range $[1, n]$ can be interpreted as a linked list where `nums[i]` points to `nums[nums[i]]`. The duplicate number is the cycle entry!

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can `fast` never "hop over" `slow` without colliding?  
**A:** Because in each iteration, `fast` takes 2 steps and `slow` takes 1 step. In the reference frame of `slow`, `fast` is moving at a relative velocity of $2 - 1 = 1$ step per turn. A pointer moving at relative speed $1$ cannot skip any integer position on a discrete grid.

---

### 🔥 Interview Questions

#### Q1: What is the maximum number of iterations `fast` takes to catch `slow` once both are in the cycle?
- **Short Answer:** At most $C$ iterations, where $C$ is the length of the cycle.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// List: 1 -> 2 -> 3 -> 2 (cycle back to 2)
// Entry node value returned: 2
```

---

## Edge Cases

1. **No Cycle:** `fast` hits `nullptr`, returns `nullptr`.
2. **Cycle of Length 1 (Self Loop):** Node points to itself (`node->next = node`). Handled correctly.

---

## Complexity Analysis

- **Time Complexity:** $O(N)$ (Detection takes $\le 2N$ steps; finding entry takes $L_1 \le N$ steps).
- **Auxiliary Space Complexity:** $O(1)$ (Only pointer references).

---

## Key Takeaways

1. **Floyd's Invariant:** $L_1 = (k-1)C + (C - d)$.
2. **Reset to Head:** Move `slow = head` and `fast` by 1 step to locate the cycle entrance.
3. **Break Cycle:** Set the last node's `next = nullptr`.

---

## ⚡ 2-Minute Revision

- Detect: `slow = slow->next; fast = fast->next->next; if (slow == fast) cycle!`.
- Find Entry: `slow = head; while (slow != fast) { slow = slow->next; fast = fast->next; } return slow;`.
- Space: $O(1)$.
