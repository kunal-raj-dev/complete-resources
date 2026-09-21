# Lecture 110: Inorder Predecessor & Successor in BST

> **One-Line Purpose:** Find the immediate predecessor and successor of a given key in a BST in $O(H)$ time and $O(1)$ auxiliary memory.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #110  
> **Video ID:** `IHNkql1tAnk`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=IHNkql1tAnk)  
> **Duration:** 19:50  
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

void findPreSuc(TreeNode* root, TreeNode*& pre, TreeNode*& suc, int key) {
    TreeNode* curr = root;

    // Find Successor: smallest key strictly greater than key
    while (curr) {
        if (curr->val > key) {
            suc = curr;
            curr = curr->left;
        } else {
            curr = curr->right;
        }
    }

    curr = root;
    // Find Predecessor: largest key strictly smaller than key
    while (curr) {
        if (curr->val < key) {
            pre = curr;
            curr = curr->right;
        } else {
            curr = curr->left;
        }
    }
}
```
- **Time Complexity:** $O(H)$.
- **Space Complexity:** $O(1)$.
