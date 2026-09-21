# 💼 Topic 18 Interview Question Bank: Binary Search Trees

> **Curated FAANG Interview Bank:** High-frequency BST questions, self-balancing mechanics, and range queries.

---

## 📌 Conceptual & Architectural Questions

### Q1: Why must BST Validation use `long long` bounds instead of `INT_MIN` / `INT_MAX`?
- **Answer:** A valid node value can be `INT_MIN` or `INT_MAX`. If the initial bounds are `INT_MIN` and `INT_MAX`, the check `node->val <= minVal` will fail on a valid root containing `INT_MIN`. Using `LLONG_MIN` and `LLONG_MAX` provides safety against boundary collisions.

### Q2: How does a BST Iterator achieve amortized $O(1)$ time per `next()` call?
- **Answer:** The iterator pushes all left children of the current node onto a stack. While some individual `next()` calls push $O(H)$ nodes, every tree node is pushed onto the stack exactly once and popped exactly once across the full tree iteration. Hence, for $N$ `next()` invocations, total operations are $2N$, yielding amortized $O(1)$ per call.

### Q3: What is the difference between a BST and a Binary Heap?
- **Answer:** A BST is designed for searching, maintaining the invariant that left children are smaller and right children are larger than the parent, allowing $O(\log N)$ search, insertion, and deletion on average. A Binary Heap (Min or Max Heap) only guarantees that a parent is smaller (or larger) than its children, without distinguishing left and right ordering. Heaps are designed for $O(1)$ access to the extremum element and are always complete binary trees, typically implemented using arrays. 

### Q4: How would you find the inorder successor of a node in a BST without parent pointers?
- **Answer:** Start from the root. If the target node's value is less than the root's value, the root is a potential successor, so remember the root and move left. If the target node's value is greater than or equal to the root's value, move right. If the target node has a right child, its successor is the minimum value in its right subtree. This takes $O(H)$ time.

### Q5: Can we construct a unique BST from its Postorder traversal?
- **Answer:** Yes. The last element of the Postorder traversal is the root. By iterating backwards, the next elements that are greater than the root belong to the right subtree, and elements smaller belong to the left subtree. We can recursively construct the tree using $O(N)$ time by maintaining valid `min` and `max` bounds, similar to BST validation.

### Q6: What is a Self-Balancing BST and name two implementations?
- **Answer:** A Self-Balancing BST automatically adjusts its structure during insertions and deletions to maintain a height of $O(\log N)$, preventing worst-case $O(N)$ operations. The two most common implementations are AVL Trees (strictly balanced, faster lookups) and Red-Black Trees (loosely balanced, faster insertions/deletions, used in `std::map` and `std::set`).

### Q7: If you wanted to find the total number of elements in a BST in range `[L, R]`, how could you optimize it?
- **Answer:** Standard DFS traversal checking range takes $O(N)$. If we augment the BST node to store the `size` of its subtree, we can answer range queries in $O(\log N)$ time by counting elements strictly less than `L` and subtracting them from elements less than or equal to `R`.

### Q8: Why does deleting a node with two children require finding the Inorder Successor or Predecessor?
- **Answer:** A node with two children cannot simply be removed because its two subtrees would be left disconnected, and a binary tree node can only hold one value. By swapping the node's value with its Inorder Successor (the smallest value in its right subtree), we preserve the BST property. The Successor is guaranteed to have at most one child (since it's the minimum, it has no left child), making the subsequent recursive deletion trivial.

### Q9: How can you convert a sorted Doubly Linked List (DLL) into a Balanced BST in $O(N)$ time and $O(\log N)$ space?
- **Answer:** We can simulate an Inorder Traversal. We maintain a global pointer to the head of the DLL. We recursively build the left subtree using the first $N/2$ elements, then allocate the root using the current DLL node, advance the global DLL pointer, and recursively build the right subtree. This constructs the tree bottom-up.

### Q10: What is the difference between an AVL Tree and a Red-Black Tree?
- **Answer:** Both are self-balancing BSTs. AVL Trees maintain a stricter balance (height difference of at most 1), leading to faster lookups ($O(\log N)$ with a smaller constant factor) but more rotations during insertions/deletions. Red-Black Trees have looser balancing rules (longest path is at most twice the shortest), resulting in fewer rotations and faster insertions/deletions. `std::set` and `std::map` in C++ use Red-Black Trees.

### Q11: Can a BST contain duplicate values? How do you handle them?
- **Answer:** Strictly speaking, standard mathematical BSTs do not allow duplicates. However, if duplicates are required, they can be handled in two ways: 
  1. Add a `count` frequency variable to the `TreeNode` struct (best approach to preserve $O(\log N)$ search).
  2. Adopt a convention (e.g., all duplicates go to the right subtree `node->val >= root->val`), though this can severely skew the tree if many duplicates exist.

### Q12: How do you verify if an array represents the Preorder traversal of a valid BST?
- **Answer:** We can use a monotonic stack. We iterate through the array, and if we encounter an element smaller than the currently recorded "lower bound", it's invalid. If we see an element larger than the top of the stack, we pop elements from the stack (since we are moving to right subtrees) and update our lower bound to the last popped element. Takes $O(N)$ time.
