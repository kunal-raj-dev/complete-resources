# Lecture 91: Lowest Common Ancestor in Binary Tree (LeetCode 236)

> **One-Line Purpose:** Find the deepest common ancestor of two nodes in an arbitrary binary tree via postorder path branching logic.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #91  
> **Video ID:** `oX5D0uKOMck`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=oX5D0uKOMck)  
> **Duration:** 18:20  
> **Status:** AUDITED  

---

## 🧠 Core Intuition — Why This Works

The **Lowest Common Ancestor (LCA)** of two nodes p and q is the deepest node that has both p and q as descendants (where a node is a descendant of itself).

**Real-world analogy:** You and a friend both share a great-grandparent. The "lowest common ancestor" in your family tree is the most recent common ancestor — not some ancient ancestor 50 generations back. In a tree, it's the deepest shared ancestor.

**The postorder branching logic:**
1. If you find `p` or `q`, return that node. You don't need to search deeper (if the other node is below p, then p IS the LCA).
2. After recursing left and right:
   - If both left and right return non-null → p and q are in DIFFERENT subtrees → **current node is the LCA**
   - If only one side returns non-null → both p and q are in that same subtree → **bubble that result up**

```
Tree:         3
            /   \
           5     1
          / \   / \
         6   2 0   8
            / \
           7   4

LCA(5, 4):
  - Search left subtree of 3: finds 5 at the root of left subtree
  - When recursing into 5's subtree: finds 4 (via 2→4)
  - Since 5 is found at the root before reaching 4, return 5
  LCA = 5

LCA(5, 1):
  - Left subtree of 3 finds 5 → returns 5
  - Right subtree of 3 finds 1 → returns 1
  - Both sides non-null → LCA = 3
```

---

## 🎯 Pattern Recognition — When to Use This

- "Lowest/deepest common ancestor" → this algorithm
- "Find the meeting point of two paths" → LCA
- "Distance between two nodes" → Find LCA first, then compute distance
- If it's a BST → use BST-specific O(H)/O(1) space algorithm (Lecture 103)

---

## 🔵 Complete C++ Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionLCA {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root || root == p || root == q) {
            return root;
        }

        TreeNode* leftSub = lowestCommonAncestor(root->left, p, q);
        TreeNode* rightSub = lowestCommonAncestor(root->right, p, q);

        if (leftSub && rightSub) {
            return root; // p and q found in different subtrees; current node is LCA!
        }

        return leftSub ? leftSub : rightSub;
    }
};
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$.

---

## 🔍 Dry Run Trace

```
LCA(root=3, p=5, q=1):
  LCA(5, p=5, q=1): root==p → return 5
  LCA(1, p=5, q=1): root==q → return 1
  leftSub=5, rightSub=1 → both non-null → return 3 (LCA)

LCA(root=3, p=6, q=4):
  LCA(5, p=6, q=4):
    LCA(6, p=6, q=4): root==p → return 6
    LCA(2, p=6, q=4):
      LCA(7, ...) → null
      LCA(4, p=6, q=4): root==q → return 4
      leftSub=null, rightSub=4 → return 4
    leftSub=6, rightSub=4 → both non-null → return 5
  LCA(1, p=6, q=4): → null (neither 6 nor 4 is in right subtree)
  leftSub=5, rightSub=null → return 5 (LCA)
```

---

## ⚠️ Common Interview Mistakes

1. **Assuming both nodes exist:** The standard LCA algorithm assumes both p and q are guaranteed to be in the tree. If either doesn't exist, the algorithm returns incorrect results (see Q5 below).

2. **Returning root when only one of p/q is found:** This is actually CORRECT — if the code finds p and returns p, it's because q is either not in the tree OR q is a descendant of p (making p the LCA). The single-return propagation handles both cases.

3. **Confusing General Tree LCA with BST LCA:** For a BST, you can use value comparisons. For a general binary tree, you must do a full postorder search.

4. **Not resetting mutable state:** If using global variables instead of return values, ensure they're reset between calls.

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$ — worst case visits every node.
- **Space Complexity:** $O(H)$ — recursion stack depth.
  - Balanced: $O(\log N)$
  - Skewed: $O(N)$

---

## 🔥 Interview Q&A — Google / Amazon / Meta Level

### Q1: [Conceptual] What is the key difference between LCA in a BST vs a general binary tree?
**Answer:** 
- **General Binary Tree:** No structural ordering information. Must perform a full $O(N)$ search, checking all subtrees. The postorder approach works by returning the first found node and checking if both sides are non-null.
- **BST:** The ordering property (`left < root < right`) allows us to navigate with value comparisons: if both p and q are less than root, go left; if both are greater, go right; otherwise, the root IS the LCA. This achieves $O(H)$ time and $O(1)$ space (iteratively), vs $O(N)$ time and $O(H)$ space for general trees.

### Q2: [Extension] What is the relationship between LCA and distance between two nodes?
**Answer:** Distance between nodes p and q = number of edges in the path p→q. This path goes: p → LCA(p,q) → q. Therefore:
$$\text{dist}(p, q) = \text{depth}(p) + \text{depth}(q) - 2 \times \text{depth}(\text{LCA}(p, q))$$
Where $\text{depth}(x)$ = number of edges from root to x. So to find distance: (1) find LCA, (2) find depth of p, q, and LCA from the root, (3) apply the formula. All steps are $O(N)$.

### Q3: [Tricky] What if one of the nodes (p or q) doesn't exist in the tree? Does the algorithm still work?
**Answer:** **No.** The standard algorithm returns `p` if it finds `p` without checking if `q` exists anywhere. For example, if the tree has p but not q: the algorithm returns p (incorrectly — should return null). To handle this, use a pair `{node, count}` where count tracks how many of {p, q} were found. Only return the LCA if count == 2:
```cpp
pair<TreeNode*, int> lcaSafe(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root) return {nullptr, 0};
    auto [leftNode, leftCount] = lcaSafe(root->left, p, q);
    if (leftCount == 2) return {leftNode, 2};
    auto [rightNode, rightCount] = lcaSafe(root->right, p, q);
    if (rightCount == 2) return {rightNode, 2};
    int count = leftCount + rightCount + (root == p) + (root == q);
    return {count == 2 ? root : (leftNode ? leftNode : rightNode), count};
}
```

### Q4: [Deep Dive] Can a node be its own LCA? When?
**Answer:** Yes! If p is an ancestor of q (or vice versa), then p is the LCA of p and q. Example: in a tree 1→2→3, `LCA(1, 3) = 1`. The algorithm handles this correctly: when it reaches node p (=1), it immediately returns p without descending further. Node q (=3) is somewhere in 1's subtree, but since we found p first, p is correctly identified as the LCA.

### Q5: [System Design] If LCA queries are going to be issued frequently for a large static tree, how would you preprocess?
**Answer:** Use **Euler Tour + Range Minimum Query (RMQ)** for $O(N)$ preprocessing and $O(1)$ per query:
1. Perform an Euler tour of the tree, recording the sequence of nodes visited.
2. Build a sparse table (RMQ structure) over the depths in this sequence.
3. LCA(p, q) = the node with minimum depth between the first occurrence of p and the first occurrence of q in the Euler tour array.
Alternative: Binary Lifting (sparse table of ancestors) — $O(N \log N)$ preprocessing, $O(\log N)$ per query.

### Q6: [Output Prediction] What does the algorithm return for `LCA(root, p=root, q=root)` where root is a single node?
**Answer:** It returns `root`. The base case `if (!root || root == p || root == q) return root;` triggers immediately for both `root == p` and `root == q`. The function returns root at the very first check. ✓

### Q7: [Extension] How do you find the LCA of multiple nodes (not just two)?
**Answer:** Generalize: traverse the tree and return a node if it matches ANY of the target nodes. The LCA of the collection is the deepest ancestor that "sees" all target nodes across its subtrees. Algorithm: track a `count` — the number of targets found. When count equals the target set size, that node is the LCA.

### Q8: [Proof] Why does returning `leftSub ? leftSub : rightSub` correctly propagate the LCA?
**Answer:** At any node, one of three cases holds:
- `leftSub && rightSub` → p is in left, q is in right (or vice versa) → current node = LCA. Return current node.
- Only `leftSub` is non-null → both p and q are in the left subtree (the LCA is leftSub itself, already found) → propagate leftSub upward unchanged.
- Only `rightSub` is non-null → symmetric case → propagate rightSub.

The key insight: once the LCA is found at some node, it gets returned upward unchanged all the way to the root, because every ancestor will have exactly one non-null child and will return it directly.

---

## 🏆 Related LeetCode Problems

| # | Problem | Key Approach |
|---|---|---|
| 236 | LCA of Binary Tree | Postorder return-based search |
| 235 | LCA of BST | Value comparison, O(H) iterative |
| 1650 | LCA with Parent Pointers | Two-pointer / hash set of ancestors |
| 1123 | Deepest Leaves Common Ancestor | LCA of all deepest leaves |

---

## 🔗 Cross-Topic Connections
- **BST LCA (Lecture 103):** Same concept but O(H) using value navigation
- **Distance between nodes:** `dist = depth(p) + depth(q) - 2*depth(LCA)`
- **Diameter of Binary Tree:** The diameter passes through the LCA of the two endpoints
- **Path between nodes:** path = (root to p) + (root to q) - 2*(root to LCA)

---

## ⚡ 2-Minute Revision Flash Card
- **LCA Logic:** Postorder; return node if it's p or q; if both children non-null, current = LCA
- **BST LCA:** O(H) using value comparisons (go left if both < root, right if both > root)
- **LCA + distance formula:** `dist(p,q) = depth(p) + depth(q) - 2*depth(LCA)`
- **Node can be its own LCA:** if p is ancestor of q, LCA(p,q) = p ✓
- **If nodes may not exist:** Track count of found targets; return LCA only if count == 2
