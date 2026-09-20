# 📖 Lecture 03: Middle of a Linked List | DSA Series
> **Video Link:** [Middle of a Linked List | DSA Series](https://www.youtube.com/watch?v=nzaHG0dme4g)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) (Easy)  
> **Core Concept:** Tortoise and Hare Algorithm (Slow & Fast Pointer Pattern)

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Problem Statement:
Hume ek singly linked list ka `head` diya gaya hai. Hume list ka **middle node** find karke uska reference return karna hai.
- Agar list ki length **Odd (Visham)** hai: Exactly ek middle node hoga (e.g. `[1, 2, 3, 4, 5]` -> Middle is `3`).
- Agar list ki length **Even (Sam)** hai: Do middle nodes honge (e.g. `[1, 2, 3, 4, 5, 6]` -> Middles are `3` and `4`).
  - Standard LeetCode / Interview convention: **Second middle node** (`4`) return karna hota hai.

```
Odd Length:   [1] ──► [2] ──► [3] ──► [4] ──► [5] ──► NULL
                              ▲
                            Middle

Even Length:  [1] ──► [2] ──► [3] ──► [4] ──► [5] ──► [6] ──► NULL
                                      ▲
                                 Second Middle
```

---

## 🧭 2. Approach 1: Two-Pass (Count Method)

### Intuition:
1. **Pass 1:** List ko `head` se lekar end tak traverse karo aur total nodes count karo ($N$).
2. **Pass 2:** Middle index hoga `N / 2`. `head` se dobara start karo aur `N / 2` steps aage badho.

```cpp
class Solution {
public:
    ListNode* middleNode(ListNode* head) {
        int count = 0;
        ListNode* temp = head;
        while (temp != nullptr) {
            count++;
            temp = temp->next;
        }

        int mid = count / 2;
        temp = head;
        for (int i = 0; i < mid; i++) {
            temp = temp->next;
        }
        return temp;
    }
};
```

**Complexity:**
- **Time Complexity:** $O(N) + O(N/2) = O(N)$ (Two passes).
- **Space Complexity:** $O(1)$.

> ⚠️ **Interview Note:** Interviewer aapse kahega: *"Can you do it in a single pass?"* Yahi se entry hoti hai **Slow & Fast Pointer** algorithm ki!

---

## 🐢🐇 3. Approach 2: Slow & Fast Pointers (Tortoise & Hare) - Optimal

### Real-World Physics Analogy:
Maan lo do runners ek track par daud rahe hain:
- **Runner 1 (Slow / Tortoise):** Speed = $1\text{ step/sec}$
- **Runner 2 (Fast / Hare):** Speed = $2\text{ steps/sec}$

Jab Fast runner finish line ($D$) par pahuchega, tab Slow runner track ke theek **aadhe raste ($D / 2$)** par hoga!

### Pointer Setup:
- `ListNode* slow = head;` (Moves 1 step at a time: `slow = slow->next`)
- `ListNode* fast = head;` (Moves 2 steps at a time: `fast = fast->next->next`)

---

## 📊 4. Visual Dry Run: Odd vs Even Length

### Case A: Odd Length `[1 -> 2 -> 3 -> 4 -> 5 -> NULL]`

#### Step 0 (Initial):
```
 slow, fast
     │
     ▼
   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► NULL
```

#### Step 1:
- `slow` moves 1 step -> Node 2
- `fast` moves 2 steps -> Node 3
```
             slow                fast
              │                   │
              ▼                   ▼
   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► NULL
```

#### Step 2:
- `slow` moves 1 step -> Node 3
- `fast` moves 2 steps -> Node 5
```
                         slow                                fast
                          │                                   │
                          ▼                                   ▼
   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► NULL
```
- Ab `fast->next == NULL` hai! Loop ruk jayega!
- **Result:** `slow` is at **Node 3** (Perfect middle!).

---

### Case B: Even Length `[1 -> 2 -> 3 -> 4 -> 5 -> 6 -> NULL]`

#### Step 0 (Initial):
```
 slow, fast
     │
     ▼
   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► [ 6 ] ──► NULL
```

#### Step 1:
- `slow` -> Node 2
- `fast` -> Node 3

#### Step 2:
- `slow` -> Node 3
- `fast` -> Node 5

#### Step 3:
- `slow` -> Node 4
- `fast` -> NULL (2 steps beyond Node 5: 5->6->NULL)
```
                                 slow                                                fast
                                  │                                                   │
                                  ▼                                                   ▼
   [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► [ 6 ] ──► NULL
```
- Ab `fast == NULL` hai! Loop ruk jayega!
- **Result:** `slow` is at **Node 4** (Second middle!).

---

## 💻 5. Optimal C++ Code

```cpp
class Solution {
public:
    ListNode* middleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;

        // Loop condition handles both odd and even lengths:
        // fast != nullptr       -> checks for even length termination
        // fast->next != nullptr -> checks for odd length termination
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;          // 1 step
            fast = fast->next->next;    // 2 steps
        }

        return slow;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N/2) = O(N)$ — Exactly single pass (fast pointer traverses $N$ nodes in $N/2$ iterations).
- **Space Complexity:** $O(1)$ — Only two pointers used.

---

## 🎯 6. Special Interview Variation: "What if we want the FIRST middle in Even Length?"

Agar interviewer bole:
> *"For `[1, 2, 3, 4, 5, 6]`, I want Node `3` (First Middle) instead of Node `4` (Second Middle), how will you modify the code?"*

### Solution:
Loop condition ko modify karo:
```cpp
while (fast->next != nullptr && fast->next->next != nullptr) {
    slow = slow->next;
    fast = fast->next->next;
}
```
**Dry run on `[1, 2, 3, 4, 5, 6]`:**
- At Step 2: `slow` is at `3`, `fast` is at `5`.
- `fast->next` is `6`, but `fast->next->next` is `NULL`!
- Loop breaks immediately! `slow` stops at Node `3`!

---

## 🧪 7. Edge Cases & Interview Pitfalls

1. **Empty List (`head == nullptr`):**
   - Agar head null ho sakta hai, toh pehle check karo `if (!head) return nullptr;`.
2. **Single Node (`head->next == nullptr`):**
   - `fast->next` is NULL, loop breaks immediately, returns `slow` (head itself). Correct!
3. **Two Nodes (`[1 -> 2 -> NULL]`):**
   - Iteration 1: `slow` moves to `2`, `fast` moves to `NULL`.
   - Loop terminates, returns Node `2`. Correct!
4. **Null Pointer Dereference Bug:**
   - Hamesha condition ka order dhyan rakho: `while (fast != nullptr && fast->next != nullptr)`.
   - Agar aapne `while (fast->next != nullptr && fast != nullptr)` likh diya, toh `fast == NULL` hone par `fast->next` check karne par **crash (segfault)** ho jayega!

---

## ⚡ 8. 1-Minute Revision Cheat Sheet

- **Pattern:** Slow & Fast Pointer (Tortoise and Hare).
- **Movement:** `slow` moves 1 step, `fast` moves 2 steps.
- **Stopping Condition for 2nd Middle:** `while (fast != NULL && fast->next != NULL)`
- **Stopping Condition for 1st Middle:** `while (fast->next != NULL && fast->next->next != NULL)`
- **Complexity:** $O(N)$ Time, $O(1)$ Space, Single Pass.
