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
- **Time Complexity:** `isSameTree`: $O(\min(N, M))$. `isSubtree`: $O(N \times M)$ worst-case.
