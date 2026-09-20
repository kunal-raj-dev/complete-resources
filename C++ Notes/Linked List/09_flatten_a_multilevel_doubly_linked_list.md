# 📖 Lecture 09: Flatten a Multilevel Doubly Linked List
> **Video Link:** [Flatten a Doubly Linked List | Leetcode 430 | DSA Series](https://www.youtube.com/watch?v=I8b0rff5F9M)  
> **Instructor:** Shradha Khapra  
> **LeetCode Problem:** [430. Flatten a Multilevel Doubly Linked List](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/) (Medium)  
> **Core Concepts:** Multilevel Doubly Linked List, Depth-First Search (DFS), Pointer Splice / Tail Stitching Technique

---

## 🎯 1. Concept Ki Baat (Core Intuition)

### Node Anatomy:
Is problem mein har node ke paas 3 pointers hote hain:
1. `prev`: Piche waale node ka pointer.
2. `next`: Agle node ka pointer.
3. `child`: Niche waali doosri doubly linked list ka pointer (agar child exist na kare toh `NULL`).

```cpp
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
};
```

### Problem Statement:
Hume is multilevel structure ko **flatten** karke ek single-level standard doubly linked list banani hai.  
Sabhi nodes **DFS (Depth-First Search / Preorder)** order mein aane chahiye:
- Pehle current node.
- Fir uska pura child branch.
- Fir bacha hua `next` branch.
- Aur har node ka `child` pointer aakhir mein **`NULL`** ho jana chahiye!

```
Original Multilevel List:
 1 <---> 2 <---> 3 <---> 4 <---> 5 <---> 6 ---> NULL
                 |
                 7 <---> 8 <---> 9 <---> 10 ---> NULL
                         |
                         11 <---> 12 ---> NULL

Flattened List (DFS Order):
 1 <-> 2 <-> 3 <-> 7 <-> 8 <-> 11 <-> 12 <-> 9 <-> 10 <-> 4 <-> 5 <-> 6 ---> NULL
```

---

## 🧭 2. Approach 1: Iterative Pointer Splice / Tail Stitching (Optimal $O(1)$ Space)

Is approach ka simple funda hai:  
Jaise hi kisi node `curr` par `child` mile, us child branch ko `curr` aur `curr->next` ke **beech mein ghusaa do (splice/stitch)**!

### 5-Step Pointer Rewiring Procedure:

```
        curr                     curr->next
         │                            │
         ▼                            ▼
   ... <---> [ curr ] <──────────────> [ nextNode ] <---> ...
               │
               ▼ (child)
             [ childHead ] <---> ... <---> [ childTail ]
```

Jab `curr->child != nullptr`:
1. **Child branch ke tail tak jao:**
   ```cpp
   Node* child = curr->child;
   Node* tail = child;
   while (tail->next != nullptr) {
       tail = tail->next;
   }
   ```
2. **Child branch ke tail ko `curr->next` se connect karo:**
   ```cpp
   tail->next = curr->next;
   if (curr->next != nullptr) {
       curr->next->prev = tail;
   }
   ```
3. **`curr` ko `child` se connect karo:**
   ```cpp
   curr->next = child;
   child->prev = curr;
   ```
4. **`child` pointer ko nullify karo (Mandatory!):**
   ```cpp
   curr->child = nullptr;
   ```
5. **Aage badho:**
   `curr = curr->next;` (Ab curr naturally child branch ke nodes ko traverse karega. Agar unme bhi koi child mila, toh wo bhi isi tarah aage stitch ho jayega!).

---

## 📊 3. Visual Pointer Dry Run

Maan lo list hai:
```
[ 1 ] <---> [ 2 ] <---> [ 3 ] ---> NULL
              │
            [ 7 ] <---> [ 8 ] ---> NULL
```

- **Step 1:** `curr` starts at `1`. No child. Move `curr` to `2`.
- **Step 2:** At `2`, `child` exists (`7`).
  - Child's tail is `8`.
  - Link `8->next = 2->next` (`3`).
  - Link `3->prev = 8`.
  - Link `2->next = 7`.
  - Link `7->prev = 2`.
  - Set `2->child = nullptr`.
- **Updated List:**
  `[ 1 ] <---> [ 2 ] <---> [ 7 ] <---> [ 8 ] <---> [ 3 ] ---> NULL`
- **Step 3:** `curr` moves to `7`, then `8`, then `3`, then `NULL`.
- Loop finishes!

---

## 💻 4. Optimal C++ Code (Iterative)

```cpp
class Solution {
public:
    Node* flatten(Node* head) {
        if (!head) return nullptr;

        Node* curr = head;

        while (curr != nullptr) {
            // Agar child node exist karta hai
            if (curr->child != nullptr) {
                Node* nextNode = curr->next;
                Node* childHead = curr->child;

                // Step 1: Child branch ka tail dhundho
                Node* tail = childHead;
                while (tail->next != nullptr) {
                    tail = tail->next;
                }

                // Step 2: Tail ko curr->next se connect karo
                tail->next = nextNode;
                if (nextNode != nullptr) {
                    nextNode->prev = tail;
                }

                // Step 3: Curr ko childHead se connect karo
                curr->next = childHead;
                childHead->prev = curr;

                // Step 4: Child pointer ko NULL set karo
                curr->child = nullptr;
            }

            // Step 5: Agle node par move karo
            curr = curr->next;
        }

        return head;
    }
};
```

**Complexity Analysis:**
- **Time Complexity:** $O(N)$ — Har node ko constant number of times visit kiya jata hai.
- **Space Complexity:** $O(1)$ — Koi recursion stack ya extra data structure use nahi hua.

---

## 🔄 5. Approach 2: Stack / DFS Approach (Alternative)

Hum ek `stack<Node*>` use kar sakte hain:
- Jab bhi kisi node par `child` mile:
  - Agar `curr->next` exist karta hai, use stack mein push karo.
  - `curr->next = curr->child;`
  - `curr->child = nullptr;`
- Jab `curr->next == NULL` ho aur stack khali na ho:
  - Stack se top node pop karo aur `curr->next` se connect karo.

**Complexity:**
- **Time:** $O(N)$
- **Space:** $O(N)$ (Stack space in worst case when every node has a child).

---

## 🧪 6. Edge Cases & Interview Pitfalls

1. **`head == nullptr`:**
   - Pehle hi check karo aur `nullptr` return karo.
2. **`curr->next == nullptr` with a Child:**
   - Maan lo last node ke paas child hai.
   - `nextNode` NULL hoga.
   - Code mein check: `if (nextNode != nullptr) nextNode->prev = tail;` safe hai aur crash prevent karta hai.
3. **Bhulne waali sabse badi galti:**
   - `curr->child = nullptr;` karna bhul jana! LeetCode par ye error deta hai: *"Output list contains non-null child pointers!"*
4. **Bidirectional Links (`prev` & `next`):**
   - Hamesha dono taraf ke pointers update karo:
     `tail->next = nextNode;` ke saath saath `nextNode->prev = tail;` bhi zaroori hai!

---

## ⚡ 7. 1-Minute Revision Cheat Sheet

- **Pattern:** DFS / Pointer Splicing.
- **Key Idea:** Child branch ko `curr` aur `curr->next` ke beech mein stitch kar do.
- **Pointer Updates:**
  1. Find `tail` of child list.
  2. `tail->next = curr->next;`
  3. `if (curr->next) curr->next->prev = tail;`
  4. `curr->next = curr->child;`
  5. `curr->child->prev = curr;`
  6. `curr->child = nullptr;`
- **Complexity:** $O(N)$ Time, $O(1)$ Space.
