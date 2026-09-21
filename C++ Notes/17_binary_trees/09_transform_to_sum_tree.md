# Lecture 93: Transform to Sum Tree

> **One-Line Purpose:** Mutate a binary tree in-place so each node stores the sum of all nodes in its subtrees, returning original total value.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #93  
> **Video ID:** `TY6kEejJEM0`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=TY6kEejJEM0)  
> **Duration:** 08:41  
> **Status:** AUDITED  

---

## 🔵 Complete Implementation

```cpp
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int toSumTree(TreeNode* root) {
    if (!root) return 0;

    int oldVal = root->val;

    int leftSum = toSumTree(root->left);
    int rightSum = toSumTree(root->right);

    root->val = leftSum + rightSum;

    return oldVal + root->val;
}
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$.
