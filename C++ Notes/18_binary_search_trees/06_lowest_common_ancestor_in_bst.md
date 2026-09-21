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
- **Time Complexity:** $O(H)$.
- **Space Complexity:** $O(1)$ strictly.
