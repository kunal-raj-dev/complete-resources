# Lecture 86: Height & Count of Nodes in Binary Tree

> **One-Line Purpose:** Formulate bottom-up recursive reductions to compute tree height, total node count, and node sum in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #86  
> **Video ID:** `7tzHzN_Ehus`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=7tzHzN_Ehus)  
> **Duration:** 23:09  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

Imagine you're a manager asking your team "How tall is the org chart below you?" Each employee can only answer by first asking THEIR direct reports. This is **bottom-up aggregation via postorder traversal**.

The key recursive insight for height:
$$\text{height}(u) = 1 + \max(\text{height}(u.\text{left}), \text{height}(u.\text{right}))$$

A null node has height 0 (it contributes nothing). A leaf node gets $1 + \max(0, 0) = 1$.

```
Tree:         1          height=3
            /   \
           2     3       height=2, height=1
          / \
         4   5           height=1, height=1

height(4) = 1 + max(0,0) = 1
height(5) = 1 + max(0,0) = 1
height(2) = 1 + max(1,1) = 2
height(3) = 1 + max(0,0) = 1
height(1) = 1 + max(2,1) = 3
```

**Height vs Depth:**
- **Height** of a node = length of the **longest path downward** to a leaf. Measured from the node to the bottom.
- **Depth** of a node = length of the path from the **root down to the node**. Root has depth 0.
- Height of the whole tree = depth of the deepest leaf = height of the root.

**Height of a leaf: 0 or 1?** — It depends on the definition:
- **Definition A (edges):** Height = number of edges on longest path down → leaf has height **0**.
- **Definition B (nodes):** Height = number of nodes on longest path down → leaf has height **1**.

The code below uses Definition B (nodes). LeetCode typically uses Definition A. Diameter is measured in edges so be consistent!

---

## 🎯 Pattern Recognition — When to Use This

- Problem asks for "height", "depth", "levels", or "balanced" → height function
- Problem asks for "count of nodes" or "size of subtree" → countNodes function
- Problem involves **complete binary tree** and asks for O(log² N) node count → special technique

---

## 🔵 Complete C++ Implementation

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(height(root->left), height(root->right));
}

int countNodes(TreeNode* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int sumOfNodes(TreeNode* root) {
    if (!root) return 0;
    return root->val + sumOfNodes(root->left) + sumOfNodes(root->right);
}
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$ stack space.

---

## 💻 Count Nodes in Complete Binary Tree — O(log² N)

A **complete binary tree** (all levels full except last, last filled left-to-right) allows a smarter count:

```cpp
// O(log^2 N) — exploits complete binary tree structure
int countComplete(TreeNode* root) {
    if (!root) return 0;

    // Find left height: keep going left
    int lh = 0;
    TreeNode* l = root;
    while (l) { lh++; l = l->left; }

    // Find right height: keep going right
    int rh = 0;
    TreeNode* r = root;
    while (r) { rh++; r = r->right; }

    // If equal, it's a perfect binary tree: 2^h - 1 nodes
    if (lh == rh) return (1 << lh) - 1;

    // Otherwise, recurse on both subtrees
    return 1 + countComplete(root->left) + countComplete(root->right);
}
```

**Why O(log² N)?** Each recursion does O(log N) work (tracing left/right paths). The recursion goes $O(\log N)$ levels deep in the worst case. Total: $O(\log N \times \log N) = O(\log^2 N)$.

---

## 🔍 Dry Run Trace

```
countNodes on:    1
                 / \
                2   3
               / \
              4   5

countNodes(1):
  countNodes(2):
    countNodes(4) → returns 1
    countNodes(5) → returns 1
    returns 1 + 1 + 1 = 3
  countNodes(3):
    countNodes(null) → returns 0
    countNodes(null) → returns 0
    returns 1 + 0 + 0 = 1
  returns 1 + 3 + 1 = 5  ✓
```

---

## ⚠️ Common Interview Mistakes

1. **Height vs Depth confusion in diameter:** When computing diameter, use the same height definition throughout. Mixing causes off-by-one.
2. **Height of null:** Must return 0, NOT -1 (unless you're using edge-based height convention). Returning -1 for null would make leaf height = 0 (edges).
3. **Stack overflow on skewed trees:** For a skewed tree of N=100,000 nodes, the O(N) recursion depth causes stack overflow. Interviewers may ask for an iterative solution using an explicit stack.
4. **Integer overflow in sumOfNodes:** If values are large, `int` can overflow. Use `long long`.

---

## ⏱️ Complexity Analysis
- **height/countNodes/sumOfNodes:** Time $O(N)$, Space $O(H)$ (recursion stack).
  - Balanced tree: $H = O(\log N)$
  - Skewed tree: $H = O(N)$
- **countComplete (complete BT):** Time $O(\log^2 N)$, Space $O(\log N)$.
  - Proof: At each level of recursion (depth $d$), one of the two recursive calls terminates immediately because either the left or right subtree is a perfect binary tree. So recursion is $O(\log N)$ depth, each level doing $O(\log N)$ path tracing work.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the difference between height and depth of a node?
**Answer:** **Height** is measured **downward from a node to the deepest leaf** in its subtree. **Depth** is measured **upward from the node to the root**. Root has depth 0. Leaves have height 0 (edge-based) or 1 (node-based). The height of the tree = height of the root = maximum depth across all leaves. In an interview, always clarify which convention is being used.

### Q2: [Extension] For a complete binary tree, how do you count nodes in O(log² N) instead of O(N)?
**Answer:** Exploit the property that in a complete binary tree, either the left subtree or the right subtree is a **perfect binary tree**. Trace the leftmost and rightmost paths from the root. If their heights are equal, the whole tree is perfect: return $2^h - 1$. If heights differ, one subtree is perfect — recurse only on the non-perfect subtree. Recurrence: $T(N) = T(N/2) + O(\log N)$, which solves to $O(\log^2 N)$ by master theorem.

### Q3: [Tricky] The following function claims to check if a tree is height-balanced. Find the bug.
```cpp
bool isBalanced(TreeNode* root) {
    if (!root) return true;
    int lh = height(root->left);
    int rh = height(root->right);
    return abs(lh - rh) <= 1 && isBalanced(root->left) && isBalanced(root->right);
}
```
**Answer:** The bug is $O(N^2)$ time complexity. `height()` is called at every node AND recursively calls itself on subtrees. For a balanced tree this is $O(N \log N)$; for a skewed tree, $O(N^2)$. The fix: combine height computation with balance checking in a single postorder pass, returning -1 to signal "unbalanced":
```cpp
int checkHeight(TreeNode* root) {
    if (!root) return 0;
    int lh = checkHeight(root->left);
    if (lh == -1) return -1;
    int rh = checkHeight(root->right);
    if (rh == -1) return -1;
    if (abs(lh - rh) > 1) return -1;
    return 1 + max(lh, rh);
}
bool isBalanced(TreeNode* root) { return checkHeight(root) != -1; }
```

### Q4: [Conceptual] When does height of a BST degrade and what is the impact?
**Answer:** BST height degrades to $O(N)$ when elements are inserted in sorted (or reverse sorted) order, producing a **skewed tree** (like a linked list). This makes search, insert, and delete $O(N)$ instead of $O(\log N)$. Self-balancing BSTs (AVL trees, Red-Black trees) maintain $O(\log N)$ height by performing rotations after insertions/deletions.

### Q5: [Output Prediction] What does `height(nullptr)` return in the implementation above?
**Answer:** `0`. The base case is `if (!root) return 0;`. This is the edge-based definition minus 1 — a null pointer has no nodes. This means a single-node tree returns height 1 (node-based). If a problem requires edge-based height (leaf = 0), change the base case to `if (!root) return -1;`.

### Q6: [Design] How would you find the height of a binary tree iteratively (without recursion)?
**Answer:** Use BFS (Level Order). Count the number of levels:
```cpp
int heightBFS(TreeNode* root) {
    if (!root) return 0;
    queue<TreeNode*> q;
    q.push(root);
    int height = 0;
    while (!q.empty()) {
        int sz = q.size();
        height++;
        for (int i = 0; i < sz; i++) {
            auto node = q.front(); q.pop();
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }
    return height;
}
```
This is $O(N)$ time and $O(W)$ space (max width of tree).

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 104 | Maximum Depth of Binary Tree | Bottom-up height recursion |
| 110 | Balanced Binary Tree | Single-pass O(N) with sentinel -1 |
| 222 | Count Complete Tree Nodes | O(log² N) perfect-subtree detection |
| 111 | Minimum Depth of Binary Tree | BFS (first level with a leaf) |

---

## 🔗 Cross-Topic Connections
- **Height** is the core subroutine in **Diameter of Binary Tree** (bottom-up postorder)
- **countNodes** pattern reused in **Largest BST in Binary Tree** (size tracking)
- **Height of BST** determines all BST operation costs (search, insert, delete)
- **Complete binary tree** height property: $H = \lfloor \log_2 N \rfloor$

---

## ⚡ 2-Minute Revision Flash Card
- **Height formula:** `1 + max(height(left), height(right))`; null returns 0
- **Height ≠ Depth:** Height = downward to leaf; Depth = upward to root
- **Leaf height:** 1 (node-count) or 0 (edge-count) — know both conventions
- **Complete BT node count:** O(log² N) by detecting perfect subtrees
- **Balanced check:** Do it in O(N) — combine height + balance check in single pass
