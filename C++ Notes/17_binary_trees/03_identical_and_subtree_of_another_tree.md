# Lecture 87: Identical Trees (LeetCode 100) & Subtree of Another Tree (LeetCode 572)

> **One-Line Purpose:** Establish structural and value equivalence recursively and evaluate subtree isomorphism.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #87  
> **Video ID:** `tumW7jsjv68`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=tumW7jsjv68)  
> **Duration:** 23:28  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Master the fundamental recursive pattern to check if two trees are structurally and strictly identical.
- Extend tree equivalence to solve the "Subtree of Another Tree" problem.
- Understand the nested recursion time complexity $O(N \times M)$ and why it happens.

## 🧠 Core Intuition — Why This Works
**Identical Trees (`isSameTree`):**
Two trees are identical if and only if:
1. The roots have the same value.
2. The left subtrees are identical.
3. The right subtrees are identical.
This is a pure structural definition that maps perfectly to recursion. The base case is when both are null (identical), or only one is null (not identical).

**Subtree of Another Tree (`isSubtree`):**
A tree `S` is a subtree of `T` if:
1. `T` is identical to `S`.
2. OR `S` is a subtree of `T`'s left child.
3. OR `S` is a subtree of `T`'s right child.
We just apply our `isSameTree` function at every single node of `T`.

**Visualization:**
```text
Tree T:       Tree S:
     3           4
    / \         / \
   4   5       1   2
  / \
 1   2
```
At node 3 in `T`, `isSameTree(3, 4)` is false.
Go left to node 4 in `T`, `isSameTree(4, 4)` is true! Match found.

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Are these trees the same?" / "Symmetric" / "Subtree" / "Pattern matching in trees" → **Simultaneous tree traversal (`isSameTree`)**.
- Comparing structures of two graphs/trees.

## 📐 Algorithm Walk-Through
**For `isSameTree(p, q)`:**
1. Base cases: If both `p` and `q` are null, return `true`. If one is null and the other isn't, return `false`.
2. Value check: If `p->val != q->val`, return `false`.
3. Recursive step: Return `isSameTree(p->left, q->left) && isSameTree(p->right, q->right)`.

**For `isSubtree(root, subRoot)`:**
1. Base cases: If `subRoot` is null, it's always a subtree, return `true`.
2. If `root` is null (but `subRoot` isn't), return `false`.
3. Identity check: If `isSameTree(root, subRoot)` is true, return `true`.
4. Recursive step: Return `isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot)`.

## 🔵 Complete C++ Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionTreeComparison {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p && !q) return true;
        if (!p || !q) return false;
        if (p->val != q->val) return false;

        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }

    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!subRoot) return true;
        if (!root) return false;

        if (isSameTree(root, subRoot)) return true;

        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
};
```

## 🔍 Dry Run Trace
**Running `isSubtree(T, S)` on the visual above:**
1. `isSubtree(3, 4)`:
   - `isSameTree(3, 4)` -> values `3 != 4`, returns `false`.
   - Proceeds to `isSubtree(3->left (4), 4) || isSubtree(3->right (5), 4)`.
2. First part: `isSubtree(4, 4)`:
   - `isSameTree(4, 4)`:
     - values match. 
     - lefts: `isSameTree(1, 1)` -> values match, null children match.
     - rights: `isSameTree(2, 2)` -> values match, null children match.
     - returns `true`.
3. `isSubtree(4, 4)` returns `true`.
4. The `||` short-circuits. Overall result is `true`.

## ⚠️ Common Interview Mistakes
- **Confusing Base Cases in `isSameTree`:** Writing `if(p == q) return true;` — this checks if they are the exact same memory address, not if they have equivalent structures. You must use `!p && !q`.
- **Order of Base Cases in `isSubtree`:** If you check `if(!root)` before `if(!subRoot)`, you will fail the case where both are null. Null is technically a subtree of null.
- **Assuming $O(N)$ Time for Subtree:** Forgetting that for every node in `root` (size $N$), you potentially do a full `isSameTree` comparison with `subRoot` (size $M$). This makes the worst-case time complexity $O(N \times M)$.

## 📊 Complexity Analysis
- **`isSameTree`:**
  - **Time Complexity:** $O(\min(N, M))$ where $N$ and $M$ are the sizes of the two trees. We only compare up to the size of the smaller tree.
  - **Space Complexity:** $O(\min(H_1, H_2))$ for the recursion stack.
- **`isSubtree`:**
  - **Time Complexity:** $O(N \times M)$ worst-case. E.g., `T` is a left-skewed tree of all 1s, and `S` is also a left-skewed tree of all 1s but slightly shorter. We check almost the full length of `S` at every node of `T`.
  - **Space Complexity:** $O(N)$ for the recursion stack of `isSubtree` in the worst case (skewed `T`).

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] Can `isSubtree` be solved in better than $O(N \times M)$ time?
**Answer:** Yes. We can serialize both trees into strings using a preorder traversal (with null markers, e.g., `#` for nulls). Then, `S` is a subtree of `T` if the string of `S` is a substring of the string of `T`. Substring search can be done in $O(N+M)$ time using the KMP algorithm. Another advanced $O(N+M)$ approach is Merkle Hashing of subtrees.

### Q2: [Output Prediction] What if `subRoot` is empty (null)?
**Answer:** The empty tree is formally a subtree of every tree (including the empty tree). The first base case `if (!subRoot) return true;` handles this perfectly.

### Q3: [Variant] How would you check if a tree is Symmetric? (Leetcode 101)
**Answer:** A tree is symmetric if its left subtree is a mirror of its right subtree. We can write an `isMirror(node1, node2)` function which is almost identical to `isSameTree`, but we compare `node1->left` with `node2->right`, and `node1->right` with `node2->left`.

### Q4: [Edge Case] In `isSameTree`, why can't we just do `return p->val == q->val && isSameTree(...)` without the null checks?
**Answer:** Because `p->val` will throw a Null Pointer Exception / Segfault if `p` is null. The null checks act as both the termination condition for the recursion and the protection against dereferencing null pointers.

## 🏆 Related Problems (Leetcode)
- **Leetcode 100:** Same Tree (Easy)
- **Leetcode 572:** Subtree of Another Tree (Easy)
- **Leetcode 101:** Symmetric Tree (Easy) - *Direct variant of Same Tree*
- **Leetcode 250:** Count Univalue Subtrees (Medium)

## 🔗 Cross-Topic Connections
- **String Matching:** The $O(N \times M)$ worst case here is identical to the naive substring search algorithm. Using KMP brings both down to $O(N+M)$.
- **Hashing:** Tree hashing (Merkle trees) is often used in distributed systems (like Git or Cassandra) to quickly verify if huge directory trees or data structures are identical without $O(N \times M)$ comparisons.

## ⚡ 2-Minute Revision Flash Card
- **isSameTree:** Compare `root`, then recurse `(p->L, q->L)` AND `(p->R, q->R)`.
- **isSameTree Base Cases:** `(!p && !q) -> true`, `(!p || !q) -> false`.
- **isSubtree:** Check `isSameTree(root, subRoot)`. If false, recurse `isSubtree(root->L, subRoot)` OR `isSubtree(root->R, subRoot)`.
- **Performance:** Subtree check is $O(N \times M)$ naive, but can be optimized to $O(N + M)$ with Serialization + KMP substring search.
