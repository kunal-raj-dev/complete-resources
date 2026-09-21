# Lecture 61: Merge Two Sorted Lists: Dummy Node Pointer Rewiring (LeetCode 21)

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
