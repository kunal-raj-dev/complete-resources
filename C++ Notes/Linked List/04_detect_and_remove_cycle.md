# 📖 Lecture 04: Detect & Remove Cycle in Linked List | DSA Series

> **Video Link:** [Detect &amp; Remove Cycle in Linked List | DSA Series](https://www.youtube.com/watch?v=-1E8ZMS0gSs)**Instructor:** Shradha Khapra**LeetCode Problems:**
>
> - [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) (Easy)
> - [142. Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) (Medium)
>   **Core Concepts:** Floyd’s Cycle Detection (Tortoise & Hare), Mathematical Proof of Meeting Point, Cycle Removal

---

## 🎯 1. Concept Ki Baat: Cycle Kya Hoti Hai?

Normal linked list mein last node ka `next` pointer `NULL` ko point karta hai.
Lekin agar kisi node ka `next` pointer wapas list ke kisi puraane node ko point karne lage, toh ek **Closed Loop (Cycle)** ban jaata hai.

```
       1 ──► 2 ──► 3 ──► 4 ──► 5
                   ▲           │
                   │           ▼
                   8 ◄── 7 ◄── 6   <-- Cycle exists (3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 3)
```

**Khatra (Danger):** Agar hum normal `while (curr != NULL)` loop chalayenge, toh code **Infinite Loop** mein fas jayega aur kabhi terminate nahi hoga!

---

## 🔍 2. Part 1: Cycle Detect Kaise Karein? (LeetCode 141)

### Approach 1: Hash Set (Brute Force)

- Har node ko visit karte waqt uske address ko `unordered_set<ListNode*>` mein store karo.
- Agar koi node already set mein exist karta hai, toh **Cycle Detected**!
- **Time:** $O(N)$, **Space:** $O(N)$ (Hash Set memory).

---

### Approach 2: Floyd's Cycle-Finding Algorithm (Optimal $O(1)$ Space)

Floyd's algorithm uses two pointers:

- `slow` (moves 1 step at a time)
- `fast` (moves 2 steps at a time)

### ❓ Question: Kya Slow aur Fast hamesha milenge agar cycle hai?

**Answer:** **Haan, 100% Guaranteed!**

- **Relative Speed Concept:**
  - `fast` har step mein `slow` se $2 - 1 = 1$ step zyada chal raha hai.
  - Maan lo jab `slow` cycle mein enter karta hai, tab dono ke beech ka distance $D$ hai.
  - Agle step mein distance $D - 1$ hoga, fir $D - 2$, ... aur aakhir mein distance $0$ ho jayega (yaani dono same node par aa jayenge).
  - Iska matlab `fast` kabhi bhi `slow` ko jump over nahi kar sakta, wo use catch karega hi!

```
Condition:
if (slow == fast) -> Cycle Hai (True)
if (fast == NULL || fast->next == NULL) -> Cycle Nahi Hai (False)
```

### 💻 Code: Cycle Detection (LeetCode 141)

```cpp
class Solution {
public:
    bool hasCycle(ListNode *head) {
        ListNode* slow = head;
        ListNode* fast = head;

        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;

            if (slow == fast) {
                return true; // Cycle detected!
            }
        }

        return false; // Reached NULL, no cycle
    }
};
```

- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

---

## 📍 3. Part 2: Starting Node of Cycle (LeetCode 142)

Jab `slow` aur `fast` mil jaate hain (Meeting Point), toh question ye banta hai: **Cycle shuru kis node se hui thi?** (e.g., node 3 in the diagram).

### 📐 Mathematical Proof (FAANG Interview Favorite):

```
       head                   Cycle Start (Entry)
        │                            │
        ▼                            ▼
        ● ──► ● ──► ● ──► ... ──► [ Node S ] ──► ● ──► ● ──► [ Meeting Point M ]
        │◄──────── L ───────────►││◄──────── d ────────►│
                                   │                      │
                                   └──◄── (C - d) ◄───────┘
```

Let:

- $L$ = Distance from `head` to Cycle Start ($S$).
- $d$ = Distance from Cycle Start ($S$) to Meeting Point ($M$).
- $C$ = Total length / circumference of the cycle.
- $k$ = Number of complete loops `fast` made inside the cycle before meeting.

**Distances Traveled when they meet:**

- $\text{Distance by Slow} = L + d$
- $\text{Distance by Fast} = L + k \cdot C + d$

Since Fast moves at twice the speed of Slow:

$$
\text{Distance by Fast} = 2 \times \text{Distance by Slow}
$$

$$
L + k \cdot C + d = 2(L + d)
$$

$$
L + k \cdot C + d = 2L + 2d
$$

$$
k \cdot C = L + d
$$

$$
L = k \cdot C - d
$$

$$
L = (k - 1)C + (C - d)
$$

### 💡 The Golden Insight:

- $L$ = `head` se cycle start tak ka distance.
- $(C - d)$ = `meeting point` se aage cycle start tak ka bacha hua distance.
- $(k - 1)C$ = Simply means fast cycle ke kuch rounds complete karega.

**Toh Algorithm kya bani?**

1. Jaise hi `slow == fast` ho (Meeting Point $M$ par), ek pointer ko wapas `head` par le aao:`slow = head;`
2. `fast` ko wahin meeting point $M$ par rehne do.
3. Ab dono ko **1 step at a time** aage badhao:
   ```cpp
   while (slow != fast) {
       slow = slow->next;
       fast = fast->next;
   }
   ```
4. Jis node par wo milenge, wahi **Starting Node of the Cycle** hoga!

---

### 💻 Code: Find Cycle Start (LeetCode 142)

```cpp
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode* slow = head;
        ListNode* fast = head;
        bool hasCycle = false;

        // Step 1: Detect cycle and find meeting point
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle) return nullptr; // No cycle

        // Step 2: Reset slow to head, move both 1 step at a time
        slow = head;
        while (slow != fast) {
            slow = slow->next;
            fast = fast->next;
        }

        // Both meet at the start of cycle
        return slow;
    }
};
```

- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

---

## ✂️ 4. Part 3: Cycle Ko Remove (Break) Kaise Karein?

Cycle remove karne ka matlab hai: **Last node ke `next` pointer ko `NULL` set karna.**

### Algorithm:

1. Cycle ka starting node find karo (`startNode`).
2. Starting node se traverse karte hue cycle ke last node tak jao (wo node jiska `next == startNode`).
3. Us last node ka `next = nullptr` kar do!

### 💻 Code: Complete Cycle Removal Function

```cpp
void removeCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    bool hasCycle = false;

    // Step 1: Detect cycle
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            hasCycle = true;
            break;
        }
    }

    if (!hasCycle) return; // No cycle to remove

    // Step 2: Find cycle start
    slow = head;

    // Special Edge Case: Agar cycle head node par hi start ho rahi ho!
    if (slow == fast) {
        while (fast->next != slow) {
            fast = fast->next;
        }
        fast->next = nullptr; // Cycle broken
        return;
    }

    // Normal case: Find start node and the node just before it in the cycle
    ListNode* prev = nullptr;
    while (slow != fast) {
        prev = fast;       // prev tracks the node before fast
        slow = slow->next;
        fast = fast->next;
    }

    // Ab slow (aur fast) cycle start par hain, aur prev last node par hai
    prev->next = nullptr; // Cycle broken!
}
```

---

## 🧪 5. Edge Cases & Interview Pitfalls

1. **No Cycle (`fast == NULL || fast->next == NULL`):**
   - Hamesha safe exit karo bina pointer dereference error ke.
2. **Cycle Starts at `head` (`L = 0`):**
   - Agar cycle `head` par hi start ho (e.g. `1 -> 2 -> 3 -> 1`), toh meeting point ke baad `slow = head` karne par `slow == fast` initially hi true ho jayega!
   - Is special case ko handle karne ke liye alag se check karo (jaisa upar code mein dikhaya gaya hai).
3. **Single Node without cycle vs Single Node with self-loop (`1 -> 1`):**
   - Self loop mein `fast->next->next` wahi node hai, algorithm safely detect karti hai.

---

## ⚡ 6. 1-Minute Revision Cheat Sheet

- **Detection:** `slow` (1 step), `fast` (2 steps). If `slow == fast` $\implies$ Cycle exists!
- **Find Start:** Meeting point ke baad `slow = head;`. Both move 1 step until `slow == fast`.
- **Remove Cycle:** Find last node in cycle whose `next == startNode`, set `last->next = nullptr`.
- **Time:** $O(N)$, **Space:** $O(1)$ strictly.
- **Interview Formula:** $L = (k-1)C + (C - d)$.
