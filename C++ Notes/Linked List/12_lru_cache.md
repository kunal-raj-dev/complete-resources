# 📖 Lecture 12: Implement LRU Cache | Linked List
> **Video Link:** [L76. Implement LRU Cache | Linked List](https://www.youtube.com/watch?v=GsY6y0iPaHw)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [146. LRU Cache](https://leetcode.com/problems/lru-cache/) (Medium / Hard Classic)  
> **Core Concepts:** LRU Eviction Policy, Doubly Linked List + Hash Map System Design, $O(1)$ Get & Put Operations

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Cache Kya Hota Hai?
Cache ek bohot fast aur limited capacity waali memory hoti hai jisme frequently accessed data store kiya jata hai taaki database ya disk par baar-baar na jana pade.

### LRU (Least Recently Used) Eviction Policy:
Jab cache ki capacity bhar jaati hai aur ek naya element add karna hota hai, toh kis element ko bahar nikala jaye?  
**LRU Policy:** *Us element ko bahar fenko (evict karo) jo sabse puraane samay se use nahi hua hai (Least Recently Used).*

```
Capacity = 3
1. put(1, 10)  -> Cache: [1]
2. put(2, 20)  -> Cache: [2, 1]
3. put(3, 30)  -> Cache: [3, 2, 1] (Cache full!)
4. get(1)      -> 1 was accessed! So 1 becomes Most Recently Used: [1, 3, 2]
5. put(4, 40)  -> 2 was Least Recently Used! Evict 2! -> Cache: [4, 1, 3]
```

### ⚡ The $O(1)$ Challenge:
Hume dono operations ko strictly **$O(1)$ average time** mein karna hai:
1. `get(key)`: $O(1)$
2. `put(key, value)`: $O(1)$

---

## 🏗️ 2. System Architecture: Why DLL + Hash Map?

| Data Structure | Lookup Time | Deletion Time | Insertion at Front/End | Can it do LRU in $O(1)$? |
|---|---|---|---|---|
| **Array / Vector** | $O(1)$ by index, $O(N)$ by key | $O(N)$ (Shifting) | $O(N)$ | ❌ No |
| **Singly Linked List** | $O(N)$ | $O(N)$ (Need prev) | $O(1)$ | ❌ No |
| **Hash Map Alone** | $O(1)$ | $O(1)$ | No order tracking | ❌ No (Order of access nahi pata) |
| **Doubly LL Alone** | $O(N)$ | $O(1)$ | $O(1)$ | ❌ No (Search slow hai) |
| **Hash Map + Doubly LL** | **$O(1)$** | **$O(1)$** | **$O(1)$** | **✅ YES! PERFECT COMBINATION!** |

### 🧩 Visual System Blueprint:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 unordered_map<int, Node*>              │
                  │   Key 1 ──► Node(1)   Key 2 ──► Node(2)   Key 3 ──► Node(3)
                  └─────┬───────────────────┬───────────────────┬──────────┘
                        │                   │                   │
                        ▼                   ▼                   ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
    │  head    │◄═══►│  Node(1) │◄═══►│  Node(3) │◄═══►│  Node(2) │◄═══►│  tail    │
    │ (Dummy)  │     │  (MRU)   │     │          │     │  (LRU)   │     │ (Dummy)  │
    └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

- **Dummy `head` & `tail` Sentinel Nodes:** Edge cases (empty list, single element) ko simplify karte hain.
- **MRU (Most Recently Used):** Hamesha `head` ke theek aage (`head->next`) rakhenge.
- **LRU (Least Recently Used):** Hamesha `tail` ke theek piche (`tail->prev`) rakhenge.

---

## 🛠️ 3. The 2 Building-Block Helper Primitives

Humare code mein sirf do fundamental pointer helpers ki zaroorat hai:

### Helper 1: `addNode(Node* newNode)`
Node ko hamesha **MRU position (`head` ke theek baad)** par insert karo:
```cpp
void addNode(Node* newNode) {
    Node* temp = head->next;
    newNode->next = temp;
    newNode->prev = head;
    head->next = newNode;
    temp->prev = newNode;
}
```

### Helper 2: `deleteNode(Node* delNode)`
Node ko DLL se hata do ($O(1)$ directly using `prev` and `next`):
```cpp
void deleteNode(Node* delNode) {
    Node* prevNode = delNode->prev;
    Node* nextNode = delNode->next;
    prevNode->next = nextNode;
    nextNode->prev = prevNode;
}
```

---

## ⚙️ 4. Operation Mechanics: `get` & `put`

### `get(key)`:
1. Check karo kya key map mein exist karti hai?
   - Agar nahi: Return `-1`.
2. Agar exist karti hai:
   - Map se us node ka address lo: `Node* resNode = mp[key];`
   - Use current position se delete karo: `deleteNode(resNode);`
   - Use `head` ke baad insert karo taaki wo **MRU ban jaye**: `addNode(resNode);`
   - Return karo uski value: `return resNode->val;`

---

### `put(key, value)`:
1. **Agar key already cache mein exist karti hai:**
   - Existing node ka value update karo.
   - Use delete karke MRU position par add karo (`deleteNode`, `addNode`).
2. **Agar key nayi hai:**
   - **Check Capacity:** Agar cache already full hai (`mp.size() == cap`):
     - LRU node nikalo (`tail->prev`).
     - Map se erase karo: `mp.erase(lruNode->key);`
     - DLL se delete karo: `deleteNode(lruNode);`
     - Heap memory free karo: `delete lruNode;`
   - Naya node banao: `Node* newNode = new Node(key, value);`
   - Use MRU position par insert karo: `addNode(newNode);`
   - Map mein add karo: `mp[key] = newNode;`

---

## 💻 5. Complete C++ Implementation (LeetCode Standard)

```cpp
#include <unordered_map>
using namespace std;

class LRUCache {
private:
    class Node {
    public:
        int key;
        int val;
        Node* prev;
        Node* next;

        Node(int _key, int _val) {
            key = _key;
            val = _val;
            prev = nullptr;
            next = nullptr;
        }
    };

    Node* head;
    Node* tail;
    int cap;
    unordered_map<int, Node*> mp;

    // Helper: Add node right after head (MRU)
    void addNode(Node* newNode) {
        Node* temp = head->next;
        newNode->next = temp;
        newNode->prev = head;
        head->next = newNode;
        temp->prev = newNode;
    }

    // Helper: Delete node from DLL
    void deleteNode(Node* delNode) {
        Node* prevNode = delNode->prev;
        Node* nextNode = delNode->next;
        prevNode->next = nextNode;
        nextNode->prev = prevNode;
    }

public:
    LRUCache(int capacity) {
        cap = capacity;
        head = new Node(-1, -1); // Dummy head
        tail = new Node(-1, -1); // Dummy tail
        head->next = tail;
        tail->prev = head;
    }

    ~LRUCache() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* nextNode = curr->next;
            delete curr;
            curr = nextNode;
        }
    }

    int get(int key) {
        if (mp.find(key) != mp.end()) {
            Node* resNode = mp[key];
            int res = resNode->val;

            // Make it Most Recently Used
            deleteNode(resNode);
            addNode(resNode);

            return res;
        }
        return -1;
    }

    void put(int key, int value) {
        // Case 1: Key already exists -> Update and move to MRU
        if (mp.find(key) != mp.end()) {
            Node* existingNode = mp[key];
            existingNode->val = value;

            deleteNode(existingNode);
            addNode(existingNode);
            return;
        }

        // Case 2: Cache is full -> Evict LRU
        if (mp.size() == cap) {
            Node* lru = tail->prev;
            mp.erase(lru->key);
            deleteNode(lru);
            delete lru; // Free memory
        }

        // Case 3: Insert new node at MRU
        Node* newNode = new Node(key, value);
        addNode(newNode);
        mp[key] = newNode;
    }
};
```

**Complexity Analysis:**
- **`get(key)`:** $O(1)$ average time.
- **`put(key, value)`:** $O(1)$ average time.
- **Space Complexity:** $O(\text{capacity})$ — Hash map and DLL nodes store at most `capacity` elements.

---

## 🧪 6. Edge Cases & Interview Pitfalls

1. **Why store `key` inside `Node`?**
   - Jab hum LRU node (`tail->prev`) ko evict karte hain, toh hume use hash map se bhi hatana hota hai: `mp.erase(lru->key)`. Agar node ke paas apni key nahi hogi, toh hum map se use $O(1)$ mein delete nahi kar payenge!
2. **Sentinel Dummy Nodes:**
   - Dummy `head` aur `tail` hone se kabhi bhi `head == nullptr` ya `tail == nullptr` ki if-conditions nahi likhni padti.
3. **Memory Leaks:**
   - Evicted nodes ko `delete` karna zaroori hai. Destructor mein saare allocated nodes free hone chahiye.

---

## ⚡ 7. 1-Minute Revision Cheat Sheet

- **Data Structures:** `unordered_map<int, Node*>` + Doubly Linked List with dummy `head` and `tail`.
- **MRU:** Right after `head` (`head->next`).
- **LRU:** Right before `tail` (`tail->prev`).
- **`get(key)`:** If exists $\implies$ `deleteNode` $\to$ `addNode` at head $\to$ return value.
- **`put(key, val)`:**
  - If exists $\implies$ update val $\to$ `deleteNode` $\to$ `addNode` at head.
  - If full $\implies$ remove `tail->prev` from map & DLL $\to$ add new node at head.
- **Complexity:** Strictly $O(1)$ Time for both operations.
