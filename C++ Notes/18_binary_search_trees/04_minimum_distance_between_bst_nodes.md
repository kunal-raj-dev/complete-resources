# Lecture 101: Minimum Absolute Difference in BST (LeetCode 783)

> **One-Line Purpose:** Find minimum distance between any two BST nodes using state-preserving inorder traversal.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #101  
> **Video ID:** `WZmjRXF_Zi4`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=WZmjRXF_Zi4)  
> **Duration:** 14:16  
> **Status:** AUDITED  

---

## 🎯 Learning Objectives
- Leverage the most important property of a BST: **Inorder traversal yields elements in strictly increasing order**.
- Understand how to maintain state (`prev` pointer) across recursive calls to compare adjacent elements.
- Solve the problem in $O(N)$ time without using extra space to store the traversal array.

## 🧠 Core Intuition — Why This Works
The minimum absolute difference between *any* two nodes in a BST must occur between two nodes that are **adjacent in sorted order**. 
Why? Because if we have a sorted sequence $A < B < C$, the difference $|A - B|$ or $|B - C|$ will always be smaller than or equal to $|A - C|$.
Since an inorder traversal of a BST gives us the nodes in sorted order, we don't need to compare every node with every other node ($O(N^2)$). We just need to do an inorder traversal and compare each node with the **previously visited node** ($O(N)$).

**Visualization:**
```text
Tree:
      4
     / \
    2   6
   / \
  1   3

Inorder: 1 -> 2 -> 3 -> 4 -> 6
Differences:
|2-1| = 1
|3-2| = 1
|4-3| = 1
|6-4| = 2
Minimum difference is 1.
```

## 🎯 Pattern Recognition — When to Use This
**Trigger cues:**
- "Minimum difference between two nodes in a BST"
- "Adjacent elements in a BST"
- "Validate BST"
→ **Action:** Use an Inorder Traversal and keep track of a `prev` node pointer.

## 📐 Algorithm Walk-Through
1. Initialize a global or class-level `minDiff` to `INT_MAX` and a `prev` pointer to `nullptr`.
2. Perform a standard Inorder Traversal:
   - **Left:** Recurse left (`inorder(root->left)`).
   - **Process Node:** If `prev` is not null, calculate `root->val - prev->val` and update `minDiff` if it's smaller.
   - **Update Prev:** Set `prev = root`.
   - **Right:** Recurse right (`inorder(root->right)`).
3. Return `minDiff`.

## 💻 Complete C++ Implementation

```cpp
#include <algorithm>
#include <climits>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class SolutionMinDiff {
private:
    int minDiff = INT_MAX;
    TreeNode* prev = nullptr;

    void inorder(TreeNode* root) {
        if (!root) return;

        inorder(root->left);

        if (prev) {
            minDiff = min(minDiff, root->val - prev->val);
        }
        prev = root;

        inorder(root->right);
    }

public:
    int minDiffInBST(TreeNode* root) {
        minDiff = INT_MAX;
        prev = nullptr;
        inorder(root);
        return minDiff;
    }
};
```

## 🔍 Dry Run Trace
**Tree:** `[4, 2, 6, 1, 3]`
- Start `minDiff = INT_MAX`, `prev = nullptr`
- Reach `1` (leftmost):
  - `prev` is null.
  - `prev` becomes `1`.
- Go back up to `2`:
  - `prev` is `1`. Diff = `2 - 1 = 1`. `minDiff = min(INT_MAX, 1) = 1`.
  - `prev` becomes `2`.
- Go to right child `3`:
  - `prev` is `2`. Diff = `3 - 2 = 1`. `minDiff = min(1, 1) = 1`.
  - `prev` becomes `3`.
- Go back up to `4`:
  - `prev` is `3`. Diff = `4 - 3 = 1`. `minDiff = min(1, 1) = 1`.
  - `prev` becomes `4`.
- Go to right child `6`:
  - `prev` is `4`. Diff = `6 - 4 = 2`. `minDiff = min(1, 2) = 1`.
  - `prev` becomes `6`.
- **Result:** `1`.

## ⚠️ Common Interview Mistakes
- **Storing the entire inorder traversal in an array:** While correct, this uses $O(N)$ extra space. Interviewers expect the $O(1)$ space optimization (ignoring the recursion stack).
- **Forgetting to reset class variables:** If the `minDiffInBST` function is called multiple times on the same object, `minDiff` and `prev` will carry over from the previous run if not explicitly reset at the start of the function.
- **Using absolute value:** Since inorder guarantees `root->val > prev->val`, you don't actually need `abs(root->val - prev->val)`, just subtraction is fine.

## 📊 Complexity Analysis
- **Time Complexity:** $O(N)$ since we visit every node exactly once.
- **Space Complexity:** $O(H)$ where $H$ is the height of the tree, representing the recursion stack. $O(\log N)$ for balanced trees, $O(N)$ worst-case for skewed trees.

## 🔥 Interview Q&A — Google / Amazon Level
### Q1: [Optimization] Can we stop early if we find a difference of 0?
**Answer:** Yes! If the tree can contain duplicate values (though standard BSTs usually don't), a difference of 0 is the absolute minimum possible. You can add `if (minDiff == 0) return;` to prune the rest of the traversal.

### Q2: [Alternative Approach] How would you solve this if you were NOT allowed to use recursion?
**Answer:** I would use an iterative inorder traversal using an explicit `stack<TreeNode*>`. The logic for `prev` and `minDiff` remains exactly the same, placed right after popping a node from the stack.

### Q3: [Follow-up] What if the tree was just a regular Binary Tree, not a BST?
**Answer:** In a regular binary tree, inorder traversal does not guarantee sorted order. We would have to traverse the tree, store all values in an array, sort the array, and then find the minimum adjacent difference. Time complexity would increase to $O(N \log N)$.

### Q4: [State Management] Why do we need `prev` as a pointer or a class member instead of passing it as a function parameter?
**Answer:** If we pass `prev` by value, the updated `prev` from the left subtree won't be reflected when the recursion unwinds to the parent. We *could* pass it as a reference to a pointer (`TreeNode*& prev`), but using a class member is often cleaner in C++.

### Q5: [Constraint Checking] What if the tree has only one node?
**Answer:** The problem usually constrains the tree to have at least 2 nodes. If it had 1, `prev` would remain null or the difference would never be calculated, and we'd return `INT_MAX`.

## 🏆 Related Problems (Leetcode)
- **Leetcode 530:** Minimum Absolute Difference in BST (Exact same problem as 783)
- **Leetcode 98:** Validate Binary Search Tree (Uses the same `prev` pointer technique)
- **Leetcode 230:** Kth Smallest Element in a BST (Inorder traversal pattern)

## 🔗 Cross-Topic Connections
- **Arrays & Sorting:** Finding the minimum difference between elements in an array requires sorting first. The BST gives us the "sorted" property for free.

## ⚡ 2-Minute Revision Flash Card
- **Pattern:** Any problem asking about sequence or order in a BST $\rightarrow$ **Inorder Traversal**.
- **Trick:** Minimum difference must be between adjacent elements in sorted order.
- **Implementation:** Track `TreeNode* prev`. At current node: `minDiff = min(minDiff, curr - prev)`. Update `prev = curr`.
- **Time/Space:** $O(N)$ Time, $O(H)$ Space (recursion stack).
