# 📖 Lecture 02: Reverse a Linked List | DSA Series
> **Video Link:** [Reverse a Linked List | DSA Series](https://www.youtube.com/watch?v=R-CKBYnOv1U)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) (Easy)  
> **Prerequisites:** Singly Linked List Basics, Pointers, Recursion

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Problem Statement:
Hume ek singly linked list di gayi hai jiska head pointer `head` hai. Hume is linked list ke pointers ko reverse (ulta) karna hai aur naya `head` return karna hai.

```
Input:   1 ──► 2 ──► 3 ──► 4 ──► 5 ──► NULL
Output:  5 ──► 4 ──► 3 ──► 2 ──► 1 ──► NULL
```

### 🧠 The Core Idea:
Linked list mein arrows (`next` pointers) aage ki taraf point kar rahe hote hain:
`Node A ──► Node B`
Hume har arrow ko piche ki taraf modna hai:
`Node A ◄── Node B`

Par dhyan rahe: Jaise hi aap `curr->next` ko ulta modoge, aapka **aage ki list ka connection toot jayega!**  
Isliye aage badhne se pehle aage waale node ka address ek temporary pointer (`next_node`) mein store karna zaroori hai.

---

## 🧭 2. Approach 1: Iterative 3-Pointer Technique (Optimal)

Ye interview ka **most preferred** approach hai kyunki isme $O(1)$ auxiliary space lagta hai.

### 3 Pointers Setup:
1. `prev`: Current node ke piche waala node (initially `nullptr`).
2. `curr`: Current node jiske arrow ko hum mod rahe hain (initially `head`).
3. `next_node`: Aage waala node taaki list ka reference na khoye (initially `nullptr`).

### 🔄 The 4-Step Golden Loop:
Har iteration mein bas ye 4 lines execute hoti hain:
```cpp
next_node = curr->next;   // Step 1: Save ahead (aage ka raasta bacha lo)
curr->next = prev;        // Step 2: Reverse link (arrow piche ghuma do)
prev = curr;              // Step 3: Move prev forward (prev ko ek kadam aage badhao)
curr = next_node;         // Step 4: Move curr forward (curr ko ek kadam aage badhao)
```

---

## 📊 3. Visual Pointer Dry Run (Step-by-Step)

Maan lo list hai: `1 -> 2 -> 3 -> NULL`

#### Initial State:
```
 prev        curr
  │           │
  ▼           ▼
 NULL        [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► NULL
```

#### Iteration 1:
1. `next_node = curr->next` (`next_node` points to `2`)
2. `curr->next = prev` (`1` points to `NULL`)
3. `prev = curr` (`prev` points to `1`)
4. `curr = next_node` (`curr` points to `2`)
```
             prev        curr        next_node
              │           │              │
              ▼           ▼              ▼
NULL ◄─── [ 1 ]         [ 2 ] ───────► [ 3 ] ──► NULL
```

#### Iteration 2:
1. `next_node = curr->next` (`next_node` points to `3`)
2. `curr->next = prev` (`2` points to `1`)
3. `prev = curr` (`prev` points to `2`)
4. `curr = next_node` (`curr` points to `3`)
```
                         prev        curr
                          │           │
                          ▼           ▼
NULL ◄─── [ 1 ] ◄─── [ 2 ]         [ 3 ] ──► NULL
```

#### Iteration 3:
1. `next_node = curr->next` (`next_node` points to `NULL`)
2. `curr->next = prev` (`3` points to `2`)
3. `prev = curr` (`prev` points to `3`)
4. `curr = next_node` (`curr` points to `NULL`)
```
                                     prev        curr
                                      │           │
                                      ▼           ▼
NULL ◄─── [ 1 ] ◄─── [ 2 ] ◄─── [ 3 ]           NULL
```

#### Loop Ends (`curr == NULL`):
Naya `head` kaun ban gaya? **`prev`** (Node `3`)!

---

## 💻 4. C++ Implementation (Iterative)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        ListNode* next_node = nullptr;

        while (curr != nullptr) {
            next_node = curr->next;  // 1. Aage ka node save karo
            curr->next = prev;       // 2. Link ulta karo
            prev = curr;             // 3. prev aage badhao
            curr = next_node;        // 4. curr aage badhao
        }

        // Loop ke baad prev naye head ko point kar raha hota hai
        return prev;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — Har node ko exact 1 baar visit kiya.
- **Space Complexity:** $O(1)$ — Only 3 pointers use hue.

---

## 🔄 5. Approach 2: Recursive Method

Recursion mein hum sochte hain:
> *"Agar bhagwan/recursion baaki bachi hui list (`head->next`) ko reverse karke de de, toh main current `head` ko kaise link karunga?"*

### Recursive Leap of Faith:
Maan lo list hai: `1 -> 2 -> 3 -> 4 -> 5 -> NULL`
- Agar recursion `2 -> 3 -> 4 -> 5` ko reverse karke return kare:
  `5 -> 4 -> 3 -> 2 -> NULL`
- Toh notice karo: Node `1` ka `next` abhi bhi `2` ko point kar raha hai!
- Matlab: `head->next` is `2`.
- Agar hum bol dein: `head->next->next = head;`
  Toh `2->next` point karega `1` ko!
- Fir `1->next = NULL;` kar do taaki circular loop na bane.

```
Before Rewiring:
[ 1 (head) ] ──► [ 2 ] ◄── [ 3 ] ◄── [ 4 ] ◄── [ 5 (newHead) ]
                   │
                  NULL

Step 1: head->next->next = head; (2 points to 1)
[ 1 (head) ] ◄── [ 2 ] ◄── [ 3 ] ◄── [ 4 ] ◄── [ 5 (newHead) ]
     │
     └── (abhi bhi 1->next 2 ko point kar raha hai)

Step 2: head->next = NULL;
NULL ◄── [ 1 (head) ] ◄── [ 2 ] ◄── [ 3 ] ◄── [ 4 ] ◄── [ 5 (newHead) ]
```

### 💻 Recursive C++ Code:
```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        // Base Case: Empty list ya Single node list
        if (head == nullptr || head->next == nullptr) {
            return head;
        }

        // Recursion call: Bachi hui list ko reverse karo
        ListNode* newHead = reverseList(head->next);

        // Self-work: Apne node ko piche jod do
        head->next->next = head;
        head->next = nullptr;

        return newHead;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — Har node ke liye ek function call.
- **Space Complexity:** $O(N)$ — Call stack memory for $N$ recursive frames.

---

## 🧪 6. Edge Cases & Interview Pitfalls

1. **Empty List (`head == NULL`):**
   - Iterative: Loop execute nahi hoga, `prev` (NULL) return hoga. Safe!
   - Recursive: Base case handles it. Safe!
2. **Single Node (`head->next == NULL`):**
   - Dono cases mein wahi node return hoga. Safe!
3. **Bhulne waali common mistake (Recursive):**
   - `head->next = nullptr;` karna bhul jana! Agar ye nahi kiya toh node 1 aur node 2 aapas mein cycle bana lenge (`1 <-> 2`), aur infinite loop ho jayega!

---

## ⚡ 7. 1-Minute Revision Cheat Sheet

- **Iterative:** 3 pointers (`prev`, `curr`, `next_node`).
  - `next_node = curr->next; curr->next = prev; prev = curr; curr = next_node;`
  - Return `prev`.
  - **Time:** $O(N)$, **Space:** $O(1)$.
- **Recursive:** 
  - `ListNode* newHead = reverseList(head->next);`
  - `head->next->next = head;`
  - `head->next = nullptr;`
  - Return `newHead`.
  - **Time:** $O(N)$, **Space:** $O(N)$ (Call Stack).
- **Golden Rule:** Iterative is always preferred in interviews due to $O(1)$ space.
