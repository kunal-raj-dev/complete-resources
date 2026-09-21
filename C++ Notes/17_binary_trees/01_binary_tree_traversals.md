# Lecture 85: Binary Trees: Node Model & Traversals (DFS & BFS)

> **One-Line Purpose:** Master the recursive hierarchical tree topology and implement Preorder, Inorder, Postorder, and Level-Order (BFS) traversals in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #85  
> **Video ID:** `eKJrXBCRuNQ`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=eKJrXBCRuNQ)  
> **Duration:** 01:14:15  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

Think of a binary tree like a **family genealogy chart**. The traversal order determines whose story you tell first:
- **Preorder (Root→Left→Right):** Like a manager briefing before delegating — you deal with yourself before your reports. Used for **cloning/serializing** a tree.
- **Inorder (Left→Root→Right):** A middle child narrative — Left sibling, then you, then right sibling. In a **BST, this gives sorted order** — the single most important property in tree interviews.
- **Postorder (Left→Right→Root):** A contractor who cleans up children's rooms before leaving their own. Used for **deletion** and computing **height/diameter** bottom-up.
- **Level Order (BFS):** Ripples spreading outward from a stone dropped in a pond — you visit all nodes at distance 1, then 2, then 3...

```
Tree:         1
            /   \
           2     3
          / \
         4   5

Preorder:   1 → 2 → 4 → 5 → 3   (Root first)
Inorder:    4 → 2 → 5 → 1 → 3   (Left subtree, root, right subtree)
Postorder:  4 → 5 → 2 → 3 → 1   (Root last)
LevelOrder: 1 → 2 3 → 4 5        (Level by level)
```

**Key Insight: Why DFS uses Stack/Recursion and BFS uses Queue?**
- DFS explores one path to its deepest point before backtracking. This is LIFO behavior — a stack naturally handles "go deep, then come back." The recursion call stack IS the stack.
- BFS explores all neighbors of a level before going deeper. This is FIFO — process nodes in the order you discovered them. A queue guarantees that.

---

## 🎯 Pattern Recognition — When to Use This

| Traversal | Signal Words | Typical Use |
|---|---|---|
| **Inorder** | "Sorted output", "Kth smallest", "BST validation" | Any problem exploiting BST sorted property |
| **Preorder** | "Serialize", "Copy tree", "Root-to-leaf path prefix" | Saving/reconstructing tree state |
| **Postorder** | "Height", "Diameter", "Delete tree", "Bottom-up aggregation" | Anything requiring child results before parent |
| **Level Order** | "By level", "Zigzag", "Right side view", "Shortest path" | Level-by-level processing |

**Distinguish from similar problems:**
- If you need to process **children before parents** → Postorder
- If you need **sorted values** from a BST → Inorder
- If you need **layer-by-layer** data → BFS/Level Order

---

## 💻 Complete C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class TreeTraversals {
public:
    // Preorder: Root -> Left -> Right
    static void preorder(TreeNode* root) {
        if (!root) return;
        cout << root->val << " ";
        preorder(root->left);
        preorder(root->right);
    }

    // Inorder: Left -> Root -> Right
    static void inorder(TreeNode* root) {
        if (!root) return;
        inorder(root->left);
        cout << root->val << " ";
        inorder(root->right);
    }

    // Postorder: Left -> Right -> Root
    static void postorder(TreeNode* root) {
        if (!root) return;
        postorder(root->left);
        postorder(root->right);
        cout << root->val << " ";
    }

    // Level Order: BFS using Queue
    static vector<vector<int>> levelOrder(TreeNode* root) {
        if (!root) return {};
        vector<vector<int>> result;
        queue<TreeNode*> q;
        q.push(root);

        while (!q.empty()) {
            int size = q.size();
            vector<int> level;

            for (int i = 0; i < size; ++i) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);

                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            result.push_back(level);
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

    cout << "Preorder:  "; TreeTraversals::preorder(root); cout << endl;
    cout << "Inorder:   "; TreeTraversals::inorder(root); cout << endl;
    cout << "Postorder: "; TreeTraversals::postorder(root); cout << endl;
    return 0;
}
```

---

## 💻 Iterative Inorder (Without Recursion) — Morris Teaser

```cpp
// Iterative inorder using explicit stack — O(N) time, O(H) space
vector<int> inorderIterative(TreeNode* root) {
    vector<int> result;
    stack<TreeNode*> st;
    TreeNode* curr = root;

    while (curr || !st.empty()) {
        // Go as far left as possible
        while (curr) {
            st.push(curr);
            curr = curr->left;
        }
        // Process node
        curr = st.top(); st.pop();
        result.push_back(curr->val);
        // Move to right subtree
        curr = curr->right;
    }
    return result;
}
```

---

## 🔍 Dry Run Trace

```
Tree: 1 → left: 2 → right: 3 → 2.left: 4 → 2.right: 5

INORDER trace:
  inorder(1)
    inorder(2)
      inorder(4)
        inorder(null) → return
        PRINT 4
        inorder(null) → return
      PRINT 2
      inorder(5)
        inorder(null) → return
        PRINT 5
        inorder(null) → return
    PRINT 1
    inorder(3)
      inorder(null) → return
      PRINT 3
      inorder(null) → return

Output: 4 2 5 1 3  ✓ (Left subtrees before root, right subtree last)
```

---

## ⚠️ Common Interview Mistakes

1. **Confusing preorder/postorder:** Remember — "POST" = root is LAST. "PRE" = root is FIRST.
2. **Forgetting the null base case:** Every recursive traversal must check `if (!root) return;` first.
3. **Level order without size snapshot:** Not snapshotting `int size = q.size()` before the inner loop. Without it, you can't distinguish level boundaries.
4. **Off-by-one in level-order:** The snapshot `size` must be taken BEFORE the for loop. If you call `q.size()` inside the loop condition, it changes as you push children.
5. **Inorder ≠ Sorted for general trees:** Inorder gives sorted output ONLY for a valid BST.

```cpp
// BUG: This does NOT correctly separate levels
while (!q.empty()) {
    for (int i = 0; i < q.size(); i++) { // q.size() changes! BUG
        ...
    }
}

// CORRECT: Snapshot size before the loop
while (!q.empty()) {
    int size = q.size(); // snapshot
    for (int i = 0; i < size; i++) { ... }
}
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ where $N$ is the number of nodes.
- **Space Complexity:** $O(H)$ recursion stack for DFS, $O(W)$ max level width for BFS.
  - In a balanced tree: $H = O(\log N)$, $W = O(N/2) = O(N)$
  - In a skewed tree: $H = O(N)$, $W = O(1)$
  - BFS worst-case space is $O(N)$ for the last level of a perfect binary tree.

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] When is inorder traversal most useful, and why?
**Answer:** Inorder traversal is most useful for **Binary Search Trees** because it visits nodes in strictly ascending sorted order. This property is exploited in: finding the Kth smallest element (stop at the Kth visited node), validating a BST (check that each visited value is greater than the previous), finding the inorder predecessor/successor, and recovering a corrupted BST (find inversions). For a general binary tree, inorder has no special significance.

### Q2: [Deep Dive] Why does BFS use a Queue while DFS uses a Stack (or recursion)? Prove this isn't arbitrary.
**Answer:** This follows from the **exploration order** each strategy requires:
- BFS processes nodes in **discovery order** — the first node discovered must be the first processed (FIFO). A Queue enforces FIFO. If you used a stack for BFS, you'd get DFS.
- DFS "dives deep" — when you go left, you suspend everything on the right until you've finished the left subtree entirely. This is **LIFO**: the most recently visited (deepest) node is processed next. A stack (or call stack) enforces LIFO.

The data structure IS the algorithm — swap them and you swap the traversal type.

### Q3: [Output Prediction] What does this buggy level-order print?
```cpp
while (!q.empty()) {
    TreeNode* node = q.front(); q.pop();
    cout << node->val << " ";
    if (node->left) q.push(node->left);
    if (node->right) q.push(node->right);
}
```
**Answer:** It prints ALL nodes in level order on a SINGLE line: `1 2 3 4 5`. The bug is that there's no level-separator logic. The code is actually correct BFS, but doesn't distinguish levels. To separate levels, you need the `size` snapshot pattern.

### Q4: [Conceptual] What is the relationship between Preorder and Postorder traversals?
**Answer:** Postorder is approximately the **reverse mirror** of Preorder. If you reverse the Preorder sequence (Root→Left→Right becomes Right→Left→Root) and then mirror-reverse Left/Right, you get Postorder. More precisely: if you do Preorder but visit right before left (Root→Right→Left) and then reverse the entire output, you get Postorder (Left→Right→Root). This is useful for computing iterative postorder using a single stack.

```cpp
// Iterative Postorder using reverse-preorder trick:
// 1. Do "modified preorder" (root, right, left) into a stack
// 2. Pop everything from stack = Postorder
```

### Q5: [Extension] How would you do a zigzag (spiral) level order traversal?
**Answer:** Use a flag `leftToRight` toggled each level. Use `deque` or reverse the level vector when `!leftToRight`. Alternatively, maintain two stacks — one for current level, one for next — and alternate push order.

```cpp
vector<vector<int>> zigzag(TreeNode* root) {
    if (!root) return {};
    vector<vector<int>> res;
    queue<TreeNode*> q;
    q.push(root);
    bool leftToRight = true;
    while (!q.empty()) {
        int sz = q.size();
        vector<int> level(sz);
        for (int i = 0; i < sz; i++) {
            auto node = q.front(); q.pop();
            int pos = leftToRight ? i : (sz - 1 - i);
            level[pos] = node->val;
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        res.push_back(level);
        leftToRight = !leftToRight;
    }
    return res;
}
```

### Q6: [Conceptual] How do you do iterative inorder without recursion in O(H) space?
**Answer:** Use an explicit stack. The algorithm mirrors the call stack of recursive inorder:
1. Push all left children until you hit null.
2. Pop the top (= leftmost unvisited), process it.
3. Move to its right child, and repeat step 1 on the right child.

This is exactly what the call stack does implicitly during recursive inorder. Space is $O(H)$ since at most $H$ nodes are on the stack at once.

### Q7: [Tricky] Can you recover the original tree from just one traversal output?
**Answer:** **No** — a single traversal is insufficient. Preorder `1 2 3` could be a line (1→2→3) or a tree with root 1 having children 2 and 3. You need **two traversals** (e.g., preorder + inorder, or postorder + inorder) to uniquely reconstruct a tree with distinct values. **Exception:** If you also record null nodes (e.g., `1 2 null null 3`), then a single traversal suffices.

### Q8: [System Design] If you had to serialize a binary tree to send over a network, which traversal would you use and why?
**Answer:** **Preorder** with null markers (e.g., `"1,2,null,null,3,null,null"`). Reasons:
- The root appears first, making it trivial to reconstruct: the first element is always the root.
- You can recursively reconstruct left and right subtrees from the remaining sequence.
- BFS serialization also works (used in LeetCode's format) but requires tracking null children explicitly per level.
- Inorder serialization requires inorder + another traversal to reconstruct uniquely.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 144 | Binary Tree Preorder Traversal | Iterative using stack |
| 94 | Binary Tree Inorder Traversal | Iterative stack or Morris O(1) space |
| 145 | Binary Tree Postorder Traversal | Reverse of (Root→Right→Left) preorder |
| 102 | Binary Tree Level Order Traversal | BFS with size snapshot |
| 103 | Binary Tree Zigzag Level Order | BFS with direction flag |

---

## 🔗 Cross-Topic Connections
- **BST + Inorder** → Kth smallest, sorted output, range queries (Topic 18)
- **Postorder** → Used as base for Diameter, Height, LCA, Largest BST subtree
- **BFS/Level Order** → Foundation for Top View, Right Side View, Bottom View
- **Morris Traversal** → Space-optimized inorder used in Recover BST, Flatten to LL (Lecture 96)
- **Preorder** → Serialization, Build tree from Preorder+Inorder (Lecture 92)

---

## ⚡ 2-Minute Revision Flash Card
- **Inorder (L→Root→R):** BST sorted output; use for Kth smallest, BST validation
- **Preorder (Root→L→R):** Serialization; first element = root always
- **Postorder (L→R→Root):** Bottom-up aggregation; use for height, diameter, deletion
- **Level Order:** BFS with queue; ALWAYS snapshot `size = q.size()` before inner loop
- **DFS → Stack (LIFO); BFS → Queue (FIFO)** — swap them and you swap the algorithm
