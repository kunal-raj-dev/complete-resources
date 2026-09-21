# Lecture 107: Largest BST in Binary Tree

> **One-Line Purpose:** Find the size of the largest valid BST subtree embedded within a binary tree in optimal $O(N)$ single-pass bottom-up post-order time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #107  
> **Video ID:** `Pr-HFxp7npk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=Pr-HFxp7npk)  
> **Duration:** 24:56  
> **Status:** AUDITED  

---

## 1. 🧱 Prerequisite Concepts
Before diving into this problem, you need a solid grasp of:
- **Binary Search Tree (BST) Properties:** Left subtree contains nodes smaller than the root, and right subtree contains nodes greater than the root.
- **Tree Traversals:** Specifically, **Post-Order Traversal** (Left, Right, Root) is crucial here. We need to evaluate the children before deciding the fate of the parent node.
- **Recursion Trust:** Trusting your recursive calls to bring back exact information from subtrees.

## 2. 🧠 Core Concept & Explanation
Imagine you're inspecting a tree from the bottom up. To prove a tree rooted at `node X` is a valid BST, you don't need to traverse its entire subtrees again. You just need a few pieces of information from its left and right subtrees:
1. Are the left and right subtrees valid BSTs themselves?
2. What is the **maximum** value in the left subtree? (It must be strictly less than `X.val`)
3. What is the **minimum** value in the right subtree? (It must be strictly greater than `X.val`)

If all these conditions hold true, congratulations! The tree at `node X` is a BST. Its size will simply be: `1 + size_of_left_BST + size_of_right_BST`. If it fails, the largest BST is simply the maximum size found in either the left or right subtrees so far. 

This requires us to pass a custom "information package" up the recursive tree!

## 3. 🚶‍♂️ Step-by-step Approach (Algorithm)
1. **Define a Custom Data Structure:** We need a struct `SubtreeInfo` that stores 4 things: `isBST` (boolean), `size` (int), `minVal` (int), and `maxVal` (int).
2. **Base Case (Null Node):** An empty tree is mathematically a valid BST of size 0. Return `{true, 0, INT_MAX, INT_MIN}`. (Why `INT_MAX` for min and `INT_MIN` for max? So that any parent node will easily be greater than `INT_MIN` and smaller than `INT_MAX`, making it always valid!).
3. **Recursive Calls:** Ask the left child and right child for their `SubtreeInfo`.
4. **Current Node Processing:** 
   - Check the BST condition for the current node.
   - If valid: Calculate the new `minVal` (left's min, or root's val if no left child) and `maxVal` (right's max, or root's val if no right child). Return `true` and the aggregated size.
   - If invalid: Return `false`, and pass up the `max` of left or right BST sizes. Reset `min` and `max` to dummy values since this subtree can no longer form a larger BST upwards.

## 4. 🔍 Dry Run / Execution Trace
Let's trace a small tree:
```text
       10
      /  \
     5    15
    / \     \
   1   8     7 (Invalidates right side)
```
- **Node 1:** Leaf. Returns `{true, 1, 1, 1}`.
- **Node 8:** Leaf. Returns `{true, 1, 8, 8}`.
- **Node 5:** Left is BST (max=1). Right is BST (min=8). 1 < 5 < 8. Valid! Returns `{true, 3, 1, 8}`.
- **Node 7:** Leaf. Returns `{true, 1, 7, 7}`.
- **Node 15:** Left is null `{true, 0, INF, -INF}`. Right is BST (min=7). Is 15 < 7? No! Invalid BST. Returns `{false, max(0, 1)=1, 0, 0}`.
- **Node 10 (Root):** Left is BST (size 3, max=8). Right is NOT a BST (size 1). Thus, Node 10 is NOT a BST. Returns `{false, max(3, 1)=3, 0, 0}`.
**Final Answer:** 3.

## 5. 💻 Complete C++ Implementation

```cpp
#include <climits>
#include <algorithm>
#include <iostream>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

struct SubtreeInfo {
    bool isBST;
    int size;
    int minVal;
    int maxVal;
};

class SolutionLargestBST {
private:
    SubtreeInfo postOrder(TreeNode* root) {
        // Base case: empty tree is a valid BST of size 0
        if (!root) {
            return {true, 0, INT_MAX, INT_MIN};
        }

        auto left = postOrder(root->left);
        auto right = postOrder(root->right);

        // Check BST condition for current root
        if (left.isBST && right.isBST && root->val > left.maxVal && root->val < right.minVal) {
            int currentMin = (root->left) ? left.minVal : root->val;
            int currentMax = (root->right) ? right.maxVal : root->val;
            return {true, 1 + left.size + right.size, currentMin, currentMax};
        }

        // Not a BST rooted at current node
        return {false, max(left.size, right.size), 0, 0};
    }

public:
    int largestBSTSubtree(TreeNode* root) {
        return postOrder(root).size;
    }
};

int main() {
    TreeNode* root = new TreeNode(10);
    root->left = new TreeNode(5);
    root->right = new TreeNode(15);
    root->left->left = new TreeNode(1);
    root->left->right = new TreeNode(8);
    root->right->right = new TreeNode(7); // Breaks BST on right side

    SolutionLargestBST solver;
    cout << "Largest BST Size: " << solver.largestBSTSubtree(root) << endl; // Output: 3 (subtree at 5: 1, 5, 8)
    return 0;
}
```

## 6. ⏱️ Complexity Analysis
- **Time Complexity:** $O(N)$. We visit each node exactly once in a post-order fashion. The operations at each node (checking max/min and size) take $O(1)$ time. This is optimal.
- **Space Complexity:** $O(H)$ where $H$ is the height of the binary tree. This space is strictly due to the recursive call stack. In the worst-case (skewed tree), it can be $O(N)$, but typically $O(\log N)$ for balanced trees.

## 7. ⚠️ Edge Cases to Consider
- **Empty Tree:** Should gracefully return size `0`.
- **Single Node Tree:** Should return size `1`.
- **Tree where all nodes have negative values:** Initialization of `INT_MAX` and `INT_MIN` protects against boundary value bugs.
- **All Left-Skewed or Right-Skewed valid BST:** Must recursively sum sizes correctly.

## 8. ❌ Common Pitfalls & Mistakes
- **Top-Down Approach (The $O(N^2)$ trap):** Beginners often write a function `isBST(node)` taking $O(N)$ and call it for every node in the tree (another $O(N)$), resulting in an inefficient $O(N^2)$ algorithm. **Always think bottom-up for tree optimizations!**
- **Incorrect Min/Max Initialization:** Returning `0` instead of `INT_MAX`/`INT_MIN` for null nodes. If you return `0`, a valid BST with negative numbers might suddenly be evaluated as invalid!
- **Not passing minimums up correctly:** `currentMin` must be `left.minVal`, not `left.val`. `left.val` is not necessarily the smallest item in the left subtree!

## 🎯 Pattern Recognition — When to Use This
- **Trigger Cues:** "Find the largest subtree that satisfies a condition", "Return the size/root of a valid sub-structure within a larger invalid structure".
- **Why Bottom-Up Post-Order?** Any problem asking to evaluate a parent node based on properties of its *entire left and right subtrees* requires a bottom-up approach (Post-Order traversal). Passing a custom struct/object up from children to parents prevents redundant $O(N^2)$ top-down scanning.

## 🏆 Related Problems (Leetcode)
- **Leetcode 333. Largest BST Subtree:** The exact problem discussed in this lecture.
- **Leetcode 98. Validate Binary Search Tree:** A simpler version of this problem that only returns true/false without computing subtree sizes.
- **Leetcode 1373. Maximum Sum BST in Binary Tree:** A harder variant where, instead of size, you must return the maximum *sum* of nodes in a valid BST subtree. Uses the exact same `SubtreeInfo` approach.

## 🔗 Cross-Topic Connections
- **Dynamic Programming on Trees:** This bottom-up state passing is effectively Tree DP. The struct represents the DP state of the subtree.
- **Post-Order Traversal:** The fundamental recursive mechanism enabling bottom-up evaluation.

## 9. 💡 Expert Q&A / Interview Follow-ups
**Q1: How would you modify this if we need to return the *root* of the largest BST instead of just its size?**  
*Answer:* We would add a `TreeNode* largestBSTRoot` inside the `SubtreeInfo` structure, or maintain a global pointer that updates whenever we find a valid BST with a size strictly greater than our previously recorded maximum.

**Q2: Does this approach handle duplicate values well?**  
*Answer:* As written, the condition `root->val > left.maxVal && root->val < right.minVal` strictly prohibits duplicates (meaning `[2, 2, 2]` is not a valid BST). If duplicates are allowed on the left/right, we just adjust the inequality signs (e.g., `>=` or `<=`).

**Q3: Can we use global variables instead of returning a struct?**  
*Answer:* You can use a global `maxSize`, but you *must* return the struct to pass `minVal`, `maxVal`, and `isBST` up the recursion chain. Global variables fail for subproblem state management in recursive tree merges.

**Q4: Why initialize `minVal = INT_MAX` and `maxVal = INT_MIN` for a null node?**
*Answer:* We want a null node to be universally valid as a child. When a leaf node checks `root->val > left.maxVal`, if `left` is null, `left.maxVal` being `INT_MIN` mathematically guarantees the inequality `root->val > INT_MIN` evaluates to true. It is a brilliant mathematical trick to avoid writing verbose `if (!left)` checks.

**Q5: What is the Time Complexity if we used a top-down `isBST` approach instead of bottom-up?**
*Answer:* $O(N^2)$. At the root, `isBST` takes $O(N)$ to scan all nodes. If the root fails, we call `isBST` on left and right children, taking $O(N-1)$. For a completely skewed tree, this evaluates to $N + (N-1) + (N-2) ... = O(N^2)$ time.

**Q6: What happens if tree node values can actually be `INT_MIN` or `INT_MAX`?**
*Answer:* The initial values for the empty tree struct would collide with actual node values, causing incorrect validation. To fix this, we should use `LONG_MAX` and `LONG_MIN` (using `long long` in C++), or use pointers/optionals to represent "infinity".

## ⚡ 2-Minute Revision Flash Card
- **Goal:** Find the size of the largest valid BST hidden inside an invalid binary tree.
- **Pattern:** Bottom-Up Post-Order Traversal (Tree DP).
- **Subtree State:** Return `{isBST, size, minVal, maxVal}`.
- **Null Base Case:** Return `{true, 0, INT_MAX, INT_MIN}` to automatically satisfy parent inequalities.
- **Complexity:** $O(N)$ Time, $O(H)$ Stack Space.
