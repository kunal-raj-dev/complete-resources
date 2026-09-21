# 💼 Topic 17 Interview Question Bank: Binary Trees

> **Curated FAANG Interview Bank:** High-frequency tree challenges, memory topologies, and recursion bounds.

---

## 📌 Conceptual & Architectural Questions

### Q1: How does Morris Traversal achieve $O(1)$ space without altering the original tree structure?
- **Answer:** Morris Traversal temporarily threads the `right` pointer of the inorder predecessor back to the current node. On the second visit, it detects that `pred->right == curr`, restores the pointer to `nullptr`, and visits the current node. Because every created thread is removed before the algorithm finishes, the original tree topology is completely preserved.

### Q2: Why does computing the diameter naively take $O(N^2)$ while bottom-up takes $O(N)$?
- **Answer:** The naive algorithm calls `height(left)` and `height(right)` at every node. Since `height()` visits the entire subtree ($O(k)$), the recurrence is $T(N) = 2T(N/2) + O(N) = O(N^2)$ in unbalanced trees. The bottom-up approach returns height directly alongside diameter calculation, visiting each node exactly once for $O(N)$.

### Q3: What is the difference between Top View and Bottom View logic?
- **Answer:** Both use BFS level-order traversal with a horizontal distance (HD) map. For Top View, we only add a node to the map if its HD is not already present (first node seen at that HD). For Bottom View, we constantly overwrite the map value for an HD so that the last node seen at that HD is kept.

### Q4: Why can't a Binary Tree be uniquely constructed from Preorder and Postorder traversals?
- **Answer:** To uniquely construct a tree, you need to know the boundary between the left and right subtrees. Inorder traversal explicitly places the root between the left and right subtrees. Preorder (Root, Left, Right) and Postorder (Left, Right, Root) do not provide a clear delimiter when a node has only one child. If a node has only one child, you cannot determine if that child is a left or right child from Preorder and Postorder alone.

### Q5: How would you serialize and deserialize a Binary Tree?
- **Answer:** Serialize using Preorder traversal, appending a special marker (like `#` or `N`) for `nullptr`. E.g., `1,2,N,N,3,N,N`. To deserialize, split the string by commas and use a recursive function that builds nodes in Preorder. When it hits a marker, it returns `nullptr`.

### Q6: Can a Binary Tree have an $O(N)$ height but still be traversed in $O(\log N)$ space?
- **Answer:** Standard DFS space complexity is strictly bounded by the height of the tree, $O(H)$. If the tree is a completely skewed list, $H = N$, so space is $O(N)$. To achieve $O(\log N)$ or $O(1)$ space on an $O(N)$ height tree, you must use Morris Traversal, which modifies the tree pointers temporarily to avoid the call stack altogether.

### Q7: When finding the Lowest Common Ancestor (LCA), why do we assume the nodes exist in the tree?
- **Answer:** The standard $O(N)$ single-pass LCA algorithm returns `root` if it matches either $p$ or $q$. If $p$ is in the tree and $q$ is not, it might return $p$, incorrectly assuming $q$ is in $p$'s subtree. If it's not guaranteed both nodes exist, you must either search for both nodes first (two passes), or modify the LCA function to keep boolean flags tracking if $p$ and $q$ were actually found during the traversal.

### Q8: What is the primary advantage of BFS over DFS when searching for a target node in a massive tree?
- **Answer:** If the target node is relatively close to the root (e.g., at depth 5 in a tree of depth 1000), BFS will find it in $O(2^5) = O(1)$ time, whereas DFS might go down a deep wrong branch of depth 1000 first, wasting massive time and stack space. BFS guarantees finding the shortest path in unweighted graphs/trees. DFS is better when the target is deep and the tree is wide, to save queue memory.

### Q9: Can you construct a unique Binary Tree given only its Pre-order and Post-order traversals?
- **Answer:** No. You can only construct a unique binary tree if you have In-order traversal paired with either Pre-order or Post-order. Pre-order + Post-order is ambiguous for nodes with only one child (you cannot tell if it is a left child or a right child). If the tree is strictly a Full Binary Tree (every node has 0 or 2 children), then Pre+Post *can* uniquely identify it.

### Q10: How do you serialize and deserialize a binary tree?
- **Answer:** We can serialize using any traversal (like BFS or Pre-order DFS), but we *must* explicitly record `NULL` pointers (usually as a string like `"#"`) to preserve the structure. For example, in Pre-order, if a node is null, we append `"#,"`. During deserialization, we split the string and recursively build the tree, returning `nullptr` when we encounter `"#"`.

### Q11: What is a Threaded Binary Tree (Morris Traversal)?
- **Answer:** A Threaded Binary Tree modifies the `nullptr` right-child pointers of leaf nodes to point to their In-order Successor. This enables $O(1)$ space In-order traversal (Morris Traversal) because we can navigate back up the tree without a stack. We temporarily create these threads during traversal and break them once we've visited the parent.

### Q12: Why is the recursion depth $O(N)$ in the worst case for a Binary Tree, but $O(\log N)$ for a Balanced Binary Tree?
- **Answer:** If the tree is entirely skewed (every node only has a right child, forming a linked list), the recursion must go $N$ levels deep before hitting the base case, requiring $N$ stack frames. In a perfectly balanced tree, the depth halves at every level, meaning the deepest leaf is exactly $\log_2(N)$ levels down.

### Q13: What is the difference between a Full Binary Tree, a Complete Binary Tree, and a Perfect Binary Tree?
- **Answer:** 
  - **Full:** Every node has either 0 or 2 children.
  - **Complete:** All levels are completely filled except possibly the last, which is filled from left to right (this is the structure of a Heap).
  - **Perfect:** All internal nodes have 2 children, and all leaves are at the exact same depth. $N = 2^{H+1} - 1$.
