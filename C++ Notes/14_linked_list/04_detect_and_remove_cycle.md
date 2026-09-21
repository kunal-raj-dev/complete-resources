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
- **Detailed Explanation:** Once `slow` enters the cycle, it is at most $C - 1$ nodes ahead of `fast` (in the reference frame where `fast` is chasing `slow`). Since the relative closing speed is $1$ node per step, `fast` catches `slow` in at most $C$ steps.

---

#### Q2: [Proof] Why can `fast` never "hop over" `slow` inside the cycle?
- **Answer:** At each discrete step, `fast` moves exactly $2$ positions and `slow` moves exactly $1$ position. In the reference frame of `slow`, `fast` moves at relative velocity $2 - 1 = 1$ position per step on a discrete integer grid. A pointer moving at relative speed $1$ can only reduce the gap by exactly $1$ each iteration — it cannot skip any integer position. Therefore, it must hit `slow` directly before passing it.

---

#### Q3: [Extension] How would you find the length of the cycle after detecting it?
- **Answer:** After detection (when `slow == fast`), keep `slow` fixed and advance `fast` one step at a time until `fast == slow` again. Count the steps taken — that count is exactly $C$, the cycle length.
```cpp
int cycleLength(ListNode* meetingPoint) {
    int length = 1;
    ListNode* curr = meetingPoint->next;
    while (curr != meetingPoint) {
        curr = curr->next;
        length++;
    }
    return length;
}
```

---

#### Q4: [Conceptual] What is the role of $k$ in the formula $L_1 = (k-1) \cdot C + (C - d)$? What happens when $k = 1$?
- **Answer:** $k$ is the number of complete cycles `fast` has completed inside the loop by the time it meets `slow`. When $k = 1$ (the minimal case), the formula simplifies to $L_1 = C - d$, which means the distance from `head` to the cycle entry is exactly the remaining arc from the meeting point to the entry. In most interview problems, assume $k = 1$ for intuition — the math holds for any $k \ge 1$.

---

#### Q5: [LeetCode 287] How does Floyd's Algorithm apply to "Find the Duplicate Number" in an array?
- **Answer:** An array `nums` of $n+1$ integers where each is in $[1, n]$ is treated as a linked list where index $i$ points to index `nums[i]`. A duplicate value means two indices point to the same "next" node, creating a cycle. Apply Floyd's algorithm treating `nums[0]` as the head:
  - Phase 1: `slow = nums[slow]; fast = nums[nums[fast]];` until they meet.
  - Phase 2: Reset `slow = nums[0]`; advance both by 1 step until `slow == fast`. The meeting value is the duplicate.
- **Why this works:** The duplicate number is exactly the cycle entry point in this linked-list analogy.

---

#### Q6: [Debugging] What is wrong with this code for finding cycle entry?
```cpp
// Buggy version
ListNode* detectCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            slow = head;
            while (slow != fast) {  // BUG: what if cycle starts at head?
                slow = slow->next;
                fast = fast->next;
            }
            return slow;
        }
    }
    return nullptr;
}
```
- **Answer:** The code is actually correct for the general case, but subtle: when `slow == fast == head` (the cycle starts at head itself and fast meets slow at head on the first collision), the inner `while (slow != fast)` exits immediately (since `slow == head == fast`), returning `head` correctly. However, the **removal** version (not detection) has the bug — you must separately handle the `slow == fast` at head case to walk `fast` around the cycle to find the last node. The detection and entry-finding logic above is safe.

---

#### Q7: [System Design] Can Floyd's Algorithm detect cycles in a directed graph?
- **Answer:** Floyd's algorithm as described works specifically on structures where each node has exactly ONE outgoing edge (functional graphs / linked lists). For a general directed graph (where nodes can have multiple edges), you must use DFS with a recursion stack (white/grey/black coloring) to detect back edges. Floyd's algorithm does NOT generalize to arbitrary graphs.

---

#### Q8: [Two-Pointer Philosophy] When should you use fast/slow pointers vs other techniques?
- **Answer:** Use fast/slow pointers when:
  1. **Cycle detection** in any structure reducible to a linked list (functional graphs, arrays with value-as-index).
  2. **Finding the middle** of a linked list in a single pass.
  3. **$k$-th node from end**: advance fast by $k$ steps first, then advance both until fast hits null.
  4. **Palindrome detection**: find middle (slow/fast), reverse second half, compare.
  
  Avoid when: random access is needed, or the structure has multiple outgoing edges per node.

---

#### Q9: [Output Prediction] What does this code print for the list `1 -> 2 -> 3 -> 4 -> 5 -> NULL` (no cycle)?
```cpp
ListNode* slow = head;
ListNode* fast = head;
while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
}
cout << slow->val;
```
- **Answer:** Prints `3`. When `fast` reaches node 5 (`fast->next == nullptr`), `slow` has taken $\lfloor N/2 \rfloor = 2$ steps from head, landing on node `3`. This is exactly the "find middle" application of the slow/fast pointer technique.

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


## 🧠 Core Intuition — Why This Works
If a linked list has a cycle, a slow pointer (1 step) and a fast pointer (2 steps) will eventually enter the cycle and run infinitely. Because the fast pointer reduces the distance to the slow pointer by exactly 1 node per step within the cycle, they are mathematically guaranteed to meet. Once they meet, resetting one pointer to the head and moving both at 1 step per time will cause them to collide exactly at the entrance of the cycle (Floyd's Cycle Detection Algorithm).

## 🎯 Pattern Recognition — When to Use This
- **"Does the list terminate or loop infinitely?"**: Immediate cue for Cycle Detection (Tortoise and Hare).
- **"Find the start of the loop"**: Requires the two-phase Floyd approach.
- **Graph cycles in limited space**: E.g., "Find the Duplicate Number" maps exactly to this linked list cycle logic.

## 🔍 Dry Run Trace
**Example:** `1 -> 2 -> 3 -> 4 -> 5 -> 3` (cycle at 3)
- **Phase 1 (Detect Cycle):**
  - `slow = 1`, `fast = 1`
  - `slow = 2`, `fast = 3`
  - `slow = 3`, `fast = 5`
  - `slow = 4`, `fast = 4` (Collision!)
- **Phase 2 (Find Entry):**
  - Reset `slow = 1`. `fast` stays at `4`.
  - Move both by 1 step:
  - `slow = 2`, `fast = 5`
  - `slow = 3`, `fast = 3` (Collision! The entry node is `3`).
- **Phase 3 (Remove Cycle):**
  - To remove, we needed a pointer just *before* the entry node to set `next = NULL`. Alternatively, while moving in Phase 2, check `slow->next == fast->next`. The collision happens *before* they step onto the entry node, allowing you to break the link.

## ⚠️ Common Interview Mistakes
1. **Setting `fast` initially to `head->next`:** For cycle *detection*, this works. But for finding the *starting node* using Floyd's math, both `slow` and `fast` MUST start at `head`. If you start `fast = head->next`, the math equation breaks, and Phase 2 will point to the wrong node!
2. **Infinite Loop during Removal:** If you just use `while(fast != slow)`, you find the entry node but you don't know the *previous* node to break the cycle. A standard trick is `while(slow->next != fast->next)` so they stop one node before the entry.
3. **Handling the Head Cycle Edge Case:** If the cycle starts at the head (`head->next = head`), checking `slow->next != fast->next` fails. You must handle the case where `slow == head` and `fast == head` separately.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$. Phase 1 takes at most $N$ steps to collide. Phase 2 takes at most $N$ steps to find the entry. Total operations $< 2N$.
- **Space Complexity:** $O(1)$. No hash maps or extra memory used.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Why does Phase 2 math (resetting to head) work?
**Answer:** Let $L$ be the straight line before the cycle, and $C$ be the cycle length. They meet at distance $X$ inside the cycle.
- Slow distance = $L + X$
- Fast distance = $L + X + kC$
- Since fast travels twice as much: $2(L + X) = L + X + kC \implies L + X = kC \implies L = kC - X$.
- The distance from the head to entry is $L$. The distance from the collision point to the entry point is $C - X$, which is equivalent to $kC - X$. Thus, moving one pointer from the head and one from the collision point at the same speed will make them meet exactly at the cycle entry!

### Q2: Could we use a Hash Set instead?
**Answer:** Yes, storing visited nodes in an `unordered_set` is $O(N)$ time and easily detects cycles and the entry node (the first duplicate). However, it uses $O(N)$ space, which fails the standard interview constraint of $O(1)$ auxiliary space.

## 🏆 Related Problems
- **[141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)**: Just return true/false.
- **[142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)**: Return the node where the cycle begins.
- **[287. Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)**: Array problem implicitly solved using Floyd's algorithm.

## 🔗 Cross-Topic Connections
- **Math/Algebra:** The proof of correctness relies on modular arithmetic and linear equations.
- **Graph Theory:** This is a specialized cycle detection for directed graphs where out-degree is 1.

## ⚡ 2-Minute Revision Flash Card
- **Detect:** `slow = head, fast = head`. `fast` moves 2, `slow` moves 1. If they equal, cycle exists.
- **Find Entry:** Reset `slow = head`. Move both 1 step until `slow == fast`.
- **Remove:** Instead of `slow == fast`, use `while(slow->next != fast->next)`. Break loop via `fast->next = NULL`. (Handle head cycle edge case explicitly!).
