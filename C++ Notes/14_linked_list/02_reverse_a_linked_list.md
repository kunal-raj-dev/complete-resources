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
- **When to use:** Only when you additionally need a copy of the original order, or in contexts where you cannot mutate the list.

---

#### Q2: [Hard Extension] How do you reverse a linked list in groups of K? (LeetCode 25)
- **Answer:** Use the `reverseKGroup` approach: verify $k$ nodes exist, reverse them with the 3-pointer technique for exactly $k$ iterations, then reconnect: `head->next = reverseKGroup(curr, k)`. The key insight is that after reversing, the original `head` becomes the **tail** of the group and must be connected to the output of the next recursion.
```cpp
ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode* temp = head;
    for (int i = 0; i < k; i++) {
        if (!temp) return head;  // Fewer than k nodes: leave as-is
        temp = temp->next;
    }
    ListNode* prev = nullptr, *curr = head;
    for (int i = 0; i < k; i++) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    head->next = reverseKGroup(curr, k);
    return prev;
}
```

---

#### Q3: [Extension] How do you reverse only a sublist from position `left` to `right`? (LeetCode 92)
- **Answer:** Use a dummy node before `head`. Advance to the node just before `left`. Run the 3-pointer reversal for exactly `right - left` steps. Reconnect the tail of the reversed segment to the node after `right`. Time: $O(N)$, Space: $O(1)$.
- **Key invariant:** Track `connPrev` (node before `left`) and `curr` (node at `left`). After reversal, `curr` is the tail; `connPrev->next->next = curr_after_right`.

---

#### Q4: [Recursion / Call Stack] What does the call stack look like when `reverseList` is called on `[1, 2, 3]`?
- **Answer:** Each recursive call suspends at `ListNode* newHead = reverseList(head->next)`:
  ```
  Frame 1: head=1, waiting...
    Frame 2: head=2, waiting...
      Frame 3: head=3, base case returns head=3
    Frame 2 resumes: head->next->next = head => 3->2. head->next = null. Returns 3.
  Frame 1 resumes: head->next->next = head => 2->1. head->next = null. Returns 3.
  ```
  The stack depth is $O(N)$, which causes **stack overflow** for $N \ge 10^5$.

---

#### Q5: [Debugging] What does this buggy recursive code do wrong?
```cpp
ListNode* reverseList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* newHead = reverseList(head->next);
    head->next->next = head;
    // BUG: Missing head->next = nullptr;
    return newHead;
}
```
- **Answer:** Without `head->next = nullptr`, after unwinding frame 1 (head=1), node 1's `next` still points to node 2, and node 2's `next` points to node 1. This creates a **circular reference** between nodes 1 and 2: `1 <-> 2 -> NULL`. Traversing the result causes an infinite loop.

---

#### Q6: [Output Prediction] What does this iterative code return for `head = [1]`?
```cpp
ListNode* prev = nullptr;
ListNode* curr = head;
while (curr) {
    ListNode* nxt = curr->next;
    curr->next = prev;
    prev = curr;
    curr = nxt;
}
return prev;
```
- **Answer:** Returns the same single node `[1]`. The while loop runs once: `nxt = null, curr->next = null, prev = node(1), curr = null`. Loop exits. Returns `prev = node(1)`. Correct — single node lists are a no-op.

---

#### Q7: [Conceptual] What is the loop invariant of the iterative reversal?
- **Answer:** At the end of each iteration, `prev` is the head of the reversed portion processed so far, and `curr` is the head of the remaining unreversed portion. This invariant is established before the first iteration (empty reversed portion, full list unreversed) and is maintained throughout. When `curr == nullptr`, the entire list is reversed and `prev` is the new head.



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


## 🧠 Core Intuition — Why This Works
To reverse a linked list, we don't need to move the data inside the nodes. Instead, we just reverse the direction of the `next` pointers. For any given node, instead of pointing to the next node, it should point to its previous node. To do this without losing the rest of the list, we need three pointers: `prev`, `curr`, and `next_node`. We carefully iterate, rewiring one link at a time.

## 🎯 Pattern Recognition — When to Use This
- **"Reverse a section of a sequence"**: Whenever a problem asks to reverse a linked list or parts of it (e.g., Reverse in K-Groups, Palindrome Linked List).
- **In-place modifications**: Reversing is strictly an $O(1)$ space operation. If an interviewer asks to do something backwards in a linked list without extra space, reverse it!

## 🔍 Dry Run Trace
**Example:** `1 -> 2 -> 3 -> NULL`
- Initialize: `prev = NULL`, `curr = 1`
- **Iteration 1:**
  - `next_node = curr->next` (`2`)
  - `curr->next = prev` (`1 -> NULL`)
  - `prev = curr` (`1`)
  - `curr = next_node` (`2`)
- **Iteration 2:**
  - `next_node = curr->next` (`3`)
  - `curr->next = prev` (`2 -> 1 -> NULL`)
  - `prev = curr` (`2`)
  - `curr = next_node` (`3`)
- **Iteration 3:**
  - `next_node = curr->next` (`NULL`)
  - `curr->next = prev` (`3 -> 2 -> 1 -> NULL`)
  - `prev = curr` (`3`)
  - `curr = next_node` (`NULL`)
- `curr` is `NULL`, loop ends. Return `prev` (which is `3`, the new head).

## ⚠️ Common Interview Mistakes
1. **Losing the rest of the list:** Writing `curr->next = prev` *before* saving `curr->next` in `next_node`. This breaks the chain and you lose access to the remaining nodes!
2. **Returning the wrong head:** Returning `curr` instead of `prev` at the end of the loop. When the loop terminates, `curr` is always `NULL`, so you end up returning an empty list!
3. **Handling single node or empty list:** Not accounting for `head == NULL` or `head->next == NULL`. The standard 3-pointer logic implicitly handles this safely, but custom logic often fails.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ to traverse the list exactly once.
- **Space Complexity:** $O(1)$ for the iterative approach (only 3 pointers). $O(N)$ for the recursive approach due to the recursion stack.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Compare the iterative and recursive approaches. Which is better?
**Answer:** The iterative approach is strictly better because it uses $O(1)$ space. The recursive approach takes $O(N)$ space on the call stack, which can lead to a Stack Overflow for a list with millions of nodes. However, understanding the recursive approach is crucial for trees and advanced linked list problems.

### Q2: How does the recursive reversal work under the hood?
**Answer:** In the recursive approach, we traverse all the way to the last node, making it the new head. As the recursion unwinds, for a given `node`, we make its next node point back to it: `node->next->next = node`, and then break the original forward link: `node->next = NULL`.

## 🏆 Related Problems
- **[92. Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/)**: Reverse only a sublist from position `left` to `right`.
- **[234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)**: Requires reversing the second half of the list.
- **[25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)**: The ultimate test of reversal logic.

## 🔗 Cross-Topic Connections
- **Recursion Stack / Call Stack**: The recursive implementation is a classic textbook example of how the call stack remembers previous states.
- **Two Pointers**: Modifying the links relies heavily on maintaining a trailing and leading pointer (`prev` and `next`).

## ⚡ 2-Minute Revision Flash Card
- **Core Logic (Iterative):** Save `next`, rewire `curr->next = prev`, shift `prev = curr`, shift `curr = next`.
- **Termination:** Loop until `curr != NULL`. Return `prev` as the new head.
- **Recursive Core:** `newHead = reverse(head->next); head->next->next = head; head->next = NULL; return newHead;`
