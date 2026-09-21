# Lecture 86: Height & Count of Nodes in Binary Tree

> **One-Line Purpose:** Formulate bottom-up recursive reductions to compute tree height, total node count, and node sum in $O(N)$ time.

---

## 📌 Source Metadata
> **Source:** YouTube Playlist (Complete C++ DSA Course | Apna College)  
> **Instructor:** Shradha Khapra  
> **Lecture:** #86  
> **Video ID:** `7tzHzN_Ehus`  
> **Video URL:** [Watch on YouTube](https://www.youtube.com/watch?v=7tzHzN_Ehus)  
> **Duration:** 23:09  
> **Status:** AUDITED  

---

## 🔵 Complete C++ Implementation

```cpp
#include <algorithm>
#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

int height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(height(root->left), height(root->right));
}

int countNodes(TreeNode* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int sumOfNodes(TreeNode* root) {
    if (!root) return 0;
    return root->val + sumOfNodes(root->left) + sumOfNodes(root->right);
}
```
- **Time Complexity:** $O(N)$.
- **Space Complexity:** $O(H)$ stack space.
