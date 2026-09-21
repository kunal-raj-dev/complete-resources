# Lecture 103: Lowest Common Ancestor in BST (LeetCode 235)

> **One-Line Purpose:** Locate the Lowest Common Ancestor in $O(H)$ time and $O(1)$ space by finding the first node where paths to $p$ and $q$ diverge.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #103  
> **Video ID:** `ORxkZ12FrU4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=ORxkZ12FrU4)  
> **Duration:** 12:29  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Understand the property of Lowest Common Ancestor (LCA) specifically in a Binary Search Tree context.
- Exploit the BST invariant to avoid the $O(N)$ post-order traversal used for generic binary trees.
- Implement the $O(1)$ space iterative traversal by following the divergence point.

## 🧠 Core Intuition — Why This Works
The Lowest Common Ancestor (LCA) is the node where the paths to $p$ and $q$ **diverge** (split).
Because it's a **Binary Search Tree**, we know exactly where nodes are located relative to any root:
- If **both** $p$ and $q$ are smaller than the current root, they are **both** in the left subtree. So we move left.
- If **both** $p$ and $q$ are greater than the current root, they are **both** in the right subtree. So we move right.
- If one is smaller and one is greater (or if one equals the current node), the paths **diverge right here**. This current node is mathematically guaranteed to be the LCA!

**Visualization:**
```text
       6
     /   \
    2     8
   / \   / \
  0   4 7   9
     / \
    3   5
```
Find LCA of `3` and `5`:
- Root is `6`. Both `3` and `5` are $< 6$. Move left to `2`.
- Node is `2`. Both `3` and `5` are $> 2$. Move right to `4`.
- Node is `4`. `3 < 4` and `5 > 4`. Divergence! `4` is the LCA.

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Lowest Common Ancestor" + "Binary Search Tree" → **Divergence point logic ($O(H)$ time)**
- Any problem asking to find a shared ancestor in a sorted tree structure.

## 📐 Algorithm Walk-Through
1. Initialize a pointer `curr` to the `root`.
2. Loop while `curr` is not null:
3. **Left Heavy:** If `p->val < curr->val` AND `q->val < curr->val`, both targets are to the left. Update `curr = curr->left`.
4. **Right Heavy:** If `p->val > curr->val` AND `q->val > curr->val`, both targets are to the right. Update `curr = curr->right`.
5. **Divergence (Else):** If one is less and one is greater, OR if one of the targets equals `curr->val`, we have found the split point. Return `curr`.

## 🔵 Optimal Iterative $O(1)$ Space Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionBSTLCA {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        TreeNode* curr = root;

        while (curr) {
            if (p->val < curr->val && q->val < curr->val) {
                curr = curr->left; // Both targets lie in left subtree
            } else if (p->val > curr->val && q->val > curr->val) {
                curr = curr->right; // Both targets lie in right subtree
            } else {
                return curr; // Targets diverge; curr is LCA!
            }
        }
        return nullptr;
    }
};
```

## 🔍 Dry Run Trace
**Finding LCA of 2 and 4:**
```text
       6
     /   \
    2     8
     \
      4
```
1. `curr = 6`. 
   - `2 < 6` and `4 < 6`. Both are smaller.
   - `curr = curr->left` $\rightarrow 2$.
2. `curr = 2`.
   - `p (2) == curr (2)`. Neither of the `<` or `>` condition pairs are fully satisfied.
   - Falls into the `else` block. 
   - Returns `2`. (Node 2 is an ancestor of Node 4).

## ⚠️ Common Interview Mistakes
- **Using Generic Binary Tree LCA:** Implementing the standard binary tree LCA algorithm, which takes $O(N)$ time and $O(N)$ space. In a BST, you must exploit the sorted property to get $O(H)$ time and $O(1)$ space.
- **Overcomplicating the Divergence Condition:** Writing `if ((p < curr && q > curr) || (p > curr && q < curr) || p == curr || q == curr)`. This is unnecessary. Just use an `else` block after checking the two "both strictly less" and "both strictly greater" conditions.
- **Assuming $p < q$:** Assuming that $p$ is always the smaller value. The conditions must be written safely regardless of which is smaller.

## 📊 Complexity Analysis
- **Time Complexity:** $O(H)$ where $H$ is the height of the tree. In the worst case (skewed tree), it's $O(N)$. In a balanced tree, it's $O(\log N)$. We traverse downwards only.
- **Space Complexity:** $O(1)$ strictly. We only use a single `curr` pointer, unlike the recursive approach which would use $O(H)$ call stack space.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] Can a node be an ancestor of itself?
**Answer:** Yes, according to the standard definition used in LCA problems, a node is considered a descendant (and ancestor) of itself. This is why if `curr` matches either $p$ or $q$, the `else` block correctly triggers and returns `curr`.

### Q2: [Complexity] Why is the iterative approach preferred over the recursive one for this specific problem?
**Answer:** The recursive approach does exactly the same operations but consumes $O(H)$ memory on the call stack. Since this algorithm is entirely tail-recursive (the recursive call is the very last operation), it can easily be converted to a `while` loop, dropping the space complexity to $O(1)$ while maintaining readability.

### Q3: [Edge Case] What if $p$ or $q$ is not present in the tree?
**Answer:** The standard algorithm assumes both nodes are guaranteed to exist in the BST. If they are not guaranteed to exist, this algorithm might return a node that *would* be the split point if they did exist. To handle missing nodes, you would either need a separate search to verify their existence first, or use a slightly modified post-order approach.

### Q4: [Variant] How would this change if it were an N-ary Search Tree?
**Answer:** The logic remains the same. You would iterate through the child pointers of `curr`, and follow the single child whose subtree encompasses the range covering both $p$ and $q$. If $p$ and $q$ fall into different subtrees of `curr`, then `curr` is the LCA.

## 🏆 Related Problems (Leetcode)
- **Leetcode 235:** Lowest Common Ancestor of a Binary Search Tree (Medium)
- **Leetcode 236:** Lowest Common Ancestor of a Binary Tree (Medium) - *The generic version*
- **Leetcode 1644:** Lowest Common Ancestor of a Binary Tree II (Medium) - *Nodes not guaranteed to exist*

## 🔗 Cross-Topic Connections
- **Generic Tree LCA:** Contrasts with generic LCA which requires a bottom-up post-order traversal to bubble up matching nodes.
- **Binary Search:** Uses the exact same elimination logic to discard halves of the search space.

## ⚡ 2-Minute Revision Flash Card
- **Concept:** LCA is the divergence point.
- **If both < root:** Go left.
- **If both > root:** Go right.
- **Else (one <, one >, or one == root):** You are at the LCA. Return root.
- **Space:** Do it iteratively for $O(1)$ space.
