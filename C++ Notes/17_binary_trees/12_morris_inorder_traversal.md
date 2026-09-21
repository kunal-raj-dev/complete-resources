# Lecture 96: Morris Inorder Traversal: $O(1)$ Auxiliary Space

> **One-Line Purpose:** Traverse a binary tree in inorder using temporary threaded predecessor pointers, achieving $O(N)$ time with strictly $O(1)$ auxiliary memory and zero recursion stack.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #96  
> **Video ID:** `PUfADhkq1LI`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=PUfADhkq1LI)  
> **Duration:** 17:52  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

**The Problem:** In recursive inorder traversal, the call stack is used as "bookmarks" — when you go left, you implicitly save where to come back. Standard iterative inorder uses an explicit stack. Both use $O(H)$ space.

**Morris's Insight:** What if we could use the tree's own null pointers as our "bookmarks"? Most leaf nodes have `right = nullptr`. Morris traversal temporarily BORROWS these null right pointers to create **threads** — links that allow us to find our way back to the current node after exploring the left subtree.

**Why "threaded"?** A **threaded binary tree** is a variant where some right pointers point to the inorder successor instead of null. Morris temporarily creates and removes these threads during traversal.

```
Original Tree:          After threading (1st visit at node 2):
       1                        1
      / \                      / \
     2   3          →         2   3
    / \                      / \
   4   5                    4   5
                                 \
                                  2 ← temporary thread! (5's right → 2's inorder successor)
```

**The Two-State Algorithm at each node `curr`:**
- **If `curr->left == null`:** No left subtree to explore. Visit `curr`, move right.
- **If `curr->left != null`:** Find the inorder predecessor (rightmost node in left subtree).
  - **If `pred->right == null`:** First visit — create thread `pred->right = curr`. Move to left child.
  - **If `pred->right == curr`:** Second visit — thread exists (we came back via the thread). Remove it, visit `curr`, move right.

---

## 🎯 Pattern Recognition — When to Use This

- Problem says "**O(1) extra space**" + traversal/inorder → Morris Traversal
- **Recover BST** without extra space → Morris traversal to find inversions
- **Kth smallest in BST** in O(1) space → Morris
- Any inorder operation where memory is constrained

---

## 🔵 Threading Mechanics
1. If `curr->left == nullptr`, print `curr->val` and advance `curr = curr->right`.
2. Otherwise, find the **inorder predecessor** of `curr` (rightmost node in left subtree):
   - If `pred->right == nullptr`, create temporary thread: `pred->right = curr` and move `curr = curr->left`.
   - If `pred->right == curr`, thread already exists! Remove thread: `pred->right = nullptr`, print `curr->val`, and move `curr = curr->right`.

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class MorrisTraversal {
public:
    static vector<int> inorder(TreeNode* root) {
        vector<int> result;
        TreeNode* curr = root;

        while (curr != nullptr) {
            if (curr->left == nullptr) {
                result.push_back(curr->val);
                curr = curr->right;
            } else {
                // Find inorder predecessor
                TreeNode* pred = curr->left;
                while (pred->right != nullptr && pred->right != curr) {
                    pred = pred->right;
                }

                if (pred->right == nullptr) {
                    // Create thread
                    pred->right = curr;
                    curr = curr->left;
                } else {
                    // Remove thread
                    pred->right = nullptr;
                    result.push_back(curr->val);
                    curr = curr->right;
                }
            }
        }
        return result;
    }
};

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);

    auto res = MorrisTraversal::inorder(root);
    cout << "Morris Inorder: ";
    for (int x : res) cout << x << " "; // Output: 4 2 5 1 3
    cout << endl;
    return 0;
}
```

---

## 🔍 Dry Run Trace

```
Tree:       1
           / \
          2   3
         / \
        4   5

Step-by-step (curr tracks current node):

curr=1: left=2, find pred in 2's right subtree → pred=5 (5.right==null)
        Create thread: 5.right=1. Move curr=2.

curr=2: left=4, find pred in 4's right subtree → pred=4 (4.right==null)
        Create thread: 4.right=2. Move curr=4.

curr=4: left=null → VISIT 4. Move curr=4.right=2 (thread!).

curr=2: left=4, find pred → pred=4, 4.right==curr(2) (thread exists!)
        Remove thread: 4.right=null. VISIT 2. Move curr=2.right=5.

curr=5: left=null → VISIT 5. Move curr=5.right=1 (thread!).

curr=1: left=2, find pred in 2's right subtree → pred=5, 5.right==curr(1) (thread exists!)
        Remove thread: 5.right=null. VISIT 1. Move curr=1.right=3.

curr=3: left=null → VISIT 3. Move curr=3.right=null.

curr=null: STOP.

Output: 4 2 5 1 3 ✓ (correct inorder)
```

---

## ⚠️ Common Interview Mistakes

1. **Modifying the tree permanently:** The predecessor-finding while loop must stop when `pred->right == curr` (thread exists), otherwise it loops infinitely. The condition `pred->right != nullptr && pred->right != curr` handles both "end of subtree" and "thread detected" cases.

2. **Confusing first visit vs second visit:** The key distinction: first visit creates the thread and goes left; second visit (thread already set) removes thread, visits, and goes right.

3. **Claiming Morris traversal is always faster:** It's NOT faster than recursive traversal — both are $O(N)$. Morris is only superior in space: $O(1)$ vs $O(H)$.

4. **Thinking Morris permanently modifies the tree:** Morris traversal RESTORES every thread it creates. The tree is identical before and after the traversal.

5. **Can Morris be used for Preorder?** Yes! Visit the node when creating the thread (first visit) instead of when removing it (second visit).

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ amortized (each edge traversed at most 3 times).
  - Each node is visited at most twice (once going left, once coming back via thread).
  - The predecessor-finding loop traverses each right-edge at most twice total.
- **Space Complexity:** Strict $O(1)$ auxiliary space.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] Why is Morris Traversal described as O(1) space even though it modifies the tree?
**Answer:** Morris traversal reuses the tree's own existing pointers — it doesn't allocate any new memory. The thread it creates is a temporary assignment to an existing `right` pointer that was previously null. Since no new heap memory or stack space is allocated, the auxiliary space is truly O(1). The modification is transient: every thread is removed before the traversal ends, leaving the tree structurally identical to before.

### Q2: [Deep Dive] What are "threaded binary trees" and how does Morris relate to them?
**Answer:** A **threaded binary tree** is a permanent variant of a binary tree where some or all null pointers are replaced with pointers to the inorder predecessor or successor. This allows traversal without recursion or explicit stacks. A **right-threaded binary tree** replaces null right pointers with inorder successor links. Morris traversal is essentially a **temporary threaded tree** — it creates threads, uses them, and destroys them, achieving the same space benefit of a permanent threaded tree without the storage overhead of maintaining threads in the data structure.

### Q3: [Output Prediction] The following Morris code has a bug. What is wrong and what output does it produce?
```cpp
// Buggy version
while (curr) {
    if (!curr->left) {
        result.push_back(curr->val);
        curr = curr->right;
    } else {
        TreeNode* pred = curr->left;
        while (pred->right) {  // BUG: missing pred->right != curr check
            pred = pred->right;
        }
        pred->right = curr;
        curr = curr->left;
    }
}
```
**Answer:** This produces an **infinite loop**. When the thread `pred->right = curr` is created and we move `curr = curr->left`, eventually we reach node 4 (leaf), go right via the thread back to 2. Now at node 2, the code tries to find the predecessor again — goes to 4, then follows `4->right = 2` (thread), then `2->right = ... (thread to 1)`. It keeps cycling in the thread without ever removing it. The fix is `while (pred->right && pred->right != curr)` to detect the thread.

### Q4: [Extension] How would you modify Morris traversal for Preorder instead of Inorder?
**Answer:** Visit the node on the FIRST encounter (when creating the thread), not the second:
```cpp
if (pred->right == nullptr) {
    result.push_back(curr->val);  // Visit HERE (first encounter)
    pred->right = curr;
    curr = curr->left;
} else {
    pred->right = nullptr;
    // Do NOT visit here
    curr = curr->right;
}
```
For nodes with no left child, still visit immediately. This gives Preorder: Root→Left→Right.

### Q5: [Tricky] Can Morris Traversal be used for Postorder? Is it harder?
**Answer:** Yes, but it's significantly more complex. One approach:
1. Create a "dummy" root with `dummy->left = actual_root`.
2. Perform a Morris traversal that, each time a thread is detected, reverses and prints the right spine from curr's left child to the predecessor, then unreverses it.
Alternatively: use the "reverse of modified preorder" trick (as with iterative postorder). Morris postorder is rarely asked in interviews — know that it exists and is complex.

### Q6: [Conceptual] Is the time complexity truly O(N) or does the predecessor-finding loop make it O(N log N) or worse?
**Answer:** It is truly $O(N)$ amortized. The key insight: each right edge in the tree is traversed AT MOST twice — once while searching for the predecessor (going right), and once when following the thread back. Since there are exactly $N-1$ edges in a tree, total predecessor-finding work across all iterations = $O(N)$. The outer loop also runs $O(N)$ times. Therefore total work = $O(N)$.

### Q7: [Application] Where is Morris traversal used in practice beyond interview problems?
**Answer:** Morris traversal is used in:
- **Memory-constrained embedded systems** where heap/stack space is at a premium
- **Recover BST (LeetCode 99):** Find inorder inversions in O(1) space
- **Database tree index traversal** when stack space is limited
- **Compilers and interpreters** for symbol table traversal in constrained environments
- Any scenario where $O(\log N)$ or $O(N)$ stack space would cause stack overflow for very deep trees

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 94 | Binary Tree Inorder Traversal | Morris or iterative stack |
| 99 | Recover BST | Morris traversal to find swapped nodes |
| 501 | Find Mode in BST | Morris inorder, track previous value |
| 114 | Flatten Binary Tree to LL | Morris-inspired O(1) space rewiring |

---

## 🔗 Cross-Topic Connections
- **Threaded Binary Trees:** Morris creates temporary threads — same concept as permanent threaded trees
- **Recover BST (Lecture 106):** Morris traversal enables O(1) space recovery of swapped nodes
- **BST Iterator (Lecture 109):** Also O(H) space; Morris is the O(1) alternative
- **Flatten to LL (Lecture 97):** Uses the same "find rightmost leaf" pattern as Morris

---

## ⚡ 2-Minute Revision Flash Card
- **Morris = temporarily thread `pred->right = curr`; remove it on 2nd visit**
- **First visit:** `pred->right == null` → create thread, go LEFT
- **Second visit:** `pred->right == curr` → remove thread, VISIT, go RIGHT
- **No left child:** VISIT immediately, go right
- **Space:** $O(1)$ — no stack, no extra memory; **Time:** $O(N)$ amortized
