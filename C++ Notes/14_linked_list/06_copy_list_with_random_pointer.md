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
