# Lecture 78: Implement LRU Cache: DLL + Hash Map $O(1)$ Design (LeetCode 146)

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
