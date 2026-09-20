# 📖 Lecture 10: Reverse Nodes in K-Group | Linked List
> **Video Link:** [Reverse Nodes in K-Group | Linked List](https://www.youtube.com/watch?v=-swgIiMIlJo)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) (Hard)  
> **Core Concepts:** Group-wise Reversal, K-Length Verification, Recursive Subproblem Linking, In-place Pointer Mechanics

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Problem Statement:
Hume ek linked list ka `head` aur ek integer `k` diya gaya hai.  
Hume list ke nodes ko **$k$ nodes ke groups** mein reverse karna hai.
- Agar aakhiri group mein nodes ki sankhya $k$ se kam hai, toh unhe **as-it-is (bina reverse kiye)** chhod dena hai.
- Node values modify karna strictly prohibited hai, sirf pointers change karne hain!

```
Example 1: List = [1, 2, 3, 4, 5], k = 2
Group 1 [1, 2] -> reversed to [2, 1]
Group 2 [3, 4] -> reversed to [4, 3]
Group 3 [5]    -> length < 2, remains [5]
Result: [ 2 ──► 1 ──► 4 ──► 3 ──► 5 ──► NULL ]

Example 2: List = [1, 2, 3, 4, 5], k = 3
Group 1 [1, 2, 3] -> reversed to [3, 2, 1]
Group 2 [4, 5]    -> length < 3, remains [4, 5]
Result: [ 3 ──► 2 ──► 1 ──► 4 ──► 5 ──► NULL ]
```

---

## 🧩 2. Problem Breakdown: Ye "Hard" Kyun Hai?

Is problem mein 3 alag-alag challenges ek saath aate hain:
1. **Verification:** Pehle check karo ki aage sach mein kam se kam $k$ nodes bache hain ya nahi.
2. **Reversal:** Current $k$ nodes ko reverse karo.
3. **Stitching:** 
   - Reversal ke baad jo naya head bana, use pichle group se jodo.
   - Puraane head (jo ab current group ka tail ban chuka hai) ko agle group se jodo.

---

## 🧭 3. Approach 1: Recursive Solution (Most Intuitive)

### The Recursive Magic:
- Agar hum pehle $k$ nodes ko reverse kar lein...
- Aur baaki bachi hui list par recursion call kar dein: `head->next = reverseKGroup(curr, k);`
- Toh recursion baaki saare groups ko reverse karke unka head laakar de dega!
- Hum simply apne current reversed group ke aakhiri node (`head`) ko recursion ke result se connect kar denge!

### Step-by-Step Algorithm:
1. **Check for $k$ nodes:**
   Ek pointer `temp = head` lo aur $k$ steps aage badhao.  
   Agar $k$ steps complete hone se pehle `temp == nullptr` ho jaye, toh iska matlab bache hue nodes $< k$ hain. Return `head` as-is!
2. **Reverse current $k$ nodes:**
   Standard 3-pointer reversal lagao for exact $k$ nodes:
   ```cpp
   ListNode* prev = nullptr;
   ListNode* curr = head;
   for (int i = 0; i < k; i++) {
       ListNode* nextNode = curr->next;
       curr->next = prev;
       prev = curr;
       curr = nextNode;
   }
   ```
3. **Recursive Call on the remaining list:**
   Ab `curr` agle group ke pehle node par khada hai.
   ```cpp
   head->next = reverseKGroup(curr, k);
   ```
   *(Notice: `head` ab current group ka aakhiri node ban chuka hai, isliye `head->next` recursion ke result se jod diya!)*
4. **Return naya head:**
   Return `prev` (jo current reversed group ka pehla node hai).

---

## 📊 4. Visual Pointer Dry Run ($k = 2$, List: `[1 -> 2 -> 3 -> 4 -> 5]`)

### Step 1: First Call `reverseKGroup(1, k=2)`
- $k=2$ nodes exist? Yes (`1` and `2`).
- Reverse 2 nodes:
  `[ 1 ] <── [ 2 ]`
  - `prev` points to `2`.
  - `curr` points to `3`.
  - `head` is `1`.

### Step 2: Recursive Call `head->next = reverseKGroup(3, k=2)`
- Inside second call on `[3 -> 4 -> 5]`:
  - $k=2$ nodes exist? Yes (`3` and `4`).
  - Reverse 2 nodes:
    `[ 3 ] <── [ 4 ]`
    - `prev` points to `4`.
    - `curr` points to `5`.
    - `head` is `3`.

### Step 3: Recursive Call `head->next = reverseKGroup(5, k=2)`
- Inside third call on `[5]`:
  - $k=2$ nodes exist? **NO** (only 1 node).
  - Returns `5` as-is!

### Backtracking & Stitching:
- Second call joins `3->next = 5` $\implies$ Group is `[4 -> 3 -> 5]`, returns `4`.
- First call joins `1->next = 4` $\implies$ Group is `[2 -> 1 -> 4 -> 3 -> 5]`, returns `2`.
- Final Answer: `[ 2 -> 1 -> 4 -> 3 -> 5 -> NULL ]`!

---

## 💻 5. Clean C++ Implementation (Recursive)

```cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        if (!head || k == 1) return head;

        // Step 1: Check if there are at least k nodes remaining
        ListNode* temp = head;
        for (int i = 0; i < k; i++) {
            if (temp == nullptr) {
                return head; // Less than k nodes, leave as is
            }
            temp = temp->next;
        }

        // Step 2: Reverse exactly k nodes
        ListNode* prev = nullptr;
        ListNode* curr = head;
        ListNode* nextNode = nullptr;

        for (int i = 0; i < k; i++) {
            nextNode = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nextNode;
        }

        // Step 3: Connect the tail of reversed group (head) to the result of next group
        head->next = reverseKGroup(curr, k);

        // Step 4: Return new head of this group
        return prev;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — Har node ko do baar visit kiya jata hai (ek baar check karne ke liye aur ek baar reverse karne ke liye). $2N \approx O(N)$.
- **Space Complexity:** $O(N / k)$ — Recursion call stack frames for $N / k$ groups.

---

## ⚡ 6. Approach 2: Iterative Solution ($O(1)$ Space)

Agar interviewer bole: *"Solve it in strictly $O(1)$ auxiliary space without recursion stack"*:

```cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        if (!head || k == 1) return head;

        ListNode dummy(0);
        dummy.next = head;
        ListNode* prevGroup = &dummy;

        while (true) {
            // Check if k nodes exist
            ListNode* kth = prevGroup;
            for (int i = 0; i < k && kth != nullptr; i++) {
                kth = kth->next;
            }
            if (kth == nullptr) break;

            ListNode* nextGroup = kth->next;
            ListNode* prev = nextGroup;
            ListNode* curr = prevGroup->next;

            // Reverse k nodes
            while (curr != nextGroup) {
                ListNode* temp = curr->next;
                curr->next = prev;
                prev = curr;
                curr = temp;
            }

            ListNode* temp = prevGroup->next;
            prevGroup->next = kth;
            prevGroup = temp;
        }

        return dummy.next;
    }
};
```
- **Time Complexity:** $O(N)$
- **Space Complexity:** $O(1)$

---

## 🧪 7. Edge Cases & Interview Pitfalls

1. **$k = 1$:**
   - No change needed. Returns `head` directly.
2. **List length $< k$:**
   - Handled by initial check, returns `head` unmodified.
3. **List length exact multiple of $k$:**
   - Last recursive call gets `nullptr` and returns `nullptr`.
4. **Altering values:**
   - Never do `swap(node1->val, node2->val)`. In FAANG interviews, changing node values is strictly forbidden unless explicitly requested.

---

## ⚡ 8. 1-Minute Revision Cheat Sheet

- **Core Idea:** Check $k$ nodes $\to$ Reverse $k$ nodes $\to$ Recursively link to next group.
- **Base Case:** If $< k$ nodes remain, return `head` as-is.
- **Linking Formula:** `head->next = reverseKGroup(curr, k);`
- **Return:** `prev` (new head of reversed group).
- **Time:** $O(N)$, **Space:** $O(N/k)$ recursive / $O(1)$ iterative.
