# 📖 Lecture 06: Copy List with Random Pointer | DSA Series
> **Video Link:** [Copy List with Random Pointer | DSA Series](https://www.youtube.com/watch?v=8ze7Zopdsaw)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) (Medium)  
> **Core Concepts:** Deep Copy vs Shallow Copy, Hash Map Mapping, In-Place Interleaving Technique ($O(1)$ Space)

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Node Anatomy:
Is problem mein standard Node ke paas ek extra pointer hota hai:
```cpp
class Node {
public:
    int val;
    Node* next;
    Node* random;   // Points to any random node in the list or NULL
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
```

### Shallow Copy vs Deep Copy:
- **Shallow Copy:** Agar hum sirf naye pointer banakar puraane nodes ko point karwa dein (`Node* copyHead = head;`), toh original list modify hone par copy bhi change ho jayegi.
- **Deep Copy:** Hume bilkul naye memory blocks (nodes) allocate karne hain. Nayi list ka koi bhi pointer (`next` ya `random`) puraani list ke kisi bhi node ko point **nahi** karna chahiye!

### ❓ The Core Dilemma:
Jab hum pehla node `A` clone karte hain, toh uska `random` pointer maan lo aakhiri node `Z` ko point kar raha hai.  
Par `Z` toh abhi bana hi nahi hai! Toh hum `A'` ka `random` kisko point karwayenge?

---

## 🗺️ 2. Approach 1: Hash Map Method ($O(N)$ Space)

### Intuition:
Hum ek dictionary / hash map use kar sakte hain: `unordered_map<Node*, Node*> oldToNew;`  
Jo har puraane node ke address ko uske naye clone node ke address se map karegi.

### 2-Pass Algorithm:
1. **Pass 1 (Create Clones):**
   - List traverse karo. Har `curr` ke liye ek `new Node(curr->val)` banao.
   - Map mein store karo: `oldToNew[curr] = new Node(curr->val);`
   - Map automatically `oldToNew[nullptr] = nullptr;` handle karega.
2. **Pass 2 (Connect Pointers):**
   - Wapas list traverse karo:
   - `oldToNew[curr]->next = oldToNew[curr->next];`
   - `oldToNew[curr]->random = oldToNew[curr->random];`
3. Return `oldToNew[head]`.

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;

        unordered_map<Node*, Node*> oldToNew;

        // Pass 1: Create nodes
        Node* curr = head;
        while (curr != nullptr) {
            oldToNew[curr] = new Node(curr->val);
            curr = curr->next;
        }

        // Pass 2: Connect next and random pointers
        curr = head;
        while (curr != nullptr) {
            oldToNew[curr]->next = oldToNew[curr->next];
            oldToNew[curr]->random = oldToNew[curr->random];
            curr = curr->next;
        }

        return oldToNew[head];
    }
};
```
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N)$ (Hash map for $N$ nodes)

---

## ⚡ 3. Approach 2: In-Place Interleaving Technique ($O(1)$ Space) - Optimal

Ye FAANG interviews ka **hero approach** hai. Bina kisi hash map ke hum $O(1)$ auxiliary space mein deep copy create karte hain!

### 3-Step Master Strategy:

```
Original:
[ A ] ──────────────► [ B ] ──────────────► [ C ] ──► NULL
```

#### Step 1: Interleave Cloned Nodes
Har original node ke theek aage uska clone node ghusaa (insert) do:
```
[ A ] ──► [ A' ] ──► [ B ] ──► [ B' ] ──► [ C ] ──► [ C' ] ──► NULL
```
- Code:
  ```cpp
  Node* copy = new Node(curr->val);
  copy->next = curr->next;
  curr->next = copy;
  curr = copy->next;
  ```

#### Step 2: Connect Random Pointers of Cloned Nodes
Notice karein:
- Agar `curr->random` kisi node `X` ko point kar raha hai...
- Toh `X` ka clone `X'` theek `X->next` par baitha hai!
- Iska matlab:
  $$\text{curr->next->random} = \text{curr->random->next}$$

```
If A->random is C:
[ A ] ──► [ A' ] ──► [ B ] ──► [ B' ] ──► [ C ] ──► [ C' ]
  │                                         ▲
  └────────────── random ───────────────────┘
Therefore:
A'->random will point to C->next (which is C')!
```

#### Step 3: Separate Both Lists (Restore Original & Extract Cloned)
Dono lists ko aapas mein alag alag (de-interleave) kar do taaki original list wapas normal ho jaye aur cloned list nikal aaye:
```cpp
curr->next = copy->next;
if (copy->next != nullptr) {
    copy->next = copy->next->next;
}
```

---

## 💻 4. Complete C++ Code (Optimal $O(1)$ Space)

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;

        // Step 1: Insert cloned nodes next to original nodes
        Node* curr = head;
        while (curr != nullptr) {
            Node* copy = new Node(curr->val);
            copy->next = curr->next;
            curr->next = copy;
            curr = copy->next;
        }

        // Step 2: Assign random pointers for cloned nodes
        curr = head;
        while (curr != nullptr) {
            Node* copy = curr->next;
            if (curr->random != nullptr) {
                copy->random = curr->random->next;
            } else {
                copy->random = nullptr;
            }
            curr = copy->next;
        }

        // Step 3: Separate the two lists
        curr = head;
        Node* cloneHead = head->next;
        Node* copyCurr = cloneHead;

        while (curr != nullptr) {
            curr->next = curr->next->next;
            if (copyCurr->next != nullptr) {
                copyCurr->next = copyCurr->next->next;
            }
            curr = curr->next;
            copyCurr = copyCurr->next;
        }

        return cloneHead;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — 3 linear passes ($3N \approx O(N)$).
- **Space Complexity:** $O(1)$ — Koi hash map use nahi hua, only pointer manipulation.

---

## 🧪 5. Edge Cases & Interview Pitfalls

1. **Empty List (`head == nullptr`):**
   - Pehle hi return `nullptr`.
2. **`random == nullptr`:**
   - Step 2 mein hamesha check karo `if (curr->random != nullptr)` before accessing `curr->random->next`. Warna crash ho jayega!
3. **Self-Referential Random Pointer (`A->random = A`):**
   - Formula `copy->random = curr->random->next` flawlessly points `A'` to `A->next` (which is `A'`).
4. **Original List Mutation:**
   - Interviewer hamesha check karega ki kya aapne Step 3 mein original list ko uski original state mein restore kiya ya nahi. Interleaved list ko as-it-is chhodna negative points deta hai.

---

## ⚡ 6. 1-Minute Revision Cheat Sheet

- **Problem:** Clone list with `val`, `next`, and arbitrary `random`.
- **Approach 1:** Hash Map `oldToNew`, 2 passes, $O(N)$ time, $O(N)$ space.
- **Approach 2 (Optimal):**
  - **Step 1:** Interleave clones (`A -> A' -> B -> B'`).
  - **Step 2:** Assign randoms: `curr->next->random = curr->random ? curr->random->next : NULL`.
  - **Step 3:** Separate lists and restore original.
  - **Complexity:** $O(N)$ Time, $O(1)$ Space.
