# Lecture 62: Copy List with Random Pointer: In-Place Interleaving (LeetCode 138)

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

#### Q2: [Conceptual] Why does the naive approach take $O(N^2)$? What makes it fail?
- **Answer:** The naive approach is: for each node $i$, scan all nodes to find which node the `random` pointer refers to, then assign it to the copy. Since finding the corresponding clone for each `random` pointer requires a linear scan of the copy list, the total work is $O(N) \times O(N) = O(N^2)$. The HashMap eliminates this by providing $O(1)$ lookup: `cloneMap[original] = clone`.

---

#### Q3: [Deep Dive] Why exactly does the interleaving technique work for `random` pointer assignment?
- **Answer:** After Step 1 (interleaving), the memory layout is:
  ```
  A -> A' -> B -> B' -> C -> C' -> NULL
  ```
  If `A->random = C`, then `A->random->next = C->next = C'`. So `A'->random = A->random->next` gives us `C'` — exactly the clone of what `A` points to. The interleaving creates a spatial invariant: **every clone sits immediately after its original**, turning "find the clone of node X" into a single pointer dereference: `X->next`.

---

#### Q4: [Extension] How would you clone a general directed graph? (LeetCode 133)
- **Answer:** Use BFS/DFS with a HashMap `original -> clone`. For each unvisited neighbor, create its clone and add to the queue. This is conceptually identical to Approach 1 (HashMap) for the linked list problem, but for graphs each node may have multiple neighbors (not just `next` and `random`). The interleaving trick does NOT generalize to arbitrary graphs.

---

#### Q5: [Debugging] What happens if you skip the `curr->random != nullptr` check in Step 2?
```cpp
// Buggy Step 2:
curr = head;
while (curr) {
    curr->next->random = curr->random->next;  // BUG: curr->random might be null!
    curr = curr->next->next;
}
```
- **Answer:** If `curr->random == nullptr`, then `curr->random->next` dereferences a null pointer → **segmentation fault / undefined behavior**. The fix is:
  ```cpp
  if (curr->random) curr->next->random = curr->random->next;
  ```

---

#### Q6: [Conceptual] Why must Step 3 (decoupling) be a separate pass and not merged with Step 2?
- **Answer:** During Step 2, we are still reading `curr->next->next` to navigate through the interleaved list. If we decouple pointers during Step 2, we would break the `curr->next->next` navigation chain, causing incorrect traversal. The three passes must be independent: **Interleave → Wire Randoms → Decouple**. Each pass leaves the structure in a state safe for the next pass.



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


## 🧠 Core Intuition — Why This Works
Copying a linked list with `random` pointers is hard because when you create `node->next`, the `random` pointer might point to a node that *hasn't been created yet*. 
There are two main ways to solve this:
1. **Hash Map Approach:** Map original nodes to their cloned counterparts. $O(N)$ space.
2. **Interleaving Nodes (Optimal):** Weave the cloned nodes directly into the original list (`A -> A' -> B -> B'`). This embeds the mapping directly into the list structure! Since `A->random` points to `C`, `A'->random` is simply `A->random->next` (which is `C'`). This achieves $O(1)$ space!

## 🎯 Pattern Recognition — When to Use This
- **"Deep copy a complex structure"**: When dealing with graphs or lists with cross-references, standard linear copying fails. Hash Maps are the universal fix, while interleaving is the specialized optimal trick.
- **Space Optimization Requirements**: If asked to do it in $O(1)$ space, the interleaving trick is the only acceptable answer.

## 🔍 Dry Run Trace (Interleaving Approach)
**Original:** `A -> B -> C`. (`A.random = C`)

- **Step 1: Interleave (Create clones next to originals)**
  - `A -> A' -> B -> B' -> C -> C'`
- **Step 2: Assign Random Pointers**
  - Iterate through originals (`curr`).
  - `A' = curr->next`.
  - `A'->random = (curr->random != NULL) ? curr->random->next : NULL;`
  - Since `A.random = C`, `A'.random` becomes `C.next`, which is exactly `C'`!
- **Step 3: Extract Clones & Restore Original**
  - Break the zigzag links to separate `A -> B -> C` and `A' -> B' -> C'`.
  - `curr->next = curr->next->next;`
  - `clone_curr->next = (clone_curr->next) ? clone_curr->next->next : NULL;`

## ⚠️ Common Interview Mistakes
1. **Failing to restore the original list:** In the optimal $O(1)$ space approach, candidates often successfully extract the deep copy but leave the original list broken. The interviewer expects the original input to be fully restored to its initial state.
2. **Null Pointer exceptions on randoms:** Blindly doing `curr->next->random = curr->random->next` crashes if `curr->random` is `NULL`. Always check `if (curr->random)`.
3. **Overlooking the Hash Map method:** Many candidates try to jump straight to the optimal interleaving method and mess it up. Always explain the $O(N)$ Hash Map method first! It's bulletproof and shows you know standard graph traversal techniques.

## 📊 Complexity Analysis
- **Hash Map Approach:** Time: $O(N)$ (2 passes). Space: $O(N)$ for the `unordered_map<Node*, Node*>`.
- **Interleaving Approach:** Time: $O(N)$ (3 passes). Space: $O(1)$ auxiliary space (excluding the output list).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: Can the Hash Map approach handle graph cloning too?
**Answer:** Yes. The Hash Map approach is the exact same concept used in "Clone Graph". The mapping strategy is universally applicable to any data structure with cycles or cross-references. The interleaving trick, however, only works for linear linked lists.

### Q2: Is the $O(1)$ space approach really better in production?
**Answer:** In academic interviews, yes. But in real-world production, the interleaving approach modifies the original list temporarily, making it **not thread-safe**. If another thread accesses the list during Steps 1 or 2, it will see corrupted data. The Hash Map approach is read-only on the input and is much safer for concurrent systems. Mentioning this tradeoff in an interview is a huge positive signal.

## 🏆 Related Problems
- **[133. Clone Graph](https://leetcode.com/problems/clone-graph/)**: The generalized version of this problem using BFS/DFS + Hash Map.
- **[148. Clone Binary Tree With Random Pointer](https://leetcode.com/problems/clone-binary-tree-with-random-pointer/)**: Similar concept applied to trees.

## 🔗 Cross-Topic Connections
- **Hash Maps:** Universal tool for keeping track of object identity vs object value.
- **Graph Traversal:** A linked list with random pointers is technically a directed graph with out-degree 2.

## ⚡ 2-Minute Revision Flash Card
- **Method 1 (Map):** `map[original] = new Node(original->val)`. Then `map[curr]->random = map[curr->random]`.
- **Method 2 (Optimal $O(1)$):**
  1. Insert `clone` immediately after `original`.
  2. `clone->random = original->random ? original->random->next : NULL`.
  3. Unweave: `orig->next = orig->next->next` and `clone->next = clone->next->next`.
