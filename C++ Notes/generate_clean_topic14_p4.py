import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t14_dir = os.path.join(root, "14_linked_list")

notes = {}

# 10: Reverse Nodes in K-Group
notes["10_reverse_nodes_in_k_group.md"] = r"""# Lecture 66: Reverse Nodes in K-Group: Hard Level Group Splicing (LeetCode 25)

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
"""

# 11: Swap Nodes in Pairs
notes["11_swap_nodes_in_pairs.md"] = r"""# Lecture 67: Swap Nodes in Pairs: 2-Node Reversal via Dummy Head (LeetCode 24)

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
"""

# 12: LRU Cache
notes["12_lru_cache.md"] = r"""# Lecture 78: Implement LRU Cache: DLL + Hash Map $O(1)$ Design (LeetCode 146)

> **One-Line Purpose:** Master composite data structure design by coupling a Doubly Linked List with a Hash Map to achieve strict $O(1)$ time complexity for both `get()` and `put()` cache operations.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #78  
> **Video ID:** `GsY6y0iPaHw`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=GsY6y0iPaHw)  
> **Duration:** 35:34  
> **Transcript:** `.transcripts/14_linked_list/078_L76._Implement_LRU_Cache___Linked_List.txt`  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives

By the end of this lecture, you should understand:
- What a Cache is and why the **Least Recently Used (LRU)** eviction policy is universally used in systems.
- Why neither a Hash Map alone ($O(N)$ eviction) nor a Doubly Linked List alone ($O(N)$ search) can satisfy $O(1)$ operations independently.
- The hybrid architecture: **Hash Map + Doubly Linked List (DLL)**.
- Implementing `addNode(head)` and `deleteNode(node)` helpers to manage MRU and LRU positions in $O(1)$ time.
- Handling capacity eviction: removing the node immediately preceding `tail` from both the DLL and the Hash Map.

---

## 🔵 Lecture Context

LRU Cache (LeetCode 146) is arguably the single most iconic system-design and data-structure interview problem at FAANG. It tests whether an engineer can combine multiple fundamental data structures to achieve optimal time complexity.

---

## 1. Problem Statement & The LRU Policy

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.
Implement the `LRUCache` class:
- `LRUCache(int capacity)`: Initialize the cache with positive size `capacity`.
- `int get(int key)`: Return value of `key` if it exists, otherwise return `-1`. Accessing a key marks it as **Most Recently Used (MRU)**.
- `void put(int key, int value)`: Update or insert `key` and `value`. If number of keys exceeds `capacity`, evict the **Least Recently Used (LRU)** key.
- **Strict Requirement:** Both `get` and `put` must run in **$O(1)$ average time complexity**.

---

## 2. The Hybrid Architecture: Hash Map + Doubly Linked List

| Data Structure | Search Time | Deletion / Insertion Time | Limitation |
|---|---|---|---|
| Array / Vector | $O(N)$ | $O(N)$ (Shifting required) | Too slow |
| Hash Map alone | **$O(1)$** | $O(1)$ | No ordering to track recency! |
| DLL alone | $O(N)$ (Linear scan) | **$O(1)$** | Search is too slow |
| **Hash Map + DLL** | **$O(1)$** | **$O(1)$** | **Combines instant search with instant reordering!** |

### The Invariants:
1. **Doubly Linked List:** Maintains chronological access order:
   - `head->next`: **Most Recently Used (MRU)** node.
   - `tail->prev`: **Least Recently Used (LRU)** node (prime candidate for eviction).
2. **Hash Map (`unordered_map<int, Node*>`):** Maps `key` directly to its corresponding `Node*` in the DLL in $O(1)$ time.

```
                    MRU                                    LRU
[head (dummy)] <-> [Node(key1, val1)] <-> [Node(key2, val2)] <-> [tail (dummy)]
       ^                       ^
       |                       |
hash_map[key1] --------+       |
hash_map[key2] ----------------+
```

---

## 3. Complete C++ Implementation

```cpp
#include <iostream>
#include <unordered_map>
using namespace std;

class LRUCache {
private:
    struct Node {
        int key;
        int val;
        Node* prev;
        Node* next;
        Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
    };

    int capacity;
    unordered_map<int, Node*> cache;
    Node* head; // Dummy head (MRU side)
    Node* tail; // Dummy tail (LRU side)

    // Helper: Add node immediately after dummy head (MRU position)
    void addNode(Node* newNode) {
        Node* temp = head->next;
        newNode->next = temp;
        newNode->prev = head;
        head->next = newNode;
        temp->prev = newNode;
    }

    // Helper: Delete arbitrary node in O(1) time
    void deleteNode(Node* delNode) {
        Node* prevNode = delNode->prev;
        Node* nextNode = delNode->next;
        prevNode->next = nextNode;
        nextNode->prev = prevNode;
    }

public:
    LRUCache(int cap) {
        capacity = cap;
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head->next = tail;
        tail->prev = head;
    }

    ~LRUCache() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* nxt = curr->next;
            delete curr;
            curr = nxt;
        }
    }

    int get(int key) {
        if (cache.find(key) == cache.end()) {
            return -1; // Key not found
        }

        Node* resNode = cache[key];
        int resVal = resNode->val;

        // Mark as Most Recently Used: Delete and re-add at head
        deleteNode(resNode);
        addNode(resNode);

        return resVal;
    }

    void put(int key, int value) {
        // Case 1: Key already exists -> Update value and move to MRU
        if (cache.find(key) != cache.end()) {
            Node* existingNode = cache[key];
            existingNode->val = value;
            deleteNode(existingNode);
            addNode(existingNode);
            return;
        }

        // Case 2: Cache is full -> Evict Least Recently Used (tail->prev)
        if (cache.size() == capacity) {
            Node* lruNode = tail->prev;
            cache.erase(lruNode->key); // Erase from hash map!
            deleteNode(lruNode);       // Remove from DLL
            delete lruNode;            // Free memory
        }

        // Case 3: Insert new node at MRU
        Node* newNode = new Node(key, value);
        cache[key] = newNode;
        addNode(newNode);
    }
};

int main() {
    LRUCache lru(2);
    lru.put(1, 1); // cache: {1=1}
    lru.put(2, 2); // cache: {2=2, 1=1}
    cout << lru.get(1) << "\n"; // returns 1, marks 1 as MRU: {1=1, 2=2}
    lru.put(3, 3); // evicts key 2! cache: {3=3, 1=1}
    cout << lru.get(2) << "\n"; // returns -1 (evicted)
    lru.put(4, 4); // evicts key 1! cache: {4=4, 3=3}
    cout << lru.get(1) << "\n"; // returns -1 (evicted)
    cout << lru.get(3) << "\n"; // returns 3
    cout << lru.get(4) << "\n"; // returns 4
    return 0;
}
```

---

## 🔍 Detailed Trace: Capacity Eviction

`capacity = 2`.
1. `put(1, 1)`: `head <-> [1:1] <-> tail`. `cache = {1}`.
2. `put(2, 2)`: `head <-> [2:2] <-> [1:1] <-> tail`. `cache = {1, 2}`.
3. `get(1)`: Removes `[1:1]` and adds to head: `head <-> [1:1] <-> [2:2] <-> tail`. Returns 1.
4. `put(3, 3)`: Full! `tail->prev` is `[2:2]` (LRU node).
   - `cache.erase(2)`.
   - `deleteNode([2:2])`.
   - Add `[3:3]` at head: `head <-> [3:3] <-> [1:1] <-> tail`.
5. `get(2)`: Not found in `cache` $\to$ Returns `-1`.

---

## 🧠 Mental Model: Desktop Documents

Think of your physical work desk:
- When you use a paper document (`get`), you pull it out and place it on top of the pile (`head`).
- When a new document arrives (`put`), you put it on top of the pile.
- When the desk is full, you grab the document from the very bottom of the pile (`tail->prev`) and shred it.

---

## ⚠️ Common Mistakes

1. **Not Storing `key` inside `Node`:** If `Node` only stores `val`, when evicting `tail->prev`, you cannot know which key to erase from the hash map (`cache.erase(lruNode->key)` requires the key!).
2. **Memory Leak on Eviction:** Removing `lruNode` from the list without calling `delete lruNode`.
3. **Forgetting to Update MRU on `get()`:** Calling `get(key)` must refresh its recency!

---

## 🖥️ System-Specific Notes

- Production caches (such as Redis and Linux page caches) use LRU or approximations like **Clock Page Replacement** to avoid pointer synchronization overhead under concurrent multi-threaded writes.

---

## 🟡 Additional Essential Context

In LeetCode 460 (LFU Cache - Least Frequently Used), nodes are evicted based on frequency of access first, with LRU breaking ties. This requires a map of frequencies to separate doubly linked lists.

---

## 🔥 Interview-Level Understanding

### 🎯 Core Concept Check

**Q1:** Why does the DLL require dummy `head` and `tail` nodes?  
**A:** Sentinel dummy nodes eliminate edge-case checks for empty lists or inserting/deleting at the very ends, guaranteeing that `addNode` and `deleteNode` execute in unconditionally safe $O(1)$ steps.

---

### 🔥 Interview Questions

#### Q1: Is this LRU Cache thread-safe? How would you make it thread-safe?
- **Short Answer:** No, it is not thread-safe.
- **Detailed Explanation:** Multiple threads calling `get()` or `put()` concurrently will cause race conditions when updating node pointers and the hash map. To make it thread-safe, guard all operations with a `std::mutex` or use a read-write lock (`std::shared_mutex`).

---

## 💻 Output / Debugging Questions

### Output Prediction
```cpp
// Capacity = 1
// lru.put(2, 1);
// lru.get(2); // returns 1
// lru.put(3, 2); // evicts 2
// lru.get(2); // returns -1
```

---

## Edge Cases

1. **Capacity 1:** Every new `put` immediately evicts the existing element.
2. **Updating Existing Key:** Does not evict; updates value and refreshes recency.

---

## Complexity Analysis

- **`get(key)`:** $O(1)$ average time.
- **`put(key, val)`:** $O(1)$ average time.
- **Space Complexity:** $O(\text{capacity})$ for storing up to `capacity` nodes and hash map entries.

---

## Key Takeaways

1. **Hash Map:** Gives $O(1)$ node lookup.
2. **Doubly Linked List:** Gives $O(1)$ node detachment and insertion.
3. **Store `key` in Node:** Necessary to erase the evicted key from the hash map.

---

## ⚡ 2-Minute Revision

- Structure: `unordered_map<int, Node*> cache` + DLL with `head` (MRU) and `tail` (LRU).
- `get()`: If found, `deleteNode(node); addNode(node); return node->val;`.
- `put()`: If full, evict `tail->prev` from map and DLL, then insert new node at head.
"""

print("Writing batch 4 linked list...")
for fn, content in notes.items():
    with open(os.path.join(t14_dir, fn), "w", encoding="utf-8") as f:
        f.write(content)
print("Updated 10, 11, 12 in Topic 14.")
