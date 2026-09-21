# Lecture 100: Validate Binary Search Tree (LeetCode 98)

> **One-Line Purpose:** Verify if a binary tree satisfies the strict Binary Search Tree invariant across all subtrees by propagating $(-\infty, +\infty)$ range bounds in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #100  
> **Video ID:** `dSBcCynP1nA`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=dSBcCynP1nA)  
> **Duration:** 12:41  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Master the strict property of a Binary Search Tree across all descendants, not just immediate children.
- Learn the "Range Propagation" (min/max bounds) technique to validate trees top-down in $O(N)$ time.
- Understand how to handle integer boundary conditions (`INT_MAX`/`INT_MIN`) using larger data types (`long long`) or pointers.

## 🧠 Core Intuition — Why This Works
The biggest trap when validating a BST is assuming that if every parent is greater than its left child and less than its right child, the tree is a valid BST.
**This is FALSE.**
In a valid BST, *every* node in the right subtree must be greater than the root, not just the right child.

**Visualization of the Trap:**
```text
      5
     / \
    1   6
       / \
      3   7
```
Here, `3 < 6` (left child of 6 is valid locally), and `7 > 6` (right child of 6 is valid locally). However, `3` is in the right subtree of `5`, meaning it MUST be greater than `5`. Since `3 < 5`, this is an **Invalid BST**.

**The Solution:**
We pass down a valid **range** `(min, max)` for every node.
- The root can be anything: `(-∞, +∞)`.
- When going **left**, the upper bound updates to the parent's value: `(-∞, 5)`.
- When going **right**, the lower bound updates to the parent's value: `(5, +∞)`.
If a node's value falls outside its inherited range, the tree is invalid.

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Validate / Is this a valid BST?" → **Range propagation (min/max)** or **Inorder traversal validation**.
- "Check if a tree satisfies a global property" → **Top-down bound passing**.

## 📐 Algorithm Walk-Through
1. Create a helper function `validate(node, min_val, max_val)`.
2. **Base case:** If `node` is null, it's valid (return `true`).
3. **Current Node Check:** If `node->val <= min_val` OR `node->val >= max_val`, return `false`. (Equality is false because BSTs usually don't allow duplicates).
4. **Recursive Step:**
   - Check left subtree: `validate(node->left, min_val, node->val)` (max becomes current node's value).
   - Check right subtree: `validate(node->right, node->val, max_val)` (min becomes current node's value).
5. Return true only if both left and right subtree checks return true.

## 💻 Complete C++ Implementation

```cpp
#include <climits>
#include <iostream>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionValidateBST {
private:
    bool validate(TreeNode* node, long long minVal, long long maxVal) {
        if (!node) return true;

        if (node->val <= minVal || node->val >= maxVal) {
            return false;
        }

        return validate(node->left, minVal, node->val) &&
               validate(node->right, node->val, maxVal);
    }

public:
    bool isValidBST(TreeNode* root) {
        return validate(root, LLONG_MIN, LLONG_MAX);
    }
};

int main() {
    TreeNode* root = new TreeNode(2);
    root->left = new TreeNode(1);
    root->right = new TreeNode(3);

    SolutionValidateBST solver;
    cout << "Is Valid BST: " << (solver.isValidBST(root) ? "YES" : "NO") << endl; // Output: YES
    return 0;
}
```

## 🔍 Dry Run Trace
**Validating the trapped tree:**
```text
      5
     / \
    1   6
       / \
      3   7
```
1. `validate(5, -∞, +∞)`:
   - `-∞ < 5 < +∞` (Valid)
   - Left call: `validate(1, -∞, 5)`
   - Right call: `validate(6, 5, +∞)`
2. `validate(1, -∞, 5)`:
   - `-∞ < 1 < 5` (Valid)
   - Left/Right both null, return `true`.
3. `validate(6, 5, +∞)`:
   - `5 < 6 < +∞` (Valid)
   - Left call: `validate(3, 5, 6)`
   - Right call: `validate(7, 6, +∞)`
4. `validate(3, 5, 6)`:
   - Check: `3 <= 5` ? **YES**. 
   - **Returns `false`.** (3 violates the lower bound of 5 inherited from the root).
5. Right call from 5 receives `false`, root returns `false`. Tree is invalid!

## ⚠️ Common Interview Mistakes
- **The Local-Only Check:** Checking only `root->left->val < root->val < root->right->val`. This is an instant interview fail.
- **Integer Overflow:** Using `INT_MAX` and `INT_MIN` for the initial bounds, and then testing a tree that actually contains the value `INT_MAX`. `node->val >= max_val` will trigger incorrectly. Always use `LLONG_MIN` and `LLONG_MAX` (or `LONG_MIN`/`LONG_MAX` in Java) or pass bounds as pointers (`TreeNode* minNode, TreeNode* maxNode`) which can be null.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$. We visit every node exactly once in the worst case (when the tree is valid).
- **Space Complexity:** $O(H)$ where $H$ is the height of the tree. This is for the recursive call stack. In the worst case (skewed tree), it's $O(N)$. In a balanced tree, it's $O(\log N)$.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Conceptual] How could you validate the BST without passing min/max ranges down?
**Answer:** By doing an Inorder Traversal. An inorder traversal of a valid BST must yield a strictly increasing sequence. We can just keep track of the `previous` node visited during the traversal. If at any point `current->val <= previous->val`, the tree is invalid. This also runs in $O(N)$ time and $O(H)$ space.

### Q2: [Edge Case] How do you handle a tree that contains nodes with the value `LLONG_MAX`?
**Answer:** The `long long` trick fails if the tree can literally contain a 64-bit max integer. The safest, most robust way in C++ is to pass pointers to the bounding nodes instead of raw values: `bool validate(TreeNode* node, TreeNode* minNode, TreeNode* maxNode)`. Then check: `if (minNode && node->val <= minNode->val) return false;`. `nullptr` represents infinity.

### Q3: [Variant] What if the BST allows duplicate values?
**Answer:** The problem definition must specify where duplicates go. If duplicates go to the left, the invariant changes to $\text{Left} \le \text{Root} < \text{Right}$. We would change the bounds check to: `node->val < min_val` (allow equality) and `node->val >= max_val`.

### Q4: [Performance] Which is faster in practice: Range propagation or Inorder Traversal?
**Answer:** Range propagation is often slightly faster in practice because it can short-circuit and prune entire branches instantly if a bound is violated high up in the tree. Inorder traversal (without a full array) also short-circuits, but might visit more nodes deep in the left subtree before catching a right-subtree violation.

## 🏆 Related Problems (Leetcode)
- **Leetcode 98:** Validate Binary Search Tree (Medium)
- **Leetcode 501:** Find Mode in Binary Search Tree (Easy) - *Good practice for Inorder tracking*
- **Leetcode 99:** Recover Binary Search Tree (Medium) - *Next step: fix the invalid BST!*

## 🔗 Cross-Topic Connections
- **Tree Traversals:** The alternative Inorder strategy directly relies on understanding DFS Tree Traversals.
- **Divide & Conquer:** The min/max passing is a form of divide and conquer, independently verifying the left and right halves with strict constraints.

## ⚡ 2-Minute Revision Flash Card
- **Trap:** `left < root < right` is NOT enough. Left subtree max must be `< root`.
- **Top-Down Range:** Pass `(min, max)` bounds downwards.
- **Updates:** Go Left $\rightarrow$ Update max to `root->val`. Go Right $\rightarrow$ Update min to `root->val`.
- **Overflow Safe:** Use `long long` for infinity, or use `TreeNode*` pointers for bounds.
- **Alternative:** Inorder traversal keeping a `prev` pointer (must be strictly increasing).
