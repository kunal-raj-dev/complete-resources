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
- **Short Answer:** Because merging two sorted linked lists takes $O(1)$ auxiliary space (pointer rewiring) and $O(1)$ time to attach remainders.
- **Detailed:** QuickSort needs $O(1)$ random-access pivoting which requires $O(N)$ traversal on linked lists for each partition. MergeSort's divide step is trivial (find middle with slow/fast pointers) and the merge step is pure pointer manipulation.

---

#### Q2: [Extension] How would you merge K sorted linked lists? (LeetCode 23)
- **Answer — Min-Heap Approach $O(N \log K)$:**
  1. Build a min-heap of size $K$ containing the heads of all $K$ lists.
  2. Pop the minimum node, add it to the result, and push its `.next` into the heap.
  3. Repeat until the heap is empty.
  - **Why $O(N \log K)$:** Each of the $N$ total nodes is pushed/popped once; each heap operation is $O(\log K)$.
  ```cpp
  // Min-heap using priority queue
  auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
  priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
  for (auto* head : lists) if (head) pq.push(head);
  ListNode dummy(0); ListNode* tail = &dummy;
  while (!pq.empty()) {
      tail->next = pq.top(); pq.pop();
      tail = tail->next;
      if (tail->next) pq.push(tail->next);
  }
  return dummy.next;
  ```
- **Divide-and-Conquer Alternative $O(N \log K)$:** Pairwise merge lists $(0,1), (2,3), \ldots$ in $\log K$ rounds.

---

#### Q3: [Conceptual] What is the difference between in-place merge and extra-space merge for linked lists?
- **Answer:**
  - **In-place (pointer rewiring):** The existing nodes are spliced into a new order by updating `next` pointers. $O(1)$ extra space. The original two lists are destroyed — their nodes are now part of the merged list.
  - **Extra-space (new node allocation):** `new ListNode(val)` is called for each element. The original lists are preserved. $O(N+M)$ extra space — wasteful and not what interviewers expect.
  - **Rule:** In interviews, ALWAYS splice existing nodes unless explicitly asked to preserve inputs.

---

#### Q4: [Debugging] What is wrong with this implementation?
```cpp
ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
    ListNode* head = nullptr;
    ListNode* tail = nullptr;
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            if (!head) head = tail = l1;  // Only sets head/tail on first node
            else tail->next = l1;         // BUG: forgets to advance tail
            l1 = l1->next;
        } else {
            if (!head) head = tail = l2;
            else tail->next = l2;
            l2 = l2->next;
        }
    }
    tail->next = l1 ? l1 : l2;
    return head;
}
```
- **Answer:** The bug is `tail` is never advanced after `tail->next = l1`. Every iteration overwrites `tail->next` with the next node but `tail` stays at the first node. The result is only a 2-node list (first + last remainder). Fix: add `tail = tail->next;` after each assignment. The dummy node technique completely avoids this class of bug.

---

#### Q5: [Conceptual] Is the dummy-node merge algorithm stable?
- **Answer:** Yes. The condition `list1->val <= list2->val` (using `<=` not `<`) ensures that when two nodes have equal values, the one from `list1` (the "left" list) is appended first. This preserves the relative ordering of equal elements across both lists — the definition of stability.

---

#### Q6: [System Design] If you had to merge 2 sorted lists in a memory-constrained embedded system with no heap allocation allowed, how would you proceed?
- **Answer:** Reuse the existing nodes via in-place pointer rewiring (exactly what the dummy-node approach does). Zero `new` calls are made — nodes from `list1` and `list2` are directly spliced into the merged result. The `ListNode dummy(0)` sentinel is allocated on the **stack**, not the heap. This is exactly $O(1)$ heap memory consumption, making it safe for embedded contexts.



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


## 🧠 Core Intuition — Why This Works
Merging two sorted linked lists is identical to the merge step in Merge Sort. Since both lists are already sorted, we only need to compare their head nodes. The smaller head becomes the next node in our merged list. We can build the merged list efficiently in $O(1)$ extra space by rewiring the `next` pointers, using a "dummy" head node to simplify the edge cases of inserting the very first node.

## 🎯 Pattern Recognition — When to Use This
- **"Merge two sorted structures"**: The classic two-pointer approach comparing current elements.
- **"Dummy Head Node"**: Used universally in linked list problems where the head of the return list is computed dynamically. It avoids messy `if (head == NULL)` initialization logic.

## 🔍 Dry Run Trace
**Example:** `L1 = 1 -> 3 -> 5`, `L2 = 2 -> 4 -> 6`
- **Setup:** `dummy = -1`, `curr = dummy`.
- **Step 1:** Compare `L1 (1)` and `L2 (2)`. `L1 < L2`. 
  - `curr->next = L1` (1). `curr = 1`. `L1` advances to `3`.
- **Step 2:** Compare `L1 (3)` and `L2 (2)`. `L2 < L1`.
  - `curr->next = L2` (2). `curr = 2`. `L2` advances to `4`.
- **Step 3:** Compare `L1 (3)` and `L2 (4)`. `L1 < L2`.
  - `curr->next = L1` (3). `curr = 3`. `L1` advances to `5`.
- **Fast Forward:** Both lists empty. If one was longer, say `L1` remained, just do `curr->next = L1` at the end to attach the remaining sorted tail instantly!

## ⚠️ Common Interview Mistakes
1. **Forgetting to attach the remainder:** A common mistake is terminating the loop when one list is empty and forgetting to link the rest of the other list. It's a simple `if (l1) curr->next = l1; else curr->next = l2;`.
2. **Memory Leak with Dummy Node:** If using `ListNode* dummy = new ListNode(-1);`, remember to save `dummy->next` to a result pointer, and then `delete dummy;` before returning, to prevent memory leaks in C++. Alternatively, stack allocate it: `ListNode dummy(-1); return dummy.next;`.
3. **Overcomplicating the Head Logic:** Trying to manually determine which node is the true head without a dummy node makes the code 2x longer and prone to edge-case bugs (like if `L1` is empty).

## 📊 Complexity Analysis
- **Time Complexity:** $O(N + M)$ where $N$ and $M$ are the lengths of the two lists. Each node is visited exactly once.
- **Space Complexity:** $O(1)$ auxiliary space since we are just rewiring existing nodes, not creating new ones. The recursive approach takes $O(N + M)$ space on the call stack.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can this be done recursively? What are the tradeoffs?
**Answer:** Yes. The recursive function is elegant: 
```cpp
if(!l1) return l2; if(!l2) return l1;
if(l1->val < l2->val) { l1->next = merge(l1->next, l2); return l1; }
else { l2->next = merge(l1, l2->next); return l2; }
```
However, the iterative approach is superior in production because it is $O(1)$ space. The recursive version takes $O(N+M)$ space on the call stack and will cause a Stack Overflow for very long lists (e.g., $10^5$ nodes).

### Q2: How does this generalize to merging $K$ sorted lists?
**Answer:** To merge $K$ sorted lists, comparing heads one by one takes $O(N \cdot K)$. The optimal approach uses a **Min-Heap (Priority Queue)** to store the heads of the $K$ lists, reducing the time complexity to $O(N \log K)$.

## 🏆 Related Problems
- **[23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)**: The follow-up question. Uses a Min-Heap or Divide & Conquer.
- **[148. Sort List](https://leetcode.com/problems/sort-list/)**: Uses this exact merge algorithm as a subroutine for Merge Sort.
- **[88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)**: The array equivalent, requiring traversing from the *back*.

## 🔗 Cross-Topic Connections
- **Merge Sort:** This is the conquer step of Merge Sort.
- **Priority Queues (Heaps):** Extending this logic to $K$ lists seamlessly transitions into heap concepts.

## ⚡ 2-Minute Revision Flash Card
- **Core Strategy:** Use a `dummy` node. Use a `curr` pointer to track the tail of the merged list.
- **Condition:** `while (l1 != NULL && l2 != NULL)`
- **Comparison:** `if (l1->val <= l2->val) { curr->next = l1; l1 = l1->next; }`
- **Tail attachment:** `curr->next = l1 ? l1 : l2;`
- **Cleanup:** Free the dummy node to avoid leaks.
