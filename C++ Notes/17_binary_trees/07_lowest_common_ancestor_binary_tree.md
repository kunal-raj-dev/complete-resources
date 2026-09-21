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
