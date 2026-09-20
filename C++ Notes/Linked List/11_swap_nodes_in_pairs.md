# 📖 Lecture 11: Swap Nodes in Pairs | Linked List
> **Video Link:** [Swap Nodes in Pairs | Linked List](https://www.youtube.com/watch?v=wwbTMNVlFHQ)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [24. Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) (Medium)  
> **Core Concepts:** 2-Node Pointer Swapping, Dummy Node Pattern, Recursive Subproblems

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Problem Statement:
Hume ek singly linked list ka `head` diya gaya hai. Hume har do adjacent (bagal-bagal waale) nodes ko aapas mein swap karna hai aur modified list ka naya `head` return karna hai.

- **Strict Constraint:** Node values ko modify karna strictly prohibited hai (`swap(n1->val, n2->val)` is NOT allowed). Sirf pointers ko rewire karna hai!

```
Input:   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► NULL
Output:  [ 2 ] ──► [ 1 ] ──► [ 4 ] ──► [ 3 ] ──► NULL

Odd Length Input:   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► NULL
Output:             [ 2 ] ──► [ 1 ] ──► [ 3 ] ──► NULL  (3 remains as is!)
```

### 💡 The Big Picture:
Ye problem darasal **Lecture 10 (Reverse Nodes in K-Group)** ka hi ek special case hai jaha **$k = 2$** hai!  
Lekin kyunki $k = 2$ fixed hai, hume koi bada loop chalane ki zaroorat nahi hai; hum directly do nodes ke pointers ko swap kar sakte hain.

---

## 🧭 2. Approach 1: Iterative with Dummy Node (Optimal $O(1)$ Space)

### Pointers Setup:
1. `dummy`: Result list ke head ko hold karne ke liye.
2. `prev`: Current pair ke piche waala node (initially `&dummy`).
3. `first`: Pair ka pehla node (`prev->next`).
4. `second`: Pair ka doosra node (`first->next`).

### 🔄 The 3-Line Pointer Swap:
Maan lo hum `first` (Node 1) aur `second` (Node 2) ko swap kar rahe hain:
```cpp
first->next = second->next; // 1. Node 1 ko Node 3 se connect karo
second->next = first;       // 2. Node 2 ko Node 1 se connect karo
prev->next = second;        // 3. Pichle group ko Node 2 se connect karo
```

Uske baad agle pair ke liye `prev` ko aage badhao:
```cpp
prev = first; // Kyunki swap ke baad 'first' ab is pair ka aakhiri node hai!
```

---

## 📊 3. Visual Pointer Dry Run

List: `[ 1 -> 2 -> 3 -> 4 -> NULL ]`

```
Initial Setup:
dummy [ 0 ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► NULL
    ▲             ▲         ▲
  prev          first     second

Step 1: first->next = second->next (1 points to 3)
[ 1 ] ────────────────────────► [ 3 ] ──► [ 4 ]
  ▲                               ▲
  │                               │
  └───────────┐                   │
              │                   │
[ 2 ] ────────┘                   │
  ▲                               │
second                            │

Step 2: second->next = first (2 points to 1)
[ 2 ] ──► [ 1 ] ──────────────► [ 3 ] ──► [ 4 ]

Step 3: prev->next = second (dummy points to 2)
dummy ──► [ 2 ] ──► [ 1 ] ────► [ 3 ] ──► [ 4 ]
                      ▲
                    prev (prev moves to first for next iteration)
```

Ab agle pair `[3, 4]` par same steps repeat honge:
`dummy ──► [ 2 ] ──► [ 1 ] ──► [ 4 ] ──► [ 3 ] ──► NULL`

---

## 💻 4. Optimal C++ Code (Iterative)

```cpp
class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        // Base case: Empty list or single node
        if (!head || !head->next) return head;

        ListNode dummy(0);
        dummy.next = head;
        ListNode* prev = &dummy;

        // Loop runs as long as there is a pair available to swap
        while (prev->next != nullptr && prev->next->next != nullptr) {
            ListNode* first = prev->next;
            ListNode* second = first->next;

            // 3-step pointer rewiring
            first->next = second->next;
            second->next = first;
            prev->next = second;

            // Move prev to the end of swapped pair
            prev = first;
        }

        return dummy.next;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — Har node ko exact 1 baar visit kiya.
- **Space Complexity:** $O(1)$ — Only a few pointer variables.

---

## 🔄 5. Approach 2: Recursive Solution

Recursion is extremely clean here:
- Agar pair exist karta hai (`head` and `head->next`):
  - `first = head`, `second = head->next`
  - Bachi hui list (`second->next`) par recursion call karo:
    `first->next = swapPairs(second->next);`
  - Current pair swap karo:
    `second->next = first;`
  - Return `second` (jo is pair ka naya head ban chuka hai).

```cpp
class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        // Base case: 0 or 1 node
        if (!head || !head->next) return head;

        ListNode* first = head;
        ListNode* second = head->next;

        // Recursive call for next pairs
        first->next = swapPairs(second->next);

        // Swap current pair
        second->next = first;

        return second;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(N / 2) = O(N)$ (Recursion stack).

---

## 🧪 6. Edge Cases & Interview Pitfalls

1. **Empty List (`head == nullptr`):** Returns `nullptr`.
2. **Single Node (`head->next == nullptr`):** Returns `head` directly without any swap.
3. **Odd Length List:**
   - Aakhiri node ka koi partner nahi hoga.
   - Condition `while (prev->next != nullptr && prev->next->next != nullptr)` gracefully terminates when only 1 node remains, leaving it unchanged.
4. **Order of pointer updates:**
   - Agar aapne `second->next = first` pehle kar diya bina `first->next` ko save kiye, toh aage ki puri list ka reference lose ho jayega!

---

## ⚡ 7. 1-Minute Revision Cheat Sheet

- **Special Case of:** Reverse in K-Group with $k = 2$.
- **Iterative Strategy:**
  - `first = prev->next`, `second = first->next`
  - `first->next = second->next;`
  - `second->next = first;`
  - `prev->next = second;`
  - `prev = first;`
- **Recursive Strategy:**
  - `first->next = swapPairs(second->next);`
  - `second->next = first;`
  - `return second;`
- **Complexity:** $O(N)$ Time, $O(1)$ Space (Iterative).
