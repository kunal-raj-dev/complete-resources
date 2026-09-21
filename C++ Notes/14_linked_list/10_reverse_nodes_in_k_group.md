# Lecture 66: Reverse Nodes in K-Group: Hard Level Group Splicing (LeetCode 25)

> **One-Line Purpose:** Master composite linked-list reversals by reversing contiguous chunks of size $k$ and stitching boundary pointers across groups, achieving strict $O(N)$ time and $O(1)$ auxiliary space.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #66  
> **Video ID:** `-swgIiMIlJo`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=-swgIiMIlJo)  
> **Duration:** 20:39  
> **Transcript:** `.transcripts/14_linked_list/066_Reverse_Nodes_in_K-Group___Linked_List.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- The requirements of LeetCode 25 (Reverse Nodes in k-Group): reversing nodes in groups of $k$ at a time.
- The rule for remaining nodes: if the number of nodes is not a multiple of $k$, left-out nodes at the end must remain in their original order.
- The 3-phase modular solution:
  1. Check if at least $k$ nodes exist ahead.
  2. Reverse the current $k$ nodes.
  3. Reconnect the reversed group to the recursively reversed subsequent groups.
- Iterative vs Recursive approaches and their space complexity implications ($O(1)$ vs $O(N/k)$).

---

## 🔵 Lecture Context

Reverse Nodes in k-Group is rated Hard on LeetCode and is a quintessential Tier-1 FAANG interview problem. It combines linked-list length verification, sublist reversal, and boundary pointer stitching.

---

## 1. Problem Statement

Given the `head` of a linked list, reverse the nodes of the list $k$ at a time, and return the modified list.
- $k$ is a positive integer and is $\le$ the length of the linked list.
- If the number of nodes is not a multiple of $k$, the remaining nodes at the end should remain as they are.
- You **cannot** alter values in the list's nodes; only nodes themselves may be changed.

```
Input: head = [1, 2, 3, 4, 5], k = 2
Output: [2, 1, 4, 3, 5]

Input: head = [1, 2, 3, 4, 5], k = 3
Output: [3, 2, 1, 4, 5]
```

---

## 2. Algorithmic Steps (Recursive Formulation)

For each group starting at `head`:
1. **Verification Pass:** Check if at least $k$ nodes exist from `head`.
   - If fewer than $k$ nodes remain, return `head` directly without reversing!
2. **Reverse Current $k$ Nodes:** Using standard 3-pointer reversal for exactly $k$ iterations.
   - `prev` becomes the new head of this reversed $k$-group.
   - `head` is now the tail of this reversed $k$-group!
3. **Recursive Reconnection:**
   - The remaining unreversed list starts at `curr`.
   - Set `head->next = reverseKGroup(curr, k);`.
4. Return `prev`.

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
    ListNode* reverseKGroup(ListNode* head, int k) {
        // Step 1: Check if there are at least k nodes available
        ListNode* temp = head;
        for (int i = 0; i < k; i++) {
            if (temp == nullptr) {
                return head; // Fewer than k nodes remain: leave as-is!
            }
            temp = temp->next;
        }

        // Step 2: Reverse the first k nodes
        ListNode* prev = nullptr;
        ListNode* curr = head;
        for (int i = 0; i < k; i++) {
            ListNode* next_node = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next_node;
        }

        // Step 3: Reconnect tail to the recursively reversed remaining list
        // 'head' is now the tail of this k-group!
        // 'curr' is the start of the next k-group
        head->next = reverseKGroup(curr, k);

        return prev; // 'prev' is the new head of this k-group
    }
};

int main() {
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);

    Solution solver;
    ListNode* res = solver.reverseKGroup(head, 2);

    cout << "K-Group Reversed: ";
    while (res) {
        cout << res->val << " -> ";
        res = res->next;
    }
    cout << "NULL\n";
    return 0;
}
```

- **Time Complexity:** $O(N)$ (Each node is traversed twice: once for length check, once for reversal).
- **Auxiliary Space Complexity:** $O(N / k)$ (Recursion stack depth).

---

## 🔍 Detailed Trace: `[1, 2, 3, 4, 5]`, $k = 2$

### Call 1 on `head = 1`:
- Verifies 2 nodes exist (`1, 2`).
- Reverses first 2 nodes: `2 -> 1`.
- `prev = 2` (new head), `head = 1` (new tail), `curr = 3`.
- Calls `reverseKGroup(3, 2)`.

### Call 2 on `head = 3`:
- Verifies 2 nodes exist (`3, 4`).
- Reverses: `4 -> 3`.
- `prev = 4`, `head = 3`, `curr = 5`.
- Calls `reverseKGroup(5, 2)`.

### Call 3 on `head = 5`:
- Only 1 node exists ($< k$) $\to$ Returns `5` untouched!

### Unwinding:
- Call 2 connects: `3->next = 5` $\to$ Returns `4`.
- Call 1 connects: `1->next = 4` $\to$ Returns `2`.
**Final Result:** `2 -> 1 -> 4 -> 3 -> 5 -> NULL`. Correct!

---

## 🧠 Mental Model: Stitching Train Couplers

Imagine a freight train with $N$ cars. You decouple the first $k$ cars, turn them around on a turntable, and reconnect their tail to the output of the next turntable down the track.

---

## ⚠️ Common Mistakes

1. **Reversing the Incomplete Remainder:** Forgetting the $k$-node lookahead check causes the leftover $N \pmod k$ nodes to be reversed, violating problem constraints.
2. **Losing the Next Group Reference:** Not tracking `curr` across the reversal loop severs the connection to the upcoming group.

---

## 🖥️ System-Specific Notes

- For strict $O(1)$ memory requirements, an iterative version using a dummy node and four pointers (`dummy`, `groupPrev`, `kTh`, `groupNext`) performs all group reversals in-place without recursion stack frames.

---

## 🟡 Additional Essential Context

When $k = 2$, this problem reduces directly to **Swap Nodes in Pairs (LeetCode 24)**.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** What is the invariant maintained by `head->next = reverseKGroup(curr, k)`?  
**A:** `head` was initially the front of the group, but after reversal it has become the group's tail. Connecting `head->next` ensures the group's tail attaches cleanly to whatever head is returned by the next group.

---

### 🔥 Interview Questions

#### Q1: Can you solve this iteratively in $O(1)$ auxiliary space?
- **Short Answer:** Yes, by maintaining `groupPrev` and finding the $k$-th node in each iteration, reversing the subsegment in-place, and rewiring `groupPrev->next` and `tail->next`.

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// [1, 2, 3], k = 4
// Output: [1, 2, 3] (Length < k -> Zero modifications)
```

---

## Edge Cases

1. **$k = 1$:** Every group is size 1 $\to$ List remains identical.
2. **$k = N$:** Equivalent to standard reverse linked list.
3. **Empty List:** Returns `nullptr`.

---

## Complexity Analysis

- **Time Complexity:** $O(N)$ (Each node visited at most twice).
- **Auxiliary Space Complexity:** $O(N / k)$ for recursive stack ($O(1)$ for iterative).

---

## Key Takeaways

1. **Lookahead:** Verify $k$ nodes exist before reversing.
2. **Boundary Stitching:** `head->next = reverseKGroup(curr, k)`.
3. **Preserve Remainder:** Leftover nodes $< k$ must remain unreversed.

---

## ⚡ 2-Minute Revision

- Verify $k$ nodes: `for (int i = 0; i < k; i++) if (!temp) return head;`.
- Reverse $k$ nodes using 3 pointers.
- Reconnect: `head->next = reverseKGroup(curr, k); return prev;`.
