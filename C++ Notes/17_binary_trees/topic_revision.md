# ⚡ Topic 17 Revision: Binary Trees

> **High-Density Review:** Tree traversals, diameter bottom-up patterns, view coordinate systems, and Morris $O(1)$ threading.

---

## 1. Traversals Cheat Sheet
- **Preorder:** Root $\to$ Left $\to$ Right (Serialization, Prefix notation)
- **Inorder:** Left $\to$ Root $\to$ Right (Sorted order in BST)
- **Postorder:** Left $\to$ Right $\to$ Root (Bottom-up deletion, Tree height/diameter)
- **Level Order:** FIFO Queue BFS (Top view, Level-by-level metrics)

---

## 2. Invariant Table

| Problem | Algorithm | Time | Space | Key Formula / Invariant |
|---|---|---|---|---|
| **Tree Diameter** | Bottom-Up DFS | $O(N)$ | $O(H)$ | $\text{diameter} = \max(\text{diam}, lh + rh)$ |
| **Top View** | BFS + Coordinate Map | $O(N \log N)$ | $O(N)$ | First node encountered at each $\text{HD}$ |
| **LCA** | Post-order Search | $O(N)$ | $O(H)$ | If left and right both non-null, root is LCA |
| **Morris Inorder** | Threaded Tree | $O(N)$ | $O(1)$ aux | Temporary thread `pred->right = curr` |
| **Sum Tree** | Post-order DFS | $O(N)$ | $O(H)$ | `root->val = sum(left) + sum(right)` |
| **Level Order** | Queue BFS | $O(N)$ | $O(W)$ | Push children; process current level size |

---

## 3. Quick Code Snippets

**Tree Node Structure:**
```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
```

**Bottom-Up Height (Base for Diameter/Balanced Tree checks):**
```cpp
int height(TreeNode* root) {
    if (!root) return 0;
    int lh = height(root->left);
    int rh = height(root->right);
    // Do something with lh and rh here
    return 1 + max(lh, rh);
}
```

**BFS Level Order Core Loop:**
```cpp
queue<TreeNode*> q;
q.push(root);
while(!q.empty()) {
    int size = q.size();
    for(int i = 0; i < size; i++) {
        TreeNode* node = q.front(); q.pop();
        if(node->left) q.push(node->left);
        if(node->right) q.push(node->right);
    }
}
```

---

## 4. Key Patterns to Remember
1. **Top-Down vs Bottom-Up:** If you need information from parents, pass it down as parameters (top-down). If you need information from children to decide parent's fate, use post-order and return it up (bottom-up).
2. **Global Variable vs Return Tuple:** When you need to compute something like Diameter, you can either keep a global/reference `max_diam` variable updated during a standard `height()` function, or return a `pair<int, int>` (height, diameter) from every call.
3. **Horizontal Distance (HD):** Any problem asking for "Vertical Order", "Top View", or "Bottom View" maps exactly to tracking `HD` where `left child = HD - 1` and `right child = HD + 1`. Map `HD` to node values.
## 5. Tree DP (Dynamic Programming on Trees)
- **Concept:** Returning multiple pieces of state up from children to parent to solve a global problem (e.g., Diameter, Largest BST).
- **Implementation:** Always use a struct (e.g., struct TreeInfo { int height, int diameter; }) and a Post-Order traversal.

## 6. Iterative Traversals (Stack-Based)
- **Pre-Order (N-L-R):** Push Right child first, then Left child. (So Left is popped first).
- **In-Order (L-N-R):** Go deep left pushing to stack. Pop, process, then step one right.
- **Post-Order (L-R-N):** Use two stacks, or one stack tracking previous visited node. Alternatively, do N-R-L (like Pre-Order but reversed pushes) and reverse the final array.

## 7. Segment Trees / Fenwick Trees vs BST
- Remember that a BST is optimized for dynamic searches and ordered extraction. If the problem asks for **Range Sum Queries** or **Point Updates** in an array, a Segment Tree or Fenwick Tree is mathematically superior and strictly (\log N)$ guaranteed, whereas a raw BST might degrade to (N)$ unless it's an AVL/Red-Black Tree.
