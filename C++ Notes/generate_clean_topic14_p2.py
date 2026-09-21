import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t14_dir = os.path.join(root, "14_linked_list")

notes = {}

# 03: Middle of Linked List
notes["03_middle_of_a_linked_list.md"] = r"""# Lecture 59: Middle of a Linked List: Fast & Slow Pointers (LeetCode 876)

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
"""

# 04: Detect & Remove Cycle
notes["04_detect_and_remove_cycle.md"] = r"""# Lecture 60: Detect & Remove Cycle: Floyd's Algorithm & Proof (LeetCode 141 & 142)

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
"""

# 05: Merge Two Sorted Lists
notes["05_merge_two_sorted_lists.md"] = r"""# Lecture 61: Merge Two Sorted Lists: Dummy Node Pointer Rewiring (LeetCode 21)

> **One-Line Purpose:** Master the Sentinel / Dummy Node technique to merge two sorted linked lists in-place into a single sorted list with strict $O(N + M)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #61  
> **Video ID:** `f8RPIb-0DDE`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=f8RPIb-0DDE)  
> **Duration:** 12:41  
> **Transcript:** `.transcripts/14_linked_list/061_Merge_Two_Sorted_Lists___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 21: splicing two sorted lists into one sorted list.
- Why using a **Dummy Node (Sentinel Node)** eliminates all special-case branching for initializing the merged `head`.
- How to rewire pointers in-place without allocating new `ListNode` instances on the heap.
- Connecting the leftover tail when one list is exhausted first.

---

## 🔵 Lecture Context

Merging two sorted lists is the fundamental subroutine of Merge Sort on Linked Lists and LeetCode 23 (Merge K Sorted Lists).

---

## 1. Problem Statement

You are given the heads of two sorted linked lists `list1` and `list2`.
Merge the two lists into one sorted list by splicing together the nodes of the first two lists.
Return the head of the merged linked list.

```
list1: 1 -> 2 -> 4 -> NULL
list2: 1 -> 3 -> 4 -> NULL
Merged: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> NULL
```

---

## 2. The Golden Technique: Dummy Node (Sentinel Node)

Without a dummy node, you must write repetitive checks:
```cpp
if (head == nullptr) { head = ...; tail = ...; }
else { tail->next = ...; }
```
A **Dummy Node** allocated on the stack (`ListNode dummy(0)`) acts as a temporary anchor:
1. `tail` points initially to `&dummy`.
2. Compare `list1->val` and `list2->val`.
3. Point `tail->next` to the smaller node, advance that list pointer, and advance `tail`.
4. When one list runs out, attach the remainder of the other list directly: `tail->next = (list1 != nullptr) ? list1 : list2`.
5. Return `dummy.next`!

---

## 3. Complete C++ Implementation

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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // Sentinel dummy node on the stack (zero heap allocation!)
        ListNode dummy(0);
        ListNode* tail = &dummy;

        // Traverse both lists in parallel
        while (list1 != nullptr && list2 != nullptr) {
            if (list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }

        // Attach remaining nodes directly
        if (list1 != nullptr) {
            tail->next = list1;
        } else {
            tail->next = list2;
        }

        return dummy.next;
    }
};

int main() {
    ListNode* l1 = new ListNode(1);
    l1->next = new ListNode(2);
    l1->next->next = new ListNode(4);

    ListNode* l2 = new ListNode(1);
    l2->next = new ListNode(3);
    l2->next->next = new ListNode(4);

    Solution solver;
    ListNode* merged = solver.mergeTwoLists(l1, l2);

    cout << "Merged List: ";
    while (merged) {
        cout << merged->val << " -> ";
        merged = merged->next;
    }
    cout << "NULL\n";
    return 0;
}
```

- **Time Complexity:** $O(N + M)$ where $N$ and $M$ are list lengths.
- **Auxiliary Space Complexity:** $O(1)$ in-place rewiring.

---

## 🔍 Detailed Trace: Merging `[1, 3]` and `[2, 4]`

1. `dummy.next` initially points to `nullptr`, `tail = &dummy`.
2. $1 \le 2$: `tail->next = node(1)`, `l1` advances to 3, `tail` at 1.
3. $3 > 2$: `tail->next = node(2)`, `l2` advances to 4, `tail` at 2.
4. $3 \le 4$: `tail->next = node(3)`, `l1` reaches `nullptr`, `tail` at 3.
5. Loop exits. Attach remainder of `l2`: `tail->next = node(4)`.
6. Return `dummy.next` (Node 1). Result: `1 -> 2 -> 3 -> 4 -> NULL`.

---

## 🧠 Mental Model: Merging Highways

Think of two freeway on-ramps merging into one highway lane. A traffic flagger (`tail`) compares the front cars on both ramps, lets the one with the smaller number pass first, and waits for the next pair.

---

## ⚠️ Common Mistakes

1. **Allocating New Nodes:** Writing `tail->next = new ListNode(list1->val)`. This wastes heap memory and runs in $O(N + M)$ space. The problem requires in-place splicing of the *existing* nodes.
2. **Looping through the Remainder:** Using a while loop to copy remaining nodes. In linked lists, you don't need a loop—simply assign `tail->next = remainingList;` in $O(1)$!

---

## 🖥️ System-Specific Notes

- Allocating `ListNode dummy(0)` on the stack costs zero heap allocations and automatically deallocates when the function returns, leaving no memory leaks.

---

## 🟡 Additional Essential Context

To solve **Merge K Sorted Lists (LeetCode 23)**:
- Pairwise Divide and Conquer: Merge lists $(0, 1), (2, 3) \dots$ in $O(N \log K)$ time.
- Min-Heap Priority Queue: Maintain a min-heap of size $K$ containing the current heads of all $K$ lists.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Can this be solved recursively? What are the trade-offs?  
**A:** Yes:
```cpp
if (!l1) return l2;
if (!l2) return l1;
if (l1->val <= l2->val) { l1->next = mergeTwoLists(l1->next, l2); return l1; }
else { l2->next = mergeTwoLists(l1, l2->next); return l2; }
```
Trade-off: Consumes $O(N + M)$ call-stack memory, risking stack overflow for long lists. Iterative with a dummy node is strictly preferred.

---

### 🔥 Interview Questions

#### Q1: Why is Merge Sort preferred for Linked Lists over Quick Sort?
- **Short Answer:** Because merging two sorted linked lists takes $O(1)$ auxiliary space and $O(1)$ time to attach remainders.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// list1 = NULL, list2 = [0]
// Returns [0] (Immediate attachment of non-null remainder)
```

---

## Edge Cases

1. **One List Empty:** `list1 = NULL, list2 = [1, 2]` $\to$ Returns `list2`.
2. **Both Lists Empty:** Returns `nullptr`.

---

## Complexity Analysis

- **Time Complexity:** $O(N + M)$ (Visits each node once).
- **Auxiliary Space Complexity:** $O(1)$ (Pointer rewiring only).

---

## Key Takeaways

1. **Dummy Node:** Eliminates edge-case branching for empty heads.
2. **Single Link Attachment:** Attach entire remaining sublist in $O(1)$ time.
3. **In-place splicing:** Zero heap allocation.

---

## ⚡ 2-Minute Revision

- Stack dummy: `ListNode dummy(0); ListNode *tail = &dummy;`.
- While loop: rewire smaller node to `tail->next`.
- Remainder: `tail->next = l1 ? l1 : l2; return dummy.next;`.
"""

# 06: Copy List with Random Pointer
notes["06_copy_list_with_random_pointer.md"] = r"""# Lecture 62: Copy List with Random Pointer: In-Place Interleaving (LeetCode 138)

> **One-Line Purpose:** Master deep-copying complex linked structures with auxiliary random pointers, contrasting $O(N)$ Hash Map lookup with the optimal $O(1)$ auxiliary space node interleaving technique.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #62  
> **Video ID:** `8ze7Zopdsaw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=8ze7Zopdsaw)  
> **Duration:** 20:52  
> **Transcript:** `.transcripts/14_linked_list/062_Copy_List_with_Random_Pointer___DSA_Series_by__shradhaKD.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The distinction between a **Shallow Copy** (copying pointer addresses) and a **Deep Copy** (allocating entirely new independent nodes).
- Why copying nodes with random pointers is non-trivial: a node's `random` pointer may point to a future node that has not been created yet.
- **Approach 1 (Hash Map Lookup):** $O(N)$ Time, $O(N)$ Space.
- **Approach 2 (In-Place Node Interleaving):** $O(N)$ Time, **$O(1)$ Auxiliary Space**.
- The 3 distinct passes of the in-place interleaving algorithm: Duplicate, Wire Randoms, and Decouple.

---

## 🔵 Lecture Context

Copy List with Random Pointer (LeetCode 138) is a premier FAANG interview problem testing deep copy mechanics, graph cloning, and space optimization.

---

## 1. Problem Statement & Node Anatomy

A linked list of length $N$ is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.
Construct a **deep copy** of the list.

```cpp
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = nullptr;
        random = nullptr;
    }
};
```

---

## 2. Approach 1: Hash Map Mapping ($O(N)$ Space)

Use a hash table `unordered_map<Node*, Node*> cloneMap` to store the mapping from `originalNode -> clonedNode`.
1. **Pass 1:** Create cloned nodes for every original node: `cloneMap[curr] = new Node(curr->val)`.
2. **Pass 2:** Wire the pointers of the clones:
   - `cloneMap[curr]->next = cloneMap[curr->next];`
   - `cloneMap[curr]->random = cloneMap[curr->random];`
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(N)$ extra hash table memory.

---

## 3. Approach 2: In-Place Interleaving ($O(1)$ Auxiliary Space)

We can eliminate the hash map by weaving the cloned nodes directly into the original list!

### Step 1: Interleave Cloned Nodes
For each original node `curr`, create `copy = new Node(curr->val)`. Insert `copy` directly between `curr` and `curr->next`:
```
Original:    A -------------> B -------------> C
Interleaved: A ----> A' ----> B ----> B' ----> C ----> C'
```

### Step 2: Wire Random Pointers for Clones
Because each clone `A'` sits immediately after its original `A`:
$$\text{copy->random} = \text{curr->random ? curr->random->next : nullptr}$$

### Step 3: Decouple the Two Lists
Separate the interleaved list back into the original list and the cloned list:
- `curr->next = copy->next;`
- `copy->next = copy->next ? copy->next->next : nullptr;`

---

## 4. Complete C++ Implementation ($O(1)$ Space)

```cpp
#include <iostream>
using namespace std;

class Node {
public:
    int val;
    Node* next;
    Node* random;
    Node(int _val) : val(_val), next(nullptr), random(nullptr) {}
};

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (head == nullptr) return nullptr;

        // Step 1: Create interleaved duplicate nodes
        Node* curr = head;
        while (curr != nullptr) {
            Node* copy = new Node(curr->val);
            copy->next = curr->next;
            curr->next = copy;
            curr = copy->next;
        }

        // Step 2: Wire random pointers for copies
        curr = head;
        while (curr != nullptr) {
            if (curr->random != nullptr) {
                curr->next->random = curr->random->next;
            }
            curr = curr->next->next;
        }

        // Step 3: Decouple original and cloned lists
        Node* cloneHead = head->next;
        curr = head;
        while (curr != nullptr) {
            Node* copy = curr->next;
            curr->next = copy->next;
            if (copy->next != nullptr) {
                copy->next = copy->next->next;
            }
            curr = curr->next;
        }

        return cloneHead;
    }
};
```

---

## 🔍 Detailed Trace: Interleaving on `A -> B -> NULL`

Let `A->random = B`, `B->random = A`.

### After Step 1 (Interleave):
`A -> A' -> B -> B' -> NULL`

### After Step 2 (Wire Randoms):
`A'->random = A->random->next` (which is `B'`). Correct!
`B'->random = B->random->next` (which is `A'`). Correct!

### After Step 3 (Decouple):
Original restored: `A -> B -> NULL`
Cloned produced: `A' -> B' -> NULL` with `A'->random = B'`, `B'->random = A'`.

---

## 🧠 Mental Model: Shadow Cloning

Think of each node creating a shadow twin that stands immediately to its right. Since each twin stands right behind its creator, finding the twin of any creator's friend is trivial: just look right behind the friend (`creator->random->next`)!

---

## ⚠️ Common Mistakes

1. **Mutating the Original List Permanently:** Failing to restore `curr->next = copy->next`. LeetCode verifies that the original input list is left intact!
2. **Null Dereference on Random:** Writing `curr->next->random = curr->random->next` without checking `curr->random != nullptr`.

---

## 🖥️ System-Specific Notes

- Hash maps (`unordered_map<Node*, Node*>`) have rehashing overhead and high constant factors. The 3-pass pointer interleaving runs over $2\times$ faster in benchmark CPU cycles.

---

## 🟡 Additional Essential Context

This interleaving pattern is fundamentally identical to cloning arbitrary directed graphs (LeetCode 133: Clone Graph), where vertex copies are mapped via lookup or inline tagging.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why can we not wire `next` and `random` pointers in a single pass?  
**A:** Because a node's `random` pointer can point to a node located far ahead in the list that has not been created yet!

---

### 🔥 Interview Questions

#### Q1: What are the space complexities of Approach 1 vs Approach 2?
- **Short Answer:** Approach 1 requires $O(N)$ auxiliary space for the hash map; Approach 2 requires $O(1)$ auxiliary space.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// Input: head = NULL
// Output: NULL (Handled by if (!head) return nullptr;)
```

---

## Edge Cases

1. **List of Length 1:** `A->random = A` (Points to itself). Handled correctly (`A'->random = A'`).
2. **All Random Pointers Null:** Valid deep copy with all `random == nullptr`.

---

## Complexity Analysis

| Approach | Time Complexity | Auxiliary Space Complexity |
|---|---|---|
| Hash Map Lookup | $O(N)$ | $O(N)$ |
| **In-Place Interleaving** | **$O(N)$** | **$O(1)$** |

---

## Key Takeaways

1. **3 Passes:** Duplicate in-place $\to$ Assign randoms $\to$ Unlink copies.
2. **Random mapping formula:** `curr->next->random = curr->random->next`.
3. **Restore original list:** Must leave input list completely intact.

---

## ⚡ 2-Minute Revision

- Pass 1: `copy->next = curr->next; curr->next = copy;`.
- Pass 2: `if (curr->random) curr->next->random = curr->random->next;`.
- Pass 3: Decouple lists.
- Space: $O(1)$.
"""

print("Writing batch 2 linked list...")
for fn, content in notes.items():
    with open(os.path.join(t14_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 03, 04, 05, 06 in Topic 14.")
