# 📖 Lecture 05: Merge Two Sorted Lists | DSA Series
> **Video Link:** [Merge Two Sorted Lists | DSA Series](https://www.youtube.com/watch?v=f8RPIb-0DDE)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) (Easy)  
> **Core Concepts:** Dummy Node Technique, In-place Pointer Rewiring, Recursion

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Problem Statement:
Hume do already sorted singly linked lists ke heads diye gaye hain: `list1` aur `list2`.  
Hume in dono lists ko merge karke **ek single sorted linked list** banani hai aur uska `head` return karna hai.

```
list1:  [ 1 ] ──► [ 2 ] ──► [ 4 ] ──► NULL
list2:  [ 1 ] ──► [ 3 ] ──► [ 4 ] ──► NULL

Result: [ 1 ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 4 ] ──► NULL
```

### 💡 The Golden Technique: Dummy Node (Sentinel Node)
Jab hum do lists ko merge karte hain, toh pehla sawal uthta hai:  
> *"Nayi list ka pehla node (`head`) kaun banega? `list1` ka pehla node ya `list2` ka pehla node?"*

Agar hum dummy node use na karein, toh hume code mein baar-baar check karna padega:
```cpp
if (head == NULL) { head = ...; tail = ...; }
else { tail->next = ...; }
```
**Dummy Node ka Magic:**  
Hum ek fake / dummy node bana lete hain: `ListNode dummy(0);`  
Aur ek pointer `tail = &dummy;` rakh lete hain. Ab hum bina kisi special condition ke direct bol sakte hain:
`tail->next = (smaller node); tail = tail->next;`  
Aur function ke end mein actual answer simply kya hoga? **`dummy.next`**!

---

## 🧭 2. Approach 1: Iterative with Dummy Node (Optimal)

### Step-by-Step Algorithm:
1. Ek dummy node create karo: `ListNode dummy(-1);`
2. Ek pointer `tail = &dummy;` rakho jo merged list ke aakhiri node ko point karega.
3. Jab tak dono lists non-empty hain (`list1 != nullptr && list2 != nullptr`):
   - Dono ke current nodes ki value compare karo.
   - Jo node chhota hai, `tail->next` ko us node par point karo.
   - Us list ke pointer ko aage badhao (`list1 = list1->next` ya `list2 = list2->next`).
   - `tail` ko bhi aage badhao (`tail = tail->next`).
4. **Attach the remaining list:**  
   Jaise hi ek list khatam hoti hai, doosri list ke baaki bache saare nodes already sorted hain!  
   Toh bas ek single step mein `tail->next` ko bachi hui list se connect kar do:
   ```cpp
   if (list1 != nullptr) tail->next = list1;
   else tail->next = list2;
   ```
5. Return karo `dummy.next`.

---

## 📊 3. Visual Pointer Dry Run

Maan lo:
- `list1: [ 1 -> 4 -> NULL ]`
- `list2: [ 2 -> 3 -> NULL ]`

```
Initial:
dummy [-1]
  ▲
 tail
list1: [ 1 ] ──► [ 4 ] ──► NULL
list2: [ 2 ] ──► [ 3 ] ──► NULL

Iteration 1 (Compare 1 and 2 -> 1 is smaller):
dummy [-1] ──► [ 1 ] (from list1)
                 ▲
                tail
list1 moves to [ 4 ]

Iteration 2 (Compare 4 and 2 -> 2 is smaller):
dummy [-1] ──► [ 1 ] ──► [ 2 ] (from list2)
                           ▲
                          tail
list2 moves to [ 3 ]

Iteration 3 (Compare 4 and 3 -> 3 is smaller):
dummy [-1] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] (from list2)
                                     ▲
                                    tail
list2 becomes NULL (Loop terminates!)

After Loop (Attach remaining list1):
tail->next = list1 (Node 4)
dummy [-1] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► NULL
```
Result Head = `dummy.next` = `[1]`.

---

## 💻 4. Optimal C++ Code (Iterative)

```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // Stack-allocated dummy node (No dynamic memory allocation needed!)
        ListNode dummy(-1);
        ListNode* tail = &dummy;

        while (list1 != nullptr && list2 != nullptr) {
            if (list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }

        // Attach remaining elements directly
        if (list1 != nullptr) {
            tail->next = list1;
        } else {
            tail->next = list2;
        }

        return dummy.next;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N + M)$ — Jaha $N$ aur $M$ dono lists ke lengths hain. Hum har node ko maximum ek baar visit karte hain.
- **Space Complexity:** $O(1)$ — Hum koi naye nodes create nahi kar rahe, sirf existing pointers ko rewire kar rahe hain.

---

## 🔄 5. Approach 2: Recursive Solution

Recursion is very elegant here:
- **Base Case:** 
  - Agar `list1` empty hai, toh `list2` return kar do.
  - Agar `list2` empty hai, toh `list1` return kar do.
- **Recursive Step:**
  - Agar `list1->val <= list2->val`:
    - `list1->next = mergeTwoLists(list1->next, list2);`
    - `return list1;`
  - Else:
    - `list2->next = mergeTwoLists(list1, list2->next);`
    - `return list2;`

```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (list1 == nullptr) return list2;
        if (list2 == nullptr) return list1;

        if (list1->val <= list2->val) {
            list1->next = mergeTwoLists(list1->next, list2);
            return list1;
        } else {
            list2->next = mergeTwoLists(list1, list2->next);
            return list2;
        }
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N + M)$
- **Space Complexity:** $O(N + M)$ (Auxiliary recursion stack frames).

---

## 🧪 6. Edge Cases & Interview Pitfalls

1. **Both Lists Empty (`list1 == NULL && list2 == NULL`):**
   - Returns `nullptr`. Handled gracefully.
2. **One List Empty (`list1 == NULL` or `list2 == NULL`):**
   - Directly attaches and returns the non-empty list.
3. **Lists of Unequal Lengths:**
   - Handled seamlessly by the `tail->next = list1 ? list1 : list2` step.
4. **Duplicates:**
   - Condition `<= ` ensures stable ordering of identical values.

---

## ⚡ 7. 1-Minute Revision Cheat Sheet

- **Best Approach:** Iterative with Dummy Node.
- **Why Dummy Node?** Eliminates special-case checks for list head.
- **Key Step:**
  - Compare `list1->val` vs `list2->val`, link smaller node to `tail->next`.
  - After loop, link leftover list in $O(1)$: `tail->next = (list1 ? list1 : list2);`
- **Return:** `dummy.next`.
- **Complexity:** $O(N + M)$ Time, $O(1)$ Space.
- **Applications:** Used in Merge Sort of Linked List and Merge K Sorted Lists.
