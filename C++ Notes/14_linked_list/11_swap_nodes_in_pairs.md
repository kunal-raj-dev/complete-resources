# Lecture 67: Swap Nodes in Pairs: 2-Node Reversal via Dummy Head (LeetCode 24)

> **One-Line Purpose:** Master pairwise pointer swapping using a sentinel dummy node to rewire adjacent node pairs in $O(N)$ time and $O(1)$ auxiliary space without modifying node data values.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #67  
> **Video ID:** `wwbTMNVlFHQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=wwbTMNVlFHQ)  
> **Duration:** 20:06  
> **Transcript:** `.transcripts/14_linked_list/067_Swap_Nodes_in_Pairs___Linked_List.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 24: swapping every two adjacent nodes in-place.
- Why modifying node values (`swap(node1->val, node2->val)`) is explicitly forbidden in technical interviews.
- The **Dummy Head Sentinel Technique** to manage head swaps cleanly.
- The 3-line pointer rewiring sequence to swap two nodes and maintain connections to preceding and succeeding sublists.

---

## 🔵 Lecture Context

Swap Nodes in Pairs is the special case of Reverse Nodes in K-Group where $k = 2$. It tests clean iterative pointer rewiring and off-by-one avoidance.

---

## 1. Problem Statement

Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (only nodes themselves may be changed).

```
Input: 1 -> 2 -> 3 -> 4 -> NULL
Output: 2 -> 1 -> 4 -> 3 -> NULL
```

---

## 2. Iterative Pointer Rewiring Strategy

Let's trace swapping pair `first` and `second` preceded by `prev`:
```
prev -> first -> second -> next_pair
```

### The 3-Line Swap Sequence:
1. `first->next = second->next;` (Node 1 now points to `next_pair`).
2. `second->next = first;`        (Node 2 points backward to Node 1).
3. `prev->next = second;`         (Preceding list now connects to Node 2).

### Advance for Next Pair:
- `prev = first;` (Because after swapping, `first` is the tail of this pair!).
- Repeat while `prev->next != nullptr && prev->next->next != nullptr`.

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
    ListNode* swapPairs(ListNode* head) {
        // Sentinel dummy node on stack
        ListNode dummy(0);
        dummy.next = head;
        ListNode* prev = &dummy;

        // Loop as long as at least two nodes exist ahead
        while (prev->next != nullptr && prev->next->next != nullptr) {
            ListNode* first = prev->next;
            ListNode* second = prev->next->next;

            // 3-step pointer rewiring
            first->next = second->next;
            second->next = first;
            prev->next = second;

            // Advance prev to the tail of the newly swapped pair
            prev = first;
        }

        return dummy.next;
    }
};

int main() {
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);

    Solution solver;
    ListNode* swapped = solver.swapPairs(head);

    cout << "Swapped Pairs: ";
    while (swapped) {
        cout << swapped->val << " -> ";
        swapped = swapped->next;
    }
    cout << "NULL\n";
    return 0;
}
```

- **Time Complexity:** $O(N)$ (Visits each node once).
- **Auxiliary Space Complexity:** $O(1)$ (Pointer manipulation only).

---

## 🔍 Detailed Trace: `1 -> 2 -> 3 -> 4 -> NULL`

1. `dummy.next = 1`, `prev = &dummy`.
2. Pair 1: `first = 1`, `second = 2`.
   - `1->next = 3`
   - `2->next = 1`
   - `dummy.next = 2`
   - List state: `dummy -> 2 -> 1 -> 3 -> 4`.
   - `prev` advances to `first` (Node 1).
3. Pair 2: `first = 3`, `second = 4`.
   - `3->next = NULL`
   - `4->next = 3`
   - `1->next = 4`
   - List state: `dummy -> 2 -> 1 -> 4 -> 3 -> NULL`.
   - `prev` advances to `first` (Node 3).
4. `prev->next == nullptr` $\to$ Loop terminates.
Return `dummy.next` (Node 2). Correct!

---

## 🧠 Mental Model: Swapping Dance Partners

Think of couples dancing in a line. The master of ceremonies (`prev`) taps the couple (`first` and `second`), directs the second person to spin in front of the first, re-attaches the line behind them, and steps to the end of that couple.

---

## ⚠️ Common Mistakes

1. **Overwriting Before Saving:** Setting `second->next = first` *before* saving `second->next` into `first->next` loses the rest of the list.
2. **Advancing `prev` incorrectly:** Writing `prev = second`. Since `first` was swapped to the second position, `first` is the actual tail of the pair!

---

## 🖥️ System-Specific Notes

- Using stack-allocated `ListNode dummy(0)` eliminates heap allocation overhead and prevents memory fragmentation.

---

## 🟡 Additional Essential Context

The recursive formulation is exceptionally elegant:
```cpp
ListNode* swapPairsRecursive(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* second = head->next;
    head->next = swapPairsRecursive(second->next);
    second->next = head;
    return second;
}
```
However, the iterative method is preferred in production to avoid $O(N)$ call-stack memory.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does LeetCode explicitly forbid swapping node values?  
**A:** In real-world enterprise codebases, a `ListNode` might store a complex object payload (e.g. user profiles, video streams, or cryptographic buffers) that is expensive or unsafe to copy. Pointer rewiring changes logical ordering in $O(1)$ time regardless of object size.

---

### 🔥 Interview Questions

#### Q1: What is the behavior on odd-length lists?
- **Short Answer:** The last remaining node is not swapped and remains attached at the end.
- **Detailed Explanation:** The condition `prev->next && prev->next->next` evaluates to false when only one node remains, leaving the odd node untouched.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// Input: [1]
// Output: [1]
```

---

## Edge Cases

1. **Empty List:** Returns `nullptr`.
2. **Single Node:** Returns `head`.
3. **Odd Length (`1 -> 2 -> 3`):** Returns `2 -> 1 -> 3`.

---

## Complexity Analysis

- **Time Complexity:** $O(N)$ (One linear pass).
- **Auxiliary Space Complexity:** $O(1)$ (Pointer updates only).

---

## Key Takeaways

1. **Sentinel Node:** Makes head swapping identical to middle swaps.
2. **3 Steps:** `first->next = second->next; second->next = first; prev->next = second;`.
3. **Advance pointer:** `prev = first;`.

---

## ⚡ 2-Minute Revision

- Loop condition: `while (prev->next && prev->next->next)`.
- Reorder: `first->next = second->next; second->next = first; prev->next = second;`.
- Advance: `prev = first;`.


## 🧠 Core Intuition — Why This Works
Swapping nodes in pairs is a specialized, simpler case of reversing nodes in $K$-groups where $K=2$. Because the group size is strictly 2, we don't need a full reversal `while` loop. We can manually rewire the three critical pointers (`prev->next`, `node1->next`, `node2->next`) in $O(1)$ operations per pair. Using a dummy node keeps the logic identical for the head pair.

## 🎯 Pattern Recognition — When to Use This
- **"Swap pairs"**: Directly maps to this algorithm.
- **"Pairwise modification"**: Reordering interleaved nodes (like Odd/Even Linked List) relies on similar 2-step pointer jumps.

## 🔍 Dry Run Trace
**Example:** `1 -> 2 -> 3 -> 4`
- **Setup:** `D -> 1 -> 2 -> 3 -> 4`. `prev = D`.
- **Iteration 1:** `curr = 1`
  - `first = 1`, `second = 2`.
  - Rewire 1: `first->next = second->next` (`1 -> 3`)
  - Rewire 2: `second->next = first` (`2 -> 1`)
  - Rewire 3: `prev->next = second` (`D -> 2`)
  - Move: `prev = first` (`1`), `curr = first->next` (`3`).
  - List is now `D -> 2 -> 1 -> 3 -> 4`.
- **Iteration 2:** `curr = 3`
  - `first = 3`, `second = 4`.
  - `first->next = second->next` (`3 -> NULL`)
  - `second->next = first` (`4 -> 3`)
  - `prev->next = second` (`1 -> 4`)
  - Move: `prev = first` (`3`), `curr = NULL`.
  - List is now `D -> 2 -> 1 -> 4 -> 3`.

## ⚠️ Common Interview Mistakes
1. **Losing the pointer to the rest of the list:** If you do `second->next = first` before saving `second->next` (node 3), you lose the rest of the list. Order of pointer assignment is critical!
2. **Missing Dummy Node:** Without a dummy node, swapping the first two nodes requires special conditional logic because the `head` of the entire list changes from `1` to `2`. 
3. **Odd number of nodes:** Forgetting to handle lists with an odd number of nodes (e.g., `1->2->3`). The loop condition must check `curr != NULL && curr->next != NULL`. If `curr->next` is `NULL`, we have an unpaired node at the end, and we just leave it alone.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$. We visit each node exactly once.
- **Space Complexity:** $O(1)$ auxiliary space for the iterative approach.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can we just swap the *values* of the nodes instead of the pointers?
**Answer:** Yes, doing `swap(first->val, second->val)` is perfectly valid C++ and takes 2 lines of code. However, interviewers will *always* explicitly forbid this. In real-world systems, the "value" of a node might be a massive 5GB object or a complex struct where copying data is prohibitively expensive or impossible. You must manipulate the pointers.

### Q2: Compare this to Reverse in K-Groups.
**Answer:** This is a hardcoded version of $K=2$. While you could reuse your $K$-group code, hardcoding the 3 pointer swaps for pairs is much faster to execute (avoids the inner `while` loop overhead) and significantly shorter to write.

## 🏆 Related Problems
- **[25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)**: The generalized version.
- **[328. Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/)**: Requires jumping pointers by 2, similar to pairwise grouping.

## 🔗 Cross-Topic Connections
- **Pointers & Memory:** Manual pointer rewiring is a fundamental C++ skill.

## ⚡ 2-Minute Revision Flash Card
- **Core Loop:** `while(curr && curr->next)`
- **Three Steps per Pair:**
  1. `first->next = second->next;`
  2. `second->next = first;`
  3. `prev->next = second;`
- **Advance:** `prev = first; curr = first->next;`
