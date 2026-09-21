# ⚡ Topic 18 Revision: Binary Search Trees (BSTs)

> **High-Density Review:** BST invariant mechanics, search/insert/delete operations, range validation, balancing transforms, and bottom-up subtree attributes.

---

## 1. BST Core Invariants & Operations
- **Inorder Property:** Inorder traversal of a valid BST is strictly sorted in ascending order.
- **Search & Insert:** $O(H)$ where $H = \log_2 N$ (Balanced / AVL / Red-Black) and $H = N$ (Skewed).
- **Deletion (3 Cases):**
  1. **Leaf Node:** Delete directly; return `nullptr`.
  2. **One Child:** Return non-null child to parent.
  3. **Two Children:** Replace node's value with its **Inorder Successor** (smallest in right subtree), then recursively delete successor.

---

## 2. Validation & Range Propagation
- Always validate BSTs by propagating `(minVal, maxVal)` using 64-bit `long long` bounds (`LLONG_MIN` and `LLONG_MAX`) to prevent edge collisions on `INT_MIN` / `INT_MAX`.
```cpp
bool validate(TreeNode* node, long long minVal, long long maxVal) {
    if (!node) return true;
    if (node->val <= minVal || node->val >= maxVal) return false;
    return validate(node->left, minVal, node->val) && validate(node->right, node->val, maxVal);
}
```

---

## 3. Key Patterns & Complexities

| Problem | Algorithm / Technique | Time | Space | Key Invariant |
|---|---|---|---|---|
| **Sorted Array to Balanced BST**| Divide & conquer midpoint | $O(N)$ | $O(\log N)$ | `mid = (L + R) / 2` becomes root |
| **Validate BST** | Range propagation bounds | $O(N)$ | $O(H)$ | Node must fall in $(minVal, maxVal)$ |
| **Kth Smallest in BST** | Inorder counter traversal | $O(H + K)$| $O(H)$ | Inorder visits in sorted order |
| **LCA in BST** | Value splitting decision | $O(H)$ | $O(1)$ | Split point where $p \le root \le q$ |
| **Largest BST in BT** | Bottom-up Quad-Tuple | $O(N)$ | $O(H)$ | Returns `{isBST, size, minVal, maxVal}` |
| **Recover BST** | Inorder pointer tracking | $O(N)$ | $O(1)$ Morris | Swap two misplaced nodes |
| **BST Iterator** | Controlled Inorder Stack | $O(1)$ avg | $O(H)$ | Stack holds left spine |

---

## 4. Key Takeaways
1. **Inorder is King:** Almost all problems involving finding next/previous elements, sorted order, or checking validity in a BST can be simplified using inorder traversal concepts.
2. **LCA Logic:** Unlike generic Binary Trees that need post-order traversal to find LCA, a BST can find LCA top-down in $O(H)$ because the first node that lies *between* values `p` and `q` is guaranteed to be their LCA.
3. **Pointers for Structure Modification:** When inserting or deleting, ensure you link the result of the recursive call back to `root->left` or `root->right` to physically stitch the modified subtree back together.

---

## 5. Iterative Tricks (Morris Traversal & BST Iterator)
- To avoid $O(H)$ stack space during Inorder Traversal, we can build a **BST Iterator** that lazily pushes only the left spine of the current node to a stack. `next()` takes amortized $O(1)$ time and uses $O(H)$ space.
- To achieve strictly $O(1)$ space, use **Morris Traversal**, which temporarily sets the right child of the inorder predecessor to point to the current root (Threaded Binary Tree).

## 6. Mathematical BST Validations
- A BST can be validated iteratively by performing an Inorder Traversal and strictly checking `curr->val > prev->val`.
- A BST can be validated recursively by passing down dynamic bounds: `isValid(node->left, minBoundary, node->val)` and `isValid(node->right, node->val, maxBoundary)`.

## 7. Segment Trees / Fenwick Trees vs BST
- Remember that a BST is optimized for dynamic searches and ordered extraction. If the problem asks for **Range Sum Queries** or **Point Updates** in an array, a Segment Tree or Fenwick Tree is mathematically superior and strictly $O(\log N)$ guaranteed, whereas a raw BST might degrade to $O(N)$ unless it's an AVL/Red-Black Tree.

## ⚡ 2-Minute Revision Flash Card
- BST Property: Left < Root < Right.
- Inorder Traversal of a BST yields a sorted array.
- Searching/Insertion takes $O(\log N)$ average, $O(N)$ worst (skewed tree).
- To delete a node with two children, replace it with its Inorder Successor (min in right subtree) or Inorder Predecessor (max in left subtree).
